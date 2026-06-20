# AstronClaw 真实运行证据采集状态

更新时间：2026-06-18

## 目标

按平台真实调用证据顺序执行：

1. T01-T39 基础稳定性。
2. S01-S10 企业部门协同。
3. ST01-ST12 异常输入压力。

## 当前可验证事实

- OCAS 赛题页 `https://challenge.xfyun.cn/topic/info?type=OCAS-skill&option=tjjg` 可打开作品提交区。
- 作品提交区当前显示文件选择框和提交按钮。
- 当前“团队提交”表格显示“暂无数据”，即没有已提交作品记录。
- SkillHub `https://skill.xfyun.cn/dashboard/skills` 当前显示“还没有技能”。
- 因此当前没有已审核发布的 SkillHub 作品，也没有可在 AstronClaw 选择调用的 `industrial-cross-department-collaboration`。
- WFC 项目页 `https://wfc.bd-iiot.com/project/cmq6lbb9x00bx1l6pxll7voae` 是 Workflow Canvas 工程画布，不是 OCAS SkillHub/AstronClaw 的作品运行页，不能作为本赛题真实运行证据。
- 2026-06-18 追加：已接管 OCAS 提交页并检测到 1 个文件输入控件和 1 个提交按钮；选择 ZIP 时被 Chrome 扩展本地文件访问权限拦截，文件未能绑定到上传框。
- 2026-06-18 15:51:44 追加：重新开启文件访问权限后，OCAS 提交成功，团队提交表出现记录 `ID 214`，提交文件名 `industrial-cross-department-collaboration`，提交者 `Ryn`。
- 点击审核状态“查看”后进入 SkillHub 预览页：`https://skill.xfyun.cn/space/global/industrial-cross-department-collaboration`。
- SkillHub 当前状态显示 `正常 / 公开 / 审核中`，页面提示“当前正在预览待审核版本”“审核通过前仅本人可见”，因此仍不能当作审核通过或公开发布证据。
- 2026-06-18 16:05 追加：本地包已改成 `2026.06.18-champion-17`，口径从“系统记录协同助理”改为“工业现场跨部门协同工作 Skill”，系统记录仅作为必要时的下游承载物。
- 2026-06-18 17:09 追加：本地包已改成 `2026.06.18-champion-18`，修复试用反馈评分报告 CSV 公式注入风险，补充对应烟测回归。
- 2026-06-18 16:07 追加：已在 OCAS 提交页重新选择新 ZIP，页面弹出“确认提交作品？”二次确认；自动点击普通按钮、DOM 节点、坐标、回车和双击均未使弹窗关闭。当前需要人工在 Chrome 弹窗右下角点击蓝色“提交”，完成新版 ZIP 重新提交。

## 已保存阻塞截图

- OCAS 提交区暂无数据：`submission_materials/platform_screenshots/OCAS_submit_no_records_20260618.png`
- SkillHub 我的技能为空：`submission_materials/platform_screenshots/SkillHub_no_skills_20260618.png`
- OCAS 提交成功记录：`submission_materials/platform_screenshots/OCAS_submit_success_ID214_20260618.png`
- SkillHub 审核中预览页：`submission_materials/platform_screenshots/SkillHub_pending_review_20260618.png`

## 当前结论

T01-T39、S01-S10、ST01-ST12 尚未开始真实 AstronClaw 运行，不能填写为通过，也不能声称已完成实测。

阻塞项不是本地包体，而是平台证据前置条件：

- OCAS 赛题页上传已完成。
- 需要等待 SkillHub 审核通过并出现真正可公开访问/可调用的作品页。
- 需要 AstronClaw 能选择并调用该 Skill。
- 当前 SkillHub 仍为审核中，不能开始 AstronClaw T/S/ST 证据采集。

## 待提交包

- 文件：`C:\Users\ryan hui\Documents\2026赛事搜集\submissions\OCAS-skill\industrial-cross-department-collaboration.zip`
- 版本：`2026.06.18-champion-18`
- 大小：`268,862 bytes`
- 文件数：`103`
- SHA256：`D6EA22161851DE7B81F63AF281C1A3965D95A82BE802525F6ED3753AF294872B`
- 作品名称：`industrial-cross-department-collaboration`

## 下一步动作

1. 定期刷新 SkillHub 预览页或 OCAS 审核状态。
2. 审核通过后保存审核通过截图和真正公开页截图。
3. 更新 `tests/platform_submission_evidence_template.json` 的 `skillhub_approval_screenshot`、`skillhub_public_page_screenshot` 和 `skillhub_public_url`。
4. 进入 AstronClaw，按 `tests/skillhub_prompt_pack.md` 跑 T01-T39。
5. 按 `tests/astronclaw_enterprise_flow_prompt_pack.md` 跑 S01-S10。
6. 按 `tests/astronclaw_stability_stress_prompt_pack.md` 跑 ST01-ST12。

## 证据记录要求

- T01-T39 写入 `tests/run_record_template.csv`。
- S01-S10 写入 `tests/run_record_enterprise_flow_template.csv`。
- ST01-ST12 写入 `tests/run_record_stability_stress_template.csv`。
- 截图或输出文件必须是真实平台输出，路径必须存在。
- 失败记录不能删除，只能追加复跑记录。
- 全部跑完后执行 `python scripts/expert_rubric_gate.py --require-astronclaw` 和 `python scripts/champion_acceptance_gate.py`。
