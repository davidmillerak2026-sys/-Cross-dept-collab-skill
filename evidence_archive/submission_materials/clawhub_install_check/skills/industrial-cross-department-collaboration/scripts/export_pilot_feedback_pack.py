#!/usr/bin/env python3
"""Export pilot-feedback interview pack and records template."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TESTS = ROOT / "tests"
ROLES = TESTS / "pilot_feedback_roles.json"
DEFAULT_INTERVIEW_OUT = TESTS / "pilot_feedback_interview_pack.md"
DEFAULT_RECORD_OUT = TESTS / "pilot_feedback_records_template.csv"

FIELDNAMES = [
    "feedback_id",
    "role_id",
    "role",
    "case_id",
    "scenario",
    "input_type",
    "before_minutes",
    "after_minutes",
    "time_saved_minutes",
    "missing_fields_before",
    "missing_fields_after",
    "missing_field_reduction",
    "handoff_clarity_score",
    "system_traceability_score",
    "unsafe_claim_count",
    "manual_confirmation_boundary",
    "evidence_file_or_screenshot",
    "consent_to_public",
    "public_quote_redacted",
    "notes",
]


def load_roles() -> list[dict]:
    data = json.loads(ROLES.read_text(encoding="utf-8"))
    roles = data.get("roles", [])
    if len(roles) < 6:
        raise SystemExit(f"expected at least 6 pilot roles, found {len(roles)}")
    return roles


def render_role(role: dict) -> str:
    questions = "\n".join(f"{idx}. {question}" for idx, question in enumerate(role["interview_questions"], start=1))
    cases = " / ".join(role["recommended_cases"])
    focus = " / ".join(role["value_focus"])
    return f"""## {role["role_id"]} {role["role"]}

推荐用例：{cases}

价值关注：{focus}

访谈问题：

{questions}

记录要求：

- 只记录角色和场景，不记录个人姓名、手机号、客户名称、订单号或系统账号。
- 没有实际计时数据时，`before_minutes`、`after_minutes` 和 `time_saved_minutes` 必须留空或标为待验证。
- 没有授权时，`consent_to_public` 填 `no`，公开短评留空或只写匿名脱敏摘要。
"""


def write_interview_pack(roles: list[dict], out: Path) -> None:
    body = [
        "# 试用反馈访谈包",
        "",
        "用途：收集真实、脱敏、可追溯的试用反馈，支撑创新性和应用价值证据。不得伪造用户反馈，不得把估算写成已实现收益。",
        "",
        f"角色数量：{len(roles)}",
        "",
    ]
    body.extend(render_role(role) for role in roles)
    out.write_text("\n".join(body), encoding="utf-8")


def write_record_template(roles: list[dict], out: Path) -> None:
    rows = []
    for role in roles:
        rows.append(
            {
                "feedback_id": f"FB-YYYYMMDD-{role['role_id']}",
                "role_id": role["role_id"],
                "role": role["role"],
                "case_id": "/".join(role["recommended_cases"]),
                "scenario": "",
                "input_type": "",
                "before_minutes": "",
                "after_minutes": "",
                "time_saved_minutes": "",
                "missing_fields_before": "",
                "missing_fields_after": "",
                "missing_field_reduction": "",
                "handoff_clarity_score": "",
                "system_traceability_score": "",
                "unsafe_claim_count": "",
                "manual_confirmation_boundary": "",
                "evidence_file_or_screenshot": "",
                "consent_to_public": "no",
                "public_quote_redacted": "",
                "notes": "template row; fill after real pilot feedback",
            }
        )
    with out.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--interview-out", default=str(DEFAULT_INTERVIEW_OUT), help="Output interview pack")
    parser.add_argument("--record-out", default=str(DEFAULT_RECORD_OUT), help="Output pilot feedback CSV template")
    args = parser.parse_args()

    roles = load_roles()
    interview_out = Path(args.interview_out)
    record_out = Path(args.record_out)
    write_interview_pack(roles, interview_out)
    write_record_template(roles, record_out)
    print(f"wrote_interview={interview_out} wrote_record={record_out} roles={len(roles)}")


if __name__ == "__main__":
    main()
