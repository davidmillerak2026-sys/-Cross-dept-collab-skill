# AstronClaw 固定模型测试问题库

范围：只记录 AstronClaw 当前可选的固定模型，不记录 Auto。

目标：先连续跑测试并归档问题，最后统一优化 Skill 和提示协议，使所有固定模型在关键场景中稳定通过。

## 问题分类

| 分类 | 说明 |
| --- | --- |
| A 格式缺漏 | 缺少指定栏目、缺少 `输入依据`、缺少 `关闭门禁`、栏目名偏移 |
| B 禁词/越权状态 | 出现无依据的 `已同步`、`已关闭`、`已恢复`、`质量已放行`、`闭环门禁` 等 |
| C 过程话术 | 输出 `Let me`、`I need`、`previous output`、`用户再次`、`我已完整读取`、评分/规则复述 |
| D 系统边界 | 把企业微信/邮件/Facebook/个人社媒误写成正式闭环或系统回执 |
| E 业务缺漏 | 生产部 Owner、维修/质量/PMC/仓库/采购/EHS/工程责任链缺失 |
| F 安全合规 | 对危险操作、刷量、提示注入、token/隐私处理不稳 |
| G 页面/运行稳定 | AstronClaw 页面卡顿、模型响应超时、无法完整截图或复制 |

## T39 固定模型门禁结果

| 模型 | 当前结论 | 分数 | 问题分类 | 具体问题 | 证据 |
| --- | --- | ---: | --- | --- | --- |
| GLM5.1 | 通过 | 100 | - | exact `关闭门禁`，无硬禁词，结构稳定 | `outputs/GLM5.1/T39_hardban.md` |
| MiniMax2.5 | 通过 | 100 | - | exact `关闭门禁`，无硬禁词，结构稳定 | `outputs/MiniMax2.5/T39_hardban.md` |
| Kimi2.6 | 条件通过 | 100 | C | 评分通过，但开头有过程话术，评审截图观感弱 | `outputs/Kimi2.6/T39_hardban.md` |
| Spark-X2-Flash | 通过但需加固 | 92 / 100 | A / C | clean 会话缺显式 `输入依据`；部分输出带 `运行轨迹`；早期 rerun 曾出现否定语境里的完成态字样 | `outputs/Spark-X2-Flash_clean/T39_user_pasted_clean_session.md` |
| Qwen3.6 | 不通过，需统一优化后重测 | 40 | B / C | 输出英文过程话术；出现 `已关闭`、`质量已放行`、`已恢复`、`已同步`、`闭环门禁` | `outputs/Qwen3.6/T39_hardban.md` |
| DeepSeek-v4-pro | 不通过，需统一优化后重测 | 40 / 16 | A / B / C | 上下文会话输出 `Let me` / `previous output` 并复述禁词；clean 会话仍用 `闭环门禁`，缺 exact `关闭门禁`，出现 `我已完整读取` | `outputs/DeepSeek-v4-pro/`, `outputs/DeepSeek-v4-pro_clean/` |

## 页面/运行稳定问题

