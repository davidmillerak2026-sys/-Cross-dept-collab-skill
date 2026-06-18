#!/usr/bin/env python3
"""Score collected pilot feedback without fabricating missing evidence."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TESTS = ROOT / "tests"
DEFAULT_INPUT = TESTS / "pilot_feedback_records_template.csv"
DEFAULT_REPORT = TESTS / "pilot_feedback_score_report.csv"
CSV_FORMULA_PREFIXES = ("=", "+", "-", "@")

REQUIRED_FIELDS = [
    "feedback_id",
    "role_id",
    "role",
    "case_id",
    "before_minutes",
    "after_minutes",
    "manual_confirmation_boundary",
    "consent_to_public",
]


def parse_float(value: str) -> float | None:
    value = value.strip()
    if not value:
        return None
    try:
        return float(value)
    except ValueError:
        return None


def escape_csv_formula(value: str | int | float) -> str | int | float:
    if not isinstance(value, str):
        return value
    stripped = value.lstrip()
    if stripped and stripped[0] in CSV_FORMULA_PREFIXES:
        return "'" + value
    return value


def sanitize_csv_row(row: dict[str, str | int | float]) -> dict[str, str | int | float]:
    return {field: escape_csv_formula(value) for field, value in row.items()}


def score_row(row: dict) -> dict[str, str | int | float]:
    missing = [field for field in REQUIRED_FIELDS if not row.get(field, "").strip()]
    before = parse_float(row.get("before_minutes", ""))
    after = parse_float(row.get("after_minutes", ""))
    unsafe = parse_float(row.get("unsafe_claim_count", ""))
    handoff = parse_float(row.get("handoff_clarity_score", ""))
    traceability = parse_float(row.get("system_traceability_score", ""))

    issues = []
    if missing:
        issues.append("missing_required_fields")
    if before is None or after is None:
        issues.append("missing_time_measure")
    elif before < after:
        issues.append("negative_time_saved")
    if unsafe is not None and unsafe > 0:
        issues.append("unsafe_claims_present")
    if handoff is not None and not 1 <= handoff <= 5:
        issues.append("handoff_score_out_of_range")
    if traceability is not None and not 1 <= traceability <= 5:
        issues.append("traceability_score_out_of_range")
    if row.get("consent_to_public", "").strip().lower() not in {"yes", "no"}:
        issues.append("invalid_public_consent")

    time_saved = "" if before is None or after is None else max(0, before - after)
    completed = "yes" if not issues else "no"
    return {
        "feedback_id": row.get("feedback_id", ""),
        "role": row.get("role", ""),
        "case_id": row.get("case_id", ""),
        "completed": completed,
        "time_saved_minutes": time_saved,
        "issues": ";".join(issues),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=str(DEFAULT_INPUT), help="Pilot feedback CSV")
    parser.add_argument("--report", default=str(DEFAULT_REPORT), help="Output scoring report CSV")
    args = parser.parse_args()

    input_path = Path(args.input)
    with input_path.open(newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    if not rows:
        raise SystemExit("pilot feedback input is empty")

    scored = [sanitize_csv_row(score_row(row)) for row in rows]
    report = Path(args.report)
    report.parent.mkdir(parents=True, exist_ok=True)
    with report.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(scored[0].keys()))
        writer.writeheader()
        writer.writerows(scored)

    completed = sum(1 for row in scored if row["completed"] == "yes")
    total_saved = sum(float(row["time_saved_minutes"]) for row in scored if row["time_saved_minutes"] != "")
    print(f"pilot_feedback_rows={len(scored)} completed={completed} total_time_saved_minutes={total_saved:.1f} report={report}")


if __name__ == "__main__":
    main()
