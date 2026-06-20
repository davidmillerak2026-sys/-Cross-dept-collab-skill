#!/usr/bin/env python3
"""Render department feedback timeline and state-transition analysis."""

from __future__ import annotations

import argparse
import csv
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "examples" / "data" / "sku_quality_coordination_timeline.csv"
DEFAULT_OUT = ROOT / "tests" / "sku_department_timeline_analysis.md"
TIME_FORMAT = "%Y-%m-%d %H:%M"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    if not rows:
        raise SystemExit(f"no timeline rows found: {path}")
    rows.sort(key=lambda row: datetime.strptime(row["event_time"], TIME_FORMAT))
    return rows


def minutes_between(start: str, end: str) -> int:
    start_dt = datetime.strptime(start, TIME_FORMAT)
    end_dt = datetime.strptime(end, TIME_FORMAT)
    return int((end_dt - start_dt).total_seconds() // 60)


def row_status(row: dict[str, str]) -> str:
    if row["event_time"] > row["feedback_due_by"]:
        return "late"
    if row["event_time"] == row["feedback_due_by"]:
        return "at_deadline"
    return "on_track"


def classify_blocker(row: dict[str, str]) -> str:
    state = row["state_after"].lower()
    if "pending" in state or "open" in state or "required" in state or "in_progress" in state:
        return "open"
    return "controlled"


def render_report(input_path: Path) -> str:
    rows = read_rows(input_path)
    event_id = rows[0]["event_id"]
    start = rows[0]["event_time"]
    end = rows[-1]["event_time"]
    total_minutes = minutes_between(start, end)
    latest_open_by_department: dict[str, dict[str, str]] = {}
    for row in rows:
        if classify_blocker(row) == "open":
            latest_open_by_department[row["department"]] = row
        elif row["department"] in latest_open_by_department:
            latest_open_by_department.pop(row["department"])
    open_blockers = list(latest_open_by_department.values())
    late_rows = [row for row in rows if row_status(row) == "late"]
    systems = sorted({row["formal_system"] for row in rows})
    departments = sorted({row["department"] for row in rows})

    lines = [
        "# SKU Department Timeline Analysis",
        "",
        f"- source_data: `{input_path.relative_to(ROOT).as_posix()}`",
        f"- event_id: `{event_id}`",
        f"- timeline_window: `{start}` to `{end}`",
        f"- elapsed_minutes: `{total_minutes}`",
        f"- transition_count: `{len(rows)}`",
        f"- departments: `{', '.join(departments)}`",
        f"- formal_systems: `{', '.join(systems)}`",
        f"- open_blocker_count: `{len(open_blockers)}`",
        f"- late_feedback_count: `{len(late_rows)}`",
        "",
        "## Timeline",
        "",
        "| Time | Department | Formal system | Action | State transition | Due | SLA | Receipt | Decision effect |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]

    for row in rows:
        lines.append(
            f"| {row['event_time']} | {row['department']} | {row['formal_system']} | {row['action']} | "
            f"`{row['state_before']}` -> `{row['state_after']}` | {row['feedback_due_by']} | {row_status(row)} | "
            f"{row['receipt_required']} | {row['decision_effect']} |"
        )

    lines.extend(
        [
            "",
            "## Current Open Blockers",
            "",
            "| State | Owner | Required receipt | Escalation owner | Why it matters |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for row in open_blockers:
        lines.append(
            f"| `{row['state_after']}` | {row['department']} | {row['receipt_required']} | "
            f"{row['escalation_owner']} | {row['decision_effect']} |"
        )

    if not open_blockers:
        lines.append("| none | - | - | - | all tracked states are controlled |")

    lines.extend(
        [
            "",
            "## Coordination Interpretation",
            "",
            "- Production remains the event owner because it owns the unified event package, sync cadence, MES production impact and OA escalation packet.",
            "- Quality feedback changes the event from production hold to QMS disposition pending; shipment cannot continue from the affected batch until QMS release exists.",
            "- Warehouse feedback separates released inventory from the affected batch, preventing accidental shipment while preserving a partial-shipment option.",
            "- PMC feedback turns the quality issue into delivery options, not a direct customer commitment; customer-facing promises remain gated by authorization.",
            "- Engineering feedback keeps root cause as a candidate until onsite validation and trial records exist.",
            "- Management decision is required because QMS disposition, engineering validation, PMC schedule version and WMS hold/unlock receipts are still formal blockers.",
            "",
            "## Guardrail",
            "",
            "Do not write 已放行、已发货、已恢复生产 or 已关闭 until QMS, WMS, MES, PMC/APS and OA receipts prove those states.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=str(DEFAULT_INPUT), help="Timeline CSV input")
    parser.add_argument("--out", default=str(DEFAULT_OUT), help="Markdown report output")
    args = parser.parse_args()

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render_report(Path(args.input)), encoding="utf-8")
    print(f"wrote={out}")


if __name__ == "__main__":
    main()
