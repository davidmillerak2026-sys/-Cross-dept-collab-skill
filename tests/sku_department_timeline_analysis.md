# SKU Department Timeline Analysis

- source_data: `examples/data/sku_quality_coordination_timeline.csv`
- event_id: `20260617-SKU-A17-QA`
- timeline_window: `2026-06-17 14:12` to `2026-06-17 15:40`
- elapsed_minutes: `88`
- transition_count: `10`
- departments: `Engineering, Management, PMC, Production, Quality, Warehouse`
- formal_systems: `MES, OA, OA + enterprise IM, PLM_ENGINEERING, PMC_APS, QMS, SAP_ERP, SAP_ERP_WMS`
- open_blocker_count: `5`
- late_feedback_count: `0`

## Timeline

| Time | Department | Formal system | Action | State transition | Due | SLA | Receipt | Decision effect |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-06-17 14:12 | Production | MES | open unified event package | `normal_running` -> `production_quality_hold` | 2026-06-17 14:20 | on_track | MES downtime record | starts unified event and stops unsafe shipment assumptions |
| 2026-06-17 14:18 | Quality | QMS | create containment and sampling record | `production_quality_hold` -> `qms_containment_open` | 2026-06-17 15:20 | on_track | QMS isolation record | blocks affected batch from shipment |
| 2026-06-17 14:28 | Quality | QMS | report first sample failure | `qms_containment_open` -> `qms_disposition_pending` | 2026-06-17 15:20 | on_track | QMS retest and disposition | keeps release blocked and triggers rework evaluation |
| 2026-06-17 14:35 | Warehouse | SAP_ERP | confirm released inventory | `qms_disposition_pending` -> `released_stock_available` | 2026-06-17 15:20 | on_track | SAP/ERP stock snapshot | allows partial shipment option only from released batch |
| 2026-06-17 14:38 | Warehouse | SAP_ERP_WMS | hold affected batch | `released_stock_available` -> `warehouse_hold_pending` | 2026-06-17 15:20 | on_track | WMS hold receipt | prevents B20260617-A17-03 from entering picking wave |
| 2026-06-17 14:42 | PMC | PMC_APS | calculate delivery gap and options | `warehouse_hold_pending` -> `pmc_delivery_gap_open` | 2026-06-17 15:40 | on_track | PMC/APS schedule version | creates partial shipment/rework/overtime decision options |
| 2026-06-17 14:48 | Engineering | PLM_ENGINEERING | confirm onsite ETA and validation scope | `pmc_delivery_gap_open` -> `engineering_eta_confirmed` | 2026-06-17 15:20 | on_track | engineering ETA acknowledgement | keeps root cause candidate open until onsite validation |
| 2026-06-17 15:05 | Engineering | PLM_ENGINEERING | start fixture and barcode parameter validation | `engineering_eta_confirmed` -> `engineering_validation_in_progress` | 2026-06-17 15:35 | on_track | trial validation record | feeds QMS rework and PMC recovery decision |
| 2026-06-17 15:20 | Production | OA + enterprise IM | review first feedback and unresolved blockers | `engineering_validation_in_progress` -> `first_sync_blockers_confirmed` | 2026-06-17 15:40 | on_track | OA sync minutes | prepares management decision packet |
| 2026-06-17 15:40 | Management | OA | choose delivery and recovery plan | `first_sync_blockers_confirmed` -> `management_decision_required` | 2026-06-17 15:40 | at_deadline | OA decision record | select hold/partial shipment/rework/overtime path |

## Current Open Blockers

| State | Owner | Required receipt | Escalation owner | Why it matters |
| --- | --- | --- | --- | --- |
| `qms_disposition_pending` | Quality | QMS retest and disposition | quality manager | keeps release blocked and triggers rework evaluation |
| `warehouse_hold_pending` | Warehouse | WMS hold receipt | warehouse supervisor | prevents B20260617-A17-03 from entering picking wave |
| `pmc_delivery_gap_open` | PMC | PMC/APS schedule version | PMC manager | creates partial shipment/rework/overtime decision options |
| `engineering_validation_in_progress` | Engineering | trial validation record | engineering manager | feeds QMS rework and PMC recovery decision |
| `management_decision_required` | Management | OA decision record | plant manager | select hold/partial shipment/rework/overtime path |

## Coordination Interpretation

- Production remains the event owner because it owns the unified event package, sync cadence, MES production impact and OA escalation packet.
- Quality feedback changes the event from production hold to QMS disposition pending; shipment cannot continue from the affected batch until QMS release exists.
- Warehouse feedback separates released inventory from the affected batch, preventing accidental shipment while preserving a partial-shipment option.
- PMC feedback turns the quality issue into delivery options, not a direct customer commitment; customer-facing promises remain gated by authorization.
- Engineering feedback keeps root cause as a candidate until onsite validation and trial records exist.
- Management decision is required because QMS disposition, engineering validation, PMC schedule version and WMS hold/unlock receipts are still formal blockers.

## Guardrail

Do not write 已放行、已发货、已恢复生产 or 已关闭 until QMS, WMS, MES, PMC/APS and OA receipts prove those states.
