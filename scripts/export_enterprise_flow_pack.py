#!/usr/bin/env python3
"""Export copy-ready AstronClaw prompts for the 10 enterprise-flow scenarios."""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TESTS = ROOT / "tests"
SCENARIOS = ROOT / "examples" / "07_enterprise_department_flow_10_scenarios.md"
DEFAULT_PROMPT_OUT = TESTS / "astronclaw_enterprise_flow_prompt_pack.md"
DEFAULT_RECORD_OUT = TESTS / "run_record_enterprise_flow_template.csv"

FIELDNAMES = [
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
]

IMPACT_SCENARIOS = {
    "S01": "7. 因为这里同时涉及停线、质量隔离和交付风险，额外输出影响评分板和管理升级决策包，写清停线/少产、交付风险、阻塞关闭原因数、决策截止时间和若不决策的后果。",
    "S05": "7. 因为这里同时涉及待料、交付风险和替代料/成本影响，额外输出影响评分板和管理升级决策包，写清待料时长、少产、交付风险、成本影响、决策截止时间和若不决策的后果。",
    "S06": "7. 因为这里同时涉及安全、生产和交付影响，额外输出影响评分板和管理升级决策包，写清隔离范围、停线时长、交付风险、阻塞关闭原因数、决策截止时间和若不决策的后果。",
    "S07": "7. 因为这里同时涉及重复停机、备件/成本和交付风险，额外输出影响评分板和管理升级决策包，写清累计停线、备件 ETA、交付风险、成本影响、决策截止时间和若不决策的后果。",
    "S08": "7. 因为这里同时涉及质量、返工/客户影响和交付风险，额外输出影响评分板和管理升级决策包，写清受影响箱数、返工工时、交付风险、客户影响、决策截止时间和若不决策的后果。",
    "S10": "7. 因为这里同时涉及设备、质量、待料、EHS 和交付多事项，额外输出影响评分板和管理升级决策包，写清各事项影响等级、阻塞关闭原因数、决策截止时间和若不决策的后果。",
}


def load_scenarios() -> list[dict[str, str]]:
    text = SCENARIOS.read_text(encoding="utf-8")
    matches = list(re.finditer(r"^## (S\d{2}) (.+)$", text, flags=re.MULTILINE))
    if len(matches) != 10:
        raise SystemExit(f"expected 10 enterprise scenarios, found {len(matches)}")

    scenarios: list[dict[str, str]] = []
    for idx, match in enumerate(matches):
        start = match.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        scenarios.append(
            {
                "id": match.group(1),
                "title": match.group(2).strip(),
                "body": text[start:end].strip(),
            }
        )
    return scenarios


def render_prompt(scenario: dict[str, str]) -> str:
    screenshot_name = f"{scenario['id']}_AstronClaw_enterprise_flow_YYYYMMDD.png"
    impact_rule = IMPACT_SCENARIOS.get(scenario["id"], "")
    impact_focus = "\n- 影响评分板\n- 管理升级决策包" if impact_rule else ""
    return f"""## {scenario["id"]} {scenario["title"]}

证据焦点：生产部发现、通知层、正式系统链路、部门反馈、闭环门禁、关闭后知识沉淀  
场景：`enterprise_flow`  
截图文件名：`{screenshot_name}`

复制到 AstronClaw 的提示词：

```text
使用 industrial-workorder-collaboration 处理下面的企业现场协同场景。请按 Skill 规则输出可执行结果，必须覆盖：

1. 生产部发现什么，以及如何建立统一事件包。
2. 企业微信/飞书/钉钉/邮件如何通知、催办和轻量确认。
3. MES、CMMS、QMS、EHS、SAP/ERP、OA、PMC/APS/排产表分别如何留痕和回执。
4. 各部门必须反馈什么字段，哪些缺口会阻塞闭环。
5. 生产部如何汇总、升级和判断能否关闭。
6. 知识库/SOP 只能在事件关闭后生成候选沉淀，不能参与最初紧急流转。
{impact_rule}

专项场景：

{scenario["title"]}

{scenario["body"]}
```

截图必须覆盖：

- 统一事件包或事件摘要
- 部门行动表
- 系统动作卡或正式系统链路
- 闭环门禁
- 决策截止时间或升级条件{impact_focus}
- 知识库/SOP 关闭后沉淀边界

运行记录填写：

```csv
{scenario["id"]},enterprise_flow,enterprise_required,YYYY-MM-DD,runner,AstronClaw,1,latency,yes,score,,no,{screenshot_name},通过后填入实际截图路径
```
"""


def write_prompt_pack(scenarios: list[dict[str, str]], out: Path) -> None:
    body = [
        "# AstronClaw 企业部门协同 10 场景专项实测包",
        "",
        "用途：审核通过后，把以下 S01-S10 提示词逐条复制到 AstronClaw，用于证明本 Skill 能处理真实企业生产部牵头的跨部门协同闭环。",
        "",
        f"专项场景数量：{len(scenarios)}",
        "",
        "通过条件：输出必须能区分通知层、正式系统留痕、部门反馈、授权边界、关闭门禁和关闭后知识沉淀；不得声称外部系统已自动完成。",
        "对高影响场景，还必须体现影响评分板、管理升级决策包、决策截止时间和若不决策的后果。",
        "",
    ]
    body.extend(render_prompt(scenario) for scenario in scenarios)
    out.write_text("\n".join(body), encoding="utf-8")


def write_run_record(scenarios: list[dict[str, str]], out: Path) -> None:
    rows = []
    for scenario in scenarios:
        rows.append(
            {
                "case_id": scenario["id"],
                "scenario": "enterprise_flow",
                "priority_for_screenshot": "enterprise_required",
                "run_date": "",
                "runner": "",
                "platform": "",
                "attempt": "1",
                "latency_seconds": "",
                "passed": "",
                "score": "",
                "error_type": "",
                "retry_needed": "",
                "output_file_or_screenshot": "",
                "notes": scenario["title"],
            }
        )
    with out.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt-out", default=str(DEFAULT_PROMPT_OUT), help="Output enterprise-flow prompt pack")
    parser.add_argument("--record-out", default=str(DEFAULT_RECORD_OUT), help="Output enterprise-flow run-record CSV")
    args = parser.parse_args()

    scenarios = load_scenarios()
    prompt_out = Path(args.prompt_out)
    record_out = Path(args.record_out)
    write_prompt_pack(scenarios, prompt_out)
    write_run_record(scenarios, record_out)
    print(f"wrote_prompt={prompt_out} wrote_record={record_out} scenarios={len(scenarios)}")


if __name__ == "__main__":
    main()
