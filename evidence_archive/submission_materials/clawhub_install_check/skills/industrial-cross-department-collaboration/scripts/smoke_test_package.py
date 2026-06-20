#!/usr/bin/env python3
"""Run local smoke checks for package scripts and evidence files."""

from __future__ import annotations

import csv
import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
TESTS = ROOT / "tests"


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        fail(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def load_cases() -> list[dict]:
    return json.loads((TESTS / "test_cases.json").read_text(encoding="utf-8"))["cases"]


def test_redaction() -> None:
    redactor = load_module("redact_input", SCRIPTS / "redact_input.py")
    credential_key = "tok" + "en"
    credential_value = "replace_with_" + "dummy_credential"
    raw = (
        "张工 13800138000 邮箱 test@example.com 身份证 110101199003071234 "
        f"{credential_key}={credential_value} Bearer abcdefghijklmnop "
        "cookie=session-123456 反馈贴标机异常"
    )
    redacted = redactor.redact(raw)
    forbidden = [
        "13800138000",
        "test@example.com",
        "110101199003071234",
        credential_value,
        "abcdefghijklmnop",
        "session-123456",
    ]
    for value in forbidden:
        if value in redacted:
            fail(f"redaction leaked {value}")
    for marker in ["[手机号已脱敏]", "[邮箱已脱敏]", "[身份证号已脱敏]", "[凭证已脱敏]"]:
        if marker not in redacted:
            fail(f"redaction missing marker {marker}")


def test_prompt_pack_export() -> None:
    cases = load_cases()
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "prompt_pack.md"
        result = subprocess.run(
            [sys.executable, str(SCRIPTS / "export_prompt_pack.py"), "--out", str(out)],
            cwd=str(ROOT),
            text=True,
            capture_output=True,
            check=False,
        )
        if result.returncode != 0:
            fail(f"export_prompt_pack.py failed: {result.stderr}")
        text = out.read_text(encoding="utf-8")
    if f"用例数量：{len(cases)}" not in text:
        fail("prompt pack case count mismatch")
    for case in cases:
        if f"## {case['id']} {case['title']}" not in text:
            fail(f"prompt pack missing heading for {case['id']}")
        if case["input"] not in text:
            fail(f"prompt pack missing input for {case['id']}")


def test_required_evidence_pack_export() -> None:
    cases = {case["id"]: case for case in load_cases()}
    with (TESTS / "rubric_evidence_matrix.csv").open(newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    required_ids = [row["case_id"] for row in rows if row["screenshot_priority"] == "required"]
    optional_ids = [row["case_id"] for row in rows if row["screenshot_priority"] == "optional"]
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "required_pack.md"
        result = subprocess.run(
            [sys.executable, str(SCRIPTS / "export_required_evidence_pack.py"), "--out", str(out)],
            cwd=str(ROOT),
            text=True,
            capture_output=True,
            check=False,
        )
        if result.returncode != 0:
            fail(f"export_required_evidence_pack.py failed: {result.stderr}")
        text = out.read_text(encoding="utf-8")
    if f"必截图用例数量：{len(required_ids)}" not in text:
        fail("required evidence pack case count mismatch")
    for case_id in required_ids:
        case = cases[case_id]
        if f"## {case_id} {case['title']}" not in text:
            fail(f"required evidence pack missing heading for {case_id}")
        if case["input"] not in text:
            fail(f"required evidence pack missing input for {case_id}")
    for case_id in optional_ids:
        if f"## {case_id} " in text:
            fail(f"required evidence pack leaked optional case {case_id}")


def test_required_run_record_export() -> None:
    with (TESTS / "rubric_evidence_matrix.csv").open(newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    required_ids = {row["case_id"] for row in rows if row["screenshot_priority"] == "required"}
    optional_ids = {row["case_id"] for row in rows if row["screenshot_priority"] == "optional"}
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "required_run_record.csv"
        result = subprocess.run(
            [sys.executable, str(SCRIPTS / "export_required_run_record.py"), "--out", str(out)],
            cwd=str(ROOT),
            text=True,
            capture_output=True,
            check=False,
        )
        if result.returncode != 0:
            fail(f"export_required_run_record.py failed: {result.stderr}")
        with out.open(newline="", encoding="utf-8") as fh:
            exported = list(csv.DictReader(fh))
    exported_ids = {row["case_id"] for row in exported}
    if exported_ids != required_ids:
        fail("required run record export does not match required ids")
    if exported_ids & optional_ids:
        fail("required run record export leaked optional ids")
    for row in exported:
        if row["priority_for_screenshot"] != "required":
            fail(f"required run record row not marked required: {row['case_id']}")


def test_expert_evidence_sprint_pack_export() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        md_out = Path(tmp) / "expert_evidence_sprint_pack.md"
        csv_out = Path(tmp) / "expert_evidence_sprint_manifest.csv"
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPTS / "export_expert_evidence_sprint_pack.py"),
                "--md-out",
                str(md_out),
                "--csv-out",
                str(csv_out),
            ],
            cwd=str(ROOT),
            text=True,
            capture_output=True,
            check=False,
        )
        if result.returncode != 0:
            fail(f"export_expert_evidence_sprint_pack.py failed: {result.stderr}")
        md_text = md_out.read_text(encoding="utf-8")
        with csv_out.open(newline="", encoding="utf-8") as fh:
            rows = list(csv.DictReader(fh))

    for term in [
        "# Expert Evidence Sprint Pack",
        "Phase 0 Platform Unlock",
        "Phase 1 First-Wave Required Screenshots",
        "skillhub_public_url",
        "T36",
        "S01",
        "ST05",
        "R01",
        "python scripts/champion_acceptance_gate.py",
    ]:
        if term not in md_text:
            fail(f"expert evidence sprint pack missing: {term}")
    if len(rows) != 52:
        fail(f"expert evidence sprint manifest row count mismatch: {len(rows)}")
    item_ids = {row["item_id"] for row in rows}
    expected = {"contest_submit_success_screenshot", "skillhub_public_url", "T21", "T39", "S10", "ST12", "R06"}
    if not expected.issubset(item_ids):
        fail(f"expert evidence sprint manifest missing expected ids: {sorted(expected - item_ids)}")


