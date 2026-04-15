---
name: linear-swarm
description: Ship a whole Linear project in one session — fan out parallel agents across git worktrees or Sandcastle-powered Vercel Sandboxes, audit with Codex + specialist reviewers, run structural smoke, sequentially merge PRs, deploy, and verify against live prod. Gracefully delegates to Every's compound-engineering plugin when installed. Use when you have a set of independent, well-specified Linear tickets to execute and ship together.
argument-hint: "<TEAM> <PROJECT_NAME> | <ISSUE-ID>  [--worker=local|sandbox] [--model=<slug>] [--dry-run] [--skip-codex]"
user-invocable: true
allowed-tools: Agent, SendMessage, Bash, Read, Write, Edit, Grep, Glob, ToolSearch, Skill, TaskCreate, TaskUpdate, TaskList, mcp__linear__list_issues, mcp__linear__list_projects, mcp__linear__get_issue, mcp__linear__save_issue
---

# Linear Swarm

Execute a Linear project end-to-end in one session using the **parallel fan-out + external review + structural smoke + sequential ship + prod verify** pattern. This skill owns the orchestration — every heavy lifting step delegates to existing primitives (compound-engineering workflows when installed, worktree/sandbox workers, `codex:rescue`, `gh`, Linear MCP, etc.).

**Invariant:** every phase is a gate. Don't skip gates.

## When to use

Use when:
- You have a Linear **project** with ≥3 well-specified parent tasks, OR a **parent issue** with ≥2 subtasks
- Each work item has explicit file paths + acceptance criteria
- Each work item fits in one agent's context
- You want them shipped in one session

Do NOT use for:
- Single tickets with no subtasks (just do them directly)
- Ambiguous tickets (run `/linear-doc` or similar to structure them first)
- Tickets requiring design decisions (pattern assumes execution, not thinking)
- XL-effort tickets that exceed one agent's window

## Trigger phrases

- "swarm the <project> project"
- "linear-swarm <team> <project>"
- "ship the <project> linear project"
- "swarm PROJ-66" (issue mode)

## Input modes

### Project mode — fan out by parent tasks
```
/linear-swarm:linear-swarm <TEAM> <PROJECT_NAME>
```
Fetches all parent tasks in the project. Each parent task = one agent. Subtasks are internal context for the agent.

### Issue mode — fan out by subtasks of a parent issue
```
/linear-swarm:linear-swarm <ISSUE-ID>
```
Fetches the parent issue + its subtasks. Each subtask = one agent. The parent description is shared context for all agents.

**Detection:** if the first arg contains a hyphen + number (e.g., `PROJ-66`, `ENG-142`), it's issue mode. Otherwise it's `<TEAM> <PROJECT>` project mode.

## Flags

- `--worker=local|sandbox` — local worktrees (Claude Max) or Vercel Sandboxes (cheap tier). Default: `local`
- `--model=<slug>` — tier-1 model when `--worker=sandbox`. Default: `zai/glm-5.1`. Fallbacks: `moonshotai/kimi-k2.5`, `anthropic/claude-haiku-4.5`, Claude Opus via Max
- `--worker=daytona` is accepted as a deprecated alias for `--worker=sandbox`
- `--dry-run` — run Phases 1-2 only, write shared test specs to `/tmp/linear-swarm-tests`, and halt before any worker, branch, worktree, or push activity
- `--skip-codex` — use only if Codex is unreachable

---

## Presentation Rules (CRITICAL — follow before executing ANY phase)

The user sees YOUR TEXT OUTPUT as the primary experience. This must feel like watching a clean dashboard, not reading a terminal log.

### What the user SHOULD see

```
Phase 1 — Scoping ACME "Q2 Platform Work"
  ✓ Found 4 parent tasks (ACME-101, ACME-102, ACME-103, ACME-104)
  ⚠ ACME-104 scored WEAK — prerequisites unchecked
  ✓ Merge order: ACME-102 → ACME-103 → ACME-101

Phase 2 — Writing test specifications
  ✓ ACME-101: 6 structural checks + 3 import smokes

--dry-run: wrote shared test specs to /tmp/linear-swarm-tests and stopped before worker fan-out.

Phase 3 — Spinning up 3 workers (Vercel Sandbox, GLM 5.1)
  ● ACME-101 working...
  ✓ ACME-101 committed — 2 files changed, all checks pass

Phase 4 — Reviewing (compound-engineering fleet + Codex)
  ✓ ACME-101: READY

--dry-run: stopping before worker fan-out.
```

