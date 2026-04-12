# Linear Swarm Architecture — the 10 phases

```
                                     INPUT
                        ──────────────────────────────
                        /linear-swarm:linear-swarm
                           <TEAM> <PROJECT_NAME>
                           [--worker=local|daytona]
                           [--model=<slug>]
                           [--dry-run] [--skip-codex]
                                       │
                                       ▼
┌───────────────────────────────────────────────────────────────────────┐
│  PHASE 0 — SCOPE + QUALITY AUDIT                                       │
│  ─────────────────────────────────────────────────────────────────    │
│  mcp__linear__list_projects(team=<TEAM>)                               │
│    fuzzy match <PROJECT_NAME> → projectId                              │
│  mcp__linear__list_issues(project=projectId, parentId=null)            │
│    → parent tasks                                                      │
│  for each parent: list_issues(parentId=parent.id)                      │
│    → subtasks become agent CONTEXT (not separate work units)           │
│                                                                        │
│  Quality audit per parent + subtasks:                                  │
│    - file paths present?                                               │
│    - acceptance criteria?                                              │
│    - effort ≤ L?                                                       │
│    - test-plan hints?                                                  │
│    → score STRONG / OK / WEAK / UNFIT                                  │
│                                                                        │
│  File-overlap matrix → recommended merge order                         │
│                                                                        │
│  ┌─────── USER CONFIRMATION GATE ───────┐                              │
│  │ Weak tickets must be fixed externally │                              │
│  │ via /linear-doc before proceeding     │                              │
│  └───────────────────────────────────────┘                              │
└─────────────────────────────┬─────────────────────────────────────────┘
                              │
                              ▼
┌───────────────────────────────────────────────────────────────────────┐
│  PHASE 0.5 — ORCHESTRATOR TEST DESIGN                                  │
│  ─────────────────────────────────────────────────────────────────    │
│  For each parent task, THIS SESSION (Claude Max) writes tests upfront: │
│    - pytest/jest case if code change                                   │
│    - structured checklist if docs/config/copy                          │
│    - "manual-review-required" tag if neither                           │
│  Stored at docs/swarm/tests/<ticket-id>.md                             │
│                                                                        │
│  Critical: worker's job becomes "make these tests pass" instead of    │
│  "figure out what to do". Big reliability gain for cheap-tier models.  │
└─────────────────────────────┬─────────────────────────────────────────┘
                              │
                              ▼
┌───────────────────────────────────────────────────────────────────────┐
│  PHASE 1 — FAN-OUT (one agent per parent task)                         │
│  ─────────────────────────────────────────────────────────────────    │
│       If --worker=local:                                               │
│         Agent(isolation="worktree", subagent_type="general-purpose")   │
│         (uses Claude Max, full smarts)                                 │
│       If --worker=daytona:                                             │
│         Skill(linear-swarm:daytona-worker)                             │
│         (cheap-tier model via Vercel AI Gateway in sandbox)            │
│                                                                        │
│  MODEL ESCALATION LADDER (on Phase 5 smoke failure):                   │
│    Tier 1:  zai/glm-5.1                  ← default                     │
│    Tier 2:  moonshotai/kimi-k2.5                                       │
│    Tier 3:  anthropic/claude-haiku-4.5                                 │
│    Tier 4:  claude-opus via Max (switches to local worktree)           │
│                                                                        │
│  Each agent commits to brandon/<ticket-id>-<slug>. Orchestrator        │
│  records {ticket_id, branch, agent_id, tier}.                          │
└─────────────────────────────┬─────────────────────────────────────────┘
                              │ all agents returned
                              ▼
┌───────────────────────────────────────────────────────────────────────┐
│  PHASE 2 — REVIEW                                                      │
│  ─────────────────────────────────────────────────────────────────    │
│  If compound-engineering plugin installed:                             │
│    Skill(compound-engineering:workflows:review)                        │
│    with "--fresh\n\nReview N branches..."                              │
│    → 14+ specialist reviewers spawn in parallel                        │
│                                                                        │
│  Else (bundled fallback):                                              │
│    Agent(subagent_type="linear-swarm:correctness-reviewer")            │
│    Agent(subagent_type="linear-swarm:security-reviewer")               │
│    Agent(subagent_type="linear-swarm:simplicity-reviewer")             │
│                                                                        │
│  THEN (always):                                                        │
│    Skill(codex:rescue) with "--fresh\n\n<review prompt>"               │
│    ^^^ META-SYNTHESIS across all branches                              │
│                                                                        │
│  CRITICAL: always prefix codex prompts with --fresh (or --resume on    │
│  follow-ups). Without a flag, codex:rescue fires AskUserQuestion       │
│  and halts automation.                                                 │
│                                                                        │
│  Output: per-branch verdict READY / NEEDS-CHANGES / BLOCKED            │
└─────────────────────────────┬─────────────────────────────────────────┘
                              │
                              ▼
┌───────────────────────────────────────────────────────────────────────┐
│  PHASE 3 — FIX-UP LOOP                                                 │
│  ─────────────────────────────────────────────────────────────────    │
│  For each NEEDS-CHANGES or BLOCKED branch:                             │
│    SendMessage(to=<original agent_id>, ...)                            │
│                                                                        │
│  RULES:                                                                │
│    - SendMessage, NOT Agent() — same agent, same worktree, same ctx   │
│    - Escalate model tier if cheap-tier fails twice                    │
│    - Re-run Phase 2 with --resume (not --fresh) so Codex has context  │
│    - Loop until all READY                                              │
└─────────────────────────────┬─────────────────────────────────────────┘
                              │
                              ▼
┌───────────────────────────────────────────────────────────────────────┐
│  PHASE 4 — STRUCTURAL SMOKE                                            │
│  ─────────────────────────────────────────────────────────────────    │
│  Skill(linear-swarm:smoke-verify)                                      │
│                                                                        │
│  1. scaffold scripts/verify_refactor.py from template if missing       │
│  2. capture baseline from pre-change main                              │
│  3. copy script + baseline to every worktree                           │
│  4. parallel: python3 scripts/verify_refactor.py --smoke               │
│                                                                        │
│  Smoke checks (all must pass):                                         │
│    - module imports cleanly                                            │
│    - framework tool inventory matches baseline                         │
│    - decoupling grep (no new imports across module boundaries)        │
│    - REAL dispatch through framework call path returns valid JSON     │
│                                                                        │
│  Rejects error-prefix strings and non-JSON returns strictly.           │
│                                                                        │
│  STOP HERE if --dry-run.                                               │
└─────────────────────────────┬─────────────────────────────────────────┘
                              │
                              ▼
┌───────────────────────────────────────────────────────────────────────┐
│  PHASE 5 — PUSH + PR                                                   │
│  ─────────────────────────────────────────────────────────────────    │
│  Parallel, per branch:                                                 │
│    git push -u origin <branch>                                         │
│    gh pr create --base main --head <branch>                            │
│                                                                        │
│  Move each Linear issue: Todo/Backlog → In Review                      │
└─────────────────────────────┬─────────────────────────────────────────┘
                              │
                              ▼
┌───────────────────────────────────────────────────────────────────────┐
│  PHASE 6 — SEQUENTIAL MERGE LADDER                                     │
│  ─────────────────────────────────────────────────────────────────    │
│  Dependency-safe order (from Phase 0):                                 │
│    6a: zero-overlap PRs                                                │
│    6b: low-overlap PRs                                                 │
│    6c: BIGGEST refactor (always absolute LAST)                         │
│                                                                        │
│  for pr in ordered:                                                    │
│    gh pr merge $pr --squash                                            │
│    sleep 3   # GH API settle                                           │
│    if state != MERGED:                                                 │
│      rebase in worktree → smoke → force-push → retry                   │
│      (for BIG refactor: surgical re-apply playbook — save dirs,       │
│       hard-reset, restore, re-apply other PRs' changes to NEW         │
│       file locations, re-smoke, force-push)                            │
│    git fetch origin main                                               │
└─────────────────────────────┬─────────────────────────────────────────┘
                              │
                              ▼
┌───────────────────────────────────────────────────────────────────────┐
│  PHASE 7 — DEPLOY + VERSION PROBE                                      │
│  ─────────────────────────────────────────────────────────────────    │
│  Auto-deploy triggered by main push (Railway, Vercel, Fly, etc)        │
│  Poll /health every 10s                                                │
│                                                                        │
│  CRITICAL: /health stays 200 during blue-green. Look for a             │
│  VERSION SIGNAL — fingerprint that changes between deploys:            │
│    - new HTTP response header                                          │
│    - new route registered                                              │
│    - new JSON field                                                    │
│    - commit hash at /version                                           │
│                                                                        │
│  GATE: signal appears → advance                                        │
└─────────────────────────────┬─────────────────────────────────────────┘
                              │
                              ▼
┌───────────────────────────────────────────────────────────────────────┐
│  PHASE 8 — PROD SMOKE (real client)                                    │
│  ─────────────────────────────────────────────────────────────────    │
│  Skill(linear-swarm:prod-verify)                                       │
│                                                                        │
│  Call live deployed service through REAL authenticated client:         │
│    - local MCP plugin pointing at prod (BEST)                          │
│    - authenticated curl / httpx script                                 │
│    - gh pr checks summary                                              │
│                                                                        │
│  Specifically probe features that depend on OPS CONFIG:                │
│    - env vars the deploy requires                                      │
│    - secrets rotated/added                                             │
│    - feature flags flipped                                             │
│    - DB migrations applied                                             │
│                                                                        │
│  ◄━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓   │
│  ┃  THIS IS THE ONLY GATE THAT CROSSES CODE ↔ OPS                ┃   │
│  ┃  Skip and you'll ship silent-broken deploys every time         ┃   │
│  ┃  ops config drifts.                                            ┃   │
│  ┃━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫   │
│                                                                        │
│  DO NOT move Linear issues to Done until this phase passes.            │
└─────────────────────────────┬─────────────────────────────────────────┘
                              │
                              ▼
┌───────────────────────────────────────────────────────────────────────┐
│  PHASE 9 — CLEANUP + COMPOUND                                          │
│  ─────────────────────────────────────────────────────────────────    │
│  git worktree remove --force (each)                                    │
│  git branch -D (each)                                                  │
│  git pull --ff-only origin main                                        │
│  Linear issues: In Review → Done                                       │
│  Daytona sandbox: stop or snapshot                                     │
│                                                                        │
│  COMPOUND (graceful enhancement):                                      │
│    If compound-engineering installed:                                  │
│      Skill(compound-engineering:workflows:compound) with "--resume\n"  │
│      → writes learnings to docs/solutions/                             │
│    Else:                                                               │
│      Write docs/swarm/solutions/<date>-<project>.md directly           │
│                                                                        │
│  This is what makes the pattern truly compound: every run writes       │
│  learnings the next run reads.                                         │
└──────────────────────────────────┬────────────────────────────────────┘
                                   ▼
                              ┌─────────┐
                              │ SHIPPED │
                              └─────────┘
```