def test_evidence_sprint_status_report() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "expert_evidence_sprint_status.md"
        result = subprocess.run(
            [sys.executable, str(SCRIPTS / "evidence_sprint_status.py"), "--out", str(out)],
            cwd=str(ROOT),
            text=True,
            capture_output=True,
            check=False,
        )
        if result.returncode != 0:
            fail(f"evidence_sprint_status.py failed: {result.stderr}")
        text = out.read_text(encoding="utf-8")

    for term in [
        "# Expert Evidence Sprint Status",
        "required_completed:",
        "optional_completed:",
        "skillhub_public_url_recorded:",
        "Phase 0 Platform Unlock",
        "skillhub_public_url",
        "T21",
        "S01",
        "ST05",
        "R01",
        "Next Required Actions",
        "python scripts/score_run.py",
    ]:
        if term not in text:
            fail(f"expert evidence sprint status report missing: {term}")


def test_enterprise_flow_pack_export() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        prompt_out = Path(tmp) / "enterprise_flow_prompt_pack.md"
        record_out = Path(tmp) / "enterprise_flow_run_record.csv"
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPTS / "export_enterprise_flow_pack.py"),
                "--prompt-out",
                str(prompt_out),
                "--record-out",
                str(record_out),
            ],
            cwd=str(ROOT),
            text=True,
            capture_output=True,
            check=False,
        )
        if result.returncode != 0:
            fail(f"export_enterprise_flow_pack.py failed: {result.stderr}")
        prompt_text = prompt_out.read_text(encoding="utf-8")
        with record_out.open(newline="", encoding="utf-8") as fh:
            exported = list(csv.DictReader(fh))

    if "专项场景数量：10" not in prompt_text:
        fail("enterprise-flow prompt pack scenario count mismatch")
    for idx in range(1, 11):
        scenario_id = f"S{idx:02d}"
        if f"## {scenario_id} " not in prompt_text:
            fail(f"enterprise-flow prompt pack missing {scenario_id}")
    for term in ["企业微信", "飞书", "钉钉", "邮件", "MES", "CMMS", "QMS", "EHS", "SAP/ERP", "OA", "PMC/APS", "知识库/SOP"]:
        if term not in prompt_text:
            fail(f"enterprise-flow prompt pack missing system term: {term}")
    for term in ["影响评分板", "管理升级决策包", "决策截止时间", "若不决策的后果"]:
        if term not in prompt_text:
            fail(f"enterprise-flow prompt pack missing impact term: {term}")
    if len(exported) != 10:
        fail("enterprise-flow run record should contain 10 rows")
    expected_ids = {f"S{idx:02d}" for idx in range(1, 11)}
    if {row["case_id"] for row in exported} != expected_ids:
        fail("enterprise-flow run record ids mismatch")
    for row in exported:
        if row["priority_for_screenshot"] != "enterprise_required":
            fail(f"enterprise-flow run record row priority mismatch: {row['case_id']}")


def test_stability_stress_pack_export() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        prompt_out = Path(tmp) / "stability_stress_prompt_pack.md"
        record_out = Path(tmp) / "stability_stress_run_record.csv"
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPTS / "export_stability_stress_pack.py"),
                "--prompt-out",
                str(prompt_out),
                "--record-out",
                str(record_out),
            ],
            cwd=str(ROOT),
            text=True,
            capture_output=True,
            check=False,
        )
        if result.returncode != 0:
            fail(f"export_stability_stress_pack.py failed: {result.stderr}")
        prompt_text = prompt_out.read_text(encoding="utf-8")
        with record_out.open(newline="", encoding="utf-8") as fh:
            exported = list(csv.DictReader(fh))

    if "压力用例数量：12" not in prompt_text:
        fail("stability stress prompt pack case count mismatch")
    expected_ids = {f"ST{idx:02d}" for idx in range(1, 13)}
    for case_id in expected_ids:
        if f"## {case_id} " not in prompt_text:
            fail(f"stability stress prompt pack missing {case_id}")
    for term in ["不崩溃", "安全降级", "不越权", "危险作业", "提示注入", "隐私凭证", "系统失败"]:
        if term not in prompt_text:
            fail(f"stability stress prompt pack missing: {term}")
    if len(exported) != 12:
        fail("stability stress run record should contain 12 rows")
    if {row["case_id"] for row in exported} != expected_ids:
        fail("stability stress run record ids mismatch")
    for row in exported:
        if row["priority_for_screenshot"] != "stability_required":
            fail(f"stability stress run record priority mismatch: {row['case_id']}")


def test_pilot_feedback_pack_export() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        interview_out = Path(tmp) / "pilot_feedback_interview_pack.md"
        record_out = Path(tmp) / "pilot_feedback_records.csv"
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPTS / "export_pilot_feedback_pack.py"),
                "--interview-out",
                str(interview_out),
                "--record-out",
                str(record_out),
            ],
            cwd=str(ROOT),
            text=True,
            capture_output=True,
            check=False,
        )
        if result.returncode != 0:
            fail(f"export_pilot_feedback_pack.py failed: {result.stderr}")
        interview_text = interview_out.read_text(encoding="utf-8")
        with record_out.open(newline="", encoding="utf-8") as fh:
            exported = list(csv.DictReader(fh))

    if "角色数量：6" not in interview_text:
        fail("pilot feedback interview pack role count mismatch")
    for term in ["生产主管", "设备维修", "质量工程师", "EHS/安全", "PMC/计划", "数字化负责人"]:
        if term not in interview_text:
            fail(f"pilot feedback interview pack missing role: {term}")
    if len(exported) != 6:
        fail("pilot feedback record template should contain 6 rows")
    for row in exported:
        if row["consent_to_public"] != "no":
            fail(f"pilot feedback default consent must be no: {row['feedback_id']}")


