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

plugin_env() {
  local name="$1"
  local plugin_name="CLAUDE_PLUGIN_OPTION_${name}"
  if [ -n "${!name:-}" ]; then
    printf '%s' "${!name}"
  elif [ -n "${!plugin_name:-}" ]; then
    printf '%s' "${!plugin_name}"
  fi
}

git_repo_root() {
  if command -v git >/dev/null 2>&1; then
    git rev-parse --show-toplevel 2>/dev/null || true
  fi
}

vercel_cli_token() {
  python3 - <<'PY'
import json
from pathlib import Path

paths = [
    Path.home() / ".vercel" / "auth.json",
    Path.home() / "Library" / "Application Support" / "com.vercel.cli" / "auth.json",
]

for path in paths:
    if not path.exists():
        continue
    try:
        payload = json.loads(path.read_text())
    except Exception:
        continue
    token = payload.get("token")
    if token:
        print(token)
        break
PY
}

linked_vercel_project() {
  local repo_root="$1"
  [ -n "$repo_root" ] || return 1
  [ -f "$repo_root/.vercel/project.json" ] || return 1
}

sandbox_auth_ready() {
  local repo_root="$1"
  local oidc token team project
  oidc="$(plugin_env VERCEL_OIDC_TOKEN)"
  token="$(plugin_env VERCEL_TOKEN)"
  [ -n "$token" ] || token="$(plugin_env VERCEL_ACCESS_TOKEN)"
  [ -n "$token" ] || token="$(vercel_cli_token)"
  team="$(plugin_env VERCEL_TEAM_ID)"
  project="$(plugin_env VERCEL_PROJECT_ID)"

  if [ -n "$oidc" ]; then
    return 0
  fi

  if [ -n "$token" ] && [ -n "$team" ] && [ -n "$project" ]; then
    return 0
  fi

  if [ -n "$token" ] && linked_vercel_project "$repo_root"; then
    return 0
  fi

  return 1
}

blocking_missing=0
optional_missing=0
repo_root="$(git_repo_root)"

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
for tool in node npm vercel gitingest jq; do
  if command -v "$tool" >/dev/null 2>&1; then
    ok "$tool found (optional)"
  else
    warn "$tool not found (optional — used by some linear-swarm paths)"
    optional_missing=$((optional_missing + 1))
  fi
done

if [ -n "$repo_root" ]; then
  ok "git repository detected"
else
  warn "not currently inside a git repository (/linear-swarm needs a repo checkout)"
  blocking_missing=$((blocking_missing + 1))
fi

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
  if [ -n "$(plugin_env "$name")" ]; then
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

if [ -n "$(plugin_env LINEAR_API_KEY)" ]; then
  ok "LINEAR_API_KEY set"
else
  warn "LINEAR_API_KEY not set (linear-swarm will need interactive Linear auth and may stall in nested runs)"
  blocking_missing=$((blocking_missing + 1))
fi

if sandbox_auth_ready "$repo_root"; then
  ok "Vercel Sandbox auth available"
else
  warn "Vercel Sandbox auth not ready (optional — set VERCEL_OIDC_TOKEN, or VERCEL_TOKEN + VERCEL_TEAM_ID + VERCEL_PROJECT_ID, or sign in with the Vercel CLI and link the repo)"
fi

if [ "$blocking_missing" -gt 0 ]; then
  printf '\n  linear-swarm: %d blocking prerequisite(s). /linear-swarm will be blocked until fixed.\n\n' "$blocking_missing" >&2
elif [ "$optional_missing" -gt 0 ] || ! sandbox_auth_ready "$repo_root"; then
  printf '\n  linear-swarm: local worktree mode is available. Sandbox mode needs extra runtime/auth setup.\n\n' >&2
fi

# Always exit 0 — this is a soft warning hook
exit 0
