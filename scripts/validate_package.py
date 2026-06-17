#!/usr/bin/env python3
"""Validate the industrial-workorder-collaboration Skill package.

This script is intentionally self-contained so reviewers or maintainers can
repeat the same quality gate before upload.
"""

from __future__ import annotations

import json
import os
import re
import sys
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_NAME = "industrial-workorder-collaboration"
MAX_TOTAL_BYTES = 100 * 1024 * 1024
MAX_FILE_BYTES = 10 * 1024 * 1024
MAX_FILE_COUNT = 500

ALLOWED_EXTENSIONS = {
    ".md",
    ".txt",
    ".json",
    ".yaml",
    ".yml",
    ".html",
    ".css",
    ".csv",
    ".pdf",
    ".toml",
    ".xml",
    ".xsd",
    ".xsl",
    ".dtd",
    ".ini",
    ".cfg",
    ".env",
    ".js",
    ".cjs",
    ".mjs",
    ".ts",
    ".py",
    ".sh",
    ".rb",
    ".go",
    ".rs",
    ".java",
    ".kt",
    ".lua",
    ".sql",
    ".r",
    ".bat",
    ".ps1",
    ".zsh",
    ".bash",
    ".png",
    ".jpg",
    ".jpeg",
    ".svg",
    ".gif",
    ".webp",
    ".ico",
    ".doc",
    ".xls",
    ".ppt",
    ".docx",
    ".xlsx",
    ".pptx",
}

FORBIDDEN_EXTENSIONS = {
    ".zip",
    ".tar",
    ".gz",
    ".7z",
    ".rar",
    ".exe",
    ".dll",
    ".so",
    ".dylib",
    ".bin",
    ".mp4",
    ".mp3",
    ".wav",
    ".avi",
    ".sqlite",
    ".db",
    ".bak",
    ".tmp",
    ".swp",
}

SECRET_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"AKIA[A-Z0-9]{16}"),
    re.compile(r"ghp_[A-Za-z0-9_]{20,}"),
    re.compile(
        r"(api_key|access_key|secret|password|token)\s*[:=]\s*[\"']?[^\s\"']{12,}",
        re.IGNORECASE,
    ),
]

REQUIRED_SKILL_PHRASES = [
    "场景路由",
    "事实分层",
    "异常输入处理",
    "异常输入压力测试",
    "输出质量门禁",
    "工具/插件协同契约",
    "动作准备度门禁",
    "证据链与可追溯输出",
    "候选诊断矩阵",
    "多角色任务分解",
    "运行轨迹",
    "信号校准门禁",
    "降级完成",
    "冠军自评卡",
    "提示注入防护",
    "闭环学习",
    "现场执行编排",
    "工单数据质量门禁",
    "试用反馈",
    "商业价值",
    "统一事件包",
    "企业部门协同专项",
    "生产部",
    "PMC",
    "工程",
    "知识库/SOP",
    "事件关闭后",
    "可复制同步消息",
    "不提供绕过联锁",
    "拒绝替代授权判断",
]

