# T01-T39 Run Outputs

用途：保存 `scripts/score_run.py` 直接读取的全量 AstronClaw/SkillHub 实际输出文本。

使用规则：

- 文件名固定为 `T01.md` 到 `T39.md`。
- 每个文件只保存该用例的实际输出，不混入其他用例内容。
- 如果截图足够说明问题，也建议同时把文本输出复制到这里，便于半自动评分。
- `tests/run_record_template.csv` 里的 `output_file_or_screenshot` 仍然优先填写真实截图路径；这里的文本输出主要用于 `scripts/score_run.py`。

建议命令：

```bash
python scripts/score_run.py --outputs tests/run_outputs --report tests/run_score_report.csv
```
