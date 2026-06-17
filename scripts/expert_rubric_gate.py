#!/usr/bin/env python3
"""Audit expert-rubric readiness without claiming unproven platform points."""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TESTS = ROOT / "tests"
SCRIPTS = ROOT / "scripts"
EVIDENCE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".pdf", ".md", ".txt"}


@dataclass(frozen=True)
class Dimension:
    key: str
    label: str
    points: int
    official: str
    local_required: tuple[str, ...]
    platform_required: tuple[str, ...]


DIMENSIONS = [
    Dimension(
        key="stability",
        label="运行稳定性与鲁棒性",
        points=30,
        official="可在 AstronClaw 正常部署调用；异常输入不崩溃；响应稳定、无频繁失败",
        local_required=(
            "scripts/validate_package.py",
            "scripts/smoke_test_package.py",
            "scripts/score_run.py",
            "tests/test_cases.json",
            "tests/astronclaw_stability_protocol.md",
            "tests/run_record_template.csv",
            "tests/stability_stress_cases.json",
            "tests/astronclaw_stability_stress_prompt_pack.md",
            "tests/run_record_stability_stress_template.csv",
            "scripts/score_stability_stress.py",
            "scripts/evidence_readiness_report.py",
            "tests/evidence_readiness_report.md",
        ),
        platform_required=("AstronClaw run records",),
    ),
    Dimension(
        key="innovation",
        label="作品创新性和应用价值",
        points=30,
        official="功能创新、体验优化、具备明确商用价值",
        local_required=(
            "references/contest_fit.md",
            "references/capability_playbook.md",
            "examples/04_complex_agent_workflow.md",
            "templates/integration_contracts.json",
            "templates/closed_loop_learning.md",
            "templates/production_cross_department_handoff.md",
            "templates/impact_scoreboard.md",
            "templates/management_escalation_packet.md",
            "templates/pilot_feedback_card.md",
            "references/commercial_value_model.md",
            "templates/enterprise_flow_output_contract.md",
            "tests/pilot_feedback_roles.json",
            "tests/pilot_feedback_interview_pack.md",
            "tests/pilot_feedback_records_template.csv",
            "scripts/score_pilot_feedback.py",
            "tests/evidence_readiness_report.md",
            "tests/platform_submission_evidence_template.json",
            "scripts/champion_acceptance_gate.py",
            "tests/champion_acceptance_report.md",
        ),
        platform_required=("real or near-real feedback",),
    ),
    Dimension(
        key="quality",
        label="结果质量",
        points=20,
        official="输出结果完整、准确，符合任务指令要求",
        local_required=(
            "tests/golden_outputs.md",
            "examples/06_expert_screenshot_outputs.md",
            "templates/evidence_trace.schema.json",
            "templates/diagnosis_matrix.schema.json",
            "templates/field_execution_plan.md",
            "templates/work_order_data_quality.md",
            "tests/enterprise_flow_golden_outputs.md",
        ),
        platform_required=("AstronClaw high-priority output screenshots",),
    ),
    Dimension(
        key="orchestration",
        label="技术设计与场景编排能力",
        points=10,
        official="模型/底座选型合理；支持多插件/多工具协同，易用性",
        local_required=(
            "templates/action_card.schema.json",
            "templates/action_readiness.schema.json",
            "templates/run_trace.schema.json",
            "templates/signal_calibration.schema.json",
            "templates/impact_scoreboard.schema.json",
            "templates/human_decision_packet.md",
            "templates/production_cross_department_handoff.md",
        ),
        platform_required=("AstronClaw action-card run evidence",),
    ),
    Dimension(
        key="engineering",
        label="工程规范与文档完整性",
        points=5,
        official="符合 Skill 开发规范；README 完整；代码结构清晰、注释规范",
        local_required=(
            "SKILL.md",
            "README.md",
            "VERSION.md",
            "submission_manifest.json",
            "tests/rubric_evidence_matrix.csv",
            "scripts/expert_rubric_gate.py",
            "scripts/evidence_readiness_report.py",
            "scripts/champion_acceptance_gate.py",
            "tests/platform_submission_evidence_template.json",
            "tests/champion_acceptance_report.md",
            "tests/evidence_readiness_report.md",
            "scripts/export_prompt_pack.py",
        ),
        platform_required=("upload/approval evidence",),
    ),
    Dimension(
        key="safety",
        label="安全合规指标",
        points=5,
        official="无安全风险、无越权行为、数据处理合规",
        local_required=(
            "templates/redaction_rules.json",
            "templates/adversarial_guardrail.md",
            "scripts/redact_input.py",
            "submission safety cases",
        ),
        platform_required=("AstronClaw T11/T30/T31 screenshots",),
    ),
]


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def rel_exists(rel: str) -> bool:
    if rel == "submission safety cases":
        cases = json.loads((TESTS / "test_cases.json").read_text(encoding="utf-8"))["cases"]
        ids = {case["id"] for case in cases}
        return {"T11", "T30", "T31", "T33", "T35"}.issubset(ids)
    return (ROOT / rel).exists()


