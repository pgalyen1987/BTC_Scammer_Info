"""
chain_tracer.py — Deep Bitcoin transaction tracer.
Hop 1: fetch all txids touching target address, map outputs.
Hop 2: for top destination addresses, follow their outbound txs one more level.
Uses mempool.space + blockstream.info public APIs with caching.
"""
import json
import time
import sys
import requests
from pathlib import Path
from collections import defaultdict

TRANSACTIONS_PATH = Path("/home/me/scamfinder/transactions.json")
TRACE_CACHE_PATH  = Path("/home/me/scamfinder/trace_cache.json")
GRAPH_PATH        = Path("/home/me/scamfinder/graph.json")

MEMPOOL_BASE     = "https://mempool.space/api"
BLOCKSTREAM_BASE = "https://blockstream.info/api"

# ── Known exchange / service addresses (public threat-intel / OSINT sources) ──
KNOWN_ENTITIES: dict[str, str] = {
    # Binance
    "34xp4vRoCGJym3xR7yCVPFHoCNxv4Twseo": "Binance (cold)",
    "1NDyJtNTjmwk5xPNhjgAMu4HDHigtobu1s": "Binance",
    "3QCsHKpEWjCBwSAqFaRY7TxNuEMwHgGODf": "Binance",
    "1HBtApAFA9B2YZw3G2YKSMCtb3dVnjuNe2": "Binance",
    "bc1qm34lsc65zpw79lxes69zkqmk6ee3ewf0j77s3h": "Binance",
    "1LQoWist8KkaUXSPKZHNvEyfrEkPHzSsCd": "Binance",
    "3M219KR5vEneNb47ewrPfWyb5jQ2DjxRP6": "Binance",
    # Coinbase
    "3Cbq7aT1tY8kMxWLbkRc7nMNGFDGqbEPQk": "Coinbase",
    "3AfP9N7LqDkVsPHgELXyACpBr8buDpAGJB": "Coinbase",
    "1GR9qNz7zgtaW5HwwVpEJWMnGWhsbsieCG": "Coinbase",
    "bc1qazcm763858nkj2dj986etajv6wquslv8uxwczt": "Coinbase",
    "1K4t2vSBSS2xFjZ6PofYnbgZewjeqbG1uM": "Coinbase",
    "3Kgcah8pWzb2QNQHdBZKbBbdxLKSf3FGJF": "Coinbase",
    "3QJmV3qfvL9SuYo34YihAoFph2d5nCJbE": "Coinbase",
    # Kraken
    "1FzWLkAahHooV3kzTgyx6qsswXJ6sCXkSR": "Kraken",
    "1Jb1yDnKTKAmrSvDDe9TXn9CWHLRXQ9Tqm": "Kraken",
    "3FupZp77ySr7jwoLYEJ9Rx5h7D4Y6PCI9h": "Kraken",
    "3H5JTt42K7RmZtromfTSefcMEFMMe18pMD": "Kraken",
    # OKX / OKCoin
    "3FHNBLobJnbCPujPDZLBqmynKzeMM3LswQ": "OKX",
    "3LCGsSmfr24demGvriN4e3ft8wEcDuHFqh": "OKX",
    "1Hf3B2HGm9kVMmGQnPCGMpMQmtPULmniJL": "OKX",
    # Huobi / HTX
    "1HckjUpRGcrrRAtFaaCAUaGjsPx9oYmLaZ": "Huobi/HTX",
    "1LdRcdxfbSnmCYYNdeYpUnztiYzVfBEQeC": "Huobi/HTX",
    "3HqAe9LtNBjnsfM4CyYaWTnvCaUYT7v4oZ": "Huobi/HTX",
    # Bitfinex
    "1KYiKJEfdJtap9QX2v9BXJMpz2SfU4pgZw": "Bitfinex",
    "12cgpFdJViXbwHbhrA3TuW1EGnL25Zqc3P": "Bitfinex",
    "3D2oetdNuZUqQHPJmcMDDHYoqkyNVsFk9r": "Bitfinex (cold)",
    "3JZq4atEAaEy5bpRqPBLBdSXpBz76CsFmk": "Bitfinex",
    # Bitstamp
    "3LDjAUJH7cFbFgFzqmpX56YB2dN2AEPG73": "Bitstamp",
    "3NLmGo2b3aTG4PfyxjPvVaMBWBaM58sARK": "Bitstamp",
    "3E35SFZkfLMGo4qX5aVs1bBDSnAuGgBTs3": "Bitstamp",
    # Gemini
    "393fP7PBmMpjxEBJSbM8VSnP6ABCFP9bUL": "Gemini",
    "3Jm1WMFAEuVm5A7sH7z5REjnkQ5RKicGN4": "Gemini",
    # KuCoin
    "3Em2BHJ3gAMuHCdWMtR5aouJgaF6biBwbE": "KuCoin",
    "1NNgM1QMBQTTuGAbH8jGSjHAFM4MWAcLXu": "KuCoin",
    # Bybit
    "3Bm3cdEcGfxBMJPfxStKuSbv3Bm3CnCfM7": "Bybit",
    # Gate.io
    "15mHRnsBzGVcrAKufGuxKyWuQmNuNY9bnA": "Gate.io",
    "3B4jyVbACq8P3KCCtEQdS2jXeEKGnNSAT6": "Gate.io",
    # Bitmex
    "3BMEXqGpG4FxBA1KWhRFufXfSTRgzfDBhJ": "BitMEX",
    "3AH3jPSLF67PBa7Q8HuMFvBDPxXhHt97Js": "BitMEX",
    # Crypto.com
    "3LYJfcfHmXLQcarwgthtzGjbUdPotw6gYD": "Crypto.com",
    # Paxos / itBit
    "38UmuUqPCrFmQo4khkomlemcx5sDTGtg1a": "Paxos/itBit",
    # Lightning Network related
    "3Hpyd3dLPqfnFfmGkZBKFWkBGiT7c3J74A": "Lightning (likely)",
    # Wasabi mixer heuristic — pay-to-taproot txs with many equal outputs
    # (identified by pattern, not address)
    # Genesis / historical
    "1A1zP1eP5QGefi2DMPTfTL5SLmv7Divfna": "Genesis Block (Satoshi)",
    "1FeexV6bAHb8ybZjqQMjJrcCrHGW9sb6uF": "Patoshi/Early Miner",
}

