#!/usr/bin/env bash
# Validate the checked-in linear-swarm package and optionally replay it through
# a nested Claude CLI session.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PLUGIN_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
REPO_ROOT="$(cd "${PLUGIN_ROOT}/../.." && pwd)"

TARGET=""
LOG_DIR="${TMPDIR:-/tmp}/linear-swarm-validation"

usage() {
  cat <<'EOF'
Usage:
  validate_swarm.sh [--target '<linear-swarm args>']

Examples:
  validate_swarm.sh
  validate_swarm.sh --target 'PLUXX-96 --worker=sandbox --dry-run --skip-codex'

Behavior:
  1. Validates the plugin manifest
  2. Checks shell, Python, and Node syntax for shipped helpers
  3. Exercises the sandbox runtime bootstrap in an isolated cache dir
  4. Optionally replays the exact nested Claude invocation used by Codex:
     claude --plugin-dir ./plugins/linear-swarm -p "/linear-swarm:linear-swarm ..."
EOF
}

run_step() {
  local label="$1"
  shift
  printf '==> %s\n' "$label"
  "$@"
}

require_command() {
  local command_name="$1"
  if ! command -v "$command_name" >/dev/null 2>&1; then
    printf 'Error: required command not found: %s\n' "$command_name" >&2
    exit 1
  fi
}

claude_auth_ready() {
  if [ -n "${ANTHROPIC_API_KEY:-}" ]; then
    return 0
  fi

  claude auth status --json 2>/dev/null | python3 -c 'import json, sys; payload = json.load(sys.stdin); raise SystemExit(0 if payload.get("loggedIn") else 1)' >/dev/null 2>&1
}

while [ $# -gt 0 ]; do
  case "$1" in
    --target)
      [ $# -ge 2 ] || { printf 'Error: --target requires a value\n' >&2; exit 1; }
      TARGET="$2"
      shift 2
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      printf 'Error: unknown argument: %s\n' "$1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

require_command claude
require_command bash
require_command python3
require_command node
require_command npm

mkdir -p "$LOG_DIR"
scratch_root="$(mktemp -d "${TMPDIR:-/tmp}/linear-swarm-validate.XXXXXX")"
trap 'rm -rf "$scratch_root"' EXIT

run_step "Validate plugin manifest" claude plugin validate "$PLUGIN_ROOT"
run_step "Check shell wrapper syntax" bash -n \
  "$PLUGIN_ROOT/bin/daytona-worker" \
  "$PLUGIN_ROOT/bin/sandbox-worker" \
  "$PLUGIN_ROOT/scripts/ensure_runtime.sh" \
  "$PLUGIN_ROOT/scripts/preflight.sh" \
  "$PLUGIN_ROOT/scripts/linear_swarm_gate.sh"
run_step "Check Python helper syntax" env \
  PYTHONPYCACHEPREFIX="$scratch_root/pycache" \
  python3 -m py_compile \
  "$PLUGIN_ROOT/scripts/linear_api.py" \
  "$PLUGIN_ROOT/scripts/linear_comment.py"
run_step "Check sandbox runtime syntax" node --check "$PLUGIN_ROOT/runtime/sandbox_worker.mjs"

runtime_cache="$scratch_root/runtime-cache"
mkdir -p "$runtime_cache"
run_step "Install sandbox runtime into isolated cache" env \
  CLAUDE_PLUGIN_ROOT="$PLUGIN_ROOT" \
  CLAUDE_PLUGIN_DATA="$runtime_cache" \
  "$PLUGIN_ROOT/scripts/ensure_runtime.sh"

if [ -n "$TARGET" ]; then
  if ! claude_auth_ready; then
    printf 'Error: nested replay needs a Claude login or ANTHROPIC_API_KEY.\n' >&2
    exit 1
  fi

  timestamp="$(date +%Y%m%d%H%M%S)"
  nested_log="${LOG_DIR}/nested-${timestamp}.log"
  prompt="/linear-swarm:linear-swarm ${TARGET}"

  printf '==> Replay nested Claude session\n'
  printf '    prompt: %s\n' "$prompt"
  printf '    log: %s\n' "$nested_log"

  (
    cd "$REPO_ROOT"
    claude \
      --plugin-dir ./plugins/linear-swarm \
      --permission-mode bypassPermissions \
      --dangerously-skip-permissions \
      -p "$prompt"
  ) | tee "$nested_log"
fi
