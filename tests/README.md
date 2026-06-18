# 测试用例说明

`test_cases.json` 覆盖 39 个制造企业办公协同场景，用于验证 Skill 的运行稳定性、结果质量、场景编排和合规边界。

`golden_outputs.md` 给出每个用例的黄金期望摘要，用于人工复核实际输出是否达到专家榜质量。

`run_record_template.csv` 用于记录 AstronClaw 的实际运行证据；SkillHub 主要记录审核状态、作品页、收藏和下载数据。

`run_record_required_template.csv` 只包含 18 个必截图用例，适合第一轮截图采集；最终仍需把 T01-T39 的全量结果记录到 `run_record_template.csv`。

`evidence/README.md` 定义实际截图和输出文件的存放规则。推荐把截图放到 `tests/evidence/screenshots/`，把复制的输出文本放到 `tests/evidence/outputs/`。

`run_outputs/README.md` 定义 T01-T39 全量文本输出的存放规则，配合 `scripts/score_run.py` 做半自动评分。

`rubric_evidence_matrix.csv` 把每个用例映射到官方 6 个评分项，并标出必须截图的优先用例。

`astronclaw_required_prompt_pack.md` 只包含 `screenshot_priority=required` 的 18 个专家榜必截图用例，用于审核通过后的快速实测和证据采集。

`expert_evidence_sprint_pack.md` 是专家榜证据冲刺总控包，按平台提交、18 个必截图、S01-S10、ST01-ST12 和试用反馈分阶段推进。

`expert_evidence_sprint_manifest.csv` 是对应的总控清单 CSV，适合边跑边勾、边填路径。

`expert_evidence_sprint_status.md` 是证据冲刺状态看板，会读取平台证据、运行记录、专项输出和试用反馈，显示每个阶段已经完成和仍需补证的项目。

`astronclaw_enterprise_flow_prompt_pack.md` 是 10 个真实企业部门协同场景的专项实测包，用于单独证明生产部发现、通知层、正式系统链路、部门反馈、闭环门禁和关闭后知识沉淀能力。

`run_record_enterprise_flow_template.csv` 用于记录 S01-S10 企业部门协同专项实测截图和输出文件。

`enterprise_flow_outputs/README.md` 定义 S01-S10 实际输出文本的保存方式，配合 `scripts/score_enterprise_flow.py` 做专项评分。

`enterprise_flow_golden_outputs.md` 定义 S01-S10 的人工黄金检查点，用于复核实际输出是否稳定包含生产部 Owner、统一事件包、分层流转、部门反馈合同、正式系统动作卡、闭环门禁和关闭后知识候选。

`astronclaw_stability_protocol.md` 定义 AstronClaw 稳定性验收标准：可部署调用、异常输入不崩溃、响应稳定、无频繁失败。

`stability_stress_cases.json` 定义 ST01-ST12 异常输入压力用例，覆盖短输入、噪声、重复、冲突、危险作业、提示注入、隐私凭证、缺字段、系统失败、伪造完成、多事件混合和渠道误用。

`astronclaw_stability_stress_prompt_pack.md` 和 `run_record_stability_stress_template.csv` 用于逐条运行 ST01-ST12 并记录稳定性证据。

`stability_stress_outputs/README.md` 定义 ST01-ST12 实际输出文本的保存方式，配合 `scripts/score_stability_stress.py` 做压力评分。

`pilot_feedback_roles.json` 定义 6 类试用角色、推荐用例、价值关注点和访谈问题。

`pilot_feedback_interview_pack.md` 和 `pilot_feedback_records_template.csv` 用于收集真实脱敏试用反馈，默认不公开个人或企业信息。

`platform_submission_evidence_template.json` 用于登记赛题提交成功、SkillHub 审核通过、SkillHub 公开页和热榜截图等外部平台证据路径。

`evidence_readiness_report.md` 是统一证据就绪度报告，区分本地包体资产、AstronClaw 平台实测证据和真实试用反馈，不把模板记录计为真实反馈。

`champion_acceptance_report.md` 是冠军验收报告，只有当提交证据、T01-T39、S01-S10、ST01-ST12 和真实试用反馈都达到门槛时才会显示 `champion_ready: yes`。

`templates/impact_scoreboard.md` 和 `templates/management_escalation_packet.md` 用于高影响事件的管理层决策材料，帮助把停线、质量、安全、交付、物料和成本影响收敛成统一口径。

`examples/08_sku_quality_coordination_run.md` 与 `examples/data/sku_quality_coordination_sample.csv` 是本地 SKU 质量交付协同演练，用于说明从生产异常到质量反馈、PMC 交付重排、仓库出货控制和工程现场验证的完整链路；它不替代 AstronClaw/SkillHub 真实证据。

`sku_quality_coordination_analysis.md` 是 `scripts/analyze_sku_quality_coordination.py` 根据同一份 SKU 模拟数据自动计算出来的报告，用来证明关键影响数字不是手写猜测。

