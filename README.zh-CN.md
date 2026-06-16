# 跨部门协同 Skill

`industrial-workorder-collaboration` 是一个面向制造企业的生产部跨部门协同 Skill。它把现场记录、报警、交接、质量异常、安全隐患和会议纪要，整理成可执行的工单草案、部门待办、系统动作卡、授权决策包和闭环复盘材料。

这个项目解决的不是“写一段漂亮总结”，而是真实企业里常见的信息断层：生产部在车间发现问题后，如何让维修、质量、工程、安全、PMC、仓库和采购围绕同一份事实协同，并让 MES、CMMS、QMS、EHS、SAP/ERP、OA、PMC/APS 分别留下正式记录和回执。

## 核心能力

- 从非结构化现场记录中提取时间、地点、设备、现象、影响、措施和待确认信息。
- 区分已确认事实、合理推断和待确认信息，避免把猜测写成结论。
- 生成生产部牵头的统一事件包，明确 Owner、影响范围、下一次同步时间和升级路径。
- 为生产、维修、质量、工程、EHS、PMC、仓库、采购生成责任明确的行动项。
- 生成 MES、CMMS、QMS、EHS、SAP/ERP、OA、PMC/APS 可承接的动作卡。
- 用企业流转输出合同稳定生成统一事件包、分层流转、部门反馈合同、正式系统动作卡、闭环门禁和关闭后知识候选。
- 在没有真实系统回执前，不声称已经同步、审批、放行、恢复生产或关闭工单。
- 对质量放行、安全许可、客户承诺、正式 SOP 发布和系统写入保留人工授权边界。
- 在系统不可用、附件不可读、记录冲突或字段缺失时，输出降级但可执行的结果。
- 内置 ST01-ST12 异常输入压力用例，覆盖短输入、噪声、重复、冲突、危险请求、提示注入、隐私凭证、缺字段、系统失败、伪造完成、多事件混合和渠道误用。
- 内置 6 类角色试用反馈访谈包和应用价值评分脚本，用于收集真实脱敏反馈，不伪造收益。
- 事件关闭后，才生成知识库/SOP 候选条目，不参与最初紧急流转。

## 企业系统分层

| 层级 | 系统或渠道 | 作用 |
| --- | --- | --- |
| 通知层 | 企业微信、飞书、钉钉、邮件 | 通知、催办、轻量确认、会议邀约 |
| 生产记录 | MES | 生产状态、停线时间、少产数量、恢复窗口 |
| 设备维修 | CMMS | 维修工单、派工、备件、工时、试运行 |
| 质量管理 | QMS | 隔离、复检、返工、放行、CAPA |
| 安全管理 | EHS | 安全隐患、作业许可、能量隔离、整改闭环 |
| 经营系统 | SAP/ERP | 订单、物料、备件、库存、采购、成本、交付影响 |
| 审批升级 | OA | 审批、异常报告、跨部门会议纪要、管理升级 |
| 计划排产 | PMC/APS/排产表 | 产能、交期、加班、插单和排产调整 |
| 经验沉淀 | 知识库/SOP | 关闭后的经验沉淀和候选 SOP 更新 |

## 文件结构

```text
.
├── SKILL.md
├── README.md
├── README.zh-CN.md
├── docs/
│   ├── architecture.md
│   ├── operating_playbook.md
│   ├── scenario_index.md
│   └── upload_manifest.md
├── examples/
│   ├── 01_voice_to_work_order.md
│   ├── 02_quality_issue_to_collaboration.md
│   ├── 03_shift_handover_weekly_report.md
│   ├── 04_complex_agent_workflow.md
│   ├── 05_enterprise_department_flow_10_scenarios.md
│   └── 06_demo_output_unplanned_stop.md
├── scripts/
│   ├── redact_input.py
│   └── validate_project.py
├── templates/
└── tests/
```

## 快速试用提示词

```text
使用 industrial-workorder-collaboration 处理下面的现场记录：

三号包装线贴标机 14:20 开始频繁漏贴，操作员更换标签卷后仍然没有改善。当前已经停线 18 分钟，质量发现 32 箱需要复检。维修怀疑传感器偏位，但还没有验证。生产希望 15:30 前恢复。
```

完整示例输出见：`examples/06_demo_output_unplanned_stop.md`。

企业协同输出合同见：`templates/enterprise_flow_output_contract.md`；S01-S10 场景复核检查点见：`tests/enterprise_flow_golden_outputs.md`。

异常输入压力用例见：`tests/stability_stress_cases.json`；可复制压力提示词见：`tests/stability_stress_prompt_pack.md`。

试用反馈访谈包见：`tests/pilot_feedback_interview_pack.md`；反馈记录模板见：`tests/pilot_feedback_records_template.csv`。

## 本地校验

```bash
python scripts/validate_project.py
python scripts/redact_input.py --text "张三 13812345678 test@example.com token=abc123"
```

## 关键边界

这个 Skill 只生成结构化草案、动作卡和决策包，不直接替企业系统完成写入。质量放行、安全许可、生产恢复、客户承诺、SOP 正式发布和带权限的系统动作，必须由授权人员或上层系统确认。
