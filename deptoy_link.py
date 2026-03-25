#!/usr/bin/env python3
"""
Investigate 3JMjHDTJjKPnrvS7DycPAgYcA6HrHRk8UG as potential deptoy.co hot wallet
and link it back to the original scammer address 3GH4EhMi1MG8rxSiAWqfoiUCMLaWPTCxuy
"""
import json, time, requests, sys
from collections import defaultdict

SCAMMER = "3GH4EhMi1MG8rxSiAWqfoiUCMLaWPTCxuy"
PIVOT    = "3JMjHDTJjKPnrvS7DycPAgYcA6HrHRk8UG"   # dominant input src found in hop-2

MEMPOOL  = "https://mempool.space/api"
BLOCKSTR = "https://blockstream.info/api"

CACHE_FILE = "deptoy_cache.json"
try:
    cache = json.load(open(CACHE_FILE))
except FileNotFoundError:
    cache = {}

def save_cache():
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f)

def get(url, label=""):
    if url in cache:
        return cache[url]
    for attempt in range(5):
        try:
            r = requests.get(url, timeout=30)
            if r.status_code == 429:
                wait = 30 * (attempt + 1)
                print(f"    [rate-limit] sleeping {wait}s …")
                time.sleep(wait)
                continue
            if r.status_code == 200:
                data = r.json()
                cache[url] = data
                save_cache()
                return data
            print(f"  HTTP {r.status_code} for {url}")
            return None
        except Exception as e:
            print(f"  Error: {e}")
            time.sleep(10)
    return None

def get_addr_txs_paged(addr, max_txs=500):
    """Fetch all transactions for an address using mempool.space paging."""
    txs = []
    last_seen = None
    while True:
        if last_seen:
            url = f"{MEMPOOL}/address/{addr}/txs?after_txid={last_seen}"
        else:
            url = f"{MEMPOOL}/address/{addr}/txs"
        batch = get(url)
        if not batch:
            break
        txs.extend(batch)
        print(f"  Fetched {len(txs)} txs for {addr[:20]}…")
        if len(batch) < 25:
            break
        last_seen = batch[-1]["txid"]
        if len(txs) >= max_txs:
            print(f"  Capped at {max_txs}")
            break
        time.sleep(1)
    return txs

def addr_stats(addr):
    url = f"{MEMPOOL}/address/{addr}"
    return get(url)

# ── Step 1: confirm PIVOT → SCAMMER flow ─────────────────────────────────────
print(f"\n{'='*60}")
print(f"PIVOT address: {PIVOT}")
print(f"{'='*60}")

stats = addr_stats(PIVOT)
if stats:
    chain = stats.get("chain_stats", {})
    mem   = stats.get("mempool_stats", {})
    total_recv = (chain.get("funded_txo_sum", 0) + mem.get("funded_txo_sum", 0)) / 1e8
    total_sent = (chain.get("spent_txo_sum", 0) + mem.get("spent_txo_sum", 0)) / 1e8
    total_txs  = chain.get("tx_count", 0)
    balance    = total_recv - total_sent
    print(f"  Total received : {total_recv:,.4f} BTC")
    print(f"  Total sent     : {total_sent:,.4f} BTC")
    print(f"  Balance        : {balance:,.4f} BTC")
    print(f"  Tx count       : {total_txs:,}")

# ── Step 2: Fetch recent txs from pivot and find direct sends to scammer ──────
print(f"\nFetching recent transactions from pivot address …")
pivot_txs = get_addr_txs_paged(PIVOT, max_txs=200)

direct_to_scammer = []
scammer_amounts = []

for tx in pivot_txs:
    txid = tx["txid"]
    block_time = tx.get("status", {}).get("block_time", 0)
    # check if any output goes to scammer
    for out in tx.get("vout", []):
        if out.get("scriptpubkey_address") == SCAMMER:
            btc = out["value"] / 1e8
            direct_to_scammer.append({
                "txid": txid,
                "btc": btc,
                "time": block_time
            })
            scammer_amounts.append(btc)
            print(f"  DIRECT SEND TO SCAMMER: {txid[:20]}… {btc:.6f} BTC")

print(f"\nDirect sends from PIVOT → SCAMMER: {len(direct_to_scammer)}")
if scammer_amounts:
    print(f"  Total: {sum(scammer_amounts):.4f} BTC")

# ── Step 3: Who funds the pivot? (co-inputs in pivot's spending txs) ─────────
print(f"\nAnalyzing funding sources for PIVOT …")
pivot_funders = defaultdict(float)
pivot_funder_txs = defaultdict(list)

for tx in pivot_txs:
    txid = tx["txid"]
    # Check if pivot is an INPUT (spending from pivot)
    pivot_is_input = any(
        inp.get("prevout", {}).get("scriptpubkey_address") == PIVOT
        for inp in tx.get("vin", [])
    )
    if not pivot_is_input:
        # pivot is receiving; record who sends to it
        for inp in tx.get("vin", []):
            src = inp.get("prevout", {}).get("scriptpubkey_address")
            val = inp.get("prevout", {}).get("value", 0) / 1e8
            if src and src != PIVOT:
                pivot_funders[src] += val
                pivot_funder_txs[src].append(txid)

top_funders = sorted(pivot_funders.items(), key=lambda x: -x[1])[:20]
print(f"\nTop funding sources for PIVOT (addresses sending TO pivot):")
for addr, btc in top_funders:
    n = len(pivot_funder_txs[addr])
    print(f"  {addr}  {btc:.4f} BTC  ({n} txs)")