REQUIRED_FILES = [
    "VERSION.md",
    "submission_manifest.json",
    "examples/00_judge_quick_run.md",
    "examples/06_expert_screenshot_outputs.md",
    "examples/07_enterprise_department_flow_10_scenarios.md",
    "examples/08_sku_quality_coordination_run.md",
    "examples/data/sku_quality_coordination_sample.csv",
    "tests/golden_outputs.md",
    "tests/enterprise_flow_golden_outputs.md",
    "scripts/score_run.py",
    "scripts/score_enterprise_flow.py",
    "scripts/redact_input.py",
    "scripts/export_prompt_pack.py",
    "scripts/export_required_evidence_pack.py",
    "scripts/export_required_run_record.py",
    "scripts/export_enterprise_flow_pack.py",
    "scripts/export_stability_stress_pack.py",
    "scripts/export_pilot_feedback_pack.py",
    "scripts/export_expert_evidence_sprint_pack.py",
    "scripts/evidence_sprint_status.py",
    "scripts/champion_acceptance_gate.py",
    "scripts/smoke_test_package.py",
    "scripts/score_stability_stress.py",
    "scripts/score_pilot_feedback.py",
    "scripts/evidence_readiness_report.py",
    "scripts/expert_rubric_gate.py",
    "tests/run_record_template.csv",
    "tests/run_record_required_template.csv",
    "tests/evidence/README.md",
    "tests/run_outputs/README.md",
    "tests/enterprise_flow_outputs/README.md",
    "tests/skillhub_prompt_pack.md",
    "tests/astronclaw_required_prompt_pack.md",
    "tests/astronclaw_enterprise_flow_prompt_pack.md",
    "tests/expert_evidence_sprint_pack.md",
    "tests/expert_evidence_sprint_manifest.csv",
    "tests/expert_evidence_sprint_status.md",
    "tests/rubric_evidence_matrix.csv",
    "tests/astronclaw_stability_protocol.md",
    "tests/stability_stress_cases.json",
    "tests/astronclaw_stability_stress_prompt_pack.md",
    "tests/run_record_enterprise_flow_template.csv",
    "tests/run_record_stability_stress_template.csv",
    "tests/stability_stress_outputs/README.md",
    "tests/pilot_feedback_roles.json",
    "tests/pilot_feedback_interview_pack.md",
    "tests/pilot_feedback_records_template.csv",
    "tests/platform_submission_evidence_template.json",
    "tests/champion_acceptance_report.md",
    "tests/evidence_readiness_report.md",
    "templates/integration_contracts.json",
    "templates/redaction_rules.json",
    "templates/action_readiness.schema.json",
    "templates/closed_loop_learning.md",
    "templates/evidence_trace.schema.json",
    "templates/diagnosis_matrix.schema.json",
    "templates/human_decision_packet.md",
    "templates/run_trace.schema.json",
    "templates/role_handoff.md",
    "templates/production_cross_department_handoff.md",
    "templates/department_communication_flow.md",
    "templates/enterprise_flow_output_contract.md",
    "templates/impact_scoreboard.md",
    "templates/impact_scoreboard.schema.json",
    "templates/management_escalation_packet.md",
    "templates/pilot_feedback_card.md",
    "templates/output_modes.md",
    "templates/signal_calibration.schema.json",
    "templates/degraded_completion.md",
    "templates/champion_self_review.schema.json",
    "templates/adversarial_guardrail.md",
    "templates/field_execution_plan.md",
    "templates/work_order_data_quality.md",
    "references/full_score_strategy.md",
    "references/expert_review_playbook.md",
    "references/capability_playbook.md",
    "references/commercial_value_model.md",
    "references/rubric_evidence_matrix.md",
    "references/expert_rubric_gate.md",
]

RUBRIC_COLUMNS = {
    "case_id",
    "scenario",
    "stability_robustness",
    "innovation_value",
    "result_quality",
    "technical_orchestration",
    "engineering_docs",
    "safety_compliance",
    "evidence_focus",
    "screenshot_priority",
}


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    sys.exit(1)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        fail(f"{path} is not valid UTF-8: {exc}")


def list_files() -> list[Path]:
    files = [
        p
        for p in ROOT.rglob("*")
        if p.is_file() and ".git" not in p.relative_to(ROOT).parts
    ]
    if not files:
        fail("no files found")
    return files


def validate_frontmatter() -> None:
    skill = ROOT / "SKILL.md"
    if not skill.exists():
        fail("SKILL.md missing")
    text = read_text(skill)
    match = re.match(r"^---\n(?P<yaml>.*?)\n---\n", text, re.DOTALL)
    if not match:
        fail("SKILL.md frontmatter missing")
    yaml = match.group("yaml")
    if f"name: {SKILL_NAME}" not in yaml:
        fail("SKILL.md name mismatch")
    if "description:" not in yaml:
        fail("SKILL.md description missing")
    for phrase in REQUIRED_SKILL_PHRASES:
        if phrase not in text:
            fail(f"SKILL.md missing champion phrase: {phrase}")