| 时间 | 分类 | 现象 | 影响 | 处置 |
| --- | --- | --- | --- | --- |
| 2026-06-20 11:20 | G | Spark-X2-Flash 测试页在发送/生成后，Chrome 控制通道多次读取 DOM、截图和关闭标签超时 | 影响自动截图和批量连续测试，不代表 Skill 内容失败 | 后续每个模型尽量新开干净标签；把可复制输出另存为证据；最终测试时优先保留人工可见页面截图 |
| 2026-06-20 11:36 | G | Qwen3.6 clean rerun 输入成功、发送成功、生成开始后，等待和最终状态读取连续超时 | 无法自动确认最终分数；初始尾部已看到输出较长、表格较多，疑似长输出渲染拖慢页面 | 记录为运行稳定问题；后续统一优化时需要限制输出长度/表格数量，并分段控制截图证据 |
| 2026-06-20 11:50 | G | Qwen3.6 short evidence rerun 新页仍接入前一生成会话，输入框保留新 prompt 且页面显示 `停止生成`；轻量状态检查仍超时 | 会话污染导致后续新测试不干净，且无法自动采集结果 | 后续需要在 AstronClaw 手动/自动明确点击新建任务并确认无 `停止生成` 后再开始；最终测试协议要增加“会话清洁检查” |
| 2026-06-20 12:34 | G | 使用显式随机 `session_id` 打开页面看似可获得空白会话，但提交后服务端返回 `Session not found` | 随机 `session_id` 不是有效测试协议；必须由 AstronClaw 页面“新建任务”创建真实 session | Chrome GUI state probe |
| 2026-06-20 12:40 | G | 点击 AstronClaw 页面 `新建任务` 可生成真实有效 session，例如 `20d992a2-7336-4bc3-8e5a-c71ce61741f7`；检查：输入框为空、无 `停止生成`、无旧输出 | 后续 GUI 测试协议：先点击 `新建任务`，确认 URL 出现服务端 session_id，再输入测试 prompt | Chrome GUI state probe |
| 2026-06-20 12:58 | G | Qwen3.6 no-forbidden-literals rerun 使用页面 `新建任务` 生成真实 session `378079fb-38e0-4b8c-96cd-11de3799fc4a`，短提示成功写入并发送，页面进入 `停止生成`；随后多次 60-90 秒文本/可见控件读取均超时 | 暂无法稳定采集最终输出和截图；这更像 Qwen3.6 + 当前页面渲染/输出长度的运行稳定问题，不宜直接等同内容失败 | 记录为 GUI 采集风险；后续统一优化时进一步压缩输出、减少表格、关闭过程段，并重测 Qwen3.6 |
| 2026-06-20 13:08 | G | DeepSeek-v4-pro ultra-short clean prompt rerun 使用页面 `新建任务` 生成真实 session `ad197486-5a17-496f-ab91-943b6fcb51d2`，模型切换成功；发送流程后状态读取 70-90 秒超时 | 无法确认最终内容；提示已压缩到 1200 字以内仍出现页面采集困难，说明 GUI 批量测试效率很低 | 先记录为运行稳定/采集风险；后续用更短的一问一答 smoke prompt 或人工复制方式补证据 |

## 新增真实 GUI 测试结果

| 时间 | 模型 | 用例 | 会话方式 | 得分 | 结论 | 问题分类 | 具体问题 | 证据 |
| --- | --- | --- | --- | ---: | --- | --- | --- | --- |
| 2026-06-20 12:45 | Qwen3.6 | T39 short evidence | 页面 `新建任务` 生成真实 session `20d992a2-7336-4bc3-8e5a-c71ce61741f7` | 16 | 不通过，但比旧上下文 run 更接近可修复 | B / C / A | 没有 `闭环门禁`，但在否定句中写出 `已恢复`、`质量已放行`、`已关闭`；开头有 `根据 skill 和模板，我现在输出...`；缺显式 `责任方` / `输入依据` / `验收标准` 关键词 | `outputs/Qwen3.6_valid_short/T39_short.md`, `Qwen3.6_valid_short_T39_score_report.csv` |
| 2026-06-20 12:58 | Qwen3.6 | T39 short no-forbidden-literals | 页面 `新建任务` 生成真实 session `378079fb-38e0-4b8c-96cd-11de3799fc4a` | N/A | 生成/采集不稳定，先归入运行稳定问题 | G | 模型显示 Qwen3.6，输入成功，发送成功，进入生成；后续页面读取、正文快照、可见控件检查均超时，未能取得最终文本 | `T39_short_no_forbidden_literals_prompt.md` |
| 2026-06-20 13:08 | DeepSeek-v4-pro | T39 ultra-short clean prompt | 页面 `新建任务` 生成真实 session `ad197486-5a17-496f-ab91-943b6fcb51d2` | N/A | 发送后采集不稳定，需补证据 | G | 模型切换成功；使用不含完成态禁词字面量的 1200 字以内提示；发送流程后页面读取超时，未能取得最终文本 | `T39_ultra_short_clean_prompt.md` |
| 2026-06-20 16:00 | Spark-X2-Flash | G01 predictive maintenance natural prompt | 人工复制 GUI 输出 | 75 | 不通过但业务结构完整 | C | 生产部 Owner、事实/待确认、跨部门、系统、授权边界和预测性维护语义都命中；问题是输出独立 `运行轨迹` 栏目 | `industrial-cross-department-collaboration/tests/gui_retest_outputs/Spark-X2-Flash/G01.md` |
| 2026-06-20 16:05 | GLM5.1 | G01 predictive maintenance natural prompt | 人工复制 GUI 输出 | 75 | 不通过但业务结构完整 | C | 结构完整，给出了停机检查建议、信号校准、候选诊断、系统动作卡和部门流转；问题同样是输出独立 `运行轨迹` 栏目 | `industrial-cross-department-collaboration/tests/gui_retest_outputs/GLM5.1/G01.md` |
| 2026-06-20 16:10 | MiniMax2.5 | G01 predictive maintenance natural prompt | 人工复制 GUI 输出 | 75 | 不通过但业务结构完整 | C | 结构更短但命中生产、维修、质量、PMC、MES/CMMS/QMS 和停机检查建议；问题同样是输出独立 `运行轨迹` 栏目 | `industrial-cross-department-collaboration/tests/gui_retest_outputs/MiniMax2.5/G01.md` |
| 2026-06-20 16:20 | Kimi2.6 | G01 predictive maintenance natural prompt | 人工复制 GUI 输出 | 75 | 不通过但业务结构完整 | C | 命中管理升级、系统动作卡、质量/维修/工程/PMC/仓库协同；问题同样是输出独立 `运行轨迹` 栏目，且开头有轻微过程话术 | `industrial-cross-department-collaboration/tests/gui_retest_outputs/Kimi2.6/G01.md` |
| 2026-06-20 16:30 | Qwen3.6 | G01 predictive maintenance natural prompt | 人工复制 GUI 输出 | 75 | 不通过但业务结构完整 | C | 命中生产/质量/PMC、管理升级、部门流转和系统动作卡；问题同样是输出独立 `运行轨迹` 栏目，末尾还有“如需我协助...”聊天式收尾 | `industrial-cross-department-collaboration/tests/gui_retest_outputs/Qwen3.6/G01.md` |
| 2026-06-20 16:35 | DeepSeek-v4-pro | G01 predictive maintenance natural prompt | 人工复制 GUI 输出 | 50 | 不通过但业务结构完整 | A / C | 业务链路最完整之一，含系统动作卡、现场执行编排和关闭条件；但输出旧词 `闭环门禁`，并继续输出独立 `运行轨迹` 栏目 | `industrial-cross-department-collaboration/tests/gui_retest_outputs/DeepSeek-v4-pro/G01.md` |

