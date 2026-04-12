#!/usr/bin/env bash
# linear-swarm SessionStart preflight
# Prints a soft warning if required tools or env vars are missing.
# Does NOT block the session — only the UserPromptSubmit gate on /linear-swarm does that.

set -u

# Extra fallback for env-heavy setups; keep this silent so hook output stays clean
for f in "$HOME/.zshenv" "$HOME/.bashrc" "$HOME/.profile"; do
  [ -f "$f" ] && set -a && source "$f" 2>/dev/null && set +a
done

warn() { printf '  ⚠ %s\n' "$1"; }
ok()   { printf '  ✓ %s\n' "$1"; }

blocking_missing=0
optional_missing=0

# CLIs required for the default local flow
for tool in git gh python3; do
  if command -v "$tool" >/dev/null 2>&1; then
    ok "$tool found"
  else
    warn "$tool NOT found (required for linear-swarm)"
    blocking_missing=$((blocking_missing + 1))
  fi
done

# Optional CLIs
for tool in daytona gitingest jq; do
  if command -v "$tool" >/dev/null 2>&1; then
    ok "$tool found (optional)"
  else
    warn "$tool not found (optional — used by some linear-swarm paths)"
    optional_missing=$((optional_missing + 1))
  fi
done

# GitHub auth
if [ -n "${GH_TOKEN:-}" ] || [ -n "${GITHUB_TOKEN:-}" ]; then
  ok "GitHub token auth available"
elif gh auth status >/dev/null 2>&1; then
  ok "gh authenticated"
else
  warn "GitHub auth missing — set GH_TOKEN/GITHUB_TOKEN or run 'gh auth login'"
  blocking_missing=$((blocking_missing + 1))
fi

# Env vars
check_env() {
  local name="$1"
  local required="$2"
  if [ -n "${!name:-}" ]; then
    ok "$name set"
  elif [ "$required" = "required" ]; then
    warn "$name NOT set (required)"
    blocking_missing=$((blocking_missing + 1))
  else
    warn "$name not set (optional)"
  fi
}

# Note: we don't hard-fail on ANTHROPIC_API_KEY because Max subscription users
# don't need it set — Claude Code handles auth internally.
check_env "VERCEL_AI_GATEWAY_KEY" "optional"
check_env "DAYTONA_API_KEY" "optional"

if [ "$blocking_missing" -gt 0 ]; then
  printf '\n  linear-swarm: %d blocking prerequisite(s). /linear-swarm will be blocked until fixed.\n\n' "$blocking_missing" >&2
elif [ "$optional_missing" -gt 0 ]; then
  printf '\n  linear-swarm: local worktree mode is available. Optional Daytona-only dependencies are still missing.\n\n' >&2
fi

# Always exit 0 — this is a soft warning hook
exit 0
