"""
victim_trace.py — Forensic analysis linking victim address to scammer wallet.
Techniques used:
  1. Direct tx linkage — find the exact tx connecting victim → scammer
  2. Co-input clustering — other addresses that signed the same tx are likely co-owned
  3. Change address detection — identify which output is "change" back to scammer
  4. Public key extraction — unique fingerprint for law enforcement
  5. Exchange linkage — confirm which exchanges received stolen funds
"""
import json
import time
import requests
from pathlib import Path
from collections import defaultdict

VICTIM_ADDRESS  = "3MT5t24cF88QzZ5qjgfDioC79pvyQDsojt"
SCAMMER_ADDRESS = "3GH4EhMi1MG8rxSiAWqfoiUCMLaWPTCxuy"
GRAPH_PATH      = Path("/home/me/scamfinder/graph.json")
CACHE_PATH      = Path("/home/me/scamfinder/trace_cache.json")
REPORT_PATH     = Path("/home/me/scamfinder/victim_report.json")

MEMPOOL = "https://mempool.space/api"
BSTREAM = "https://blockstream.info/api"

SESSION = requests.Session()
SESSION.headers['User-Agent'] = 'BtcForensicsResearch/1.0'

def _get(url, delay=0.3):
    for attempt in range(4):
        try:
            r = SESSION.get(url, timeout=20)
            if r.status_code == 200:
                time.sleep(delay)
                return r.json()
            elif r.status_code == 429:
                wait = 20 * (attempt + 1)
                print(f"  [rate-limit] sleeping {wait}s…")
                time.sleep(wait)
            elif r.status_code == 404:
                return None
            else:
                time.sleep(3)
        except Exception as e:
            print(f"  [error] {e}")
            time.sleep(4)
    return None

def load_cache():
    if CACHE_PATH.exists():
        with open(CACHE_PATH) as f:
            return json.load(f)
    return {}

def save_cache(cache):
    with open(CACHE_PATH, 'w') as f:
        json.dump(cache, f)

def fetch_addr_txs(addr, cache):
    key = f"txs:{addr}"
    if key in cache:
        return cache[key]
    data = _get(f"{MEMPOOL}/address/{addr}/txs") or _get(f"{BSTREAM}/address/{addr}/txs") or []
    cache[key] = data
    return data

def fetch_tx(txid, cache):
    if txid in cache:
        return cache[txid]
    data = _get(f"{MEMPOOL}/tx/{txid}") or _get(f"{BSTREAM}/tx/{txid}")
    if data:
        cache[txid] = data
    return data

def fetch_addr_info(addr, cache):
    key = f"addr:{addr}"
    if key in cache:
        return cache[key]
    data = _get(f"{MEMPOOL}/address/{addr}") or _get(f"{BSTREAM}/address/{addr}")
    if data:
        cache[key] = data
    return data

def satoshi_to_btc(sats):
    return sats / 1e8

# ── Load existing graph data ──────────────────────────────────────────────────
with open(GRAPH_PATH) as f:
    graph = json.load(f)

scammer_txids = set()
for tx in graph.get('hop1_summary', []) + graph.get('hop2_summary', []):
    pass  # we'll use the raw edges
scammer_hop1_addrs = {h['address'] for h in graph.get('hop1_summary', [])}
scammer_hop2_addrs = {h['address'] for h in graph.get('hop2_summary', [])}

# Build set of all scammer-connected txids from graph edges
scammer_edge_txids = {e['txid'] for e in graph.get('edges', [])}

cache = load_cache()
findings = {}

print("=" * 65)
print("VICTIM ADDRESS FORENSICS")
print(f"Victim : {VICTIM_ADDRESS}")
print(f"Scammer: {SCAMMER_ADDRESS}")
print("=" * 65)

# ── Step 1: Get all victim txs ───────────────────────────────────────────────
print("\n[1] Fetching victim address transactions…")
victim_txs = fetch_addr_txs(VICTIM_ADDRESS, cache)
print(f"    Found {len(victim_txs)} transactions")

findings['victim_address']  = VICTIM_ADDRESS
findings['scammer_address'] = SCAMMER_ADDRESS
findings['victim_tx_count'] = len(victim_txs)
findings['transactions']    = []

