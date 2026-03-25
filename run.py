"""
run.py — Master runner: parse PDF → trace chain → generate report
Usage:
  python3 run.py [--max-pages N] [--max-tx N]

Defaults: reads all PDF pages, traces up to 50 outbound transactions.
"""
import argparse
import subprocess
import sys
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description='ScamFinder — Bitcoin transaction tracer')
    parser.add_argument('--max-pages', type=int, default=None, help='Limit PDF pages to parse (default: all)')
    parser.add_argument('--max-tx', type=int, default=50, help='Max outbound transactions to trace on-chain (default: 50)')
    parser.add_argument('--skip-parse', action='store_true', help='Skip PDF parsing (use existing transactions.json)')
    parser.add_argument('--skip-trace', action='store_true', help='Skip chain tracing (use existing graph.json)')
    args = parser.parse_args()

    base = Path("/home/me/scamfinder")

    if not args.skip_parse:
        print("=" * 60)
        print("STEP 1: Parsing PDF")
        print("=" * 60)
        cmd = [sys.executable, str(base / "parse_pdf.py")]
        if args.max_pages:
            cmd.append(str(args.max_pages))
        result = subprocess.run(cmd)
        if result.returncode != 0:
            print("PDF parsing failed.")
            sys.exit(1)
    else:
        print("Skipping PDF parse (using existing transactions.json)")

    if not args.skip_trace:
        print("\n" + "=" * 60)
        print("STEP 2: Tracing on-chain transactions")
        print("=" * 60)
        import chain_tracer
        chain_tracer.trace_transactions(max_tx=args.max_tx)
    else:
        print("Skipping chain trace (using existing graph.json)")

    print("\n" + "=" * 60)
    print("STEP 3: Generating report")
    print("=" * 60)
    import report
    report_path = report.generate_report()

    print("\n" + "=" * 60)
    print(f"DONE. Open your report: file://{report_path}")
    print("=" * 60)

if __name__ == '__main__':
    main()
