#!/usr/bin/env python3
"""Print or copy the next V29 AstronClaw GUI prompt.

Default behavior:
  - read `v29_run_record.csv`
  - find the first row without `output_file`
  - print model, case id, and prompt

Convenience:
  python scripts/next_v29_prompt.py --copy
  python scripts/next_v29_prompt.py --model Qwen3.6 --copy
  python scripts/next_v29_prompt.py --case V29-G02 --copy
"""

from __future__ import annotations

import argparse
import csv
import ctypes
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ROOT = (
    ROOT
    / "evidence_archive"
    / "submission_materials"
    / "astronclaw_real_runs"
    / "20260620_v29_retest"
)
DEFAULT_PROMPT_PACK = DEFAULT_ROOT / "v29_prompt_pack.md"
DEFAULT_RUN_RECORD = DEFAULT_ROOT / "v29_run_record.csv"

MODELS = [
    "Spark-X2-Flash",
    "GLM5.1",
    "MiniMax2.5",
    "Kimi2.6",
    "Qwen3.6",
    "DeepSeek-v4-pro",
]

CASES = [f"V29-G{idx:02d}" for idx in range(1, 9)]


PROMPT_BLOCK_RE = re.compile(
    r"##\s+(V29-G\d{2})\s+.*?```text\s*(.*?)\s*```",
    re.DOTALL,
)


def load_prompts(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    prompts = {case_id: prompt.strip() for case_id, prompt in PROMPT_BLOCK_RE.findall(text)}
    missing = [case_id for case_id in CASES if case_id not in prompts]
    if missing:
        raise SystemExit(f"Missing prompts for: {', '.join(missing)}")
    return prompts


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def choose_row(rows: list[dict[str, str]], model: str | None, case_id: str | None) -> dict[str, str]:
    candidates = rows
    if model:
        candidates = [row for row in candidates if row["model"] == model]
    if case_id:
        candidates = [row for row in candidates if row["case_id"] == case_id]
    if not candidates:
        raise SystemExit("No matching run-record row")
    for row in candidates:
        if not row.get("output_file", "").strip():
            return row
    raise SystemExit("All matching rows already have output_file")


def copy_to_clipboard(text: str) -> None:
    if sys.platform.startswith("win"):
        set_windows_clipboard_text(text)
        return
    if sys.platform == "darwin":
        subprocess.run(["pbcopy"], input=text, text=True, encoding="utf-8", check=True)
        return
    raise RuntimeError("--copy is currently supported on Windows and macOS")


def set_windows_clipboard_text(text: str) -> None:
    user32 = ctypes.windll.user32
    kernel32 = ctypes.windll.kernel32
    kernel32.GlobalAlloc.restype = ctypes.c_void_p
    kernel32.GlobalAlloc.argtypes = [ctypes.c_uint, ctypes.c_size_t]
    kernel32.GlobalLock.restype = ctypes.c_void_p
    kernel32.GlobalLock.argtypes = [ctypes.c_void_p]
    kernel32.GlobalUnlock.argtypes = [ctypes.c_void_p]
    kernel32.GlobalFree.argtypes = [ctypes.c_void_p]
    user32.SetClipboardData.restype = ctypes.c_void_p
    user32.SetClipboardData.argtypes = [ctypes.c_uint, ctypes.c_void_p]
    cf_unicode_text = 13
    gmem_moveable = 0x0002
    data = (text + "\0").encode("utf-16-le")
    handle = kernel32.GlobalAlloc(gmem_moveable, len(data))
    if not handle:
        raise OSError("GlobalAlloc failed")
    locked = kernel32.GlobalLock(handle)
    if not locked:
        kernel32.GlobalFree(handle)
        raise OSError("GlobalLock failed")
    ctypes.memmove(locked, data, len(data))
    kernel32.GlobalUnlock(handle)
    if not user32.OpenClipboard(None):
        kernel32.GlobalFree(handle)
        raise OSError("OpenClipboard failed")
    try:
        user32.EmptyClipboard()
        if not user32.SetClipboardData(cf_unicode_text, handle):
            kernel32.GlobalFree(handle)
            raise OSError("SetClipboardData failed")
        handle = None
    finally:
        user32.CloseClipboard()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", choices=MODELS)
    parser.add_argument("--case", choices=CASES, dest="case_id")
    parser.add_argument("--prompt-pack", default=str(DEFAULT_PROMPT_PACK))
    parser.add_argument("--run-record", default=str(DEFAULT_RUN_RECORD))
    parser.add_argument("--copy", action="store_true", help="Copy only the natural-language prompt to clipboard")
    parser.add_argument("--with-header", action="store_true", help="Include model/case header when copying")
    args = parser.parse_args()

    prompts = load_prompts(Path(args.prompt_pack))
    row = choose_row(load_rows(Path(args.run_record)), args.model, args.case_id)
    prompt = prompts[row["case_id"]]
    header = (
        f"model={row['model']} case={row['case_id']} "
        f"version={row['version_under_test']}"
    )
    clipboard_text = f"{header}\n\n{prompt}" if args.with_header else prompt

    if args.copy:
        copy_to_clipboard(clipboard_text)
        print(f"copied_next_v29_prompt {header}")
    else:
        print(header)
        print()
        print(prompt)


if __name__ == "__main__":
    main()
