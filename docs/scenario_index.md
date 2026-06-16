# Scenario Index

This project includes 10 production-led enterprise flow scenarios. Each scenario shows what Production discovers, which departments are notified, which systems keep formal records, what feedback is required and what gates must be satisfied before closure.

Full walkthroughs are in [examples/05_enterprise_department_flow_10_scenarios.md](../examples/05_enterprise_department_flow_10_scenarios.md).

| ID | Scenario | Production discovery | Main departments | Formal systems |
| --- | --- | --- | --- | --- |
| S01 | Labeler missing labels and likely unplanned stop | Repeated missing labels after label roll change | Maintenance, Quality, EHS, PMC, Warehouse/Procurement | MES, CMMS, QMS, EHS, SAP/ERP, OA, PMC/APS |
| S02 | First article oversized after changeover | Batch production paused after first-article deviation | Quality, Engineering, PMC | MES, QMS, OA/PLM, PMC/APS, SAP/ERP |
| S03 | Injection machine oil temperature alarm | Rising temperature with unclear threshold and calibration state | Maintenance, EHS, Engineering, PMC | MES, CMMS, EHS, OA, PMC/APS |
| S04 | Fire passage blocked by materials | Line-side material blocks safe passage and feeding | EHS, Warehouse, PMC, Production supervisor | EHS, OA, SAP/ERP, PMC/APS, MES |
| S05 | Critical packaging material delay | Production team and equipment ready, but material unavailable | PMC, Warehouse, Procurement, Quality | SAP/ERP, PMC/APS, QMS, MES, OA |
| S06 | Unknown liquid leakage | Unknown liquid near the line with unclear source | EHS, Maintenance, Warehouse, Production | EHS, CMMS, SAP/ERP, MES, OA |
| S07 | Repeated equipment failure requiring vendor and spare parts | Same asset fails repeatedly and temporary reset is unstable | Maintenance, Engineering, Procurement, PMC | CMMS, SAP/ERP, OA, PMC/APS, MES |
| S08 | Customer complaint about wrong label | Need to trace affected batches and organize rework | Quality, Warehouse, Sales/Customer interface, PMC | QMS, MES, SAP/ERP, PMC/APS, OA |
| S09 | Temporary process parameter change | Engineering proposes temporary parameter change with production risk | Engineering, Quality, PMC, Production | OA/PLM, MES, QMS, PMC/APS, SAP/ERP |
| S10 | Daily production close meeting with multiple open items | Several equipment, quality, material, safety and schedule actions need closure | Maintenance, Quality, EHS, PMC, Procurement | OA, MES, CMMS, QMS, EHS, SAP/ERP, PMC/APS |

## Common Closure Gates

- MES confirms actual production impact and recovery window.
- CMMS confirms repair action, labor, spare parts and trial run.
- QMS confirms isolation, recheck, rework, release or CAPA stage.
- EHS confirms permit, isolation and safety corrective closure when needed.
- SAP/ERP confirms order, material, spare part, purchase, inventory, cost or delivery impact.
- PMC/APS confirms schedule, capacity, overtime, insertion or delivery decision.
- OA records approval, incident report, meeting notes or escalation when needed.
- Knowledge base/SOP candidates are created only after event closure and authorization review.

