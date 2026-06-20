#!/usr/bin/env python3
"""Save one copied V29 AstronClaw GUI output and update the retest record.

Typical use after copying the AstronClaw page output:

  python scripts/save_v29_output.py --model Qwen3.6 --case V29-G01 --from-clipboard

Alternative use with a text file:

  python scripts/save_v29_output.py --model GLM5.1 --case V29-G01 --input-file output.txt

The script:

1. writes `outputs/<model>/<case>.md`
2. scores that output with `score_v29_retest.py` heuristics
3. updates `v29_run_record.csv`
4. regenerates `v29_score_report.csv`
5. regenerates `v29_summary.md`
"""

from __future__ import annotations

import argparse
import csv
import ctypes
import subprocess
import sys
from datetime import date
from pathlib import Path

from score_v29_retest import DEFAULT_OUTPUTS, DEFAULT_REPORT, DEFAULT_RUN_RECORD, ROOT, score_text


MODELS = [
    "Spark-X2-Flash",
    "GLM5.1",
    "MiniMax2.5",
    "Kimi2.6",
    "Qwen3.6",
    "DeepSeek-v4-pro",
]

CASES = [f"V29-G{idx:02d}" for idx in range(1, 9)]


def read_clipboard() -> str:
    if sys.platform.startswith("win"):
        return get_windows_clipboard_text()
    raise RuntimeError("--from-clipboard is currently implemented for Windows PowerShell only")


def get_windows_clipboard_text() -> str:
    user32 = ctypes.windll.user32
    kernel32 = ctypes.windll.kernel32
    user32.GetClipboardData.restype = ctypes.c_void_p
    user32.GetClipboardData.argtypes = [ctypes.c_uint]
    kernel32.GlobalLock.restype = ctypes.c_void_p
    kernel32.GlobalLock.argtypes = [ctypes.c_void_p]
    kernel32.GlobalUnlock.argtypes = [ctypes.c_void_p]
    cf_unicode_text = 13
    if not user32.OpenClipboard(None):
        raise OSError("OpenClipboard failed")
    try:
        handle = user32.GetClipboardData(cf_unicode_text)
        if not handle:
            return ""
        locked = kernel32.GlobalLock(handle)
        if not locked:
            raise OSError("GlobalLock failed")
        try:
            return ctypes.wstring_at(locked)
        finally:
            kernel32.GlobalUnlock(handle)
    finally:
        user32.CloseClipboard()


def read_input(args: argparse.Namespace) -> str:
    sources = [bool(args.input_file), args.stdin, args.from_clipboard]
    if sum(sources) != 1:
        raise SystemExit("Choose exactly one input source: --input-file, --stdin, or --from-clipboard")
    if args.input_file:
        return Path(args.input_file).read_text(encoding="utf-8")
    if args.stdin:
        return sys.stdin.read()
    return read_clipboard()


def normalize_output(model: str, case_id: str, text: str) -> str:
    body = text.strip()
    if not body:
        raise SystemExit("Input output text is empty")
    if body.startswith("#"):
        return body + "\n"
    return f"# {model} {case_id} GUI Output\n\n{body}\n"


def relative_to_root(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def update_run_record(
    run_record: Path,
    model: str,
    case_id: str,
    output_file: Path,
    score_row: dict[str, str | int],
) -> None:
    rows: list[dict[str, str]] = []
    with run_record.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        fieldnames = reader.fieldnames
        if not fieldnames:
            raise SystemExit(f"Run record has no header: {run_record}")
        for row in reader:
            if row["model"] == model and row["case_id"] == case_id:
                risk = str(score_row["risk_level"])
                row["run_date"] = date.today().isoformat()
                row["output_file"] = relative_to_root(output_file)
                row["old_issue_fixed"] = "yes" if risk in {"pass", "minor"} else "no"
                row["collaboration_quality"] = "pass" if risk in {"pass", "minor"} else "review"
                row["risk_level"] = risk
                row["score"] = str(score_row["score"])
                row["issues"] = str(score_row["issue_labels"])
                row["next_action"] = "continue_matrix" if risk in {"pass", "minor"} else "manual_review_and_fix"
            rows.append(row)

    matched = any(row["model"] == model and row["case_id"] == case_id for row in rows)
    if not matched:
        raise SystemExit(f"No run-record row for model={model} case={case_id}")

    with run_record.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def regenerate_score_report(outputs: Path, run_record: Path, report: Path) -> None:
    script = ROOT / "scripts" / "score_v29_retest.py"
    subprocess.run(
        [
            sys.executable,
            str(script),
            "--outputs",
            str(outputs),
            "--run-record",
            str(run_record),
            "--report",
            str(report),
        ],
        check=True,
    )


def regenerate_summary(run_record: Path, report: Path) -> None:
    script = ROOT / "scripts" / "summarize_v29_retest.py"
    summary = report.with_name("v29_summary.md")
    subprocess.run(
        [
            sys.executable,
            str(script),
            "--run-record",
            str(run_record),
            "--score-report",
            str(report),
            "--summary",
            str(summary),
        ],
        check=True,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True, choices=MODELS)
    parser.add_argument("--case", required=True, choices=CASES, dest="case_id")
    parser.add_argument("--input-file")
    parser.add_argument("--stdin", action="store_true")
    parser.add_argument("--from-clipboard", action="store_true")
    parser.add_argument("--outputs", default=str(DEFAULT_OUTPUTS))
    parser.add_argument("--run-record", default=str(DEFAULT_RUN_RECORD))
    parser.add_argument("--report", default=str(DEFAULT_REPORT))
    args = parser.parse_args()

    outputs = Path(args.outputs)
    run_record = Path(args.run_record)
    report = Path(args.report)
    output_file = outputs / args.model / f"{args.case_id}.md"
    output_file.parent.mkdir(parents=True, exist_ok=True)

    text = normalize_output(args.model, args.case_id, read_input(args))
    output_file.write_text(text, encoding="utf-8")

    score_row = score_text(args.model, args.case_id, text)
    update_run_record(run_record, args.model, args.case_id, output_file, score_row)
    regenerate_score_report(outputs, run_record, report)
    regenerate_summary(run_record, report)

    print(
        "saved_v29_output "
        f"model={args.model} case={args.case_id} "
        f"score={score_row['score']} risk={score_row['risk_level']} "
        f"file={relative_to_root(output_file)}"
    )


if __name__ == "__main__":
    main()
