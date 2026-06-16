# Demo Output: Unplanned Stop Collaboration

Input:

```text
Line 3 labeler started missing labels at 14:20. The operator changed the label roll but the issue remained. The line has been stopped for 18 minutes. Quality found 32 cartons that need recheck. Maintenance suspects sensor misalignment but has not verified it. Production wants recovery before 15:30.
```

## Event Summary

- event_id: `20260616-L3-labeler-missing-label`
- Production owner: Line 3 shift leader
- Current status: unplanned stop in progress
- Line/SKU/order: Line 3, SKU/order not provided
- Production impact: stopped for 18 minutes; lost output requires MES confirmation
- Quality impact: 32 cartons require recheck
- Safety impact: unknown until maintenance confirms whether guard opening, electrical work or energy isolation is needed
- Next sync time: 15 minutes after first notification, or immediately if safety/quality risk expands

## Confirmed Facts

| ID | Fact | Source |
| --- | --- | --- |
| F01 | Labeler started missing labels at 14:20 | User input |
| F02 | Label roll was changed and issue remained | User input |
| F03 | Line has been stopped for 18 minutes | User input |
| F04 | Quality found 32 cartons needing recheck | User input |
| F05 | Sensor misalignment is suspected but not verified | User input |
| F06 | Production wants recovery before 15:30 | User input |

## Reasonable Inference

- The event may affect production output and delivery if recovery misses the target window.
- Sensor misalignment is only a candidate cause; do not write it as verified root cause.
- Quality release is blocked until QMS recheck and authorized disposition are complete.

## Missing Information

- SKU, order number and affected batch.
- MES line state, actual downtime start record and estimated lost output.
- Labeler asset ID and CMMS asset hierarchy.
- Whether maintenance work requires lockout, energy isolation or permit.
- QMS isolation range, recheck method and release authority.
- SAP/ERP spare-part and label-roll inventory.
- PMC/APS delivery impact and reschedule decision.

## Department Action Table

| Department | Action | Formal system | Feedback required | Due time | Closure gate |
| --- | --- | --- | --- | --- | --- |
| Production | Open unified event package and record downtime | MES | downtime, lost output, target recovery window | now | MES record updated |
| Maintenance | Inspect labeler, verify candidate sensor issue and define repair action | CMMS | arrival time, verified cause, action, spare parts, labor, trial run | first response in 15 min | trial run completed and recorded |
| Quality | Isolate and recheck 32 cartons | QMS | isolation scope, recheck result, release/rework decision, authorizer | before production release | authorized QMS disposition |
| EHS | Confirm whether repair requires guard opening, electrical work or isolation | EHS/OA | risk level, permit need, isolation status | before maintenance starts risky work | safety clearance recorded |
| Warehouse/Procurement | Check label roll and sensor spare inventory | SAP/ERP | inventory, substitute, ETA, purchase status | first response in 20 min | material/spare status confirmed |
| PMC | Assess delivery impact if recovery misses 15:30 | PMC/APS | reschedule, overtime, insertion or delivery-risk plan | before next sync | plan confirmed |
| OA/Management | Escalate if stop exceeds threshold or delivery risk grows | OA | approval, meeting note or decision | when threshold hit | decision recorded |

## System Action Cards

### MES Action Card

```json
{
  "target_system": "MES",
  "action_type": "update_production_state",
  "readiness": "needs_confirmation",
  "required_fields": ["line", "downtime_start", "current_state", "order", "sku", "lost_output_estimate", "recovery_window"],
  "missing_fields": ["order", "sku", "lost_output_estimate"],
  "authorization_required": false,
  "post_submit_verification": "MES event id and updated line state"
}
```

### CMMS Action Card

```json
{
  "target_system": "CMMS",
  "action_type": "create_or_update_repair_work_order",
  "readiness": "needs_confirmation",
  "required_fields": ["asset_id", "symptom", "downtime_impact", "candidate_cause", "assigned_team", "safety_requirement"],
  "missing_fields": ["asset_id", "assigned_team", "safety_requirement"],
  "authorization_required": false,
  "post_submit_verification": "CMMS work order id, repair action, labor, spare parts and trial-run result"
}
```

### QMS Action Card

```json
{
  "target_system": "QMS",
  "action_type": "create_isolation_and_recheck_record",
  "readiness": "requires_authorization",
  "required_fields": ["batch", "quantity", "defect", "isolation_scope", "recheck_method", "release_authorizer"],
  "missing_fields": ["batch", "recheck_method", "release_authorizer"],
  "authorization_required": true,
  "post_submit_verification": "QMS record id and authorized disposition"
}
```

### EHS Action Card

```json
{
  "target_system": "EHS/OA",
  "action_type": "confirm_repair_safety_boundary",
  "readiness": "needs_confirmation",
  "required_fields": ["repair_scope", "energy_isolation_need", "permit_need", "risk_level"],
  "missing_fields": ["repair_scope", "energy_isolation_need", "permit_need", "risk_level"],
  "authorization_required": true,
  "post_submit_verification": "safety clearance, permit or isolation record when required"
}
```

### SAP/ERP Action Card

```json
{
  "target_system": "SAP/ERP",
  "action_type": "check_material_and_spare_status",
  "readiness": "needs_confirmation",
  "required_fields": ["label_roll_material_code", "sensor_part_code", "inventory_location", "order"],
  "missing_fields": ["label_roll_material_code", "sensor_part_code", "order"],
  "authorization_required": false,
  "post_submit_verification": "inventory, ETA and purchase status"
}
```

### PMC/APS Action Card

```json
{
  "target_system": "PMC/APS",
  "action_type": "evaluate_schedule_impact",
  "readiness": "needs_confirmation",
  "required_fields": ["order", "target_recovery_time", "lost_output_estimate", "quality_hold_status", "material_status"],
  "missing_fields": ["order", "lost_output_estimate", "quality_hold_status", "material_status"],
  "authorization_required": false,
  "post_submit_verification": "reschedule, overtime, insertion or delivery-risk decision"
}
```

## Copy-ready Notification

```text
[Line 3 labeler missing labels / unplanned stop risk]
Production owner: Line 3 shift leader.
Confirmed facts: labeler started missing labels at 14:20; label roll changed but issue remained; line stopped for 18 minutes; Quality found 32 cartons needing recheck; sensor misalignment is only suspected, not verified.

Requests:
- Maintenance: confirm arrival time, verified cause, repair action, spare parts, labor and trial-run requirement in CMMS.
- Quality: create QMS isolation/recheck record for 32 cartons and confirm release/rework authorization boundary.
- EHS: confirm whether repair requires permit, guard opening, electrical work or energy isolation.
- Warehouse/Procurement: check label roll and sensor spare inventory in SAP/ERP.
- PMC: assess delivery impact if recovery misses 15:30 and prepare reschedule/overtime option.

Next sync: 15 minutes. Do not mark recovered, released or closed until MES, CMMS, QMS/EHS and PMC gates are complete.
```

## Closure Gates

- MES: actual downtime, lost output and recovery time recorded.
- CMMS: verified cause, repair action, labor, spare parts and trial-run result recorded.
- QMS: isolation/recheck and authorized disposition complete.
- EHS: permit/isolation/safety clearance complete when required.
- SAP/ERP: material and spare-part status confirmed.
- PMC/APS: delivery and capacity impact decided.
- OA: escalation or approval recorded if threshold is reached.
- Knowledge base/SOP candidate note created only after closure and authorized review.