### Rules

1. **Print a clean phase header before each phase.** Format: `Phase N — <verb-phrase>`. No code, no file paths, no implementation detail.

2. **Print ✓/✗/⚠/● status bullets** as steps complete. One line per meaningful result. ✓ = done, ✗ = failed, ⚠ = warning, ● = in progress.

3. **Every Bash tool call MUST have a `description:` parameter.** The description is what the user sees in the UI — not the command. Examples of GOOD descriptions:
   - `description: "Spinning up sandbox worker for SEND-82"`
   - `description: "Writing test spec for SEND-83"`
   - `description: "Pushing 3 branches to origin"`
   - `description: "Merging PR #127"`
   - `description: "Checking deploy status"`

   Examples of BAD (never do this):
   - `description: "Run command"` — too vague
   - No description at all — user sees raw command
   - `description: "sandbox-worker --branch SEND-82..."` — just repeating the command

4. **Use `bin/` commands, NEVER write Python scripts.** The plugin ships executables on PATH:
   - `sandbox-worker --repo R --branch B --brief F --commit-msg M` — full sandbox lifecycle
   - `linear-comment --issue ID --body "message"` — post to Linear
   These are one-liners. Do NOT write wrapper scripts, do NOT use base64 encoding, do NOT bake API keys into generated code. All credentials come from env vars automatically.

5. **Use TaskCreate/TaskUpdate** for phase tracking so the user sees visual progress:
   ```
   TaskCreate("Phase 1: Scope Linear issues")
   TaskUpdate(taskId, status="in_progress")
   ... work ...
   TaskUpdate(taskId, status="completed")
   ```

6. **Agent descriptions must be human-readable:** `"ACME-101 auth migration"` not `"Run task in worktree for issue"`.

7. **Suppress intermediate output.** When calling bin/ scripts, pipe to a log and surface only the summary:
   ```
   Bash(command: "sandbox-worker ... > /tmp/worker-SEND-82.log 2>&1 && tail -4 /tmp/worker-SEND-82.log",
        description: "Running sandbox worker for SEND-82")
   ```

8. **The golden rule:** if a tool call's `description` or visible output would confuse someone watching over the user's shoulder, rewrite it.

9. **Post Linear comments at every phase gate.** This creates an audit trail visible to anyone on the team — not just whoever's watching the Claude Code session. Use `mcp__linear__save_comment` from the orchestrator at:
   - Phase 1 complete: `"[scope] Picked up by linear-swarm — worker: <mode>, model: <model>"`
   - Phase 3 complete: `"✓ Worker committed: <hash> — <summary of changes>"`
   - Phase 4 complete: `"[review] Review verdict: READY"` or `"⚠ Review: NEEDS-CHANGES — <finding>"`
   - Phase 7 complete: `"[pr] PR #<n> opened: <url>"`
   - Phase 8 complete: `"[done] Merged to main"`
   - Phase 9 complete: `"[deploy] Deployed + prod smoke passed"`
   Sandbox workers post their own mid-work comments via the wrapper when `LINEAR_API_KEY` is available. Non-fatal — never block a phase on a failed comment.

---

## Phase 1 — Scope + Quality Audit

### Detect input mode

If the first arg matches `[A-Z]+-[0-9]+` (e.g., `PROJ-66`), this is **issue mode**. Otherwise it's **project mode**.

### Project mode (`<TEAM> <PROJECT>`)

1. Resolve `<TEAM>` + `<PROJECT_NAME>` to a Linear project ID:
   ```
   mcp__linear__list_projects(team: "<TEAM>")
   → fuzzy-match project name → projectId
   ```
2. Pull every parent task in the project:
   ```
   mcp__linear__list_issues(project: projectId, limit: 250)
   → filter state ∈ {Backlog, Todo, In Progress}
   → filter parentId IS NULL (parent tasks only)
   ```
3. For each parent task, pull its subtasks:
   ```
   mcp__linear__list_issues(parentId: parent.id)
   ```
4. **Fan-out unit = parent task.** Subtasks are internal context for the agent.

### Issue mode (`<ISSUE-ID>`)

