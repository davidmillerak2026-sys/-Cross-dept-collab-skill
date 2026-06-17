# Enterprise Flow Output Folder

After running `tests/astronclaw_enterprise_flow_prompt_pack.md` in AstronClaw, save copied text outputs here:

```text
tests/enterprise_flow_outputs/S01.md
tests/enterprise_flow_outputs/S02.md
...
tests/enterprise_flow_outputs/S10.md
```

Then run:

```bash
python scripts/score_enterprise_flow.py --outputs tests/enterprise_flow_outputs --report tests/enterprise_flow_score_report.csv
```

This scorer checks whether each output covers:

- production-owned unified event package
- enterprise IM/email notification layer
- MES, CMMS, QMS, EHS, SAP/ERP, OA and PMC/APS formal system records
- department feedback requirements
- closure gates
- post-closure knowledge base/SOP boundary
- forbidden unsupported claims such as automatic system sync, quality release, production recovery or work order closure

