"""
report.py — Generate an interactive HTML report with transaction graph visualization.
"""
import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict

GRAPH_PATH   = Path("/home/me/scamfinder/graph.json")
VICTIM_PATH  = Path("/home/me/scamfinder/victim_report.json")
TX_PATH      = Path("/home/me/scamfinder/transactions.json")
REPORT_PATH  = Path("/home/me/scamfinder/report-full.html")

ENTITY_OVERRIDE = {
    'Exchange': '#2ecc71', 'Coinbase': '#2ecc71', 'Binance': '#f1c40f',
    'Kraken': '#1abc9c',   'Bitfinex': '#e67e22', 'Huobi': '#e67e22',
    'OKX': '#e67e22',      'Bitstamp': '#1abc9c', 'Gemini': '#2ecc71',
    'KuCoin': '#e67e22',   'Bybit': '#e67e22',    'BitMEX': '#e74c3c',
    'Swept': '#27ae60',    'Service': '#f39c12',  'Pool': '#f39c12',
    'Active': '#95a5a6',
}
TYPE_COLOR = {'target': '#e74c3c', 'hop1': '#3498db', 'hop2': '#9b59b6'}

def badge_color(entity):
    for kw, col in ENTITY_OVERRIDE.items():
        if kw in entity:
            return col
    return '#95a5a6'

def node_color(node):
    entity = node.get('entity', '')
    for kw, col in ENTITY_OVERRIDE.items():
        if kw in entity:
            return col
    return TYPE_COLOR.get(node.get('type', 'hop1'), '#3498db')

def node_size(node):
    if node.get('type') == 'target': return 45
    btc = node.get('total_btc_from_target') or node.get('total_btc_from_prev') or 0
    return max(8, min(35, int(btc * 1.5 + 8)))

def is_exchange(entity):
    return any(k in entity for k in [
        'Exchange','Coinbase','Binance','Kraken','Bitfinex',
        'Huobi','OKX','Bitstamp','Gemini','KuCoin','Bybit','BitMEX','Swept'
    ])


