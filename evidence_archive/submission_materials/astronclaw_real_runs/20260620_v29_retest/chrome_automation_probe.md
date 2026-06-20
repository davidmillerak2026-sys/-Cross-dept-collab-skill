# Chrome Automation Probe For AstronClaw GUI

Date: 2026-06-20

Purpose: determine whether Codex can directly control the already logged-in Chrome AstronClaw page for full automatic GUI testing.

## Attempted Control Path

The Chrome control plugin requires the Node-backed JavaScript execution tool to load the browser client and talk to the Codex Chrome Extension.

Attempted setup:

```text
import browser-client.mjs
setupBrowserRuntime(...)
agent.browsers.get("extension")
browser.documentation()
```

Observed failure:

```text
codex/sandbox-state-meta: missing field sandboxPolicy
```

Interpretation:

- The failure happens before browser-client can communicate with Chrome.
- This is a Codex runtime/tool metadata issue, not evidence that the AstronClaw page, Chrome profile, extension, or Skill failed.

## Read-Only Chrome Environment Checks

Chrome installed:

```text
Google Chrome 149.0.7827.116
C:\Program Files\Google\Chrome\Application\chrome.exe
```

Chrome running:

```text
running: true
process_name: chrome.exe
```

Codex Chrome Extension:

```text
extensionId: hehggadaopoacecdllhhajmbjkdcmajg
selectedProfileDirectory: Default
installed: true
enabled: true
version: 1.1.5_0
```

Native host manifest:

```text
manifestPath: C:\Users\ryan hui\AppData\Local\OpenAI\extension\com.openai.codexextension.json
registryKey: HKCU\Software\Google\Chrome\NativeMessagingHosts\com.openai.codexextension
correct: true
problem: null
```

## Current Automation Boundary

Direct Chrome extension control is not currently usable from this Codex session because the JavaScript execution tool fails before browser setup.

Per Chrome troubleshooting guidance, do not force the browser task through unrelated scripting once extension-backed control is unavailable. The current safe and traceable workflow remains:

1. `python scripts/next_v29_prompt.py --copy`
2. User or operator pastes the copied prompt into AstronClaw GUI and sends it.
3. Copy the AstronClaw GUI output.
4. `python scripts/save_v29_output.py --model <model> --case <case> --from-clipboard`
5. Review `v29_score_report.csv` and decide whether Skill changes are needed.

This keeps the deployed AstronClaw GUI as the authoritative test surface while automating the repeatable bookkeeping and scoring steps around it.
