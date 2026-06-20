#!/usr/bin/env python3
"""Redact sensitive fields from industrial field records before evaluation.

Usage:
  python scripts/redact_input.py --text "张三 13800138000 反馈..."
  python scripts/redact_input.py --file record.txt
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


PATTERNS: list[tuple[str, str]] = [
    (r"(?<!\d)1[3-9]\d{9}(?!\d)", "[手机号已脱敏]"),
    (r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", "[邮箱已脱敏]"),
    (r"(?<![0-9A-Za-z])\d{17}[\dXx](?![0-9A-Za-z])", "[身份证号已脱敏]"),
    (r"(?i)(api[_-]?key|access[_-]?key|secret|password|token)\s*[:=]\s*[^\s,;]+", "[凭证已脱敏]"),
    (r"(?i)(bearer\s+)[A-Za-z0-9._~+/-]{12,}", "[凭证已脱敏]"),
    (r"(?i)(cookie|sessionid)\s*[:=]\s*[^\s,;]+", "[凭证已脱敏]"),
]


def redact(text: str) -> str:
    result = text
    for pattern, replacement in PATTERNS:
        result = re.sub(pattern, replacement, result)
    return result


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Redact sensitive industrial record text.")
    source = parser.add_mutually_exclusive_group()
    source.add_argument("--text", help="Text to redact.")
    source.add_argument("--file", type=Path, help="UTF-8 text file to redact.")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    if args.text is not None:
        text = args.text
    elif args.file is not None:
        text = args.file.read_text(encoding="utf-8")
    else:
        text = sys.stdin.read()
    print(redact(text))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
