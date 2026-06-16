# Cross-department Collaboration Skill

[中文说明](README.zh-CN.md)

`industrial-workorder-collaboration` is a manufacturing operations Skill that turns production-floor notes, alarms, handover records and meeting notes into cross-department work orders, action cards and closure-ready collaboration packages.

The project focuses on a realistic enterprise flow: production owns the event package, enterprise IM/email handles notification, and formal systems such as MES, CMMS, QMS, EHS, SAP/ERP, OA and PMC/APS carry records, approvals, feedback and closure evidence.

## What It Does

- Converts unstructured production-floor records into work order drafts and cross-department action items.
- Separates confirmed facts, reasonable inference and missing information.
- Produces role-based tasks for Production, Maintenance, Quality, Engineering, EHS, PMC, Warehouse and Procurement.
- Creates action cards for MES, CMMS, QMS, EHS, SAP/ERP, OA and PMC/APS instead of pretending external systems have already been updated.
- Applies quality, safety and authorization gates before claiming release, repair completion, production recovery or work order closure.
- Handles degraded states such as missing attachments, expired system login, conflicting records and incomplete evidence.
- Redacts sensitive information before examples, logs or public materials are shared.
- Converts closed incidents into candidate knowledge-base or SOP notes only after closure and authorization.

## Enterprise System Model

| Layer | Systems or channels | Responsibility |
| --- | --- | --- |
| Notification | Enterprise WeChat, Feishu, DingTalk, email | Notify, remind, request lightweight confirmation, schedule sync meetings |
| Production record | MES | Production state, downtime, lost output, recovery window |
| Maintenance | CMMS | Repair work order, dispatch, spare parts, labor, trial run |
| Quality | QMS | Isolation, recheck, rework, release, CAPA |
| Safety | EHS | Hazard record, work permit, energy isolation, corrective closure |
| Business operations | SAP/ERP | Orders, materials, spare parts, inventory, procurement, cost, delivery impact |
| Approval and escalation | OA | Approval, incident report, cross-department meeting notes, management escalation |
| Planning | PMC/APS/schedule | Capacity, delivery date, overtime, insertion and reschedule decisions |
| Learning | Knowledge base/SOP | Post-closure lessons learned and candidate SOP updates only |

## Repository Layout

```text
.
├── SKILL.md
├── README.md
├── docs/
│   ├── architecture.md
│   ├── operating_playbook.md
│   ├── scenario_index.md
│   └── upload_manifest.md
├── examples/
│   ├── 01_voice_to_work_order.md
│   ├── 02_quality_issue_to_collaboration.md
│   ├── 03_shift_handover_weekly_report.md
│   ├── 04_complex_agent_workflow.md
│   ├── 05_enterprise_department_flow_10_scenarios.md
│   └── 06_demo_output_unplanned_stop.md
├── scripts/
│   ├── redact_input.py
│   └── validate_project.py
├── templates/
│   ├── department_communication_flow.md
│   ├── integration_contracts.json
│   ├── production_cross_department_handoff.md
│   └── ...
└── tests/
    └── project_cases.json
```

## Quick Prompt

```text
Use industrial-workorder-collaboration to process this production-floor record.

Line 3 labeler started missing labels at 14:20. The operator changed the label roll but the issue remained. The line has been stopped for 18 minutes. Quality found 32 cartons that need recheck. Maintenance suspects sensor misalignment but has not verified it. Production wants recovery before 15:30.
```

## Local Validation

```bash
python scripts/validate_project.py
python scripts/redact_input.py --text "张三 13812345678 设备 token=abc123"
```

`validate_project.py` checks that the public project copy contains only project content, not contest operations or judging material.

## Safety Boundary

The Skill prepares structured drafts, action cards and decision packets. It does not directly update MES, CMMS, QMS, EHS, SAP/ERP, OA or PMC systems. Any release, permit, production recovery, customer promise, SOP publication or privileged system write must be confirmed by an authorized person or upstream system.

## Key Scenario Pack

See [docs/scenario_index.md](docs/scenario_index.md) for the production-led scenario map, and [examples/05_enterprise_department_flow_10_scenarios.md](examples/05_enterprise_department_flow_10_scenarios.md) for full walkthroughs.

See [examples/06_demo_output_unplanned_stop.md](examples/06_demo_output_unplanned_stop.md) for a complete example output generated for an unplanned labeler stop.
