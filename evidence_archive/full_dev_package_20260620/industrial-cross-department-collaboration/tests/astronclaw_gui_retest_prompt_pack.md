# AstronClaw GUI Natural Retest Matrix

Use this pack after the reviewed Skill version is approved and installed in AstronClaw. Test fixed models only; do not use Auto. Start every run from AstronClaw `新建任务`, keep the input box clean, paste exactly one short prompt, and save the output under the matching model and case id.

Recommended execution order: keep one scenario fixed, run the same prompt across all six models, then move to the next scenario. Start with G01 on Spark-X2-Flash, GLM5.1, MiniMax2.5, Kimi2.6, Qwen3.6 and DeepSeek-v4-pro before moving to G02.

## Model Axis

Run every case against every fixed model:

- Spark-X2-Flash
- GLM5.1
- MiniMax2.5
- Kimi2.6
- Qwen3.6
- DeepSeek-v4-pro

## Scenario Axis

Each prompt is intentionally short and natural. Do not add rubric headings to the prompt during GUI testing; the Skill should infer the needed cross-department structure by itself.

### G01 Predictive Maintenance Limit

```text
请用 industrial-cross-department-collaboration 处理这个现场情况。三号包装线贴标机这两天漏贴率明显升高，传感器偶尔抖动，维修只说再观察，但生产担心突然停线。请帮生产部判断要不要提前安排停机检查，并拉通质量、维修和PMC。
```

### G02 ICT Test Station Drift

```text
请用 industrial-cross-department-collaboration 处理这个现场情况。ICT测试站今天误判率突然升高，返测后大多又通过，生产怀疑是夹具或探针问题。请帮生产部组织工程、质量、设备和计划一起排查，先不要直接下根因结论。
```

### G03 Changeover And First Article

```text
请用 industrial-cross-department-collaboration 处理这个现场情况。今晚要从SKU A17切到B22，工程参数还没最终确认，质量说首件检验必须提前到场，PMC担心交期。请整理生产部该怎么拉通各部门推进换线。
```

### G04 Electrical Safety Risk

```text
请用 industrial-cross-department-collaboration 处理这个现场情况。巡检发现一台设备电柜附近有焦味和温升，现场有人想先开柜看看，但EHS还没到。请帮生产部判断该怎么处理，并协调安全、维修和计划。
```

### G05 Root Cause Discovery

```text
请用 industrial-cross-department-collaboration 处理这个现场情况。同一条线连续三班出现短暂停机，但每次报警码不一致，班组各说各的原因。请帮生产部整理事实、可能原因、验证动作和跨部门分工。
```

### G06 Material Shortage Delivery Risk

```text
请用 industrial-cross-department-collaboration 处理这个现场情况。关键包材预计晚到4小时，今日订单已经排满，销售一直在催客户交期。请帮生产部协调PMC、采购、仓库和质量，看怎么稳住交付。
```

### G07 Quality Isolation Before Shipment

```text
请用 industrial-cross-department-collaboration 处理这个现场情况。包装外观抽检发现批次混标风险，仓库已经准备出货，质量要求先隔离但生产担心今天交不了。请帮生产部组织质量、仓库、PMC和客服处理。
```

### G08 EHS And Warehouse Conflict

```text
请用 industrial-cross-department-collaboration 处理这个现场情况。仓库临时堆料堵住消防通道，同时也影响生产领料，仓库说马上挪但没有给完成时间。请帮生产部协调EHS、仓库、PMC和班组。
```

### G09 QMS Failure Degraded Collaboration

```text
请用 industrial-cross-department-collaboration 处理这个现场情况。QMS现在登录异常，质检附件暂时传不上去，但生产现场已经等复检结论。请帮生产部先做可执行的协同安排，并说明哪些事情不能算正式完成。
```

### G10 Multi-Platform Feedback Mess

```text
请用 industrial-cross-department-collaboration 处理这个现场情况。维修、质量和PMC都在不同群里反馈，企业微信、飞书和钉钉信息混在一起，QQ里还有供应商回复。请帮生产部把这些反馈整理成一个可追踪的协同流程。
```

## Run Matrix

| Model | G01 | G02 | G03 | G04 | G05 | G06 | G07 | G08 | G09 | G10 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Spark-X2-Flash |  |  |  |  |  |  |  |  |  |  |
| GLM5.1 |  |  |  |  |  |  |  |  |  |  |
| MiniMax2.5 |  |  |  |  |  |  |  |  |  |  |
| Kimi2.6 |  |  |  |  |  |  |  |  |  |  |
| Qwen3.6 |  |  |  |  |  |  |  |  |  |  |
| DeepSeek-v4-pro |  |  |  |  |  |  |  |  |  |  |

## Evidence Naming

Preferred local evidence path outside the upload package:

```text
../submission_materials/astronclaw_real_runs/<date>_gui_matrix/<case_id>/<model>_<case_id>.md
```

Example:

```text
../submission_materials/astronclaw_real_runs/20260620_gui_matrix/G01/Qwen3.6_G01.md
```

After each copied result, run:

```bash
python scripts/score_gui_retest.py --outputs ../submission_materials/astronclaw_real_runs/20260620_gui_matrix/G01 --model Qwen3.6 --report tests/gui_retest_score_report.csv
```

Before making an upload ZIP, keep `tests/gui_retest_outputs/` free of copied model outputs. Failed real outputs can contain words that should not be included in the Skill package.
