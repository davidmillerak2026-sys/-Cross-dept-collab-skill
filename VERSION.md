# Version History

## 2026.06.17-champion-12

Status: local evidence-sprint status layer added; platform and AstronClaw evidence still pending.

Key changes:

- Added `scripts/evidence_sprint_status.py` to render a phase-by-phase status report from the evidence sprint manifest, platform evidence JSON, AstronClaw run records, enterprise-flow records, stability-stress records and pilot-feedback records.
- Added generated artifact `tests/expert_evidence_sprint_status.md` so the team can see required/optional completion counts, SkillHub public URL status and the next required evidence actions after each real test run.
- Added `skillhub_public_url` to the expert evidence sprint manifest so the public SkillHub page is tracked as a durable link, not only as a screenshot.
- Wired the status layer into README, tests README, submission manifest, validate gate and smoke coverage.
- Updated `scripts/validate_package.py` to ignore root `.git` metadata when the same package is mirrored into the GitHub publication worktree.

Verification:

- `scripts/export_expert_evidence_sprint_pack.py`
- `scripts/evidence_sprint_status.py`
- `scripts/smoke_test_package.py`
- `scripts/validate_package.py`

## 2026.06.17-champion-11

Status: local evidence-sprint workflow tightened; platform evidence pending.

Key changes:

- Added `scripts/export_expert_evidence_sprint_pack.py` to generate one ranked evidence sprint plan across platform submission, 18 required cases, S01-S10 enterprise flow, ST01-ST12 stability stress, and 6 pilot-feedback roles.
- Added generated artifacts `tests/expert_evidence_sprint_pack.md` and `tests/expert_evidence_sprint_manifest.csv` so the real capture sequence can be executed without hand-assembling priorities.
- Added `tests/run_outputs/README.md` to make the T01-T39 text-output scoring path explicit for `scripts/score_run.py`.
- Wired the sprint-pack layer into README, tests README, validate gate, submission manifest, and smoke coverage.

Verification:

- `scripts/export_expert_evidence_sprint_pack.py`
- `scripts/smoke_test_package.py`
- `scripts/validate_package.py`

## 2026.06.17-champion-10

Status: local runtime-scoring layer tightened; platform evidence pending.

Key changes:

- Tightened `scripts/score_run.py` so high-value expert-review cases can require grouped semantics such as notification-vs-system layering, PMС/SAP/MES coordination, engineering change boundaries, and action-card contract fields.
- Extended `tests/test_cases.json` for T21, T36, T37 and T38 with `must_contain_any_groups`, stronger `critical_terms`, and stricter forbidden wording.
- Strengthened `scripts/smoke_test_package.py` so local scoring tests now prove T21 integration action cards, T36 high-impact PMC escalation, T37 engineering-change boundary control, and T38 daily-close orchestration behavior.

Verification:

- `scripts/smoke_test_package.py`
- `scripts/validate_package.py`
- `scripts/expert_rubric_gate.py`

## 2026.06.17-champion-09

Status: local orchestration-contract layer ready; platform evidence pending.

Key changes:

- Split `templates/integration_contracts.json` into clearer real-enterprise system layers: `ENTERPRISE_IM_EMAIL`, `OA_APPROVAL`, `PMC_APS`, and `PLM_ENGINEERING_CHANGE`, alongside the existing CMMS/MES/QMS/EHS/SAP_ERP contracts.
- Extended the shared action-card contract with `service_level_target`, `business_decision_deadline`, `channel_boundary`, `side_effect_boundary`, and `expected_receipt.receipt_owner`.
- Strengthened `SKILL.md`, `README.md`, `references/capability_playbook.md`, and `references/expert_review_playbook.md` so the production-led orchestration story matches the actual contract file.
- Added smoke coverage to prevent future regressions that collapse notification, approval, planning and engineering-change flows back into a single vague system action.

Verification:

- `scripts/validate_package.py`
- `scripts/smoke_test_package.py`
- `scripts/expert_rubric_gate.py`

