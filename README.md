# 工业现场工单协同助理 Skill

本 Skill 面向制造企业“生产部现场信息到跨部门办公协同”的断层问题，把一线语音、巡检、故障、质量、安全、计划变更和交接记录转成由生产部牵头的可执行工单、跨部门待办、复盘纪要、审批说明、PMC 同步和管理周报。

## 适用场景

- 设备维修：报警、停机、异常声响、预测性维护提醒
- 质量协同：批次异常、返工返修、临时隔离、复检安排
- EHS 安全：隐患上报、整改闭环、危险作业提醒
- 换线换型：SKU 切换、参数确认、首件检验待办
- 生产计划协同：PMC 排产、产能、交期、缺料、插单和加班评估
- 跨部门办公：会议纪要、审批说明、日报/周报、行动项追踪

## 核心能力

1. 从非结构化现场记录中提取时间、地点、设备、现象、影响、措施和待确认信息。
2. 生成维修、质量、安全、生产等部门可直接执行的工单草案。
3. 将现场事实转成以生产部为 Owner、责任方明确、截止时间明确、验收标准明确的待办表。
4. 区分已确认事实、合理推断和待确认信息，避免误把猜测写成结论。
5. 对安全、质量和合规风险做保守提示，不给出绕过 SOP 的建议。
6. 生成 CMMS、MES、QMS、EHS、SAP/ERP、OA 审批、PMC/APS、PLM/工程变更和协同 IM 可用的动作卡，用统一事件包区分聊天通知、业务留痕、审批链路和系统回执，但不假装已经完成外部系统同步。
7. 用脱敏规则处理真实记录，避免在样例、日志和评审材料中暴露个人信息或凭证。
8. 输出动作准备度门禁，区分可提交、需确认、需授权和字段缺失。
9. 对已关闭事项生成闭环学习草稿，沉淀为后续相似工单和 SOP 候选知识。
10. 建立证据索引、候选诊断矩阵、授权人决策包和运行轨迹，支撑复杂任务的可审计推进。
11. 对趋势、阈值和老师傅经验执行信号校准门禁，缺阈值不乱判报警。
12. 对工具失败、附件不可读、系统未登录等情况输出降级完成结果和恢复路径。
13. 对提示注入、刷量请求、冲突记录和长噪声输入执行安全隔离和鲁棒处理。
14. 对维修/现场服务生成现场执行包，覆盖班组技能、备件工具、作业许可、停机窗口、PMC 交期影响和验收试运行。
15. 对创建、更新、关闭工单执行数据质量门禁，缺故障码、原因码、措施、工时、备件或验收证据时不允许假装闭环。
16. 输出试用反馈卡和商业价值量化模型，帮助审核通过后收集真实试用证据，但不夸大未验证收益。
17. 内置 10 个生产部牵头的真实企业流转场景，覆盖 MES、CMMS、QMS、EHS、SAP/ERP、OA、PMC/APS 和企业 IM 的分工、反馈和闭环门禁。
18. 内置 ST01-ST12 异常输入压力包，覆盖短输入、噪声、重复、冲突、危险请求、提示注入、隐私凭证、缺字段、系统失败、伪造完成、多事件混合和渠道误用。
19. 内置 6 类角色试用反馈访谈包、反馈记录模板和价值评分脚本，用于收集真实脱敏试用证据，不伪造收益。
20. 对跨部门高影响事件输出影响评分板和管理升级决策包，帮助生产经理、PMC、质量和安全负责人快速做决策。

## 适合谁收藏和下载

- 制造业设备、维修、工艺、生产、质量、安全管理人员
- 需要把现场语音和巡检记录整理成办公材料的一线班组
- 需要把会议纪要、整改事项、复检任务和审批说明标准化的运营团队
- 正在建设 CMMS、MES、QMS、EHS、OA 或企业知识库的数字化团队

如果你经常遇到“现场说清楚了，但工单、待办、纪要没人整理”的问题，可以收藏并下载这个 Skill 试用。

## 使用方式

把现场语音转写、巡检记录、会议纪要或异常描述发给支持 Agent Skills 的智能体，并要求：

- “帮我生成工单”
- “整理成跨部门待办”
- “生成维修复盘纪要”
- “写成审批说明”
- “汇总成本周现场协同周报”

## 快速试用提示词

```text
使用 industrial-workorder-collaboration，把下面这段现场记录整理成工单、跨部门待办和待确认信息：

三号包装线贴标机 14:20 开始频繁漏贴，操作员说更换标签卷后还是有问题。现在已经停了 18 分钟，质检发现 32 箱需要复检。维修看过传感器位置可能偏了，但还没确认。生产希望 15:30 前恢复。
```

## 文件结构

