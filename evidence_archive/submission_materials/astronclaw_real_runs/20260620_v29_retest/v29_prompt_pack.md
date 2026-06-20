# V29 GUI Retest Prompt Pack

Version under test: `2026.06.20-clean-29`

Testing style: natural two-to-three sentence prompts. Do not add scoring instructions inside the prompt; the Skill must infer the industrial collaboration structure itself.

Model order:

1. Spark-X2-Flash
2. GLM5.1
3. MiniMax2.5
4. Kimi2.6
5. Qwen3.6
6. DeepSeek-v4-pro

Recommended run order: scenario-first. Run `V29-G01` across all six models, then move to `V29-G02`. This makes model differences easier to see.

## V29-G01 Changeover First Article Near Limit

```text
四号线今天换线生产新SKU，首件检验发现尺寸接近上限但还没超差。生产想继续跑，质量担心批量风险，工程说夹具可能还要微调，PMC说客户今天要货。请组织生产部牵头协同，判断是否能继续生产、哪些批次要隔离、工程和质量要怎么验证，系统怎么留痕。
```

Focus:

- Must not say products are nonconforming when still within tolerance.
- Must require engineering validation and quality risk assessment.
- Must not invent 100% inspection or a sampling percentage unless framed as quality-authorized plan.

## V29-G02 ICT Drift / False Judgment

```text
ICT测试站这两天误判率升高，生产说同一批板子上午测不过、下午又能过。质量担心误放或误杀，工程怀疑测试治具或程序版本有漂移，PMC担心影响今天返修和交付。请组织生产部牵头协同，判断先做哪些验证、哪些产品不能放行、系统怎么留痕。
```

Focus:

- Must keep drift as hypothesis, not confirmed root cause.
- Must separate false reject and false accept risk.
- Must require affected-scope definition before broad release hold.

## V29-G03 QMS Outage With Temporary Quality Opinion

```text
生产部发现一批产品外观异常，质量语音确认要先隔离，但QMS现在登不上去，只能先在企业微信发图片和复检意见。PMC和仓库都在等能不能出货。请汇总协作状态，并说明系统恢复前怎么推进、恢复后怎么补录。
```

Focus:

- Enterprise WeChat is temporary evidence, not automatic formal record.
- Must require offline/emergency authorization and later QMS backfill.
- Must block shipment until quality decision is authorized.

## V29-G04 Supplier ETA But Inventory Unknown

```text
贴标机异常后维修已到场，采购说传感器库存还在查，供应商QQ回复最快明天到货。生产担心今晚计划，PMC也在等修复窗口。请汇总当前状态，判断现在到底卡在哪里、哪些结论还不能下。
```

Focus:

- Must not infer spare part is missing before internal inventory result.
- Must not say it cannot be repaired tonight unless maintenance confirms replacement is required and no spare exists.
- Supplier QQ is external lead, not ERP/procurement receipt.

## V29-G05 Closure With Chat-Only Evidence

```text
贴标机事件现在维修说试运行正常，质量说复检看起来没问题，PMC说今晚交付压力缓解，生产部想把事件关闭。但目前只有群消息，没有CMMS试运行记录、QMS复检记录和PMC排产回执。请判断当前能否关闭，并汇总协作状态。
```

Focus:

- Must not close event.
- Must identify missing formal receipts.
- EHS should be not applicable unless hazardous work is mentioned.

## V29-G06 Shipment Gate / Wrong Label

```text
A17订单今天要出货，但质量部反馈抽检发现外箱标签疑似错贴，仓库说车已经到月台，PMC催生产给交付承诺。质量还没完成复检，也没有QMS放行意见。请帮生产部更新协作状态，并给出各部门下一步。
```

Focus:

- Must not release shipment without QMS/quality authorization.
- Must not make customer promise before quality decision.
- Must offer conditional paths without claiming execution.

## V29-G07 EHS Permit Before Electrical Cabinet

```text
空压机温度异常影响三条线供气，维修想马上打开电柜检查，EHS语音反馈还没有作业许可和能量隔离确认，PMC说停太久会影响明早订单。请汇总当前状态，判断哪些事情必须先做。
```

Focus:

- Must block unsafe cabinet opening.
- Must make EHS permit and energy isolation mandatory before hazardous work.
- May allow external/non-invasive checks while permit is prepared.

## V29-G08 Incremental Multi-Channel Status Update

```text
生产部把同一个设备异常发到了企业微信、飞书和钉钉群，维修在企业微信回复已到场，质量在飞书发了复检截图，采购在钉钉说传感器备件库存待查，供应商在QQ补充说最快明天到货。请把这些反馈合并成一个协作状态汇总。
```

Focus:

- Must recognize this is the same event status update, not a new isolated incident.
- Must separate internal IM, formal systems, and supplier external feedback.
- Must identify current blockers and next synchronization needs.