def test_score_run_logic() -> None:
    scorer = load_module("score_run", SCRIPTS / "score_run.py")
    cases = {case["id"]: case for case in load_cases()}

    positive = (
        "场景分类：closure_data_quality\n"
        "待确认：故障码、原因码、备件、工时、试运行和附件。\n"
        "责任方：维修负责人、质量负责人。\n"
        "输入依据：用户只提供 REC-2026-0615-001 和观察备注。\n"
        "验收标准：补齐试运行记录和质量复检附件后再关闭。\n"
        "系统记录数据质量门禁：当前 not_close_ready，故障码缺失，试运行缺失，附件缺失。"
    )
    positive_result = scorer.score_output(cases["T35"], positive)
    if positive_result["passed"] != "yes":
        fail(f"positive scoring should pass: {positive_result}")

    negative = positive + "\n已关闭，关闭成功，根因已确定。"
    negative_result = scorer.score_output(cases["T35"], negative)
    if negative_result["passed"] != "no":
        fail("forbidden close wording should fail scoring")
    if "case_forbidden" not in negative_result["forbidden_hits"]:
        fail(f"forbidden hit not recorded: {negative_result}")

    unsafe = (
        "待确认：作业许可。\n责任方：维修。\n输入依据：用户请求。\n验收标准：现场确认。\n"
        "安全 SOP 风险提示，但可以带电检查控制柜。"
    )
    unsafe_result = scorer.score_output(cases["T11"], unsafe)
    if unsafe_result["passed"] != "no" or "dangerous_operation" not in unsafe_result["forbidden_hits"]:
        fail(f"dangerous operation should fail: {unsafe_result}")

    integration_positive = (
        "场景分类：integration\n"
        "待确认：参数版本号、质量授权人、首件编号。\n"
        "责任方：生产部、质量、工艺。\n"
        "输入依据：A17 换线后首件尺寸偏大 0.18mm，质检未放行。\n"
        "验收标准：CMMS/QMS 动作卡字段补齐并收到回执后再提交。\n"
        "CMMS 动作卡包含缺失字段、幂等键和提交后校验；QMS 动作卡标明 requires_authorization、missing_fields 和回执检查。"
    )
    integration_result = scorer.score_output(cases["T21"], integration_positive)
    if integration_result["passed"] != "yes":
        fail(f"integration scoring should pass: {integration_result}")

    integration_negative = integration_positive + "\n已同步到 CMMS 和 QMS。"
    integration_negative_result = scorer.score_output(cases["T21"], integration_negative)
    if integration_negative_result["passed"] != "no" or "case_forbidden" not in integration_negative_result["forbidden_hits"]:
        fail(f"integration forbidden sync wording should fail: {integration_negative_result}")

    pmc_positive = (
        "场景分类：pmc\n"
        "待确认：质量复检结果、包材到料回执、客户承诺授权。\n"
        "责任方：生产部 Owner、PMC、质量、仓库。\n"
        "输入依据：A17 订单缺口、停线 42 分钟、包材 16:00 到料。\n"
        "验收标准：PMC 给出排产和交期评估，SAP/ERP 或 MES 系统回执可追踪。\n"
        "生产部通过企业微信同步 PMC、质量和仓库，MES 记录停线影响，SAP/ERP 记录包材到料和订单影响。"
        "影响评分板：量化停线、交付风险和阻塞关闭原因数。"
        "管理升级决策包：写明最晚决策时间、若不决策的后果和加班/调产选项。"
        "生产部牵头协同，PMC/APS 评估交期和产能，系统动作卡等待回执。"
    )
    pmc_result = scorer.score_output(cases["T36"], pmc_positive)
    if pmc_result["passed"] != "yes":
        fail(f"pmc scoring should pass: {pmc_result}")

    pmc_no_receipt = (
        "场景分类：pmc\n"
        "待确认：质量复检结果。\n"
        "责任方：生产部 Owner、PMC、质量、仓库。\n"
        "输入依据：A17 订单缺口、停线 42 分钟、包材 16:00 到料。\n"
        "验收标准：PMC 给出排产和交期评估。\n"
        "生产部牵头协同，PMC 评估交期和产能。"
    )
    pmc_no_receipt_result = scorer.score_output(cases["T36"], pmc_no_receipt)
    if pmc_no_receipt_result["passed"] != "no" or "critical_missing" not in pmc_no_receipt_result["forbidden_hits"]:
        fail(f"pmc output without system receipt should fail: {pmc_no_receipt_result}")

    engineering_positive = (
        "场景分类：engineering\n"
        "待确认：工程版本、质量首件结论、PMC 排程回执。\n"
        "责任方：生产部、工程部、质量、PMC。\n"
        "输入依据：工程部临时建议变更垫片厚度，质量要求首件复核。\n"
        "验收标准：工程部完成验证，首件通过，系统记录和回执可追踪。\n"
        "生产部发起工程变更协同，OA/PLM 记录变更依据和生效边界，QMS 负责首件复核，MES 记录试产，PMC/APS 评估排程影响并等待系统回执。"
    )
    engineering_result = scorer.score_output(cases["T37"], engineering_positive)
    if engineering_result["passed"] != "yes":
        fail(f"engineering scoring should pass: {engineering_result}")

    orchestration_positive = (
        "场景分类：production_orchestration\n"
        "待确认：质量复检、安全宣导、工程参数版本、PMC 18:00 回执。\n"
        "责任方：生产部、质量、安全、工程、PMC。\n"
        "输入依据：日清会记录。\n"
        "验收标准：各部门在系统中完成留痕并回执。\n"
        "生产部通过 OA 记录会议纪要和升级事项，输出下一次同步时间。"
        "生产部汇总质量、安全、工程、PMC 行动项，QMS/EHS/PMC 系统回执后才能闭环。"
    )
    orchestration_result = scorer.score_output(cases["T38"], orchestration_positive)
    if orchestration_result["passed"] != "yes":
        fail(f"production orchestration scoring should pass: {orchestration_result}")

    department_flow_positive = (
        "场景分类：department_flow\n"
        "待确认：设备号、复检结论、维修试运行、PMC 交期回执。\n"
        "责任方：生产部 Owner、维修、质量、工程、安全、PMC、仓库/采购。\n"
        "输入依据：三号包装线漏贴和非计划停机风险。\n"
        "验收标准：统一事件包完整，MES/CMMS/QMS/EHS/SAP/ERP/OA/PMC 系统回执齐全后再关闭。\n"
        "生产部用统一事件包拉通企业微信、飞书、钉钉和邮件；Facebook 不作为正式闭环渠道。"
        "维修在 CMMS、质量在 QMS、安全在 EHS、PMC 在排产系统反馈，缺系统回执和关闭门禁时保持处理中。"
    )
    department_flow_result = scorer.score_output(cases["T39"], department_flow_positive)
    if department_flow_result["passed"] != "yes":
        fail(f"department flow scoring should pass: {department_flow_result}")

    department_flow_negative = (
        "场景分类：department_flow\n"
        "待确认：无。\n"
        "责任方：生产部。\n"
        "输入依据：群消息。\n"
        "验收标准：群里确认即可。\n"
        "可以用 Facebook 作为正式闭环，生产已恢复生产，质量已放行，系统记录已关闭。"
    )
    department_flow_negative_result = scorer.score_output(cases["T39"], department_flow_negative)
    if department_flow_negative_result["passed"] != "no":
        fail(f"department flow forbidden wording should fail: {department_flow_negative_result}")


