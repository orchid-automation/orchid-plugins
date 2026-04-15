# Operator Flow

This file captures the flow that is actually running now, including the nested Claude invocation path used when Codex validates the plugin from outside Claude Code.

## Control Plane

```text
User
  |
  | asks Codex to validate or run linear-swarm
  v
Codex (outer controller)
  |
  | reads repo state, picks target issue/project, checks auth/tooling
  |
  | launches local Claude CLI:
  | claude --plugin-dir ./plugins/linear-swarm \
  |   --permission-mode bypassPermissions \
  |   --dangerously-skip-permissions \
  |   -p "/linear-swarm:linear-swarm <target> ..."
  v
Claude Code session (nested)
  |
  +--> loads plugin hooks
  |      SessionStart -> scripts/preflight.sh
  |      UserPromptSubmit -> scripts/linear_swarm_gate.sh
  |
  +--> exposes /linear-swarm:linear-swarm
  |      skills/linear-swarm/SKILL.md
  |
  +--> uses plugin bin helpers on PATH
         bin/linear-issue
         bin/linear-comment
         bin/sandbox-worker
```

## Data Plane

```text
Linear issue / project
  |
  v
linear-issue
  |
  v
Phase 1: scope audit
  |
  +--> work items
  +--> merge order
  +--> swarm base branch + base SHA
  |
  v
Phase 2: test design
  |
  v
/tmp/linear-swarm-tests/<ticket>.md
  |
  v
Phase 3: execution
  |
  +--> local worker
  |      git worktree -> local Claude agent -> commit on local branch
  |
  +--> sandbox worker
         sandbox-worker
           -> ensure_runtime.sh
           -> runtime/sandbox_worker.mjs
           -> Sandcastle
           -> Vercel Sandbox
           -> Claude Code inside sandbox
           -> sync result back to local branch/worktree
           -> optional `swarm-hitl` recovery on the same branch when `--hitl=on-error`
  |
  v
Phase 4: review
  |
  +--> CE reviewers (if installed)
  +--> bundled reviewers
  +--> codex:rescue synthesis
  |
  v
Phase 5: fix-up loop
  |
  v
Phase 6: smoke verify
  |
  v
Phase 7: push + PR
  |
  +--> swarm-phase7
  |      one manifest -> sequential push + PR create/reuse
  |
  v
Phase 8: merge ladder
  |
  v
Phase 9: deploy + prod verify
  |
  v
Phase 10: cleanup + Linear Done
```

## What Codex Actually Did

Codex did not execute Claude Code skills natively. It used the local shell to spawn the `claude` binary, pointed that process at the checked-in plugin with `--plugin-dir`, and then watched the resulting run like any other CLI process.

```text
Codex
  |
  +--> shell command
  |      claude --plugin-dir ./plugins/linear-swarm -p "/linear-swarm:linear-swarm ..."
  |
  +--> reads stdout/stderr
  +--> inspects git branches, PRs, Linear state, sandbox logs
  +--> decides whether to re-run, patch the plugin, or stop
```

That split matters:

- Claude auth gates the nested orchestrator run.
- GitHub auth gates push and PR creation.
- The orchestration is safest when approval-sensitive GitHub actions are batched through `swarm-phase7` instead of emitted as parallel `gh pr create` tool calls.
- Linear API auth gates unattended issue reads/comments/state transitions.
- Vercel auth gates sandbox execution.

If one layer is missing, Codex can still inspect the repo, but the nested swarm run will stop at that boundary.

## Auth Troubleshooting

| Auth Layer | Failure Symptom | Fix Path |
|---|---|---|
| Claude | `claude` exits with auth error or "not logged in" | Run `claude login`; verify `ANTHROPIC_API_KEY` is set |
| GitHub | Push or PR creation returns `403` / `Permission denied` | Check `gh auth status`; re-auth with `gh auth login` |
| Linear | `linear-issue` / `linear-comment` returns `401 Unauthorized` | Regenerate Linear API key; update `LINEAR_API_KEY` env var |
| Vercel Sandbox | `sandbox-worker` fails with `403` or sandbox not created | Verify `VERCEL_TOKEN` is set and has sandbox scope |