```text
industrial-workorder-collaboration/
├── SKILL.md
├── README.md
├── VERSION.md
├── submission_manifest.json
├── examples/
│   ├── 00_judge_quick_run.md
│   ├── 01_voice_to_work_order.md
│   ├── 02_quality_issue_to_collaboration.md
│   ├── 03_shift_handover_weekly_report.md
│   ├── 04_complex_agent_workflow.md
│   ├── 05_signal_degraded_self_review.md
│   ├── 06_expert_screenshot_outputs.md
│   ├── 07_enterprise_department_flow_10_scenarios.md
│   ├── 08_sku_quality_coordination_run.md
│   └── data/
│       └── sku_quality_coordination_sample.csv
├── references/
│   ├── contest_fit.md
│   ├── evaluation_evidence.md
│   ├── expert_review_playbook.md
│   ├── capability_playbook.md
│   ├── rubric_evidence_matrix.md
│   ├── commercial_value_model.md
│   └── full_score_strategy.md
├── scripts/
│   ├── redact_input.py
│   ├── score_run.py
│   ├── score_enterprise_flow.py
│   ├── score_stability_stress.py
│   ├── score_pilot_feedback.py
│   ├── export_prompt_pack.py
│   ├── export_required_evidence_pack.py
│   ├── export_required_run_record.py
│   ├── export_enterprise_flow_pack.py
│   ├── export_stability_stress_pack.py
│   ├── export_pilot_feedback_pack.py
│   ├── export_expert_evidence_sprint_pack.py
│   ├── evidence_sprint_status.py
│   ├── evidence_readiness_report.py
│   ├── champion_acceptance_gate.py
│   ├── smoke_test_package.py
│   ├── expert_rubric_gate.py
│   └── validate_package.py
├── tests/
│   ├── astronclaw_stability_protocol.md
│   ├── astronclaw_stability_stress_prompt_pack.md
│   ├── golden_outputs.md
│   ├── enterprise_flow_golden_outputs.md
│   ├── stability_stress_cases.json
│   ├── pilot_feedback_roles.json
│   ├── pilot_feedback_interview_pack.md
│   ├── pilot_feedback_records_template.csv
│   ├── platform_submission_evidence_template.json
│   ├── champion_acceptance_report.md
│   ├── evidence_readiness_report.md
│   ├── README.md
│   ├── rubric_evidence_matrix.csv
│   ├── run_record_template.csv
│   ├── run_record_required_template.csv
│   ├── run_record_stability_stress_template.csv
│   ├── evidence/
│   │   └── README.md
│   ├── run_outputs/
│   │   └── README.md
│   ├── enterprise_flow_outputs/
│   │   └── README.md
│   ├── stability_stress_outputs/
│   │   └── README.md
│   ├── astronclaw_required_prompt_pack.md
│   ├── astronclaw_enterprise_flow_prompt_pack.md
│   ├── expert_evidence_sprint_pack.md
│   ├── expert_evidence_sprint_manifest.csv
│   ├── expert_evidence_sprint_status.md
│   ├── skillhub_prompt_pack.md
│   ├── run_record_enterprise_flow_template.csv
│   └── test_cases.json
└── templates/
    ├── action_card.schema.json
    ├── action_readiness.schema.json
    ├── adversarial_guardrail.md
    ├── champion_self_review.schema.json
    ├── closed_loop_learning.md
    ├── degraded_completion.md
    ├── diagnosis_matrix.schema.json
    ├── department_communication_flow.md
    ├── enterprise_flow_output_contract.md
    ├── evidence_trace.schema.json
    ├── field_execution_plan.md
    ├── handoff_summary.md
    ├── human_decision_packet.md
    ├── impact_scoreboard.md
    ├── impact_scoreboard.schema.json
    ├── integration_contracts.json
    ├── management_escalation_packet.md
    ├── office_message_templates.md
    ├── output_modes.md
    ├── pilot_feedback_card.md
    ├── quality_gate.md
    ├── redaction_rules.json
    ├── role_handoff.md
    ├── run_trace.schema.json
    ├── scorecard.schema.json
    ├── signal_calibration.schema.json
    ├── work_order_data_quality.md
    └── work_order.schema.json
```

## 评审对应关系

