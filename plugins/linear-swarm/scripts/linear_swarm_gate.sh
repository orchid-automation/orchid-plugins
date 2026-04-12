#!/usr/bin/env bash
# linear-swarm UserPromptSubmit gate
# Blocks /linear-swarm invocations when required prerequisites are missing.
# Receives JSON on stdin via the hook API with `prompt` field.

set -u

# Extra fallback for env-heavy setups; keep this silent so hook output stays clean
for f in "$HOME/.zshenv" "$HOME/.bashrc" "$HOME/.profile"; do
  [ -f "$f" ] && set -a && source "$f" 2>/dev/null && set +a
done

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

command -v git       >/dev/null 2>&1 || missing+=("git CLI")
command -v gh        >/dev/null 2>&1 || missing+=("gh CLI (install with: brew install gh)")
command -v python3   >/dev/null 2>&1 || missing+=("python3")

if [ -n "${GH_TOKEN:-}" ] || [ -n "${GITHUB_TOKEN:-}" ]; then
  :
elif ! gh auth status >/dev/null 2>&1; then
  missing+=("GH_TOKEN/GITHUB_TOKEN env var or gh auth login")
fi

# Daytona is only required if --worker=daytona is in the prompt
if printf '%s' "$prompt" | grep -q -- '--worker=daytona'; then
  command -v daytona >/dev/null 2>&1 || missing+=("daytona CLI (install: brew install daytonaio/cli/daytona)")
  [ -n "${DAYTONA_API_KEY:-}" ] || missing+=("DAYTONA_API_KEY env var")
  [ -n "${VERCEL_AI_GATEWAY_KEY:-}" ] || missing+=("VERCEL_AI_GATEWAY_KEY env var")
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
