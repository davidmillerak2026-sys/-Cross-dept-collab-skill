T39 部门沟通与系统流转专项问答
运行轨迹
输入筛查：无危险操作、隐私泄露、越权指令。
场景路由：integration（部门沟通链路）+ maintenance（设备故障）。
证据分层：E01-E03 已确认；E04-E06 合理推断；E07-E09 待确认。
风险门禁：未复检前禁止放行结论。
动作门禁：系统写入需授权人确认。
输出门禁：行动项含责任方、依据、验收标准。
一、统一事件包
表格
字段	内容
事件编号	EVT-20260619-001
Owner	生产部
产线/设备	三号包装线贴标机
状态	处理中
首次记录时间	2026-06-19 01:27
优先级	P1（可能非计划停线）
已确认事实
表格
证据ID	来源类型	摘录	可信度
E01	用户输入	三号包装线贴标机频繁漏贴	已确认
E02	用户输入	可能非计划停机	已确认
E03	用户输入	涉及部门：生产部、维修、质量、工程、安全、PMC、仓库/采购	已确认
合理推断
表格
证据ID	推断内容	置信度
E04	漏贴产品可能需隔离复检	中
E05	停机将影响排产与交期	高
E06	跨部门需明确反馈时限与系统回执	高
待确认信息
表格
证据ID	缺失字段	阻塞点
E07	设备编号、资产层级	无法精准派工
E08	漏贴频次、涉及批次/SKU	无法量化损失与隔离范围
E09	公司系统部署情况（MES/CMMS/QMS是否可用）	决定正式链路可行性
二、分层流转说明
分层架构
┌───────────────────────────────────────────────────────────┐
│               统一事件包（沟通母体）                         │
│          生产部 Owner · 全部部门围绕此母体协同               │
└───────────────────────────────────────────────────────────┘
│
┌─────────────────┴─────────────────┐
▼                                   ▼
通知层（不替代正式留痕）              正式业务系统链路
· 企业微信/飞书/钉钉/邮件            · MES → 生产状态、停线时间、少产
· 仅负责：通知、催办、               · CMMS → 维修工单、派工、备件、工时
轻量确认、会议邀约                 · QMS → 质量隔离、复检、放行
· Facebook/个人社媒/个人微信         · EHS → 作业许可、能量隔离、整改
❌ 不合规，不得作为正式             · SAP/ERP → 订单、物料、库存、成本
业务闭环渠道                       · OA → 审批、管理升级
· PMC/APS → 排产、产能、交期调整

渠道边界
表格
渠道	定位	能否作为正式闭环渠道
企业微信/飞书/钉钉/邮件	通知层	❌ 仅通知、催办、轻量确认
Facebook/个人社媒	非企业授权	❌ 不合规
个人微信	非企业授权	❌ 不合规
MES/CMMS/QMS/EHS/SAP/ERP/OA/PMC	正式业务系统	✅ 正式留痕、审批、回执、交付影响
端到端流转
生产部发现漏贴
↓
① 生产部建立统一事件包 → MES记录
↓
② 企业微信/邮件通知协同部门（通知层，非正式留痕）
↓
③ 各部门按职责在正式系统中反馈
├─ 维修 → CMMS 接收派工，反馈到场时间、候选原因、措施、备件
├─ 质量 → QMS 建立隔离/复检申请，反馈隔离范围、复检结论
├─ EHS  → EHS/OA 评估作业许可，反馈许可或豁免
├─ PMC  → PMC/APS 评估交期影响，反馈调产方案
└─ 仓库/采购 → SAP/ERP 回传统计库存、到料时间、替代方案
↓
④ 生产部汇总正式系统回执 + 人工反馈
↓
⑤ 决策恢复窗口或管理升级
↓
⑥ 事件关闭后 → 知识库/SOP 候选条目（需授权人审核后发布）

