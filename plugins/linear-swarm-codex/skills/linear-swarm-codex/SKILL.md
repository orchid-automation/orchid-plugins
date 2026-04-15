---
name: linear-swarm-codex
description: Use when the user wants a Codex-native Linear swarm. Codex owns Linear scope, planning, review, smoke, and merge sequencing while cheap-tier cloud workers implement code in Vercel Sandbox.
metadata:
  short-description: Codex-native Linear swarm orchestration
---

# Linear Swarm Codex

This skill is the Codex-native control plane for swarm work.

The key split is:

- Codex does the orchestration.
- Sandbox workers do the coding.
- The default coding lane is `zai/glm-5.1` in Vercel Sandbox via `opencode`.

## When to use this skill

Use this skill when the user wants any of:

- a Codex-native alternative to the Claude Code `linear-swarm` plugin
- Codex to read Linear, scope work, and fan out coding workers
- Codex to manage review, smoke verification, PR ordering, and merge sequencing

## Current implementation boundary

Start with the executable entrypoint:

```bash
plugins/linear-swarm-codex/bin/swarm-codex --issue TEAM-123 --dry-run
```

This plugin currently reuses the shared execution helpers from:

- [`plugins/_shared/linear-swarm/bin/linear-issue`](/Users/brandonguerrero/Documents/Orchid Automation/Orchid Labs/orchid-plugins/plugins/_shared/linear-swarm/bin/linear-issue)
- [`plugins/_shared/linear-swarm/bin/linear-comment`](/Users/brandonguerrero/Documents/Orchid Automation/Orchid Labs/orchid-plugins/plugins/_shared/linear-swarm/bin/linear-comment)
- [`plugins/_shared/linear-swarm/bin/sandbox-worker`](/Users/brandonguerrero/Documents/Orchid Automation/Orchid Labs/orchid-plugins/plugins/_shared/linear-swarm/bin/sandbox-worker)
- [`plugins/_shared/linear-swarm/bin/swarm-phase7`](/Users/brandonguerrero/Documents/Orchid Automation/Orchid Labs/orchid-plugins/plugins/_shared/linear-swarm/bin/swarm-phase7)

That means the control plane is Codex-native, while the worker runtime is shared.

## Required workflow

### Step 1: Build scope from Linear

Prefer the installed Linear tools when available. If tool access is missing or the user wants repo-local reproducibility, fall back to:

- `plugins/linear-swarm-codex/bin/swarm-codex --issue ...`
- `plugins/_shared/linear-swarm/bin/linear-issue project-parents ...`
- `plugins/_shared/linear-swarm/bin/linear-issue children ...`

Output from this step:

- work item list
- file overlap notes
- merge order
- base branch and base SHA

### Step 2: Write explicit test specs before any coding starts

For each work item, Codex writes a concrete spec to `/tmp/linear-swarm-tests/<ticket-id>.md`.

The spec must be one of:

- executable test case
- structured checklist
- manual-review-required

### Step 3: Delegate implementation to cloud workers

Use the shared sandbox worker for implementation:

```bash
plugins/_shared/linear-swarm/bin/sandbox-worker \
  --branch <branch> \
  --brief /tmp/brief-<ticket>.md \
  --commit-msg "<commit message>" \
  --model zai/glm-5.1 \
  --agent-provider opencode \
  --hitl on-error \
  --linear-issue <ticket-id>
```

Rules:

- Default worker model is `zai/glm-5.1`.
- Default worker agent provider is `opencode`.
- Use `--hitl on-error` when the run should surface a manual recovery path instead of failing silently.
- Treat the sandbox worker as an implementation engine, not the orchestration layer.

### Step 4: Codex reviews locally

After worker fan-out, Codex reviews the branches locally.

Focus on:

- correctness
- overlap or merge-order risks
- missing tests
- unnecessary complexity

If there are actionable issues, route fix-up back onto the same branch before PR creation.

### Step 5: Smoke and PR sequencing

Run the structural smoke path from the shared implementation, then batch PR creation through:

- `plugins/_shared/linear-swarm/bin/swarm-phase7`

Never emit multiple independent PR-creation actions when a single manifest-driven batch will do.

### Step 6: Merge in dependency order

Merge in the order established during Step 1.

Codex owns this sequencing. The cheap-tier workers do not.

## Operating model

```text
Codex
  |
  +--> Linear scope and planning
  +--> test design
  +--> local review and smoke
  +--> PR ordering and merge ladder
  |
  +--> sandbox-worker
         -> Sandcastle
         -> Vercel Sandbox
         -> opencode
         -> GLM 5.1 coding lane
```

## Important constraint

This plugin removes Claude Code from the orchestration layer. The default worker lane is no longer Claude-derived, but `claude-code` remains available as a fallback provider.

Inference:

- today: Codex-native control plane, shared worker runtime, `opencode` default
- next: Codex should own more of the later review and merge phases directly
- later: add more proven gateway-compatible worker providers if they outperform `opencode`
