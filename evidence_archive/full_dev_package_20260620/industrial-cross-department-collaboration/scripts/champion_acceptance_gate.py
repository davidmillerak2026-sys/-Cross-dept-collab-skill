#!/usr/bin/env python3
"""Check whether the package is ready for a real champion-level submission."""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
TESTS = ROOT / "tests"
DEFAULT_OUT = TESTS / "champion_acceptance_report.md"
SUBMISSION_EVIDENCE = TESTS / "platform_submission_evidence_template.json"
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

REQUIRED_SUBMISSION_SCREENSHOTS = (
    "contest_submit_success_screenshot",
    "skillhub_approval_screenshot",
    "skillhub_public_page_screenshot",
)

OPTIONAL_SUBMISSION_SCREENSHOTS = (
    "skillhub_dashboard_status_screenshot",
    "heat_rank_screenshot",
)


def truthy(value: str) -> bool:
    return value.strip().lower() in {"yes", "pass", "passed", "true", "1"}


def parse_float(value: str) -> float | None:
    value = value.strip()
    if not value:
        return None
    try:
        return float(value)
    except ValueError:
        return None


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


def read_csv(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def run_script(args: list[str]) -> tuple[bool, str]:
    result = subprocess.run(
        [sys.executable, *args],
        cwd=str(ROOT),
        text=True,
        capture_output=True,
        check=False,
    )
    return result.returncode == 0, (result.stdout + result.stderr).strip()


def summarize_local_gates(skip_local_gates: bool) -> dict:
    if skip_local_gates:
        return {
            "status": "skipped",
            "validate": "skipped",
            "smoke": "skipped",
            "expert": "skipped",
        }

    validate_ok, _ = run_script(["scripts/validate_package.py"])
    smoke_ok, _ = run_script(["scripts/smoke_test_package.py"])
    expert_ok, _ = run_script(["scripts/expert_rubric_gate.py", "--skip-subchecks"])
    status = "PASS" if validate_ok and smoke_ok and expert_ok else "FAIL"
    return {
        "status": status,
        "validate": "PASS" if validate_ok else "FAIL",
        "smoke": "PASS" if smoke_ok else "FAIL",
        "expert": "PASS" if expert_ok else "FAIL",
    }


def summarize_run_sheet(sheet: RunSheet) -> dict:
    rows = read_csv(sheet.path)
    astron_rows = [
        row for row in rows
        if row.get("platform", "").strip().lower() == "astronclaw" and row.get("passed", "").strip()
    ]
    passed_rows = [row for row in astron_rows if truthy(row.get("passed", ""))]
    failed_rows = [row for row in astron_rows if not truthy(row.get("passed", ""))]
    filled_ids = {row.get("case_id", "") for row in astron_rows}
    unfilled_ids = [row.get("case_id", "") for row in rows if row.get("case_id", "") not in filled_ids]
    file_rows = [row for row in rows if evidence_exists(row.get("output_file_or_screenshot", ""))]
    missing_file_ids = [row.get("case_id", "") for row in rows if row not in file_rows]

    required_rows = rows
    if sheet.required_priority:
        required_rows = [row for row in rows if row.get("priority_for_screenshot", "") == sheet.required_priority]
    required_file_rows = [row for row in required_rows if evidence_exists(row.get("output_file_or_screenshot", ""))]
    required_missing_ids = [row.get("case_id", "") for row in required_rows if row not in required_file_rows]

    ready = (
        len(astron_rows) == len(rows)
        and len(passed_rows) == len(rows)
        and not failed_rows
        and len(file_rows) == len(rows)
    )
    return {
        "label": sheet.label,
        "path": sheet.path.relative_to(ROOT).as_posix(),
        "total": len(rows),
        "filled": len(astron_rows),
        "passed": len(passed_rows),
        "failed": len(failed_rows),
        "file_count": len(file_rows),
        "unfilled_ids": unfilled_ids,
        "missing_file_ids": missing_file_ids,
        "required_total": len(required_rows),
        "required_file_count": len(required_file_rows),
        "required_missing_ids": required_missing_ids,
        "ready": ready,
    }


def summarize_submission_evidence() -> dict:
    data = json.loads(SUBMISSION_EVIDENCE.read_text(encoding="utf-8"))
    missing = []
    for key in REQUIRED_SUBMISSION_SCREENSHOTS:
        if not evidence_exists(str(data.get(key, ""))):
            missing.append(key)
    if not str(data.get("skillhub_public_url", "")).strip():
        missing.append("skillhub_public_url")

    optional_present = [
        key for key in OPTIONAL_SUBMISSION_SCREENSHOTS
        if evidence_exists(str(data.get(key, "")))
    ]
    return {
        "path": SUBMISSION_EVIDENCE.relative_to(ROOT).as_posix(),
        "data": data,
        "missing_required": missing,
        "optional_present": optional_present,
        "ready": not missing,
    }


def summarize_pilot_feedback() -> dict:
    rows = read_csv(TESTS / "pilot_feedback_records_template.csv")
    real_rows = [row for row in rows if "YYYYMMDD" not in row.get("feedback_id", "")]
    completed = []
    with_time = []
    with_evidence = []
    unsafe_rows = []
    for row in real_rows:
        required = [
            row.get("feedback_id", "").strip(),
            row.get("role_id", "").strip(),
            row.get("role", "").strip(),
            row.get("case_id", "").strip(),
            row.get("before_minutes", "").strip(),
            row.get("after_minutes", "").strip(),
            row.get("manual_confirmation_boundary", "").strip(),
            row.get("consent_to_public", "").strip(),
        ]
        if all(required):
            completed.append(row)
        before = parse_float(row.get("before_minutes", ""))
        after = parse_float(row.get("after_minutes", ""))
        if before is not None and after is not None:
            with_time.append(row)
        if evidence_exists(row.get("evidence_file_or_screenshot", "")):
            with_evidence.append(row)
        unsafe = parse_float(row.get("unsafe_claim_count", ""))
        if unsafe is not None and unsafe > 0:
            unsafe_rows.append(row)

    public_consent_yes = [
        row for row in real_rows if row.get("consent_to_public", "").strip().lower() == "yes"
    ]
    ready = (
        len(completed) >= 3
        and len(with_time) >= 3
        and len(with_evidence) >= 3
        and not unsafe_rows
    )
    return {
        "path": "tests/pilot_feedback_records_template.csv",
        "total_rows": len(rows),
        "real_rows": len(real_rows),
        "completed_feedback": len(completed),
        "with_time_measure": len(with_time),
        "with_evidence_file": len(with_evidence),
        "unsafe_rows": len(unsafe_rows),
        "public_consent_yes": len(public_consent_yes),
        "ready": ready,
    }


def render_report(skip_local_gates: bool) -> tuple[str, bool]:
    local = summarize_local_gates(skip_local_gates)
    submission = summarize_submission_evidence()
    runs = [summarize_run_sheet(sheet) for sheet in RUN_SHEETS]
    pilot = summarize_pilot_feedback()

    run_map = {item["label"]: item for item in runs}
    full_run_ready = run_map["T01-T39 full run"]["ready"]
    enterprise_ready = run_map["S01-S10 enterprise-flow run"]["ready"]
    stability_ready = run_map["ST01-ST12 stability stress run"]["ready"]
    champion_ready = (
        local["status"] in {"PASS", "skipped"}
        and submission["ready"]
        and full_run_ready
        and enterprise_ready
        and stability_ready
        and pilot["ready"]
    )

    lines = [
        "# Champion Acceptance Report",
        "",
        "This report checks whether the package has crossed from local readiness into real champion-level external evidence readiness.",
        "",
        "## Summary",
        "",
        f"- local_gate_status: {local['status']}",
        f"- platform_submission_ready: {'yes' if submission['ready'] else 'no'}",
        f"- full_run_ready: {'yes' if full_run_ready else 'no'}",
        f"- enterprise_flow_ready: {'yes' if enterprise_ready else 'no'}",
        f"- stability_stress_ready: {'yes' if stability_ready else 'no'}",
        f"- pilot_feedback_ready: {'yes' if pilot['ready'] else 'no'}",
        f"- champion_ready: {'yes' if champion_ready else 'no'}",
        "",
        "## Local Gates",
        "",
        f"- validate_package: {local['validate']}",
        f"- smoke_test: {local['smoke']}",
        f"- expert_rubric_local: {local['expert']}",
        "",
        "## Platform Submission Evidence",
        "",
        f"- source: `{submission['path']}`",
        f"- skillhub_public_url: `{submission['data'].get('skillhub_public_url', '')}`",
        f"- missing_required: `{';'.join(submission['missing_required']) or '-'}`",
        f"- optional_present: `{';'.join(submission['optional_present']) or '-'}`",
        "",
        "## Platform Run Evidence",
        "",
        "| Evidence set | Ready | Filled | Passed | Failed | Files | Missing fill IDs | Missing file IDs |",
        "| --- | --- | ---: | ---: | ---: | ---: | --- | --- |",
    ]
    for item in runs:
        lines.append(
            f"| {item['label']} | {'yes' if item['ready'] else 'no'} | {item['filled']}/{item['total']} | "
            f"{item['passed']}/{item['total']} | {item['failed']} | {item['file_count']}/{item['total']} | "
            f"{';'.join(item['unfilled_ids']) or '-'} | {';'.join(item['missing_file_ids']) or '-'} |"
        )

    lines.extend(
        [
            "",
            "## Pilot Feedback Evidence",
            "",
            f"- source: `{pilot['path']}`",
            f"- real_rows: {pilot['real_rows']}",
            f"- completed_feedback: {pilot['completed_feedback']}",
            f"- with_time_measure: {pilot['with_time_measure']}",
            f"- with_evidence_file: {pilot['with_evidence_file']}",
            f"- unsafe_rows: {pilot['unsafe_rows']}",
            f"- public_consent_yes: {pilot['public_consent_yes']}",
            "",
            "## Champion Decision",
            "",
        ]
    )
    if champion_ready:
        lines.append("- Champion acceptance gate is satisfied. Preserve the report together with the real screenshots and output files.")
    else:
        if not submission["ready"]:
            lines.append("- Fill `tests/platform_submission_evidence_template.json` with real SkillHub/submit evidence paths and the live SkillHub URL.")
        if not full_run_ready:
            lines.append("- Finish all T01-T39 AstronClaw runs, mark them passed, and point every row to a real screenshot or output file.")
        if not enterprise_ready:
            lines.append("- Finish all S01-S10 enterprise-flow runs and save each real output or screenshot path.")
        if not stability_ready:
            lines.append("- Finish all ST01-ST12 stability stress runs and save each real output or screenshot path.")
        if not pilot["ready"]:
            lines.append("- Collect at least 3 real anonymized pilot feedback records with timing, evidence files and zero unsafe claims.")
        lines.append("- Keep the claims boundary: local readiness can be proven now, but champion completion is not yet proven.")
    lines.append("")
    return "\n".join(lines), champion_ready


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=str(DEFAULT_OUT), help="Output markdown report")
    parser.add_argument("--strict", action="store_true", help="Fail unless champion-level evidence is complete")
    parser.add_argument("--skip-local-gates", action="store_true", help="Skip validate/smoke/expert local gates")
    args = parser.parse_args()

    report, champion_ready = render_report(args.skip_local_gates)
    out = Path(args.out)
    out.write_text(report, encoding="utf-8")
    print(f"wrote={out}")
    print(f"champion_ready={'yes' if champion_ready else 'no'}")
    if args.strict and not champion_ready:
        raise SystemExit("champion acceptance evidence is incomplete")


if __name__ == "__main__":
    main()
