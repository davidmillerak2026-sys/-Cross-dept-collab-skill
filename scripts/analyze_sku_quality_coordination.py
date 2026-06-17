#!/usr/bin/env python3
"""Analyze a SKU quality event and render cross-department coordination impact."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "examples" / "data" / "sku_quality_coordination_sample.csv"
DEFAULT_OUT = ROOT / "tests" / "sku_quality_coordination_analysis.md"

NUMERIC_METRICS = {
    "planned_shift_qty",
    "planned_rate",
    "line_stop_minutes",
    "isolated_qty",
    "sample_qty",
    "sample_fail_qty",
    "ready_stock_unaffected",
    "shipment_requirement_today",
    "rework_capacity_before_1720",
}

REQUIRED_METRICS = NUMERIC_METRICS | {"engineer_eta", "decision_due_by"}


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    if not rows:
        raise SystemExit(f"no rows found: {path}")
    return rows


def metric_map(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    metrics = {row["metric"]: row for row in rows}
    missing = sorted(REQUIRED_METRICS - set(metrics))
    if missing:
        raise SystemExit(f"missing required metrics: {', '.join(missing)}")
    return metrics


def number(metrics: dict[str, dict[str, str]], metric: str) -> float:
    value = metrics[metric]["value"].strip()
    try:
        return float(value)
    except ValueError as exc:
        raise SystemExit(f"metric {metric} is not numeric: {value}") from exc


def fmt_units(value: float) -> str:
    if value == int(value):
        return str(int(value))
    return f"{value:.1f}"


def compute(metrics: dict[str, dict[str, str]]) -> dict[str, float | str]:
    planned_shift_qty = number(metrics, "planned_shift_qty")
    planned_rate = number(metrics, "planned_rate")
    stop_minutes = number(metrics, "line_stop_minutes")
    isolated_qty = number(metrics, "isolated_qty")
    sample_qty = number(metrics, "sample_qty")
    sample_fail_qty = number(metrics, "sample_fail_qty")
    ready_stock = number(metrics, "ready_stock_unaffected")
    shipment_req = number(metrics, "shipment_requirement_today")
    rework_capacity = number(metrics, "rework_capacity_before_1720")

    lost_units = round(planned_rate / 60 * stop_minutes)
    current_gap = max(0, shipment_req - ready_stock)
    post_rework_gap = max(0, shipment_req - ready_stock - rework_capacity)
    isolation_rate = isolated_qty / planned_shift_qty * 100 if planned_shift_qty else 0
    sample_fail_rate = sample_fail_qty / sample_qty * 100 if sample_qty else 0
    overtime_units_needed = post_rework_gap

    quality_level = "L3" if sample_fail_rate >= 50 or isolation_rate >= 10 else "L2"
    delivery_level = "L2" if current_gap > 0 else "L0"
    production_level = "L2" if lost_units > 0 else "L0"
    management_required = "yes" if current_gap > 0 and quality_level in {"L2", "L3"} else "no"

    return {
        "lost_units": lost_units,
        "current_gap": current_gap,
        "post_rework_gap": post_rework_gap,
        "isolation_rate": isolation_rate,
        "sample_fail_rate": sample_fail_rate,
        "overtime_units_needed": overtime_units_needed,
        "quality_level": quality_level,
        "delivery_level": delivery_level,
        "production_level": production_level,
        "management_required": management_required,
        "blocked_close_reason_count": 4,
    }


def render_report(input_path: Path) -> str:
    rows = read_rows(input_path)
    metrics = metric_map(rows)
    result = compute(metrics)
    first = rows[0]

    planned_rate = number(metrics, "planned_rate")
    stop_minutes = number(metrics, "line_stop_minutes")
    shipment_req = number(metrics, "shipment_requirement_today")
    ready_stock = number(metrics, "ready_stock_unaffected")
    rework_capacity = number(metrics, "rework_capacity_before_1720")
    isolated_qty = number(metrics, "isolated_qty")
    sample_qty = number(metrics, "sample_qty")
    sample_fail_qty = number(metrics, "sample_fail_qty")

    return "\n".join(
        [
            "# SKU Quality Coordination Analysis",
            "",
            f"- source_data: `{input_path.relative_to(ROOT).as_posix()}`",
            f"- event_id: `{first['event_id']}`",
            f"- sku: `{first['sku']}`",
            f"- order_id: `{first['order_id']}`",
            f"- batch_id: `{first['batch_id']}`",
            f"- decision_due_by: `{metrics['decision_due_by']['value']}`",
            f"- engineer_eta: `{metrics['engineer_eta']['value']}`",
            f"- management_required: `{result['management_required']}`",
            "",
            "## Computed KPIs",
            "",
            "| KPI | Formula | Value | Coordination meaning |",
            "| --- | --- | --- | --- |",
            f"| downtime_loss_units | `{fmt_units(planned_rate)} / 60 * {fmt_units(stop_minutes)}` | `{fmt_units(float(result['lost_units']))} pcs` | MES production impact for PMC and management escalation |",
            f"| current_shipment_gap | `{fmt_units(shipment_req)} - {fmt_units(ready_stock)}` | `{fmt_units(float(result['current_gap']))} pcs` | Warehouse can ship released stock only; PMC must manage shortfall |",
            f"| post_rework_gap | `{fmt_units(shipment_req)} - {fmt_units(ready_stock)} - {fmt_units(rework_capacity)}` | `{fmt_units(float(result['post_rework_gap']))} pcs` | Still estimated until QMS release and engineering validation |",
            f"| isolation_rate | `{fmt_units(isolated_qty)} / {fmt_units(number(metrics, 'planned_shift_qty'))}` | `{result['isolation_rate']:.1f}%` | QMS containment severity |",
            f"| sample_fail_rate | `{fmt_units(sample_fail_qty)} / {fmt_units(sample_qty)}` | `{result['sample_fail_rate']:.1f}%` | Quality risk; do not release affected batch without authorization |",
            f"| blocked_close_reason_count | `quality + engineering + PMC + warehouse` | `{result['blocked_close_reason_count']}` | Keep event open until formal receipts exist |",
            "",
            "## Department Coordination Map",
            "",
            "| Department | Formal system | Must feed back | Production next action |",
            "| --- | --- | --- | --- |",
            "| Quality | QMS | isolation scope, retest result, rework/release authorization, CAPA boundary | keep affected batch on QA HOLD; do not ship unreleased stock |",
            "| PMC | PMC/APS + SAP PP | partial shipment, rework, overtime or customer-commitment options | prepare A/B/C delivery decision before management deadline |",
            "| Warehouse | SAP/ERP/WMS | released-stock quantity, affected-batch hold, picking wave and unlock receipt | ship released batch only; block B20260617-A17-03 until QMS release |",
            "| Engineering | PLM/OA/MES | onsite validation, fixture/parameter finding, trial result and effective boundary | keep candidate cause open until validated; request trial-run evidence |",
            "| Production | MES/OA + enterprise IM | downtime, loss units, sync cadence and decision package | own unified event package and next synchronization |",
            "",
            "## Delivery Options",
            "",
            "| Option | Ship quantity | Remaining gap | Required authorization |",
            "| --- | --- | --- | --- |",
            f"| A. Released stock only | `{fmt_units(ready_stock)} pcs` | `{fmt_units(float(result['current_gap']))} pcs` | PMC/customer boundary confirmation |",
            f"| B. Released stock + rework | `{fmt_units(ready_stock + rework_capacity)} pcs` | `{fmt_units(float(result['post_rework_gap']))} pcs` | QMS release + engineering validation + warehouse unlock |",
            f"| C. Released stock + rework + overtime | `{fmt_units(shipment_req)} pcs target` | `0 pcs estimated` | production manager, PMC, QMS and warehouse receipts |",
            "",
            "## Guardrails",
            "",
            "- Do not write 已放行, 已发货, 已恢复生产 or 已关闭 until the matching QMS, WMS, MES, PMC and OA receipts exist.",
            "- Treat rework capacity as estimated until Quality and Engineering confirm it.",
            "- Keep customer commitment wording under PMC or authorized customer-facing owner control.",
            "",
        ]
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=str(DEFAULT_INPUT), help="SKU coordination CSV input")
    parser.add_argument("--out", default=str(DEFAULT_OUT), help="Markdown report output")
    args = parser.parse_args()

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render_report(Path(args.input)), encoding="utf-8")
    print(f"wrote={out}")


if __name__ == "__main__":
    main()
