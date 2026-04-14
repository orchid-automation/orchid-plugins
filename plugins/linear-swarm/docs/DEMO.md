# Linear Swarm — Student Demo Guide

A hands-on walkthrough of `/linear-swarm`: one command that ships an entire
Linear project end-to-end — fan out, review, smoke, merge, deploy, verify.

This doc is the demo script. It trades density for clarity. For the full
reference architecture, see [ARCHITECTURE.md](ARCHITECTURE.md).

---

## The problem we're solving

```
 BEFORE                                AFTER
 ────────────────────                  ────────────────────
 1 engineer                            1 orchestrator (you)
   │                                     │
   ├─ pick a ticket                      ├─ point at a Linear project
   ├─ branch + code                      │    (6 tickets, 1 epic — doesn't matter)
   ├─ wait for review                    │
   ├─ fix comments                       ▼
   ├─ rebase                            ┌──────────────────────────┐
   ├─ merge                             │ 10 parallel agents spawn │
   ├─ deploy                            │ review runs              │
   ├─ next ticket                       │ smoke runs               │
   └─ repeat × 6                        │ PRs merged in order      │
                                        │ prod verified            │
 ~3 days serial                         └──────────────────────────┘
                                        ~20 minutes parallel
```

---

## What you'll see during the demo

```
You type  ▶  /linear-swarm PLAYKIT "Infrastructure and observability" --worker=daytona

Claude    ▶  Phase 0 — scope audit        [~30s]
Claude    ▶  quality table + merge plan   [~gate: you say "go"]
Claude    ▶  Phase 1 — fan out 5 agents   [~5 min, parallel]
Claude    ▶  Phase 2 — Codex + reviews    [~2 min]
Claude    ▶  Phase 3 — fix-up loop        [~3 min]
Claude    ▶  Phase 4 — structural smoke   [~1 min]
Claude    ▶  Phase 5 — push + PRs         [~30s]
Claude    ▶  Phase 6 — merge ladder       [~2 min]
Claude    ▶  Phase 7 — deploy + probe     [~2 min]
Claude    ▶  Phase 8 — prod smoke         [~1 min]
Claude    ▶  Phase 9 — compound + clean   [~30s]
          ✓ 5 PRs shipped, Linear → Done
```

Total: ~15–20 minutes for what normally takes a week.

---

## Prerequisites (one-time setup)

```
┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐
│   Linear MCP    │   │      gh CLI     │   │  Claude Code    │
│   (read tickets)│   │  (push/PR/merge)│   │ (orchestrator)  │
└─────────────────┘   └─────────────────┘   └─────────────────┘
         │                     │                     │
         └─────────────────────┼─────────────────────┘
                               ▼
                   ┌────────────────────────┐
                   │   orchid-plugins       │
                   │   /plugin install      │
                   │   linear-swarm         │
                   └───────────┬────────────┘
                               │
                               ▼
                   optional cheap-tier workers
                   ┌────────────────────────┐
                   │ DAYTONA_API_KEY        │  ← cloud sandbox
                   │ VERCEL_AI_GATEWAY_KEY  │  ← cheap models
                   └────────────────────────┘
```

Install:

```bash
/plugin marketplace add orchid-automation/orchid-plugins
/plugin install linear-swarm@orchid-plugins
```

Set API keys via the plugin's `userConfig` prompt, or in `~/.zshenv`.

---

## The 10 steps

Each step is a **gate** — the run does not advance until the gate passes.

```
  1. SCOPE         you approve the plan
  2. TEST DESIGN   orchestrator writes tests per ticket
  3. FAN-OUT       N agents work in parallel (worktree or sandbox)
  4. REVIEW        Codex + specialists judge every branch
  5. FIX-UP        same agent fixes review findings
  6. SMOKE         structural verify against baseline
  7. PUSH + PR     branches go up, Linear → In Review
  8. MERGE         sequential, biggest refactor last
  9. DEPLOY        poll /health, confirm version signal
 10. PROD VERIFY   real client hits prod; compound learnings; cleanup
```

### Step 1 — SCOPE

```
   Linear                     Claude (orchestrator)
   ────────                   ─────────────────────
   6 tickets  ──────►         audit: STRONG / OK / WEAK / UNFIT
                              file-overlap matrix
                              merge order (zero-overlap first, refactor last)
                              ┌───────────────────────┐
                              │ USER CONFIRMATION ◄── │ you say "go"
                              └───────────────────────┘
```

Weak tickets (missing file paths, no acceptance criteria) get flagged. You
fix them with `/linear-doc` before the swarm runs. **The tool refuses to
guess on bad input.**

### Step 2 — TEST DESIGN