# ── Step 4: Cross-reference pivot funders against scammer's known inputs ──────
print(f"\nFetching scammer's inbound transactions to cross-reference …")
scammer_txs = get_addr_txs_paged(SCAMMER, max_txs=300)

scammer_input_addrs = defaultdict(float)
for tx in scammer_txs:
    # txs where scammer is recipient
    scammer_receives = any(
        out.get("scriptpubkey_address") == SCAMMER
        for out in tx.get("vout", [])
    )
    if scammer_receives:
        for inp in tx.get("vin", []):
            src = inp.get("prevout", {}).get("scriptpubkey_address")
            val = inp.get("prevout", {}).get("value", 0) / 1e8
            if src:
                scammer_input_addrs[src] += val

print(f"  Found {len(scammer_input_addrs)} unique input addresses to scammer")

# Find overlap between pivot funders and scammer inputs
funder_set = set(pivot_funders.keys())
scammer_input_set = set(scammer_input_addrs.keys())
overlap = funder_set & scammer_input_set

print(f"\nAddresses that fund BOTH pivot AND scammer directly:")
if overlap:
    for addr in sorted(overlap, key=lambda a: -(scammer_input_addrs[a] + pivot_funders[a])):
        print(f"  {addr}")
        print(f"    → to pivot  : {pivot_funders[addr]:.4f} BTC")
        print(f"    → to scammer: {scammer_input_addrs[addr]:.4f} BTC")
else:
    print("  None found in sampled transactions")

# ── Step 5: Check if pivot address appears in deptoy.co JS source ─────────────
print(f"\n{'='*60}")
print("Searching deptoy.co JS source for known addresses …")
print(f"{'='*60}")

import subprocess, os

js_file = "/home/me/deptoy/static/js/app.66bc9f716f39a8a33c06.js"
if os.path.exists(js_file):
    # Search for the pivot and scammer addresses
    for needle in [PIVOT, SCAMMER, "3JMjH", "3GH4E"]:
        result = subprocess.run(
            ["grep", "-o", f".{{0,30}}{needle}.{{0,30}}", js_file],
            capture_output=True, text=True
        )
        if result.stdout.strip():
            print(f"\n  Found '{needle}' in deptoy JS:")
            for line in result.stdout.strip().split("\n")[:5]:
                print(f"    {line}")
        else:
            print(f"  '{needle}' NOT found in deptoy JS")
else:
    print(f"  JS file not found at {js_file}")

# ── Step 6: Search deptoy.co for any BTC addresses (P2PKH, P2SH, bech32) ──────
print(f"\nExtracting all BTC addresses from deptoy.co JS source …")
if os.path.exists(js_file):
    import re
    with open(js_file, "r", errors="ignore") as f:
        js_content = f.read()

    # BTC address patterns
    p2pkh   = re.findall(r'\b[13][a-km-zA-HJ-NP-Z1-9]{25,34}\b', js_content)
    bech32  = re.findall(r'\bbc1[a-z0-9]{6,87}\b', js_content)

    all_addrs = list(set(p2pkh + bech32))
    print(f"  Found {len(all_addrs)} unique potential BTC addresses in JS")

    # Filter out obvious non-addresses (version hashes etc.)
    # BTC addresses are 26-34 chars for legacy, 42 or 62 for bech32
    btc_addrs = []
    for a in all_addrs:
        if a.startswith("bc1") and len(a) >= 26:
            btc_addrs.append(a)
        elif a[0] in "13" and 26 <= len(a) <= 34:
            btc_addrs.append(a)

    print(f"  After filtering: {len(btc_addrs)} valid BTC addresses")

    # Cross-check against scammer's known transaction graph
    known_scammer_addrs = set(scammer_input_addrs.keys())
    # Also load graph.json for more addresses
    try:
        graph = json.load(open("graph.json"))
        graph_addrs = set(n["id"] for n in graph.get("nodes", []))
        known_scammer_addrs |= graph_addrs
        print(f"  Loaded {len(graph_addrs)} addresses from graph.json")
    except:
        pass

    overlap_deptoy = set(btc_addrs) & known_scammer_addrs
    print(f"\n  BTC addresses in deptoy.co JS that appear in scammer graph: {len(overlap_deptoy)}")
    for a in overlap_deptoy:
        print(f"    {a}")

    print(f"\n  All BTC addresses found in deptoy.co JS:")
    for a in sorted(btc_addrs):
        in_graph = "*** IN SCAMMER GRAPH ***" if a in known_scammer_addrs else ""
        print(f"    {a}  {in_graph}")

    # Save for report
    deptoy_btc_addrs = btc_addrs
else:
    deptoy_btc_addrs = []
    print("  JS file not found")

# ── Step 7: Save results ───────────────────────────────────────────────────────
results = {
    "pivot_address": PIVOT,
    "pivot_stats": stats,
    "direct_to_scammer": direct_to_scammer,
    "top_funders": top_funders,
    "overlap_funders": list(overlap),
    "deptoy_btc_addresses": deptoy_btc_addrs,
    "deptoy_graph_overlap": list(overlap_deptoy) if 'overlap_deptoy' in dir() else []
}

with open("deptoy_link.json", "w") as f:
    json.dump(results, f, indent=2)

print(f"\n\nResults saved to deptoy_link.json")
print(f"{'='*60}")
print("SUMMARY")
print(f"{'='*60}")
print(f"  Pivot {PIVOT[:20]}… → scammer direct sends: {len(direct_to_scammer)}")
print(f"  deptoy.co JS BTC addresses: {len(deptoy_btc_addrs)}")
if 'overlap_deptoy' in dir():
    print(f"  Overlap with scammer graph : {len(overlap_deptoy)}")