1. Fetch the parent issue:
   ```
   mcp__linear__get_issue(id: "<ISSUE-ID>")
   ```
2. Fetch all subtasks:
   ```
   mcp__linear__list_issues(parentId: "<ISSUE-ID>")
   ```
3. If zero subtasks → abort: "This issue has no subtasks. Use it directly, not through linear-swarm."
4. **Fan-out unit = subtask.** The parent description is shared context for all agents.

### Quality audit (both modes)
4. **Quality audit** — for each parent + its subtasks:
   - File paths present? (yes/no)
   - Acceptance criteria present? (yes/no)
   - Effort size S/M/L/XL? (XL flagged as risky)
   - Test-plan hints present? (yes/no)
   - Score: STRONG / OK / WEAK / UNFIT
5. **File-overlap matrix** — grep each ticket description for file paths, compute pairwise overlap. Flag PRs that touch the same files.
6. **Recommended merge order** — compute dependency-safe order:
   - Phase 8a: zero-overlap PRs (merge first, parallel-safe)
   - Phase 8b: low-overlap PRs
   - Phase 8c: the biggest refactor (always absolute LAST)
7. **Print the plan to user:**
   - Count of parent tasks by quality score
   - Per-ticket quality report with remediation hints
   - File-overlap warnings
   - Recommended merge order
   - Worker mode + model
8. **USER CONFIRMATION GATE.** Wait for `go` / `yes` / `ship it`. Weak tickets should be fixed by the user via `/linear-doc` before proceeding. Do NOT auto-fix tickets.

---

## Phase 2 — Orchestrator Test Design (CRITICAL, non-skippable)

**Before any worker spawns**, the orchestrator (this session, running Claude Max) defines the test spec for each parent task.

For each parent:
1. Read every file path mentioned in the ticket + subtasks.
2. Write a test specification — the shared quality bar for worker + reviewer:
   - Pytest/jest case if the change is testable in code
   - Structured checklist (YAML frontmatter + bullets) for docs/config/copy changes — "file X exists", "file X contains Y", "file X does NOT contain Z"
   - Skip tag `"manual-review-required"` if neither applies; flagged for manual merge in Phase 9
3. Store tests at `${TMPDIR:-/tmp}/linear-swarm-tests/<ticket-id>.md` for reference by workers + reviewers.

If `--dry-run` is set:
- stop immediately after Phase 2
- print the generated spec paths and the recommended execution plan
- do NOT create worktrees, branches, repo-local scratch files, sandbox jobs, or review tasks

This transforms the worker's job from "figure out what to do" → "make these tests pass." Huge reliability gain for cheap-tier models.

---

## Phase 3 — Fan-Out

Spawn **one execution unit per work item** in parallel.

**CRITICAL RULE: NEVER write Python wrapper scripts for workers.** The plugin ships prebaked executables in `bin/` that are on your PATH. Use them.

### Worker A — Local worktree (default, uses Claude Max)

```
Agent(
  description: "<ticket-id> <short title>",
  subagent_type: "general-purpose",
  isolation: "worktree",
  mode: "acceptEdits",
  prompt: <contents of the brief file you wrote>
)
```

### Worker B — Sandcastle + Vercel Sandbox (cheap-tier)

**Step 1:** Write the brief to a temp file. Use the template at `${CLAUDE_PLUGIN_ROOT}/templates/worker-brief.md` as the base — fill in the `{{VARIABLES}}` with the ticket data. Example:

```bash
# Copy template + fill in variables
cp ${CLAUDE_PLUGIN_ROOT}/templates/worker-brief.md /tmp/brief-SEND-82.md
# Then edit the file to replace {{TICKET_IDS}}, {{TASK_DESCRIPTION}}, etc.
```

Or just Write() the brief directly — the template shows the expected format.

**Step 2:** Call `sandbox-worker` (one command, in PATH via plugin `bin/`):

```bash
sandbox-worker \
  --repo orchidautomation/sendlens \
  --branch brandon/send-82-elements \
  --brief /tmp/brief-SEND-82.md \
  --commit-msg "feat: install PromptInput and Suggestions (SEND-82, SEND-86)" \
  --linear-issue SEND-82
```

That's it. The script handles: runtime bootstrap, Vercel auth resolution, Sandcastle execution, local branch sync-back, deterministic commit creation when needed, and Linear comments. **All credentials come from env vars or plugin settings — never pass keys in arguments or generated code.**