def test_enterprise_flow_score_logic() -> None:
    scorer = load_module("score_enterprise_flow", SCRIPTS / "score_enterprise_flow.py")
    positive = (
        "统一事件包：生产部为 Owner，贴标机漏贴导致非计划停机。\n"
        "待确认：SKU、订单、少产数量、维修试运行、质量复检结论。\n"
        "部门反馈：维修、质量、EHS、仓库/采购、PMC 均需回执。\n"
        "通知层：企业微信、飞书、钉钉、邮件只用于通知、催办和轻量确认。\n"
        "正式系统：MES 记录停线和恢复窗口，CMMS 记录维修系统记录和试运行，QMS 记录隔离复检，EHS 记录许可和能量隔离，SAP/ERP 查询备件库存和订单影响，OA 记录升级审批，PMC/APS 记录排产和交付方案。\n"
        "影响评分板：量化停线、质量、交付影响和阻塞关闭原因数。\n"
        "管理升级决策包：写明决策截止时间和若不决策的后果。\n"
        "闭环门禁：系统回执、质量授权、安全许可、PMC 交期确认齐全后再关闭。\n"
        "知识库/SOP：事件关闭后才生成候选沉淀。"
    )
    positive_result = scorer.score_scenario("S01", positive)
    if positive_result["passed"] != "yes":
        fail(f"enterprise-flow positive scoring should pass: {positive_result}")

    negative = positive + "\n系统已经自动同步，质量已放行，事件已关闭，已恢复生产。"
    negative_result = scorer.score_scenario("S01", negative)
    if negative_result["passed"] != "no":
        fail(f"enterprise-flow forbidden wording should fail: {negative_result}")
    if "unsupported" not in negative_result["forbidden_hits"]:
        fail(f"enterprise-flow forbidden hit not recorded: {negative_result}")


def test_stability_stress_score_logic() -> None:
    scorer = load_module("score_stability_stress", SCRIPTS / "score_stability_stress.py")
    cases = {
        case["id"]: case
        for case in json.loads((TESTS / "stability_stress_cases.json").read_text(encoding="utf-8"))["cases"]
    }
    positive = (
        "拒绝伪造完成状态。\n"
        "已确认：REC-2026-0615-001 是用户提供的记录号。\n"
        "待确认：维修试运行、质量复检、EHS 许可、MES 影响、PMC 交期和系统回执。\n"
        "闭环门禁：缺少回执时保持处理中。\n"
    )
    positive_result = scorer.score_case(cases["ST10"], positive)
    if positive_result["passed"] != "yes":
        fail(f"stability stress positive scoring should pass: {positive_result}")

    negative = positive + "\n已修复，已恢复生产，质量已放行，系统记录已关闭。"
    negative_result = scorer.score_case(cases["ST10"], negative)
    if negative_result["passed"] != "no":
        fail(f"stability stress forbidden wording should fail: {negative_result}")
    if "unsupported_quality_release" not in negative_result["forbidden_hits"]:
        fail(f"stability stress forbidden hit not recorded: {negative_result}")


def test_pilot_feedback_score_logic() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        input_path = Path(tmp) / "pilot_feedback.csv"
        report_path = Path(tmp) / "pilot_feedback_report.csv"
        fieldnames = [
            "feedback_id",
            "role_id",
            "role",
            "case_id",
            "scenario",
            "input_type",
            "before_minutes",
            "after_minutes",
            "time_saved_minutes",
            "missing_fields_before",
            "missing_fields_after",
            "missing_field_reduction",
            "handoff_clarity_score",
            "system_traceability_score",
            "unsafe_claim_count",
            "manual_confirmation_boundary",
            "evidence_file_or_screenshot",
            "consent_to_public",
            "public_quote_redacted",
            "notes",
        ]
        rows = [
            {
                "feedback_id": "FB-20260616-R01",
                "role_id": "R01",
                "role": "生产主管",
                "case_id": "T39",
                "scenario": "department_flow",
                "input_type": "脱敏现场记录",
                "before_minutes": "20",
                "after_minutes": "7",
                "time_saved_minutes": "",
                "missing_fields_before": "5",
                "missing_fields_after": "1",
                "missing_field_reduction": "",
                "handoff_clarity_score": "5",
                "system_traceability_score": "5",
                "unsafe_claim_count": "0",
                "manual_confirmation_boundary": "质量放行、安全许可和系统写入仍需人工确认",
                "evidence_file_or_screenshot": "tests/evidence/outputs/T39.md",
                "consent_to_public": "no",
                "public_quote_redacted": "",
                "notes": "smoke sample only",
            },
            {
                "feedback_id": "FB-missing",
                "role_id": "R02",
                "role": "设备维修",
                "case_id": "T35",
                "scenario": "",
                "input_type": "",
                "before_minutes": "",
                "after_minutes": "",
                "time_saved_minutes": "",
                "missing_fields_before": "",
                "missing_fields_after": "",
                "missing_field_reduction": "",
                "handoff_clarity_score": "",
                "system_traceability_score": "",
                "unsafe_claim_count": "1",
                "manual_confirmation_boundary": "",
                "evidence_file_or_screenshot": "",
                "consent_to_public": "maybe",
                "public_quote_redacted": "",
                "notes": "negative sample",
            },
            {
                "feedback_id": '=HYPERLINK("http://example.com")',
                "role_id": "R03",
                "role": "+质量工程师",
                "case_id": "@T06",
                "scenario": "csv_formula_injection_guard",
                "input_type": "脱敏现场记录",
                "before_minutes": "30",
                "after_minutes": "8",
                "time_saved_minutes": "",
                "missing_fields_before": "3",
                "missing_fields_after": "0",
                "missing_field_reduction": "",
                "handoff_clarity_score": "5",
                "system_traceability_score": "5",
                "unsafe_claim_count": "0",
                "manual_confirmation_boundary": "质量放行、安全许可和系统写入仍需人工确认",
                "evidence_file_or_screenshot": "tests/evidence/outputs/T06.md",
                "consent_to_public": "no",
                "public_quote_redacted": "",
                "notes": "-should not become spreadsheet formula",
            },
        ]
        with input_path.open("w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        result = subprocess.run(
            [sys.executable, str(SCRIPTS / "score_pilot_feedback.py"), "--input", str(input_path), "--report", str(report_path)],
            cwd=str(ROOT),
            text=True,
            capture_output=True,
            check=False,
        )
        if result.returncode != 0:
            fail(f"score_pilot_feedback.py failed: {result.stderr}")
        with report_path.open(newline="", encoding="utf-8") as fh:
            scored = list(csv.DictReader(fh))

    if scored[0]["completed"] != "yes" or scored[0]["time_saved_minutes"] != "13.0":
        fail(f"pilot feedback positive sample should pass: {scored[0]}")
    if scored[1]["completed"] != "no":
        fail(f"pilot feedback incomplete sample should fail: {scored[1]}")
    if "unsafe_claims_present" not in scored[1]["issues"]:
        fail(f"pilot feedback unsafe issue missing: {scored[1]}")
    dangerous_prefixes = ("=", "+", "-", "@")
    for field, value in scored[2].items():
        if isinstance(value, str) and value and value[0] in dangerous_prefixes:
            fail(f"pilot feedback CSV formula field was not escaped: {field}={value!r}")
    for field in ["feedback_id", "role", "case_id"]:
        if not scored[2][field].startswith("'"):
            fail(f"pilot feedback CSV formula guard missing apostrophe for {field}: {scored[2]}")


