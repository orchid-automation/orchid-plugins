---
name: prod-verify
description: Internal skill. After deploy rollover, calls the live production service through a real authenticated client (local MCP, authenticated curl, or integration script) to catch ops-config regressions that CI and structural smoke miss. Used by linear-swarm Phase 8.
user-invocable: false
allowed-tools: Bash, Read, Skill, ToolSearch
---

# Prod Verify

The phase that crosses **code ↔ ops**. Called by `linear-swarm` Phase 8 after deploy rollover confirms a version signal.

## Why this exists

Every earlier phase validates CODE:
- Phase 2 review — judges code quality
- Phase 4 smoke — validates code dispatches through the framework
- Phase 7 version probe — confirms new code is running

**None of them catch ops drift.** Missing env vars, unset secrets, unflipped feature flags, un-applied DB migrations — these look like perfectly successful deploys until the first live request fails.

The only way to catch ops drift is to **call the live service** with a **real authenticated client** and probe features that depend on ops config.

## The failure case this skill exists for

A PR adds a fail-closed check for a new env var (e.g., an encryption key). It merges, deploys, `/health` returns 200, all structural smoke passes, ship signal confirmed. Then a real client calls the service and gets:

```
Error: REQUIRED_ENV_VAR must be set in production
```

The env var was never set on the deploy platform. **Silent-broken deploy.** This happens any time code adds a new ops dependency (env var, secret, feature flag, DB migration) without the ops side being configured first.

This skill would have caught it. It calls the live service through a real client and specifically probes features that depend on ops config.

## Inputs

- Deployed service URL (auto-detected from repo config — Railway, Vercel, Fly, etc.)
- Authenticated client options (prioritized):
  1. Local MCP plugin pointing at prod — BEST, uses real framework dispatch
  2. Authenticated curl/httpx script with real credentials
  3. `gh pr checks` (CI smoke)
- List of 3-5 features that exercise ops config (env vars, secrets, flags, migrations)

## Steps

### 1. Identify the client

Check what's available:
- Is there an MCP plugin already installed that points at the target prod URL?
- Is there an authenticated integration script in the repo?
- Fall back to `gh pr checks` summary

### 2. Pick probe tests

For each feature that depends on ops config, pick a call that will fail if the config isn't set:
- **Encryption key** → call a tool that reads/writes encrypted state
- **OAuth client secret** → call a tool that initiates OAuth flow
- **Feature flag** → call a tool the flag gates
- **DB migration** → call a tool that reads/writes the new schema
- **Rate limit config** → call a tool that triggers limit (should 429, not 500)

### 3. Call through the real client

```python
# If there's a local MCP plugin:
Skill(<plugin>:<tool>)
  with args that exercise ops-dependent paths
```

```bash
# If not:
curl -sS -H "Authorization: Bearer $PROD_API_KEY" \
     -H "Content-Type: application/json" \
     -X POST https://<prod-url>/<endpoint> \
     -d '{"<args that trigger ops path>"}'
```

### 4. Assert no ops-config errors

Reject responses that contain:
- `"must be set"` (env var missing)
- `"not configured"` (feature flag missing)
- `"migration"` (schema drift)
- `"key not found"` (secret missing)
- HTTP 500 with an env-var-shaped error

### 5. On failure — diagnose and recover

**Ops config missing** (e.g., env var not set on the deploy platform):
1. Identify which var / secret / flag is missing from the error
2. Set it via the platform CLI:
   - Railway: `railway variables --set "KEY=value"` (triggers redeploy)
   - Vercel: `vercel env add KEY` + `vercel deploy --prod`
   - Fly: `fly secrets set KEY=value` (triggers redeploy)
3. Poll `/health` for redeploy completion
4. Re-run this skill

**Code bug (ops config IS set but the code is wrong):**
1. Mini-swarm one hotfix ticket through `linear-swarm` for that specific fix
2. Do NOT move Linear issues to Done until this passes

## Hard rule

**DO NOT let the orchestrator advance to Phase 9 (cleanup + Linear → Done) until this skill passes.** "In Review" is the holding state. Prod smoke is the gate.

## What good looks like

```
=== Prod Smoke Results ===
Target: https://api.your-service.sh
Client: local MCP plugin pointing at prod

✓ health             → 200
✓ free-tool-1       → valid JSON
✓ free-tool-2       → valid response
✓ <ops-dependent>    → succeeded (encryption key present)
✓ <feature flag>     → new feature path active
✓ <migration check>  → new columns populated

All production probes passing. Safe to close Linear issues.
```

## What bad looks like

```
=== Prod Smoke Results ===
✓ health             → 200
✓ free-tool-1       → valid JSON
✗ protected-tool    → Error: ENCRYPTION_KEY must be set in production
                       
BLOCKER: env var missing on deploy platform. Setting now...
  <platform> variables --set "ENCRYPTION_KEY=<generated>"
  Waiting for redeploy...
  
Retrying probes after redeploy...
✓ protected-tool    → succeeded

All production probes passing. Safe to close Linear issues.
```