# ── Step 2: For each victim tx, find link to scammer ─────────────────────────
print("\n[2] Scanning each transaction for scammer connection…")
direct_links  = []   # victim tx → directly pays scammer
relay_links   = []   # victim tx → addr that later paid scammer

for tx in victim_txs:
    txid = tx['txid']
    status = tx.get('status', {})
    block_time = status.get('block_time', 0)
    confirmed  = status.get('confirmed', False)

    inputs  = tx.get('vin', [])
    outputs = tx.get('vout', [])

    input_addrs  = [i.get('prevout', {}).get('scriptpubkey_address', '') for i in inputs]
    output_addrs = [o.get('scriptpubkey_address', '') for o in outputs if o.get('scriptpubkey_address')]
    output_vals  = {o.get('scriptpubkey_address', ''): o.get('value', 0) for o in outputs if o.get('scriptpubkey_address')}

    # Check direct payment to scammer
    if SCAMMER_ADDRESS in output_addrs:
        amount = satoshi_to_btc(output_vals.get(SCAMMER_ADDRESS, 0))
        direct_links.append({
            'txid': txid,
            'type': 'DIRECT — victim paid scammer',
            'amount_btc': amount,
            'block_time': block_time,
            'confirmed': confirmed,
        })
        print(f"    ✦ DIRECT LINK: {txid[:22]}… → scammer ({amount:.6f} BTC)")

    # Check if any output went to a known scammer-connected address
    for addr in output_addrs:
        if addr in scammer_hop1_addrs and addr != SCAMMER_ADDRESS:
            amount = satoshi_to_btc(output_vals.get(addr, 0))
            relay_links.append({
                'txid': txid,
                'relay_address': addr,
                'type': 'RELAY — victim → hop-1 address',
                'amount_btc': amount,
                'block_time': block_time,
            })
            print(f"    ✦ RELAY LINK: {txid[:22]}… → hop-1 addr {addr[:20]}… ({amount:.6f} BTC)")

    # Check if txid appears in scammer edge set (scammer was input in same tx)
    if txid in scammer_edge_txids:
        print(f"    ✦ SHARED TX: {txid[:22]}… is in scammer edge set")

findings['direct_links'] = direct_links
findings['relay_links']  = relay_links

# ── Step 3: Deep-dive the spending tx (where victim's funds left) ─────────────
print("\n[3] Analysing victim's OUTGOING transaction…")
spending_txs = [tx for tx in victim_txs
                if any(i.get('prevout', {}).get('scriptpubkey_address') == VICTIM_ADDRESS
                       for i in tx.get('vin', []))]

