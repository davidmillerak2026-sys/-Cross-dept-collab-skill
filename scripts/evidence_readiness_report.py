#!/usr/bin/env python3
"""Build a unified evidence-readiness report for local and platform proof."""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TESTS = ROOT / "tests"
DEFAULT_OUT = TESTS / "evidence_readiness_report.md"
EVIDENCE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".pdf", ".md", ".txt"}


@dataclass(frozen=True)
class RunSheet:
    label: str
    path: Path
    required_priority: str | None = None


RUN_SHEETS = [
    RunSheet("T01-T39 full run", TESTS / "run_record_template.csv", "required"),
    RunSheet("S01-S10 enterprise-flow run", TESTS / "run_record_enterprise_flow_template.csv", "enterprise_required"),
    RunSheet("ST01-ST12 stability stress run", TESTS / "run_record_stability_stress_template.csv", "stability_required"),
]

LOCAL_ASSETS = [
    "SKILL.md",
    "README.md",
    "VERSION.md",
    "submission_manifest.json",
    "scripts/validate_package.py",
    "scripts/smoke_test_package.py",
    "scripts/expert_rubric_gate.py",
    "scripts/evidence_readiness_report.py",
    "scripts/champion_acceptance_gate.py",
    "tests/test_cases.json",
    "tests/rubric_evidence_matrix.csv",
    "tests/astronclaw_required_prompt_pack.md",
    "tests/astronclaw_enterprise_flow_prompt_pack.md",
    "tests/astronclaw_stability_stress_prompt_pack.md",
    "tests/pilot_feedback_interview_pack.md",
    "tests/pilot_feedback_records_template.csv",
    "tests/platform_submission_evidence_template.json",
    "tests/champion_acceptance_report.md",
    "templates/impact_scoreboard.md",
    "templates/impact_scoreboard.schema.json",
    "templates/management_escalation_packet.md",
]


def read_csv(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def truthy(value: str) -> bool:
    return value.strip().lower() in {"yes", "pass", "passed", "true", "1"}


def evidence_exists(reference: str) -> bool:
    ref = reference.strip()
    if not ref:
        return False
    path = Path(ref)
    if not path.is_absolute():
        path = ROOT / ref
    if path.suffix.lower() not in EVIDENCE_EXTENSIONS:
        return False
    return path.exists() and path.is_file()


def summarize_run_sheet(sheet: RunSheet) -> dict:
    rows = read_csv(sheet.path)
    filled = [row for row in rows if row.get("platform", "").strip() and row.get("passed", "").strip()]
    passed = [row for row in filled if truthy(row.get("passed", ""))]
    failed = [row for row in filled if row.get("passed", "").strip() and not truthy(row.get("passed", ""))]
    required = rows
    if sheet.required_priority:
        required = [row for row in rows if row.get("priority_for_screenshot", "") == sheet.required_priority]
    required_with_ref = [row for row in required if row.get("output_file_or_screenshot", "").strip()]
    required_with_file = [row for row in required if evidence_exists(row.get("output_file_or_screenshot", ""))]
    missing_ids = [row.get("case_id", "") for row in required if row not in required_with_file]
    return {
        "label": sheet.label,
        "path": sheet.path.relative_to(ROOT).as_posix(),
        "total": len(rows),
        "filled": len(filled),
        "passed": len(passed),
        "failed": len(failed),
        "required_total": len(required),
        "required_with_reference": len(required_with_ref),
        "required_with_file": len(required_with_file),
        "required_missing_file_ids": missing_ids,
    }


def summarize_pilot_feedback() -> dict:
    path = TESTS / "pilot_feedback_records_template.csv"
    rows = read_csv(path)
    completed = []
    with_time = []
    with_public_consent = []
    template_rows = []
    for row in rows:
        feedback_id = row.get("feedback_id", "")
        if "YYYYMMDD" in feedback_id:
            template_rows.append(row)
            continue
        required = [
            row.get("role_id", "").strip(),
            row.get("role", "").strip(),
            row.get("case_id", "").strip(),
            row.get("before_minutes", "").strip(),
            row.get("after_minutes", "").strip(),
            row.get("manual_confirmation_boundary", "").strip(),
        ]
        if all(required):
            completed.append(row)
        if row.get("before_minutes", "").strip() and row.get("after_minutes", "").strip():
            with_time.append(row)
        if row.get("consent_to_public", "").strip().lower() == "yes":
            with_public_consent.append(row)
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "total_rows": len(rows),
        "template_rows": len(template_rows),
        "completed_feedback": len(completed),
        "with_time_measure": len(with_time),
        "public_consent_yes": len(with_public_consent),
    }