# tx-count thresholds → entity classification
def classify_address(addr: str, tx_count: int = 0, balance_sat: int = 0,
                     received_sat: int = 0) -> str:
    if addr in KNOWN_ENTITIES:
        return KNOWN_ENTITIES[addr]
    # High volume strongly suggests an exchange hot wallet or custodian
    if tx_count >= 100_000:
        return "Exchange/Custodian (very high volume)"
    if tx_count >= 10_000:
        return "Exchange/Service (high volume)"
    if tx_count >= 1_000:
        return "Service/Pool (medium volume)"
    if tx_count >= 100:
        return "Active wallet (100+ txs)"
    # Dust balance with lots of received → likely swept (exchange deposit addr)
    if received_sat > 10_000_000 and balance_sat < 100_000:
        return "Swept deposit address (likely exchange)"
    return "Unknown"


# ── Cache helpers ─────────────────────────────────────────────────────────────

def load_cache() -> dict:
    if TRACE_CACHE_PATH.exists():
        with open(TRACE_CACHE_PATH) as f:
            return json.load(f)
    return {}

def save_cache(cache: dict):
    with open(TRACE_CACHE_PATH, 'w') as f:
        json.dump(cache, f)

# ── HTTP helpers ──────────────────────────────────────────────────────────────

SESSION = requests.Session()
SESSION.headers['User-Agent'] = 'BtcForensicsResearch/1.0'

def _get(url: str, delay: float = 0.25) -> dict | list | None:
    """GET with automatic retry and fallback."""
    for attempt in range(4):
        try:
            r = SESSION.get(url, timeout=20)
            if r.status_code == 200:
                time.sleep(delay)
                return r.json()
            elif r.status_code == 429:
                wait = 20 * (attempt + 1)
                print(f"    [rate-limit] sleeping {wait}s …", flush=True)
                time.sleep(wait)
            elif r.status_code == 404:
                return None
            else:
                time.sleep(3)
        except Exception as e:
            print(f"    [error] {e}", flush=True)
            time.sleep(4)
    return None


