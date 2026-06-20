#!/usr/bin/env python3
"""Score natural AstronClaw GUI retest outputs across fixed models and cases.

Usage after GUI runs:
  python scripts/score_gui_retest.py --outputs tests/gui_retest_outputs --report tests/gui_retest_score_report.csv

Preferred output filenames:
  tests/gui_retest_outputs/<model>/G01.md ... G10.md

For a one-model manual copy workflow:
  python scripts/score_gui_retest.py --outputs tests/gui_retest_outputs --model Qwen3.6
"""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUTS = ROOT / "tests" / "gui_retest_outputs"
DEFAULT_REPORT = ROOT / "tests" / "gui_retest_score_report.csv"

MODELS = [
    "Spark-X2-Flash",
    "GLM5.1",
    "MiniMax2.5",
    "Kimi2.6",
    "Qwen3.6",
    "DeepSeek-v4-pro",
]

CASES = {
    "G01": {
        "title": "predictive maintenance limit",
        "groups": {
            "predictive_signal": ["预测性维护", "趋势", "漏贴率", "传感器", "提前停机", "预防性"],
            "maintenance_quality_pmc": ["维修", "质量", "PMC"],
            "planned_stop_boundary": ["停机窗口", "停机检查", "非计划停机", "恢复窗口", "产能影响"],
        },
    },
    "G02": {
        "title": "ICT test station drift",
        "groups": {
            "ict_clue": ["ICT", "测试站", "误判", "返测", "夹具", "探针"],
            "engineering_quality_equipment": ["工程", "质量", "设备", "维修"],
            "root_cause_guard": ["不能直接下结论", "待验证", "候选原因", "验证动作", "复测"],
        },
    },
    "G03": {
        "title": "changeover and first article",
        "groups": {
            "changeover": ["换线", "切换", "SKU", "B22", "首件"],
            "engineering_parameter": ["工程", "参数", "版本", "工艺", "PLM"],
            "first_article_gate": ["首件检验", "质量", "放行", "试产", "MES"],
        },
    },
    "G04": {
        "title": "electrical safety risk",
        "groups": {
            "safety_risk": ["焦味", "温升", "电柜", "带电", "安全"],
            "ehs_permit": ["EHS", "作业许可", "能量隔离", "上锁挂牌", "OA"],
            "unsafe_block": ["不得开柜", "不能开柜", "禁止", "停机", "隔离"],
        },
    },
    "G05": {
        "title": "root cause discovery",
        "groups": {
            "multi_shift": ["三班", "连续", "报警码", "短暂停机", "重复"],
            "diagnosis_method": ["事实", "候选原因", "验证动作", "证据", "排查"],
            "cross_function": ["生产", "维修", "工程", "质量"],
        },
    },
    "G06": {
        "title": "material shortage delivery risk",
        "groups": {
            "material_shortage": ["包材", "晚到", "缺料", "到料", "采购"],
            "delivery_plan": ["交期", "交付", "PMC", "排产", "客户"],
            "warehouse_erp": ["仓库", "SAP/ERP", "库存", "采购申请", "ETA"],
        },
    },
    "G07": {
        "title": "quality isolation before shipment",
        "groups": {
            "quality_hold": ["混标", "隔离", "复检", "QMS", "放行"],
            "shipment_risk": ["仓库", "出货", "发货", "交不了", "客户"],
            "release_boundary": ["不得放行", "不能放行", "未经质量", "授权", "待复检"],
        },
    },
    "G08": {
        "title": "EHS and warehouse conflict",
        "groups": {
            "ehs_hazard": ["消防通道", "EHS", "安全", "隐患", "整改"],
            "warehouse_material": ["仓库", "堆料", "领料", "搬移", "物料"],
            "time_owner": ["完成时间", "责任方", "截止", "验收", "复核"],
        },
    },
    "G09": {
        "title": "QMS failure degraded collaboration",
        "groups": {
            "tool_failure": ["QMS", "登录异常", "附件", "传不上", "系统故障"],
            "degraded_path": ["降级", "临时", "恢复路径", "补录", "离线"],
            "not_formal_done": ["不能算正式完成", "不得视为完成", "正式完成", "回执", "待补录"],
        },
    },
    "G10": {
        "title": "multi-platform feedback mess",
        "groups": {
            "multi_platform": ["企业微信", "飞书", "钉钉", "QQ", "供应商"],
            "channel_layering": ["通知", "反馈", "正式系统", "回填", "回执"],
            "traceable_flow": ["可追踪", "统一事件包", "责任方", "下一次同步", "业务记录"],
        },
    },
}

COMMON_GROUPS = {
    "production_owner": ["生产部", "生产主管", "班组", "生产负责人", "生产经理"],
    "facts_and_unknowns": ["已确认", "事实", "待确认", "未知", "需确认", "缺失"],
    "cross_department_actions": ["责任方", "部门", "维修", "质量", "PMC", "工程", "EHS", "仓库", "采购"],
    "formal_systems": ["MES", "CMMS", "QMS", "EHS", "SAP/ERP", "OA", "PMC/APS", "PLM"],
    "channel_boundary": ["企业微信", "飞书", "钉钉", "邮件", "通知", "正式系统", "业务系统", "回填", "回执"],
    "acceptance_and_timing": ["截止", "时限", "验收", "下一次同步", "下一步", "SLA"],
    "authorization_boundary": ["不得", "不能", "授权", "许可", "待复检", "待确认", "未确认"],
}

WRONG_CLOSE_GATE = "闭环" + "门禁"
PROCESS_TRACE_HEADING = "运行" + "轨迹"

