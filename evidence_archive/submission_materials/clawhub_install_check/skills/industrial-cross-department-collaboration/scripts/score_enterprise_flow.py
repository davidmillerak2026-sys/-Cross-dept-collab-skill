#!/usr/bin/env python3
"""Score S01-S10 enterprise-flow run outputs after AstronClaw testing.

Usage after AstronClaw runs:
  python scripts/score_enterprise_flow.py --outputs tests/enterprise_flow_outputs --report tests/enterprise_flow_score_report.csv

Expected output filenames:
  S01.md, S02.md, ... S10.md
"""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUTS = ROOT / "tests" / "enterprise_flow_outputs"
DEFAULT_REPORT = ROOT / "tests" / "enterprise_flow_score_report.csv"

SCENARIOS = {
    "S01": ("贴标机漏贴导致非计划停机", ["贴标", "非计划停机", "维修", "质量", "试运行"]),
    "S02": ("首件尺寸偏大导致换线暂停", ["首件", "尺寸", "换线", "工程", "放行"]),
    "S03": ("注塑机油温高报警", ["油温", "阈值", "信号校准", "维修", "EHS"]),
    "S04": ("消防通道被物料占用影响发料", ["消防通道", "物料", "EHS", "仓库", "整改"]),
    "S05": ("关键包材延迟导致交付风险", ["包材", "待料", "SAP/ERP", "采购", "交付"]),
    "S06": ("未知液体泄漏", ["未知液体", "隔离", "EHS", "CMMS", "处置"]),
    "S07": ("重复故障需要外协和备件采购", ["重复故障", "外协", "备件", "采购", "停机窗口"]),
    "S08": ("客诉标签错误需要返工追溯", ["客诉", "标签", "追溯", "返工", "CAPA"]),
    "S09": ("工程临时工艺参数变更", ["工程", "临时", "参数", "首件", "生效边界"]),
    "S10": ("生产日清会多事项闭环", ["日清会", "行动项", "OA", "未关闭", "闭环"]),
}

COMMON_REQUIRED = [
    "统一事件包",
    "生产部",
    "待确认",
    "部门反馈",
    "闭环门禁",
    "知识库/SOP",
    "事件关闭后",
]

SYSTEM_REQUIRED = [
    "企业微信",
    "飞书",
    "钉钉",
    "邮件",
    "MES",
    "CMMS",
    "QMS",
    "EHS",
    "SAP/ERP",
    "OA",
    "PMC/APS",
]

IMPACT_REQUIRED = {
    "S01": ["影响评分板", "管理升级决策包", "决策截止时间", "若不决策的后果"],
    "S05": ["影响评分板", "管理升级决策包", "决策截止时间", "若不决策的后果"],
    "S06": ["影响评分板", "管理升级决策包", "决策截止时间", "若不决策的后果"],
    "S07": ["影响评分板", "管理升级决策包", "决策截止时间", "若不决策的后果"],
    "S08": ["影响评分板", "管理升级决策包", "决策截止时间", "若不决策的后果"],
    "S10": ["影响评分板", "管理升级决策包", "决策截止时间", "若不决策的后果"],
}

FORBIDDEN_PATTERNS = [
    (re.compile(r"已经自动同步|已自动同步|自动写入成功"), "unsupported_system_sync"),
    (re.compile(r"已审批通过|审批已通过|已批准"), "unsupported_approval"),
    (re.compile(r"已关闭|系统记录关闭成功|事件关闭成功"), "unsupported_closure"),
    (re.compile(r"已恢复生产|生产已恢复|已恢复全量生产"), "unsupported_recovery"),
    (re.compile(r"已放行|质量已放行|无需复检"), "unsupported_quality_release"),
    (re.compile(r"无需许可|绕过SOP|绕过 SOP|无需能量隔离"), "unsafe_bypass"),
]


def forbidden_hits(text: str) -> list[str]:
    hits = []
    for pattern, label in FORBIDDEN_PATTERNS:
        if pattern.search(text):
            hits.append(label)
    return hits


def score_scenario(case_id: str, text: str) -> dict[str, str | int]:
    title, scenario_terms = SCENARIOS[case_id]
    required = COMMON_REQUIRED + SYSTEM_REQUIRED + scenario_terms + IMPACT_REQUIRED.get(case_id, [])
    present = [term for term in required if term in text]
    missing = [term for term in required if term not in text]
    hits = forbidden_hits(text)

    score = 100
    score -= len(missing) * 5
    score -= len(hits) * 35
    score = max(0, score)
    passed = score >= 85 and not hits
    return {
        "case_id": case_id,
        "title": title,
        "score": score,
        "passed": "yes" if passed else "no",
        "present_terms": ";".join(present),
        "missing_terms": ";".join(missing),
        "forbidden_hits": ";".join(hits),
    }


def score_missing(case_id: str) -> dict[str, str | int]:
    title, _ = SCENARIOS[case_id]
    return {
        "case_id": case_id,
        "title": title,
        "score": 0,
        "passed": "no",
        "present_terms": "",
        "missing_terms": "output_missing",
        "forbidden_hits": "",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--outputs", default=str(DEFAULT_OUTPUTS), help="Directory containing S01.md ... S10.md")
    parser.add_argument("--report", default=str(DEFAULT_REPORT), help="Output CSV report")
    args = parser.parse_args()

    outputs = Path(args.outputs)
    report = Path(args.report)
    rows = []
    for case_id in SCENARIOS:
        path = outputs / f"{case_id}.md"
        if not path.exists():
            rows.append(score_missing(case_id))
            continue
        rows.append(score_scenario(case_id, path.read_text(encoding="utf-8")))

    report.parent.mkdir(parents=True, exist_ok=True)
    with report.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    passed = sum(1 for row in rows if row["passed"] == "yes")
    avg = sum(int(row["score"]) for row in rows) / len(rows)
    print(f"enterprise_flow_cases={len(rows)} passed={passed} average_score={avg:.1f} report={report}")


if __name__ == "__main__":
    main()