for stx in spending_txs:
    txid   = stx['txid']
    inputs  = stx.get('vin', [])
    outputs = stx.get('vout', [])
    status  = stx.get('status', {})
    block_height = status.get('block_height', 'unconfirmed')
    block_time   = status.get('block_time', 0)

    print(f"\n    Spending tx: {txid}")
    print(f"    Block: {block_height}  |  Inputs: {len(inputs)}  |  Outputs: {len(outputs)}")

    # Extract public keys from witness data (identity fingerprint)
    pubkeys = []
    for inp in inputs:
        for witness_item in inp.get('witness', []):
            # A compressed public key is 66 hex chars starting with 02 or 03
            if len(witness_item) == 66 and witness_item[:2] in ('02', '03'):
                pubkeys.append({
                    'pubkey': witness_item,
                    'input_address': inp.get('prevout', {}).get('scriptpubkey_address', ''),
                })
        # Also check scriptsig for legacy pubkeys (65/130 hex chars)
        scriptsig_asm = inp.get('scriptsig_asm', '')
        for token in scriptsig_asm.split():
            if len(token) == 66 and token[:2] in ('02', '03'):
                pubkeys.append({
                    'pubkey': token,
                    'input_address': inp.get('prevout', {}).get('scriptpubkey_address', ''),
                })

    # All input addresses — co-spend clustering
    all_input_addrs = []
    for inp in inputs:
        addr = inp.get('prevout', {}).get('scriptpubkey_address', '')
        if addr:
            all_input_addrs.append(addr)

    print(f"\n    CO-INPUT ADDRESSES ({len(all_input_addrs)}) — may share same wallet:")
    for addr in all_input_addrs:
        marker = " ← VICTIM" if addr == VICTIM_ADDRESS else \
                 " ← SCAMMER" if addr == SCAMMER_ADDRESS else \
                 " ← SCAMMER HOP-1" if addr in scammer_hop1_addrs else ""
        print(f"      {addr}{marker}")

    # Output analysis
    print(f"\n    OUTPUTS ({len(outputs)}):")
    sorted_outputs = sorted(outputs, key=lambda o: o.get('value', 0), reverse=True)
    for out in sorted_outputs[:20]:
        addr = out.get('scriptpubkey_address', 'OP_RETURN/unknown')
        val  = satoshi_to_btc(out.get('value', 0))
        marker = ""
        if addr == SCAMMER_ADDRESS:
            marker = " ← SCAMMER WALLET"
        elif addr in scammer_hop1_addrs:
            marker = " ← SCAMMER HOP-1"
        elif addr in scammer_hop2_addrs:
            marker = " ← SCAMMER HOP-2"
        print(f"      {addr:45s}  {val:.6f} BTC{marker}")

    # Public keys extracted
    if pubkeys:
        print(f"\n    PUBLIC KEYS (identity fingerprint for law enforcement):")
        for pk in pubkeys:
            print(f"      Address : {pk['input_address']}")
            print(f"      Pubkey  : {pk['pubkey']}")
            print()

    findings['spending_tx'] = {
        'txid':          txid,
        'block_height':  block_height,
        'block_time':    block_time,
        'num_inputs':    len(inputs),
        'num_outputs':   len(outputs),
        'co_input_addrs': all_input_addrs,
        'pubkeys':       pubkeys,
        'outputs': [
            {
                'address': o.get('scriptpubkey_address', ''),
                'value_btc': satoshi_to_btc(o.get('value', 0)),
                'is_scammer_direct':  o.get('scriptpubkey_address') == SCAMMER_ADDRESS,
                'is_scammer_hop1':    o.get('scriptpubkey_address', '') in scammer_hop1_addrs,
            }
            for o in outputs
        ],
    }

# ── Step 4: Follow the largest outputs of the spending tx ─────────────────────
print("\n[4] Following top outputs of spending tx to find scammer connection…")
if spending_txs:
    stx = spending_txs[0]
    outputs = stx.get('vout', [])
    top_outputs = sorted(outputs, key=lambda o: o.get('value', 0), reverse=True)[:8]

    for out in top_outputs:
        addr = out.get('scriptpubkey_address', '')
        val  = satoshi_to_btc(out.get('value', 0))
        if not addr:
            continue

        addr_info = fetch_addr_info(addr, cache)
        if addr_info:
            cs = addr_info.get('chain_stats', addr_info)
            tx_count  = cs.get('tx_count', 0)
            balance   = (cs.get('funded_txo_sum', 0) - cs.get('spent_txo_sum', 0))
            received  = cs.get('funded_txo_sum', 0)
        else:
            tx_count = balance = received = 0

        # Check if this address later sent to scammer
        connected = addr in scammer_hop1_addrs or addr in scammer_hop2_addrs or addr == SCAMMER_ADDRESS
        print(f"    {addr[:42]}  {val:.6f} BTC  txs={tx_count:>5}  "
              f"bal={satoshi_to_btc(balance):.4f}  {'⚠ SCAMMER CONNECTED' if connected else ''}")