## 2026.06.17-champion-08

Status: local management-impact layer ready; platform evidence pending.

Key changes:

- Split `templates/integration_contracts.json` into clearer real-enterprise system layers: `ENTERPRISE_IM_EMAIL`, `OA_APPROVAL`, `PMC_APS`, and `PLM_ENGINEERING_CHANGE`, alongside the existing CMMS/MES/QMS/EHS/SAP_ERP contracts.
- Extended the shared action-card contract with `service_level_target`, `business_decision_deadline`, `channel_boundary`, `side_effect_boundary`, and `expected_receipt.receipt_owner`.
- Strengthened `README.md`, `references/capability_playbook.md`, and `references/expert_review_playbook.md` so the production-led orchestration story matches the actual contract file.
- Added smoke coverage to prevent future regressions that collapse notification, approval, planning and engineering-change flows back into a single vague system action.
- Added `templates/impact_scoreboard.md`, `templates/impact_scoreboard.schema.json` and `templates/management_escalation_packet.md` so high-impact events can be summarized for production managers, PMC, quality and safety leads.
- Extended `SKILL.md`, `templates/department_communication_flow.md`, `templates/enterprise_flow_output_contract.md` and `templates/output_modes.md` to require an impact scoreboard and escalation decision packet when production, quality, safety, delivery, material or cost are jointly affected.
- Expanded `references/commercial_value_model.md` with management-facing metrics such as `production_loss_units`, `delivery_risk_level` and `blocked_close_reason_count`.
- Updated `examples/06_expert_screenshot_outputs.md` to show a screenshot-ready impact scoreboard and management escalation packet for the T01 unplanned-stop case.
- Wired the new management-impact layer into README, submission manifest, evidence readiness, validate gate, smoke gate and expert-rubric innovation/orchestration evidence.

Verification:

- `scripts/validate_package.py`
- `scripts/smoke_test_package.py`
- `scripts/expert_rubric_gate.py`
- `scripts/champion_acceptance_gate.py`

## 2026.06.16-champion-07

Status: local champion-acceptance gate ready; platform evidence pending.

Key changes:

- Added `scripts/champion_acceptance_gate.py` to unify the final champion-level acceptance check across local gates, SkillHub submission evidence, T01-T39 full AstronClaw runs, S01-S10 enterprise-flow runs, ST01-ST12 stability stress runs and real pilot feedback.
- Added `tests/platform_submission_evidence_template.json` to register the real contest-submit screenshot, SkillHub approval screenshot, SkillHub public page screenshot and live SkillHub URL.
- Added `tests/champion_acceptance_report.md` as the generated acceptance report with `champion_ready` status and missing-action guidance.
- Extended README, tests README, submission manifest, validate gate, smoke gate and expert-rubric engineering/application-value evidence to include the champion acceptance layer.
- Tightened the platform evidence list to explicitly include contest submit success, S01-S10 enterprise-flow runs and real pilot feedback evidence files.

Verification:

- `scripts/validate_package.py`
- `scripts/smoke_test_package.py`
- `scripts/expert_rubric_gate.py`
- `scripts/champion_acceptance_gate.py`

## 2026.06.16-champion-06

Status: local enterprise-flow output contract ready; platform evidence pending.

Key changes:

