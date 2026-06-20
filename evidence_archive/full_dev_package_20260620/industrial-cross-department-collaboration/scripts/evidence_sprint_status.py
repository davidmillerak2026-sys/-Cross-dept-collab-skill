#!/usr/bin/env python3
"""Render a phase-by-phase status report for expert evidence sprint execution."""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TESTS = ROOT / "tests"
MANIFEST = TESTS / "expert_evidence_sprint_manifest.csv"
PLATFORM = TESTS / "platform_submission_evidence_template.json"
RUN_RECORD = TESTS / "run_record_template.csv"
ENTERPRISE_RECORD = TESTS / "run_record_enterprise_flow_template.csv"
STABILITY_RECORD = TESTS / "run_record_stability_stress_template.csv"
PILOT_RECORD = TESTS / "pilot_feedback_records_template.csv"
DEFAULT_OUT = TESTS / "expert_evidence_sprint_status.md"
EVIDENCE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".pdf", ".md", ".txt"}


def read_csv(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def truthy(value: str) -> bool:
    return value.strip().lower() in {"yes", "pass", "passed", "true", "1"}


def evidence_exists(reference: str) -> bool:
    ref = reference.strip()
    if not ref:
        return False
    if ref.startswith("http://") or ref.startswith("https://"):
        return True
    path = Path(ref)
    if not path.is_absolute():
        path = ROOT / ref
    if path.suffix.lower() not in EVIDENCE_EXTENSIONS:
        return False
    return path.exists() and path.is_file()


def load_platform() -> dict:
    return json.loads(PLATFORM.read_text(encoding="utf-8"))


def load_run_record_map(path: Path) -> dict[str, dict]:
    return {row["case_id"]: row for row in read_csv(path)}


def summarize_pilot_role(role_id: str) -> dict:
    rows = [row for row in read_csv(PILOT_RECORD) if row.get("role_id") == role_id and "YYYYMMDD" not in row.get("feedback_id", "")]
    if not rows:
        return {"recorded": False, "artifact": False, "done": False, "detail": "no_real_feedback"}
    best = rows[0]
    recorded = all(
        best.get(key, "").strip()
        for key in ["before_minutes", "after_minutes", "manual_confirmation_boundary", "consent_to_public"]
    )
    artifact = evidence_exists(best.get("evidence_file_or_screenshot", ""))
    return {
        "recorded": recorded,
        "artifact": artifact,
        "done": recorded and artifact,
        "detail": f"feedback_id={best.get('feedback_id', '')}",
    }


def status_for_row(row: dict, platform_data: dict, run_maps: dict[str, dict[str, dict]]) -> dict:
    track = row["track"]
    item_id = row["item_id"]
    if track == "platform_submission":
        value = str(platform_data.get(item_id, "")).strip()
        recorded = bool(value)
        artifact = evidence_exists(value) if item_id != "skillhub_public_url" else bool(value)
        return {
            "recorded": recorded,
            "artifact": artifact,
            "done": recorded and artifact,
            "detail": value or "missing",
        }
    if track == "required_cases":
        run = run_maps["required_cases"].get(item_id, {})
        recorded = bool(run.get("platform", "").strip()) and bool(run.get("passed", "").strip())
        artifact = evidence_exists(run.get("output_file_or_screenshot", ""))
        secondary = evidence_exists(row.get("suggested_secondary_artifact", ""))
        return {
            "recorded": recorded and truthy(run.get("passed", "")),
            "artifact": artifact,
            "done": recorded and truthy(run.get("passed", "")) and artifact,
            "detail": f"run_output={'yes' if secondary else 'no'}",
        }
    if track == "enterprise_flow":
        run = run_maps["enterprise_flow"].get(item_id, {})
        recorded = bool(run.get("platform", "").strip()) and bool(run.get("passed", "").strip())
        artifact = evidence_exists(run.get("output_file_or_screenshot", ""))
        secondary = evidence_exists(row.get("suggested_secondary_artifact", ""))
        return {
            "recorded": recorded and truthy(run.get("passed", "")),
            "artifact": artifact,
            "done": recorded and truthy(run.get("passed", "")) and artifact,
            "detail": f"enterprise_output={'yes' if secondary else 'no'}",
        }
    if track == "stability_stress":
        run = run_maps["stability_stress"].get(item_id, {})
        recorded = bool(run.get("platform", "").strip()) and bool(run.get("passed", "").strip())
        artifact = evidence_exists(run.get("output_file_or_screenshot", ""))
        secondary = evidence_exists(row.get("suggested_secondary_artifact", ""))
        return {
            "recorded": recorded and truthy(run.get("passed", "")),
            "artifact": artifact,
            "done": recorded and truthy(run.get("passed", "")) and artifact,
            "detail": f"stability_output={'yes' if secondary else 'no'}",
        }
    if track == "pilot_feedback":
        return summarize_pilot_role(item_id)
    return {"recorded": False, "artifact": False, "done": False, "detail": "unknown_track"}


def render_report() -> str:
    manifest_rows = read_csv(MANIFEST)
    platform_data = load_platform()
    run_maps = {
        "required_cases": load_run_record_map(RUN_RECORD),
        "enterprise_flow": load_run_record_map(ENTERPRISE_RECORD),
        "stability_stress": load_run_record_map(STABILITY_RECORD),
    }

    phased: dict[str, list[dict]] = defaultdict(list)
    required_total = 0
    required_done = 0
    optional_total = 0
    optional_done = 0
    enriched_rows = []

    for row in manifest_rows:
        status = status_for_row(row, platform_data, run_maps)
        enriched = {**row, **status}
        enriched_rows.append(enriched)
        phased[row["phase"]].append(enriched)
        if row["priority"] == "optional":
            optional_total += 1
            if status["done"]:
                optional_done += 1
        else:
            required_total += 1
            if status["done"]:
                required_done += 1

    lines = [
        "# Expert Evidence Sprint Status",
        "",
        "This report tracks phase-by-phase progress for the ranked expert evidence sprint plan. It is designed to reduce missed screenshots, missing run records, and forgotten pilot-feedback evidence.",
        "",
        "## Summary",
        "",
        f"- required_completed: {required_done}/{required_total}",
        f"- optional_completed: {optional_done}/{optional_total}",
        f"- overall_completed: {required_done + optional_done}/{required_total + optional_total}",
        f"- skillhub_public_url_recorded: {'yes' if str(platform_data.get('skillhub_public_url', '')).strip() else 'no'}",
        "",
    ]

    phase_titles = {
        "0": "Platform Unlock",
        "1": "First-Wave Required Screenshots",
        "2": "Remaining Required Screenshots",
        "3": "High-Impact Enterprise Flow",
        "4": "Remaining Enterprise Flow",
        "5": "High-Risk Stability Stress",
        "6": "Remaining Stability Stress",
        "7": "Pilot Feedback Minimum Gate",
        "8": "Pilot Feedback Expansion",
    }

    for phase in sorted(phased, key=lambda value: int(value)):
        rows = phased[phase]
        done = sum(1 for row in rows if row["done"])
        lines.extend(
            [
                f"## Phase {phase} {phase_titles.get(phase, '')}".rstrip(),
                "",
                f"- completed: {done}/{len(rows)}",
                "",
                "| Item | Track | Priority | Recorded | Artifact | Done | Detail |",
                "| --- | --- | --- | --- | --- | --- | --- |",
            ]
        )
        for row in rows:
            lines.append(
                f"| `{row['item_id']}` | {row['track']} | {row['priority']} | "
                f"{'yes' if row['recorded'] else 'no'} | {'yes' if row['artifact'] else 'no'} | "
                f"{'yes' if row['done'] else 'no'} | {row['detail']} |"
            )
        lines.append("")

    pending_required = [row for row in enriched_rows if row["priority"] != "optional" and not row["done"]]
    pending_required.sort(key=lambda row: (int(row["phase"]), row["track"], row["item_id"]))
    lines.extend(["## Next Required Actions", ""])
    for row in pending_required[:15]:
        lines.append(
            f"- Phase {row['phase']} `{row['item_id']}` {row['title']} -> 补 `{row['suggested_primary_artifact']}`；"
            f"记录文件 `{row['record_file']}`；建议命令 `{row['scoring_command']}`"
        )
    if not pending_required:
        lines.append("- Required evidence rows are complete. Run `python scripts/expert_rubric_gate.py --require-astronclaw` and preserve all artifacts.")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=str(DEFAULT_OUT), help="Output markdown status report")
    args = parser.parse_args()

    out = Path(args.out)
    out.write_text(render_report(), encoding="utf-8")
    print(f"wrote={out}")


if __name__ == "__main__":
    main()