三、部门反馈合同
表格
部门	必反馈字段	正式系统	缺回执时阻塞项	反馈时限
维修	到场时间、候选原因、措施方案、备件需求、工时	CMMS	不得声称修复完成	60分钟
质量	隔离范围、复检结论、授权人意见	QMS	质量放行完成尚无依据	90分钟
EHS	作业许可需求、安全宣导、能量隔离	EHS/OA	无许可不得开机	按需
PMC	交期影响、调产方案、加班/插单需求	PMC/APS	不得承诺客户交期	120分钟
仓库/采购	备件库存、到料ETA、替代方案	SAP/ERP	不得承诺到货	60分钟
工程	参数/夹具/版本验证结论	PLM/OA	不得确认工艺恢复	120分钟
四、跨部门行动项
表格
责任方	任务	输入依据	验收标准	待确认
生产部	建立统一事件包，通知协同部门	E01-E03	事件包字段完整、通知送达回执	E07设备编号、E08批次
维修	到场检查传感器/机械部件，输出候选原因	事件包+设备编号	CMMS工单含候选原因+措施	E07设备编号
质量	隔离可疑批次，执行复检	事件包+批次信息	QMS隔离单+复检结论	E08批次号、SKU
工程	参数/夹具/版本验证	事件包	工程确认书或变更单	参数历史基线
安全	评估是否需作业许可	事件包	EHS许可或豁免说明	停机检修范围
PMC	评估停线影响，输出排产调整方案	事件包+MES数据	PMC协调单含交期影响	当前排产数据
仓库/采购	确认备件/包材库存与到料时间	事件包+备件清单	SAP/ERP库存回传	E09物料编码
五、正式系统动作卡
动作卡 AC-1：MES 创建事件记录
表格
字段	内容
target_system	MES
action_type	create
payload_summary	三号包装线贴标机漏贴事件，可能非计划停机
evidence_ids	E01, E02, E03
required_fields	产线、设备编号、症状、发起人、时间
missing_fields	设备编号(E07)、批次/SKU(E08)
authorization_required	生产部主管
idempotency_key	EVT-20260619-001
preconditions	事件包草稿完成、必填字段齐全
post_submit_verification	MES记录号返回、状态为"处理中"
channel_boundary	正式业务记录层
动作卡 AC-2：企业微信/飞书/钉钉 通知
表格
字段	内容
target_system	企业微信/飞书/钉钉
action_type	notify
payload_summary	三号包装线贴标机漏贴，请各部门在规定时限内反馈
evidence_ids	E01-E03
required_fields	接收人列表、反馈截止时间、事件包链接
missing_fields	接收人群组、反馈时限
authorization_required	否（通知层）
idempotency_key	NOTIFY-20260619-001
preconditions	MES事件记录创建完成
post_submit_verification	已读/送达回执
channel_boundary	通知层——同步完成尚无依据，以正式系统回执为准
动作卡 AC-3：CMMS 维修派工
表格
字段	内容
target_system	CMMS
action_type	create
payload_summary	贴标机检查派工，需备件清单
evidence_ids	E01, E07
required_fields	资产编号、故障现象、优先级、预计工时
missing_fields	设备编号(E07)、备件编码
authorization_required	维修主管
idempotency_key	CMMS-WO-20260619-001
preconditions	设备编号确认、维修到场评估完成
post_submit_verification	CMMS工单号返回
channel_boundary	正式业务记录层
动作卡 AC-4：QMS 质量隔离
表格
字段	内容
target_system	QMS
action_type	create
payload_summary	可疑批次隔离申请，待复检
evidence_ids	E01, E08
required_fields	批次号、隔离数量、隔离原因
missing_fields	批次号(E08)、SKU、数量
authorization_required	质量负责人
idempotency_key	QMS-ISO-20260619-001
preconditions	质量人员到场评估、批次号确认
post_submit_verification	QMS隔离单号返回——质量放行完成尚无依据
动作卡 AC-5：PMC/APS 排产调整
表格
字段	内容
target_system	PMC/APS
action_type	update
payload_summary	根据停线影响调整排产
evidence_ids	E01, E05
required_fields	受影响SKU、计划产量、调整方案
missing_fields	当前排产数据、客户交期
authorization_required	PMC主管
idempotency_key	PMC-SCH-20260619-001
preconditions	维修确认停机时间窗口
post_submit_verification	APS排产单号返回
动作卡 AC-6：SAP/ERP 备件库存查询
表格
字段	内容
target_system	SAP/ERP
action_type	query
payload_summary	查询贴标机备件/包材库存
evidence_ids	E01, E09
required_fields	物料编码、库存数量、到料时间
missing_fields	物料编码(E09)、备件清单
authorization_required	仓库主管
idempotency_key	SAP-INV-20260619-001
preconditions	维修提供备件清单
post_submit_verification	SAP库存查询结果返回
六、风险边界
表格
风险项	边界	不可越过条件
质量放行	未复检合格前不得出货	质量放行完成尚无依据，须质量负责人签字
安全许可	停机检修需EHS许可或豁免	无许可不得开机
客户承诺	PMC承诺交期前须确认产能与物料	无SAP/ERP数据不得承诺
系统写入	未真实调用工具不得声称写入完成	同步完成尚无依据，须工具回执
根因确定	未经验证不得写最终根因	须维修试运行证据
渠道合规	Facebook/个人社媒/个人微信不得用于正式业务	仅通知层可用企业IM
生产恢复	未通过试运行与复检不得声称恢复	生产恢复完成尚无依据
七、关闭门禁
表格
门禁项	检查内容	未满足时状态
维修验收	CMMS含试运行记录与验收结论	处理中
质量复检	QMS含复检合格与放行授权	处理中——质量放行完成尚无依据
EHS许可	EHS/OA含许可或豁免说明	处理中
PMC交期	PMC/APS含排产调整方案与交期确认	处理中
系统回执	MES/CMMS/QMS/SAP均返回记录号	处理中——同步完成尚无依据
生产部汇总	事件包状态更新为"关闭"	处理中——关闭完成尚无依据

任一门禁未满足，事件状态保持"处理中"或"待确认"，关闭完成尚无依据。

八、下一次同步
表格
轮次	时间	责任人	同步内容
第1次	30分钟内	生产部	事件包创建完成，通知各部门
第2次	60分钟内	生产部	汇总维修/仓库初步反馈
第3次	90分钟内	生产部	汇总质量复检进展
第4次	120分钟内	生产部	汇总全部系统回执，决策恢复窗口或管理升级
第5次	事件关闭后	生产部	复盘纪要、知识库候选条目
九、可复制通知消息模板
【事件通知】三号包装线贴标机漏贴 EVT-20260619-001

各位同事，三号包装线贴标机频繁漏贴，存在非计划停机风险。
生产部已建立统一事件包，请各部门在以下时限内通过正式系统反馈：

🔧 维修 → CMMS派工：60分钟内反馈到场时间、候选原因、措施
🔍 质量 → QMS隔离：90分钟内反馈隔离范围、复检结论
⚠️  EHS → EHS/OA：按需反馈作业许可评估
📊 PMC → PMC/APS：120分钟内反馈交期影响、调产方案
🏪 仓库/采购 → SAP/ERP：60分钟内反馈备件库存、到料ETA

⚠️ 本消息为通知层，正式留痕以MES/CMMS/QMS/EHS/SAP/OA/PMC系统回执为准。