def fetch_tx(txid: str, cache: dict) -> dict | None:
    if txid in cache:
        return cache[txid]
    raw = _get(f"{MEMPOOL_BASE}/tx/{txid}")
    if raw is None:
        raw = _get(f"{BLOCKSTREAM_BASE}/tx/{txid}")
    if not raw or 'vout' not in raw:
        return None
    tx = {
        'txid': txid,
        'fee':  raw.get('fee', 0),
        'size': raw.get('size', 0),
        'outputs': [
            {'recipient': o['scriptpubkey_address'], 'value': o['value']}
            for o in raw.get('vout', []) if o.get('scriptpubkey_address')
        ],
        'inputs': [
            {'sender': i['prevout']['scriptpubkey_address'],
             'value':  i['prevout']['value']}
            for i in raw.get('vin', [])
            if i.get('prevout', {}).get('scriptpubkey_address')
        ],
    }
    cache[txid] = tx
    return tx


def fetch_addr(addr: str, cache: dict) -> dict | None:
    key = f"addr:{addr}"
    if key in cache:
        return cache[key]
    raw = _get(f"{MEMPOOL_BASE}/address/{addr}")
    if raw is None:
        raw = _get(f"{BLOCKSTREAM_BASE}/address/{addr}")
    if not raw:
        return None
    cs = raw.get('chain_stats', raw)  # mempool wraps in chain_stats
    result = {
        'tx_count':     cs.get('tx_count', 0),
        'funded_sat':   cs.get('funded_txo_sum', 0),
        'spent_sat':    cs.get('spent_txo_sum', 0),
        'balance_sat':  cs.get('funded_txo_sum', 0) - cs.get('spent_txo_sum', 0),
    }
    cache[key] = result
    return result


def fetch_addr_txids(addr: str, cache: dict, limit: int = 25) -> list[str]:
    """Return the most recent txids for an address (mempool.space)."""
    key = f"txids:{addr}"
    if key in cache:
        return cache[key]
    raw = _get(f"{MEMPOOL_BASE}/address/{addr}/txs")
    if not raw:
        raw = _get(f"{BLOCKSTREAM_BASE}/address/{addr}/txs")
    if not raw:
        return []
    txids = [t['txid'] for t in raw[:limit] if 'txid' in t]
    cache[key] = txids
    return txids


# ── Core tracer ───────────────────────────────────────────────────────────────

