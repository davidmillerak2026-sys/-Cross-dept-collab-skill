#!/usr/bin/env python3
"""Export copy-ready AstronClaw prompts from tests/test_cases.json."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "tests" / "test_cases.json"
DEFAULT_OUT = ROOT / "tests" / "skillhub_prompt_pack.md"


def load_cases() -> list[dict]:
    return json.loads(CASES.read_text(encoding="utf-8"))["cases"]


def render_case(case: dict) -> str:
    checks = "\n".join(f"- {item}" for item in case.get("checks", []))
    return f"""## {case["id"]} {case["title"]}

场景：`{case["scenario"]}`  
期望输出：{case["expected_output"]}

复制到 AstronClaw 的提示词：

```text
使用 industrial-workorder-collaboration 处理下面的现场记录。请按 Skill 规则输出可执行结果，并保留待确认信息、风险提示和安全边界。

{case["input"]}
```

人工检查要点：

{checks}
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=str(DEFAULT_OUT), help="Output markdown prompt pack")
    args = parser.parse_args()
    out = Path(args.out)
    cases = load_cases()
    body = [
        "# AstronClaw 实测提示词包",
        "",
        "用途：审核通过后，把以下提示词逐条复制到 AstronClaw，用于截图留证和半自动评分。SkillHub 用于审核状态、作品页和热度数据截图。",
        "",
        f"用例数量：{len(cases)}",
        "",
    ]
    body.extend(render_case(case) for case in cases)
    out.write_text("\n".join(body), encoding="utf-8")
    print(f"wrote={out} cases={len(cases)}")


if __name__ == "__main__":
    main()