## G01 横向共性观察

| 时间 | 覆盖模型 | 结论 | 优先级 | 后续处理 |
| --- | --- | --- | --- | --- |
| 2026-06-20 16:35 | Spark-X2-Flash, GLM5.1, MiniMax2.5, Kimi2.6, Qwen3.6, DeepSeek-v4-pro | 六个模型均能理解预测性维护/质量风险/PMC协同，但全部输出独立 `运行轨迹` 栏目；DeepSeek 额外输出旧词 `闭环门禁` | P0 | 暂停进入 G02，先统一加固 Skill 输出协议：移除/改写可被模型复述的过程段字面量，强化只输出业务交付物；复测 G01 后再继续矩阵 |

## 静态扫描问题

| 时间 | 分类 | 发现 | 影响 | 证据 |
| --- | --- | --- | --- | --- |
| 2026-06-20 11:45 | A / B | `SKILL.md` 主规则已要求栏目名写 `关闭门禁`，但 README、企业流转测试包、示例、参考材料、评分脚本仍大量出现 `闭环门禁` | 模型会从上下文/示例学习到错误栏目名，DeepSeek clean rerun 已实际输出错误栏目 | `rg -n "闭环门禁" .` |
| 2026-06-20 11:52 | A | 评分口径冲突：`scripts/score_run.py` 的 T39 critical term 是 `关闭门禁`，但 `scripts/score_enterprise_flow.py` 和 S01-S10 材料仍使用 `闭环门禁` | 同一 Skill 在不同测试包中被要求输出两个不同栏目名，导致跨模型稳定性下降 | `scripts/score_run.py`, `scripts/score_enterprise_flow.py` |
| 2026-06-20 11:45 | B | 负例、示例和测试提示中大量出现 `已同步`、`已关闭`、`已恢复生产`、`质量已放行` 等硬禁词 | 某些模型会复述负例或把禁词带入结果，Qwen/DeepSeek 已触发 | `rg -n "已同步|已关闭|已恢复生产|质量已放行" .` |
| 2026-06-20 11:45 | C | `SKILL.md` 允许复杂任务末尾加入 `运行轨迹`，实际 Spark/Qwen 输出中也出现该段 | 对“只看业务结果”的评审截图可能显得像过程说明；需要改成可选或隐藏式业务审计摘要 | `rg -n "运行轨迹" SKILL.md README.md templates examples tests references scripts` |
| 2026-06-20 11:45 | 证据缺口 | 本地 `validate_package.py`、`smoke_test_package.py`、`expert_rubric_gate.py` 均 PASS；但 expert gate 明确提示 AstronClaw evidence filled=0 | 工程包本地满分不等于专家榜实测满分，还必须补平台截图/运行证据 | `scripts/expert_rubric_gate.py` 输出 |
| 2026-06-20 11:56 | 版本不一致 | AstronClaw 本地安装目录 `.openclaw/skills/industrial-cross-department-collaboration/SKILL.md` 与源码包 `submissions/OCAS-skill/.../SKILL.md` hash 不一致；安装版本为 `20260618.092920` | 网页实测可能仍在跑旧 Skill，导致 T39 修复、术语修复、反复述规则未生效；后续模型失败不能全部归因到模型 | `.openclaw/skills/.../.clawhub/origin.json`, `Get-FileHash` |
| 2026-06-20 11:59 | 版本不一致 | 关键文件对比显示：`templates/enterprise_flow_output_contract.md` 源码版与 AstronClaw 安装版 hash 不一致；安装版 `SKILL.md` 仍要求 S01-S10 输出 `闭环门禁`，源码版改为 `关闭门禁` | 真实 AstronClaw 测试需要先更新安装包，否则同一提示在不同模型上会继续受旧模板影响 | `Compare-Object`, `Get-FileHash` |
| 2026-06-20 12:03 | 测试覆盖缺口 | AstronClaw 安装版本地 `validate_package.py` / `smoke_test_package.py` / `expert_rubric_gate.py` 全 PASS，但网页实测仍出现 Qwen/DeepSeek 跨模型问题 | 现有本地门禁没有覆盖“不同模型复述负例、栏目名漂移、长输出卡顿、安装版/源码版不一致” | `.openclaw/skills/.../scripts/*` |
| 2026-06-20 12:06 | 版本不一致 | 安装版 vs 源码版全量对比：11 个文件 hash_diff，1 个安装元数据 extra_inst。差异集中在 `SKILL.md`、部门沟通/企业流转模板、集成合同、办公消息模板和校验脚本 | AstronClaw 当前安装版缺少后续增强，必须纳入后续统一优化/重装/发布流程 | 全量 `Get-FileHash` 对比 |
| 2026-06-20 12:10 | B / C | 禁词/负例复述风险统计：`tests/astronclaw_stability_stress_prompt_pack.md` 命中 46 次，`examples/06_expert_screenshot_outputs.md` 40 次，`tests/astronclaw_enterprise_flow_prompt_pack.md` 32 次 | 某些模型会把“禁止出现”的例子直接复述到答案里，造成硬性扣分 | forbidden-term count scan |
| 2026-06-20 13:35 | 已修复 / A / B | 源码包已全量清除 `闭环门禁`，统一使用 `关闭门禁`；企业流转评分和提示包同步更新 | 消除 DeepSeek/Qwen 从模板学习错误栏目名的主要来源 | `rg -n "闭环门禁" .` 无命中 |
| 2026-06-20 13:40 | 已修复 / C | `SKILL.md` 已将独立 `运行轨迹` 改为默认不输出；只有用户要求审计/调试/证据时才输出不超过 6 行的 `业务审计摘要`；README 和复杂示例同步改口径 | 降低评审截图中出现模型过程话术、规则复述和自检段落的风险 | `SKILL.md`, `README.md`, `examples/04_complex_agent_workflow.md` |
| 2026-06-20 13:45 | 已增强 / D | 已加入 AstronClaw 多端协作接入卡：企业微信/企微、飞书、钉钉、微信、邮件为通知/催办/轻量确认入口；QQ/微博/Facebook 仅作为企业授权外联连接器；正式关闭仍以 MES/CMMS/QMS/EHS/SAP/ERP/OA/PMC 回执为准 | 回答用户“多端推送”诉求，同时避免把聊天渠道误写成正式闭环 | `SKILL.md`, `templates/enterprise_flow_output_contract.md`, `templates/office_message_templates.md` |
| 2026-06-20 13:50 | 已验证 / 本地门禁 | 多端协作和术语修复后，本地 `validate_package.py`、`smoke_test_package.py`、`expert_rubric_gate.py` 均 PASS；`champion_acceptance_gate.py` 仍提示缺 AstronClaw 真实证据和试用反馈 | 源码包可进入 republish/reinstall；冠军状态仍需平台实测证明 | local command output |

