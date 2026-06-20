# 提交后 24 小时证据采集 SOP

目标：把专家榜“能运行、够稳定、可落地、合规安全”的证据一次性补齐。

## 0. 提交前

1. 运行包体自检：

```bash
python submissions/OCAS-skill/industrial-cross-department-collaboration/scripts/validate_package.py
```

2. 确认 ZIP 路径：

```text
submissions/OCAS-skill/industrial-cross-department-collaboration.zip
```

3. 确认作品名称：

```text
industrial-cross-department-collaboration
```

## 1. 赛题页提交

官方赛题页：https://challenge.xfyun.cn/topic/info?type=OCAS-skill

必须从赛题页“作品提交”上传 ZIP，不要直接从 SkillHub 上传。

前端提交字段已核对：

- `contestFlag`：`OCAS-skill`
- `skillName`：页面中填写的作品名称，必须为 `industrial-cross-department-collaboration`
- `fileUrl`：ZIP 上传后平台返回的文件地址

不要把中文展示名填到 `skillName` 位置；否则可能与 `SKILL.md` frontmatter 的 `name` 不一致。

截图：

- 赛题页报名/登录状态。
- 上传 ZIP 前的作品名称输入。
- 上传成功提示。

## 2. SkillHub 审核

入口：https://skill.xfyun.cn/dashboard/skills

截图：

- 我的技能列表。
- 审核中状态。
- 审核通过状态。
- 作品详情页。
- 初始收藏量、下载量。

## 3. AstronClaw 实测样例

优先跑 `tests/rubric_evidence_matrix.csv` 中 `screenshot_priority=required` 的样例：

| 编号 | 用途 | 文件 |
| --- | --- | --- |
| T01 | 设备维修 + 质量复检 | `tests/test_cases.json` |
| T06 | 质量隔离 + 销售交付压力 | `tests/test_cases.json` |
| T11 | 带电检修拒绝越权 | `tests/test_cases.json` |
| T21 | 多系统动作卡 + 准备度门禁 | `tests/test_cases.json` |
| T24 | 已有系统记录状态更新边界 | `tests/test_cases.json` |
| T25 | 候选诊断矩阵 + 验证计划 | `tests/test_cases.json` |
| T27 | 信号校准 + 阈值缺失边界 | `tests/test_cases.json` |
| T28 | 外部系统失败 + 降级完成 | `tests/test_cases.json` |
| T29 | 专家榜保守自评边界 | `tests/test_cases.json` |
| T30 | 提示注入隔离 | `tests/test_cases.json` |
| T33 | 冲突记录不二选一 | `tests/test_cases.json` |
| T34 | 现场执行包 | `tests/test_cases.json` |
| T35 | 关闭系统记录数据质量门禁 | `tests/test_cases.json` |

每个样例截图必须包含：

- 输入文本。
- Skill 输出。
- 场景分类。
- 已确认事实/合理推断/待确认信息。
- 跨部门待办或行动项。
- 风险与合规提示。
- 动作准备度或授权状态。

## 4. 评分记录

把实际输出保存为：

```text
tests/run_outputs/T01.md
tests/run_outputs/T06.md
tests/run_outputs/T11.md
tests/run_outputs/T21.md
tests/run_outputs/T24.md
tests/run_outputs/T25.md
tests/run_outputs/T27.md
tests/run_outputs/T28.md
tests/run_outputs/T29.md
tests/run_outputs/T30.md
tests/run_outputs/T33.md
tests/run_outputs/T34.md
tests/run_outputs/T35.md
```

然后运行：

```bash
python scripts/score_run.py --outputs tests/run_outputs --report tests/run_score_report.csv
```

导出：

- `tests/run_score_report.csv`
- 评分脚本终端截图
- 5 个输出文件截图
- `tests/rubric_evidence_matrix.csv` 对应关系截图
- `tests/run_record_template.csv` 中成功率、耗时、错误类型、重试记录

## 5. 脱敏证据

运行示例：

```bash
python scripts/redact_input.py --text "张工 13800138000 邮箱 test@example.com 身份证 110101199003071234 反馈贴标机异常"
```

截图要求：

- 脱敏前输入。
- 脱敏后输出。
- 说明真实数据进入公开材料前必须先脱敏。

## 6. 用户反馈

至少收集 3 条真实反馈：

| 角色 | 试用场景 | 反馈点 | 是否可公开 |
| --- | --- | --- | --- |
| 设备/维修 | 故障记录转系统记录 | 责任方和验收标准是否清楚 | 是/否 |
| 质量 | 批次异常转复检待办 | 是否避免越权放行 | 是/否 |
| 生产/数字化 | 班组交接转周报 | 是否减少重复整理 | 是/否 |

反馈不要包含手机号、客户名、个人身份信息或未脱敏现场记录。

## 7. 更新评审材料

把以下证据补入 PPT/PDF：

- 官方提交截图。
- SkillHub 审核截图。
- 高优先级实测输出截图。
- 专家评分证据矩阵。
- 测试评分表。
- 脱敏脚本截图。
- 用户反馈。
- SkillHub 作品页链接。
