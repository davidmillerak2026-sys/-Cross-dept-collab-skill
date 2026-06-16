# Architecture

The Skill uses a layered collaboration model:

1. Input parsing: production-floor notes, alarms, handover records, meeting notes or incident descriptions.
2. Fact discipline: split confirmed facts, reasonable inference and missing information.
3. Event package: create a shared production-owned event record.
4. Department routing: assign responsibilities to Production, Maintenance, Quality, Engineering, EHS, PMC, Warehouse and Procurement.
5. System action cards: prepare structured payloads for MES, CMMS, QMS, EHS, SAP/ERP, OA and PMC/APS.
6. Authorization gates: block unsupported claims about release, repair, recovery, closure and SOP publication.
7. Closure learning: convert closed incidents into candidate knowledge-base or SOP updates.

## Why Action Cards

The Skill should not pretend that an external enterprise system has already been updated. Instead, it produces action cards with required fields, missing fields, authorization requirements and post-submit verification. A user, tool or upstream Agent can then submit the action card to the real system.

## Integration Boundaries

| Integration | Skill behavior |
| --- | --- |
| MES | Prepare production-impact records and recovery-window updates |
| CMMS | Prepare maintenance work order, dispatch, spare-part and trial-run updates |
| QMS | Prepare isolation, recheck, rework, release and CAPA records |
| EHS | Prepare hazard, permit, isolation and corrective closure records |
| SAP/ERP | Prepare material, inventory, purchase, order and cost-impact checks |
| OA | Prepare approvals, meeting minutes, incident reports and escalation records |
| PMC/APS | Prepare schedule, capacity, overtime, insertion and delivery-impact adjustments |

