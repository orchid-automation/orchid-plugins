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
/linear-swarm:linear-swarm PROJ-142 --worker=daytona --model=zai/glm-5.1
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

1. **Scope + Quality Audit** — Read Linear (project or parent issue), quality-audit every work item, user confirm
2. **Test Design** — Orchestrator writes test specs per ticket before any agent spawns
3. **Fan-Out** — One agent per work item, in worktree OR Daytona sandbox
4. **Review** — CE `workflows:review` + `codex:rescue --fresh`
5. **Fix-Up Loop** — reuse same agent with review findings; Daytona branches mirrored locally
6. **Structural Smoke** — `scripts/verify_refactor.py` against baseline + real framework dispatch
7. **Push + PRs** — `gh pr create` per branch, Linear → In Review
8. **Merge Ladder** — dependency-safe order, rebase on conflict, big refactor LAST
9. **Deploy + Prod Verify** — poll `/health`, version signal, then real-client prod smoke
10. **Compound + Cleanup** — write learnings, worktree/branch cleanup, Linear → Done

## What makes this different from CE alone

- **Linear as source of truth** — CE reads from `docs/brainstorms/` on disk; this reads Linear tickets (team, mobile, multi-user)
- **Daytona sandbox workers** — run cheap-tier models ($0.30/M) inside isolated sandboxes via Vercel AI Gateway, preserving your Claude Max quota for orchestration and synthesis
- **Cross-code/ops prod verify** — Phase 9 catches ops-config regressions (missing env vars, feature flags) that every structural test will miss

## Attribution

Heavily inspired by [Every Inc's compound-engineering-plugin](https://github.com/EveryInc/compound-engineering-plugin). See [docs/ATTRIBUTION.md](docs/ATTRIBUTION.md).

## License

MIT © Orchid Automation
