# GUI Retest Outputs

This folder is only a local scoring workspace and should stay clean before creating an upload ZIP.

Use one clean AstronClaw `新建任务` session per model and prompt. Do not use Auto. Preferred evidence layout is outside the upload package:

```text
../submission_materials/astronclaw_real_runs/<date>_gui_matrix/
└── G01/
    ├── Spark-X2-Flash_G01.md
    ├── GLM5.1_G01.md
    └── ...
```

If temporary output files are saved here for scoring, move them to `submission_materials` and clean this folder before packaging the Skill. Failed model outputs may contain wording that should not be included in the published Skill package.

Each scenario should eventually collect:

- `G01.md`
- `G02.md`
- `G03.md`
- `G04.md`
- `G05.md`
- `G06.md`
- `G07.md`
- `G08.md`
- `G09.md`
- `G10.md`

Score the current evidence set with:

```bash
python scripts/score_gui_retest.py --outputs ../submission_materials/astronclaw_real_runs/<date>_gui_matrix/G01 --model Spark-X2-Flash --report tests/gui_retest_score_report.csv
```
