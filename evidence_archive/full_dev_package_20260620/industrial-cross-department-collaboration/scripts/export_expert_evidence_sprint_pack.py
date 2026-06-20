#!/usr/bin/env python3
"""Export a ranked expert-evidence sprint pack for platform proof collection."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TESTS = ROOT / "tests"
CASES = TESTS / "test_cases.json"
MATRIX = TESTS / "rubric_evidence_matrix.csv"
ENTERPRISE_RECORD = TESTS / "run_record_enterprise_flow_template.csv"
STABILITY_RECORD = TESTS / "run_record_stability_stress_template.csv"
PILOT_ROLES = TESTS / "pilot_feedback_roles.json"
DEFAULT_MD_OUT = TESTS / "expert_evidence_sprint_pack.md"
DEFAULT_CSV_OUT = TESTS / "expert_evidence_sprint_manifest.csv"

PLATFORM_REQUIRED = [
    ("contest_submit_success_screenshot", "赛题提交成功截图"),
    ("skillhub_approval_screenshot", "SkillHub 审核通过截图"),
    ("skillhub_public_page_screenshot", "SkillHub 公开作品页截图"),
    ("skillhub_public_url", "SkillHub 公开作品链接"),
]

PLATFORM_OPTIONAL = [
    ("skillhub_dashboard_status_screenshot", "SkillHub 后台状态截图"),
    ("heat_rank_screenshot", "热度榜截图"),
]

FIRST_WAVE_REQUIRED = ["T01", "T21", "T36", "T37", "T38", "T39", "T11", "T30", "T31"]
HIGH_IMPACT_ENTERPRISE = ["S01", "S05", "S07", "S08", "S10"]
HIGH_RISK_STABILITY = ["ST05", "ST06", "ST07", "ST10", "ST12"]
MIN_PILOT_ROLES = ["R01", "R03", "R05"]


def load_cases() -> dict[str, dict]:
    cases = json.loads(CASES.read_text(encoding="utf-8"))["cases"]
    return {case["id"]: case for case in cases}


def load_required_rows() -> list[dict[str, str]]:
    with MATRIX.open(newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    return [row for row in rows if row["screenshot_priority"] == "required"]


def load_record_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def load_roles() -> list[dict]:
    return json.loads(PILOT_ROLES.read_text(encoding="utf-8"))["roles"]


def screenshot_path(case_id: str, scenario: str) -> str:
    return f"tests/evidence/screenshots/{case_id}_AstronClaw_{scenario}_YYYYMMDD.png"


def run_output_path(case_id: str) -> str:
    return f"tests/run_outputs/{case_id}.md"


def enterprise_output_path(case_id: str) -> str:
    return f"tests/enterprise_flow_outputs/{case_id}.md"


def stability_output_path(case_id: str) -> str:
    return f"tests/stability_stress_outputs/{case_id}.md"


def render_required_case(row: dict[str, str], case: dict) -> str:
    must = ", ".join(case.get("must_contain", [])) or "人工检查要点"
    checks = "\n".join(f"- {item}" for item in case.get("checks", []))
    return (
        f"### {case['id']} {case['title']}\n\n"
        f"- 证据焦点：{row['evidence_focus']}\n"
        f"- 期望输出：{case['expected_output']}\n"
        f"- 建议截图：`{screenshot_path(case['id'], case['scenario'])}`\n"
        f"- 建议文本输出：`{run_output_path(case['id'])}`\n"
        f"- 运行记录：`tests/run_record_template.csv`\n"
        f"- 关键必须出现：{must}\n"
        f"- 人工检查：\n{checks}\n"
    )


def render_record_block(rows: list[dict[str, str]], title_lookup: dict[str, str], output_func) -> str:
    lines = []
    for row in rows:
        case_id = row["case_id"]
        lines.append(
            f"- `{case_id}` {title_lookup[case_id]} -> 输出保存 `{output_func(case_id)}`；运行记录填 `tests/{row['case_id']}` 对应行。"
        )
    return "\n".join(lines)


def build_manifest_rows() -> list[dict[str, str]]:
    cases = load_cases()
    required_rows = load_required_rows()
    enterprise_rows = load_record_rows(ENTERPRISE_RECORD)
    stability_rows = load_record_rows(STABILITY_RECORD)
    roles = load_roles()

    required_map = {row["case_id"]: row for row in required_rows}
    remaining_required = [row for row in required_rows if row["case_id"] not in FIRST_WAVE_REQUIRED]
    enterprise_titles = {row["case_id"]: row["notes"] for row in enterprise_rows}
    stability_titles = {row["case_id"]: row["notes"] for row in stability_rows}

    rows: list[dict[str, str]] = []
    for key, title in PLATFORM_REQUIRED:
        primary_artifact = f"tests/evidence/screenshots/{key}_YYYYMMDD.png"
        if key == "skillhub_public_url":
            primary_artifact = "https://skill.xfyun.cn/..."
        rows.append(
            {
                "phase": "0",
                "track": "platform_submission",
                "item_id": key,
                "title": title,
                "priority": "required",
                "record_file": "tests/platform_submission_evidence_template.json",
                "suggested_primary_artifact": primary_artifact,
                "suggested_secondary_artifact": "",
                "scoring_command": "python scripts/champion_acceptance_gate.py",
                "notes": "提交或审核完成后立刻补路径。" if key != "skillhub_public_url" else "审核通过并公开后立刻补真实链接。",
            }
        )
    for key, title in PLATFORM_OPTIONAL:
        rows.append(
            {
                "phase": "0",
                "track": "platform_submission",
                "item_id": key,
                "title": title,
                "priority": "optional",
                "record_file": "tests/platform_submission_evidence_template.json",
                "suggested_primary_artifact": f"tests/evidence/screenshots/{key}_YYYYMMDD.png",
                "suggested_secondary_artifact": "",
                "scoring_command": "python scripts/champion_acceptance_gate.py",
                "notes": "可选，但有助于后续热榜与后台状态追踪。",
            }
        )

    for case_id in FIRST_WAVE_REQUIRED:
        case = cases[case_id]
        row = required_map[case_id]
        rows.append(
            {
                "phase": "1",
                "track": "required_cases",
                "item_id": case_id,
                "title": case["title"],
                "priority": "required",
                "record_file": "tests/run_record_template.csv",
                "suggested_primary_artifact": screenshot_path(case_id, case["scenario"]),
                "suggested_secondary_artifact": run_output_path(case_id),
                "scoring_command": "python scripts/score_run.py --outputs tests/run_outputs --report tests/run_score_report.csv",
                "notes": row["evidence_focus"],
            }
        )

    for row in remaining_required:
        case = cases[row["case_id"]]
        rows.append(
            {
                "phase": "2",
                "track": "required_cases",
                "item_id": case["id"],
                "title": case["title"],
                "priority": "required",
                "record_file": "tests/run_record_template.csv",
                "suggested_primary_artifact": screenshot_path(case["id"], case["scenario"]),
                "suggested_secondary_artifact": run_output_path(case["id"]),
                "scoring_command": "python scripts/score_run.py --outputs tests/run_outputs --report tests/run_score_report.csv",
                "notes": row["evidence_focus"],
            }
        )

    for row in enterprise_rows:
        phase = "3" if row["case_id"] in HIGH_IMPACT_ENTERPRISE else "4"
        priority = "enterprise_first_wave" if row["case_id"] in HIGH_IMPACT_ENTERPRISE else "enterprise_full"
        rows.append(
            {
                "phase": phase,
                "track": "enterprise_flow",
                "item_id": row["case_id"],
                "title": enterprise_titles[row["case_id"]],
                "priority": priority,
                "record_file": "tests/run_record_enterprise_flow_template.csv",
                "suggested_primary_artifact": screenshot_path(row["case_id"], "enterprise_flow"),
                "suggested_secondary_artifact": enterprise_output_path(row["case_id"]),
                "scoring_command": "python scripts/score_enterprise_flow.py --outputs tests/enterprise_flow_outputs --report tests/enterprise_flow_score_report.csv",
                "notes": "高影响场景优先补管理升级与影响评分板证据。" if phase == "3" else "企业部门协同补齐全套场景。",
            }
        )

    for row in stability_rows:
        phase = "5" if row["case_id"] in HIGH_RISK_STABILITY else "6"
        priority = "stability_first_wave" if row["case_id"] in HIGH_RISK_STABILITY else "stability_full"
        rows.append(
            {
                "phase": phase,
                "track": "stability_stress",
                "item_id": row["case_id"],
                "title": stability_titles[row["case_id"]],
                "priority": priority,
                "record_file": "tests/run_record_stability_stress_template.csv",
                "suggested_primary_artifact": screenshot_path(row["case_id"], "stability"),
                "suggested_secondary_artifact": stability_output_path(row["case_id"]),
                "scoring_command": "python scripts/score_stability_stress.py --outputs tests/stability_stress_outputs --report tests/stability_stress_score_report.csv",
                "notes": "优先证明不崩溃、不越权、不伪造完成。" if phase == "5" else "补齐异常输入全覆盖。",
            }
        )

    role_map = {role["role_id"]: role for role in roles}
    for role_id in MIN_PILOT_ROLES:
        role = role_map[role_id]
        rows.append(
            {
                "phase": "7",
                "track": "pilot_feedback",
                "item_id": role_id,
                "title": role["role"],
                "priority": "pilot_minimum",
                "record_file": "tests/pilot_feedback_records_template.csv",
                "suggested_primary_artifact": f"tests/evidence/outputs/{role_id}_pilot_feedback_YYYYMMDD.md",
                "suggested_secondary_artifact": ",".join(role["recommended_cases"][:3]),
                "scoring_command": "python scripts/score_pilot_feedback.py --input tests/pilot_feedback_records_template.csv --report tests/pilot_feedback_score_report.csv",
                "notes": "建议先拿到至少 3 份真实脱敏反馈，满足冠军验收最低门槛。",
            }
        )

    for role in roles:
        if role["role_id"] in MIN_PILOT_ROLES:
            continue
        rows.append(
            {
                "phase": "8",
                "track": "pilot_feedback",
                "item_id": role["role_id"],
                "title": role["role"],
                "priority": "pilot_expansion",
                "record_file": "tests/pilot_feedback_records_template.csv",
                "suggested_primary_artifact": f"tests/evidence/outputs/{role['role_id']}_pilot_feedback_YYYYMMDD.md",
                "suggested_secondary_artifact": ",".join(role["recommended_cases"][:3]),
                "scoring_command": "python scripts/score_pilot_feedback.py --input tests/pilot_feedback_records_template.csv --report tests/pilot_feedback_score_report.csv",
                "notes": "扩充业务价值与生态落地证据。",
            }
        )

    return rows


def write_manifest(rows: list[dict[str, str]], out: Path) -> None:
    fieldnames = [
        "phase",
        "track",
        "item_id",
        "title",
        "priority",
        "record_file",
        "suggested_primary_artifact",
        "suggested_secondary_artifact",
        "scoring_command",
        "notes",
    ]
    with out.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(rows: list[dict[str, str]], out: Path) -> None:
    cases = load_cases()
    required_rows = load_required_rows()
    required_map = {row["case_id"]: row for row in required_rows}
    enterprise_rows = load_record_rows(ENTERPRISE_RECORD)
    stability_rows = load_record_rows(STABILITY_RECORD)
    roles = load_roles()
    enterprise_titles = {row["case_id"]: row["notes"] for row in enterprise_rows}
    stability_titles = {row["case_id"]: row["notes"] for row in stability_rows}
    role_map = {role["role_id"]: role for role in roles}

    remaining_required = [row for row in required_rows if row["case_id"] not in FIRST_WAVE_REQUIRED]
    first_wave_blocks = "\n".join(
        render_required_case(required_map[case_id], cases[case_id]) for case_id in FIRST_WAVE_REQUIRED
    )
    remaining_blocks = "\n".join(
        render_required_case(row, cases[row["case_id"]]) for row in remaining_required
    )

    enterprise_first = [
        f"- `{row['case_id']}` {enterprise_titles[row['case_id']]} -> 截图 `{screenshot_path(row['case_id'], 'enterprise_flow')}`；输出 `{enterprise_output_path(row['case_id'])}`"
        for row in enterprise_rows
        if row["case_id"] in HIGH_IMPACT_ENTERPRISE
    ]
    enterprise_rest = [
        f"- `{row['case_id']}` {enterprise_titles[row['case_id']]} -> 截图 `{screenshot_path(row['case_id'], 'enterprise_flow')}`；输出 `{enterprise_output_path(row['case_id'])}`"
        for row in enterprise_rows
        if row["case_id"] not in HIGH_IMPACT_ENTERPRISE
    ]
    stability_first = [
        f"- `{row['case_id']}` {stability_titles[row['case_id']]} -> 截图 `{screenshot_path(row['case_id'], 'stability')}`；输出 `{stability_output_path(row['case_id'])}`"
        for row in stability_rows
        if row["case_id"] in HIGH_RISK_STABILITY
    ]
    stability_rest = [
        f"- `{row['case_id']}` {stability_titles[row['case_id']]} -> 截图 `{screenshot_path(row['case_id'], 'stability')}`；输出 `{stability_output_path(row['case_id'])}`"
        for row in stability_rows
        if row["case_id"] not in HIGH_RISK_STABILITY
    ]

    minimum_roles = "\n".join(
        f"- `{role_id}` {role_map[role_id]['role']}：优先跑 {', '.join(role_map[role_id]['recommended_cases'][:3])}；关注 {', '.join(role_map[role_id]['value_focus'])}"
        for role_id in MIN_PILOT_ROLES
    )
    expansion_roles = "\n".join(
        f"- `{role['role_id']}` {role['role']}：补强 {', '.join(role['recommended_cases'][:3])}"
        for role in roles
        if role["role_id"] not in MIN_PILOT_ROLES
    )

    body = [
        "# Expert Evidence Sprint Pack",
        "",
        "用途：把平台提交、专家榜必截图、企业部门协同、稳定性压力和真实试用反馈放进一个可执行的冲刺顺序里，减少实测时漏截图、漏记录、漏评分。",
        "",
        "总控清单 CSV：`tests/expert_evidence_sprint_manifest.csv`",
        "",
        "建议节奏：每完成一个阶段，就刷新对应评分脚本和 `scripts/champion_acceptance_gate.py`，避免最后集中返工。",
        "",
        "## Phase 0 Platform Unlock",
        "",
        "- `contest_submit_success_screenshot` -> `tests/evidence/screenshots/contest_submit_success_screenshot_YYYYMMDD.png`",
        "- `skillhub_approval_screenshot` -> `tests/evidence/screenshots/skillhub_approval_screenshot_YYYYMMDD.png`",
        "- `skillhub_public_page_screenshot` -> `tests/evidence/screenshots/skillhub_public_page_screenshot_YYYYMMDD.png`",
        "- `skillhub_public_url` -> SkillHub 公开作品真实链接",
        "- 可选：`skillhub_dashboard_status_screenshot`、`heat_rank_screenshot`",
        "- 更新文件：`tests/platform_submission_evidence_template.json`",
        "",
        "## Phase 1 First-Wave Required Screenshots",
        "",
        "先跑最能代表价值、最容易拉开差距的 9 个 required 用例：T01、T21、T36、T37、T38、T39、T11、T30、T31。",
        "",
        first_wave_blocks,
        "",
        "阶段完成后建议运行：",
        "",
        "```bash",
        "python scripts/score_run.py --outputs tests/run_outputs --report tests/run_score_report.csv",
        "```",
        "",
        "## Phase 2 Remaining Required Screenshots",
        "",
        remaining_blocks,
        "",
        "## Phase 3 High-Impact Enterprise Flow",
        "",
        "这些场景最适合证明跨部门协同、管理升级和落地价值：",
        "",
        *enterprise_first,
        "",
        "阶段完成后建议运行：",
        "",
        "```bash",
        "python scripts/score_enterprise_flow.py --outputs tests/enterprise_flow_outputs --report tests/enterprise_flow_score_report.csv",
        "```",
        "",
        "## Phase 4 Remaining Enterprise Flow",
        "",
        *enterprise_rest,
        "",
        "## Phase 5 High-Risk Stability Stress",
        "",
        "优先证明不崩溃、不越权、不伪造完成：",
        "",
        *stability_first,
        "",
        "阶段完成后建议运行：",
        "",
        "```bash",
        "python scripts/score_stability_stress.py --outputs tests/stability_stress_outputs --report tests/stability_stress_score_report.csv",
        "```",
        "",
        "## Phase 6 Remaining Stability Stress",
        "",
        *stability_rest,
        "",
        "## Phase 7 Pilot Feedback Minimum Gate",
        "",
        "冠军验收最低门槛至少要 3 份真实脱敏反馈，建议先拿：",
        "",
        minimum_roles,
        "",
        "阶段完成后建议运行：",
        "",
        "```bash",
        "python scripts/score_pilot_feedback.py --input tests/pilot_feedback_records_template.csv --report tests/pilot_feedback_score_report.csv",
        "```",
        "",
        "## Phase 8 Pilot Feedback Expansion",
        "",
        expansion_roles,
        "",
        "## Final Gate",
        "",
        "所有阶段完成后依次运行：",
        "",
        "```bash",
        "python scripts/expert_rubric_gate.py --require-astronclaw",
        "python scripts/champion_acceptance_gate.py",
        "```",
        "",
    ]
    out.write_text("\n".join(body), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--md-out", default=str(DEFAULT_MD_OUT), help="Output markdown sprint pack")
    parser.add_argument("--csv-out", default=str(DEFAULT_CSV_OUT), help="Output CSV sprint manifest")
    args = parser.parse_args()

    rows = build_manifest_rows()
    md_out = Path(args.md_out)
    csv_out = Path(args.csv_out)
    write_markdown(rows, md_out)
    write_manifest(rows, csv_out)
    print(f"wrote_md={md_out} wrote_csv={csv_out} rows={len(rows)}")


if __name__ == "__main__":
    main()
