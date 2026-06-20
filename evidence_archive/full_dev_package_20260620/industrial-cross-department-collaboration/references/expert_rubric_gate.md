# 专家榜硬评分门禁

用途：把官方 100 分评分标准转成可检查证据，避免把本地包体通过误认为专家榜满分。

## 官方评分标准

| 评分维度 | 分值 | 关键验收 |
| --- | ---: | --- |
| 运行稳定性与鲁棒性 | 30 | 可在 AstronClaw 正常部署调用；异常输入不崩溃；响应稳定、无频繁失败 |
| 作品创新性和应用价值 | 30 | 功能创新、体验优化、具备明确商用价值 |
| 结果质量 | 20 | 输出结果完整、准确，符合任务指令要求 |
| 技术设计与场景编排能力 | 10 | 模型/底座选型合理；支持多插件/多工具协同，易用性 |
| 工程规范与文档完整性 | 5 | 符合 Skill 开发规范；README 完整；代码结构清晰、注释规范 |
| 安全合规指标 | 5 | 无安全风险、无越权行为、数据处理合规 |

## 本地门禁

运行：

```bash
python scripts/validate_package.py
python scripts/smoke_test_package.py
python scripts/expert_rubric_gate.py
```

本地门禁只能证明包体结构、脚本链路、测试矩阵、评分矩阵、脱敏和安全规则已准备好；不能证明 AstronClaw 运行稳定。

## AstronClaw 门禁

平台可用后运行 39 个用例并记录到 `tests/run_record_template.csv`，然后运行：

```bash
python scripts/expert_rubric_gate.py --require-astronclaw
```

通过条件：

- T01-T39 至少各运行 1 次。
- T01、T06、T11、T21、T24、T25、T27、T28、T29、T30、T31、T33、T34、T35、T36、T37、T38、T39 有截图或输出文件。
- 运行记录中的 `output_file_or_screenshot` 必须指向真实存在的本地文件，推荐放在 `tests/evidence/screenshots/` 或 `tests/evidence/outputs/`。
- 不出现连续平台错误、空输出、越权、危险操作或 forbidden_hits。
- 失败记录不删除，必须通过后续 attempt 证明恢复。