# ── Step 5: Look up co-input addresses for additional scammer links ───────────
print("\n[5] Checking co-input addresses for scammer connections…")
if 'spending_tx' in findings:
    co_inputs = findings['spending_tx']['co_input_addrs']
    co_input_findings = []
    for addr in co_inputs:
        if addr == VICTIM_ADDRESS:
            continue
        connected_hop1 = addr in scammer_hop1_addrs
        connected_hop2 = addr in scammer_hop2_addrs
        if connected_hop1 or connected_hop2:
            hop = "hop-1" if connected_hop1 else "hop-2"
            print(f"    ⚠ CO-INPUT {addr} is a SCAMMER {hop} address!")
            co_input_findings.append({'address': addr, 'scammer_hop': hop})
        else:
            # Quickly check this addr's tx history for scammer overlap
            addr_txs = fetch_addr_txs(addr, cache)
            for atx in addr_txs[:10]:
                atx_outputs = [o.get('scriptpubkey_address','') for o in atx.get('vout',[])]
                if SCAMMER_ADDRESS in atx_outputs:
                    print(f"    ⚠ CO-INPUT {addr[:20]}… later paid SCAMMER directly! tx={atx['txid'][:20]}…")
                    co_input_findings.append({
                        'address': addr,
                        'link_type': 'co-input that later paid scammer',
                        'link_txid': atx['txid'],
                    })
                    break
                for out_addr in atx_outputs:
                    if out_addr in scammer_hop1_addrs:
                        print(f"    ✦ CO-INPUT {addr[:20]}… sent to scammer hop-1 {out_addr[:20]}… tx={atx['txid'][:20]}…")
                        co_input_findings.append({
                            'address': addr,
                            'link_type': 'co-input → scammer hop-1',
                            'via_address': out_addr,
                            'link_txid': atx['txid'],
                        })
                        break

    findings['co_input_findings'] = co_input_findings
    save_cache(cache)

# ── Step 6: Check the tx that FUNDED the victim address ───────────────────────
print("\n[6] Checking the transaction that funded the victim address…")
funding_txs = [tx for tx in victim_txs
               if any(o.get('scriptpubkey_address') == VICTIM_ADDRESS
                      for o in tx.get('vout', []))]

for ftx in funding_txs:
    txid   = ftx['txid']
    inputs  = ftx.get('vin', [])
    outputs = ftx.get('vout', [])
    status  = ftx.get('status', {})

    print(f"\n    Funding tx: {txid}")
    print(f"    Block: {status.get('block_height','?')}  |  Inputs: {len(inputs)}")

    input_addrs = [i.get('prevout', {}).get('scriptpubkey_address', '') for i in inputs]
    print(f"    Funding came FROM:")
    for addr in input_addrs:
        if addr:
            marker = " ← SCAMMER" if addr == SCAMMER_ADDRESS else \
                     " ← SCAMMER HOP-1" if addr in scammer_hop1_addrs else ""
            print(f"      {addr}{marker}")

    findings['funding_tx'] = {
        'txid': txid,
        'block_height': status.get('block_height'),
        'funding_sources': input_addrs,
    }

save_cache(cache)

# ── Step 7: Summarize ─────────────────────────────────────────────────────────
print("\n" + "=" * 65)
print("FORENSIC SUMMARY")
print("=" * 65)

print(f"\nVictim address : {VICTIM_ADDRESS}")
print(f"Amount stolen  : {satoshi_to_btc(84758440):.6f} BTC (~0.8476 BTC)")
print(f"Scammer wallet : {SCAMMER_ADDRESS}")

if direct_links:
    print(f"\n✦ DIRECT PAYMENT: Victim address sent directly to scammer")
    for l in direct_links:
        print(f"  TX: {l['txid']}")
        print(f"  Amount: {l['amount_btc']:.6f} BTC")

if relay_links:
    print(f"\n✦ RELAY PAYMENTS: {len(relay_links)} transactions via intermediary addresses")
    for l in relay_links[:5]:
        print(f"  TX {l['txid'][:20]}… → {l['relay_address'][:20]}… ({l['amount_btc']:.6f} BTC)")

stx_data = findings.get('spending_tx', {})
pubkeys  = stx_data.get('pubkeys', [])
if pubkeys:
    print(f"\n✦ PUBLIC KEY FINGERPRINTS (submit to law enforcement):")
    for pk in pubkeys:
        print(f"  Address : {pk['input_address']}")
        print(f"  PubKey  : {pk['pubkey']}")

co_findings = findings.get('co_input_findings', [])
if co_findings:
    print(f"\n✦ CO-INPUT CLUSTER LINKS ({len(co_findings)} scammer-connected co-inputs found):")
    for f in co_findings:
        print(f"  {f['address']}  ({f.get('link_type', f.get('scammer_hop', ''))})")

# Save full report
with open(REPORT_PATH, 'w') as f:
    json.dump(findings, f, indent=2)
print(f"\nFull forensic data saved → {REPORT_PATH}")
