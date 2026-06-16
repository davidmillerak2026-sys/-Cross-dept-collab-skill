from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "README.md",
    "README.zh-CN.md",
    "SKILL.md",
    "docs/architecture.md",
    "docs/operating_playbook.md",
    "docs/scenario_index.md",
    "examples/01_voice_to_work_order.md",
    "examples/02_quality_issue_to_collaboration.md",
    "examples/03_shift_handover_weekly_report.md",
    "examples/04_complex_agent_workflow.md",
    "examples/05_enterprise_department_flow_10_scenarios.md",
    "templates/department_communication_flow.md",
    "templates/integration_contracts.json",
    "templates/production_cross_department_handoff.md",
    "templates/action_readiness.schema.json",
    "templates/work_order.schema.json",
    "scripts/redact_input.py",
    "tests/project_cases.json",
]

FORBIDDEN_PUBLIC_TERMS = [
    "\u4e13\u5bb6\u699c",
    "\u8bc4\u59d4",
    "\u51a0\u519b",
    "O" + "CAS",
    "Skill" + "Hub",
    "Astron" + "Claw",
    "\u70ed\u5ea6\u699c",
    "\u83b7\u5956",
    "\u5b98\u65b9\u8bc4\u5206",
    "\u6ee1\u5206",
]

REQUIRED_PROJECT_TERMS = [
    "MES",
    "CMMS",
    "QMS",
    "EHS",
    "SAP/ERP",
    "OA",
    "PMC/APS",
    "知识库/SOP",
    "事件关闭后",
]


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        fail(f"{path.relative_to(ROOT)} is not UTF-8: {exc}")


def validate_required_files() -> None:
    for rel in REQUIRED_FILES:
        if not (ROOT / rel).exists():
            fail(f"missing required file: {rel}")


def validate_public_terms() -> None:
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if path.relative_to(ROOT).as_posix() == "scripts/validate_project.py":
            continue
        if path.suffix.lower() not in {".md", ".json", ".py", ".txt", ".csv", ".yml", ".yaml"}:
            continue
        text = read_text(path)
        for term in FORBIDDEN_PUBLIC_TERMS:
            if term in text:
                fail(f"public project file contains contest/judging term {term!r}: {path.relative_to(ROOT)}")


def validate_project_terms() -> None:
    combined = "\n".join(read_text(ROOT / rel) for rel in ["README.md", "SKILL.md", "examples/05_enterprise_department_flow_10_scenarios.md"])
    for term in REQUIRED_PROJECT_TERMS:
        if term not in combined:
            fail(f"missing core project term: {term}")


def validate_scenarios() -> None:
    text = read_text(ROOT / "examples/05_enterprise_department_flow_10_scenarios.md")
    for i in range(1, 11):
        marker = f"## S{i:02d} "
        if marker not in text:
            fail(f"missing enterprise scenario marker: {marker}")


def validate_json() -> None:
    for path in ROOT.rglob("*.json"):
        try:
            json.loads(read_text(path))
        except json.JSONDecodeError as exc:
            fail(f"invalid JSON in {path.relative_to(ROOT)}: {exc}")


def main() -> int:
    validate_required_files()
    validate_public_terms()
    validate_project_terms()
    validate_scenarios()
    validate_json()
    print("PASS: public project package is clean and complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