```
   For each ticket:
   ┌────────────────────────────────────────┐
   │ orchestrator READS the ticket files    │
   │ writes a test spec:                    │
   │   - pytest case (code change)          │
   │   - checklist (docs/config/copy)       │
   │   - "manual-review" tag (ambiguous)    │
   │ saves to docs/swarm/tests/<ID>.md      │
   └────────────────────────────────────────┘
```

**Why this matters:** the worker's job becomes *"make this test pass,"* not
*"figure out what to do."* Huge reliability gain for cheap-tier models.

### Step 3 — FAN-OUT

```
                    ┌────── orchestrator ──────┐
                    │                          │
          ┌─────────┼──────────┬───────────────┼─────────┐
          ▼         ▼          ▼               ▼         ▼
      ┌──────┐  ┌──────┐   ┌──────┐        ┌──────┐  ┌──────┐
      │ T-1  │  │ T-2  │   │ T-3  │        │ T-4  │  │ T-5  │
      │      │  │      │   │      │  ...   │      │  │      │
      │ wt/  │  │ wt/  │   │ wt/  │        │ wt/  │  │ wt/  │
      └──────┘  └──────┘   └──────┘        └──────┘  └──────┘
         OR with --worker=daytona:
      ┌──────┐  ┌──────┐   ┌──────┐        ┌──────┐  ┌──────┐
      │ ☁ sb │  │ ☁ sb │   │ ☁ sb │        │ ☁ sb │  │ ☁ sb │
      │GLM-5 │  │GLM-5 │   │GLM-5 │        │GLM-5 │  │GLM-5 │
      └──────┘  └──────┘   └──────┘        └──────┘  └──────┘
```

**Two modes:**
- `--worker=local` — git worktrees on your machine, Claude Max does the work
- `--worker=daytona` — cloud sandboxes running cheap models via Vercel AI Gateway

**Model escalation ladder** (auto-retries on smoke failure):
```
   zai/glm-5.1  →  moonshotai/kimi-k2.5  →  claude-haiku-4.5  →  Opus
```

### Step 4 — REVIEW

```
                    all branches ready
                           │
                           ▼
        ┌──────────────────┴──────────────────┐
        │                                     │
        ▼                                     ▼
   specialist reviewers            Codex (external)
   ┌────────────────────┐          ┌────────────────────┐
   │ correctness        │          │ meta-synthesis     │
   │ security           │          │ across all branches│
   │ simplicity         │          │ with --fresh flag  │
   │ architecture       │          └──────────┬─────────┘
   │ ... 14 total       │                     │
   └──────────┬─────────┘                     │
              └─────────────┬─────────────────┘
                            ▼
              per-branch verdict:  READY / NEEDS-CHANGES / BLOCKED
```

### Step 5 — FIX-UP LOOP

```
   NEEDS-CHANGES branch
        │
        ▼
   SendMessage(original agent, "fix these findings: ...")
        │
        ▼
   worker re-runs tests → commits → loop back to step 4
        │
        ▼
   READY  →  advance
```

Uses the **same agent in the same worktree** (not a fresh spawn) so context
is preserved. Usually 1–2 rounds.

### Step 6 — STRUCTURAL SMOKE

```
   Every worktree runs:  python3 scripts/verify_refactor.py --smoke

   ┌────────────────────────────────────────┐
   │ ✓ module imports cleanly               │
   │ ✓ framework tool inventory = baseline  │
   │ ✓ no new cross-module imports          │
   │ ✓ live dispatch returns valid JSON     │ ← the critical one
   └────────────────────────────────────────┘
```

**Why this isn't just unit tests:** smoke runs through the real framework
dispatch path. Unit tests pass while the framework call crashes all the
time. Smoke catches that.

### Step 7 — PUSH + PR

```
   for each branch:
     git push -u origin <branch>
     gh pr create --base main --head <branch>
     Linear issue:  Todo  →  In Review
```

### Step 8 — MERGE LADDER

```
   Merge order from Step 1:

   6a  zero-overlap PRs   ──►  squash-merge in parallel
                                    │
                                    ▼
   6b  low-overlap PRs    ──►  squash-merge sequentially
                                    │
                                    ▼
   6c  BIGGEST refactor   ──►  surgical re-apply if needed
        (absolute LAST)        (save dirs, reset, restore,
                                re-apply other PRs, smoke,
                                force-push, merge)
```

### Step 9 — DEPLOY + VERSION PROBE

```
   main push  ──►  Railway/Vercel/Fly auto-deploys
                          │
                          ▼
                   poll /health every 10s
                          │
                          ▼
   ┌────────────────────────────────────────┐
   │ /health is 200 during blue-green!      │
   │ Look for a VERSION SIGNAL instead:     │
   │   - new header                         │
   │   - new route                          │
   │   - new JSON field                     │
   │   - commit hash at /version            │
   └────────────────────────────────────────┘
                          │
                          ▼
                    signal appears  ──►  advance
```

### Step 10 — PROD VERIFY + COMPOUND

