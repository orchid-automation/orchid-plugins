#!/usr/bin/env bash
# Sync and install the linear-swarm runtime into plugin data.

set -euo pipefail

SOFT_FAIL="${LINEAR_SWARM_SOFT_FAIL:-0}"

warn() {
  printf '  ⚠ %s\n' "$1" >&2
}

fail() {
  if [ "$SOFT_FAIL" = "1" ]; then
    warn "$1"
    exit 0
  fi

  printf 'Error: %s\n' "$1" >&2
  exit 1
}

for tool in node npm; do
  if ! command -v "$tool" >/dev/null 2>&1; then
    fail "$tool is required for sandbox-worker runtime setup"
  fi
done

PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}"

if [ -n "${CLAUDE_PLUGIN_DATA:-}" ]; then
  PLUGIN_DATA="$CLAUDE_PLUGIN_DATA"
elif [ -n "${XDG_CACHE_HOME:-}" ]; then
  PLUGIN_DATA="${XDG_CACHE_HOME}/claude-code/linear-swarm"
else
  PLUGIN_DATA="${HOME}/.cache/claude-code/linear-swarm"
fi

RUNTIME_SRC="${PLUGIN_ROOT}/runtime"
RUNTIME_DST="${PLUGIN_DATA}/runtime"
STAMP_FILE="${RUNTIME_DST}/.install-stamp"
LOG_FILE="${RUNTIME_DST}/npm-install.log"

mkdir -p "$RUNTIME_DST"
cp "${RUNTIME_SRC}/package.json" "${RUNTIME_DST}/package.json"
cp "${RUNTIME_SRC}/package-lock.json" "${RUNTIME_DST}/package-lock.json"
cp "${RUNTIME_SRC}/sandbox_worker.mjs" "${RUNTIME_DST}/sandbox_worker.mjs"

LOCK_HASH="$(shasum -a 256 "${RUNTIME_DST}/package-lock.json" | awk '{print $1}')"
CURRENT_HASH=""

if [ -f "$STAMP_FILE" ]; then
  CURRENT_HASH="$(cat "$STAMP_FILE")"
fi

if [ ! -d "${RUNTIME_DST}/node_modules" ] || [ "$CURRENT_HASH" != "$LOCK_HASH" ]; then
  rm -f "$LOG_FILE"
  if ! npm ci --no-audit --no-fund --silent --prefix "$RUNTIME_DST" >"$LOG_FILE" 2>&1; then
    if [ "$SOFT_FAIL" = "1" ]; then
      warn "sandbox runtime install failed; local worktree mode is still available"
      tail -n 20 "$LOG_FILE" >&2 || true
      exit 0
    fi

    printf 'Failed to install linear-swarm sandbox runtime. Recent npm output:\n' >&2
    tail -n 40 "$LOG_FILE" >&2 || true
    exit 1
  fi

  printf '%s' "$LOCK_HASH" >"$STAMP_FILE"
fi