## Support systems (running alongside the phases)

```
┌────────────────────────────┐  ┌────────────────────────────┐
│ SessionStart hook          │  │ UserPromptSubmit hook      │
│ ──────────────────         │  │ ──────────────────         │
│ scripts/preflight.sh       │  │ scripts/linear_swarm_gate  │
│                            │  │                            │
│ Soft-warns if any of:      │  │ Hard-blocks /linear-swarm  │
│  - git / gh / daytona /    │  │ prompts when required      │
│    python3 missing         │  │ prerequisites are missing. │
│  - gh not authenticated    │  │                            │
│  - VERCEL_AI_GATEWAY_KEY   │  │ Checks --worker=daytona    │
│    not set (optional)      │  │ path specifically for      │
│  - DAYTONA_API_KEY not     │  │ DAYTONA_API_KEY + VAG key  │
│    set (optional)          │  │                            │
│                            │  │ Exit 2 = block the prompt  │
│ Never blocks; exit 0       │  │ per Claude Code hooks API  │
└────────────────────────────┘  └────────────────────────────┘

┌────────────────────────────┐  ┌────────────────────────────┐
│ verify_refactor.py         │  │ daytona_worker.py          │
│ ──────────────────         │  │ ──────────────────         │
│ Lives in scripts/ of the   │  │ Wrapper around the base64  │
│ target repo. Scaffolded    │  │ + exec pattern for running │
│ from template on first     │  │ headless Claude Code       │
│ run if missing.            │  │ inside Daytona sandboxes   │
│                            │  │ via Vercel AI Gateway.     │
│ Customized per framework   │  │                            │
│ by editing:                │  │ Handles shell-quoting traps│
│  - TARGET_MODULE_NAME      │  │ that break plain            │
│  - get_tool_names()        │  │ `daytona exec` calls.      │
│  - dispatch_tool()         │  │                            │
│  - SMOKE_TOOLS list        │  │ Clones repo throwaway,     │
│                            │  │ runs cheap model, commits, │
│                            │  │ pushes, reports back.      │
└────────────────────────────┘  └────────────────────────────┘
```

## Interaction with compound-engineering-plugin

Linear Swarm **is not a replacement for CE** — it's a Linear-first, prod-verify-aware orchestrator that **graceful-enhances** to CE's full workflow library when both are installed.

| Phase | With CE installed | Without CE |
|---|---|---|
| 0.5 Plan | `Skill(compound-engineering:workflows:plan)` | Orchestrator writes inline test spec |
| 1 Work (local) | `Skill(compound-engineering:workflows:work)` | `Agent(isolation:"worktree", ...)` |
| 2 Review | `Skill(compound-engineering:workflows:review)` + `Skill(codex:rescue)` | Bundled 3 reviewers + `Skill(codex:rescue)` |
| 3 Fix-up | `Skill(compound-engineering:resolve_todo_parallel)` | Inline `SendMessage` loop |
| 9 Compound | `Skill(compound-engineering:workflows:compound)` | Write to `docs/swarm/solutions/` directly |

All other phases (0 scope, 4 smoke, 5 push, 6 merge, 7 deploy, 8 prod verify) are unique to linear-swarm and not covered by CE.