For parallel workers, run multiple `sandbox-worker` calls as background Bash commands. Each gets its own sandbox and local branch state automatically.

**Step 3:** Reuse the returned local worktree if the wrapper prints `WORKTREE:`. If it does not, create a local worktree for later phases:

```bash
git worktree add .sandcastle/worktrees/<ticket-id> <branch>
```

### Available bin/ commands (all on PATH, all read creds from env)

| Command | What it does |
|---|---|
| `sandbox-worker --repo R --branch B --brief F --commit-msg M` | Full sandbox worker lifecycle |
| `daytona-worker --repo R --branch B --brief F --commit-msg M` | Deprecated alias for `sandbox-worker` |
| `linear-comment --issue ID --body "message"` | Post a comment to a Linear issue |

### Brief format (per agent)

```
You are implementing Linear parent task <ID>: <title>.

## Parent task
<full description>

## Subtasks (your internal task list)
<enumerated subtasks with descriptions>

## Files to modify
<explicit file list derived from ticket + subtasks>

## Test specification (MUST pass before you commit)
<paste from ${TMPDIR:-/tmp}/linear-swarm-tests/<ticket-id>.md>

## Instructions
1. Read the files you need to modify
2. Work through each subtask in order
3. Verify your changes pass the test specification
4. Post a comment to Linear issue <ID> as you complete each subtask (optional, for paper trail)
5. Commit with conventional commit message ending with (<ID>)
6. Report back in ≤250 words: branch, commit hash, subtasks completed, test spec pass/fail per item

Do NOT push. Do NOT open a PR. Stop after committing.
```

Local worktree agents follow that verbatim. Sandbox workers use the same brief, but the wrapper syncs results back onto a normal local branch and may preserve a local worktree for the later phases.

### Model escalation ladder (per-ticket, on failure of smoke in Phase 6)

```
Tier 1:  zai/glm-5.1                  ← default (best SWE-Bench Pro, Claude Code optimized)
Tier 2:  moonshotai/kimi-k2.5         ← fallback (proven Anthropic Messages compat)
Tier 3:  anthropic/claude-haiku-4.5   ← guaranteed-compat safety net
Tier 4:  claude-opus (via Max)         ← reserved for tickets the cheap tiers keep failing
```

Orchestrator records `{ticket_id, branch, execution_mode, agent_id?, local_worktree, tier}` for Phases 2-7.

---

## Phase 4 — External Review

Graceful enhancement: use CE's review fleet if installed.

### If compound-engineering plugin is installed
```
Skill(compound-engineering:workflows:review) with: "--fresh\n\nReview these N branches..."
```
CE's `/workflows:review` spawns 14+ specialist reviewers (security-sentinel, performance-oracle, architecture-strategist, code-simplicity-reviewer, Kieran-* reviewers, etc.) in parallel.

### If CE is NOT installed — bundled fallback
Spawn 3-4 bundled reviewer subagents in parallel:
```
Agent(subagent_type: "linear-swarm:correctness-reviewer", ...)
Agent(subagent_type: "linear-swarm:security-reviewer", ...)
Agent(subagent_type: "linear-swarm:simplicity-reviewer", ...)
```

### Meta-synthesis — always runs
After the review fleet (either CE or bundled):
```
Skill(codex:rescue) with: "--fresh\n\nReview all branches + the review findings above..."
```

**CRITICAL: always prefix the codex prompt with `--fresh` on first call, `--resume` on every subsequent call.** Otherwise `codex:rescue` fires `AskUserQuestion` and halts automation.

Output: per-branch verdict `READY / NEEDS-CHANGES / BLOCKED` with specific file:line findings.

---

## Phase 5 — Fix-Up Loop

For each NEEDS-CHANGES or BLOCKED branch:

- If the branch came from a local Phase 3 agent, continue the same agent:

```
SendMessage(
  to: <original agent_id from Phase 3>,
  summary: "<ID> fix-up",
  message: "Codex review flagged: <exact finding with file:line>.
Fix: <specific steps>.
Re-run test spec: <from ${TMPDIR:-/tmp}/linear-swarm-tests/<ID>.md>.
Commit with message: <type>: <summary> (<ID>).
Report new commit hash in ≤180 words."
)
```