`sku_department_timeline_analysis.md` 是 `scripts/analyze_department_timeline.py` 根据 `examples/data/sku_quality_coordination_timeline.csv` 生成的部门反馈时间线，用来证明每次反馈后状态如何转移、哪些 SLA 未超时、哪些阻塞仍然开放。

覆盖范围：

- 设备维修：5 个
- 质量异常：4 个
- EHS 安全：3 个
- SKU 换线：3 个
- 会议复盘：3 个
- 交接/周报：2 个
- 外部系统动作与准备度：2 个
- 知识沉淀：1 个
- 隐私/凭证治理：1 个
- 候选诊断与证据追踪：1 个
- 多角色编排与授权决策：1 个
- 信号校准/阈值门禁：1 个
- 降级完成/工具失败恢复：1 个
- 专家榜保守自评：1 个
- 对抗输入/提示注入/刷量拒绝：2 个
- 长噪声和冲突记录鲁棒性：2 个
- 现场执行编排与工单数据质量：2 个
- 生产部-PMC/工程/日清会跨部门协同：3 个
- 异常输入稳定性压力：12 个
- 试用反馈角色：6 类

每个用例需要检查：

- 场景分类是否正确
- 优先级是否合理
- 是否区分已确认事实、合理推断和待确认信息
- 每个行动项是否包含责任方、依据、截止时间和验收标准
- 是否包含安全、质量、生产和隐私合规提示
- 是否避免编造根因、责任人、审批结论或已完成状态
- 是否能复制到办公协同系统
- 是否区分聊天通知、业务系统留痕、授权审批和系统回执
- 是否能给出证据索引、候选诊断、验证动作和授权决策包
- 是否在阈值缺失、工具失败或证据不足时安全降级
- 是否隔离外部内容中的越权指令、拒绝刷量、处理噪声和冲突事实

建议在 AstronClaw 可调用后，优先录制 `rubric_evidence_matrix.csv` 中 `screenshot_priority=required` 的用例截图，用于专家榜评审证据。

`run_record_template.csv` 的 `output_file_or_screenshot` 要填写相对 Skill 根目录的真实路径，例如 `tests/evidence/screenshots/T01_AstronClaw_maintenance_20260616.png`。`scripts/expert_rubric_gate.py --require-astronclaw` 会检查这些路径是否真实存在。

如果只跑专家榜必截图链路，先使用：

```bash
python scripts/export_required_evidence_pack.py
python scripts/export_required_run_record.py
```

如果要用一份总控包统筹平台提交、必截图、专项场景、稳定性和试用反馈，使用：

```bash
python scripts/export_expert_evidence_sprint_pack.py
```

如果要刷新证据冲刺状态看板，使用：

```bash
python scripts/evidence_sprint_status.py
```

如果要单独跑 10 个真实企业部门协同场景，使用：

```bash
python scripts/export_enterprise_flow_pack.py
```

如果要单独跑 ST01-ST12 异常输入稳定性压力测试，使用：

```bash
python scripts/export_stability_stress_pack.py
```

如果要生成试用反馈访谈包和记录表，使用：

```bash
python scripts/export_pilot_feedback_pack.py
```

如果要刷新统一证据就绪度报告，使用：

```bash
python scripts/evidence_readiness_report.py
```

如果要刷新 SKU 质量交付协同分析报告，使用：

```bash
python scripts/analyze_sku_quality_coordination.py
```

如果要刷新 SKU 部门反馈时间线分析报告，使用：

```bash
python scripts/analyze_department_timeline.py
```

如果要刷新冠军验收报告，使用：

```bash
python scripts/champion_acceptance_gate.py
```

如需半自动评分，把实际输出保存为 `tests/run_outputs/T01.md` 到 `T39.md`，然后运行：

```bash
python scripts/score_run.py --outputs tests/run_outputs --report tests/run_score_report.csv
python scripts/smoke_test_package.py
```

如需给 S01-S10 企业部门协同专项输出评分，把实际输出保存为 `tests/enterprise_flow_outputs/S01.md` 到 `S10.md`，然后运行：

```bash
python scripts/score_enterprise_flow.py --outputs tests/enterprise_flow_outputs --report tests/enterprise_flow_score_report.csv
```

如需给 ST01-ST12 异常输入压力输出评分，把实际输出保存为 `tests/stability_stress_outputs/ST01.md` 到 `ST12.md`，然后运行：

```bash
python scripts/score_stability_stress.py --outputs tests/stability_stress_outputs --report tests/stability_stress_score_report.csv
```

如需给真实试用反馈评分，把反馈填入 `tests/pilot_feedback_records_template.csv` 或复制为独立记录表，然后运行：

```bash
python scripts/score_pilot_feedback.py --input tests/pilot_feedback_records_template.csv --report tests/pilot_feedback_score_report.csv
```