FORBIDDEN_PATTERNS = [
    (re.compile(WRONG_CLOSE_GATE), "wrong_close_gate_wording"),
    (re.compile(PROCESS_TRACE_HEADING), "process_trace_section"),
    (re.compile(r"Let me|I need|previous output", re.IGNORECASE), "english_process_talk"),
    (re.compile(r"我已完整读取|我现在输出|根据.*(?:skill|模板|规则)"), "meta_process_talk"),
    (re.compile(r"已经自动同步|已自动同步|自动写入成功|消息已发送|推送成功"), "unsupported_external_action"),
    (re.compile(r"已关闭|系统记录关闭成功|事件关闭成功"), "unsupported_closure"),
    (re.compile(r"已恢复生产|生产已恢复|已恢复全量生产"), "unsupported_recovery"),
    (re.compile(r"已放行|质量已放行|无需复检"), "unsupported_quality_release"),
    (
        re.compile(
            r"(?:个人微信|QQ|微博|Facebook)[^。；\n]{0,20}(?:作为|当作|视为|就是|等同于)[^。；\n]{0,10}正式"
            r"|正式(?:业务)?(?:系统|记录|闭环)[^。；\n]{0,20}(?:个人微信|QQ|微博|Facebook)"
        ),
        "social_channel_as_formal_record",
    ),
    (re.compile(r"无需许可|绕过SOP|绕过 SOP|无需能量隔离|带电开柜"), "unsafe_bypass"),
]


def group_present(text: str, terms: list[str]) -> bool:
    return any(term in text for term in terms)


def forbidden_hits(text: str) -> list[str]:
    hits = []
    for pattern, label in FORBIDDEN_PATTERNS:
        matched = False
        for match in pattern.finditer(text):
            context = text[max(0, match.start() - 24): match.end() + 24]
            protective_context = any(
                guard in context
                for guard in [
                    "不建议",
                    "不要",
                    "不得",
                    "不能",
                    "不可",
                    "禁止",
                    "未",
                    "未经",
                    "直到",
                    "不能算",
                    "不得视为",
                ]
            )
            if label.startswith("unsupported_") and protective_context:
                continue
            matched = True
            break
        if matched:
            hits.append(label)
    return hits


def output_candidates(outputs: Path, model: str, case_id: str, allow_flat: bool) -> list[Path]:
    candidates = [
        outputs / model / f"{case_id}.md",
        outputs / f"{model}_{case_id}.md",
    ]
    if allow_flat:
        candidates.append(outputs / f"{case_id}.md")
    return candidates


def find_output(outputs: Path, model: str, case_id: str, allow_flat: bool) -> Path | None:
    for path in output_candidates(outputs, model, case_id, allow_flat):
        if path.exists():
            return path
    return None


def score_case(case_id: str, text: str, model: str = "") -> dict[str, str | int]:
    case = CASES[case_id]
    group_checks: dict[str, list[str]] = {}
    group_checks.update(COMMON_GROUPS)
    group_checks.update(case["groups"])

    present = [name for name, terms in group_checks.items() if group_present(text, terms)]
    missing = [name for name, terms in group_checks.items() if not group_present(text, terms)]
    hits = forbidden_hits(text)

    common_missing = [name for name in COMMON_GROUPS if name in missing]
    case_missing = [name for name in case["groups"] if name in missing]

    score = 100
    score -= len(common_missing) * 7
    score -= len(case_missing) * 8
    score -= len(hits) * 25
    score = max(0, score)
    passed = score >= 82 and not hits

    return {
        "model": model,
        "case_id": case_id,
        "title": case["title"],
        "score": score,
        "passed": "yes" if passed else "no",
        "present_groups": ";".join(present),
        "missing_groups": ";".join(missing),
        "forbidden_hits": ";".join(hits),
        "output_path": "",
    }


def score_missing(model: str, case_id: str) -> dict[str, str | int]:
    case = CASES[case_id]
    return {
        "model": model,
        "case_id": case_id,
        "title": case["title"],
        "score": 0,
        "passed": "no",
        "present_groups": "",
        "missing_groups": "output_missing",
        "forbidden_hits": "",
        "output_path": "",
    }


def select_models(requested: str | None) -> list[str]:
    if not requested:
        return MODELS
    models = [item.strip() for item in requested.split(",") if item.strip()]
    unknown = [model for model in models if model not in MODELS]
    if unknown:
        raise SystemExit(f"Unknown model(s): {', '.join(unknown)}")
    return models


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--outputs", default=str(DEFAULT_OUTPUTS), help="Directory containing GUI output markdown files")
    parser.add_argument("--report", default=str(DEFAULT_REPORT), help="Output CSV report")
    parser.add_argument("--model", default="", help="Optional comma-separated fixed model filter; allows flat G01.md files for one-model workflows")
    args = parser.parse_args()

    outputs = Path(args.outputs)
    report = Path(args.report)
    models = select_models(args.model or None)
    allow_flat = bool(args.model)

    rows = []
    for model in models:
        for case_id in CASES:
            path = find_output(outputs, model, case_id, allow_flat)
            if path is None:
                rows.append(score_missing(model, case_id))
                continue
            row = score_case(case_id, path.read_text(encoding="utf-8"), model=model)
            row["output_path"] = str(path.relative_to(ROOT) if path.is_relative_to(ROOT) else path)
            rows.append(row)

    report.parent.mkdir(parents=True, exist_ok=True)
    with report.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    passed = sum(1 for row in rows if row["passed"] == "yes")
    avg = sum(int(row["score"]) for row in rows) / len(rows)
    print(f"gui_retest_cells={len(rows)} passed={passed} average_score={avg:.1f} report={report}")


if __name__ == "__main__":
    main()