- If the branch came from a sandbox worker, work from the synced local branch instead:

```
git worktree add .sandcastle/worktrees/<ticket-id>-fix <branch>
Agent(
  description: "<ticket-id> fix-up",
  subagent_type: "general-purpose",
  isolation: "worktree",
  mode: "acceptEdits",
  prompt: <same brief + exact review findings + latest test spec>
)
```

**Rules:**
- `SendMessage` is only for long-lived local worktree agents. Do NOT try to `SendMessage` a one-shot sandbox worker run.
- Sandbox branches must exist as normal local branches before entering Phase 4, so every later phase has a standard branch checkout.
- **Escalate model tier** only for repeated Phase 3 sandbox failures. Once a branch is synced locally, later fix-ups stay local unless you explicitly choose to restart Phase 3.
- Re-run Phase 4 with `--resume` (not `--fresh`) so Codex continues the prior review thread with context.
- Loop until all READY. Usually 1-2 rounds.

---

## Phase 6 — Structural Smoke

Delegate to the `smoke-verify` skill in this plugin:
```
Skill(linear-swarm:smoke-verify)
```

It:
1. Scaffolds `scripts/verify_refactor.py` in the target repo if missing (from template)
2. Captures a baseline from current `main`
3. Copies script + baseline into each local worktree, including sandbox-origin branches
4. Runs `python3 scripts/verify_refactor.py --smoke` in parallel across every worktree
5. Asserts: module imports cleanly, framework inventory matches baseline, decoupling holds, **live tool dispatch through real framework call path returns valid JSON** (not error-prefix strings)

Every worktree must emit `✓ VERIFY PASSED` before advancing. On failure: back to Phase 5 with the specific assertion that broke.

**`--dry-run` should never reach this phase.** If the user set `--dry-run`, stop after Phase 2 instead.

---

## Phase 7 — Push + PR

Parallel, one bash call per branch:
```
git push -u origin <branch>
gh pr create --base main --head <branch> \
  --title "<conventional commit>" \
  --body <summary + Linear link + test plan>
```

Sandbox-origin branches remain local after Phase 3. Phase 7 is the first push before opening the PR.

After all PRs open:
- Print PR URL table
- Move each Linear issue `Todo|Backlog → In Review` via `mcp__linear__save_issue`
- Check `gh pr view <n> --json mergeable` for every PR; flag `CONFLICTING` immediately for pre-emptive rebase

---

## Phase 8 — Sequential Merge Ladder

Order from Phase 1:
- 6a: zero-overlap PRs (merge first)
- 6b: low-overlap PRs
- 6c: biggest refactor (absolute LAST)

```
for pr in ordered_list:
  gh pr merge $pr --squash
  sleep 3    # GitHub API needs a beat
  state = gh pr view $pr --json state -q .state
  if state != MERGED:
    # CONFLICT HANDLING
    if small conflict:
      cd <worktree>
      git fetch origin main
      git rebase origin/main
      resolve markers inline OR SendMessage the agent
      python3 scripts/verify_refactor.py --smoke
      git push --force-with-lease origin <branch>
      gh pr merge $pr --squash
    if BIG refactor conflict (touches files every other PR also modified):
      SendMessage(agent) with the surgical re-apply playbook:
        1. save branch's extracted dirs to /tmp
        2. git reset --hard origin/main
        3. restore saved dirs
        4. re-apply every merged PR's changes to NEW file locations
        5. re-run smoke
        6. git push --force
      gh pr merge $pr --squash
  git fetch origin main
```

---

## Phase 9 — Deploy + Version Probe

Identify the deploy platform (Railway, Vercel, Fly, etc.) from the repo. Poll `/health` every 10s during rollover.

**Critical:** `/health` stays 200 during blue-green. You need a VERSION SIGNAL — something in the response that proves new code is live:
- A new HTTP response header added in this batch
- A new route registered
- A new JSON field in a response
- A commit hash at `/version` if one exists

GATE: signal appears → advance.

---

## Phase 9 — Prod Smoke (real client)

Call the live deployed service through a **real authenticated client**:
- Local plugin/MCP pointing at prod is best (uses real dispatch path)
- Otherwise authenticated curl script

**Specifically test features that depend on OPS CONFIG:**
- Env vars the new deploy requires
- Secrets rotated/added
- Feature flags flipped
- DB migrations applied

