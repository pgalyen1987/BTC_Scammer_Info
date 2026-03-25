"""
parse_pdf.py — Extract transaction IDs and metadata from a Blockchair address statement PDF.
Uses word-position grouping to handle txids split across 3 visual rows.
"""
import re
import pdfplumber
import json
import sys
from pathlib import Path
from collections import defaultdict

PDF_PATH = Path("/home/me/Downloads/Wallet statement 1_1 2009-01-03 - 2026-03-23.pdf")

HEX_RE = re.compile(r'^[0-9a-f]{10,}$', re.IGNORECASE)
DATE_RE = re.compile(r'^\d{4}-\d{2}-\d{2}$')
TIME_RE = re.compile(r'^\d{2}:\d{2}:\d{2}$')
INDEX_RE = re.compile(r'^\d+$')


def group_words_by_row(words: list, y_tolerance: int = 8) -> list[list[dict]]:
    """Group words into visual rows based on their y (top) coordinate."""
    if not words:
        return []
    rows = []
    current_row = [words[0]]
    current_y = words[0]['top']

    for word in words[1:]:
        if abs(word['top'] - current_y) <= y_tolerance:
            current_row.append(word)
        else:
            rows.append(sorted(current_row, key=lambda w: w['x0']))
            current_row = [word]
            current_y = word['top']
    rows.append(sorted(current_row, key=lambda w: w['x0']))
    return rows


def row_texts(row: list[dict]) -> list[str]:
    return [w['text'] for w in row]


def extract_transactions(pdf_path: Path, max_pages: int = None) -> dict:
    address_info = {}
    transactions = []
    seen_txids = set()

    print(f"Opening PDF: {pdf_path}")
    with pdfplumber.open(pdf_path) as pdf:
        total_pages = len(pdf.pages)
        pages_to_read = min(total_pages, max_pages) if max_pages else total_pages
        print(f"Total pages: {total_pages}, reading: {pages_to_read}")

        for page_num in range(pages_to_read):
            page = pdf.pages[page_num]
            words = page.extract_words()
            rows = group_words_by_row(words)

            # Extract address info from page 1
            if page_num == 0:
                text = page.extract_text() or ""
                addr_match = re.search(r'ADDRESS ID\s+([13bc][a-zA-Z0-9]{25,62})', text)
                if addr_match:
                    address_info['address'] = addr_match.group(1)
                recv_match = re.search(r'TOTAL RECEIVED\s+([\d,]+\.[\d]+)\s*BTC', text)
                if recv_match:
                    address_info['total_received_btc'] = recv_match.group(1).replace(',', '')
                sent_match = re.search(r'TOTAL SENT\s+([\d,]+\.[\d]+)\s*BTC', text)
                if sent_match:
                    address_info['total_sent_btc'] = sent_match.group(1).replace(',', '')

            # Parse transaction rows.
            # Pattern (3 consecutive visual rows per transaction):
            #   Row A: {index} {YYYY-MM-DD} {hex_part1} {+|-} {amount} BTC...
            #   Row B: {HH:MM:SS} {hex_part2} {usd_amount} USD
            #   Row C: {hex_part3}
            i = 0
            while i < len(rows):
                texts = row_texts(rows[i])

                # Detect Row A: starts with integer index + date
                if (len(texts) >= 3
                        and INDEX_RE.match(texts[0])
                        and DATE_RE.match(texts[1])
                        and HEX_RE.match(texts[2])):

                    tx_index = int(texts[0])
                    date_str = texts[1]
                    hex1 = texts[2].lower()

                    # Sign and amount on Row A
                    sign = '?'
                    amount_btc = 0.0
                    for j, t in enumerate(texts):
                        if t in ('+', '-'):
                            sign = t
                            if j + 1 < len(texts):
                                try:
                                    amount_btc = float(texts[j + 1].replace(',', ''))
                                except ValueError:
                                    pass
                            break

                    # Row B: time + hex_part2
                    hex2 = ''
                    time_str = ''
                    if i + 1 < len(rows):
                        row_b = row_texts(rows[i + 1])
                        if row_b and TIME_RE.match(row_b[0]):
                            time_str = row_b[0]
                            if len(row_b) > 1 and HEX_RE.match(row_b[1]):
                                hex2 = row_b[1].lower()

                    # Row C: hex_part3
                    hex3 = ''
                    if i + 2 < len(rows):
                        row_c = row_texts(rows[i + 2])
                        if row_c and HEX_RE.match(row_c[0]) and len(row_c[0]) >= 10:
                            # Make sure it's not another transaction row
                            if not INDEX_RE.match(row_c[0]) and not DATE_RE.match(row_c[0]):
                                hex3 = row_c[0].lower()

                    txid = (hex1 + hex2 + hex3).lower()

                    if len(txid) == 64:
                        direction = 'in' if sign == '+' else 'out'
                        tx_entry = {
                            'index': tx_index,
                            'date': date_str,
                            'time': time_str,
                            'datetime': f"{date_str} {time_str}",
                            'txid': txid,
                            'direction': direction,
                            'amount_btc': amount_btc,
                            'page': page_num + 1,
                        }
                        # Deduplicate by (txid, direction) — same txid can appear as both in+out
                        dedup_key = f"{txid}:{direction}"
                        if dedup_key not in seen_txids:
                            seen_txids.add(dedup_key)
                            transactions.append(tx_entry)

                i += 1

            if (page_num + 1) % 100 == 0:
                print(f"  Processed page {page_num + 1}/{pages_to_read}, txs so far: {len(transactions)}")

    print(f"\nExtraction complete: {len(transactions)} unique transactions found")
    return {
        'address_info': address_info,
        'transactions': transactions,
    }


if __name__ == '__main__':
    max_pages = int(sys.argv[1]) if len(sys.argv) > 1 else None
    result = extract_transactions(PDF_PATH, max_pages=max_pages)

    out_path = Path("/home/me/scamfinder/transactions.json")
    with open(out_path, 'w') as f:
        json.dump(result, f, indent=2)

    print(f"Saved to {out_path}")
    print(f"Address: {result['address_info'].get('address', 'unknown')}")
    print(f"Transactions extracted: {len(result['transactions'])}")

    for tx in result['transactions'][:5]:
        print(f"  [{tx['index']}] {tx['datetime']} {tx['direction']:3s} "
              f"{tx['amount_btc']:.8f} BTC  txid: {tx['txid']}")
