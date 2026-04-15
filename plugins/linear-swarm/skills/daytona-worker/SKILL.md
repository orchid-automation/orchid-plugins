---
name: daytona-worker
description: Deprecated compatibility alias for linear-swarm's sandbox-worker. Use sandbox-worker and --worker=sandbox in new prompts.
user-invocable: false
allowed-tools: Bash, Read, Write
---

# Deprecated Alias

`daytona-worker` is retained only so older prompts and cached instructions do not break.

The actual implementation path now lives in [`sandbox-worker`](../sandbox-worker/SKILL.md), which runs Claude Code inside a Sandcastle-managed Vercel Sandbox and syncs the result back onto a local branch.

Use `--worker=sandbox` in new flows. `--worker=daytona` is treated as a deprecated alias.