**This is the ONLY phase that crosses code ↔ ops.** Skip it and you'll ship silent-broken deploys every time ops config drifts.

On failure:
- Diagnose ops vs code
- If ops: fix env/secret/flag, redeploy, re-smoke
- If code: hotfix via mini-swarm (Phase 3 for one ticket)

**DO NOT move Linear issues to Done until Phase 9 passes.**

---

## Phase 10 — Cleanup + Compound

```bash
# Worktrees
for wt in .claude/worktrees/agent-*; do
  git worktree remove "$wt" --force
done

# Local branches (all merged)
for br in $(git branch --list "<prefix>*"); do
  git branch -D "$br"
done

# Pull main after cleanup
git pull --ff-only origin main

# Move Linear issues to Done (only if Phase 9 passed)
for id in <ticket_ids>; do
  mcp__linear__save_issue(id="$id", state="Done")
done
```

### Compound phase (NEW — graceful enhancement with CE)

If `compound-engineering` plugin is installed:
```
Skill(compound-engineering:workflows:compound) with: "--resume\n\nSession just shipped N tickets. Extract learnings to docs/solutions/ ..."
```

If CE is NOT installed, write a minimal learning file directly:
```
docs/swarm/solutions/<date>-<project-slug>.md
  frontmatter: {date, project, tickets, duration, verdict}
  body: what we learned + what to compound next time
```

This is what makes the pattern truly compound: every run writes learnings the next run reads.

---

## Failure modes + recovery

| Failure | Recovery |
|---|---|
| Agent never commits | `SendMessage` with "you haven't committed yet, run git add + commit now" |
| Sandbox worker exits non-zero | Stop immediately, surface sandbox stderr, fix the wrapper/input, then rerun Phase 3 |
| Codex unreachable | `--skip-codex` flag falls back to bundled reviewers only |
| Structural smoke fails after fix-up | `SendMessage` the agent with the exact assertion that broke; escalate model tier if persistent |
| Merge conflict cascade | Halt ladder, rebase + smoke + force-push, continue |
| Deploy stuck | Check platform logs (`railway logs`, `vercel logs`), investigate before forcing |
| Prod smoke fails (ops config) | Fix env/secret/flag, redeploy, re-smoke. DO NOT move Linear to Done |
| Prod smoke fails (code) | Hotfix via mini-swarm on one ticket |
| Worktree won't remove | `git worktree remove --force` (safe since all work is committed + pushed) |
| `codex:rescue` asks AskUserQuestion | You forgot `--fresh` or `--resume` in the prompt prefix — fix and retry |

---

## Non-obvious rules (baked in from prior runs)

1. **"CI green" ≠ "deploy correct."** Phase 9 is the only code↔ops crossing. Never skip.
2. **The biggest refactor's rebase is nonlinear.** Save → reset → restore → surgical re-apply. Not git-rebase.
3. **`SendMessage` > `Agent()`.** Continue existing agents. Fresh spawns cost full re-onboarding.
4. **Smoke ≠ unit tests.** Smoke runs through the framework dispatch path. Unit tests miss "function exists but framework call crashes."
5. **Version signal ≠ /health.** Blue-green keeps /health green. Pick a fingerprint that changes between deploys.
6. **Don't move Linear to Done until Phase 9 passes.** "In Review" is the holding state.
7. **`codex:rescue` ALWAYS needs `--fresh` or `--resume`.** Without a flag, it fires `AskUserQuestion` and halts.
8. **One agent per parent task, subtasks are internal.** Never spawn one agent per subtask — subtasks share files, so parallelism at that level creates conflicts.

---

## Success criteria

The run is successful when:
- [done] Every Phase 3 agent committed
- [done] Phase 4 reviews all READY (or NEEDS-CHANGES all addressed in Phase 5)
- [done] Every worktree emits `✓ VERIFY PASSED` in Phase 6
- [done] Every PR is `MERGED` in Phase 8
- [done] Deploy rollover completes with version signal confirmed in Phase 9
- [done] Phase 9 prod smoke passes via real client
- [done] Linear issues moved `In Review → Done`
- [done] Worktrees + branches cleaned up
- [done] Compound learnings written (to CE `docs/solutions/` or `docs/swarm/solutions/`)

If any are missing at session end → do NOT declare victory. Report what's incomplete and what's needed to finish.