- 运行稳定性与鲁棒性：固定输入处理流程、优先级规则、事实/推断/待确认分层。
- 创新性和应用价值：把 AR/边缘智能采集到的一线信息转化为企业办公协同资产。
- 结果质量：统一输出工单、待办、风险、待确认信息，便于落地到 CMMS、MES、QMS、EHS 或协同办公系统。
- 技术设计与场景编排：支持多场景分类，并可与知识库、工单系统和审批流程组合。
- 多工具协同：提供 CMMS/MES/QMS/EHS/SAP/ERP/OA 审批/PMC/APS/PLM/协同 IM 的动作卡契约，标明必填字段、缺失字段、渠道边界和授权要求。
- 系统分层契约：`templates/integration_contracts.json` 把企业 IM/邮件、OA 审批、PMC/APS、PLM/工程变更、SAP/ERP、MES、CMMS、QMS、EHS 明确拆开，避免把通知、审批、排产和工程变更混成一个模糊动作。
- 部门沟通链路：用统一事件包解释生产部、维修、质量、工程、EHS、PMC、仓库/采购如何通过聊天通知和业务系统互通反馈。
- 真实企业流转：内置 10 个生产部牵头场景，明确企业 IM 只做通知，MES/CMMS/QMS/EHS/SAP/ERP/OA/PMC/APS 承接正式记录和回执，知识库/SOP 只在关闭后沉淀。
- 企业协同输出合同：用 `templates/enterprise_flow_output_contract.md` 固化统一事件包、分层流转、部门反馈合同、正式系统动作卡、闭环门禁、升级时钟和关闭后知识候选。
- 管理决策层：用 `templates/impact_scoreboard.md` 和 `templates/management_escalation_packet.md` 把停线、质量、安全、交付、物料和成本影响收敛成可拍板材料。
- 动作准备度：输出 `ready_to_submit`、`needs_confirmation`、`requires_authorization`、`blocked_missing_fields`。
- 复杂任务推进：输出证据索引、候选诊断、角色交接、授权决策和运行轨迹。
- 工业信号处理：输出信号校准门禁，避免阈值缺失时乱判超限。
- 现场执行编排：把派工推进到班组技能、备件工具、作业许可、停机窗口、试运行和失败回退。
- 工单数据质量：关闭或更新前检查故障码、原因码、措施、工时、备件、停机影响和验收证据。
- 稳定降级：外部系统或附件失败时仍给出最小可执行结果和恢复路径。
- 对抗鲁棒性：隔离外部内容中的越权指令，拒绝刷量和伪造状态，处理长噪声和冲突事实。
- 闭环学习：把已关闭工单、复盘结论和整改记录转成候选知识条目。
- 应用价值证据：用试用反馈卡和商业价值量化模型记录真实试用、节省时间、字段完整度和人工授权边界。
- 影响量化：把生产损失、交付风险、阻止闭环的关键缺口和决策截止时间显式化，减少管理层反复追问。
- 工程规范与文档完整性：包含主 Skill、README、示例和 JSON Schema。
- 版本与提交可复核性：`VERSION.md` 和 `submission_manifest.json` 记录版本、用例数量、必截图清单和本地门禁。
- 安全合规：内置隐私脱敏、安全风险保守处理和不编造事实原则。

## 冠军版增强点