def validate_required_files() -> None:
    for rel in REQUIRED_FILES:
        if not (ROOT / rel).exists():
            fail(f"required evidence file missing: {rel}")


def validate_files(files: list[Path]) -> None:
    total = 0
    for path in files:
        rel = path.relative_to(ROOT)
        if any(part in {"__MACOSX", ".git"} for part in rel.parts):
            fail(f"forbidden metadata path: {rel}")
        if ".." in rel.parts:
            fail(f"path traversal found: {rel}")
        if re.match(r"^[A-Za-z]:", str(rel)):
            fail(f"windows drive path found: {rel}")
        ext = path.suffix.lower()
        if ext in FORBIDDEN_EXTENSIONS:
            fail(f"forbidden file extension {ext}: {rel}")
        if ext and ext not in ALLOWED_EXTENSIONS:
            fail(f"unsupported file extension {ext}: {rel}")
        size = path.stat().st_size
        if size > MAX_FILE_BYTES:
            fail(f"file too large: {rel} ({size} bytes)")
        total += size
    if len(files) > MAX_FILE_COUNT:
        fail(f"too many files: {len(files)}")
    if total > MAX_TOTAL_BYTES:
        fail(f"package too large: {total} bytes")


def validate_json(files: list[Path]) -> None:
    for path in files:
        if path.suffix.lower() == ".json":
            try:
                json.loads(read_text(path))
            except json.JSONDecodeError as exc:
                fail(f"invalid JSON {path.relative_to(ROOT)}: {exc}")


def validate_test_cases() -> None:
    path = ROOT / "tests" / "test_cases.json"
    if not path.exists():
        fail("tests/test_cases.json missing")
    data = json.loads(read_text(path))
    cases = data.get("cases")
    if not isinstance(cases, list) or len(cases) < 38:
        fail("at least 38 test cases required")
    scenarios = {case.get("scenario") for case in cases}
    required = {"maintenance", "quality", "safety", "changeover", "meeting", "handover", "procurement", "pmc", "engineering", "production_orchestration"}
    missing = required - scenarios
    if missing:
        fail(f"test cases missing scenarios: {sorted(missing)}")
    for case in cases:
        for field in ("id", "scenario", "title", "input", "expected_output", "checks"):
            if not case.get(field):
                fail(f"test case {case.get('id', '<unknown>')} missing {field}")
        if len(case["checks"]) < 3:
            fail(f"test case {case['id']} has too few checks")
        for pattern in case.get("must_not_contain_regex", []):
            try:
                re.compile(pattern)
            except re.error as exc:
                fail(f"test case {case['id']} invalid forbidden regex {pattern}: {exc}")


def validate_rubric_matrix() -> None:
    cases_path = ROOT / "tests" / "test_cases.json"
    matrix_path = ROOT / "tests" / "rubric_evidence_matrix.csv"
    cases = json.loads(read_text(cases_path))["cases"]
    expected_ids = {case["id"] for case in cases}
    rows = []
    import csv

    with matrix_path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        if set(reader.fieldnames or []) != RUBRIC_COLUMNS:
            fail("rubric_evidence_matrix.csv has unexpected columns")
        rows = list(reader)
    row_ids = {row["case_id"] for row in rows}
    if row_ids != expected_ids:
        fail("rubric_evidence_matrix.csv case coverage does not match tests/test_cases.json")
    required_priority = [row for row in rows if row["screenshot_priority"] == "required"]
    if len(required_priority) < 10:
        fail("rubric_evidence_matrix.csv needs at least 10 required screenshot cases")
    rubric_fields = [
        "stability_robustness",
        "innovation_value",
        "result_quality",
        "technical_orchestration",
        "engineering_docs",
        "safety_compliance",
    ]
    for field in rubric_fields:
        hits = [row for row in rows if row[field] == "yes"]
        if len(hits) < 10:
            fail(f"rubric evidence too thin for {field}")
    for row in rows:
        if row["screenshot_priority"] not in {"required", "optional"}:
            fail(f"invalid screenshot priority for {row['case_id']}")
        if not row["evidence_focus"].strip():
            fail(f"rubric evidence focus missing for {row['case_id']}")


