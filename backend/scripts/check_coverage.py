#!/usr/bin/env python3
"""Check that every measured source file meets a minimum coverage threshold.

Usage:
    python -m pytest --cov --cov-report=json  # produces coverage.json
    python scripts/check_coverage.py [--min 80] [--report coverage.json]
"""

import argparse
import json
import sys


def main() -> int:
    parser = argparse.ArgumentParser(description="Per-file coverage gate")
    parser.add_argument("--min", type=float, default=80, help="Minimum coverage %% per file")
    parser.add_argument("--report", default="coverage.json", help="Path to coverage JSON report")
    args = parser.parse_args()

    with open(args.report) as f:
        data = json.load(f)

    failures: list[tuple[str, float]] = []
    print(f"\nPer-file coverage (minimum: {args.min}%)")
    print("-" * 60)

    for filepath, info in sorted(data.get("files", {}).items()):
        pct = info["summary"]["percent_covered"]
        status = "OK" if pct >= args.min else "FAIL"
        if status == "FAIL":
            failures.append((filepath, pct))
        print(f"  {status}  {pct:5.1f}%  {filepath}")

    total = data.get("totals", {}).get("percent_covered", 0)
    print("-" * 60)
    print(f"  TOTAL  {total:.1f}%\n")

    if failures:
        print(f"FAILED: {len(failures)} file(s) below {args.min}% coverage:")
        for path, pct in failures:
            print(f"  {pct:.1f}%  {path}")
        return 1

    print("All files meet the minimum coverage threshold.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
