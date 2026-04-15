# Linear Swarm Codex

`linear-swarm-codex` is the Codex-native control plane for the swarm workflow.

## Entry point

Use [swarm-codex](/Users/brandonguerrero/Documents/Orchid Automation/Orchid Labs/orchid-plugins/plugins/linear-swarm-codex/bin/swarm-codex) to prepare a run directory and, if you want, launch the shared cloud workers:

```bash
plugins/linear-swarm-codex/bin/swarm-codex --issue PLUXX-104 --dry-run
plugins/linear-swarm-codex/bin/swarm-codex --team-project PLUXX "My Project" --execute
```

## Design

- Codex handles scope audit, test design, review, fix-up coordination, and merge order.
- Cheap-tier cloud implementation stays delegated to `zai/glm-5.1` in Vercel Sandbox.
- The default worker agent provider is now `opencode`, not the Claude CLI path.
- Both plugins reuse the shared runtime under [`plugins/_shared/linear-swarm`](/Users/brandonguerrero/Documents/Orchid Automation/Orchid Labs/orchid-plugins/plugins/_shared/linear-swarm/runtime/sandbox_worker.mjs).

## Current split

```text
Codex plugin
  |
  +--> Linear scope + planning
  +--> test design
  +--> review + smoke + merge planning
  |
  +--> execution lane
         -> plugins/_shared/linear-swarm/bin/sandbox-worker
         -> Sandcastle
         -> Vercel Sandbox
         -> opencode
         -> GLM 5.1 via Vercel AI Gateway
```

## Near-term roadmap

1. Keep this plugin as the orchestration layer.
2. Grow the entrypoint from run-prep plus worker fan-out into a fuller end-to-end Codex flow.
3. Make the worker lane support more than `opencode` and `claude-code` when there is a proven gateway-compatible option.