def validate_required_screenshot_examples() -> None:
    import csv

    matrix_path = ROOT / "tests" / "rubric_evidence_matrix.csv"
    examples_path = ROOT / "examples" / "06_expert_screenshot_outputs.md"
    examples = read_text(examples_path)
    with matrix_path.open(newline="", encoding="utf-8") as fh:
        required_ids = [
            row["case_id"]
            for row in csv.DictReader(fh)
            if row["screenshot_priority"] == "required"
        ]
    missing = []
    for case_id in required_ids:
        if not re.search(rf"^## {re.escape(case_id)}\b", examples, re.MULTILINE):
            missing.append(case_id)
    if missing:
        fail(f"examples/06_expert_screenshot_outputs.md missing required screenshot cases: {missing}")


def validate_required_prompt_pack() -> None:
    import csv

    matrix_path = ROOT / "tests" / "rubric_evidence_matrix.csv"
    pack_path = ROOT / "tests" / "astronclaw_required_prompt_pack.md"
    pack = read_text(pack_path)
    with matrix_path.open(newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    required_ids = [row["case_id"] for row in rows if row["screenshot_priority"] == "required"]
    optional_ids = [row["case_id"] for row in rows if row["screenshot_priority"] == "optional"]
    if f"必截图用例数量：{len(required_ids)}" not in pack:
        fail("astronclaw_required_prompt_pack.md required case count mismatch")
    missing = []
    for case_id in required_ids:
        if not re.search(rf"^## {re.escape(case_id)}\b", pack, re.MULTILINE):
            missing.append(case_id)
    if missing:
        fail(f"astronclaw_required_prompt_pack.md missing required cases: {missing}")
    leaked_optional = []
    for case_id in optional_ids:
        if re.search(rf"^## {re.escape(case_id)}\b", pack, re.MULTILINE):
            leaked_optional.append(case_id)
    if leaked_optional:
        fail(f"astronclaw_required_prompt_pack.md includes optional cases: {leaked_optional}")


def validate_run_record_template() -> None:
    path = ROOT / "tests" / "run_record_template.csv"
    required_columns = {
        "case_id",
        "scenario",
        "priority_for_screenshot",
        "run_date",
        "runner",
        "platform",
        "attempt",
        "latency_seconds",
        "passed",
        "score",
        "error_type",
        "retry_needed",
        "output_file_or_screenshot",
        "notes",
    }
    import csv

    with path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        if set(reader.fieldnames or []) != required_columns:
            fail("run_record_template.csv has unexpected columns")
        rows = list(reader)
    cases = json.loads(read_text(ROOT / "tests" / "test_cases.json"))["cases"]
    if {row["case_id"] for row in rows} != {case["id"] for case in cases}:
        fail("run_record_template.csv case coverage does not match tests/test_cases.json")
    for row in rows:
        if row["platform"]:
            continue
        if row["attempt"] != "1":
            fail(f"run record default attempt must be 1 for {row['case_id']}")


def validate_required_run_record_template() -> None:
    import csv

    full_path = ROOT / "tests" / "run_record_template.csv"
    required_path = ROOT / "tests" / "run_record_required_template.csv"
    matrix_path = ROOT / "tests" / "rubric_evidence_matrix.csv"
    with matrix_path.open(newline="", encoding="utf-8") as fh:
        required_ids = {
            row["case_id"]
            for row in csv.DictReader(fh)
            if row["screenshot_priority"] == "required"
        }
    with full_path.open(newline="", encoding="utf-8") as fh:
        full_reader = csv.DictReader(fh)
        full_columns = full_reader.fieldnames or []
    with required_path.open(newline="", encoding="utf-8") as fh:
        required_reader = csv.DictReader(fh)
        if (required_reader.fieldnames or []) != full_columns:
            fail("run_record_required_template.csv columns do not match run_record_template.csv")
        rows = list(required_reader)
    row_ids = {row["case_id"] for row in rows}
    if row_ids != required_ids:
        fail("run_record_required_template.csv does not match required screenshot cases")
    for row in rows:
        if row["priority_for_screenshot"] != "required":
            fail(f"required run record row is not marked required: {row['case_id']}")


def validate_submission_manifest() -> None:
    import csv

    manifest = json.loads(read_text(ROOT / "submission_manifest.json"))
    if manifest.get("skill_name") != SKILL_NAME:
        fail("submission_manifest.json skill_name mismatch")
    if manifest.get("entrypoint") != "SKILL.md":
        fail("submission_manifest.json entrypoint must be SKILL.md")
    if manifest.get("readme") != "README.md":
        fail("submission_manifest.json readme must be README.md")
    if not (ROOT / manifest.get("version_file", "")).exists():
        fail("submission_manifest.json version_file missing")

    cases = json.loads(read_text(ROOT / "tests" / "test_cases.json"))["cases"]
    if manifest.get("test_case_count") != len(cases):
        fail("submission_manifest.json test_case_count mismatch")

    with (ROOT / "tests" / "rubric_evidence_matrix.csv").open(newline="", encoding="utf-8") as fh:
        required_ids = [
            row["case_id"]
            for row in csv.DictReader(fh)
            if row["screenshot_priority"] == "required"
        ]
    if manifest.get("required_screenshot_count") != len(required_ids):
        fail("submission_manifest.json required_screenshot_count mismatch")
    if manifest.get("required_screenshot_case_ids") != required_ids:
        fail("submission_manifest.json required_screenshot_case_ids mismatch")

    for rel in manifest.get("local_evidence_assets", []):
        if not (ROOT / rel).exists():
            fail(f"submission_manifest.json local evidence missing: {rel}")
    boundary = manifest.get("claims_boundary", "")
    if "Do not claim" not in boundary or "AstronClaw" not in boundary:
        fail("submission_manifest.json claims boundary is too weak")


def validate_secret_scan(files: list[Path]) -> None:
    text_exts = {".md", ".txt", ".json", ".yaml", ".yml", ".py", ".js", ".env", ".csv"}
    for path in files:
        if path.suffix.lower() not in text_exts:
            continue
        text = read_text(path)
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                fail(f"possible secret found in {path.relative_to(ROOT)}")


def validate_zip(zip_path: Path) -> None:
    if not zip_path.exists():
        return
    with zipfile.ZipFile(zip_path) as archive:
        names = archive.namelist()
        required = f"{SKILL_NAME}/SKILL.md"
        if required not in names:
            fail(f"zip missing {required}")
        zip_files = {n for n in names if not n.endswith("/")}
        if len(zip_files) > MAX_FILE_COUNT:
            fail("zip has too many files")
        expected_files = {
            f"{SKILL_NAME}/{p.relative_to(ROOT).as_posix()}"
            for p in ROOT.rglob("*")
            if p.is_file()
        }
        missing = expected_files - zip_files
        extra = zip_files - expected_files
        if missing:
            fail(f"zip is stale; missing files: {sorted(missing)[:5]}")
        if extra:
            fail(f"zip has files not present in package root: {sorted(extra)[:5]}")


def main() -> None:
    files = list_files()
    validate_frontmatter()
    validate_required_files()
    validate_files(files)
    validate_json(files)
    validate_test_cases()
    validate_rubric_matrix()
    validate_required_screenshot_examples()
    validate_required_prompt_pack()
    validate_run_record_template()
    validate_required_run_record_template()
    validate_submission_manifest()
    validate_secret_scan(files)
    validate_zip(ROOT.parent / f"{SKILL_NAME}.zip")
    print("PASS: Skill package quality gate passed")
    print(f"files={len(files)} total_bytes={sum(p.stat().st_size for p in files)} root={ROOT}")


if __name__ == "__main__":
    main()
