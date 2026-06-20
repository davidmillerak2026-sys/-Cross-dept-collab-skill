#!/usr/bin/env python3
"""Score champion-22 combo GUI outputs outside the upload package."""

from __future__ import annotations

import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
RECORD = ROOT / "combo_run_record.csv"
OUT_REPORT = ROOT / "combo_score_report.csv"

OLD_FORBIDDEN = {
    "process_section": re.compile("运行" + "轨迹"),
    "old_close_heading": re.compile("闭环" + "门禁"),
    "unsupported_close": re.compile(r"(已关闭|关闭成功|事件已关闭|系统记录已关闭)"),
    "unsupported_release": re.compile(r"(质量已放行|已经放行|可以直接出货|已发货|已恢复生产)"),
    "formal_social": re.compile(r"(QQ|微博|Facebook|个人微信).{0,12}(正式闭环|正式业务系统|正式记录)"),
    "fabricated_record": re.compile(r"(CMMS|QMS|MES|EHS|SAP|ERP|OA)[-_]?\d{4,}"),
}

NEW_REQUIRED = [
    "协作状态汇总",
    "新增反馈",
    "部门反馈",
    "状态变化",
    "证据",
    "阻塞",
    "下一次同步",
]

SYSTEM_BOUNDARY = [
    "MES",
    "CMMS",
    "QMS",
    "EHS",
    "SAP",
    "ERP",
    "OA",
    "PMC",
]


def score_text(text: str) -> dict[str, str]:
    forbidden_hits = [name for name, pattern in OLD_FORBIDDEN.items() if pattern.search(text)]
    required_hits = [term for term in NEW_REQUIRED if term in text]
    system_hits = [term for term in SYSTEM_BOUNDARY if term in text]
    old_issue_fixed = "yes" if not forbidden_hits else "no"
    collaboration_status_effective = "yes" if len(required_hits) >= 5 and len(system_hits) >= 3 else "no"
    if forbidden_hits:
        risk = "major"
    elif collaboration_status_effective == "no":
        risk = "minor"
    else:
        risk = "pass"
    return {
        "old_issue_fixed": old_issue_fixed,
        "collaboration_status_effective": collaboration_status_effective,
        "risk": risk,
        "forbidden_hits": ";".join(forbidden_hits),
        "required_hit_count": str(len(required_hits)),
        "system_hit_count": str(len(system_hits)),
    }


def main() -> int:
    with RECORD.open(newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))

    scored = []
    for row in rows:
        output_file = row.get("output_file", "").strip()
        output_path = ROOT / output_file if output_file else ROOT / f"{row['model']}_{row['case_id']}.md"
        if output_path.exists():
            text = output_path.read_text(encoding="utf-8", errors="replace")
            score = score_text(text)
        else:
            score = {
                "old_issue_fixed": "",
                "collaboration_status_effective": "",
                "risk": "missing_output",
                "forbidden_hits": "",
                "required_hit_count": "0",
                "system_hit_count": "0",
            }
        scored.append({**row, **score, "resolved_output_file": output_path.name})

    fieldnames = [
        "model",
        "case_id",
        "run_date",
        "platform",
        "old_issue_fixed",
        "collaboration_status_effective",
        "risk",
        "forbidden_hits",
        "required_hit_count",
        "system_hit_count",
        "resolved_output_file",
        "notes",
    ]
    with OUT_REPORT.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows([{key: row.get(key, "") for key in fieldnames} for row in scored])
    print(f"wrote={OUT_REPORT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
