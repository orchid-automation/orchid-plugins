#!/usr/bin/env bash
# linear-swarm SessionStart preflight
# Prints a soft warning if required tools or env vars are missing.
# Does NOT block the session — only the UserPromptSubmit gate on /linear-swarm does that.

set -u

warn() { printf '  ⚠ %s\n' "$1"; }
ok()   { printf '  ✓ %s\n' "$1"; }

missing=0

# CLIs
for tool in git gh daytona python3; do
  if command -v "$tool" >/dev/null 2>&1; then
    ok "$tool found"
  else
    warn "$tool NOT found (required for linear-swarm)"
    missing=$((missing + 1))
  fi
done

# Optional CLIs
for tool in gitingest jq; do
  if command -v "$tool" >/dev/null 2>&1; then
    ok "$tool found (optional)"
  else
    warn "$tool not found (optional — used by some linear-swarm paths)"
  fi
done

# gh auth
if gh auth status >/dev/null 2>&1; then
  ok "gh authenticated"
else
  warn "gh not authenticated — run 'gh auth login'"
  missing=$((missing + 1))
fi

# Env vars
check_env() {
  local name="$1"
  local required="$2"
  if [ -n "${!name:-}" ]; then
    ok "$name set"
  elif [ "$required" = "required" ]; then
    warn "$name NOT set (required)"
    missing=$((missing + 1))
  else
    warn "$name not set (optional)"
  fi
}

# Note: we don't hard-fail on ANTHROPIC_API_KEY because Max subscription users
# don't need it set — Claude Code handles auth internally.
check_env "VERCEL_AI_GATEWAY_KEY" "optional"
check_env "DAYTONA_API_KEY" "optional"

if [ "$missing" -gt 0 ]; then
  printf '\n  linear-swarm: %d missing prerequisite(s). /linear-swarm will be blocked until fixed.\n\n' "$missing" >&2
fi

# Always exit 0 — this is a soft warning hook
exit 0
