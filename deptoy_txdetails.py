#!/usr/bin/env python3
"""Fetch details on the 7 direct pivot→scammer transactions and check timing."""
import json, time, requests, datetime

MEMPOOL = "https://mempool.space/api"
PIVOT   = "3JMjHDTJjKPnrvS7DycPAgYcA6HrHRk8UG"
SCAMMER = "3GH4EhMi1MG8rxSiAWqfoiUCMLaWPTCxuy"

CACHE_FILE = "deptoy_cache.json"
try:
    cache = json.load(open(CACHE_FILE))
except FileNotFoundError:
    cache = {}

def save_cache():
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f)

def get(url):
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

# Load the deptoy_link.json results
link = json.load(open("deptoy_link.json"))
direct_txs = link["direct_to_scammer"]

print(f"{'='*70}")
print(f"7 DIRECT TRANSACTIONS: PIVOT → SCAMMER")
print(f"{'='*70}")
print(f"Pivot  : {PIVOT}")
print(f"Scammer: {SCAMMER}")
print()

total = 0
for entry in direct_txs:
    txid = entry["txid"]
    btc  = entry["btc"]
    ts   = entry["time"]
    dt   = datetime.datetime.utcfromtimestamp(ts).strftime("%Y-%m-%d %H:%M UTC") if ts else "unconfirmed"
    total += btc
    print(f"  {txid}")
    print(f"    Amount: {btc:.6f} BTC")
    print(f"    Date  : {dt}")

    # Fetch full tx
    tx = get(f"{MEMPOOL}/tx/{txid}")
    if tx:
        # Find all inputs
        print(f"    Inputs:")
        input_addrs = []
        for inp in tx.get("vin", []):
            src = inp.get("prevout", {}).get("scriptpubkey_address", "unknown")
            val = inp.get("prevout", {}).get("value", 0) / 1e8
            input_addrs.append((src, val))
            flag = " ← PIVOT" if src == PIVOT else ""
            print(f"      {src}  {val:.6f} BTC{flag}")
        # Find outputs
        print(f"    Outputs:")
        for out in tx.get("vout", []):
            dst = out.get("scriptpubkey_address", "unknown")
            val = out.get("value", 0) / 1e8
            flag = " ← SCAMMER" if dst == SCAMMER else ""
            print(f"      {dst}  {val:.6f} BTC{flag}")
    print()
    time.sleep(0.5)

print(f"Total PIVOT → SCAMMER: {total:.4f} BTC")
print()

# Now look at the 4 Binance→Pivot txs
print(f"{'='*70}")
print(f"BINANCE → PIVOT TRANSACTIONS (top funder: bc1qm34lsc65zpw79lxes69...)")
print(f"{'='*70}")
BINANCE = "bc1qm34lsc65zpw79lxes69zkqmk6ee3ewf0j77s3h"

# Load the cached pivot txs to find Binance→Pivot
pivot_txs_raw = get(f"{MEMPOOL}/address/{PIVOT}/txs")
if pivot_txs_raw:
    binance_to_pivot = []
    for tx in pivot_txs_raw:
        for inp in tx.get("vin", []):
            if inp.get("prevout", {}).get("scriptpubkey_address") == BINANCE:
                ts = tx.get("status", {}).get("block_time", 0)
                dt = datetime.datetime.utcfromtimestamp(ts).strftime("%Y-%m-%d") if ts else "?"
                total_in = sum(o["value"] for o in tx.get("vout", [])
                              if o.get("scriptpubkey_address") == PIVOT) / 1e8
                binance_to_pivot.append((tx["txid"], total_in, dt))
                break

    print(f"  Found {len(binance_to_pivot)} txs where Binance funds PIVOT:")
    for txid, btc, dt in binance_to_pivot:
        print(f"    {txid[:40]}… {btc:.4f} BTC  {dt}")

# Pull the list of ALL addresses that sent to pivot (not just top 20)
print(f"\n{'='*70}")
print(f"ALL UNIQUE INPUT ADDRESSES TO PIVOT (from 200 sampled txs)")
print(f"{'='*70}")

deptoy_cache = json.load(open("deptoy_cache.json"))
# Find the pivot txs in cache
pivot_url = f"{MEMPOOL}/address/{PIVOT}/txs"
pivot_txs_all = []
# Collect from all paged results in cache
for url, data in deptoy_cache.items():
    if f"address/{PIVOT}/txs" in url and isinstance(data, list):
        pivot_txs_all.extend(data)

# Deduplicate by txid
seen = set()
unique_txs = []
for tx in pivot_txs_all:
    if tx["txid"] not in seen:
        seen.add(tx["txid"])
        unique_txs.append(tx)

print(f"  Total unique txs available: {len(unique_txs)}")

# Get all addresses that sent to pivot
from collections import defaultdict
pivot_receivers = defaultdict(float)  # addresses that RECEIVED from pivot
pivot_senders   = defaultdict(float)  # addresses that SENT to pivot

for tx in unique_txs:
    # determine if pivot is input or output
    pivot_in_inputs = any(
        inp.get("prevout", {}).get("scriptpubkey_address") == PIVOT
        for inp in tx.get("vin", [])
    )
    pivot_in_outputs = any(
        out.get("scriptpubkey_address") == PIVOT
        for out in tx.get("vout", [])
    )

    if pivot_in_outputs and not pivot_in_inputs:
        # Pivot is receiving: record senders
        for inp in tx.get("vin", []):
            src = inp.get("prevout", {}).get("scriptpubkey_address")
            val = inp.get("prevout", {}).get("value", 0) / 1e8
            if src and src != PIVOT:
                pivot_senders[src] += val

print(f"\n  Top 30 addresses sending TO PIVOT:")
for addr, btc in sorted(pivot_senders.items(), key=lambda x: -x[1])[:30]:
    print(f"    {addr}  {btc:.4f} BTC")

# Save comprehensive results
results = {
    "direct_txs_detail": [
        {"txid": e["txid"], "btc": e["btc"], "time": e["time"]}
        for e in direct_txs
    ],
    "total_direct_to_scammer_btc": total,
    "pivot_top_senders": dict(sorted(pivot_senders.items(), key=lambda x: -x[1])[:50])
}
with open("deptoy_link_v2.json", "w") as f:
    json.dump(results, f, indent=2)

print(f"\nSaved to deptoy_link_v2.json")
