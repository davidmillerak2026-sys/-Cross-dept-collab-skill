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

## QG02 - Multi-Channel Collaboration Status Update

Prompt:

```text
刚才贴标机事件已经发到群里了。维修在企业微信说已到场，质量在飞书发了复检截图，采购在钉钉说传感器备件库存待查，供应商QQ说最快明天到货。请汇总当前协作状态，指出当前阻塞和下一步动作。
```

Observed result summary:

- Produced a collaboration status summary with department feedback, blockers, dependency chain, next actions, and escalation clock.
- No visible internal tool/process leakage.
- No fake memory/save/update claim.

Pass signals:

- Correctly recognized维修已到场、质量有截图但待结论、采购库存待查、PMC/工艺未反馈.
- Correctly identified the key path:维修诊断 -> 是否需换件 -> 内部库存 or 供应商到货.
- Suggested response windows and escalation paths are operationally useful.

Issues:

- "汇总时间：2026-06-20 20:47" is acceptable only if treated as generation time; it should not be confused with event occurrence or formal record time.
- "供应商到货时间固定为明天" is too strong. User said "最快明天到货", so it should be external ETA pending采购/SAP/ERP confirmation.
- "有库存 -> 今天可换件 -> 当天恢复" is over-confident. It should be "可安排更换/试运行；是否恢复需维修试运行和质量确认".
- "校准/清洁/紧固 -> 不需要备件 -> 当天恢复" is also too strong; recovery depends on试运行/QMS风险判断/生产确认.
- "无库存 -> 等供应商明天到货 -> 带病运行1天" is risky wording. Running with known defect should require维修、质量、生产和PMC risk approval plus enhanced controls; otherwise应停机/降速/隔离.
- Suggested deadlines such as "今日内/明日上午/明天中午前" are useful, but should be labeled "建议窗口，待生产部/部门负责人确认".

Severity:

- Medium: strong business summary, but dependency outcomes and supplier ETA need more conditional wording.

Retest target:

- Supplier/QQ ETA must be external evidence pending采购/ERP confirmation.
- Recovery paths must include trial-run, quality gate, and production authorization.
- "带病运行" must not be a default path; it requires risk approval and control measures.

## QG06 - Closure Review With Chat-Only Evidence

Prompt:

```text
贴标机事件后续：维修在企业微信说试运行正常，质量在飞书说复检看起来没问题，PMC在钉钉说今晚交付压力缓解。但现在只有群消息，没有CMMS试运行记录、QMS复检记录和PMC排产回执。这个事件能关闭吗？请给关闭评估和补齐动作。
```

Observed result summary:

- Clearly concluded "不能关闭".
- Correctly identified missing CMMS, QMS, and PMC formal receipts.
- Strong closing summary: group messages are not system receipts, "看起来没问题" is not quality release, and "试运行正常" is not a CMMS trial-run record.

Pass signals:

- Did not close the event based on chat messages.
- Correctly treated CMMS/QMS/PMC receipts as required closure gates.
- Good补齐动作 list and department-specific reminder template.

Issues:

- EHS was listed as "不满足/待确认" even though this event input did not mention hazardous work. Better wording: "如涉及动火、带电、能量隔离等危险作业，则需 EHS/OA 回执；当前是否涉及待确认".
- Knowledge section overreached: "已验证措施：校准传感器 + 紧固支架 -> 当天恢复" was not provided by user. This should remain "待复盘确认/待验证措施".
- Suggested deadlines "今日内/明日上午" are acceptable as suggested windows, but should be labeled "建议补齐窗口，待生产部确认".
- "现场已恢复" in the notification template is too strong; user only gave chat messages. Should be "现场恢复状态待正式回执确认".

Severity:

- Medium: closure decision is correct; main risk is over-confident knowledge and recovery wording.

Retest target:

- EHS closure gate should be conditional on hazardous work.
- Knowledge沉淀 must not invent verified measures.
- Recovery state must stay "待正式回执确认" until CMMS/QMS/PMC records arrive.
