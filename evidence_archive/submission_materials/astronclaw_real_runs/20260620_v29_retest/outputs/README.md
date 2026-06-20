# V29 Retest Outputs

Save copied AstronClaw GUI outputs here:

```text
outputs/<model>/<case_id>.md
```

Example:

```text
outputs/Qwen3.6/V29-G01.md
```

After saving output files, run:

```text
python scripts/score_v29_retest.py
```

The script writes `v29_score_report.csv` in the parent retest folder.

Faster workflow after copying the AstronClaw GUI output:

```text
python scripts/save_v29_output.py --model Qwen3.6 --case V29-G01 --from-clipboard
```

That command saves the output, updates `v29_run_record.csv`, and regenerates `v29_score_report.csv`.

It also regenerates `v29_summary.md`, which shows progress by model, progress by scenario, recurring issue labels, and the next missing rows.
