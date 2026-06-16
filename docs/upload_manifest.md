# Upload Manifest

This manifest lists the public project files prepared for the GitHub repository.

## Root

- `.gitignore`
- `README.md`
- `README.zh-CN.md`
- `SKILL.md`

## Documentation

- `docs/architecture.md`
- `docs/operating_playbook.md`
- `docs/scenario_index.md`
- `docs/upload_manifest.md`

## Examples

- `examples/01_voice_to_work_order.md`
- `examples/02_quality_issue_to_collaboration.md`
- `examples/03_shift_handover_weekly_report.md`
- `examples/04_complex_agent_workflow.md`
- `examples/05_enterprise_department_flow_10_scenarios.md`
- `examples/06_demo_output_unplanned_stop.md`

## Scripts

- `scripts/redact_input.py`
- `scripts/export_stability_stress_pack.py`
- `scripts/export_pilot_feedback_pack.py`
- `scripts/score_stability_stress.py`
- `scripts/score_pilot_feedback.py`
- `scripts/validate_project.py`

## Tests

- `tests/project_cases.json`
- `tests/enterprise_flow_golden_outputs.md`
- `tests/stability_stress_cases.json`
- `tests/stability_stress_prompt_pack.md`
- `tests/run_record_stability_stress_template.csv`
- `tests/stability_stress_outputs/README.md`
- `tests/pilot_feedback_roles.json`
- `tests/pilot_feedback_interview_pack.md`
- `tests/pilot_feedback_records_template.csv`

## Templates

- `templates/action_card.schema.json`
- `templates/action_readiness.schema.json`
- `templates/adversarial_guardrail.md`
- `templates/closed_loop_learning.md`
- `templates/degraded_completion.md`
- `templates/department_communication_flow.md`
- `templates/enterprise_flow_output_contract.md`
- `templates/diagnosis_matrix.schema.json`
- `templates/evidence_trace.schema.json`
- `templates/field_execution_plan.md`
- `templates/handoff_summary.md`
- `templates/human_decision_packet.md`
- `templates/integration_contracts.json`
- `templates/office_message_templates.md`
- `templates/output_modes.md`
- `templates/production_cross_department_handoff.md`
- `templates/quality_gate.md`
- `templates/redaction_rules.json`
- `templates/role_handoff.md`
- `templates/run_trace.schema.json`
- `templates/signal_calibration.schema.json`
- `templates/work_order.schema.json`
- `templates/work_order_data_quality.md`

## Validation

Run:

```bash
python scripts/validate_project.py
```

Expected output:

```text
PASS: public project package is clean and complete
```