def run_script(rel: str) -> tuple[bool, str]:
    result = subprocess.run(
        [sys.executable, str(ROOT / rel)],
        cwd=str(ROOT),
        text=True,
        capture_output=True,
        check=False,
    )
    output = (result.stdout + result.stderr).strip()
    return result.returncode == 0, output


def load_run_records() -> list[dict]:
    path = TESTS / "run_record_template.csv"
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def load_required_screenshot_ids() -> set[str]:
    path = TESTS / "rubric_evidence_matrix.csv"
    with path.open(newline="", encoding="utf-8") as fh:
        return {
            row["case_id"]
            for row in csv.DictReader(fh)
            if row["screenshot_priority"] == "required"
        }


def evidence_reference_exists(reference: str) -> bool:
    ref = reference.strip()
    if not ref:
        return False
    path = Path(ref)
    if not path.is_absolute():
        path = ROOT / ref
    if path.suffix.lower() not in EVIDENCE_EXTENSIONS:
        return False
    return path.exists() and path.is_file()


def astronclaw_status() -> dict:
    rows = load_run_records()
    filled = [row for row in rows if row.get("platform", "").lower() == "astronclaw" and row.get("passed")]
    passed = [row for row in filled if row["passed"].lower() in {"yes", "pass", "passed", "true"}]
    failed = [row for row in filled if row["passed"].lower() in {"no", "fail", "failed", "false"}]
    required_ids = load_required_screenshot_ids()
    screenshot_ids = {
        row["case_id"]
        for row in passed
        if row["case_id"] in required_ids and row.get("output_file_or_screenshot", "").strip()
    }
    evidence_file_ids = {
        row["case_id"]
        for row in passed
        if row["case_id"] in required_ids
        and evidence_reference_exists(row.get("output_file_or_screenshot", ""))
    }
    return {
        "total_rows": len(rows),
        "filled": len(filled),
        "passed": len(passed),
        "failed": len(failed),
        "required_screenshots": len(screenshot_ids),
        "required_screenshot_missing": sorted(required_ids - screenshot_ids),
        "required_evidence_files": len(evidence_file_ids),
        "required_evidence_file_missing": sorted(required_ids - evidence_file_ids),
    }


def local_dimension_status(dimension: Dimension) -> tuple[bool, list[str]]:
    missing = [rel for rel in dimension.local_required if not rel_exists(rel)]
    return not missing, missing


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--require-astronclaw",
        action="store_true",
        help="Fail unless AstronClaw run records and required screenshots are present.",
    )
    parser.add_argument(
        "--skip-subchecks",
        action="store_true",
        help="Skip validate/smoke subprocesses; used by smoke_test_package.py to avoid recursion.",
    )
    args = parser.parse_args()

    if args.skip_subchecks:
        validate_ok, validate_output = True, "SKIPPED"
        smoke_ok, smoke_output = True, "SKIPPED"
    else:
        validate_ok, validate_output = run_script("scripts/validate_package.py")
        smoke_ok, smoke_output = run_script("scripts/smoke_test_package.py")

    rows = []
    local_points = 0
    for dimension in DIMENSIONS:
        ready, missing = local_dimension_status(dimension)
        if ready:
            local_points += dimension.points
        rows.append((dimension, ready, missing))

    print("# Expert Rubric Gate")
    print(f"local_gate_points={local_points}/100")
    print(f"validate_package={'PASS' if validate_ok else 'FAIL'}")
    print(f"smoke_test={'PASS' if smoke_ok else 'FAIL'}")
    print()

    for dimension, ready, missing in rows:
        print(f"## {dimension.label} ({dimension.points})")
        print(f"official={dimension.official}")
        print(f"local_evidence={'ready' if ready else 'missing'}")
        if missing:
            print(f"missing={';'.join(missing)}")
        print(f"platform_evidence_required={';'.join(dimension.platform_required)}")
        print()

    status = astronclaw_status()
    print("## AstronClaw Evidence")
    for key, value in status.items():
        if isinstance(value, list):
            value = ";".join(value)
        print(f"{key}={value}")

    if not validate_ok:
        print(validate_output)
        fail("validate_package.py failed")
    if not smoke_ok:
        print(smoke_output)
        fail("smoke_test_package.py failed")
    if local_points < 100:
        fail("local expert-rubric evidence is incomplete")

    if args.require_astronclaw:
        if status["passed"] < 38:
            fail("AstronClaw full-case run evidence is incomplete")
        if status["failed"] > 0:
            fail("AstronClaw run records contain failures")
        if status["required_screenshot_missing"]:
            fail("AstronClaw required screenshots are incomplete")
        if status["required_evidence_file_missing"]:
            fail("AstronClaw required screenshot/output files are missing on disk")
        print("PASS: expert rubric gate with AstronClaw evidence passed")
    else:
        print("PASS: local expert rubric gate passed")
        print("NOTE: 100 expert points remain unproven until AstronClaw evidence is collected.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
