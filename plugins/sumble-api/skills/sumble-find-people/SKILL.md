---
name: sumble-find-people
description: Discover people at specific companies by role, seniority, location, and technical skills. Returns LinkedIn profiles and employment details. Use for identifying decision-makers, finding engineers, researching team structure, building prospect lists, or account mapping.
user-invocable: true
disable-model-invocation: true
argument-hint: "[domain and criteria, e.g. 'stripe.com engineers managers US']"
allowed-tools: Bash, Read
---

# Find People with Sumble

**User's request:** $ARGUMENTS

## Execution

1. Parse request for company domain, job functions, levels, countries
2. Map user intent to filters (see table below)
3. Run the shared helper — **ONE call, no retries, no debugging**:

```bash
python3 "PLUGIN_DIR/scripts/sumble_api.py" "people/find" '{"organization": {"domain": "stripe.com"}, "filters": {"job_functions": ["Engineer"], "job_levels": ["Manager", "Director"]}, "limit": 50}'
```

Replace `PLUGIN_DIR` with the absolute path to the `sumble-api` plugin directory.

**CRITICAL**: Do NOT use curl. Do NOT echo/test the API key. Do NOT show raw JSON. The helper handles auth, retries, errors, and formatting automatically.

## Intent → Filters Mapping

| User says | job_functions | job_levels |
|-----------|--------------|------------|
| "engineers" | `["Engineer"]` | — |
| "engineering managers" | `["Engineer"]` | `["Manager", "Director"]` |
| "decision makers" | — | `["Director", "VP", "C-Level"]` |
| "leadership" | — | `["VP", "Senior VP", "C-Level"]` |
| "sales team" | `["Sales"]` | — |
| "VPs of Sales" | `["Sales"]` | `["VP", "Senior VP"]` |
| "product managers" | `["Product"]` | `["Manager", "Director"]` |
| "C-suite" / "executives" | — | `["C-Level"]` |
| "marketing" | `["Marketing"]` | — |
| "DevOps" | `["DevOps Engineer"]` | — |

## Filters Reference

| Filter | Type | Example |
|--------|------|---------|
| job_functions | string[] | `["Engineer", "Sales"]` |
| job_levels | string[] | `["Manager", "Director", "VP", "C-Level"]` |
| countries | string[] | `["US", "CA", "GB"]` |
| technologies | string[] | `["python", "react"]` |
| since | string | `"2023-01-01"` |

**Organization ID**: domain (preferred), id, slug, or linkedin_url
**Pagination**: `limit` (1-250), `offset` (0-10000)
**Cost**: 1 credit per person returned
