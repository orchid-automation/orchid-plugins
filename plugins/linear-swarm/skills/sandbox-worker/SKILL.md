---
name: sandbox-worker
description: Internal skill. Runs a headless Claude Code worker inside a Sandcastle-managed Vercel Sandbox with a cheap model via Vercel AI Gateway. Syncs the result back onto a local git branch so later review, smoke, PR, and merge phases operate on normal local worktrees. Used by linear-swarm Phase 1 when --worker=sandbox.
user-invocable: false
allowed-tools: Bash, Read, Write
---

# Sandbox Worker

This skill wraps the "headless Claude Code in a Vercel Sandbox via Sandcastle" pattern. It's called by `linear-swarm` Phase 1 when the user picks `--worker=sandbox`.

## Inputs

```json
{
  "ticket_id": "<LINEAR-ID>",
  "branch": "<gitBranchName from Linear>",
  "model": "zai/glm-5.1" | "moonshotai/kimi-k2.5" | "anthropic/claude-haiku-4.5",
  "brief": "<full self-contained task description with files + tests>",
  "repo": "<owner>/<repo>",
  "base_branch": "main"
}
```

## Prerequisites

- `node` and `npm` available locally
- `VERCEL_AI_GATEWAY_KEY` set
- Vercel Sandbox auth is available through either:
  - `VERCEL_OIDC_TOKEN`, or
  - `VERCEL_TOKEN` plus `VERCEL_TEAM_ID` and `VERCEL_PROJECT_ID`, or
  - a logged-in Vercel CLI plus a linked `.vercel/project.json`
- The current git checkout is clean before Phase 1 starts

## Canonical command

```bash
sandbox-worker \
  --repo orchidautomation/sendlens \
  --branch brandon/send-82-elements \
  --brief /tmp/brief-SEND-82.md \
  --commit-msg "feat: install PromptInput and Suggestions (SEND-82, SEND-86)" \
  --linear-issue SEND-82
```

The wrapper handles runtime install, Vercel auth resolution, Sandcastle execution, local branch sync-back, deterministic commit creation when the sandbox leaves uncommitted changes, and final status reporting.

## Behavioral rules

- Never pass API keys in arguments or generated code. The wrapper reads env vars and plugin config automatically.
- Treat the sandbox lane as a **Phase 1 implementation engine**, not a long-lived fix-up environment.
- Later phases operate on the synced local branch or preserved local worktree.
- If the worker exits non-zero, stop the swarm and surface the sandbox error. Do not mark the ticket READY.

## Notes

- `daytona-worker` remains as a deprecated compatibility shim that forwards to `sandbox-worker`.
- The wrapper writes Sandcastle logs outside the repo so the base checkout stays clean.
