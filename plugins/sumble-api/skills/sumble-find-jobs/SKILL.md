---
name: sumble-find-jobs
description: Search job postings by company, technologies, job functions, and location using Sumble's sales intelligence database. Returns structured job data with extracted tech stacks. Use for hiring trend analysis, tech stack discovery, competitive intelligence, market sizing, or identifying companies scaling specific teams.
user-invocable: true
disable-model-invocation: true
argument-hint: "[domain or criteria, e.g. 'stripe.com python' or 'AI engineers US']"
allowed-tools: Bash, Read
---

# Find Jobs with Sumble

**User's request:** $ARGUMENTS

## Execution

1. Parse request for company domain (optional), technologies, job functions, countries
2. If no company specified, set organization to `null` for broad search
3. Run the shared helper — **ONE call, no retries, no debugging**:

```bash
python3 "PLUGIN_DIR/scripts/sumble_api.py" "jobs/find" '{"organization": {"domain": "stripe.com"}, "filters": {"technologies": ["python"], "job_functions": ["Engineer"]}, "limit": 25}'
```

For broad search (no specific company):
```bash
python3 "PLUGIN_DIR/scripts/sumble_api.py" "jobs/find" '{"organization": null, "filters": {"technology_categories": ["artificial-intelligence"], "countries": ["US"]}, "limit": 25}'
```

Replace `PLUGIN_DIR` with the absolute path to the `sumble-api` plugin directory.

**CRITICAL**: Do NOT use curl. Do NOT echo/test the API key. Do NOT show raw JSON. The helper handles auth, retries, errors, and formatting automatically.

## Filters Reference

| Filter | Type | Example |
|--------|------|---------|
| technologies | string[] | `["python", "react", "kubernetes"]` |
| technology_categories | string[] | `["artificial-intelligence", "databases"]` |
| job_functions | string[] | `["Engineer", "Data Scientist"]` |
| countries | string[] | `["US", "CA"]` |
| since | string | `"2024-01-01"` |

**Organization**: domain, id, slug, linkedin_url, or `null` (all companies)
**Pagination**: `limit` (1-100), `offset` (0-10000)
**Cost**: 3 credits per job returned
