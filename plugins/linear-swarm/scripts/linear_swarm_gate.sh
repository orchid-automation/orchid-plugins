#!/usr/bin/env bash
# linear-swarm UserPromptSubmit gate
# Blocks /linear-swarm invocations when required prerequisites are missing.
# Receives JSON on stdin via the hook API with `prompt` field.

set -u

# Extra fallback for env-heavy setups; keep this silent so hook output stays clean
for f in "$HOME/.zshenv" "$HOME/.bashrc" "$HOME/.profile"; do
  [ -f "$f" ] && set -a && source "$f" 2>/dev/null && set +a
done

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

# Only gate /linear-swarm prompts — let everything else through
input=$(cat)
prompt=$(printf '%s' "$input" | python3 -c 'import json,sys; d=json.loads(sys.stdin.read()); print(d.get("prompt",""))' 2>/dev/null || true)

# Trigger check: only inspect prompts that mention /linear-swarm
case "$prompt" in
  */linear-swarm*|*linear-swarm:*) ;;
  *) exit 0 ;;
esac

# Collect missing prerequisites
missing=()
repo_root="$(git_repo_root)"

command -v git       >/dev/null 2>&1 || missing+=("git CLI")
command -v gh        >/dev/null 2>&1 || missing+=("gh CLI (install with: brew install gh)")
command -v python3   >/dev/null 2>&1 || missing+=("python3")
[ -n "$repo_root" ] || missing+=("an active git repository checkout")

if [ -n "${GH_TOKEN:-}" ] || [ -n "${GITHUB_TOKEN:-}" ]; then
  :
elif ! gh auth status >/dev/null 2>&1; then
  missing+=("GH_TOKEN/GITHUB_TOKEN env var or gh auth login")
fi

# Sandbox mode is optional and only required when explicitly selected.
if printf '%s' "$prompt" | grep -Eq -- '--worker=(sandbox|vercel|vercel-sandbox|daytona)'; then
  command -v node >/dev/null 2>&1 || missing+=("node CLI (required for sandbox-worker runtime)")
  command -v npm >/dev/null 2>&1 || missing+=("npm CLI (required for sandbox-worker runtime)")
  [ -n "$(plugin_env VERCEL_AI_GATEWAY_KEY)" ] || missing+=("VERCEL_AI_GATEWAY_KEY env var or plugin setting")
  sandbox_auth_ready "$repo_root" || missing+=("Vercel Sandbox auth: VERCEL_OIDC_TOKEN, or VERCEL_TOKEN plus VERCEL_TEAM_ID and VERCEL_PROJECT_ID, or a logged-in Vercel CLI plus a linked .vercel/project.json")
fi

if [ ${#missing[@]} -gt 0 ]; then
  printf '\n🚫 linear-swarm blocked — missing prerequisites:\n\n' >&2
  for item in "${missing[@]}"; do
    printf '  ✗ %s\n' "$item" >&2
  done
  printf '\nFix the above, then re-run your /linear-swarm command.\n\n' >&2
  # Exit 2 = block the prompt per Claude Code hooks API
  exit 2
fi

exit 0
