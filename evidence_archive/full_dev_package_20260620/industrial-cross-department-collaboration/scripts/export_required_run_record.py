#!/usr/bin/env python3
"""Export a required-screenshot run-record template from the full record sheet."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TESTS = ROOT / "tests"
FULL_RECORD = TESTS / "run_record_template.csv"
MATRIX = TESTS / "rubric_evidence_matrix.csv"
DEFAULT_OUT = TESTS / "run_record_required_template.csv"


def load_required_ids() -> set[str]:
    with MATRIX.open(newline="", encoding="utf-8") as fh:
        return {
            row["case_id"]
            for row in csv.DictReader(fh)
            if row["screenshot_priority"] == "required"
        }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=str(DEFAULT_OUT), help="Output required-only run-record CSV")
    args = parser.parse_args()

    required_ids = load_required_ids()
    with FULL_RECORD.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        fieldnames = reader.fieldnames or []
        rows = [row for row in reader if row["case_id"] in required_ids]

    row_ids = {row["case_id"] for row in rows}
    missing = sorted(required_ids - row_ids)
    if missing:
        raise SystemExit(f"required cases missing from run_record_template.csv: {missing}")

    out = Path(args.out)
    with out.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote={out} required_records={len(rows)}")


if __name__ == "__main__":
    main()