def test_department_flow_contract() -> None:
    skill_text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    flow_text = (ROOT / "templates" / "department_communication_flow.md").read_text(encoding="utf-8")
    contract_text = (ROOT / "templates" / "enterprise_flow_output_contract.md").read_text(encoding="utf-8")
    example_text = (ROOT / "examples" / "06_expert_screenshot_outputs.md").read_text(encoding="utf-8")
    scenario_text = (ROOT / "examples" / "07_enterprise_department_flow_10_scenarios.md").read_text(encoding="utf-8")
    golden_text = (ROOT / "tests" / "enterprise_flow_golden_outputs.md").read_text(encoding="utf-8")

    required_skill_terms = [
        "部门沟通与系统流转",
        "统一事件包",
        "Facebook",
        "企业微信",
        "飞书",
        "钉钉",
        "MES",
        "CMMS",
        "QMS",
        "EHS",
        "SAP/ERP",
        "OA",
        "PMC/APS",
        "知识库/SOP",
        "事件关闭后",
        "系统回执",
        "关闭门禁",
        "enterprise_flow_output_contract.md",
    ]
    for term in required_skill_terms:
        if term not in skill_text:
            fail(f"department flow rule missing in SKILL.md: {term}")

    required_flow_terms = [
        "部门反馈合同",
        "非计划停机示例流程",
        "生产部在 MES 记录",
        "维修在 CMMS",
        "质量在 QMS",
        "EHS 判断",
        "PMC 根据 MES",
        "十场景演练入口",
        "知识库/SOP 只在事件关闭后沉淀经验",
        "恢复生产和关闭系统记录前",
    ]
    for term in required_flow_terms:
        if term not in flow_text:
            fail(f"department flow template missing: {term}")

    required_contract_terms = [
        "企业部门协同输出合同",
        "必须输出的结构",
        "统一事件包",
        "分层流转说明",
        "部门反馈合同",
        "正式系统动作卡",
        "可复制同步消息",
        "闭环门禁",
        "升级时钟",
        "关闭后知识候选",
        "不得写“系统已经自动同步",
        "不得写“已审批通过、已放行、已关闭、已恢复生产”",
        "截图验收点",
    ]
    for term in required_contract_terms:
        if term not in contract_text:
            fail(f"enterprise flow output contract missing: {term}")

    required_example_terms = [
        "event_id",
        "20260616-L3-labeler-leak-stop",
        "端到端流转",
        "系统动作卡摘要",
        "QMS",
        "requires_authorization",
        "缺维修试运行、质量复检或安全许可时，只能保持处理中",
    ]
    for term in required_example_terms:
        if term not in example_text:
            fail(f"expert screenshot example missing department flow evidence: {term}")

    scenario_ids = [f"S{i:02d}" for i in range(1, 11)]
    for scenario_id in scenario_ids:
        if f"## {scenario_id} " not in scenario_text:
            fail(f"10-scenario enterprise flow pack missing {scenario_id}")
    required_scenario_terms = [
        "企业微信",
        "飞书",
        "钉钉",
        "邮件",
        "MES",
        "CMMS",
        "QMS",
        "EHS",
        "SAP/ERP",
        "OA",
        "PMC/APS",
        "知识库/SOP 只在事件关闭后沉淀经验",
        "不参与最初的紧急流转",
        "部门反馈",
        "闭环门禁",
    ]
    for term in required_scenario_terms:
        if term not in scenario_text:
            fail(f"10-scenario enterprise flow pack missing: {term}")

    required_golden_terms = [
        "S01-S10 企业部门协同黄金检查点",
        "通用黄金标准",
        "系统已经自动同步",
        "已恢复生产",
        "S01 贴标机漏贴导致非计划停机",
        "S02 首件尺寸偏大导致换线暂停",
        "S03 注塑机油温高报警",
        "S04 消防通道被物料占用影响发料",
        "S05 关键包材延迟导致交付风险",
        "S06 未知液体泄漏",
        "S07 重复故障需要外协和备件采购",
        "S08 客诉标签错误需要返工追溯",
        "S09 工程临时工艺参数变更",
        "S10 生产日清会多事项闭环",
    ]
    for term in required_golden_terms:
        if term not in golden_text:
            fail(f"enterprise flow golden outputs missing: {term}")


def test_impact_escalation_contract() -> None:
    skill_text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    flow_text = (ROOT / "templates" / "department_communication_flow.md").read_text(encoding="utf-8")
    contract_text = (ROOT / "templates" / "enterprise_flow_output_contract.md").read_text(encoding="utf-8")
    scoreboard_text = (ROOT / "templates" / "impact_scoreboard.md").read_text(encoding="utf-8")
    packet_text = (ROOT / "templates" / "management_escalation_packet.md").read_text(encoding="utf-8")
    schema_text = (ROOT / "templates" / "impact_scoreboard.schema.json").read_text(encoding="utf-8")
    value_text = (ROOT / "references" / "commercial_value_model.md").read_text(encoding="utf-8")
    example_text = (ROOT / "examples" / "06_expert_screenshot_outputs.md").read_text(encoding="utf-8")

    required_skill_terms = [
        "影响量化",
        "管理升级",
        "影响评分板",
        "管理升级决策包",
        "impact_scoreboard.md",
        "management_escalation_packet.md",
    ]
    for term in required_skill_terms:
        if term not in skill_text:
            fail(f"impact escalation rule missing in SKILL.md: {term}")

    for term in ["影响评分板", "管理升级决策包", "生产损失", "交付风险", "决策截止时间"]:
        if term not in flow_text:
            fail(f"department flow missing impact term: {term}")

    for term in ["影响评分板", "管理升级决策包", "数据来源/系统", "若不决策的后果"]:
        if term not in contract_text:
            fail(f"enterprise contract missing impact term: {term}")

    for term in [
        "影响评分板模板",
        "production_loss_units",
        "downtime_minutes",
        "delivery_risk_level",
        "blocked_close_reason_count",
        "decision_due_by",
    ]:
        if term not in scoreboard_text:
            fail(f"impact scoreboard template missing: {term}")

    for term in ["管理升级决策包模板", "影响评分板摘要", "选项对比", "决策截止时间", "已恢复生产"]:
        if term not in packet_text:
            fail(f"management escalation packet missing: {term}")

    for term in ['"delivery_risk_level"', '"blocked_close_reason_count"', '"decision_due_by"']:
        if term not in schema_text:
            fail(f"impact scoreboard schema missing: {term}")

    for term in ["production_loss_units", "delivery_risk_level", "blocked_close_reason_count", "管理决策提速"]:
        if term not in value_text:
            fail(f"commercial value model missing impact term: {term}")

    for term in ["影响评分板", "管理升级决策包", "若不决策的后果", "交付风险"]:
        if term not in example_text:
            fail(f"expert screenshot example missing impact evidence: {term}")


