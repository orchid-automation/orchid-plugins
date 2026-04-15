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
You type  ▶  /linear-swarm PLAYKIT "Infrastructure and observability" --worker=sandbox

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
│  LINEAR_API_KEY │   │      gh CLI     │   │  Claude Code    │
│ (issue/project  │   │  (push/PR/merge)│   │ (orchestrator)  │
│  reads + states)│   │                 │   │                 │
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
                   │ VERCEL_TOKEN           │  ← sandbox auth
                   │ VERCEL_TEAM_ID         │  ← sandbox auth
                   │ VERCEL_PROJECT_ID      │  ← sandbox auth
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
   │ saves to /tmp/linear-swarm-tests/<ID>.md │
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
         OR with --worker=sandbox:
      ┌──────┐  ┌──────┐   ┌──────┐        ┌──────┐  ┌──────┐
      │ ☁ sb │  │ ☁ sb │   │ ☁ sb │        │ ☁ sb │  │ ☁ sb │
      │GLM-5 │  │GLM-5 │   │GLM-5 │        │GLM-5 │  │GLM-5 │
      └──────┘  └──────┘   └──────┘        └──────┘  └──────┘
```

**Two modes:**
- `--worker=local` — git worktrees on your machine, Claude Max does the work
- `--worker=sandbox` — Vercel Sandboxes running cheap models via Vercel AI Gateway

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
     gh pr create --base <swarm-base-branch> --head <branch>
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
   deploy-branch push  ──►  Railway/Vercel/Fly auto-deploys
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

   If swarm-base-branch != deploy branch:
     mark this phase N/A for the run
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
│ ☁ sandbox│◄──────►│ codex   │        │ gh pr    │
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
/linear-swarm:linear-swarm PLAYKIT "Q2 Platform" --worker=sandbox

# Dry run (stop before worker fan-out)
/linear-swarm:linear-swarm PLAYKIT "Q2 Platform" --dry-run
```

---

## Walkthrough: repo-local dry run

A dry run is the fastest way to validate that `linear-swarm` can read your
Linear issue, audit its tickets, and produce a merge plan — all without
spawning workers, pushing branches, or touching production.

### What `--dry-run` does

`--dry-run` executes **Phases 1–2** (SCOPE and TEST DESIGN) and **skips
Phases 3–10** (FAN-OUT through PROD VERIFY). No agents are spawned, no
branches are created, no PRs are opened, and no deployments happen. You get
the scope audit and the test design artifacts so you can inspect quality
before committing to a full run.

### Command shape

```bash
# Issue mode — single parent issue with subtasks
/linear-swarm:linear-swarm <ISSUE-ID> --dry-run

# Example
/linear-swarm:linear-swarm PLAYKIT-22 --dry-run
```

### Step-by-step

```
1.  Point at a Linear issue that has subtasks already defined.
    The issue must live in a project your LINEAR_API_KEY can read.

2.  Run the command:
      /linear-swarm:linear-swarm PLAYKIT-22 --dry-run

3.  What you'll see:

    Phase 1 — SCOPE
      • linear-swarm reads every subtask on the parent issue
      • audits each ticket: STRONG / OK / WEAK / UNFIT
      • prints the file-overlap matrix and proposed merge order
      • asks for your confirmation  ← you review and say "go" or "stop"

    Phase 2 — TEST DESIGN
      • orchestrator reads the repo files each ticket touches
      • writes a test spec per ticket to /tmp/linear-swarm-tests/<ID>.md
      • prints a summary table

    ── dry run ends here ──
    Phases 3–10 are skipped. No workers, no branches, no PRs, no deploys.

4.  Inspect the output:
      • Are all tickets STRONG or OK?  Fix WEAK/UNFIT tickets before a real run.
      • Does the merge order look right?  The biggest refactor should be last.
      • Do the test specs cover the acceptance criteria?

5.  When you're satisfied, remove --dry-run and run for real:
      /linear-swarm:linear-swarm PLAYKIT-22 --worker=sandbox
```

### Why start with a dry run?

- **Catch bad input early.** Weak tickets (missing file paths, no acceptance
  criteria) waste worker time. Fix them before paying for sandbox compute.
- **Validate the merge plan.** A wrong merge order causes conflicts that the
  merge ladder can't untangle. Cheaper to reorder now than to re-run later.
- **No side effects.** Nothing is pushed, no Linear states change, no
  Vercel Sandboxes are created. Safe to run repeatedly.

---

## Walkthrough: repo-local issue-mode on a non-default branch

When you're working on a stacked branch (not `main`), `linear-swarm` records
the branch you started from as the **swarm base branch**. This affects PR
targets, review context, and whether deploy/prod-verify phases run.

### Command shape

```bash
# Issue mode — runs against current branch as the base
/linear-swarm:linear-swarm <ISSUE-ID>

# Example: you're on feature/auth-v2 (branched from main)
/linear-swarm:linear-swarm PLUXX-102
```

### What changes vs. a default-branch run

1. **Review and PR base follow the swarm base branch.** When the orchestrator
   opens PRs in Step 7, each PR targets the recorded swarm base branch — not
   a hardcoded `main`. Reviews are also scoped against that base so diff
   context matches what will actually merge.

2. **Deploy and prod-verify are N/A.** If the swarm base branch is not the
   deploy branch (the branch your CI/CD pipeline watches), Steps 9–10 are
   marked N/A and skipped. There is nothing to deploy or verify — merging
   into a feature branch doesn't trigger a production deploy.

### Step-by-step

```
1.  Check out your feature branch:
      git checkout feature/auth-v2

2.  Run issue mode:
      /linear-swarm:linear-swarm PLUXX-102

3.  What you'll see:

    Phase 1 — SCOPE
      • swarm base recorded: feature/auth-v2
      • tickets audited, merge plan produced

    Phases 2–6 — TEST DESIGN → SMOKE
      • same as a default-branch run

    Phase 7 — PUSH + PR
      • each PR targets feature/auth-v2 (the swarm base), not main

    Phase 8 — MERGE
      • squash-merges into feature/auth-v2

    Phase 9 — DEPLOY        N/A  (swarm base ≠ deploy branch)
    Phase 10 — PROD VERIFY  N/A  (swarm base ≠ deploy branch)

4.  Result: your feature branch now contains the merged work.
    When you later merge feature/auth-v2 into main, a separate
    deploy/prod-verify cycle runs at that time.
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