def local_asset_status() -> list[tuple[str, bool]]:
    return [(rel, (ROOT / rel).exists()) for rel in LOCAL_ASSETS]


def render_report() -> str:
    assets = local_asset_status()
    run_summaries = [summarize_run_sheet(sheet) for sheet in RUN_SHEETS]
    pilot = summarize_pilot_feedback()
    assets_ready = all(ok for _, ok in assets)
    platform_ready = all(summary["required_with_file"] == summary["required_total"] for summary in run_summaries)
    pilot_ready = pilot["completed_feedback"] >= 3 and pilot["with_time_measure"] >= 3

    lines = [
        "# Evidence Readiness Report",
        "",
        "This report separates local package readiness from platform and pilot evidence. It must not be used to claim final expert-score completion until the missing evidence items are collected.",
        "",
        "## Summary",
        "",
        f"- local_assets_ready: {'yes' if assets_ready else 'no'}",
        f"- platform_run_evidence_ready: {'yes' if platform_ready else 'no'}",
        f"- pilot_feedback_ready: {'yes' if pilot_ready else 'no'}",
        "",
        "## Local Assets",
        "",
        "| Asset | Status |",
        "| --- | --- |",
    ]
    lines.extend(f"| `{rel}` | {'present' if ok else 'missing'} |" for rel, ok in assets)
    lines.extend(["", "## Platform Run Evidence", "", "| Evidence set | Rows | Filled | Passed | Failed | Required files | Missing required IDs |", "| --- | ---: | ---: | ---: | ---: | ---: | --- |"])
    for summary in run_summaries:
        missing = ";".join(summary["required_missing_file_ids"]) or "-"
        lines.append(
            f"| {summary['label']} | {summary['total']} | {summary['filled']} | {summary['passed']} | {summary['failed']} | "
            f"{summary['required_with_file']}/{summary['required_total']} | {missing} |"
        )
    lines.extend(
        [
            "",
            "## Pilot Feedback Evidence",
            "",
            f"- source: `{pilot['path']}`",
            f"- total_rows: {pilot['total_rows']}",
            f"- template_rows_not_counted_as_feedback: {pilot['template_rows']}",
            f"- completed_feedback: {pilot['completed_feedback']}",
            f"- with_time_measure: {pilot['with_time_measure']}",
            f"- public_consent_yes: {pilot['public_consent_yes']}",
            "",
            "## Next Evidence Actions",
            "",
        ]
    )
    if not platform_ready:
        lines.append("- Run and save T01-T39, S01-S10 and ST01-ST12 outputs/screenshots, then fill the corresponding run-record CSV files with real paths.")
    if not pilot_ready:
        lines.append("- Collect at least 3 real anonymized pilot feedback records with before/after timing and manual-confirmation boundaries.")
    if assets_ready and platform_ready and pilot_ready:
        lines.append("- Evidence report is complete; run `scripts/expert_rubric_gate.py --require-astronclaw` and preserve the generated report.")
    else:
        lines.append("- Keep the claims boundary: local readiness is proven, final 100-point expert evidence is not yet proven.")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=str(DEFAULT_OUT), help="Output markdown report")
    args = parser.parse_args()

    out = Path(args.out)
    report = render_report()
    out.write_text(report, encoding="utf-8")
    print(f"wrote={out}")


if __name__ == "__main__":
    main()
