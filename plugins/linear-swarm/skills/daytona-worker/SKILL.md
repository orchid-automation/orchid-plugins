---
name: daytona-worker
description: Internal skill. Runs a headless Claude Code worker inside a Daytona sandbox with a cheap model (GLM 5.1 / Kimi K2.5 / MiniMax) via Vercel AI Gateway. Clones the target repo throwaway, executes a self-contained brief, commits, and pushes so the orchestrator can mirror the branch into a local worktree for later review, fix-up, smoke, and PR phases. Used by linear-swarm Phase 1 when --worker=daytona.
user-invocable: false
allowed-tools: Bash, Read, Write
---

# Daytona Worker

This skill wraps the "headless Claude Code in a Daytona sandbox via Vercel AI Gateway" pattern. It's called by `linear-swarm` Phase 1 when the user picks `--worker=daytona`.

**This is NOT a user-invocable skill.** It's an internal primitive.

## Inputs

```
{
  "ticket_id": "<LINEAR-ID>",
  "branch": "<gitBranchName from Linear>",
  "model": "zai/glm-5.1" | "moonshotai/kimi-k2.5" | "anthropic/claude-haiku-4.5" | "minimax/minimax-m2.7",
  "brief": "<full self-contained task description with files + tests>",
  "repo_url": "https://github.com/<owner>/<repo>.git",
  "base_branch": "main"
}
```

## Prerequisites (validated by preflight hook)

- `daytona` CLI installed and authenticated (`daytona login --api-key $DAYTONA_API_KEY`)
- A sandbox exists and is reachable (default: `claude-sandbox`)
- `VERCEL_AI_GATEWAY_KEY` set in env
- `GH_TOKEN` / `GITHUB_TOKEN` is set, or `gh auth token` succeeds (we pass this token into the sandbox for clone + push)

## Steps

### 1. Wake sandbox
```bash
daytona start claude-sandbox 2>&1 | tail -3
```
The sandbox ships with `claude` v2.1.19 pre-installed at `/usr/local/share/nvm/current/bin/claude`. No install needed.

### 2. Throwaway clone
```bash
GH_TOKEN=${GH_TOKEN:-${GITHUB_TOKEN:-$(gh auth token)}}
daytona exec claude-sandbox -- rm -rf /tmp/<repo>
daytona exec claude-sandbox -- git clone --depth 1 \
  "https://$GH_TOKEN@github.com/<owner>/<repo>.git" /tmp/<repo>
```

### 3. Set git identity + branch
```bash
daytona exec claude-sandbox -- git -C /tmp/<repo> config user.email brandon@orchidautomation.com
daytona exec claude-sandbox -- git -C /tmp/<repo> config user.name orchid-linear-swarm
daytona exec claude-sandbox -- git -C /tmp/<repo> checkout -b <branch>
```

### 4. Run headless Claude via Vercel AI Gateway

**Daytona exec has brutal shell-quoting.** Never pass multi-line prompts or anything with parens/brackets directly. Use the base64-wrapped Python subprocess pattern:

Write a local Python wrapper file with `env=` and `subprocess.run(['claude', '-p', '--dangerously-skip-permissions', prompt], ...)`:

```python
# /tmp/swarm_run_claude.py
import subprocess, os
env = os.environ.copy()
env['ANTHROPIC_BASE_URL'] = 'https://ai-gateway.vercel.sh'
env['ANTHROPIC_AUTH_TOKEN'] = '<VAG_KEY>'
env['ANTHROPIC_API_KEY'] = ''   # MUST be empty string, not unset
env['ANTHROPIC_DEFAULT_SONNET_MODEL'] = '<model>'
prompt = """<full brief>"""
result = subprocess.run(
    ['claude', '-p', '--dangerously-skip-permissions', prompt],
    env=env, capture_output=True, text=True, timeout=900, cwd='/tmp/<repo>'
)
print(result.stdout)
print(result.stderr[-2000:])
print("rc:", result.returncode)
```

Then base64-encode and exec via Python in the sandbox:
```bash
B64=$(base64 < /tmp/swarm_run_claude.py | tr -d '\n')
daytona exec claude-sandbox -- python3 -c 'exec\(__import__\(\"base64\"\).b64decode\(\"'$B64'\"\).decode\(\)\)'
```

**Shell-quoting rules (from prior debugging):**
- **Always** single-quote on the Mac side with backslash-escaped parens: `'exec\(\)'`
- **Never** put spaces, parens, or `/` in commit messages passed via `git commit -m` on `daytona exec` — daytona word-splits them
- Use a Python wrapper for anything non-trivial

### 5. Verify the diff
```bash
daytona exec claude-sandbox -- git -C /tmp/<repo> diff --stat
daytona exec claude-sandbox -- git -C /tmp/<repo> diff
```
Send the diff back to the orchestrator, then mirror the pushed branch into a local worktree:

```bash
git fetch origin <branch>
git worktree add .claude/worktrees/<ticket-id> -B <branch> FETCH_HEAD
```

All later phases operate on that local mirror worktree. Daytona is the Phase 1 implementation engine, not the long-lived fix-up environment.

### 6. Commit + push (via Python wrapper to avoid shell-quoting issues)

```python
# /tmp/swarm_commit.py
import subprocess
msg = "<conventional commit message>"
subprocess.run(['git', '-C', '/tmp/<repo>', 'add', '-A'], check=True)
subprocess.run(['git', '-C', '/tmp/<repo>', 'commit', '-m', msg], check=True)
subprocess.run(['git', '-C', '/tmp/<repo>', 'push', '--force', 'origin', '<branch>'], check=True)
```

Then base64 + exec as in Step 4.

**Important**: use `--force`, NOT `--force-with-lease`. The lease check rejects pushes from a sandbox with stale refs.

### 7. Report back
Print the final commit hash + branch + test-spec pass/fail to the orchestrator. The wrapper must exit non-zero if the Claude run, commit, or push failed; the orchestrator should never treat a failed sandbox run as READY.

## Model escalation (on smoke failure)

The orchestrator calls this skill with `model` picked from the ladder:
1. `zai/glm-5.1` — default
2. `moonshotai/kimi-k2.5` — fallback
3. `anthropic/claude-haiku-4.5` — guaranteed-compat
4. Claude Opus via Max (orchestrator switches from Daytona to local worktree)

On each failure, orchestrator re-invokes this skill with the next tier for a fresh Phase 1 attempt. Once the branch has been mirrored locally, later fix-up rounds happen in the local worktree, not by `SendMessage` to this one-shot skill.

## Known sandbox constraints

- **Daytona cannot reach most consumer websites** (Cloudflare edge TLS-rejects datacenter IPs). `api.firecrawl.dev`, `ollama.com`, `tryprofound.com` are all blocked.
- **Reachable from Daytona**: `ai-gateway.vercel.sh`, `github.com`, `npm registry`, `google.com`, plain non-Cloudflare sites.
- **Ollama Cloud / Ollama Pro ($20/mo) does NOT help** — same blocked hostname, no datacenter bypass mode.

This is why the sandbox path is **file-editing only**, not web-scraping. Inputs must be pre-fetched on the Mac side and passed in the brief.

## Cleanup

After the orchestrator confirms the branch is pushed and the PR is open:
```bash
daytona exec claude-sandbox -- rm -rf /tmp/<repo>
```

Leave the sandbox running (next swarm run reuses it) or stop it (`daytona stop claude-sandbox`) if you're done for the session.
