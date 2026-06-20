# Qwen3.6 Manual AstronClaw Test Log

Date: 2026-06-20
Skill: industrial-cross-department-collaboration
Model: Qwen3.6
Mode: Manual GUI test with user paste/send support

## Scoring Calibration Note

Recommended response windows and inspection frequencies are useful in industrial coordination. They should not be treated as defects when they are clearly framed as suggestions. The defect is when a model presents an unprovided time, frequency, file path, system action, or meeting arrangement as already confirmed.

## QG01 - New Maintenance + Quality Event

Prompt:

```text
三号包装线贴标机这两天漏贴率明显升高，传感器偶尔抖动。维修只说再观察，生产担心突然停线，请帮我组织一次生产部牵头的跨部门协同。
```

Observed result summary:

- Produced a much richer business structure than Spark-X2-Flash: unified event package, evidence facts, signal calibration, candidate diagnosis matrix, department action matrix, system chain, feedback contract, risk hints, missing information, and copyable sync message.

Pass signals:

- Correctly recognized maintenance + quality compound scenario and P1 risk.
- Correctly kept "维修再观察" as unresolved and asked for CMMS record.
- Good evidence IDs E01-E04.
- Good formal system chain: MES, CMMS, QMS, SAP/ERP.
- Good candidate diagnosis matrix and missing information list.

Issues:

- Exposed internal/tool process at the beginning: "工具调用完成 read", "让我先读取相关的工业跨部门协同技能文件", "根据 Skill 的输出模式...". This must not appear in final Skill output.
- Suggested deadlines such as "今日内", "明日上午", and "3 个工作日内" need confirmation wording; they are acceptable as recommended urgency windows if labeled as such.
- Suggested operating frequency "每班次至少 2 次点检" can be useful, but should be framed as "建议频次，待生产/质量确认".
- Suggested "100% 全检" as a recommendation without qualifying it as quality-authorized and risk-based.
- The sync message says "维修已关注" though the input only says维修说再观察; better phrase as "维修已有初步反馈但未形成系统性排查结论".
- It still does not use a strict action-card readiness state for CMMS/QMS/MES writes.

Severity:

- Major: internal tool/process leakage.
- Medium: suggested deadlines/frequency need clearer "建议/需确认" labeling.
- Medium: some over-strong operational recommendations.

Retest target:

- Hide all tool/process reasoning: no "read", no "根据 Skill", no "让我分析".
- Keep time/frequency fields as待确认 unless provided by user or企业SLA; suggested values are allowed when clearly labeled as recommendations.
- Recommendations such as全检 must be explicitly "由质量负责人确认".
