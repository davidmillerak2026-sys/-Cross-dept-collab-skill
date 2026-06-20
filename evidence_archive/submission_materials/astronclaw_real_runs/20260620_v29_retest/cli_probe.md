# V29 CLI Probe

Date: 2026-06-20

Purpose: determine whether the deployed AstronClaw Skill can be batch-tested from CLI instead of manual GUI copy/paste.

## Commands Checked

```text
npx --yes clawhub --help
npx --yes clawhub install --help
npx --yes clawhub inspect --help
npx --yes clawhub scan --help
npx --yes openclaw --help
npx --yes openclaw status
npx --yes openclaw skills --help
npx --yes openclaw agent --help
```

## Findings

`clawhub` is available as ClawHub CLI v0.22.0.

Relevant capabilities:

- login/logout/whoami
- search/install/update/uninstall/list/inspect
- publish/scan/download scan report

No command was found for running a deployed AstronClaw chat session, selecting the AstronClaw page model, or invoking `agent.xfyun.cn/astron-claw/deployed/chat` directly.

`openclaw` is available and has a local `agent` command, but current local status is not ready for authoritative AstronClaw testing:

- Gateway: unreachable
- Gateway service: not installed
- Node service: not installed
- Agents: 0
- Channels: none

`openclaw agent --local` may be useful later for auxiliary local regression tests if model provider keys and an agent workspace are configured, but it is not evidence that the Skill works inside the deployed AstronClaw GUI.

## Current Test Authority

Until a documented AstronClaw deployed-chat API or CLI run command is available, authoritative evidence remains:

1. manual or semi-automated AstronClaw GUI run
2. model selected in the AstronClaw page
3. output copied from the deployed chat page
4. output saved with model, case id, run date, and observed defects

