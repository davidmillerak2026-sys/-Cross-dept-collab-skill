# Operating Playbook

## Standard Flow

1. Capture the production-floor record.
2. Redact sensitive data when the content may be shared.
3. Build a unified event package.
4. Identify involved departments and formal systems.
5. Generate department tasks and action cards.
6. Send notification through enterprise IM or email.
7. Collect system receipts and department feedback.
8. Apply closure gates.
9. Create candidate knowledge only after closure.

## Closure Gates

| Gate | Required evidence |
| --- | --- |
| Production recovery | MES recovery time, output impact and owner confirmation |
| Maintenance completion | CMMS repair action, labor, spare parts and trial-run result |
| Quality release | QMS recheck, isolation disposition and authorized release |
| Safety clearance | EHS permit, isolation release or corrective verification |
| Planning confirmation | PMC/APS delivery and capacity decision |
| Business impact | SAP/ERP order, material, inventory, procurement or cost status |
| Management escalation | OA approval, incident report or meeting-note decision when required |

## Degraded Completion

When a system is unavailable, an attachment cannot be read, a record conflicts or required fields are missing, the Skill should still produce a useful result:

- what is confirmed
- what cannot be confirmed
- what can be done safely now
- what must not be claimed yet
- what fields or receipts are needed to continue