## 后续测试队列

| 优先级 | 测试包 | 模型 | 用例 |
| ---: | --- | --- | --- |
| 1 | T39 clean rerun | Qwen3.6, DeepSeek-v4-pro, Kimi2.6, Spark-X2-Flash | 验证失败是否由会话污染导致 |
| 2 | 代表场景包 | GLM5.1, MiniMax2.5, Spark-X2-Flash, Kimi2.6 | T01, T06, T11, T30, T31, T36, T39 |
| 3 | 失败模型代表场景 | Qwen3.6, DeepSeek-v4-pro | 只跑 T01, T11, T30, T36, T39，重点抓共性失败 |
| 4 | 稳定压力 | 所有固定模型 | 异常输入、提示注入、缺字段、危险操作、刷量请求 |

## CLI 批量测试可行性

| 时间 | 结论 | 证据 | 影响 |
| --- | --- | --- | --- |
| 2026-06-20 12:28 | 未发现 AstronClaw 云端对话/已部署 Bot 的官方 CLI 批量测试入口 | 本机 `Get-Command astronclaw, astron-claw, claw, xfyun` 无结果；npm `astronclaw` / `astron-claw` / `@xfyun/astron-claw` 均 404；官方 AstronClaw 文档描述为云端一键部署和浏览器/渠道使用 | 后续真实证据采集仍以 AstronClaw GUI 为准 |
| 2026-06-20 12:20 | `npx clawhub` 存在，但定位是 Skill 注册表/安装/发布/扫描工具，不是运行 Skill 的批量测试器 | `npx clawhub --help` | 可用于安装、更新、发布和 scan，不适合直接跑多模型输出 |
| 2026-06-20 12:20 | `npx openclaw` 存在，支持 `openclaw agent --local --model ... --message ... --json`，也支持 `openclaw infer model run --model ... --prompt ...` | `npx openclaw agent --help`; `npx openclaw infer model run --help` | 可作为本地批量回归通道 |
| 2026-06-20 12:20 | Skill 在 OpenClaw CLI 中为 Ready、Visible to model、Available as command | `npx openclaw skills info industrial-cross-department-collaboration` | 适合用 `openclaw agent` 做带 Skill 的本地批量测试 |
| 2026-06-20 12:20 | OpenClaw CLI 的模型池是本地 provider 配置，不等同于 AstronClaw 网页订阅里的固定模型池 | `npx openclaw infer model providers`; `npx openclaw models status` | CLI 结果可作预筛，最终仍需 AstronClaw 网页固定模型截图确认 |
| 2026-06-20 12:20 | 本地 `qwen/glm-5` 最小 CLI 运行触发 401，提示 provider token 失效 | `npx openclaw agent --local --model qwen/glm-5 ...` | 需要更新本地 provider auth 后才能大规模跑 CLI |
| 2026-06-20 14:10 | ClawHub dry-run 成功；真实发布暂未完成 | `npx clawhub publish . --slug industrial-cross-department-collaboration --version 20260620.1350.0 --dry-run --json --registry https://skill.xfyun.cn` 返回 `would-publish`，fileCount=105，最终 fingerprint=`99f10132649651912c6404c94187d58a64429b5eb9e250aba65fa99b510eb696`；CLI `whoami` 未登录，网页上传控件需要原生文件选择器，自动接管不稳定 | champion-20 包体已可发布；需用户完成 ClawHub login 或网页上传 zip 后，再重测 AstronClaw 固定模型 |

## 统一优化候选，不在测试阶段立即修改

| 候选优化 | 关联问题 |
| --- | --- |
| 在 Skill 顶部加入“只输出业务结果，不复述规则、不写自检过程、不引用上一轮输出”的强制条款 | C，已部分完成，需 GUI 复测 |
| 把所有模板中的“闭环门禁”统一替换为“关闭门禁”，测试材料也同步替换，避免模型学到错误栏目名 | A / B，已完成，需 republish 后复测 |
| 对禁词做“状态词替代表”，例如 `关闭完成尚无依据`、`同步完成尚无依据`、`生产恢复完成尚无依据`、`质量放行完成尚无依据` | B |
| 每个行动项表强制包含 `责任方 / 输入依据 / 验收标准 / 待确认` | A / E |
| 对平台/渠道分层增加硬规则：企业 IM/邮件只通知，Facebook/个人社媒/个人微信不得进入正式闭环 | D，已扩展为 AstronClaw 多端协作接入卡，需 GUI 复测 |
