# Linear Swarm

Ship a whole Linear project in one session. Fan out parallel agents across worktrees or Daytona sandboxes, audit with Codex + specialist reviewers, run a structural smoke script, sequentially merge PRs, deploy, and verify against live production.

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

| Env var | Required | Purpose |
|---|---|---|
| `LINEAR_API_KEY` or Linear MCP configured | yes | Read project + issues |
| `ANTHROPIC_API_KEY` (or Max subscription) | yes | Orchestrator Claude |
| `VERCEL_AI_GATEWAY_KEY` | optional | Cheap-tier model access for Daytona workers |
| `DAYTONA_API_KEY` | optional | Sandbox workers (alternative to local worktrees) |
| `GH_TOKEN` / `GITHUB_TOKEN` or `gh auth login` | yes | Push branches + open PRs |

The plugin's `SessionStart` hook prints a preflight checklist. The `UserPromptSubmit` hook hard-blocks `/linear-swarm:*` commands when required credentials are missing. Missing Daytona setup is treated as optional unless you actually choose `--worker=daytona`.

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

```bash
/linear-swarm:linear-swarm <TEAM> <PROJECT_NAME>
```

Examples:
```bash
/linear-swarm:linear-swarm ENGINEERING "Q2 Platform Work"
/linear-swarm:linear-swarm MOBILE "Auth Migration" --dry-run
/linear-swarm:linear-swarm GROWTH "Landing Page Refresh" --worker=local
/linear-swarm:linear-swarm PLATFORM "API v2" --worker=daytona --model=zai/glm-5.1
```

## Flags

| Flag | Default | Effect |
|---|---|---|
| `--worker=local\|daytona` | `local` | Execute in local git worktrees (Claude Max) or Daytona sandboxes (cheap tier) |
| `--model=<slug>` | `zai/glm-5.1` | Tier-1 model when `--worker=daytona` |
| `--dry-run` | off | Run through plan + review + smoke, stop before push |
| `--skip-codex` | off | Skip external Codex review (use only if Codex is unavailable) |

When you use `--worker=daytona`, Phase 1 pushes the sandbox branch, then mirrors it into a local git worktree before review. Later fix-up, smoke, and PR phases run against that local mirror so the rest of the pipeline stays uniform.

## The 10 phases

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for the full phase-by-phase diagram.

0. **Scope** — Read Linear, quality-audit every parent task + subtask, user confirm
1. **Plan per parent task** — Delegate to CE `workflows:plan` if installed, else inline
2. **Fan-out** — One agent per parent task, in worktree OR Daytona sandbox
3. **Review** — CE `workflows:review` + `codex:rescue --fresh`
4. **Fix-up loop** — reuse the same local worktree agent when possible; Daytona branches are mirrored locally before any fix-up
5. **Structural smoke** — `scripts/verify_refactor.py` template against baseline
6. **Push + PRs** — `gh pr create` per branch, Linear → In Review
7. **Sequential merge ladder** — dependency-safe order, rebase on conflict, big refactor LAST
8. **Deploy + version probe** — poll `/health` until new-code signal appears
9. **Prod smoke** — call live service through real client; catches ops-config regressions
10. **Cleanup + Compound** — worktree/branch cleanup, Linear → Done, CE `workflows:compound` or `docs/solutions/` write-back

## What makes this different from CE alone

- **Linear as source of truth** — CE reads from `docs/brainstorms/` on disk; this reads Linear tickets (team, mobile, multi-user)
- **Daytona sandbox workers** — run cheap-tier models ($0.30/M) inside isolated sandboxes via Vercel AI Gateway, preserving your Claude Max quota for orchestration and synthesis
- **Cross-code/ops prod verify** — Phase 9 catches ops-config regressions (missing env vars, feature flags) that every structural test will miss

## Attribution

Heavily inspired by [Every Inc's compound-engineering-plugin](https://github.com/EveryInc/compound-engineering-plugin). See [docs/ATTRIBUTION.md](docs/ATTRIBUTION.md).

## License

MIT © Orchid Automation
