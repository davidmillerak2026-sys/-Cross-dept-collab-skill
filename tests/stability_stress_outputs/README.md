# ST01-ST12 稳定性压力输出保存说明

运行 `tests/stability_stress_prompt_pack.md` 中 ST01-ST12 后，把实际输出保存到本目录：

- `ST01.md`
- `ST02.md`
- `ST03.md`
- `ST04.md`
- `ST05.md`
- `ST06.md`
- `ST07.md`
- `ST08.md`
- `ST09.md`
- `ST10.md`
- `ST11.md`
- `ST12.md`

保存后运行：

```bash
python scripts/score_stability_stress.py --outputs tests/stability_stress_outputs --report tests/stability_stress_score_report.csv
```

评分通过不代表所有运行环境稳定性已经完全证明；仍需要把真实运行输出路径填入 `tests/run_record_stability_stress_template.csv`。
