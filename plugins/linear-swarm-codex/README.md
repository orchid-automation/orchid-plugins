# Linear Swarm Codex

`linear-swarm-codex` is the Codex-native control plane for the swarm workflow.

## Design

- Codex handles scope audit, test design, review, fix-up coordination, and merge order.
- Cheap-tier cloud implementation stays delegated to `zai/glm-5.1` in Vercel Sandbox.
- The first version deliberately reuses the proven execution helpers from [`plugins/linear-swarm`](/Users/brandonguerrero/Documents/Orchid Automation/Orchid Labs/orchid-plugins/plugins/linear-swarm/README.md) instead of forking a second runtime immediately.

## Current split

```text
Codex plugin
  |
  +--> Linear scope + planning
  +--> test design
  +--> review + smoke + merge planning
  |
  +--> execution lane
         -> plugins/linear-swarm/bin/sandbox-worker
         -> Sandcastle
         -> Vercel Sandbox
         -> GLM 5.1 via Vercel AI Gateway
```

## Near-term roadmap

1. Keep this plugin as the orchestration layer.
2. Extract shared worker/runtime helpers from `plugins/linear-swarm` into a common package.
3. Make the sandbox agent provider swappable so the execution lane can move off Claude tooling completely if needed.
