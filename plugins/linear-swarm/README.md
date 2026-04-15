# Linear Swarm

Ship a whole Linear project in one session. Fan out parallel agents across local worktrees or Sandcastle-powered Vercel Sandboxes, audit with Codex + specialist reviewers, run a structural smoke script, sequentially merge PRs, deploy, and verify against live production.

Inspired by [Every Inc's compound-engineering-plugin](https://github.com/EveryInc/compound-engineering-plugin). Gracefully delegates to their workflows when both plugins are installed; falls back to bundled reviewers otherwise.

## Install

```bash
/plugin marketplace add orchid-automation/orchid-plugins
/plugin install linear-swarm@orchid-plugins
```

For local development, validate the plugin before testing it:

```bash
claude plugin validate ./plugins/linear-swarm
claude --plugin-dir ./plugins/linear-swarm
```

## Required environment

Before running `/linear-swarm:linear-swarm`, set these:

| Env var / setup | Required | Purpose |
|---|---|---|
| `LINEAR_API_KEY` | yes | Unattended Linear reads, comments, and state transitions |
| `ANTHROPIC_API_KEY` (or Max subscription) | yes | Orchestrator Claude |
| `GH_TOKEN` / `GITHUB_TOKEN` or `gh auth login` | yes | Push branches + open PRs |
| clean git working tree | yes | Sandcastle branches from the local checkout |
| `VERCEL_AI_GATEWAY_KEY` | sandbox only | Cheap-tier model access for sandbox workers |
| `VERCEL_OIDC_TOKEN` | sandbox only | Preferred Vercel Sandbox auth |
| `VERCEL_TOKEN` + `VERCEL_TEAM_ID` + `VERCEL_PROJECT_ID` | sandbox only | Token-based Vercel Sandbox auth |
| logged-in Vercel CLI + linked `.vercel/project.json` | sandbox only | The worker can reuse your local Vercel CLI token and linked project metadata |

The plugin's `SessionStart` hook prints a preflight checklist. The `UserPromptSubmit` hook hard-blocks `/linear-swarm:*` commands when required credentials are missing. Sandbox runtime/auth setup is treated as optional unless you explicitly choose `--worker=sandbox`.

`linear-swarm` now prefers the bundled `linear-issue` / `linear-comment` CLI helpers over Linear MCP so nested Claude runs stay unattended and do not stop for browser OAuth.

## Graceful enhancement

If [Every Inc's compound-engineering plugin](https://github.com/EveryInc/compound-engineering-plugin) is also installed, `linear-swarm` automatically delegates:

| Phase | With CE installed | Without CE |
|---|---|---|
| Plan per parent task | `/compound-engineering:workflows:plan` | Orchestrator writes plan inline |
| Execute in worktree | `/compound-engineering:workflows:work` | Spawn `Agent(isolation:"worktree")` |
| Review | `/compound-engineering:workflows:review` (14+ specialists) | Bundled 3 reviewers + `codex:rescue` |
| Resolve findings | `/compound-engineering:resolve_todo_parallel` | Inline fix-up loop |
| Compound learnings | `/compound-engineering:workflows:compound` | Write to `docs/solutions/` directly |

**Install CE too for the deluxe experience:**

```bash
/plugin marketplace add EveryInc/compound-engineering-plugin
/plugin install compound-engineering@EveryInc-compound-engineering-plugin
```

## Usage

### Project mode — fan out by parent tasks
```bash
/linear-swarm:linear-swarm <TEAM> <PROJECT_NAME>
```

### Issue mode — fan out by subtasks of a parent issue
```bash
/linear-swarm:linear-swarm <ISSUE-ID>
```

### Examples
```bash
# Project mode
/linear-swarm:linear-swarm ENGINEERING "Q2 Platform Work"
/linear-swarm:linear-swarm MOBILE "Auth Migration" --dry-run

# Issue mode (epic with subtasks)
/linear-swarm:linear-swarm ENG-66
/linear-swarm:linear-swarm PROJ-142 --worker=sandbox --model=zai/glm-5.1
/linear-swarm:linear-swarm TEAM-404 --worker=sandbox --dry-run
```

> **`--dry-run` stops before worker fan-out.** It runs scope discovery (Phase 1) and test design (Phase 2), writes shared specs to `/tmp/linear-swarm-tests`, and then exits — no agents are spawned in worktrees or Vercel Sandboxes.

## Flags

| Flag | Default | Effect |
|---|---|---|
| `--worker=local\|sandbox` | `local` | Execute in local git worktrees (Claude Max) or Vercel Sandboxes (cheap tier) |
| `--model=<slug>` | `zai/glm-5.1` | Tier-1 model when `--worker=sandbox` |
| `--dry-run` | off | Run scope + test design only, write shared specs to `/tmp/linear-swarm-tests`, then stop before worker fan-out |
| `--skip-codex` | off | Skip external Codex review (use only if Codex is unavailable) |

`--worker=daytona` is still accepted as a deprecated alias for `--worker=sandbox` so older prompts do not break.

When you use `--worker=sandbox`, Phase 1 runs in a Vercel Sandbox, syncs the result back onto a local git branch, and leaves the rest of the workflow uniform. Review, fix-up, smoke, PR, and merge phases all operate on normal local branches and worktrees.

`linear-swarm` records a **swarm base branch + base SHA** at startup. Review, PR, smoke, merge, and cleanup all key off that recorded base instead of assuming `main`, so stacked runs stay scoped correctly.

## The 10 phases

- **New here?** Start with [docs/DEMO.md](docs/DEMO.md) — a student-friendly walkthrough with ASCII diagrams for every step.
- **Reference?** See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for the full phase-by-phase diagram.

1. **Scope + Quality Audit** — Read Linear (project or parent issue), quality-audit every work item, user confirm
2. **Test Design** — Orchestrator writes test specs per ticket before any agent spawns
3. **Fan-Out** — One agent per work item, in worktree OR sandbox
4. **Review** — CE `workflows:review` + `codex:rescue --fresh`
5. **Fix-Up Loop** — reuse same agent with review findings; sandbox branches stay local after sync-back
6. **Structural Smoke** — `scripts/verify_refactor.py` against baseline + real framework dispatch
7. **Push + PRs** — `gh pr create --base <swarm-base-branch>` per branch, Linear → In Review
8. **Merge Ladder** — dependency-safe order, rebase on the swarm base branch, big refactor LAST
9. **Deploy + Prod Verify** — only when the swarm base branch is the deploy branch; otherwise mark this phase N/A
10. **Compound + Cleanup** — write learnings, worktree/branch cleanup, Linear → Done

## What makes this different from CE alone

- **Linear as source of truth** — CE reads from `docs/brainstorms/` on disk; this reads Linear tickets (team, mobile, multi-user)
- **Sandcastle + Vercel Sandbox workers** — run cheap-tier models via Vercel AI Gateway while syncing results back onto normal local branches
- **Cross-code/ops prod verify** — Phase 9 catches ops-config regressions (missing env vars, feature flags) that every structural test will miss

## Attribution

Heavily inspired by [Every Inc's compound-engineering-plugin](https://github.com/EveryInc/compound-engineering-plugin). See [docs/ATTRIBUTION.md](docs/ATTRIBUTION.md).

## License

MIT © Orchid Automation