def trace(max_hop1: int = 504, hop2_top_n: int = 30, hop2_tx_limit: int = 10):
    """
    Hop 1 : fetch every unique txid from the PDF statement, map non-self outputs.
    Hop 2 : for the top hop2_top_n destination addresses, fetch their recent
             outbound txs and follow one more level.
    """
    with open(TRANSACTIONS_PATH) as f:
        data = json.load(f)

    address_info  = data['address_info']
    target        = address_info.get('address', '')
    all_txs       = data['transactions']

    # Unique txids (dedup; order = most-recent first from the PDF)
    seen_ids, unique_txs = set(), []
    for t in all_txs:
        if t['txid'] not in seen_ids:
            seen_ids.add(t['txid'])
            unique_txs.append(t)

    hop1_txs = unique_txs[:max_hop1]
    print(f"Target : {target}")
    print(f"Hop-1  : {len(hop1_txs)} unique txids to trace")

    cache = load_cache()

    # ── Hop 1 ────────────────────────────────────────────────────────────────
    nodes: dict[str, dict] = {
        target: {
            'id':    target,
            'label': f"TARGET\n{target[:14]}…",
            'type':  'target',
            'hop':   0,
            'total_received_btc': float(address_info.get('total_received_btc', 0)),
            'total_sent_btc':     float(address_info.get('total_sent_btc', 0)),
            'entity': 'TARGET (scammer wallet)',
        }
    }
    edges:    list[dict] = []
    hop1_dests: dict[str, dict] = defaultdict(
        lambda: {'total_btc': 0.0, 'tx_count': 0, 'txids': [], 'dates': []}
    )

    for i, tx in enumerate(hop1_txs):
        txid = tx['txid']
        pct  = f"{i+1}/{len(hop1_txs)}"
        if (i+1) % 25 == 0 or i == 0:
            print(f"  Hop-1 [{pct}] {txid[:22]}… {tx['date']}", flush=True)

        tx_data = fetch_tx(txid, cache)
        if not tx_data:
            continue

        for out in tx_data['outputs']:
            recv = out['recipient']
            if not recv or recv == target:
                continue
            val_btc = out['value'] / 1e8
            hop1_dests[recv]['total_btc']  += val_btc
            hop1_dests[recv]['tx_count']   += 1
            hop1_dests[recv]['txids'].append(txid)
            hop1_dests[recv]['dates'].append(tx['date'])
            edges.append({
                'from': target, 'to': recv,
                'amount_btc': val_btc, 'txid': txid,
                'date': tx['date'], 'hop': 1,
            })

        # Save cache every 50 txs
        if (i + 1) % 50 == 0:
            save_cache(cache)

    save_cache(cache)
    sorted_hop1 = sorted(hop1_dests.items(), key=lambda x: x[1]['total_btc'], reverse=True)
    print(f"\nHop-1 complete: {len(hop1_dests)} unique destination addresses found")

    # ── Fetch address metadata for ALL hop-1 destinations ────────────────────
    print(f"Fetching address metadata for {len(sorted_hop1)} hop-1 destinations …")
    for i, (addr, info) in enumerate(sorted_hop1):
        if (i+1) % 20 == 0:
            print(f"  addr metadata [{i+1}/{len(sorted_hop1)}]", flush=True)
        meta = fetch_addr(addr, cache)
        if meta:
            tx_count    = meta['tx_count']
            balance_sat = meta['balance_sat']
            recv_sat    = meta['funded_sat']
        else:
            tx_count = balance_sat = recv_sat = 0

        entity = classify_address(addr, tx_count, balance_sat, recv_sat)
        nodes[addr] = {
            'id':    addr,
            'label': f"{entity}\n{addr[:14]}…",
            'type':  'hop1',
            'hop':   1,
            'entity': entity,
            'total_btc_from_target': info['total_btc'],
            'tx_count_chain': tx_count,
            'balance_btc':    balance_sat / 1e8,
            'total_received_btc': recv_sat / 1e8,
        }

        if (i + 1) % 30 == 0:
            save_cache(cache)

    save_cache(cache)

    # ── Hop 2: follow top destinations one more level ─────────────────────────
    top_hop1 = sorted_hop1[:hop2_top_n]
    print(f"\nHop-2: tracing outbound txs from top {len(top_hop1)} hop-1 addresses …")

    hop2_dests: dict[str, dict] = defaultdict(
        lambda: {'total_btc': 0.0, 'tx_count': 0, 'txids': [], 'dates': [],
                 'via_addr': ''}
    )

    for j, (addr, info) in enumerate(top_hop1):
        print(f"  [{j+1}/{len(top_hop1)}] {addr[:22]}… "
              f"({info['total_btc']:.4f} BTC from target)", flush=True)

        txids_for_addr = fetch_addr_txids(addr, cache, limit=hop2_tx_limit)
        for txid in txids_for_addr:
            tx_data = fetch_tx(txid, cache)
            if not tx_data:
                continue

            # Only look at txs where this addr was a SENDER (input)
            senders = {inp['sender'] for inp in tx_data['inputs']}
            if addr not in senders:
                continue  # addr only received in this tx, skip

            for out in tx_data['outputs']:
                recv = out['recipient']
                if not recv or recv == addr or recv == target:
                    continue
                val_btc = out['value'] / 1e8
                hop2_dests[recv]['total_btc']  += val_btc
                hop2_dests[recv]['tx_count']   += 1
                hop2_dests[recv]['txids'].append(txid)
                hop2_dests[recv]['via_addr']    = addr
                edges.append({
                    'from': addr, 'to': recv,
                    'amount_btc': val_btc, 'txid': txid,
                    'date': '', 'hop': 2,
                })

        if (j + 1) % 10 == 0:
            save_cache(cache)

    save_cache(cache)
    sorted_hop2 = sorted(hop2_dests.items(), key=lambda x: x[1]['total_btc'], reverse=True)
    print(f"Hop-2 complete: {len(hop2_dests)} unique secondary destinations")

    # Fetch metadata for top hop-2 addresses
    print(f"Fetching metadata for top {min(50, len(sorted_hop2))} hop-2 addresses …")
    for i, (addr, info) in enumerate(sorted_hop2[:50]):
        if addr in nodes:
            continue  # already have it
        meta = fetch_addr(addr, cache)
        if meta:
            tx_count    = meta['tx_count']
            balance_sat = meta['balance_sat']
            recv_sat    = meta['funded_sat']
        else:
            tx_count = balance_sat = recv_sat = 0

        entity = classify_address(addr, tx_count, balance_sat, recv_sat)
        nodes[addr] = {
            'id':    addr,
            'label': f"{entity}\n{addr[:14]}…",
            'type':  'hop2',
            'hop':   2,
            'entity': entity,
            'total_btc_from_prev': info['total_btc'],
            'via_hop1_addr': info.get('via_addr', ''),
            'tx_count_chain': tx_count,
            'balance_btc':    balance_sat / 1e8,
            'total_received_btc': recv_sat / 1e8,
        }

    save_cache(cache)

    # ── Assemble final graph ──────────────────────────────────────────────────
    def _btc(n): return n.get('total_btc_from_target') or n.get('total_btc_from_prev') or 0

    graph = {
        'target_address': target,
        'address_info':   address_info,
        'nodes': list(nodes.values()),
        'edges': edges,
        'hop1_summary': [
            {
                'address':       addr,
                'total_btc':     info['total_btc'],
                'tx_count':      info['tx_count'],
                'dates':         sorted(set(info['dates'])),
                'entity':        nodes.get(addr, {}).get('entity', 'Unknown'),
                'chain_tx_count': nodes.get(addr, {}).get('tx_count_chain', 0),
                'balance_btc':   nodes.get(addr, {}).get('balance_btc', 0),
                'total_received_btc': nodes.get(addr, {}).get('total_received_btc', 0),
            }
            for addr, info in sorted_hop1
        ],
        'hop2_summary': [
            {
                'address':   addr,
                'total_btc': info['total_btc'],
                'tx_count':  info['tx_count'],
                'via_addr':  info.get('via_addr', ''),
                'entity':    nodes.get(addr, {}).get('entity', 'Unknown'),
                'chain_tx_count': nodes.get(addr, {}).get('tx_count_chain', 0),
                'balance_btc': nodes.get(addr, {}).get('balance_btc', 0),
            }
            for addr, info in sorted_hop2[:100]
        ],
    }

    with open(GRAPH_PATH, 'w') as f:
        json.dump(graph, f, indent=2)

    print(f"\nGraph saved → {GRAPH_PATH}")
    print(f"  Nodes  : {len(graph['nodes'])}")
    print(f"  Edges  : {len(graph['edges'])}")

    print("\n══ TOP HOP-1 DESTINATIONS ══")
    for e in graph['hop1_summary'][:20]:
        flag = " ⚠ EXCHANGE" if "Exchange" in e['entity'] or "Swept" in e['entity'] else ""
        print(f"  {e['address'][:22]}…  {e['total_btc']:10.4f} BTC  "
              f"txs={e['chain_tx_count']:>7,}  bal={e['balance_btc']:.4f}  "
              f"{e['entity']}{flag}")

    print("\n══ TOP HOP-2 DESTINATIONS ══")
    for e in graph['hop2_summary'][:15]:
        flag = " ⚠ EXCHANGE" if "Exchange" in e['entity'] or "Swept" in e['entity'] else ""
        print(f"  {e['address'][:22]}…  {e['total_btc']:10.4f} BTC  "
              f"txs={e['chain_tx_count']:>7,}  {e['entity']}{flag}")

    return graph


if __name__ == '__main__':
    max_hop1    = int(sys.argv[1]) if len(sys.argv) > 1 else 504
    hop2_top_n  = int(sys.argv[2]) if len(sys.argv) > 2 else 30
    hop2_tx_lim = int(sys.argv[3]) if len(sys.argv) > 3 else 10
    trace(max_hop1=max_hop1, hop2_top_n=hop2_top_n, hop2_tx_limit=hop2_tx_lim)
