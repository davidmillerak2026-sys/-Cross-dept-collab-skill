# 闭环数据质量门禁模板

用于创建、更新、关闭、复盘工业现场跨部门协同事件前的记录质量检查。CMMS/QMS/MES/OA 中的维修、质量或审批记录只是下游系统载体。

## 数据质量检查

| 字段 | 当前值 | 状态 | 影响 |
| --- | --- | --- | --- |
| 资产层级/设备号 |  | complete/missing/conflict |  |
| 症状/故障现象 |  | complete/missing/conflict |  |
| 影响范围/停机影响 |  | complete/missing/conflict |  |
| 时间窗口 |  | complete/missing/conflict |  |
| 候选故障码/原因码 |  | complete/missing/conflict |  |
| 处置措施 |  | complete/missing/conflict |  |
| 工时/班组 |  | complete/missing/conflict |  |
| 备件/物料 |  | complete/missing/conflict |  |
| 试运行/复检结果 |  | complete/missing/conflict |  |
| 附件/证据 |  | complete/missing/conflict |  |
| 授权/回执 |  | complete/missing/conflict |  |

## 关闭状态

- `close_ready`：关键字段完整，验收/复检证据齐全，状态变化有回执。
- `needs_confirmation`：字段基本完整，但仍需确认授权、版本、附件或接收人。
- `not_close_ready`：缺少根因/措施/验收/授权/回执等关键字段。

故障码、原因码和根因未经验证时只能写为候选项。