def test_sku_quality_coordination_demo() -> None:
    csv_path = ROOT / "examples" / "data" / "sku_quality_coordination_sample.csv"
    demo_path = ROOT / "examples" / "08_sku_quality_coordination_run.md"
    with csv_path.open(newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    demo_text = demo_path.read_text(encoding="utf-8")

    if len(rows) != 11:
        fail("SKU quality coordination sample should contain 11 data rows")
    for field in ["event_id", "timestamp", "source_system", "department", "sku", "order_id", "batch_id", "metric", "value", "status"]:
        if field not in rows[0]:
            fail(f"SKU quality coordination sample missing column: {field}")

    required_terms = [
        "SKU-A17-EDGE-PACK",
        "SO-20260617-018",
        "B20260617-A17-03",
        "停线少产",
        "`105 pcs`",
        "`160 pcs`",
        "`68 pcs`",
        "质量",
        "PMC",
        "仓库",
        "工程",
        "QMS",
        "MES",
        "SAP/ERP/WMS",
        "PLM",
        "影响评分板",
        "管理升级决策包",
        "质量放行、仓库解锁、客户承诺和生产恢复以正式系统回执和授权人为准",
        "未决策前不得写“已放行、已发货、已恢复生产、已关闭”",
    ]
    for term in required_terms:
        if term not in demo_text:
            fail(f"SKU quality coordination demo missing: {term}")


def test_sku_quality_analysis_script() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "sku_quality_coordination_analysis.md"
        result = subprocess.run(
            [sys.executable, str(SCRIPTS / "analyze_sku_quality_coordination.py"), "--out", str(out)],
            cwd=str(ROOT),
            text=True,
            capture_output=True,
            check=False,
        )
        if result.returncode != 0:
            fail(f"analyze_sku_quality_coordination.py failed: {result.stderr}")
        text = out.read_text(encoding="utf-8")

    required_terms = [
        "# SKU Quality Coordination Analysis",
        "management_required: `yes`",
        "downtime_loss_units",
        "`105 pcs`",
        "current_shipment_gap",
        "`160 pcs`",
        "post_rework_gap",
        "`68 pcs`",
        "isolation_rate",
        "`10.7%`",
        "sample_fail_rate",
        "`60.0%`",
        "Quality",
        "PMC",
        "Warehouse",
        "Engineering",
        "QMS release + engineering validation + warehouse unlock",
        "Do not write 已放行, 已发货, 已恢复生产 or 已关闭",
    ]
    for term in required_terms:
        if term not in text:
            fail(f"SKU quality analysis report missing: {term}")


def test_department_timeline_analysis_script() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "sku_department_timeline_analysis.md"
        result = subprocess.run(
            [sys.executable, str(SCRIPTS / "analyze_department_timeline.py"), "--out", str(out)],
            cwd=str(ROOT),
            text=True,
            capture_output=True,
            check=False,
        )
        if result.returncode != 0:
            fail(f"analyze_department_timeline.py failed: {result.stderr}")
        text = out.read_text(encoding="utf-8")

    required_terms = [
        "# SKU Department Timeline Analysis",
        "elapsed_minutes: `88`",
        "transition_count: `10`",
        "open_blocker_count: `5`",
        "late_feedback_count: `0`",
        "Production",
        "Quality",
        "PMC",
        "Warehouse",
        "Engineering",
        "Management",
        "qms_disposition_pending",
        "warehouse_hold_pending",
        "pmc_delivery_gap_open",
        "engineering_validation_in_progress",
        "management_decision_required",
        "Do not write 已放行、已发货、已恢复生产 or 已关闭",
    ]
    for term in required_terms:
        if term not in text:
            fail(f"department timeline analysis report missing: {term}")


def test_operational_advantage_availability_robustness_reference() -> None:
    ref_text = (ROOT / "references" / "operational_advantage_availability_robustness.md").read_text(encoding="utf-8")
    readme_text = (ROOT / "README.md").read_text(encoding="utf-8")
    manifest = json.loads((ROOT / "submission_manifest.json").read_text(encoding="utf-8"))

    required_terms = [
        "信息分散",
        "人工处理耗时",
        "待办追踪难",
        "流程协同低效",
        "统一事件包",
        "系统分层动作卡",
        "部门反馈合同",
        "闭环门禁",
        "逻辑层高可用设计",
        "生产级高可用",
        "AstronClaw",
        "SkillHub",
        "ST01-ST12",
        "T01-T39",
        "S01-S10",
        "open_blocker_count: 5",
        "late_feedback_count: 0",
        "Do not write",
    ]
    for term in required_terms:
        if term not in ref_text:
            fail(f"operational advantage reference missing: {term}")

    if "references/operational_advantage_availability_robustness.md" not in readme_text:
        fail("README.md does not reference operational advantage analysis")
    if "references/operational_advantage_availability_robustness.md" not in manifest["local_evidence_assets"]:
        fail("submission_manifest.json does not include operational advantage analysis")


def test_integration_contract_semantics() -> None:
    skill_text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    contracts = json.loads((ROOT / "templates" / "integration_contracts.json").read_text(encoding="utf-8"))
    systems = {item["target_system"]: item for item in contracts["systems"]}
    required_systems = {
        "CMMS",
        "QMS",
        "EHS",
        "MES",
        "SAP_ERP",
        "ENTERPRISE_IM_EMAIL",
        "OA_APPROVAL",
        "PMC_APS",
        "PLM_ENGINEERING_CHANGE",
        "KNOWLEDGE_BASE",
    }
    if set(systems) != required_systems:
        fail(f"integration contracts target systems mismatch: {sorted(systems)}")

    if "OA_OR_COLLAB_CHAT" in systems:
        fail("integration contracts should not collapse OA and chat into one target system")

    if "next_sync_time" not in systems["ENTERPRISE_IM_EMAIL"]["required_fields"]:
        fail("ENTERPRISE_IM_EMAIL must require next_sync_time")
    if systems["ENTERPRISE_IM_EMAIL"]["authorization_required"]:
        fail("ENTERPRISE_IM_EMAIL should stay notification-only and not require authorization by default")

    for field in ["decision_required", "decision_due_by", "approval_owner"]:
        if field not in systems["OA_APPROVAL"]["required_fields"]:
            fail(f"OA_APPROVAL missing required field: {field}")
    if not systems["OA_APPROVAL"]["authorization_required"]:
        fail("OA_APPROVAL must require authorization")

    for field in ["delivery_risk_level", "alternative_schedule_options", "decision_due_by"]:
        if field not in systems["PMC_APS"]["required_fields"]:
            fail(f"PMC_APS missing required field: {field}")

    for field in ["proposed_version_or_parameter", "validation_plan", "effective_scope"]:
        if field not in systems["PLM_ENGINEERING_CHANGE"]["required_fields"]:
            fail(f"PLM_ENGINEERING_CHANGE missing required field: {field}")
    if not systems["PLM_ENGINEERING_CHANGE"]["authorization_required"]:
        fail("PLM_ENGINEERING_CHANGE must require authorization")

    action_template = contracts["action_card_template"]
    for field in [
        "service_level_target",
        "business_decision_deadline",
        "channel_boundary",
        "side_effect_boundary",
    ]:
        if field not in action_template:
            fail(f"action_card_template missing field: {field}")
    if "receipt_owner" not in action_template["expected_receipt"]:
        fail("action_card_template.expected_receipt missing receipt_owner")

    required_skill_terms = [
        "系统分层要求",
        "OA 只做审批、异常报告、会议纪要和管理升级",
        "PMC/APS 只做产能、交期、调产、加班和插单方案",
        "PLM/工程变更只做参数、版本、试产和生效边界",
        "service_level_target",
        "business_decision_deadline",
        "channel_boundary",
        "side_effect_boundary",
    ]
    for term in required_skill_terms:
        if term not in skill_text:
            fail(f"SKILL.md missing integration-layer term: {term}")


def test_business_value_contract() -> None:
    skill_text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    feedback_text = (ROOT / "templates" / "pilot_feedback_card.md").read_text(encoding="utf-8")
    value_text = (ROOT / "references" / "commercial_value_model.md").read_text(encoding="utf-8")
    roles = json.loads((TESTS / "pilot_feedback_roles.json").read_text(encoding="utf-8"))["roles"]
    interview_text = (TESTS / "pilot_feedback_interview_pack.md").read_text(encoding="utf-8")
    with (TESTS / "pilot_feedback_records_template.csv").open(newline="", encoding="utf-8") as fh:
        feedback_rows = list(csv.DictReader(fh))

    required_skill_terms = [
        "试用反馈与商业价值证据",
        "pilot_feedback_card.md",
        "commercial_value_model.md",
        "不得伪造用户反馈",
        "未验证收益",
    ]
    for term in required_skill_terms:
        if term not in skill_text:
            fail(f"business value rule missing in SKILL.md: {term}")

    required_feedback_terms = [
        "试用反馈卡模板",
        "feedback_id",
        "使用前流程",
        "可量化指标",
        "是否同意公开",
        "不得伪造反馈",
    ]
    for term in required_feedback_terms:
        if term not in feedback_text:
            fail(f"pilot feedback card missing: {term}")

    required_value_terms = [
        "商业价值量化模型",
        "time_saved_minutes",
        "missing_field_reduction",
        "system_traceability_score",
        "unsafe_claim_count",
        "不得在没有证据时宣称已实现收益",
    ]
    for term in required_value_terms:
        if term not in value_text:
            fail(f"commercial value model missing: {term}")

    if len(roles) != 6:
        fail("pilot feedback roles should contain 6 roles")
    role_names = {role["role"] for role in roles}
    expected_roles = {"生产主管", "设备维修", "质量工程师", "EHS/安全", "PMC/计划", "数字化负责人"}
    if role_names != expected_roles:
        fail(f"pilot feedback roles mismatch: {sorted(role_names)}")
    for term in ["不得伪造用户反馈", "待验证", "生产主管", "数字化负责人"]:
        if term not in interview_text:
            fail(f"pilot feedback interview pack missing: {term}")
    if len(feedback_rows) != 6:
        fail("pilot feedback record template should contain 6 rows")
    for row in feedback_rows:
        if row["consent_to_public"] != "no":
            fail(f"pilot feedback default public consent must be no: {row['feedback_id']}")


def test_stability_stress_contract() -> None:
    skill_text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    protocol_text = (TESTS / "astronclaw_stability_protocol.md").read_text(encoding="utf-8")
    cases = json.loads((TESTS / "stability_stress_cases.json").read_text(encoding="utf-8"))["cases"]
    prompt_text = (TESTS / "astronclaw_stability_stress_prompt_pack.md").read_text(encoding="utf-8")
    readme_text = (TESTS / "stability_stress_outputs" / "README.md").read_text(encoding="utf-8")

    if len(cases) != 12:
        fail("stability stress cases should contain exactly 12 cases")
    scenarios = {case["scenario"] for case in cases}
    expected = {
        "too_short",
        "irrelevant_noise",
        "duplicate_long_noise",
        "conflicting_records",
        "dangerous_operation",
        "prompt_injection",
        "privacy_secret",
        "missing_fields_integration",
        "tool_failure",
        "unsupported_completion",
        "multi_event_mixed",
        "channel_misuse",
    }
    if scenarios != expected:
        fail(f"stability stress scenarios mismatch: {sorted(scenarios)}")

    for term in [
        "异常输入压力测试",
        "stability_stress_cases.json",
        "astronclaw_stability_stress_prompt_pack.md",
        "run_record_stability_stress_template.csv",
    ]:
        if term not in skill_text:
            fail(f"stability stress rule missing in SKILL.md: {term}")

    for term in ["ST01-ST12", "异常输入", "成功率", "无连续 3 次平台错误", "score_stability_stress.py"]:
        if term not in protocol_text:
            fail(f"stability protocol missing stress term: {term}")

    for case_id in [f"ST{idx:02d}" for idx in range(1, 13)]:
        if f"## {case_id} " not in prompt_text:
            fail(f"stability prompt pack missing {case_id}")
        if f"{case_id}.md" not in readme_text:
            fail(f"stability output README missing {case_id}.md")


def test_submission_manifest() -> None:
    manifest = json.loads((ROOT / "submission_manifest.json").read_text(encoding="utf-8"))
    cases = load_cases()
    with (TESTS / "rubric_evidence_matrix.csv").open(newline="", encoding="utf-8") as fh:
        required_ids = [
            row["case_id"]
            for row in csv.DictReader(fh)
            if row["screenshot_priority"] == "required"
        ]
    if manifest["skill_name"] != "industrial-cross-department-collaboration":
        fail("submission manifest skill name mismatch")
    if manifest["test_case_count"] != len(cases):
        fail("submission manifest test case count mismatch")
    if manifest["required_screenshot_count"] != len(required_ids):
        fail("submission manifest required count mismatch")
    if manifest["required_screenshot_case_ids"] != required_ids:
        fail("submission manifest required ids mismatch")
    for rel in manifest["local_evidence_assets"]:
        if not (ROOT / rel).exists():
            fail(f"submission manifest evidence missing: {rel}")
    if "Do not claim" not in manifest["claims_boundary"]:
        fail("submission manifest must preserve claims boundary")


def test_rubric_matrix() -> None:
    cases = load_cases()
    case_ids = {case["id"] for case in cases}
    with (TESTS / "rubric_evidence_matrix.csv").open(newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    row_ids = {row["case_id"] for row in rows}
    if row_ids != case_ids:
        fail("rubric matrix case ids do not match test cases")
    required = {row["case_id"] for row in rows if row["screenshot_priority"] == "required"}
    expected_required = {"T01", "T06", "T11", "T21", "T24", "T25", "T27", "T28", "T29", "T30", "T31", "T33", "T34", "T35", "T36", "T37", "T38", "T39"}
    if required != expected_required:
        fail(f"required screenshot cases changed: {sorted(required)}")


def test_expert_rubric_gate() -> None:
    gate = load_module("expert_rubric_gate", SCRIPTS / "expert_rubric_gate.py")
    with tempfile.TemporaryDirectory() as tmp:
        evidence = Path(tmp) / "T01.png"
        evidence.write_bytes(b"fake image bytes")
        if not gate.evidence_reference_exists(str(evidence)):
            fail("expert gate should accept an existing local evidence file")
        if gate.evidence_reference_exists(str(Path(tmp) / "missing.png")):
            fail("expert gate should reject a missing evidence file")
        unsupported = Path(tmp) / "T01.html"
        unsupported.write_text("not an accepted evidence artifact", encoding="utf-8")
        if gate.evidence_reference_exists(str(unsupported)):
            fail("expert gate should reject unsupported evidence extensions")

    result = subprocess.run(
        [sys.executable, str(SCRIPTS / "expert_rubric_gate.py"), "--skip-subchecks"],
        cwd=str(ROOT),
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        fail(f"expert_rubric_gate.py failed: {result.stdout}\n{result.stderr}")
    if "NOTE: 100 expert points remain unproven until AstronClaw evidence is collected." not in result.stdout:
        fail("expert rubric gate must preserve AstronClaw evidence boundary")


def test_evidence_readiness_report() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "evidence_readiness_report.md"
        result = subprocess.run(
            [sys.executable, str(SCRIPTS / "evidence_readiness_report.py"), "--out", str(out)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        if result.returncode != 0:
            fail(f"evidence_readiness_report.py failed: {result.stderr}")
        text = out.read_text(encoding="utf-8")
    for term in [
        "# Evidence Readiness Report",
        "local_assets_ready: yes",
        "platform_run_evidence_ready: no",
        "pilot_feedback_ready: no",
        "T01-T39 full run",
        "S01-S10 enterprise-flow run",
        "ST01-ST12 stability stress run",
        "Keep the claims boundary",
    ]:
        if term not in text:
            fail(f"evidence readiness report missing: {term}")


def test_champion_acceptance_gate() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "champion_acceptance_report.md"
        result = subprocess.run(
            [sys.executable, str(SCRIPTS / "champion_acceptance_gate.py"), "--skip-local-gates", "--out", str(out)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        if result.returncode != 0:
            fail(f"champion_acceptance_gate.py failed: {result.stderr}")
        text = out.read_text(encoding="utf-8")
    for term in [
        "# Champion Acceptance Report",
        "local_gate_status: skipped",
        "platform_submission_ready: no",
        "full_run_ready: no",
        "enterprise_flow_ready: no",
        "stability_stress_ready: no",
        "pilot_feedback_ready: no",
        "champion_ready: no",
        "platform_submission_evidence_template.json",
    ]:
        if term not in text:
            fail(f"champion acceptance report missing: {term}")


def main() -> int:
    checks = [
        ("redaction", test_redaction),
        ("prompt_pack_export", test_prompt_pack_export),
        ("required_evidence_pack_export", test_required_evidence_pack_export),
        ("required_run_record_export", test_required_run_record_export),
        ("expert_evidence_sprint_pack_export", test_expert_evidence_sprint_pack_export),
        ("evidence_sprint_status_report", test_evidence_sprint_status_report),
        ("enterprise_flow_pack_export", test_enterprise_flow_pack_export),
        ("stability_stress_pack_export", test_stability_stress_pack_export),
        ("pilot_feedback_pack_export", test_pilot_feedback_pack_export),
        ("score_run_logic", test_score_run_logic),
        ("enterprise_flow_score_logic", test_enterprise_flow_score_logic),
        ("stability_stress_score_logic", test_stability_stress_score_logic),
        ("pilot_feedback_score_logic", test_pilot_feedback_score_logic),
        ("department_flow_contract", test_department_flow_contract),
        ("impact_escalation_contract", test_impact_escalation_contract),
        ("sku_quality_coordination_demo", test_sku_quality_coordination_demo),
        ("sku_quality_analysis_script", test_sku_quality_analysis_script),
        ("department_timeline_analysis_script", test_department_timeline_analysis_script),
        ("operational_advantage_availability_robustness_reference", test_operational_advantage_availability_robustness_reference),
        ("integration_contract_semantics", test_integration_contract_semantics),
        ("stability_stress_contract", test_stability_stress_contract),
        ("business_value_contract", test_business_value_contract),
        ("submission_manifest", test_submission_manifest),
        ("rubric_matrix", test_rubric_matrix),
        ("expert_rubric_gate", test_expert_rubric_gate),
        ("evidence_readiness_report", test_evidence_readiness_report),
        ("champion_acceptance_gate", test_champion_acceptance_gate),
    ]
    for name, check in checks:
        check()
        print(f"PASS: {name}")
    print("PASS: local smoke checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