def generate_report():
    with open(GRAPH_PATH) as f:
        graph = json.load(f)
    victim = json.loads(VICTIM_PATH.read_text()) if VICTIM_PATH.exists() else {}
    tx_data = json.loads(TX_PATH.read_text()) if TX_PATH.exists() else {}

    target     = graph['target_address']
    addr_info  = graph['address_info']
    hop1       = graph.get('hop1_summary', [])
    hop2       = graph.get('hop2_summary', [])
    nodes_raw  = graph['nodes']
    edges_raw  = graph['edges']
    all_txs    = tx_data.get('transactions', [])

    exchanges_found = [h for h in hop1 + hop2 if is_exchange(h.get('entity', ''))]
    high_vol        = [h for h in hop1 if h.get('chain_tx_count', 0) >= 1000
                       and not is_exchange(h.get('entity', ''))]
    total_btc_h1    = sum(h['total_btc'] for h in hop1)
    total_btc_h2    = sum(h.get('total_btc', 0) for h in hop2)
    generated_at    = datetime.now().strftime("%Y-%m-%d %H:%M UTC")

    # ── Activity timeline (monthly buckets) ───────────────────────────────────
    monthly = defaultdict(lambda: {'in': 0.0, 'out': 0.0, 'count': 0})
    for tx in all_txs:
        ym = tx['date'][:7]  # YYYY-MM
        if tx['direction'] == 'in':
            monthly[ym]['in'] += tx['amount_btc']
        else:
            monthly[ym]['out'] += tx['amount_btc']
        monthly[ym]['count'] += 1
    sorted_months = sorted(monthly.keys())
    first_seen = sorted_months[0] if sorted_months else 'unknown'
    last_seen  = sorted_months[-1] if sorted_months else 'unknown'
    peak_month = max(monthly, key=lambda m: monthly[m]['in']) if monthly else ''
    peak_btc   = monthly[peak_month]['in'] if peak_month else 0

    chart_labels = json.dumps(sorted_months)
    chart_in     = json.dumps([round(monthly[m]['in'], 4) for m in sorted_months])
    chart_out    = json.dumps([round(monthly[m]['out'], 4) for m in sorted_months])

    # ── Entity breakdown ──────────────────────────────────────────────────────
    entity_totals = defaultdict(float)
    for h in hop1:
        entity_totals[h.get('entity', 'Unknown')] += h['total_btc']
    entity_sorted = sorted(entity_totals.items(), key=lambda x: x[1], reverse=True)

    breakdown_labels = json.dumps([e for e, _ in entity_sorted[:10]])
    breakdown_vals   = json.dumps([round(v, 4) for _, v in entity_sorted[:10]])
    breakdown_colors = json.dumps([badge_color(e) for e, _ in entity_sorted[:10]])

    # ── Victim money trail ────────────────────────────────────────────────────
    stx      = victim.get('spending_tx', {})
    pubkeys  = stx.get('pubkeys', [])
    vtx_rows = ""
    for out in sorted(stx.get('outputs', []), key=lambda o: o['value_btc'], reverse=True)[:12]:
        addr  = out['address']
        val   = out['value_btc']
        flags = []
        if out.get('is_scammer_direct'):  flags.append('<span class="badge" style="background:#e74c3c">SCAMMER DIRECT</span>')
        if out.get('is_scammer_hop1'):    flags.append('<span class="badge" style="background:#f39c12">HOP-1</span>')
        vtx_rows += f"""<tr>
          <td style="font-family:monospace;font-size:11px"><a href="https://mempool.space/address/{addr}" target="_blank">{addr}</a></td>
          <td style="text-align:right">{val:.6f}</td>
          <td>{"".join(flags)}</td>
        </tr>"""

    # Victim loss figures — sourced from blockexplorer.one receipt generated 2025-02-17
    STOLEN_BTC         = 0.84758448   # exact from receipt input value
    STOLEN_SAT         = 84_758_448
    TX_FEE_BTC         = 0.00018993
    TX_FEE_SAT         = 18_993
    TX_FEE_USD         = 18.29        # from receipt (Feb 2025 prices)
    NET_SWEPT_BTC      = 0.84739455   # total outputs per receipt
    BTC_PRICE_THEFT    = 23_400       # approx BTC price on 2022-07-31
    BTC_PRICE_FEB25    = 96_284       # implied from receipt USD ($81,605.74 / 0.84758448)
    BTC_PRICE_NOW      = 95_000       # approx current
    USD_AT_THEFT       = STOLEN_BTC * BTC_PRICE_THEFT
    USD_RECEIPT        = 81_605.74    # from receipt — AT Feb 2025 prices, NOT theft-time
    USD_NOW            = STOLEN_BTC * BTC_PRICE_NOW
    funding_sources    = list(dict.fromkeys(victim.get('funding_tx', {}).get('funding_sources', [])))

    trail_html = ""
    if victim:
        pk_rows = "".join(
            f'<tr><td style="font-family:monospace;font-size:11px;word-break:break-all">{p["pubkey"]}</td>'
            f'<td style="font-family:monospace;font-size:11px"><a href="https://mempool.space/address/{p["input_address"]}" target="_blank">{p["input_address"]}</a></td></tr>'
            for p in pubkeys
        )
        funding_rows = "".join(
            f'<tr><td style="font-family:monospace;font-size:11px"><a href="https://mempool.space/address/{a}" target="_blank">{a}</a></td></tr>'
            for a in funding_sources
        )
        trail_html = f"""
<div class="section">
  <h2>Victim Forensics — Money Trail</h2>

  <!-- Loss summary cards -->
  <div style="display:flex;gap:12px;flex-wrap:wrap;margin-bottom:16px">
    <div class="card" style="border-color:#e74c3c">
      <div class="lbl">BTC Stolen (exact)</div>
      <div class="val" style="color:#e74c3c;font-size:22px">0.84758448</div>
      <div class="sub2">84,758,448 satoshis · full address balance</div>
    </div>
    <div class="card" style="border-color:#e74c3c">
      <div class="lbl">USD at Time of Theft</div>
      <div class="val" style="color:#ffa657;font-size:20px">${USD_AT_THEFT:,.0f}</div>
      <div class="sub2">BTC ≈ $23,400 · 2022-07-31 03:09 UTC</div>
    </div>
    <div class="card" style="border-color:#f1c40f">
      <div class="lbl">USD per Official Receipt</div>
      <div class="val" style="color:#f1c40f;font-size:20px">${USD_RECEIPT:,.2f}</div>
      <div class="sub2">blockexplorer.one receipt · Feb 2025 BTC price (~$96,284)</div>
    </div>
    <div class="card" style="border-color:#e74c3c">
      <div class="lbl">USD at Current Prices</div>
      <div class="val" style="color:#ffa657;font-size:20px">${USD_NOW:,.0f}</div>
      <div class="sub2">BTC ≈ $95,000 · {generated_at[:10]}</div>
    </div>
    <div class="card">
      <div class="lbl">Miner Fee Paid</div>
      <div class="val" style="font-size:16px">{TX_FEE_SAT:,} sat</div>
      <div class="sub2">{TX_FEE_BTC:.8f} BTC · ${TX_FEE_USD:.2f} USD</div>
    </div>
    <div class="card">
      <div class="lbl">Outputs in Sweep TX</div>
      <div class="val">{stx.get('num_outputs',0)}</div>
      <div class="sub2">funds fanned out immediately</div>
    </div>
    <div class="card">
      <div class="lbl">Change Returned</div>
      <div class="val" style="color:#e74c3c">$0.00</div>
      <div class="sub2">0 satoshis returned to victim</div>
    </div>
  </div>

  <div class="warn-box" style="margin-bottom:14px">
    <b>Sweep pattern:</b> The entire 0.84758448 BTC balance was drained in a single transaction with 1 input and {stx.get('num_outputs',0)} outputs at 2022-07-31 03:09:14 UTC. Zero change was returned. The funds were immediately fanned out across {stx.get('num_outputs',0)} addresses to complicate tracing — a standard scammer laundering technique. The largest single output (0.46 BTC) went to the relay address below.
  </div>
  <div class="info-box" style="margin-bottom:14px">
    <b>Receipt note:</b> The official blockexplorer.one transaction receipt (generated 2025-02-17) shows <b>$81,605.74 USD</b>. This figure uses the BTC price at receipt generation (~$96,284/BTC in Feb 2025), <i>not</i> the price at the time of the theft. At theft-date prices (BTC ≈ $23,400 on 2022-07-31) the loss was approximately <b>$19,833 USD</b>. Both figures are documented for legal purposes.
  </div>

  <div class="info-box" style="margin-bottom:14px">
    <b>Funding source note:</b> The victim address was funded from <code>38ABnUgrfwLg3wdP5jbytmGWKqskh3QvwE</code> (9 UTXOs, funding TX <a href="https://mempool.space/tx/cbd6b435d189b6ba05216098a7bdf7e90be617936001dba0d55ba1d88ff41541" target="_blank" style="color:#58a6ff">cbd6b435…</a>, block 747293 — 5 blocks before the sweep). The scammer may have controlled this funding source and used it to seed the victim address as a "proof of investment" to build trust. This address is a subpoena target for additional KYC data.
  </div>

  <div class="trail">
    <div class="trail-step" style="background:#0d1117;border:1px solid #30363d;border-radius:6px;padding:10px 16px;min-width:600px">
      <div class="ts-label">Funding Source (pre-theft)</div>
      <div class="ts-addr"><a href="https://mempool.space/address/38ABnUgrfwLg3wdP5jbytmGWKqskh3QvwE" target="_blank">38ABnUgrfwLg3wdP5jbytmGWKqskh3QvwE</a></div>
      <div class="ts-val">9 UTXOs → funded victim address at block 747293 · may be scammer-controlled</div>
    </div>
    <div class="trail-arrow">▼</div>
    <div class="trail-step s-victim">
      <div class="ts-label">Victim Address — Full Balance Stolen</div>
      <div class="ts-addr"><a href="https://mempool.space/address/{victim.get('victim_address','')}" target="_blank">{victim.get('victim_address','')}</a></div>
      <div class="ts-val"><b>0.84758440 BTC</b> · ~${USD_AT_THEFT:,.0f} at time of theft · ~${USD_NOW:,.0f} today · 2 txs total · balance now 0</div>
    </div>
    <div class="trail-arrow">▼</div>
    <div class="trail-step s-relay">
      <div class="ts-label">Sweep Transaction — Block 747298 (July 31 2022)</div>
      <div class="ts-addr"><a href="https://mempool.space/tx/{stx.get('txid','')}" target="_blank">{stx.get('txid','')[:40]}…</a></div>
      <div class="ts-val">{stx.get('num_inputs',0)} input · {stx.get('num_outputs',0)} outputs · fee {TX_FEE_SAT:,} sat · no change returned</div>
    </div>
    <div class="trail-arrow">▼</div>
    <div class="trail-step s-relay">
      <div class="ts-label">Relay Address (largest output — 0.46 BTC)</div>
      <div class="ts-addr"><a href="https://mempool.space/address/3R1Gs7RniDHRc6Trn214gVffSErYMbGuJ6" target="_blank">3R1Gs7RniDHRc6Trn214gVffSErYMbGuJ6</a></div>
      <div class="ts-val">8.65 BTC total received · 26 on-chain txs · balance 0</div>
    </div>
    <div class="trail-arrow">▼</div>
    <div class="trail-step s-agg">
      <div class="ts-label">Aggregator / Consolidation Wallet</div>
      <div class="ts-addr"><a href="https://mempool.space/address/34HVDP9RFA9MpopGQ4TutLLVMFhhJFM9AX" target="_blank">34HVDP9RFA9MpopGQ4TutLLVMFhhJFM9AX</a></div>
      <div class="ts-val">3,294 on-chain txs · 1,403 BTC total received · sent 97.25 BTC to Binance across 34 txs · balance ~0</div>
    </div>
    <div class="trail-arrow">▼</div>
    <div class="trail-step s-exchange">
      <div class="ts-label">Binance Hot Wallet — KYC IDENTITY HERE</div>
      <div class="ts-addr"><a href="https://mempool.space/address/bc1quhruqrghgcca950rvhtrg7cpd7u8k6svpzgzmrjy8xyukacl5lkq0r8l2d" target="_blank">bc1quhruqrghgcca950rvhtrg7cpd7u8k6svpzgzmrjy8xyukacl5lkq0r8l2d</a></div>
      <div class="ts-val">335,452 on-chain txs · 5,447,353 BTC lifetime received · Confirmed Binance</div>
    </div>
  </div>

  <!-- TX Metadata -->
  <h2 style="margin-top:20px">Sweep Transaction — Full Technical Metadata</h2>
  <div class="warn-box" style="margin-bottom:12px">
    <b>Forensic significance:</b> Fee rate of 13 sat/vbyte on 2022-07-31 indicates a scheduled, non-urgent automated sweep — not a manual panicked transfer. The 41-output batch structure and mixed output script types (P2SH + P2PKH + SegWit) require purpose-built bulk-payout software, consistent with a professional laundering operation.
  </div>
  <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:10px;margin-bottom:16px">
    <div style="background:#161b22;border:1px solid #30363d;border-radius:6px;padding:12px">
      <div style="font-size:10px;color:#8b949e;text-transform:uppercase;margin-bottom:6px">Transaction ID</div>
      <div style="font-family:monospace;font-size:10px;word-break:break-all;color:#58a6ff"><a href="https://mempool.space/tx/02ab77e433e9aaf3f78f8ccb65090a4dae8698de6f987d10b5d4c3c453984c69" target="_blank">02ab77e433e9aaf3f78f8ccb65090a4dae8698de6f987d10b5d4c3c453984c69</a></div>
    </div>
    <div style="background:#161b22;border:1px solid #30363d;border-radius:6px;padding:12px">
      <div style="font-size:10px;color:#8b949e;text-transform:uppercase;margin-bottom:6px">Block Hash</div>
      <div style="font-family:monospace;font-size:10px;word-break:break-all;color:#58a6ff"><a href="https://mempool.space/block/000000000000000000011663b2e30b4a4ee41c51d72d725f3c19136b084a4d6f" target="_blank">000000000000000000011663b2e30b4a4ee41c51d72d725f3c19136b084a4d6f</a></div>
    </div>
    <div style="background:#161b22;border:1px solid #30363d;border-radius:6px;padding:12px">
      <div style="font-size:10px;color:#8b949e;text-transform:uppercase;margin-bottom:6px">Merkle Root</div>
      <div style="font-family:monospace;font-size:10px;word-break:break-all">13b288d360cda30e7a2c2824bd4b99dd41270dcc87a02ed9bf51602ed7a1f6d0</div>
    </div>
  </div>
  <table style="margin-bottom:16px">
    <thead><tr>
      <th>Field</th><th>Value</th><th>Forensic Note</th>
    </tr></thead>
    <tbody>
      <tr><td>Timestamp</td><td style="font-family:monospace">2022-07-31 03:09:14 UTC</td><td style="color:#8b949e">03:09 UTC = 11:09 Beijing / 10:09 Bangkok / 08:39 Delhi — consistent with Asia business hours</td></tr>
      <tr><td>Block Height</td><td style="font-family:monospace">747,298</td><td style="color:#8b949e">Confirmed, immutable, permanently on-chain</td></tr>
      <tr><td>TX Version</td><td style="font-family:monospace">1</td><td style="color:#8b949e">Basic version — no SegWit v2 or Taproot features</td></tr>
      <tr><td>Locktime</td><td style="font-family:monospace">0</td><td style="color:#8b949e">No time-lock — could be broadcast and mined immediately</td></tr>
      <tr><td>Size</td><td style="font-family:monospace">1,538 bytes</td><td style="color:#8b949e">Large due to 41 outputs — requires scripted construction</td></tr>
      <tr><td>vSize (virtual)</td><td style="font-family:monospace">~1,456 vbytes</td><td style="color:#8b949e">Used for fee calculation in SegWit</td></tr>
      <tr><td>Weight</td><td style="font-family:monospace">5,822 weight units</td><td style="color:#8b949e">Standard SegWit weighting</td></tr>
      <tr><td>Fee</td><td style="font-family:monospace">18,993 sat (0.00018993 BTC)</td><td style="color:#8b949e">$4.45 at theft-day prices · $18.29 at Feb-2025 prices</td></tr>
      <tr><td>Fee Rate</td><td style="font-family:monospace">~13 sat/vbyte</td><td style="color:#8b949e">Normal/medium priority on 2022-07-31 — not urgent, scheduled</td></tr>
      <tr><td>Input count</td><td style="font-family:monospace">1</td><td style="color:#8b949e">Single UTXO drained — full balance sweep, no partial withdrawal</td></tr>
      <tr><td>Output count</td><td style="font-family:monospace">41</td><td style="color:#8b949e">Fan-out to 41 addresses — deliberate obfuscation pattern</td></tr>
      <tr><td>Input script type</td><td style="font-family:monospace">P2SH-P2WPKH</td><td style="color:#8b949e">SegWit wrapped in P2SH — public key exposed in witness (extracted above)</td></tr>
      <tr><td>Output script types</td><td style="font-family:monospace">P2SH · P2PKH · P2WPKH · P2WSH</td><td style="color:#8b949e">Mixed types indicate pre-generated multi-wallet infrastructure</td></tr>
      <tr><td>SegWit</td><td style="font-family:monospace">Yes</td><td style="color:#8b949e">Witness data present — enables public key extraction</td></tr>
      <tr><td>RBF (replaceable)</td><td style="font-family:monospace">No</td><td style="color:#8b949e">Transaction could not be cancelled once broadcast</td></tr>
      <tr><td>OP_RETURN data</td><td style="font-family:monospace">None</td><td style="color:#8b949e">No embedded messages or metadata</td></tr>
      <tr><td>Sig ops</td><td style="font-family:monospace">29</td><td style="color:#8b949e">Normal for this input/output structure</td></tr>
      <tr><td>Input value</td><td style="font-family:monospace">84,758,440 sat (0.84758448 BTC)</td><td style="color:#8b949e">Exact victim balance — entire address drained</td></tr>
      <tr><td>Output value</td><td style="font-family:monospace">84,739,447 sat (0.84739455 BTC)</td><td style="color:#8b949e">Input minus fee — zero returned to victim</td></tr>
      <tr><td>Block tx count</td><td style="font-family:monospace">3,027 transactions</td><td style="color:#8b949e">Normal busy block — sweep not isolated or suspicious to miners</td></tr>
      <tr><td>Block difficulty</td><td style="font-family:monospace">27,692,567,959,233.59</td><td style="color:#8b949e">Network state at time of confirmation</td></tr>
      <tr><td>Confirmed</td><td style="font-family:monospace" style="color:#2ecc71">Yes — permanent</td><td style="color:#8b949e">Irreversible. Cannot be reversed without exchange cooperation.</td></tr>
    </tbody>
  </table>

  <h2 style="margin-top:20px">Spending TX Outputs ({stx.get('num_outputs',0)} total — top 12 by value)</h2>
  <div class="tab-body" style="max-height:300px">
    <table id="tbl-vtx">
      <thead><tr>
        <th class="sortable" data-col="0">Destination Address</th>
        <th class="sortable" data-col="1">BTC Amount</th>
        <th>Flags</th>
      </tr></thead>
      <tbody>{vtx_rows}</tbody>
    </table>
  </div>

  <h2 style="margin-top:20px">Victim Address Funding Sources</h2>
  <div class="tab-body">
    <table>
      <thead><tr><th>Source Address (funded victim address — possible scammer-controlled)</th></tr></thead>
      <tbody>{funding_rows if funding_rows else '<tr><td style="color:#8b949e">No funding sources found</td></tr>'}</tbody>
    </table>
  </div>

  <h2 style="margin-top:20px">Public Key Fingerprint (submit to law enforcement)</h2>
  <div class="tab-body">
    <table>
      <thead><tr><th>Public Key (extracted from witness — uniquely identifies key holder)</th><th>Controlling Address</th></tr></thead>
      <tbody>{pk_rows if pk_rows else '<tr><td colspan="2" style="color:#8b949e">No public keys extracted</td></tr>'}</tbody>
    </table>
  </div>
</div>"""

    # ── Binance attribution evidence ──────────────────────────────────────────
    binance_html = """
<div class="section">
  <h2>Binance Attribution — Evidence Summary</h2>
  <div class="warn-box" style="background:#1a1100;border-color:#f1c40f;color:#ffd166">
    <b>⚡ Why we believe this is Binance:</b> Three independent lines of evidence converge.
  </div>

  <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:14px">

    <div style="background:#161b22;border:1px solid #30363d;border-radius:8px;padding:16px">
      <div style="font-size:11px;text-transform:uppercase;color:#8b949e;margin-bottom:8px;letter-spacing:.5px">Evidence 1 — Known Public Identifier</div>
      <div style="font-family:monospace;font-size:11px;word-break:break-all;color:#58a6ff">bc1qm34lsc65zpw79lxes69zkqmk6ee3ewf0j77s3h</div>
      <div style="margin-top:8px;font-size:12px">This address appears in multiple published Binance hot-wallet lists and blockchain intelligence databases. It has processed <b>2,173,077 on-chain transactions</b> — consistent only with a top-tier exchange.</div>
      <div style="margin-top:6px;font-size:11px;color:#8b949e">Direct hop-2 destination from the scammer wallet. Received 472.52 BTC via this trace.</div>
    </div>

    <div style="background:#161b22;border:1px solid #30363d;border-radius:8px;padding:16px">
      <div style="font-size:11px;text-transform:uppercase;color:#8b949e;margin-bottom:8px;letter-spacing:.5px">Evidence 2 — Exchange-Scale Transaction Volume</div>
      <div style="font-family:monospace;font-size:11px;word-break:break-all;color:#58a6ff">bc1quhruqrghgcca950rvhtrg7cpd7u8k6svpzgzmrjy8xyukacl5lkq0r8l2d</div>
      <div style="margin-top:8px;font-size:12px"><b>335,452 transactions</b> and <b>5,447,353 BTC received lifetime</b>. No privately controlled wallet operates at this scale. This volume is only possible for a major custodial exchange with millions of users.</div>
      <div style="margin-top:6px;font-size:11px;color:#8b949e">This is the address the aggregator wallet sent 97.25 BTC to across 34 separate transactions.</div>
    </div>

    <div style="background:#161b22;border:1px solid #30363d;border-radius:8px;padding:16px">
      <div style="font-size:11px;text-transform:uppercase;color:#8b949e;margin-bottom:8px;letter-spacing:.5px">Evidence 3 — Aggregator Deposit Pattern</div>
      <div style="font-family:monospace;font-size:11px;word-break:break-all;color:#58a6ff">34HVDP9RFA9MpopGQ4TutLLVMFhhJFM9AX</div>
      <div style="margin-top:8px;font-size:12px">This aggregator wallet received funds consolidated from the victim's relay address, then forwarded them in <b>34 discrete transactions</b> to the Binance hot wallet. This pattern (consolidate → batch deposit) is the textbook method used by bad actors to deposit stolen BTC into a KYC exchange.</div>
      <div style="margin-top:6px;font-size:11px;color:#8b949e">3,294 on-chain txs. Zero current balance (fully swept). Account holder registered KYC with Binance.</div>
    </div>

    <div style="background:#161b22;border:1px solid #30363d;border-radius:8px;padding:16px">
      <div style="font-size:11px;text-transform:uppercase;color:#8b949e;margin-bottom:8px;letter-spacing:.5px">Evidence 4 — Swept Deposit Address Heuristic</div>
      <div style="font-size:12px;margin-bottom:8px">Across both hops, <b>208 exchange deposit addresses</b> were identified with this signature pattern:</div>
      <ul style="font-size:11px;color:#8b949e;margin-left:16px;line-height:1.8">
        <li>Large BTC received in 1–12 transactions</li>
        <li>Current balance = 0.0000 BTC (fully swept by exchange)</li>
        <li>Outbound TX sends entire balance to high-volume custodial address</li>
        <li>No further on-chain activity from the deposit address</li>
      </ul>
      <div style="margin-top:8px;font-size:11px;color:#8b949e">Exchange deposit addresses are one-time use. They are issued to a specific registered account. Binance retains the mapping between deposit address → user account ID.</div>
    </div>

  </div>


  <h3 style="color:#f0f6fc;font-size:13px;margin:16px 0 8px">Transaction Chain — Victim → Binance (complete hop-by-hop)</h3>
  <div style="overflow-x:auto">
  <table>
    <thead><tr>
      <th>Step</th><th>From</th><th>To</th><th>Amount BTC</th><th>Block / TX</th>
    </tr></thead>
    <tbody>
      <tr>
        <td>1. Victim → Relay</td>
        <td style="font-family:monospace;font-size:10px"><a href="https://mempool.space/address/3MT5t24cF88QzZ5qjgfDioC79pvyQDsojt" target="_blank">3MT5t24…QDsojt</a></td>
        <td style="font-family:monospace;font-size:10px"><a href="https://mempool.space/address/3R1Gs7RniDHRc6Trn214gVffSErYMbGuJ6" target="_blank">3R1Gs7R…MbGuJ6</a></td>
        <td>0.46 BTC</td>
        <td style="font-size:10px"><a href="https://mempool.space/tx/02ab77e433e9aaf3f78f8ccb65090a4dae8698de6f987d10b5d4c3c453984c69" target="_blank">Block 747298</a></td>
      </tr>
      <tr>
        <td>2. Relay → Aggregator</td>
        <td style="font-family:monospace;font-size:10px"><a href="https://mempool.space/address/3R1Gs7RniDHRc6Trn214gVffSErYMbGuJ6" target="_blank">3R1Gs7R…MbGuJ6</a></td>
        <td style="font-family:monospace;font-size:10px"><a href="https://mempool.space/address/34HVDP9RFA9MpopGQ4TutLLVMFhhJFM9AX" target="_blank">34HVDP9…hJFM9AX</a></td>
        <td>~8.65 BTC total</td>
        <td style="font-size:10px">Multiple TXs</td>
      </tr>
      <tr>
        <td>3. Aggregator → Binance</td>
        <td style="font-family:monospace;font-size:10px"><a href="https://mempool.space/address/34HVDP9RFA9MpopGQ4TutLLVMFhhJFM9AX" target="_blank">34HVDP9…hJFM9AX</a></td>
        <td style="font-family:monospace;font-size:10px"><a href="https://mempool.space/address/bc1quhruqrghgcca950rvhtrg7cpd7u8k6svpzgzmrjy8xyukacl5lkq0r8l2d" target="_blank">bc1quhruq…lkq0r8l2d</a></td>
        <td>97.25 BTC total (34 txs)</td>
        <td style="font-size:10px">Multiple TXs</td>
      </tr>
    </tbody>
  </table>
  </div>

  <h3 style="color:#f0f6fc;font-size:13px;margin:16px 0 8px">Scammer Wallet → Binance (direct hop-2 path)</h3>
  <div style="overflow-x:auto">
  <table>
    <thead><tr>
      <th>Hop-1 Address</th><th>BTC Forwarded</th><th>Hop-2 Binance Address</th><th>BTC to Binance</th>
    </tr></thead>
    <tbody>
      <tr>
        <td style="font-family:monospace;font-size:10px"><a href="https://mempool.space/address/1JpeKeUVhRYWCzA3roGCABcmLLnkMgRntm" target="_blank">1JpeKeUVh…mgRntm</a></td>
        <td>500.25 BTC</td>
        <td style="font-family:monospace;font-size:10px"><a href="https://mempool.space/address/bc1qm34lsc65zpw79lxes69zkqmk6ee3ewf0j77s3h" target="_blank">bc1qm34lsc…j77s3h</a></td>
        <td>472.52 BTC</td>
      </tr>
      <tr>
        <td style="font-family:monospace;font-size:10px">Multiple hop-1 addresses</td>
        <td>~909.72 BTC combined</td>
        <td style="font-family:monospace;font-size:10px"><a href="https://mempool.space/address/bc1quhruqrghgcca950rvhtrg7cpd7u8k6svpzgzmrjy8xyukacl5lkq0r8l2d" target="_blank">bc1quhruq…lkq0r8l2d</a></td>
        <td>436.66 BTC</td>
      </tr>
    </tbody>
  </table>
  </div>
</div>"""

    # ── deptoy.co / BIPPAX platform link section ─────────────────────────────
    deptoy_html = """
<div class="section">
  <h2>deptoy.co Platform Link — BIPPAX Fake Exchange</h2>

  <div class="warn-box" style="background:#1a0a1a;border-color:#9b59b6;color:#d9b3ff">
    <b>⚡ KEY FINDING:</b> A high-volume intermediary address (<code>3JMjHDTJjKPnrvS7DycPAgYcA6HrHRk8UG</code>)
    sent <b>140 BTC directly to the scammer wallet</b> in 7 transactions between February 2024 and August 2025.
    This address processed 64,255 BTC across 25,117 on-chain transactions and operates as an aggregator
    for victim deposits collected through the <b>BIPPAX</b> fake exchange platform at <b>deptoy.co</b>.
  </div>

  <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:14px">

    <div style="background:#161b22;border:1px solid #30363d;border-radius:8px;padding:16px">
      <div style="font-size:11px;text-transform:uppercase;color:#8b949e;margin-bottom:8px;letter-spacing:.5px">BIPPAX / deptoy.co Platform Overview</div>
      <ul style="font-size:12px;line-height:1.9;margin-left:16px;color:#c9d1d9">
        <li>Domain: <b>deptoy.co</b> — registered May 2024 (active through at least Dec 2024)</li>
        <li>Platform: <b>BIPPAX</b> — white-label fake cryptocurrency exchange</li>
        <li>Alternate BIPPAX domain: <b>www.bippaxcoins.com</b> (found in platform source)</li>
        <li>Official brand: <b>BIPPAX.PRO</b> (self-stated in English text)</li>
        <li>WeChat customer service: <b>bmate601</b> (confirmed banned) · <b>bizzzan01</b> (second operator)</li>
        <li>Additional WeChat/social handle: <b>883le</b> (found in wechat context)</li>
        <li>Contact email: <code>Promotion@BIPPAX.com</code> / <code>promotion@BIPPAX.com</code></li>
        <li>Second email domain: <code>anwerbung@bitspaieex.com</code> ("anwerbung" = German for "recruitment/advertising" — possible prior deployment)</li>
        <li>Chinese ICP registration: <b>沪ICP备13026899号-3</b> — hardcoded in platform source in 13 languages as a legitimacy signal · Third-party ICP database query returned <b style="color:#e74c3c">NO RECORD</b> — number may be fabricated or revoked · MLAT request to MIIT will confirm</li>
        <li>Corporate claim: "Registered in the Cayman Islands, core operating team in Hong Kong"</li>
        <li>Server OS: <b>CentOS Linux</b> (confirmed from api.deptoy.co default page)</li>
        <li>Multi-language: ZH, JA, KO, ID, TH, IT, ES, FR, DE, HI (13 languages)</li>
        <li>API endpoint: <code>api.deptoy.co</code> (now offline)</li>
        <li>Internal IPs in source: <code>192.168.1.1/2/3</code>, <code>192.168.100.100</code></li>
      </ul>
    </div>

    <div style="background:#161b22;border:1px solid #30363d;border-radius:8px;padding:16px">
      <div style="font-size:11px;text-transform:uppercase;color:#8b949e;margin-bottom:8px;letter-spacing:.5px">Pivot Address — Victim Collection Hub</div>
      <div style="font-family:monospace;font-size:11px;word-break:break-all;color:#58a6ff;margin-bottom:8px">
        <a href="https://mempool.space/address/3JMjHDTJjKPnrvS7DycPAgYcA6HrHRk8UG" target="_blank">3JMjHDTJjKPnrvS7DycPAgYcA6HrHRk8UG</a>
      </div>
      <ul style="font-size:12px;line-height:1.9;margin-left:16px;color:#c9d1d9">
        <li>64,255.78 BTC total received · 25,117 on-chain transactions</li>
        <li>Identified in hop-2 analysis as "Exchange/Service (high volume)"</li>
        <li>Sent 41.30 BTC to scammer in our hop-2 trace</li>
        <li><b>7 confirmed direct sends to scammer — 140 BTC total</b></li>
        <li>Round-number disbursements: 50, 20, 20, 20, 20, 5, 5 BTC</li>
        <li>Jan 2025 TX: 300+ tiny inputs (victim deposits) consolidated → 5 BTC to scammer</li>
      </ul>
    </div>

  </div>

  <h3 style="color:#f0f6fc;font-size:13px;margin:16px 0 8px">7 Direct Transfers: Pivot → Scammer Wallet</h3>
  <div class="tab-body" style="max-height:280px">
    <table>
      <thead><tr>
        <th>Date (UTC)</th>
        <th>Transaction ID</th>
        <th style="text-align:right">BTC Amount</th>
        <th>Pattern</th>
      </tr></thead>
      <tbody>
        <tr>
          <td>2024-02-29</td>
          <td style="font-family:monospace;font-size:10px"><a href="https://mempool.space/tx/9e13b5434ceceef380a47119bb5ad489007eff4983e02b0c9b2cf4480484e256" target="_blank">9e13b5434ceceef380a4…</a></td>
          <td style="text-align:right;font-weight:bold">50.000000</td>
          <td><span class="badge" style="background:#9b59b6">Large round sweep</span></td>
        </tr>
        <tr>
          <td>2024-06-03</td>
          <td style="font-family:monospace;font-size:10px"><a href="https://mempool.space/tx/1d50ec9afbb10fd20aeaad25ff31384ddb4a98386e5f443684009f090a6ef0c4" target="_blank">1d50ec9afbb10fd20aea…</a></td>
          <td style="text-align:right;font-weight:bold">20.000000</td>
          <td><span class="badge" style="background:#9b59b6">deptoy.co active period</span></td>
        </tr>
        <tr>
          <td>2024-09-27</td>
          <td style="font-family:monospace;font-size:10px"><a href="https://mempool.space/tx/954f8ae890e428b5ecd08aec11de8d59857c6dd6a4ce477c28b976d69e9869c0" target="_blank">954f8ae890e428b5ecd0…</a></td>
          <td style="text-align:right;font-weight:bold">20.000000</td>
          <td><span class="badge" style="background:#9b59b6">deptoy.co active period</span></td>
        </tr>
        <tr>
          <td>2024-11-02</td>
          <td style="font-family:monospace;font-size:10px"><a href="https://mempool.space/tx/39e3ed3fbec32c5f61303564898dccf65cd7157d3796568644878104be9f9ef5" target="_blank">39e3ed3fbec32c5f6130…</a></td>
          <td style="text-align:right;font-weight:bold">20.000000</td>
          <td><span class="badge" style="background:#9b59b6">deptoy.co active period</span></td>
        </tr>
        <tr>
          <td>2024-12-12</td>
          <td style="font-family:monospace;font-size:10px"><a href="https://mempool.space/tx/2277732773156dcb859006d776706d45018dea5897452bb7d6cee4eb9ff8a630" target="_blank">2277732773156dcb8590…</a></td>
          <td style="text-align:right;font-weight:bold">20.000000</td>
          <td><span class="badge" style="background:#9b59b6">deptoy.co active period</span></td>
        </tr>
        <tr>
          <td>2025-01-28</td>
          <td style="font-family:monospace;font-size:10px"><a href="https://mempool.space/tx/471189025a911b5dcf905d505d8a10298a3baac248901cc5d6124a5289edf514" target="_blank">471189025a911b5dcf90…</a></td>
          <td style="text-align:right;font-weight:bold">5.000000</td>
          <td><span class="badge" style="background:#e74c3c">300+ victim UTXO consolidation</span></td>
        </tr>
        <tr>
          <td>2025-08-12</td>
          <td style="font-family:monospace;font-size:10px"><a href="https://mempool.space/tx/01b2e703c9fb821317ab6428b9cccae983818e7ff4569fdf948fdc263652753d" target="_blank">01b2e703c9fb821317ab…</a></td>
          <td style="text-align:right;font-weight:bold">5.000000</td>
          <td><span class="badge" style="background:#9b59b6">Single large input sweep</span></td>
        </tr>
        <tr style="background:#1c1010">
          <td><b>TOTAL</b></td>
          <td></td>
          <td style="text-align:right;font-weight:bold;color:#e74c3c">140.000000</td>
          <td></td>
        </tr>
      </tbody>
    </table>
  </div>

  <h3 style="color:#f0f6fc;font-size:13px;margin:16px 0 8px">Money Flow Architecture — deptoy.co to Scammer</h3>
  <div class="trail">
    <div class="trail-step" style="background:#1a0a1a;border-color:#9b59b6">
      <div class="ts-label">BIPPAX Victims (many users)</div>
      <div class="ts-addr">Multiple victim deposit addresses — served dynamically from api.deptoy.co (now offline)</div>
      <div class="ts-val">Victims instructed to deposit BTC to platform-generated addresses. Deposits collected in batches of 0.012–0.017 BTC (typical victim deposit size)</div>
    </div>
    <div class="trail-arrow">▼</div>
    <div class="trail-step" style="background:#1a1a10;border-color:#f39c12">
      <div class="ts-label">Victim Aggregation Hub (Pivot)</div>
      <div class="ts-addr"><a href="https://mempool.space/address/3JMjHDTJjKPnrvS7DycPAgYcA6HrHRk8UG" target="_blank">3JMjHDTJjKPnrvS7DycPAgYcA6HrHRk8UG</a></div>
      <div class="ts-val">64,255 BTC lifetime received · 25,117 txs · Consolidates hundreds of small UTXOs into round-number batches for transfer to scammer</div>
    </div>
    <div class="trail-arrow">▼</div>
    <div class="trail-step" style="background:#1c1010;border-color:#e74c3c">
      <div class="ts-label">Original Scammer Wallet</div>
      <div class="ts-addr"><a href="https://mempool.space/address/3GH4EhMi1MG8rxSiAWqfoiUCMLaWPTCxuy" target="_blank">3GH4EhMi1MG8rxSiAWqfoiUCMLaWPTCxuy</a></div>
      <div class="ts-val"><b>140 BTC received from pivot</b> in 7 transfers (2024-02 through 2025-08) · <b>395,190 BTC total lifetime received</b> · 5,170 txs · Balance: 3.22 BTC (last tx 2026-01-21) · Pivot address (3JMjHDT...) appears 1,050 times as co-input in sampled txs — same operator</div>
    </div>
  </div>

  <h3 style="color:#f0f6fc;font-size:13px;margin:16px 0 8px">5-Hop Chain — Second Theft via deptoy.co (Jul 2024, ~$10,040 = 0.14970 BTC)</h3>
  <div class="warn-box" style="background:#0a1a1a;border-color:#1abc9c;color:#a8e6cf;margin-bottom:10px">
    <b>SECOND VICTIM THEFT FULLY TRACED:</b> Victim made <b>two deposits</b> to deptoy.co on 2024-07-25 and 2024-07-26 totalling <b>0.14970240 BTC (~$10,040)</b>.
    Both transactions confirmed on-chain. Funds swept with 70+ other victims into BIPPAX platform aggregator, then forwarded to scammer wallet.
    <br><br>
    <b>TX 1:</b> <code><a href="https://mempool.space/tx/e81ac50854e47dddfb955cf3ff9dfebe05d3016c759de8e1c23719620dfccc08" target="_blank" style="color:#1abc9c">e81ac50854e47dddfb955cf3ff9dfebe05d3016c759de8e1c23719620dfccc08</a></code> · 2024-07-25 · 0.07622126 BTC<br>
    <b>TX 2:</b> <code><a href="https://mempool.space/tx/ef504db1bb3800700198eae26a7ca97a455aed0f6f835dfa115efbca23dc581d" target="_blank" style="color:#1abc9c">ef504db1bb3800700198eae26a7ca97a455aed0f6f835dfa115efbca23dc581d</a></code> · 2024-07-26 · 0.07348114 BTC
  </div>
  <div class="trail">
    <div class="trail-step" style="background:#0a1a0a;border-color:#1abc9c">
      <div class="ts-label">Exchange Hot Wallet (Hop 0) — KYC IDENTITY HERE ⚡</div>
      <div class="ts-addr"><a href="https://mempool.space/address/bc1qprdf80adfz7aekh5nejjfrp3jksc8r929svpxk" target="_blank">bc1qprdf80adfz7aekh5nejjfrp3jksc8r929svpxk</a></div>
      <div class="ts-val">183,572 on-chain txs · <b>14,036,540 BTC lifetime received</b> · <b>ROBINHOOD CRYPTO LLC</b> hot wallet (confirmed by victim) · US company · FinCEN MSB · Subpoenable under 18 USC §2703 · Subpoena for victim withdrawal records (two txs on 2024-07-25 and 2024-07-26) — will document victim account KYC and exact withdrawal amounts</div>
    </div>
    <div class="trail-arrow">▼</div>
    <div class="trail-step" style="background:#1a1a0a;border-color:#f39c12">
      <div class="ts-label">deptoy.co Victim Deposit Address (Hop 1) — TWO VICTIM DEPOSITS</div>
      <div class="ts-addr"><a href="https://mempool.space/address/129z2g1vNMvVes3yiwbnVS8KtMSZFGm7Mc" target="_blank">129z2g1vNMvVes3yiwbnVS8KtMSZFGm7Mc</a></div>
      <div class="ts-val">0.14970240 BTC total · 3 txs · Received victim's two deposits (0.07622126 BTC on 2024-07-25, 0.07348114 BTC on 2024-07-26) · Swept to consolidator 3 days later with 70+ co-depositors · Now empty</div>
    </div>
    <div class="trail-arrow">▼</div>
    <div class="trail-step" style="background:#1a1a0a;border-color:#f39c12">
      <div class="ts-label">Mass-Victim Sweep (Hop 2) — 70+ Victims Swept Simultaneously</div>
      <div class="ts-addr"><a href="https://mempool.space/address/1NjU5czLRBWn89LmWHfyq9Vi8Fskjqy6kA" target="_blank">1NjU5czLRBWn89LmWHfyq9Vi8Fskjqy6kA</a></div>
      <div class="ts-val">13.83 BTC total · 37 txs · <b>Sweep TX <a href="https://mempool.space/tx/4a512679c63b3a8186b48d6251511e89ff2fd32ab8608c1984264f7d7dc67d12" target="_blank" style="color:#f39c12">4a512679c63b3a8186b48d6...</a></b> had 70+ inputs from individual victim deposit addresses — all swept simultaneously into 1.344 BTC consolidation. This single transaction documents the deposit addresses of 70+ additional victims.</div>
    </div>
    <div class="trail-arrow">▼</div>
    <div class="trail-step" style="background:#1a1a0a;border-color:#f39c12">
      <div class="ts-label">Secondary Aggregator (Hop 3)</div>
      <div class="ts-addr"><a href="https://mempool.space/address/3NWjDQkpSQTnjtJSUwVpnC2ivLCZr1zGKu" target="_blank">3NWjDQkpSQTnjtJSUwVpnC2ivLCZr1zGKu</a></div>
      <div class="ts-val">4.49 BTC total · 29 txs</div>
    </div>
    <div class="trail-arrow">▼</div>
    <div class="trail-step" style="background:#1a1a0a;border-color:#f39c12">
      <div class="ts-label">Large Collection Wallet (Hop 4) — WalletExplorer Cluster 6cbec0582a</div>
      <div class="ts-addr"><a href="https://mempool.space/address/145hFvPqPLWevK5TNpAXkMNpGEYBXhB66z" target="_blank">145hFvPqPLWevK5TNpAXkMNpGEYBXhB66z</a></div>
      <div class="ts-val">37.39 BTC total · 120 txs · Part of a larger co-spend cluster (WalletExplorer 6cbec0582a)</div>
    </div>
    <div class="trail-arrow">▼</div>
    <div class="trail-step" style="background:#1a1a0a;border-color:#f39c12">
      <div class="ts-label">Further Aggregation (Hop 5) — WalletExplorer Cluster 329c3b500b</div>
      <div class="ts-addr"><a href="https://mempool.space/address/323XtjvdYZMJp3CAJ2SbJMUcAyV4VmZgc7" target="_blank">323XtjvdYZMJp3CAJ2SbJMUcAyV4VmZgc7</a></div>
      <div class="ts-val">15.76 BTC total · 108 txs · Co-spend cluster 329c3b500b</div>
    </div>
    <div class="trail-arrow">▼</div>
    <div class="trail-step" style="background:#1c1010;border-color:#e74c3c">
      <div class="ts-label">Terminal Wallet (Hop 6) — Now Empty</div>
      <div class="ts-addr"><a href="https://mempool.space/address/bc1q2u2eyvnndad0dlqmrwzp0pncaxpn9ka40f47mk" target="_blank">bc1q2u2eyvnndad0dlqmrwzp0pncaxpn9ka40f47mk</a></div>
      <div class="ts-val">15.72 BTC total · 119 txs · Balance now 0 — funds fully laundered through chain</div>
    </div>
  </div>

  <div class="info-box" style="margin-top:14px">
    <b>Forensic significance of the Jan 2025 consolidation transaction:</b>
    Transaction <code>471189025a911b5dcf905d505d8a10298a3baac248901cc5d6124a5289edf514</code>
    consolidates <b>300+ individual UTXOs</b> — each valued 0.012–0.017 BTC — all from the pivot address,
    then sends exactly <b>5.000000 BTC</b> to the scammer. This pattern is characteristic of a custodial
    platform (fake exchange) that has collected hundreds of small victim deposits and is sweeping the
    accumulated funds to the operator. The fractional input sizes (~$1,200–$1,700 each at Jan 2025 prices)
    are consistent with typical "minimum deposit" amounts on pig butchering platforms.
  </div>

  <div class="info-box" style="margin-top:10px">
    <b>Platform continuity — same criminal network:</b> The original theft occurred 2022-07-31.
    deptoy.co was registered May 2024 — a gap of ~22 months. This is consistent with the scam operation
    migrating to a new platform/domain (deptoy.co / BIPPAX) while continuing to funnel proceeds to the
    same scammer wallet. The user confirmed the site moved; the pivot address provides the on-chain
    bridge between the two operational phases.
  </div>

  <h3 style="color:#f0f6fc;font-size:13px;margin:16px 0 8px">Additional Subpoena Targets (deptoy.co investigation)</h3>
  <table>
    <thead><tr>
      <th>Address / Identifier</th>
      <th>Type</th>
      <th>Relevance</th>
    </tr></thead>
    <tbody>
      <tr>
        <td style="font-family:monospace;font-size:11px"><a href="https://mempool.space/address/3JMjHDTJjKPnrvS7DycPAgYcA6HrHRk8UG" target="_blank">3JMjHDTJjKPnrvS7DycPAgYcA6HrHRk8UG</a></td>
        <td>Victim aggregation hub</td>
        <td>Sent 140 BTC directly to scammer · 64,255 BTC total · Any exchange holding this account has KYC</td>
      </tr>
      <tr>
        <td style="font-family:monospace;font-size:11px"><a href="https://mempool.space/address/3HaHcbNmhJKgJ3dtbm2tg8XH87BJkRx7QE" target="_blank">3HaHcbNmhJKgJ3dtbm2tg8XH87BJkRx7QE</a></td>
        <td>Secondary funder of pivot</td>
        <td>Sent 67.43 BTC to pivot in 1 transaction — possible second collection wallet</td>
      </tr>
      <tr>
        <td style="font-family:monospace;font-size:11px">bmate601</td>
        <td>WeChat customer service ID</td>
        <td>Embedded in deptoy.co platform source code — confirmed banned on WeChat — subpoena Tencent for account creation IP/phone</td>
      </tr>
      <tr>
        <td style="font-family:monospace;font-size:11px">bizzzan01</td>
        <td>WeChat second operator ID</td>
        <td>Second WeChat contact found in same source code context as bmate601 — likely second customer service operator</td>
      </tr>
      <tr>
        <td style="font-family:monospace;font-size:11px">883le</td>
        <td>WeChat/social handle</td>
        <td>Third identifier found in WeChat context in platform source — possible agent/affiliate account</td>
      </tr>
      <tr>
        <td style="font-family:monospace;font-size:11px">Promotion@BIPPAX.com</td>
        <td>Platform email</td>
        <td>Contact address embedded in deptoy.co — subpoena email host for registration/IP records</td>
      </tr>
      <tr>
        <td style="font-family:monospace;font-size:11px">anwerbung@bitspaieex.com</td>
        <td>Recruitment/marketing email</td>
        <td>"anwerbung" = German for recruitment/advertising. Domain bitspaieex.com = probable prior BIPPAX deployment targeting German-speaking victims — subpoena for registrant/hosting</td>
      </tr>
      <tr>
        <td style="font-family:monospace;font-size:11px">www.bippaxcoins.com</td>
        <td>Alternate BIPPAX domain</td>
        <td>Hardcoded in BIPPAX platform source as the official alternate domain — WHOIS + hosting subpoena</td>
      </tr>
      <tr>
        <td style="font-family:monospace;font-size:11px;color:#2ecc71"><b>ROBINHOOD CRYPTO LLC</b><br>bc1qprdf80adfz7aekh5nejjfrp3jksc8r929svpxk</td>
        <td><b style="color:#2ecc71">⚡ VICTIM'S OWN EXCHANGE — US jurisdiction</b></td>
        <td><b>Victim confirmed withdrawing from Robinhood on 2024-07-25 and 2024-07-26.</b> Robinhood holds: victim KYC, withdrawal records, IP address at time of withdrawal. Subpoena under 18 USC §2703. Robinhood Crypto LLC · 85 Willow Road, Menlo Park, CA 94025 · legal@robinhood.com · FinCEN MSB 31000192417028</td>
      </tr>
      <tr>
        <td style="font-family:monospace;font-size:11px">沪ICP备13026899号-3</td>
        <td>Chinese ICP license</td>
        <td>Hardcoded in deptoy.co source in 13 languages as legitimacy signal · <b style="color:#e74c3c">Third-party database query: NO RECORD FOUND</b> — number may be fabricated (additional evidence of deliberate victim deception) or revoked · MLAT to MIIT will confirm status · If fabricated: using a false government registration number is an additional fraud element</td>
      </tr>
      <tr>
        <td style="font-family:monospace;font-size:11px">api.deptoy.co</td>
        <td>Backend API domain</td>
        <td>Subpoena registrar + hosting provider for server logs, registration data, payment records</td>
      </tr>
      <tr style="background:#1c1a0a">
        <td style="font-family:monospace;font-size:11px;color:#f1c40f"><b>12LejAUpWg1v4zemPy1kH6mnSm2kNR6mki</b></td>
        <td><b style="color:#f1c40f">Active holding address (6.69 BTC)</b></td>
        <td>Received 2.60 BTC from scammer wallet 2025-03-14 · Current balance 6.69 BTC · Funds not yet moved · Subpoena any exchange holding this address</td>
      </tr>
      <tr style="background:#1c100a">
        <td style="font-family:monospace;font-size:11px;color:#ff6b6b"><b>3Hcu3AeQZX3KxjKYSjhJKF9FRhH9EBqZEm</b></td>
        <td><b style="color:#ff6b6b">MOST RECENT OUTFLOW (1.0 BTC)</b></td>
        <td>Last known destination from scammer wallet · Received 1.0012 BTC on <b>2026-01-21</b> · Balance: 1.0 BTC · Most recent confirmed scammer activity</td>
      </tr>
      <tr style="background:#1c1a0a">
        <td style="font-family:monospace;font-size:11px;color:#f1c40f"><b>3Lw8hTF9app5gDf97LnrkMn9CVUYcRmJqP</b></td>
        <td><b style="color:#f1c40f">Second holding address (5.047 BTC)</b></td>
        <td>Received 5.047 BTC from scammer wallet on 2025-08-12 via 33CNxS6... relay · Still holds full balance · Subpoena any exchange</td>
      </tr>
      <tr style="background:#1c100a">
        <td style="font-family:monospace;font-size:11px;color:#ff6b6b"><b>aztexchange.com (NEW — 2026-03-01)</b></td>
        <td><b style="color:#ff6b6b">⚠ ACTIVE: New scam domain, just suspended</b></td>
        <td>Registered 2026-03-01 by Realtime Register B.V. (Netherlands) · SSL cert issued same day · Registrar immediately placed on clientHold (suspended) · Operation attempted new infrastructure 23 days ago — confirms criminal network is still active and attempting to re-launch · Abuse report contact: rtr-security-threats@realtimeregister.com</td>
      </tr>
    </tbody>
  </table>
</div>

<!-- ── CRIMINAL NETWORK OSINT PROFILE ─────────────────────────────────────── -->
<div class="section">
  <h2>Criminal Network OSINT Profile — BIPPAX / BISSNEX Operation</h2>

  <div class="warn-box" style="background:#0a1a0a;border-color:#2ecc71;color:#a8f0a8">
    <b>⚡ CANADIAN FEDERAL CORPORATION IDENTIFIED:</b> The BIPPAX / deptoy.co operation incorporated a
    Canadian money service business (<b>Alpha Technology Holding → BIPPAX CRYPTO GROUP → BISSNEX CRYPTO GROUP</b>)
    registered with FINTRAC. FINTRAC holds mandatory KYC documentation on all beneficial owners — this is the
    highest-priority law enforcement target for real identity disclosure.
  </div>

  <div class="warn-box" style="background:#0d1117;border:2px solid #f1c40f;color:#f1f8ff;margin-top:10px">
    <div style="font-weight:bold;color:#f1c40f;font-size:13px;margin-bottom:8px">🔗 DIRECT PROOF: deptoy.co IS the BIPPAX / BISSNEX Platform</div>
    <p style="font-size:12px;margin:0 0 8px">The following text is <b>hardcoded in 13 languages</b> directly inside the deptoy.co JavaScript source code (<code>app.66bc9f716f39a8a33c06.js</code>):</p>
    <blockquote style="background:#161b22;border-left:3px solid #f1c40f;padding:8px 12px;margin:8px 0;font-size:12px;font-style:italic;color:#e6edf3">
      "BIPPAX.PRO is a leading digital asset trading platform in the world, <b>registered in the Cayman Islands</b>, with a <b>core operating team in Hong Kong</b>. The core members of BIPPAX.PRO come from top Internet and financial companies."
    </blockquote>
    <p style="font-size:12px;margin:8px 0 4px">Compare with <b>BISSNEX CRYPTO GROUP</b> press releases (GlobeNewswire, December 2023):</p>
    <blockquote style="background:#161b22;border-left:3px solid #2ecc71;padding:8px 12px;margin:8px 0;font-size:12px;font-style:italic;color:#e6edf3">
      "BISSNEX is registered in the Cayman Islands, with a core operating team in Hong Kong…"
    </blockquote>
    <p style="font-size:12px;margin:8px 0 0"><b>The language is identical.</b> The same entity authored both. The platform also hardcodes <code>www.bippaxcoins.com</code> as its domain — the same domain the Canadian corporation was explicitly named after ("BIPPAX CRYPTO GROUP LIMITED").</p>
    <p style="font-size:12px;margin:4px 0 0;color:#8b949e"><i>Note: This quote appears in English, Chinese (Simplified), Chinese (Traditional), Japanese, Korean, Indonesian, Thai, Italian, Spanish, French, German, Hindi, Turkish — 13 languages — confirming this is core platform content, not a third-party reference.</i></p>
  </div>

  <h3 style="color:#f0f6fc;font-size:13px;margin:16px 0 8px">Corporate Shell Chain</h3>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px">
    <div style="background:#161b22;border:1px solid #30363d;border-radius:8px;padding:16px">
      <div style="font-size:11px;text-transform:uppercase;color:#8b949e;margin-bottom:8px">Federal Canadian Corporation #1231288-3</div>
      <table style="font-size:12px;width:100%">
        <tr><td style="color:#8b949e;padding:2px 8px 2px 0">Original name</td><td><b>Alpha Technology Holding Limited</b></td></tr>
        <tr><td style="color:#8b949e;padding:2px 8px 2px 0">Renamed</td><td>BIPPAX CRYPTO GROUP LIMITED (2022-12-22)</td></tr>
        <tr><td style="color:#8b949e;padding:2px 8px 2px 0">Renamed</td><td>BISSNEX CRYPTO GROUP LIMITED (2023-05-18)</td></tr>
        <tr><td style="color:#8b949e;padding:2px 8px 2px 0">Incorporated</td><td>2020-09-02</td></tr>
        <tr><td style="color:#8b949e;padding:2px 8px 2px 0">Dissolved</td><td style="color:#e74c3c">2025-07-25 (non-compliance, s.212)</td></tr>
        <tr><td style="color:#8b949e;padding:2px 8px 2px 0">Director</td><td style="color:#f1c40f"><b>JACK WILLIAMS</b> (likely fictitious — common Anglo cover name)</td></tr>
        <tr><td style="color:#8b949e;padding:2px 8px 2px 0">Registered address</td><td>20 Leslie St, Toronto, ON M4M 3L4</td></tr>
        <tr><td style="color:#8b949e;padding:2px 8px 2px 0">Branch address</td><td>719 Euclid Avenue, Toronto, ON M6G 2V1</td></tr>
        <tr><td style="color:#8b949e;padding:2px 8px 2px 0">Business number</td><td style="font-family:monospace">705303337RC0001</td></tr>
      </table>
    </div>
    <div style="background:#161b22;border:1px solid #30363d;border-radius:8px;padding:16px">
      <div style="font-size:11px;text-transform:uppercase;color:#8b949e;margin-bottom:8px">FINTRAC MSB Registration</div>
      <table style="font-size:12px;width:100%">
        <tr><td style="color:#8b949e;padding:2px 8px 2px 0">FINTRAC #</td><td style="font-family:monospace"><b>M20852872</b></td></tr>
        <tr><td style="color:#8b949e;padding:2px 8px 2px 0">Registered</td><td>2020-11-02</td></tr>
        <tr><td style="color:#8b949e;padding:2px 8px 2px 0">Expired</td><td>2025-08-26</td></tr>
        <tr><td style="color:#8b949e;padding:2px 8px 2px 0">Phone filed</td><td style="color:#f39c12;font-family:monospace">2478001924 <span style="color:#8b949e;font-family:sans-serif">(invalid CA area code — likely fabricated)</span></td></tr>
        <tr><td style="color:#8b949e;padding:2px 8px 2px 0">Activities</td><td>Foreign exchange · Money transfer · Virtual currencies</td></tr>
        <tr><td style="color:#8b949e;padding:2px 8px 2px 0">PCMLTFA</td><td>Subject to mandatory AML reporting — FINTRAC holds transaction records + beneficial owner ID</td></tr>
        <tr><td style="color:#8b949e;padding:2px 8px 2px 0">Website</td><td><a href="https://www.bissnex.com" target="_blank">bissnex.com</a></td></tr>
      </table>
      <div class="warn-box" style="margin-top:10px;background:#1a1000;border-color:#f39c12;padding:8px;font-size:11px">
        <b>Key:</b> FINTRAC registration under PCMLTFA required identity verification of beneficial owners. RCMP/CBSA can obtain this via domestic production order — no MLAT needed.
      </div>
    </div>
  </div>

  <h3 style="color:#f0f6fc;font-size:13px;margin:16px 0 8px">Full Domain Network (Same Operation)</h3>
  <table>
    <thead><tr><th>Domain</th><th>Registered</th><th>Registrar / Host</th><th>Role</th></tr></thead>
    <tbody>
      <tr><td style="font-family:monospace;font-size:11px">deptoy.co</td><td>May 2024</td><td>Let's Encrypt SSL (active May–Dec 2024)</td><td>Victim-facing fake exchange (direct victim)</td></tr>
      <tr><td style="font-family:monospace;font-size:11px">bippax.com</td><td>2024-06-21</td><td>Adriatic Domains / Trellian AU (IP: 103.224.212.213)</td><td>Main BIPPAX brand platform</td></tr>
      <tr><td style="font-family:monospace;font-size:11px">bippaxcoins.com</td><td>2023-04-03</td><td><b>GoDaddy</b> / Domains By Proxy / Acquia Hosting</td><td>Alternate BIPPAX domain — GoDaddy subpoena target</td></tr>
      <tr><td style="font-family:monospace;font-size:11px">bissnex.com</td><td>2023+</td><td>—</td><td>Corporate website for BISSNEX entity</td></tr>
      <tr><td style="font-family:monospace;font-size:11px">byxgcoins.com</td><td>2023-02-17</td><td><b>GoDaddy</b> / Domains By Proxy / <b>Alibaba</b> hosting</td><td>Prior platform deployment</td></tr>
      <tr><td style="font-family:monospace;font-size:11px">byxgexchange.com</td><td>2023-02-17</td><td>GoDaddy / Alibaba</td><td>Prior platform deployment · Subdomains: agent.byxgexchange.com · pay.byxgexchange.com · m.byxgexchange.com · active SSL certs through 2024-02-27</td></tr>
      <tr><td style="font-family:monospace;font-size:11px">aztexchange.com</td><td>2023-08-09</td><td><b>GoDaddy</b> / Domains By Proxy / <b>Alibaba</b> hosting</td><td>Parallel platform · Subdomains: *.aztexchange.com confirmed via SSL certs</td></tr>
      <tr><td style="font-family:monospace;font-size:11px">aztexcoins.com</td><td>2023-08-25</td><td>GoDaddy / Alibaba · TrustAsia cert (C=CN)</td><td>Parallel platform · Subdomains: agent.aztexcoins.com · api.aztexcoins.com · m.aztexcoins.com · static.aztexcoins.com</td></tr>
      <tr><td style="font-family:monospace;font-size:11px;color:#ff6b6b"><b>aztexchange.com (NEW)</b></td><td><b>2026-03-01</b></td><td>Realtime Register B.V. (Netherlands) — <b style="color:#ff6b6b">SUSPENDED</b> by registrar</td><td><b style="color:#ff6b6b">⚠ ACTIVE OPERATION:</b> New domain registered 23 days ago, SSL cert immediately issued, then suspended (clientHold). Operation attempted new infrastructure in March 2026 — confirms ongoing criminal activity. Abuse contact: rtr-security-threats@realtimeregister.com</td></tr>
      <tr><td style="font-family:monospace;font-size:11px">bitspaie.com</td><td>—</td><td>—</td><td>Email domain (support@, ceo@, apply@, coop@) — prior deployment</td></tr>
      <tr><td style="font-family:monospace;font-size:11px">bitspaieex.com</td><td>—</td><td>—</td><td>In deptoy.co JS source — "anwerbung@" German recruitment email</td></tr>
      <tr><td style="font-family:monospace;font-size:11px">bit-swap.net</td><td>2023-07-10</td><td>—</td><td>Platform — Cryptolly app</td></tr>
      <tr><td style="font-family:monospace;font-size:11px">coinbf.com</td><td>2023-08-11</td><td>—</td><td>Platform variant</td></tr>
      <tr><td style="font-family:monospace;font-size:11px">elwallets.com</td><td>2022-05-27</td><td>—</td><td>Earliest linked domain (pre-BIPPAX branding)</td></tr>
      <tr><td style="font-family:monospace;font-size:11px">userhelpsdesk.com</td><td>2023-06-05</td><td>—</td><td>Fake customer support (customer-feedback@userhelpsdesk.com)</td></tr>
    </tbody>
  </table>

  <h3 style="color:#f0f6fc;font-size:13px;margin:16px 0 8px">Known Operator Personas &amp; Handles</h3>
  <table>
    <thead><tr><th>Identifier</th><th>Platform</th><th>Role</th><th>Notes</th></tr></thead>
    <tbody>
      <tr><td style="font-family:monospace">bmate601</td><td>WeChat</td><td>Customer service operator</td><td>Confirmed banned — account was active during deptoy.co period</td></tr>
      <tr><td style="font-family:monospace">bizzzan01</td><td>WeChat</td><td>Second customer service operator</td><td>Found in same JS context as bmate601 — likely same naming pool (bmate/bizz)</td></tr>
      <tr><td style="font-family:monospace">883le</td><td>WeChat</td><td>Unknown — possible affiliate/agent</td><td>In WeChat context block — shorter handle suggests senior or different role</td></tr>
      <tr><td style="font-family:monospace">coinex</td><td>WeChat / Telegram / Weibo / Twitter</td><td>Platform social impersonation</td><td>Fake CoinEx exchange account used across all platforms for social proof</td></tr>
      <tr><td style="font-family:monospace">Professor Bingham</td><td>WhatsApp</td><td>Group leader / signals provider</td><td>WhatsApp investment group recruiter — likely one of multiple personas</td></tr>
      <tr><td style="font-family:monospace">Susan / Bexley</td><td>WhatsApp</td><td>Group operators</td><td>"Caryle &amp; BIPPAX-185" WhatsApp group — Susan and Bexley = operator personas</td></tr>
      <tr><td style="font-family:monospace">Jack Williams</td><td>Canada Corp</td><td>Director of record</td><td>Fictitious Anglo name on federal filing — real person's ID required by Corporations Canada</td></tr>
      <tr><td style="font-family:monospace">Darryl Joel Dorfman</td><td>Corporate fiction</td><td>Claimed BYXG founder</td><td>Linked to BYXG Cryptocurrency Group Ltd — likely fabricated identity</td></tr>
    </tbody>
  </table>

  <h3 style="color:#f0f6fc;font-size:13px;margin:16px 0 8px">Email Addresses Attributed to This Network</h3>
  <div style="display:flex;flex-wrap:wrap;gap:6px;margin-bottom:12px">
    <code style="background:#161b22;padding:4px 8px;border-radius:4px;font-size:11px">Promotion@BIPPAX.com</code>
    <code style="background:#161b22;padding:4px 8px;border-radius:4px;font-size:11px">promotion@BIPPAX.com</code>
    <code style="background:#161b22;padding:4px 8px;border-radius:4px;font-size:11px">service@bippax.com</code>
    <code style="background:#161b22;padding:4px 8px;border-radius:4px;font-size:11px">anwerbung@bitspaieex.com</code>
    <code style="background:#161b22;padding:4px 8px;border-radius:4px;font-size:11px">support@bitspaie.com</code>
    <code style="background:#161b22;padding:4px 8px;border-radius:4px;font-size:11px">apply@bitspaie.com</code>
    <code style="background:#161b22;padding:4px 8px;border-radius:4px;font-size:11px">ceo@bitspaie.com</code>
    <code style="background:#161b22;padding:4px 8px;border-radius:4px;font-size:11px">coop@bitspaie.com</code>
    <code style="background:#161b22;padding:4px 8px;border-radius:4px;font-size:11px">bippax0319@hotmail.com</code>
    <code style="background:#161b22;padding:4px 8px;border-radius:4px;font-size:11px">CBOTiYEX2022@hotmail.com</code>
    <code style="background:#161b22;padding:4px 8px;border-radius:4px;font-size:11px">barbarafelixv7@gmail.com</code>
    <code style="background:#161b22;padding:4px 8px;border-radius:4px;font-size:11px">support@bissnex.com</code>
    <code style="background:#161b22;padding:4px 8px;border-radius:4px;font-size:11px">customer-feedback@userhelpsdesk.com</code>
  </div>

  <h3 style="color:#f0f6fc;font-size:13px;margin:16px 0 8px">Network Size Analysis</h3>
  <div style="background:#161b22;border:1px solid #30363d;border-radius:8px;padding:16px">
    <table style="font-size:12px;width:100%">
      <thead><tr><th>Role</th><th>Evidence</th><th>Estimated Count</th></tr></thead>
      <tbody>
        <tr><td>Technical platform operators</td><td>CentOS server management, BIPPAX white-label deployment, Vue.js app, API server</td><td>2–3</td></tr>
        <tr><td>WeChat customer service agents</td><td>bmate601 (banned), bizzzan01, 883le — likely a numbered pool</td><td>3–8</td></tr>
        <tr><td>WhatsApp/Telegram recruiters</td><td>Professor Bingham, Susan, Bexley — per-group operators across 13 language regions</td><td>5–10</td></tr>
        <tr><td>Domain / corporate shell management</td><td>14+ domains registered, Canadian/Cayman corporate entities, FINTRAC MSB</td><td>1–2</td></tr>
        <tr><td>BTC laundering / money handling</td><td>Pivot address (64,255 BTC), 7-hop chain, 140 BTC direct to scammer</td><td>1–3</td></tr>
        <tr><td>Senior principals / organizers</td><td>140 BTC + 395,190 BTC total scammer wallet volume (64,255 BTC via deptoy pivot) — full-time operation since 2020</td><td>2–4</td></tr>
        <tr style="background:#1c1010"><td><b>Estimated total</b></td><td>All roles, active 2020–2025, 13 language regions</td><td><b>15–28 people</b></td></tr>
      </tbody>
    </table>
    <div class="warn-box" style="margin-top:12px;background:#1a0a00;border-color:#e67e22;font-size:11px">
      <b>⚠ FRAUDULENT VC CLAIMS IN PRESS RELEASES (additional wire fraud evidence):</b>
      BISSNEX's December 2023 GlobeNewswire press releases falsely claim funding from
      <b>Paradigm</b>, <b>NGC Ventures</b>, <b>Multicoin Capital</b>, and <b>Pantera Capital</b> — all well-known legitimate crypto venture firms.
      None of these firms have any disclosed investment in BISSNEX. These false claims constitute securities fraud / wire fraud under 18 USC §1343
      and can be verified by contacting each firm's PR/legal teams. The press releases were distributed from "New York, NY" despite corporate
      registration in Toronto — a further misrepresentation. GlobeNewswire (Notified) holds the submitting account's payment and identity records.
    </div>
    <div class="info-box" style="margin-top:10px;font-size:11px">
      The naming pattern <b>bmate601</b> / <b>bizzzan01</b> strongly suggests a numbered agent pool — the 601/01 suffixes imply many more accounts exist. The operation maintained at least 14 domains, a Google Play app (1000+ downloads), German/Italian/Japanese/Korean/Indonesian language support, and a FINTRAC-registered Canadian entity from 2020–2025. This is not a small group.
    </div>
  </div>

  <h3 style="color:#f0f6fc;font-size:13px;margin:16px 0 8px">MLAT &amp; Jurisdictional Subpoena Guide</h3>
  <table>
    <thead><tr><th>Jurisdiction</th><th>Target</th><th>Legal Mechanism</th><th>Expected Intelligence</th></tr></thead>
    <tbody>
      <tr>
        <td><b>Canada</b></td>
        <td>Corporations Canada · FINTRAC (M20852872)</td>
        <td>Domestic production order (RCMP/CBSA) — no MLAT needed, Canada is Five Eyes</td>
        <td><b>Real identity of beneficial owner behind "Jack Williams" — passport, SIN, bank records</b></td>
      </tr>
      <tr>
        <td><b>USA</b></td>
        <td>GoDaddy (Scottsdale, AZ) — bippaxcoins.com, byxgcoins.com, aztexchange.com</td>
        <td>18 USC §2703 subpoena — US company, fast compliance</td>
        <td>Domain registrant identity, payment method, billing address, IP addresses used at registration</td>
      </tr>
      <tr>
        <td><b>USA</b></td>
        <td>Google (Play Store) — BIPPAX app, T-AUZ Ultra app developer accounts</td>
        <td>18 USC §2703 subpoena</td>
        <td>Developer account email, payment info, APK signing key, geographic location of uploads</td></tr>
      <tr>
        <td><b>USA</b></td>
        <td>Microsoft (Hotmail) — bippax0319@hotmail.com, CBOTiYEX2022@hotmail.com</td>
        <td>18 USC §2703 subpoena</td>
        <td>Account creation IP, recovery phone/email, login history</td>
      </tr>
      <tr>
        <td><b>USA</b></td>
        <td>Google (Gmail) — barbarafelixv7@gmail.com</td>
        <td>18 USC §2703 subpoena</td>
        <td>Account creation IP, recovery info, login history</td>
      </tr>
      <tr>
        <td><b>China</b> (via MLAT)</td>
        <td>Tencent/WeChat — bmate601, bizzzan01, 883le, coinex handles</td>
        <td>MLAT through DOJ Office of International Affairs → Ministry of Justice China · or Interpol NCB Beijing</td>
        <td>Real phone number linked at registration, IP logs, chat history, payment records (WeChat Pay)</td>
      </tr>
      <tr>
        <td><b>China</b> (via MLAT)</td>
        <td>MIIT — 沪ICP备13026899号-3 registrant</td>
        <td>MLAT → MIIT holds Chinese business entity name + legally responsible person</td>
        <td>Company name, legal representative name, ID number, contact details — legally required by Chinese law</td>
      </tr>
      <tr>
        <td><b>Australia</b></td>
        <td>Trellian Pty Ltd — bippax.com hosting (IP: 103.224.212.213)</td>
        <td>Australian Federal Police mutual assistance → AUSTRAC</td>
        <td>Server logs, customer account data, payment records for bippax.com hosting</td>
      </tr>
      <tr>
        <td><b>Cayman Islands</b></td>
        <td>CIMA (Cayman Islands Monetary Authority)</td>
        <td>MLAT or direct request — Cayman has anti-money laundering cooperation framework</td>
        <td>If BIPPAX.PRO is actually registered there, CIMA holds beneficial ownership under OECD exchange framework</td>
      </tr>
      <tr>
        <td><b>Binance</b></td>
        <td>Account linked to 34HVDP9RFA9MpopGQ4TutLLVMFhhJFM9AX (original theft)</td>
        <td>Binance LE portal / Binance.US subpoena</td>
        <td>KYC identity of aggregator wallet owner — highest value single target for original 2022 theft</td>
      </tr>
    </tbody>
  </table>
</div>"""

    # ── Law enforcement copy block ─────────────────────────────────────────────
    le_package = f"""================================================================================
LAW ENFORCEMENT EVIDENCE PACKAGE — PIG BUTCHERING / ROMANCE SCAM
Generated: {generated_at}
Prepared for submission to: FBI IC3 · RCMP · Interpol NCB
================================================================================

--- CASE OVERVIEW ---
This report documents two separate theft incidents against the same victim,
both traceable to the same criminal organization via blockchain analysis.

INCIDENT 1 — Romance scam / pig butchering (2022-07-31)
  Victim address  : 3MT5t24cF88QzZ5qjgfDioC79pvyQDsojt
  Amount stolen   : 0.84758448 BTC (~$19,833 at theft · ~$80,500 today)
  Method          : Full wallet sweep, 41-output fan-out, automated laundering
  Ultimate dest.  : {target} (via relay + aggregator → Binance)

INCIDENT 2 — Fake cryptocurrency exchange deptoy.co (July–August 2024)
  Platform        : deptoy.co (BIPPAX fake exchange)
  Amount stolen   : 0.14970240 BTC (~$10,040 USD at time of theft, 2024-07-25/26)
  TX 1 (2024-07-25): e81ac50854e47dddfb955cf3ff9dfebe05d3016c759de8e1c23719620dfccc08 (0.07622126 BTC)
  TX 2 (2024-07-26): ef504db1bb3800700198eae26a7ca97a455aed0f6f835dfa115efbca23dc581d (0.07348114 BTC)
  Victim deposit address: 129z2g1vNMvVes3yiwbnVS8KtMSZFGm7Mc (deptoy.co-assigned)
  Sending exchange: bc1qprdf80adfz7aekh5nejjfrp3jksc8r929svpxk (14M BTC Robinhood Crypto hot wallet (confirmed by victim))
  Sweep TX: 4a512679c63b3a8186b48d6251511e89ff2fd32ab8608c1984264f7d7dc67d12 (70+ victims swept simultaneously)
  Corporate entity: BISSNEX CRYPTO GROUP LIMITED
    Canada corp # : 1231288-3 (federal, incorporated 2020-09-02)
    FINTRAC MSB # : M20852872 (money service business)
    Director filed: JACK WILLIAMS (likely fictitious — real ID held by Corporations Canada)
    Address        : 20 Leslie St, Toronto, ON M4M 3L4
  Ultimate dest.  : 6-hop chain → terminal wallet (now empty)

CRITICAL LINK — SAME CRIMINAL ORGANIZATION:
  The deptoy.co aggregation wallet 3JMjHDTJjKPnrvS7DycPAgYcA6HrHRk8UG
  sent 140.000000 BTC in 7 direct transactions to {target} — the
  same wallet that received the 2022 theft. Same private key = same operator.
  Total criminal enterprise: 395,190 BTC total received at subject wallet (5,170 txs). Deptoy.co pivot alone processed 64,255 BTC (25,117 txs). Last outbound tx: 2026-01-21 — OPERATION ONGOING.

TOP PRIORITY SUBPOENA TARGETS (no MLAT required):
  1. RCMP / Corporations Canada — Corp #1231288-3: real ID behind "Jack Williams"
     (domestic production order — Five Eyes, no MLAT needed)
  2. Binance — account linked to aggregator 34HVDP9RFA9MpopGQ4TutLLVMFhhJFM9AX
     (18 USC §2703 — Binance.US, BAM Trading Services Inc.)
  3. GoDaddy LLC (Scottsdale, AZ) — registrant behind bippaxcoins.com, byxgcoins.com
     (18 USC §2703)

MLAT TARGETS (require treaty process):
  4. Tencent/WeChat (China) — accounts bmate601, bizzzan01, 883le
  5. MIIT (China) — 沪ICP备13026899号-3 registrant identity

--- SUBJECT WALLET ---
Scammer BTC address : {target}
Total received      : {float(addr_info.get('total_received_btc',0)):,.4f} BTC
Active period       : {first_seen} to {last_seen}
On-chain transactions: {len(set(t['txid'] for t in all_txs))} unique txids

--- VICTIM DETAILS ---
Victim address      : {victim.get('victim_address','')}
Victim funding TX   : cbd6b435d189b6ba05216098a7bdf7e90be617936001dba0d55ba1d88ff41541
  Block height      : 747293
  Funding source    : 38ABnUgrfwLg3wdP5jbytmGWKqskh3QvwE (9 UTXOs consolidated)
  Note              : Funding source may be scammer-controlled (seeded victim address)
Victim spending TX  : {stx.get('txid','')}
  Block height      : {stx.get('block_height','')}
  Block timestamp   : 2022-07-31 (UTC)
  Inputs            : {stx.get('num_inputs',0)}
  Outputs           : {stx.get('num_outputs',0)} (fan-out sweep — zero change returned)
  TX fee paid       : {TX_FEE_SAT:,} satoshis
Amount stolen       : {STOLEN_BTC:.8f} BTC ({STOLEN_SAT:,} satoshis)
  USD at theft date : ~${USD_AT_THEFT:,.0f} (BTC ≈ $23,400 on 2022-07-31)
  USD per receipt   : $81,605.74 (blockexplorer.one receipt, BTC price at 2025-02-17)
  USD current value : ~${USD_NOW:,.0f} (BTC ≈ $95,000 on {generated_at[:10]})
TX timestamp        : 2022-07-31 03:09:14 UTC
TX fee              : {TX_FEE_SAT:,} satoshis ({TX_FEE_BTC:.8f} BTC)
Change returned     : 0 satoshis (full balance swept)
Receipt source      : blockexplorer.one · generated 2025-02-17T00:56:59+00:00

--- CRYPTOGRAPHIC EVIDENCE ---
Victim public key   : {pubkeys[0]['pubkey'] if pubkeys else 'N/A'}
  (extracted from witness data of spending TX — uniquely identifies the key holder)

--- MONEY TRAIL ---
STEP 1: Victim 3MT5t24cF88QzZ5qjgfDioC79pvyQDsojt
        → TX 02ab77e433e9aaf3f78f8ccb65090a4dae8698de6f987d10b5d4c3c453984c69 (Block 747298)
        → Relay  3R1Gs7RniDHRc6Trn214gVffSErYMbGuJ6  (0.46 BTC largest output)

STEP 2: Relay 3R1Gs7RniDHRc6Trn214gVffSErYMbGuJ6
        → Aggregator 34HVDP9RFA9MpopGQ4TutLLVMFhhJFM9AX
        (8.65 BTC total received at relay; 3,294 on-chain txs at aggregator)

STEP 3: Aggregator 34HVDP9RFA9MpopGQ4TutLLVMFhhJFM9AX
        → Binance hot wallet bc1quhruqrghgcca950rvhtrg7cpd7u8k6svpzgzmrjy8xyukacl5lkq0r8l2d
        (97.25 BTC total across 34 transactions)
        **Binance has KYC records for the account that owns this aggregator address**

STEP 4: Scammer wallet 3GH4EhMi1MG8rxSiAWqfoiUCMLaWPTCxuy (HOP-1/HOP-2)
        → bc1qm34lsc65zpw79lxes69zkqmk6ee3ewf0j77s3h (known Binance hot wallet)
          472.52 BTC · 2,173,077 on-chain txs
        → bc1quhruqrghgcca950rvhtrg7cpd7u8k6svpzgzmrjy8xyukacl5lkq0r8l2d (Binance)
          436.66 BTC · 335,452 txs · 5,447,353 BTC lifetime received

--- EXCHANGE ATTRIBUTION ---
Primary exchange    : Binance (BAM Trading Services Inc. in the US)
Confidence          : HIGH — 4 independent evidence lines (see report)
Exchange addresses  : {len(exchanges_found)} deposit addresses identified in trace
Subpoena targets    :
  1. Binance — account linked to 34HVDP9RFA9MpopGQ4TutLLVMFhhJFM9AX
  2. Binance — account(s) linked to 1JpeKeUVhRYWCzA3roGCABcmLLnkMgRntm (500 BTC hop-1)
  3. Any exchange holding 3JMjHDTJjKPnrvS7DycPAgYcA6HrHRk8UG (pivot/aggregator)

--- DEPTOY.CO / BIPPAX PLATFORM (linked to same criminal network) ---
Platform name       : BIPPAX (fake cryptocurrency exchange)
Official brand      : BIPPAX.PRO (self-stated in English source)
Domain              : deptoy.co (registered May 2024, now offline)
Alternate domain    : www.bippaxcoins.com (hardcoded in platform source)
API domain          : api.deptoy.co
WeChat customer svc : bmate601 (confirmed banned) · bizzzan01 (second operator)
Additional handle   : 883le (WeChat/social context in platform source)
Platform email      : Promotion@BIPPAX.com / promotion@BIPPAX.com
Recruitment email   : anwerbung@bitspaieex.com (bitspaieex.com = probable prior BIPPAX deployment)
ICP registration    : 沪ICP备13026899号-3 (MIIT database — holds registrant business entity + responsible person)
Corporate claim     : Registered in Cayman Islands, core team in Hong Kong (self-stated in platform)
Server OS           : CentOS Linux (confirmed from api.deptoy.co default Apache page)
Admin modules found : addressmanager, assetmanage, financial_management, innovationmanage, managerfee, trademanage

ON-CHAIN LINK — Pivot address bridges deptoy.co to scammer wallet:
  Pivot address     : 3JMjHDTJjKPnrvS7DycPAgYcA6HrHRk8UG
  Total processed   : 64,255.78 BTC · 25,117 on-chain txs
  Sent to scammer   : 140.000000 BTC in 7 transactions

  Direct transactions (Pivot → Scammer):
    2024-02-29  9e13b5434ceceef380a47119bb5ad489007eff4983e02b0c9b2cf4480484e256  50.00 BTC
    2024-06-03  1d50ec9afbb10fd20aeaad25ff31384ddb4a98386e5f443684009f090a6ef0c4  20.00 BTC
    2024-09-27  954f8ae890e428b5ecd08aec11de8d59857c6dd6a4ce477c28b976d69e9869c0  20.00 BTC
    2024-11-02  39e3ed3fbec32c5f61303564898dccf65cd7157d3796568644878104be9f9ef5  20.00 BTC
    2024-12-12  2277732773156dcb859006d776706d45018dea5897452bb7d6cee4eb9ff8a630  20.00 BTC
    2025-01-28  471189025a911b5dcf905d505d8a10298a3baac248901cc5d6124a5289edf514   5.00 BTC (300+ victim UTXOs consolidated)
    2025-08-12  01b2e703c9fb821317ab6428b9cccae983818e7ff4569fdf948fdc263652753d   5.00 BTC

SECOND THEFT CHAIN (Aug 2024 deptoy.co deposit, ~$10,000):
  Hop 0 (exchange): bc1qprdf80adfz7aekh5nejjfrp3jksc8r929svpxk  (183,572 txs · 14,036,540 BTC — Robinhood Crypto LLC hot wallet, confirmed by victim)
  Hop 1 (swept addr): 129z2g1vNMvVes3yiwbnVS8KtMSZFGm7Mc          (0.1497 BTC · 3 txs · deposit address)
  Hop 2 (consolidator): 1NjU5czLRBWn89LmWHfyq9Vi8Fskjqy6kA        (13.83 BTC · 37 txs · ~50+ victims)
  Hop 3 (aggregator): 3NWjDQkpSQTnjtJSUwVpnC2ivLCZr1zGKu          (4.49 BTC · 29 txs)
  Hop 4 (collection): 145hFvPqPLWevK5TNpAXkMNpGEYBXhB66z           (37.39 BTC · 120 txs · cluster 6cbec0582a)
  Hop 5 (aggregator): 323XtjvdYZMJp3CAJ2SbJMUcAyV4VmZgc7          (15.76 BTC · 108 txs · cluster 329c3b500b)
  Hop 6 (terminal):  bc1q2u2eyvnndad0dlqmrwzp0pncaxpn9ka40f47mk  (15.72 BTC · 119 txs · now empty)

Additional subpoena targets (deptoy.co investigation):
  4.  WeChat/Tencent — account bmate601 (platform customer service, confirmed banned)
  5.  WeChat/Tencent — account bizzzan01 (second operator found in same source)
  6.  WeChat/Tencent — account 883le (third handle in WeChat context)
  7.  Email host — Promotion@BIPPAX.com registration/IP records
  8.  Email host — anwerbung@bitspaieex.com (bitspaieex.com domain registration + hosting)
  9.  Domain registrar — deptoy.co + www.bippaxcoins.com registration/payment records
  10. Hosting provider — api.deptoy.co server logs
  11. MIIT — 沪ICP备13026899号-3 registrant details (via MLAT or judicial assistance)
  12. Robinhood Crypto LLC — victim's account withdrawal records (two txs 2024-07-25/26 totalling 0.14970 BTC) · 18 USC §2703
  13. GlobeNewswire/Notified — submitting account identity for BISSNEX press releases (Dec 28 2023)
      (fraudulent VC funding claims = wire fraud evidence; GlobeNewswire holds payment+account records)
  14. Paradigm / NGC Ventures / Multicoin Capital / Pantera Capital — confirm they never funded BISSNEX
      (false VC claims in press releases constitute securities fraud / 18 USC §1343)

Report generated: {generated_at}"""

    # ── Exchange alert ────────────────────────────────────────────────────────
    ex_rows = "".join(
        f"<li><code>{ex['address']}</code> — <b>{ex['entity']}</b> — {ex.get('total_btc',0):.4f} BTC</li>"
        for ex in exchanges_found[:10]
    )
    exchange_alert = f'<div class="alert-box"><b>⚡ ACTIONABLE: {len(exchanges_found)} exchange/swept addresses detected.</b> Law enforcement can subpoena KYC.<br><ul style="margin:8px 0 0 20px">{ex_rows}</ul></div>' if exchanges_found else ''

    # ── vis.js data ───────────────────────────────────────────────────────────
    vis_nodes = []
    for n in nodes_raw:
        entity   = n.get('entity', 'Unknown')
        btc_recv = n.get('total_btc_from_target') or n.get('total_btc_from_prev') or 0
        hop_lbl  = {0:'',1:'[H1] ',2:'[H2] '}.get(n.get('hop',1),'')
        vis_nodes.append({
            'id': n['id'], 'color': node_color(n), 'size': node_size(n),
            'label': f"{hop_lbl}{entity[:20]}\n{n['id'][:14]}…",
            'title': (f"<b>{n['id']}</b><br>Entity: {entity}<br>Hop: {n.get('hop','?')}<br>"
                      f"BTC: {btc_recv:.6f}<br>Chain txs: {n.get('tx_count_chain',0):,}<br>"
                      f"Balance: {n.get('balance_btc',0):.6f} BTC<br>"
                      f"<a href='https://mempool.space/address/{n['id']}' target='_blank'>mempool.space ↗</a>"),
        })

    edge_map = {}
    for e in edges_raw:
        key = (e['from'], e['to'])
        if key in edge_map:
            edge_map[key]['value'] += e['amount_btc']
            edge_map[key]['count'] += 1
        else:
            edge_map[key] = {'from':e['from'],'to':e['to'],'value':e['amount_btc'],'count':1,'hop':e.get('hop',1)}
    vis_edges = [
        {'from':ed['from'],'to':ed['to'],'value':ed['value'],'arrows':'to',
         'title':f"{ed['value']:.4f} BTC ({ed['count']} txs)",
         'color':{'color':'#58a6ff' if ed['hop']==1 else '#9b59b6','opacity':0.5}}
        for ed in edge_map.values()
    ]

    # ── Table row builder ─────────────────────────────────────────────────────
    def table_rows(entries, show_via=False, table_id=''):
        rows = ""
        for e in entries:
            entity = e.get('entity', 'Unknown')
            bc     = badge_color(entity)
            dates  = sorted(set(e.get('dates', [])))
            dates_str = ', '.join(dates[:4]) + (f' (+{len(dates)-4})' if len(dates) > 4 else '')
            first_d = dates[0] if dates else ''
            last_d  = dates[-1] if dates else ''
            btc_val = e.get('total_btc', e.get('total_btc_from_prev', 0))
            via_cell = (f'<td style="font-size:10px;font-family:monospace"><a href="https://mempool.space/address/{e["via_addr"]}" target="_blank">{e.get("via_addr","")[:22]}…</a></td>'
                        if show_via else '')
            rows += f"""<tr>
              <td style="font-size:11px;font-family:monospace"><a href="https://mempool.space/address/{e['address']}" target="_blank">{e['address']}</a></td>
              <td style="text-align:right;font-weight:bold" data-val="{btc_val}">{btc_val:.6f}</td>
              <td style="text-align:right" data-val="{e.get('tx_count',0)}">{e.get('tx_count','—')}</td>
              <td style="text-align:right" data-val="{e.get('chain_tx_count',0)}">{e.get('chain_tx_count',0):,}</td>
              <td style="text-align:right" data-val="{e.get('balance_btc',0)}">{e.get('balance_btc',0):.6f}</td>
              <td><span style="background:{bc};color:#111;padding:1px 6px;border-radius:3px;font-size:10px;font-weight:bold">{entity}</span></td>
              {via_cell}
              <td style="font-size:10px" data-val="{first_d}">{dates_str}</td>
            </tr>"""
        return rows

    hop1_rows    = table_rows(hop1,         table_id='tbl-hop1')
    hop2_rows    = table_rows(hop2,         show_via=True, table_id='tbl-hop2')
    highvol_rows = table_rows(high_vol,     table_id='tbl-hv')

    # ── Render ────────────────────────────────────────────────────────────────
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>BTC Scam Trace — {target[:18]}…</title>
<script src="https://cdn.jsdelivr.net/npm/vis-network@9.1.2/dist/vis-network.min.js"></script>
<link  href="https://cdn.jsdelivr.net/npm/vis-network@9.1.2/dist/dist/vis-network.min.css" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:'Segoe UI',Arial,sans-serif;background:#0d1117;color:#c9d1d9;font-size:13px}}
.header{{background:#161b22;padding:18px 28px;border-bottom:2px solid #e74c3c}}
.header h1{{color:#e74c3c;font-size:20px;margin-bottom:4px}}
.header .sub{{color:#8b949e;font-size:12px}}
.stats{{display:flex;gap:12px;padding:14px 28px;flex-wrap:wrap;background:#0d1117}}
.card{{background:#161b22;border:1px solid #30363d;border-radius:8px;padding:12px 16px;min-width:140px}}
.card .lbl{{font-size:10px;color:#8b949e;text-transform:uppercase;letter-spacing:.5px}}
.card .val{{font-size:18px;font-weight:700;color:#f0f6fc;margin-top:3px}}
.card .sub2{{font-size:10px;color:#8b949e;margin-top:2px}}
.section{{padding:16px 28px}}
.section h2{{color:#f0f6fc;font-size:14px;border-bottom:1px solid #30363d;padding-bottom:8px;margin-bottom:12px}}
#net{{width:100%;height:580px;background:#161b22;border:1px solid #30363d;border-radius:8px}}
.charts{{display:grid;grid-template-columns:1fr 320px;gap:14px;margin-bottom:6px}}
.chart-box{{background:#161b22;border:1px solid #30363d;border-radius:8px;padding:14px}}
.chart-box h3{{font-size:12px;color:#8b949e;margin-bottom:10px;text-transform:uppercase;letter-spacing:.5px}}
table{{width:100%;border-collapse:collapse}}
th{{background:#161b22;color:#8b949e;text-align:left;padding:7px 8px;border-bottom:1px solid #30363d;font-size:10px;text-transform:uppercase;white-space:nowrap;position:sticky;top:0;z-index:1}}
th.sortable{{cursor:pointer;user-select:none}}
th.sortable:hover{{color:#f0f6fc}}
th.sort-asc::after{{content:' ↑'}}
th.sort-desc::after{{content:' ↓'}}
td{{padding:6px 8px;border-bottom:1px solid #21262d;vertical-align:middle}}
tr:hover td{{background:#161b22}}
a{{color:#58a6ff;text-decoration:none}}
a:hover{{text-decoration:underline}}
.alert-box{{background:#1c2a1c;border:1px solid #2ecc71;border-radius:6px;padding:14px 18px;margin:10px 0;color:#a8e6b0}}
.warn-box{{background:#2a1a00;border:1px solid #d08020;border-radius:6px;padding:14px 18px;margin:10px 0;color:#ffa657}}
.info-box{{background:#0d1f2d;border:1px solid #1f6feb;border-radius:6px;padding:14px 18px;margin:10px 0;color:#79c0ff}}
.legend{{display:flex;gap:16px;margin-bottom:10px;flex-wrap:wrap}}
.li{{display:flex;align-items:center;gap:5px;font-size:11px}}
.dot{{width:11px;height:11px;border-radius:50%;flex-shrink:0}}
.tabs{{display:flex;gap:0}}
.tab{{padding:7px 16px;cursor:pointer;background:#161b22;border:1px solid #30363d;border-bottom:none;color:#8b949e;border-radius:4px 4px 0 0;font-size:12px}}
.tab.active{{background:#0d1117;color:#f0f6fc;border-bottom:1px solid #0d1117}}
.tab-body{{border:1px solid #30363d;border-radius:0 4px 4px 4px;overflow:auto;max-height:460px}}
.hidden{{display:none}}
.badge{{padding:1px 6px;border-radius:3px;font-size:10px;font-weight:bold;color:#111}}
/* Money trail */
.trail{{display:flex;flex-direction:column;align-items:flex-start;gap:0;margin:10px 0}}
.trail-step{{border:1px solid #30363d;border-radius:6px;padding:10px 16px;min-width:600px;max-width:900px}}
.trail-arrow{{font-size:18px;color:#8b949e;margin:2px 20px}}
.ts-label{{font-size:10px;text-transform:uppercase;letter-spacing:.5px;color:#8b949e;margin-bottom:3px}}
.ts-addr{{font-family:monospace;font-size:12px;word-break:break-all}}
.ts-val{{font-size:11px;color:#8b949e;margin-top:3px}}
.s-victim  {{background:#1c1010;border-color:#e74c3c}}
.s-relay   {{background:#161b22;border-color:#30363d}}
.s-agg     {{background:#1a1a10;border-color:#f39c12}}
.s-exchange{{background:#0d2010;border-color:#2ecc71}}
/* Copy button */
.copy-btn{{float:right;background:#21262d;border:1px solid #30363d;color:#8b949e;padding:3px 10px;border-radius:4px;cursor:pointer;font-size:11px}}
.copy-btn:hover{{background:#30363d;color:#f0f6fc}}
pre.le-block{{background:#161b22;border:1px solid #30363d;border-radius:6px;padding:14px;font-size:11px;line-height:1.7;white-space:pre-wrap;word-break:break-all;color:#a8e6b0}}
</style>
</head>
<body>

<div class="header">
  <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:8px">
    <div>
      <div style="font-size:10px;letter-spacing:2px;text-transform:uppercase;color:#8b949e;margin-bottom:6px">LAW ENFORCEMENT EVIDENCE PACKAGE</div>
      <h1 style="font-size:22px;margin-bottom:6px">Pig Butchering / Romance Scam — Blockchain Trace Report</h1>
      <div class="sub"><b>Victim:</b> Address <code style="color:#ffa657">3MT5t24cF88QzZ5qjgfDioC79pvyQDsojt</code> &nbsp;|&nbsp; <b>Subject wallet:</b> <code style="color:#e74c3c">{target}</code></div>
      <div class="sub" style="margin-top:4px">Generated: {generated_at} &nbsp;|&nbsp; All blockchain data sourced from public records (mempool.space / blockstream.info)</div>
    </div>
    <div style="background:#1c0a0a;border:1px solid #e74c3c;border-radius:6px;padding:10px 16px;font-size:12px;min-width:200px">
      <div style="color:#e74c3c;font-weight:bold;margin-bottom:4px">TWO CONFIRMED THEFTS</div>
      <div>① 2022-07-31 — <b>0.848 BTC</b> (~$19,833)</div>
      <div>② Aug 2024 — <b>~$10,000 USD</b></div>
      <div style="color:#8b949e;font-size:10px;margin-top:4px">Both traceable to same criminal network</div>
    </div>
  </div>
</div>

<!-- ── EXECUTIVE SUMMARY ──────────────────────────────────────────────────── -->
<div style="background:#161b22;border-left:4px solid #e74c3c;padding:18px 28px;border-bottom:1px solid #30363d">
  <div style="font-size:10px;letter-spacing:2px;text-transform:uppercase;color:#8b949e;margin-bottom:10px">Executive Summary — For Law Enforcement</div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px;max-width:1100px">
    <div>
      <div style="color:#f0f6fc;font-weight:bold;margin-bottom:8px;font-size:13px">INCIDENT 1 — Romance / Pig Butchering Scam (2022)</div>
      <ul style="font-size:12px;line-height:1.8;margin-left:16px;color:#c9d1d9">
        <li><b>Date:</b> 2022-07-31 03:09 UTC</li>
        <li><b>Stolen:</b> 0.84758448 BTC (~$19,833 at theft · ~$80,500 today)</li>
        <li><b>From:</b> Victim address <code>3MT5t24cF88QzZ5qjgfDioC79pvyQDsojt</code></li>
        <li><b>Method:</b> Full balance swept in single TX with 41 fan-out outputs — automated laundering software</li>
        <li><b>Destination:</b> Subject wallet <code style="color:#e74c3c">{target}</code> (via 2-hop relay)</li>
        <li><b>Exchange link:</b> Aggregator wallet forwarded 97.25 BTC to <b>Binance</b> — KYC available via subpoena</li>
      </ul>
    </div>
    <div>
      <div style="color:#f0f6fc;font-weight:bold;margin-bottom:8px;font-size:13px">INCIDENT 2 — Fake Exchange Platform deptoy.co (Aug 2024)</div>
      <ul style="font-size:12px;line-height:1.8;margin-left:16px;color:#c9d1d9">
        <li><b>Date:</b> August 2024</li>
        <li><b>Stolen:</b> ~$10,000 USD deposited to fake exchange platform</li>
        <li><b>Platform:</b> deptoy.co — white-label BIPPAX fake cryptocurrency exchange</li>
        <li><b>Method:</b> Victim instructed to deposit BTC as "investment" — funds collected into aggregator then forwarded</li>
        <li><b>Destination:</b> 6-hop chain ending at terminal wallet (now empty)</li>
        <li><b>Corporate entity:</b> <b>BISSNEX CRYPTO GROUP LIMITED</b> (Canada #1231288-3, FINTRAC M20852872)</li>
      </ul>
    </div>
  </div>

  <div style="margin-top:14px;padding:12px 16px;background:#1c1010;border:1px solid #e74c3c;border-radius:6px;max-width:1100px">
    <div style="color:#e74c3c;font-weight:bold;font-size:12px;margin-bottom:6px">🔗 KEY CONNECTION — SAME CRIMINAL ORGANIZATION BEHIND BOTH THEFTS</div>
    <div style="font-size:12px;line-height:1.8;color:#c9d1d9">
      The deptoy.co / BIPPAX platform aggregation wallet (<code>3JMjHDTJjKPnrvS7DycPAgYcA6HrHRk8UG</code>) sent
      <b>140 BTC in 7 direct transactions</b> to <code style="color:#e74c3c">{target}</code> — the same wallet that received
      the 2022 theft. Only the holder of the private key for <code style="color:#e74c3c">{target}</code> can receive funds there.
      The same person or group stole from this victim in 2022 and again in 2024 via a different platform.
      The wallet has received <b>395,190 BTC total</b> across 5,170 transactions over its lifetime. Deptoy.co/BIPPAX pivot contributed 64,255 BTC (25,117 txs). Most recent transaction: 2026-01-21.
    </div>
  </div>

  <div style="margin-top:12px;padding:12px 16px;background:#0a1a0a;border:1px solid #2ecc71;border-radius:6px;max-width:1100px">
    <div style="color:#2ecc71;font-weight:bold;font-size:12px;margin-bottom:6px">⚡ TOP 3 ACTIONABLE SUBPOENA TARGETS (no MLAT required)</div>
    <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;font-size:12px">
      <div style="background:#0d1117;padding:10px;border-radius:4px">
        <div style="color:#2ecc71;font-weight:bold;margin-bottom:4px">① RCMP / Corporations Canada</div>
        <div style="color:#c9d1d9">Canadian Corp #1231288-3 · FINTRAC M20852872<br>Director "Jack Williams" used government ID at registration — real identity held on file.<br><b>Domestic production order only — no MLAT needed.</b></div>
      </div>
      <div style="background:#0d1117;padding:10px;border-radius:4px">
        <div style="color:#2ecc71;font-weight:bold;margin-bottom:4px">② Binance (via US subpoena)</div>
        <div style="color:#c9d1d9">Aggregator wallet <code>34HVDP9RFA9MpopGQ4TutLLVMFhhJFM9AX</code> sent 97.25 BTC to confirmed Binance hot wallet in 34 txs. Binance holds full KYC for that account.<br><b>Binance.US: 18 USC §2703</b></div>
      </div>
      <div style="background:#0d1117;padding:10px;border-radius:4px">
        <div style="color:#2ecc71;font-weight:bold;margin-bottom:4px">③ GoDaddy (US subpoena)</div>
        <div style="color:#c9d1d9">Registrar for bippaxcoins.com, byxgcoins.com, aztexchange.com — all Domains By Proxy.<br>GoDaddy holds real registrant identity behind proxy.<br><b>GoDaddy LLC, Scottsdale AZ: 18 USC §2703</b></div>
      </div>
    </div>
  </div>
</div>

<!-- ── STAT CARDS ─────────────────────────────────────────────────────────── -->
<div class="stats">
  <div class="card">
    <div class="lbl">Total Received</div>
    <div class="val">{float(addr_info.get('total_received_btc',0)):,.2f}</div>
    <div class="sub2">BTC into scammer wallet</div>
  </div>
  <div class="card">
    <div class="lbl">Total Sent</div>
    <div class="val">{float(addr_info.get('total_sent_btc',0)):,.2f}</div>
    <div class="sub2">BTC out of scammer wallet</div>
  </div>
  <div class="card">
    <div class="lbl">Unique Txids</div>
    <div class="val">{len(set(t['txid'] for t in all_txs))}</div>
    <div class="sub2">across {len(all_txs)} ledger entries</div>
  </div>
  <div class="card">
    <div class="lbl">Activity Window</div>
    <div class="val" style="font-size:13px">{first_seen}</div>
    <div class="sub2">through {last_seen}</div>
  </div>
  <div class="card">
    <div class="lbl">Peak Month</div>
    <div class="val" style="font-size:13px">{peak_month}</div>
    <div class="sub2">{peak_btc:,.2f} BTC received</div>
  </div>
  <div class="card">
    <div class="lbl">Hop-1 Destinations</div>
    <div class="val">{len(hop1)}</div>
    <div class="sub2">{total_btc_h1:,.2f} BTC traced</div>
  </div>
  <div class="card">
    <div class="lbl">Hop-2 Destinations</div>
    <div class="val">{len(hop2)}</div>
    <div class="sub2">{total_btc_h2:,.2f} BTC further traced</div>
  </div>
  <div class="card" style="border-color:#e74c3c">
    <div class="lbl">Victim Loss</div>
    <div class="val" style="color:#e74c3c">0.8476 BTC</div>
    <div class="sub2">~$19,918 stolen · ~$80,520 today</div>
  </div>
  <div class="card" style="border-color:#2ecc71">
    <div class="lbl">Exchanges Identified</div>
    <div class="val" style="color:#2ecc71">{len(exchanges_found)}</div>
    <div class="sub2">subpoena targets</div>
  </div>
  <div class="card">
    <div class="lbl">Graph Nodes / Edges</div>
    <div class="val">{len(nodes_raw)}</div>
    <div class="sub2">{len(edges_raw)} fund flow paths</div>
  </div>
</div>

<!-- ── MASTER CONNECTION DIAGRAM ──────────────────────────────────────────── -->
<div class="section">
  <h2>Master Connection Map — How Both Thefts Link to the Same Criminal Network</h2>

  <div style="background:#0d1117;border:1px solid #30363d;border-radius:8px;padding:20px;overflow-x:auto">
    <div style="display:flex;gap:0;min-width:900px">

      <!-- INCIDENT 1 column -->
      <div style="flex:1;padding-right:16px;border-right:1px dashed #30363d">
        <div style="font-size:10px;letter-spacing:2px;color:#e74c3c;text-transform:uppercase;margin-bottom:10px;font-weight:bold">Incident 1 · 2022-07-31</div>
        <div style="background:#1c1010;border:1px solid #e74c3c;border-radius:6px;padding:8px 12px;margin-bottom:4px;font-size:11px">
          <div style="color:#8b949e;font-size:10px">VICTIM ADDRESS</div>
          <div style="font-family:monospace;color:#ffa657;word-break:break-all">3MT5t24cF88QzZ5qjgfDioC79pvyQDsojt</div>
          <div style="color:#8b949e;margin-top:2px">0.84758448 BTC stolen · 2022-07-31 03:09 UTC</div>
        </div>
        <div style="text-align:center;color:#8b949e;font-size:18px;line-height:1">▼</div>
        <div style="background:#161b22;border:1px solid #30363d;border-radius:6px;padding:8px 12px;margin-bottom:4px;font-size:11px">
          <div style="color:#8b949e;font-size:10px">RELAY ADDRESS</div>
          <div style="font-family:monospace;word-break:break-all">3R1Gs7RniDHRc6Trn214gVffSErYMbGuJ6</div>
          <div style="color:#8b949e;margin-top:2px">0.46 BTC (largest of 41 fan-out outputs)</div>
        </div>
        <div style="text-align:center;color:#8b949e;font-size:18px;line-height:1">▼</div>
        <div style="background:#161b22;border:1px solid #30363d;border-radius:6px;padding:8px 12px;margin-bottom:4px;font-size:11px">
          <div style="color:#8b949e;font-size:10px">AGGREGATOR WALLET</div>
          <div style="font-family:monospace;word-break:break-all">34HVDP9RFA9MpopGQ4TutLLVMFhhJFM9AX</div>
          <div style="color:#8b949e;margin-top:2px">1,403 BTC total · sent 97.25 BTC → Binance</div>
        </div>
        <div style="text-align:center;color:#f1c40f;font-size:18px;line-height:1">▼</div>
        <div style="background:#1a1a00;border:1px solid #f1c40f;border-radius:6px;padding:8px 12px;font-size:11px">
          <div style="color:#f1c40f;font-size:10px;font-weight:bold">⚡ BINANCE — KYC SUBPOENA TARGET</div>
          <div style="font-family:monospace;font-size:10px;word-break:break-all">bc1quhruqrghgcca950rvhtrg7cpd7u8k6svpzgzmrjy8xyukacl5lkq0r8l2d</div>
          <div style="color:#8b949e;margin-top:2px">Confirmed Binance hot wallet · 335,452 txs · 5,447,353 BTC lifetime</div>
        </div>
      </div>

      <!-- CENTER — shared scammer wallet -->
      <div style="width:220px;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:0 16px">
        <div style="font-size:10px;letter-spacing:2px;color:#e74c3c;text-transform:uppercase;margin-bottom:8px;text-align:center;font-weight:bold">Convergence Point</div>
        <div style="background:#1c1010;border:2px solid #e74c3c;border-radius:8px;padding:12px;width:100%;text-align:center">
          <div style="color:#e74c3c;font-weight:bold;font-size:12px;margin-bottom:6px">SCAMMER WALLET</div>
          <div style="font-family:monospace;font-size:10px;word-break:break-all;color:#ffa657">{target}</div>
          <div style="margin-top:8px;font-size:11px;color:#c9d1d9">395,190 BTC received<br>64,255 BTC via deptoy<br>Active 2022–2026</div>
          <div style="margin-top:8px;background:#0d1117;border-radius:4px;padding:6px;font-size:10px;color:#e74c3c">Both thefts funnel<br>to this wallet</div>
        </div>
        <div style="margin-top:16px;text-align:center;font-size:11px;color:#8b949e;line-height:1.6">
          ← Incident 1 feeds in<br>via relay + aggregator
          <br><br>
          Incident 2 feeds in →<br>via BIPPAX pivot
        </div>
      </div>

      <!-- INCIDENT 2 column -->
      <div style="flex:1;padding-left:16px;border-left:1px dashed #30363d">
        <div style="font-size:10px;letter-spacing:2px;color:#9b59b6;text-transform:uppercase;margin-bottom:10px;font-weight:bold">Incident 2 · Aug 2024</div>
        <div style="background:#1a0a1a;border:1px solid #9b59b6;border-radius:6px;padding:8px 12px;margin-bottom:4px;font-size:11px">
          <div style="color:#8b949e;font-size:10px">VICTIM DEPOSITS TO FAKE EXCHANGE</div>
          <div style="color:#c9d1d9">~$10,000 sent to deptoy.co (BIPPAX platform)</div>
          <div style="color:#8b949e;margin-top:2px">Victim told it was a cryptocurrency investment platform</div>
        </div>
        <div style="text-align:center;color:#8b949e;font-size:18px;line-height:1">▼</div>
        <div style="background:#1a0a1a;border:1px solid #9b59b6;border-radius:6px;padding:8px 12px;margin-bottom:4px;font-size:11px">
          <div style="color:#9b59b6;font-size:10px;font-weight:bold">DEPTOY.CO / BIPPAX PLATFORM</div>
          <div style="color:#c9d1d9">Fake exchange — BISSNEX CRYPTO GROUP LIMITED</div>
          <div style="color:#8b949e;margin-top:2px">Canadian Corp #1231288-3 · FINTRAC M20852872<br>WeChat: bmate601 · bizzzan01 · 883le<br>沪ICP备13026899号-3 (China MIIT registration)</div>
        </div>
        <div style="text-align:center;color:#8b949e;font-size:18px;line-height:1">▼</div>
        <div style="background:#161b22;border:1px solid #30363d;border-radius:6px;padding:8px 12px;margin-bottom:4px;font-size:11px">
          <div style="color:#8b949e;font-size:10px">VICTIM AGGREGATION HUB (PIVOT)</div>
          <div style="font-family:monospace;word-break:break-all">3JMjHDTJjKPnrvS7DycPAgYcA6HrHRk8UG</div>
          <div style="color:#8b949e;margin-top:2px">64,255 BTC processed · 25,117 txs · consolidates 300+ victim UTXOs</div>
        </div>
        <div style="text-align:center;color:#e74c3c;font-size:18px;line-height:1">▼</div>
        <div style="background:#1c1010;border:1px solid #e74c3c;border-radius:6px;padding:8px 12px;font-size:11px">
          <div style="color:#e74c3c;font-size:10px;font-weight:bold">140 BTC IN 7 DIRECT TRANSFERS → SCAMMER WALLET</div>
          <div style="color:#c9d1d9;margin-top:2px">Feb 2024 – Aug 2025 · Round-number disbursements: 50+20+20+20+20+5+5 BTC</div>
          <div style="color:#8b949e;margin-top:2px">Jan 2025 TX: 300+ victim deposits consolidated → scammer</div>
        </div>
      </div>

    </div>
  </div>
</div>

<!-- ── ALERTS ─────────────────────────────────────────────────────────────── -->
<div class="section">
  {exchange_alert}
</div>

<!-- ── CHARTS ─────────────────────────────────────────────────────────────── -->
<div class="section">
  <h2>Activity Analysis</h2>
  <div class="charts">
    <div class="chart-box">
      <h3>Monthly BTC Flow (Received vs Sent)</h3>
      <div style="position:relative;height:220px"><canvas id="timeline-chart"></canvas></div>
    </div>
    <div class="chart-box">
      <h3>Hop-1 Destination Breakdown</h3>
      <div style="position:relative;height:220px"><canvas id="breakdown-chart"></canvas></div>
    </div>
  </div>
</div>

<!-- ── GRAPH ──────────────────────────────────────────────────────────────── -->
<div class="section">
  <h2>Transaction Flow Graph</h2>
  <div class="legend">
    <div class="li"><div class="dot" style="background:#e74c3c"></div>Target (scammer)</div>
    <div class="li"><div class="dot" style="background:#f1c40f"></div>Binance</div>
    <div class="li"><div class="dot" style="background:#2ecc71"></div>Other exchange</div>
    <div class="li"><div class="dot" style="background:#27ae60"></div>Swept deposit addr</div>
    <div class="li"><div class="dot" style="background:#f39c12"></div>High-volume service</div>
    <div class="li"><div class="dot" style="background:#3498db"></div>Hop-1 unknown</div>
    <div class="li"><div class="dot" style="background:#9b59b6"></div>Hop-2 unknown</div>
    <div class="li" style="color:#8b949e">Blue edge = hop 1 &nbsp;·&nbsp; Purple edge = hop 2</div>
  </div>
  <div id="net"></div>
</div>

<!-- ── VICTIM MONEY TRAIL ─────────────────────────────────────────────────── -->
{trail_html}

<!-- ── BINANCE ATTRIBUTION ────────────────────────────────────────────────── -->
{binance_html}

<!-- ── DEPTOY.CO / BIPPAX PLATFORM LINK ───────────────────────────────────── -->
{deptoy_html}

<!-- ── ADDRESS TABLES ─────────────────────────────────────────────────────── -->
<div class="section">
  <h2>Address Analysis</h2>
  <div class="tabs">
    <div class="tab active" onclick="showTab('hop1')">Hop-1 Destinations ({len(hop1)})</div>
    <div class="tab" onclick="showTab('hop2')">Hop-2 Destinations ({len(hop2)})</div>
    <div class="tab" onclick="showTab('highvol')">High-Volume Wallets ({len(high_vol)})</div>
    <div class="tab" onclick="showTab('exchanges')">Exchanges ({len(exchanges_found)})</div>
  </div>

  <div id="tab-hop1" class="tab-body">
    <table id="tbl-hop1">
      <thead><tr>
        <th class="sortable" data-col="0">Address</th>
        <th class="sortable" data-col="1">BTC from Target</th>
        <th class="sortable" data-col="2">Txs via</th>
        <th class="sortable" data-col="3">On-chain Txs</th>
        <th class="sortable" data-col="4">Balance BTC</th>
        <th class="sortable" data-col="5">Entity</th>
        <th class="sortable" data-col="6">First Seen</th>
      </tr></thead>
      <tbody>{hop1_rows}</tbody>
    </table>
  </div>

  <div id="tab-hop2" class="tab-body hidden">
    <table id="tbl-hop2">
      <thead><tr>
        <th class="sortable" data-col="0">Address</th>
        <th class="sortable" data-col="1">BTC Received</th>
        <th class="sortable" data-col="2">Txs</th>
        <th class="sortable" data-col="3">On-chain Txs</th>
        <th class="sortable" data-col="4">Balance BTC</th>
        <th class="sortable" data-col="5">Entity</th>
        <th class="sortable" data-col="6">Via Hop-1 Addr</th>
        <th class="sortable" data-col="7">First Seen</th>
      </tr></thead>
      <tbody>{hop2_rows}</tbody>
    </table>
  </div>

  <div id="tab-highvol" class="tab-body hidden">
    <table id="tbl-hv">
      <thead><tr>
        <th class="sortable" data-col="0">Address</th>
        <th class="sortable" data-col="1">BTC from Target</th>
        <th class="sortable" data-col="2">Txs via</th>
        <th class="sortable" data-col="3">On-chain Txs</th>
        <th class="sortable" data-col="4">Balance BTC</th>
        <th class="sortable" data-col="5">Entity</th>
        <th class="sortable" data-col="6">First Seen</th>
      </tr></thead>
      <tbody>{highvol_rows}</tbody>
    </table>
  </div>

  <div id="tab-exchanges" class="tab-body hidden">
    <table id="tbl-ex">
      <thead><tr>
        <th class="sortable" data-col="0">Address</th>
        <th class="sortable" data-col="1">BTC from Target</th>
        <th class="sortable" data-col="2">Txs via</th>
        <th class="sortable" data-col="3">On-chain Txs</th>
        <th class="sortable" data-col="4">Balance BTC</th>
        <th class="sortable" data-col="5">Entity</th>
        <th class="sortable" data-col="6">First Seen</th>
      </tr></thead>
      <tbody>{table_rows(exchanges_found)}</tbody>
    </table>
  </div>
</div>

<!-- ── LAW ENFORCEMENT PACKAGE ────────────────────────────────────────────── -->
<div class="section">
  <h2>Law Enforcement Evidence Package</h2>
  <button class="copy-btn" onclick="copyLE()">Copy to clipboard</button>
  <pre class="le-block" id="le-block">{le_package}</pre>
</div>

<div class="section" style="color:#444;font-size:11px;padding-top:4px;padding-bottom:20px">
  Data: mempool.space · blockstream.info · All data is publicly visible on-chain. Report generated {generated_at}.
</div>

<!-- ── SCRIPTS ─────────────────────────────────────────────────────────────── -->
<script>
// ── vis.js graph ──────────────────────────────────────────────────────────────
const nodes = new vis.DataSet({json.dumps(vis_nodes)});
const edges = new vis.DataSet({json.dumps(vis_edges)});
new vis.Network(document.getElementById('net'), {{nodes, edges}}, {{
  physics:{{enabled:true,solver:'forceAtlas2Based',
    forceAtlas2Based:{{gravitationalConstant:-80,centralGravity:0.005,springLength:160,damping:0.4}},
    stabilization:{{iterations:300,updateInterval:50}}}},
  edges:{{smooth:{{type:'continuous'}},scaling:{{min:1,max:10}}}},
  nodes:{{shape:'dot',font:{{color:'#c9d1d9',size:10}},borderWidth:2}},
  interaction:{{hover:true,tooltipDelay:80,navigationButtons:true,keyboard:true}},
}});

// ── Chart.js timeline ─────────────────────────────────────────────────────────
new Chart(document.getElementById('timeline-chart'), {{
  type: 'bar',
  data: {{
    labels: {chart_labels},
    datasets: [
      {{label:'Received (BTC)', data:{chart_in}, backgroundColor:'rgba(52,152,219,0.7)', borderColor:'#3498db', borderWidth:1}},
      {{label:'Sent (BTC)',     data:{chart_out}, backgroundColor:'rgba(231,76,60,0.5)',  borderColor:'#e74c3c', borderWidth:1}},
    ]
  }},
  options:{{
    responsive:true, maintainAspectRatio:false,
    plugins:{{legend:{{labels:{{color:'#8b949e',font:{{size:11}}}}}}}},
    scales:{{
      x:{{ticks:{{color:'#8b949e',font:{{size:9}},maxRotation:60}},grid:{{color:'#21262d'}}}},
      y:{{ticks:{{color:'#8b949e',font:{{size:10}}}},grid:{{color:'#21262d'}}}}
    }}
  }}
}});

// ── Chart.js breakdown doughnut ───────────────────────────────────────────────
new Chart(document.getElementById('breakdown-chart'), {{
  type: 'doughnut',
  data: {{
    labels: {breakdown_labels},
    datasets: [{{data:{breakdown_vals}, backgroundColor:{breakdown_colors}, borderWidth:1, borderColor:'#0d1117'}}]
  }},
  options:{{
    responsive:true, maintainAspectRatio:false,
    plugins:{{
      legend:{{position:'right',labels:{{color:'#8b949e',font:{{size:10}},boxWidth:12}}}},
      tooltip:{{callbacks:{{label:ctx => ctx.label + ': ' + ctx.parsed.toFixed(2) + ' BTC'}}}}
    }}
  }}
}});

// ── Tab switching ─────────────────────────────────────────────────────────────
function showTab(name) {{
  const names = ['hop1','hop2','highvol','exchanges'];
  names.forEach(t => document.getElementById('tab-'+t).classList.toggle('hidden', t !== name));
  document.querySelectorAll('.tab').forEach((el,i) => el.classList.toggle('active', names[i] === name));
}}

// ── Sortable tables ───────────────────────────────────────────────────────────
function parseVal(cell) {{
  const v = cell.dataset.val;
  if (v !== undefined) return isNaN(v) ? v.toLowerCase() : parseFloat(v);
  const t = cell.textContent.trim().replace(/,/g,'');
  return isNaN(t) || t==='' ? t.toLowerCase() : parseFloat(t);
}}

function sortTable(th) {{
  const table  = th.closest('table');
  const col    = parseInt(th.dataset.col);
  const tbody  = table.querySelector('tbody');
  const rows   = Array.from(tbody.querySelectorAll('tr'));
  const asc    = th.classList.contains('sort-desc') || !th.classList.contains('sort-asc');

  table.querySelectorAll('th').forEach(h => h.classList.remove('sort-asc','sort-desc'));
  th.classList.add(asc ? 'sort-asc' : 'sort-desc');

  rows.sort((a, b) => {{
    const va = parseVal(a.cells[col]);
    const vb = parseVal(b.cells[col]);
    if (typeof va === 'number' && typeof vb === 'number') return asc ? va-vb : vb-va;
    return asc ? String(va).localeCompare(String(vb)) : String(vb).localeCompare(String(va));
  }});
  rows.forEach(r => tbody.appendChild(r));
}}

document.querySelectorAll('th.sortable').forEach(th => th.addEventListener('click', () => sortTable(th)));

// ── Copy LE package ───────────────────────────────────────────────────────────
function copyLE() {{
  navigator.clipboard.writeText(document.getElementById('le-block').textContent)
    .then(() => {{ const b = document.querySelector('.copy-btn'); b.textContent='Copied!'; setTimeout(()=>b.textContent='Copy to clipboard',2000); }});
}}
</script>
</body>
</html>"""

    REPORT_PATH.write_text(html)
    print(f"Report → {REPORT_PATH}")
    return REPORT_PATH


if __name__ == '__main__':
    generate_report()
