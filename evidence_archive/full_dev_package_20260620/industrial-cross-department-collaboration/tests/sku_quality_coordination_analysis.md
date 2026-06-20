# SKU Quality Coordination Analysis

- source_data: `examples/data/sku_quality_coordination_sample.csv`
- event_id: `20260617-SKU-A17-QA`
- sku: `SKU-A17-EDGE-PACK`
- order_id: `SO-20260617-018`
- batch_id: `B20260617-A17-03`
- decision_due_by: `2026-06-17 15:40`
- engineer_eta: `2026-06-17 15:05`
- management_required: `yes`

## Computed KPIs

| KPI | Formula | Value | Coordination meaning |
| --- | --- | --- | --- |
| downtime_loss_units | `150 / 60 * 42` | `105 pcs` | MES production impact for PMC and management escalation |
| current_shipment_gap | `520 - 360` | `160 pcs` | Warehouse can ship released stock only; PMC must manage shortfall |
| post_rework_gap | `520 - 360 - 92` | `68 pcs` | Still estimated until QMS release and engineering validation |
| isolation_rate | `128 / 1200` | `10.7%` | QMS containment severity |
| sample_fail_rate | `18 / 30` | `60.0%` | Quality risk; do not release affected batch without authorization |
| blocked_close_reason_count | `quality + engineering + PMC + warehouse` | `4` | Keep event open until formal receipts exist |

## Department Coordination Map

| Department | Formal system | Must feed back | Production next action |
| --- | --- | --- | --- |
| Quality | QMS | isolation scope, retest result, rework/release authorization, CAPA boundary | keep affected batch on QA HOLD; do not ship unreleased stock |
| PMC | PMC/APS + SAP PP | partial shipment, rework, overtime or customer-commitment options | prepare A/B/C delivery decision before management deadline |
| Warehouse | SAP/ERP/WMS | released-stock quantity, affected-batch hold, picking wave and unlock receipt | ship released batch only; block B20260617-A17-03 until QMS release |
| Engineering | PLM/OA/MES | onsite validation, fixture/parameter finding, trial result and effective boundary | keep candidate cause open until validated; request trial-run evidence |
| Production | MES/OA + enterprise IM | downtime, loss units, sync cadence and decision package | own unified event package and next synchronization |

## Delivery Options

| Option | Ship quantity | Remaining gap | Required authorization |
| --- | --- | --- | --- |
| A. Released stock only | `360 pcs` | `160 pcs` | PMC/customer boundary confirmation |
| B. Released stock + rework | `452 pcs` | `68 pcs` | QMS release + engineering validation + warehouse unlock |
| C. Released stock + rework + overtime | `520 pcs target` | `0 pcs estimated` | production manager, PMC, QMS and warehouse receipts |

## Guardrails

- Do not write 已放行, 已发货, 已恢复生产 or 已关闭 until the matching QMS, WMS, MES, PMC and OA receipts exist.
- Treat rework capacity as estimated until Quality and Engineering confirm it.
- Keep customer commitment wording under PMC or authorized customer-facing owner control.
