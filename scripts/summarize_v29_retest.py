#!/usr/bin/env python3
"""Create a Markdown summary for the V29 AstronClaw GUI retest."""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ROOT = (
    ROOT
    / "evidence_archive"
    / "submission_materials"
    / "astronclaw_real_runs"
    / "20260620_v29_retest"
)
DEFAULT_RUN_RECORD = DEFAULT_ROOT / "v29_run_record.csv"
DEFAULT_SCORE_REPORT = DEFAULT_ROOT / "v29_score_report.csv"
DEFAULT_SUMMARY = DEFAULT_ROOT / "v29_summary.md"

MODEL_ORDER = [
    "Spark-X2-Flash",
    "GLM5.1",
    "MiniMax2.5",
    "Kimi2.6",
    "Qwen3.6",
    "DeepSeek-v4-pro",
]

CASE_ORDER = [f"V29-G{idx:02d}" for idx in range(1, 9)]

CASE_TITLES = {
    "V29-G01": "Changeover first article near limit",
    "V29-G02": "ICT drift / false judgment",
    "V29-G03": "QMS outage temporary opinion",
    "V29-G04": "Supplier ETA and unknown inventory",
    "V29-G05": "Closure with chat-only evidence",
    "V29-G06": "Wrong-label shipment gate",
    "V29-G07": "EHS permit before electrical cabinet",
    "V29-G08": "Incremental multi-channel status update",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def escape_cell(value: object) -> str:
    text = "" if value is None else str(value)
    text = text.replace("\n", " ").replace("|", "\\|")
    return text


def markdown_table(headers: list[str], rows: list[list[object]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(escape_cell(value) for value in row) + " |")
    return "\n".join(lines)


def summarize(run_rows: list[dict[str, str]], score_rows: list[dict[str, str]]) -> str:
    score_by_key = {(row["model"], row["case_id"]): row for row in score_rows}
    planned = len(run_rows)
    completed_rows = [row for row in run_rows if row.get("output_file", "").strip()]
    completed = len(completed_rows)
    score_completed = [
        score_by_key[(row["model"], row["case_id"])]
        for row in completed_rows
        if (row["model"], row["case_id"]) in score_by_key
    ]
    pass_count = sum(1 for row in score_completed if row.get("risk_level") == "pass")
    minor_count = sum(1 for row in score_completed if row.get("risk_level") == "minor")
    major_count = sum(1 for row in score_completed if row.get("risk_level") == "major")
    blocker_count = sum(1 for row in score_completed if row.get("risk_level") == "blocker")
    avg_score = (
        sum(int(row.get("score") or 0) for row in score_completed) / len(score_completed)
        if score_completed
        else 0.0
    )

    by_model: dict[str, list[dict[str, str]]] = defaultdict(list)
    by_case: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in run_rows:
        by_model[row["model"]].append(row)
        by_case[row["case_id"]].append(row)

    model_rows = []
    for model in MODEL_ORDER:
        rows = by_model.get(model, [])
        done = [row for row in rows if row.get("output_file", "").strip()]
        scored = [score_by_key[(row["model"], row["case_id"])] for row in done if (row["model"], row["case_id"]) in score_by_key]
        model_rows.append([
            model,
            f"{len(done)}/{len(rows)}",
            sum(1 for row in scored if row.get("risk_level") == "pass"),
            sum(1 for row in scored if row.get("risk_level") in {"major", "blocker"}),
            f"{(sum(int(row.get('score') or 0) for row in scored) / len(scored)):.1f}" if scored else "-",
        ])

    case_rows = []
    for case_id in CASE_ORDER:
        rows = by_case.get(case_id, [])
        done = [row for row in rows if row.get("output_file", "").strip()]
        scored = [score_by_key[(row["model"], row["case_id"])] for row in done if (row["model"], row["case_id"]) in score_by_key]
        issue_counter = Counter()
        for row in scored:
            for label in (row.get("issue_labels") or "").split(";"):
                if label:
                    issue_counter[label] += 1
        top_issues = ", ".join(f"{label}({count})" for label, count in issue_counter.most_common(3)) or "-"
        case_rows.append([
            case_id,
            CASE_TITLES.get(case_id, ""),
            f"{len(done)}/{len(rows)}",
            sum(1 for row in scored if row.get("risk_level") == "pass"),
            sum(1 for row in scored if row.get("risk_level") in {"major", "blocker"}),
            top_issues,
        ])

    issue_counter = Counter()
    issue_evidence: dict[str, str] = {}
    for row in score_completed:
        for label in (row.get("issue_labels") or "").split(";"):
            if not label:
                continue
            issue_counter[label] += 1
            issue_evidence.setdefault(label, row.get("issue_evidence", ""))

    issue_rows = [
        [label, count, issue_evidence.get(label, "")]
        for label, count in issue_counter.most_common(12)
    ]
    if not issue_rows:
        issue_rows = [["-", 0, "No scored issues yet"]]

    next_rows = [
        row for row in run_rows if not row.get("output_file", "").strip()
    ][:6]
    next_table_rows = [
        [row["model"], row["case_id"], CASE_TITLES.get(row["case_id"], "")]
        for row in next_rows
    ] or [["-", "-", "All planned rows have outputs"]]

    lines = [
        "# V29 AstronClaw GUI Retest Summary",
        "",
        f"Generated: {datetime.now().isoformat(timespec='seconds')}",
        "",
        "## Overall",
        "",
        markdown_table(
            ["Planned", "Completed", "Pass", "Minor", "Major", "Blocker", "Average Score"],
            [[planned, completed, pass_count, minor_count, major_count, blocker_count, f"{avg_score:.1f}"]],
        ),
        "",
        "## By Model",
        "",
        markdown_table(["Model", "Completed", "Pass", "Major/Blocker", "Average Score"], model_rows),
        "",
        "## By Scenario",
        "",
        markdown_table(["Case", "Scenario", "Completed", "Pass", "Major/Blocker", "Top Issues"], case_rows),
        "",
        "## Top Issues",
        "",
        markdown_table(["Issue", "Count", "Sample Evidence"], issue_rows),
        "",
        "## Next Rows",
        "",
        markdown_table(["Model", "Case", "Scenario"], next_table_rows),
        "",
        "## Notes",
        "",
        "- This summary is generated from `v29_run_record.csv` and `v29_score_report.csv`.",
        "- The score report is a fast defect screen; manual review still decides whether to update the Skill.",
        "- Missing outputs are expected until the GUI matrix is fully run.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-record", default=str(DEFAULT_RUN_RECORD))
    parser.add_argument("--score-report", default=str(DEFAULT_SCORE_REPORT))
    parser.add_argument("--summary", default=str(DEFAULT_SUMMARY))
    args = parser.parse_args()

    run_record = Path(args.run_record)
    score_report = Path(args.score_report)
    summary = Path(args.summary)
    text = summarize(read_csv(run_record), read_csv(score_report))
    summary.parent.mkdir(parents=True, exist_ok=True)
    summary.write_text(text, encoding="utf-8")
    print(f"v29_summary written={summary}")


if __name__ == "__main__":
    main()