```
   call the LIVE deployed service via a real client
   (local MCP pointing at prod, or authenticated curl)
                          │
                          ▼
   ┌────────────────────────────────────────────────────┐
   │  THE ONLY GATE THAT CROSSES CODE ↔ OPS             │
   │  catches missing env vars, unflipped flags,        │
   │  missed migrations — things every structural       │
   │  test is blind to.                                 │
   └────────────────────────────────────────────────────┘
                          │
                 ┌────────┴────────┐
                 ▼                 ▼
              PASS              FAIL
                 │                 │
                 ▼                 ▼
   Linear → Done        diagnose ops vs code
   cleanup worktrees    fix env/flag OR mini-swarm hotfix
   compound learnings   redeploy → re-verify
   ✓ SHIPPED            (do NOT move Linear to Done)
```

---

## End-to-end data flow

```
┌──────────┐
│  Linear  │  ← source of truth
└────┬─────┘
     │  read tickets + subtasks
     ▼
┌────────────────────────────────────────────────────────────┐
│                    ORCHESTRATOR (you)                       │
│  - audits tickets                                           │
│  - writes test specs                                        │
│  - spawns workers                                           │
│  - reads review verdicts                                    │
│  - calls merge/deploy/verify                                │
└──┬───────────────────┬───────────────────┬─────────────────┘
   │                   │                   │
   ▼ fan-out           ▼ review            ▼ ship
┌─────────┐        ┌─────────┐        ┌──────────┐
│ WORKERS │        │ REVIEW  │        │ GITHUB   │
│         │        │         │        │          │
│ ☁ daytona│◄──────►│ codex   │        │ gh pr    │
│  or     │        │ specialists│      │ merge    │
│ 💻 local │        └─────────┘        └────┬─────┘
└────┬────┘                                 │
     │ commits + pushes                     ▼
     │                                  ┌──────────┐
     └─────────────────────────────────►│ RAILWAY  │
                                        │ deploys  │
                                        └────┬─────┘
                                             │
                                             ▼
                                        ┌──────────┐
                                        │   PROD   │
                                        │ verified │
                                        └──────────┘
```

---

## Run it yourself

```bash
# Project mode (epic with parent tasks)
/linear-swarm:linear-swarm PLAYKIT "Infrastructure and observability"

# Issue mode (parent with subtasks)
/linear-swarm:linear-swarm PLAYKIT-22

# Cheap-tier cloud workers
/linear-swarm:linear-swarm PLAYKIT "Q2 Platform" --worker=daytona

# Dry run (stop before push)
/linear-swarm:linear-swarm PLAYKIT "Q2 Platform" --dry-run
```

---

## Live demo example (2026-04-12 run)

```
input:  /linear-swarm PLAYKIT "Repo Hardening" --worker=local

Phase 0 audit:      13 tickets — all STRONG
Phase 1 fan-out:    13 worktrees spawned in parallel
Phase 2 review:     Codex flagged 4 branches NEEDS-CHANGES
Phase 3 fix-up:     all 4 resolved in one round
Phase 4 smoke:      13/13 ✓ VERIFY PASSED
Phase 5 PR:         13 PRs opened
Phase 6 merge:      merged in order, refactor last
Phase 7 deploy:     Railway deploy → version signal confirmed
Phase 8 prod:       MCP tool dispatch returning valid JSON ✓
Phase 9 cleanup:    worktrees removed, Linear → Done

result:  mcp_slim.py  5723 → 309 lines  (94% reduction)
         wall time:  ~18 minutes
         orchestrator input:  1 command
```

---

## Non-obvious rules (burned in from prior runs)

1. **"CI green" ≠ "deploy correct."** Step 10 is the only code↔ops crossing. Never skip.
2. **The biggest refactor's rebase is nonlinear.** Save → reset → restore → surgical re-apply. Not git rebase.
3. **`SendMessage` > `Agent()`.** Continue existing agents. Fresh spawns cost full re-onboarding.
4. **Smoke ≠ unit tests.** Smoke runs through framework dispatch. Unit tests miss "function exists but framework call crashes."
5. **Version signal ≠ /health.** Blue-green keeps /health green. Pick a fingerprint that changes between deploys.
6. **Don't move Linear to Done until Step 10 passes.** "In Review" is the holding state.
7. **`codex:rescue` ALWAYS needs `--fresh` or `--resume`.** Otherwise it fires `AskUserQuestion` and halts automation.
8. **One agent per parent task.** Subtasks are the agent's internal task list — never spawn one agent per subtask (they share files and conflict).

---

## Where to go next

- [ARCHITECTURE.md](ARCHITECTURE.md) — full phase-by-phase reference
- [ATTRIBUTION.md](ATTRIBUTION.md) — inspiration + credits to Every Inc's compound-engineering-plugin
- [../README.md](../README.md) — install + flags reference
