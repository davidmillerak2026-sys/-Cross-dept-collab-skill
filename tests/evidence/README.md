# AstronClaw Evidence Folder

Use this folder after SkillHub approval to store real AstronClaw evidence.

Recommended layout:

```text
tests/evidence/
├── screenshots/
│   ├── T01_AstronClaw_maintenance_YYYYMMDD.png
│   └── ...
└── outputs/
    ├── T01.md
    └── ...
```

Rules:

- Put required screenshot files under `tests/evidence/screenshots/`.
- Put copied text outputs under `tests/evidence/outputs/`.
- Fill `tests/run_record_template.csv` with paths relative to the Skill root, such as `tests/evidence/screenshots/T01_AstronClaw_maintenance_20260616.png`.
- `scripts/expert_rubric_gate.py --require-astronclaw` only passes when required records are marked passed and the referenced screenshot/output files exist on disk.
- Do not store real customer data, ID documents, phone numbers, credentials, or unredacted production records here.