- 场景路由：覆盖维修、质量、EHS、换线、会议、交接、备件/外协。
- 质量门禁：每次输出前检查责任方、依据、验收标准、待确认信息和合规风险。
- 异常输入处理：输入过短、信息冲突、危险操作、隐私信息、越权放行均有处理规则。
- 证据包：内置 39 个测试用例，便于提交后截图证明运行稳定性。
- 评分矩阵：`tests/rubric_evidence_matrix.csv` 把 39 个用例逐一映射到官方 6 个评分项。
- 必截图实测包：`tests/astronclaw_required_prompt_pack.md` 只保留 18 个专家榜 required 截图用例，避免实测漏项。
- 必截图记录表：`tests/run_record_required_template.csv` 只保留 18 个专家榜 required 截图记录，方便第一轮实测采集。
- 总控冲刺包：`scripts/export_expert_evidence_sprint_pack.py` 会生成 `tests/expert_evidence_sprint_pack.md` 和 `tests/expert_evidence_sprint_manifest.csv`，把平台提交、18 个必截图、S01-S10、ST01-ST12 和 6 类试用反馈按阶段串起来，减少漏跑、漏记和漏评分。
- 证据冲刺状态：`scripts/evidence_sprint_status.py` 会生成 `tests/expert_evidence_sprint_status.md`，逐阶段显示 SkillHub 公开链接、平台截图、T01-T39、S01-S10、ST01-ST12 和试用反馈哪些已经有真实证据，哪些仍阻塞冠军验收。
- 证据目录：`tests/evidence/README.md` 定义实测截图和输出文件的存放规则。
- 全量评分输出目录：`tests/run_outputs/README.md` 定义 T01-T39 文本输出保存方式，直接服务 `scripts/score_run.py`。
- 异常输入压力包：`tests/stability_stress_cases.json`、`tests/astronclaw_stability_stress_prompt_pack.md` 和 `tests/run_record_stability_stress_template.csv` 用于证明输入过短、噪声、冲突、危险请求、提示注入、隐私凭证、系统失败等场景不崩溃、不越权。
- 应用价值证据：`templates/pilot_feedback_card.md` 和 `references/commercial_value_model.md` 用于收集真实试用反馈和估算可审计价值。
- 试用访谈证据包：`tests/pilot_feedback_roles.json`、`tests/pilot_feedback_interview_pack.md` 和 `tests/pilot_feedback_records_template.csv` 覆盖生产主管、设备维修、质量、EHS、PMC 和数字化负责人 6 类角色。
- 版本记录：`VERSION.md` 记录冠军版迭代历史，`submission_manifest.json` 固化提交清单、用例数量、required 截图 ID 和证据边界。
- 十场景演练：`examples/07_enterprise_department_flow_10_scenarios.md` 覆盖非计划停机、首件异常、油温报警、安全隐患、待料、泄漏、重复故障、客诉返工、临时工艺变更和日清会闭环。
- SKU 质量交付演练：`examples/08_sku_quality_coordination_run.md` 和 `examples/data/sku_quality_coordination_sample.csv` 展示从生产异常到 QMS 质量反馈、PMC 交付重排、仓库发货锁定、工程现场验证和管理升级决策的完整链路。
- 十场景实测包：`tests/astronclaw_enterprise_flow_prompt_pack.md` 和 `tests/run_record_enterprise_flow_template.csv` 可逐条记录 S01-S10 真实企业部门协同输出。
- 十场景黄金检查点：`tests/enterprise_flow_golden_outputs.md` 用于人工复核 S01-S10 实测输出是否命中关键业务语义且没有越权完成措辞。
- 专家门禁：`scripts/expert_rubric_gate.py` 按官方 100 分评分项检查本地证据和 AstronClaw 待证明项；`--require-astronclaw` 会校验记录里的截图/输出文件真实存在。
- 赛题匹配：明确把工业现场信息转化为办公协同材料，而不是硬件或平台宣传。
- 自检脚本：`scripts/validate_package.py` 可重复检查包体格式、JSON、测试覆盖、敏感信息和官方上传约束。
- 运行评分：`scripts/score_run.py` 可在 AstronClaw 实际调用后生成测试评分报告，支撑专家榜“运行稳定性与鲁棒性”证据。
- 专项评分：`scripts/score_enterprise_flow.py` 可在 S01-S10 实测输出后检查企业部门协同链路是否完整。
- 压力评分：`scripts/score_stability_stress.py` 可在 ST01-ST12 实测输出后检查危险建议、凭证泄露、未授权同步/放行/关闭等问题。
- 试用评分：`scripts/score_pilot_feedback.py` 可在真实试用反馈收集后检查反馈完整度、节省时间、公开授权和安全边界。
- 证据就绪度报告：`scripts/evidence_readiness_report.py` 生成 `tests/evidence_readiness_report.md`，把本地资产、平台实测证据和真实试用反馈分开判定，避免把本地通过误报成专家榜最终完成。
- 冠军验收门禁：`scripts/champion_acceptance_gate.py` 生成 `tests/champion_acceptance_report.md`，把 SkillHub 提交/审核截图、T01-T39、S01-S10、ST01-ST12 和真实试用反馈统一纳入最终验收。
- 管理升级模板：`templates/impact_scoreboard.md`、`templates/management_escalation_packet.md` 和 `templates/impact_scoreboard.schema.json` 支撑管理层评估与结构化输出。
- 实测提示词：`scripts/export_prompt_pack.py` 可生成 AstronClaw 逐条复制测试包。
- 脱敏工具：`scripts/redact_input.py` 可在使用真实现场记录前先屏蔽手机号、邮箱、身份证号和凭证类字段。
- 本地回归：`scripts/smoke_test_package.py` 可调试脱敏、提示词导出、评分逻辑和评分矩阵覆盖。

## 上传前调试门禁

```bash
python scripts/validate_package.py
python scripts/smoke_test_package.py
python scripts/expert_rubric_gate.py
```

以上只证明本地包体和脚本链路通过。真正的运行稳定性必须按 `tests/astronclaw_stability_protocol.md` 在 AstronClaw 连续实测：能正常部署调用，异常输入不崩溃，响应稳定，无频繁失败。

## 注意事项

- 不要在 Skill 包中放入真实 API Key、系统账号、客户数据或未脱敏现场记录。
- 如需展示视频、安装包或大型二进制文件，请在材料中提供外链，不要放入 Skill ZIP。
- 上传到 OCAS-skill 赛题页时，作品名称必须填写 `industrial-workorder-collaboration`，与 `SKILL.md` 的 `name` 保持一致。