- Added `templates/enterprise_flow_output_contract.md` to stabilize S01-S10 outputs around unified event package, layered flow, department feedback contract, formal system action cards, close gates, escalation clock and post-closure knowledge candidates.
- Added `tests/enterprise_flow_golden_outputs.md` with scenario-specific golden checkpoints for all 10 production-led enterprise flow scenarios.
- Wired the enterprise-flow contract into `SKILL.md`, README, submission manifest, validate gate, smoke gate and expert-rubric local evidence.
- Preserved strict boundary: no unsupported claims of automatic sync, approval, quality release, recovery, closure or SOP publication without real evidence.
- Added ST01-ST12 abnormal-input stability stress assets: `tests/stability_stress_cases.json`, `scripts/export_stability_stress_pack.py`, `tests/astronclaw_stability_stress_prompt_pack.md`, `tests/run_record_stability_stress_template.csv`, `scripts/score_stability_stress.py` and `tests/stability_stress_outputs/README.md`.
- Extended the stability protocol to require abnormal-input pressure runs for short input, noise, duplicate records, conflict, dangerous requests, prompt injection, privacy/credential data, missing fields, system failure, unsupported completion, mixed events and channel misuse.
- Added pilot-value evidence assets: `tests/pilot_feedback_roles.json`, `scripts/export_pilot_feedback_pack.py`, `tests/pilot_feedback_interview_pack.md`, `tests/pilot_feedback_records_template.csv` and `scripts/score_pilot_feedback.py`.
- Extended application-value evidence to cover 6 anonymized pilot roles: production supervisor, maintenance, quality engineer, EHS/safety, PMC/planning and digital owner.
- Added `scripts/evidence_readiness_report.py` and `tests/evidence_readiness_report.md` to separate local package readiness from missing AstronClaw run evidence and real pilot feedback.

Verification:

- `scripts/validate_package.py`
- `scripts/smoke_test_package.py`
- `scripts/expert_rubric_gate.py`

## 2026.06.16-champion-05

Status: local enterprise-flow gate ready; platform evidence pending.

Key changes:

- Added 10 production-led enterprise flow scenarios for nonplanned stop, first-article quality hold, temperature alarm, EHS hazard, material shortage, unknown liquid leak, repeated failure, customer complaint rework, temporary process change and daily close meeting.
- Strengthened system layering: enterprise IM/email for notification only; MES, CMMS, QMS, EHS, SAP/ERP, OA and PMC/APS for formal records, approvals, feedback and close gates.
- Made knowledge base/SOP post-closure only: candidate lessons are created after event closure and cannot replace urgent flow or authorization.
- Added local smoke coverage and submission manifest evidence for the 10-scenario enterprise flow pack.
- Added exportable AstronClaw enterprise-flow prompt pack and run-record template for S01-S10.
- Added S01-S10 enterprise-flow output scorer for post-run quality checks.

Verification:

- `scripts/validate_package.py`
- `scripts/smoke_test_package.py`
- `scripts/expert_rubric_gate.py`

## 2026.06.16-champion-04

Status: local expert-gate ready; platform evidence pending.

Key changes:

- Added T39 department-flow required case for unified event package, enterprise IM, MES/CMMS/QMS/EHS/SAP/ERP/OA/PMC feedback and close gate evidence.
- Added business-value evidence assets: `templates/pilot_feedback_card.md` and `references/commercial_value_model.md`.
- Added local gates for department-flow and business-value contracts.
- Expanded evidence pack to 39 test cases and 18 required AstronClaw screenshots.
- Preserved compliance boundary: no claim of 100 expert points until SkillHub approval and AstronClaw run evidence exist.

Verification:

- `scripts/validate_package.py`
- `scripts/smoke_test_package.py`
- `scripts/expert_rubric_gate.py`

## 2026.06.16-champion-03

Status: local expert-gate ready; platform evidence pending.

Key changes:

- Added required-only AstronClaw run-record template.
- Added real evidence-file existence checks for required screenshots and outputs.
- Added T31 heat-ranking compliance evidence as a required case.
- Updated PPT and submission materials to match required evidence strategy.

## 2026.06.15-champion-02

Status: package hardening.

Key changes:

- Added expert rubric matrix, smoke tests, redaction script and expert gate.
- Added action-readiness gates, degraded completion, signal calibration and champion self-review.
- Added field execution and work-order data quality gates.
- Added production-led PMC, engineering and daily-close orchestration cases.

## 2026.06.15-initial

Status: first contest-ready package.

Key changes:

- Created `industrial-workorder-collaboration` Skill for manufacturing现场-to-office collaboration.
- Added core scenarios: maintenance, quality, safety, changeover, meetings, handover and procurement.
- Added README, examples, templates and test pack.
