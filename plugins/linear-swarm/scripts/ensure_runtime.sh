#!/usr/bin/env bash
# ensure_runtime compatibility wrapper — delegates to the shared linear-swarm runtime

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SHARED_ROOT="$(cd "${SCRIPT_DIR}/../../_shared/linear-swarm" && pwd)"

export CLAUDE_PLUGIN_ROOT="${SHARED_ROOT}"

exec "${SHARED_ROOT}/scripts/ensure_runtime.sh" "$@"
