---
name: smoke-verify
description: Internal skill. Scaffolds a structural verification script in the target repo, captures a baseline from main, and runs smoke tests in parallel across every worktree. Catches regressions that unit tests miss by dispatching real tools through the framework's call path. Used by linear-swarm Phase 4.
user-invocable: false
allowed-tools: Bash, Read, Write
---

# Smoke Verify

This skill runs structural smoke across every worktree after the fan-out phase. Called by `linear-swarm` Phase 4.

## Why this exists

Unit tests catch "function X returns wrong value". They don't catch:
- **Import errors** in refactored modules
- **Framework-level dispatch** breaking (tool registered but crashes when called)
- **Decoupling regressions** (new imports creeping into files that should be independent)
- **Runtime regressions that look like success** (function returns an error-string instead of raising)

The smoke script runs the REAL framework call path for 2-3 representative tools and asserts the returns are valid JSON, not error-prefix strings.

## Inputs

- Target repo path
- List of worktree paths
- Module entry point name (auto-detect or user-provided)
- 2-3 "free tool" names that can be called with no auth (e.g. `get_pricing`, `get_tool_costs`)

## Steps

### 1. Scaffold the script if missing

Check if `<repo>/scripts/verify_refactor.py` exists. If not, copy the template from this skill's directory (`verify_refactor.py.template`) and customize:
- Swap `TARGET_MODULE_NAME` → the repo's main module (e.g., `app`, `server`, `mcp_slim`)
- Swap `get_tool_names()` → the target framework's inventory API (FastMCP, FastAPI, Flask, etc.)
- Swap `SMOKE_TOOLS` → 2-3 free endpoints/tools that can be called with no auth

### 2. Capture baseline from main

```bash
cd <repo> && git checkout main
python3 scripts/verify_refactor.py --baseline
# writes scripts/.refactor_baseline.json with:
#   - module import status
#   - framework inventory (tool names, route paths, handler count)
#   - known file line counts
#   - decoupling grep matrix (e.g., imports from the refactored-away module)
```

### 3. Copy script + baseline into every worktree

```bash
for wt in .claude/worktrees/agent-*; do
  cp scripts/verify_refactor.py "$wt/scripts/"
  cp scripts/.refactor_baseline.json "$wt/scripts/"
done
```

### 4. Parallel smoke across all worktrees

Launch one background Bash call per worktree, all in the same tool message. Each runs:
```bash
cd <worktree> && python3 scripts/verify_refactor.py --smoke 2>&1 | tail -15
```

Wait for all to complete.

### 5. Assert every worktree passes

Each worktree must print `✓ VERIFY PASSED` to stdout. If any print `✗ VERIFY FAILED`:
- Collect the specific failures (script names the broken assertions)
- Return them to the orchestrator for Phase 3 fix-up round
- Escalate model tier if the same worker fails twice

## The verify script contract

Located at `scripts/verify_refactor.py` in the target repo. Supports three modes:

- `--baseline` — write current state to `scripts/.refactor_baseline.json`
- (no flag) — compare current tree to baseline, fail on drift
- `--smoke` — everything above + actually dispatch free tools through the real framework call path

**Strictness on smoke:** reject ANY of these as failures:
- Import error
- Tool name drift (missing or added names vs baseline)
- Decoupling regression (new imports from the refactored-away module)
- Response that starts with `"Error"` or `"Traceback"` (case-insensitive)
- Response that isn't valid JSON when JSON is expected

## Template

See `verify_refactor.py.template` in this directory for a Python starter that handles the FastMCP / FastAPI / Flask / Next.js dispatch patterns. Copy and customize `get_inventory()` and `run_smoke_tests()` for the target framework.

## When it fails in weird ways

- **"VERIFY PASSED" but PR still broken at deploy** — the smoke script didn't exercise the actual broken code path. Add more free tools to the dispatch list.
- **"✗ VERIFY FAILED" on a branch that should be clean** — the baseline is stale. Re-capture baseline with `--baseline` from current main.
- **Smoke hangs** — a framework call is blocking. Add a timeout to the asyncio.run() wrapper in the template.
- **Non-JSON return accepted as passing** — the template's smoke check is too lenient. Reject anything starting with `"Error"` or not parseable as JSON.
