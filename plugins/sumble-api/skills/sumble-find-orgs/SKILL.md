---
name: sumble-find-orgs
description: Search for companies by technology stack, industry, employee count, location, and hiring trends using Sumble's sales intelligence database. Use when building target account lists, finding competitors, analyzing market segments, or researching companies that match specific tech criteria.
user-invocable: true
disable-model-invocation: true
argument-hint: "[technologies or criteria, e.g. 'python react US' or 'cybersecurity startups']"
allowed-tools: Bash, Read
---

# Find Organizations with Sumble

**User's request:** $ARGUMENTS

## Execution

1. Parse the request for technologies, industries, countries, employee count
2. Build the JSON payload (see filters below)
3. Run the shared helper — **ONE call, no retries, no debugging**:

```bash
python3 "PLUGIN_DIR/scripts/sumble_api.py" "organizations/find" '{"filters": {"technologies": ["python"]}, "limit": 20}'
```

Replace `PLUGIN_DIR` with the absolute path to the `sumble-api` plugin directory.

**CRITICAL**: Do NOT use curl. Do NOT echo/test the API key. Do NOT show raw JSON. The helper handles auth, retries, errors, and formatting automatically.

## Filters Reference

| Filter | Type | Example |
|--------|------|---------|
| technologies | string[] | `["python", "react"]` |
| technology_categories | string[] | `["cybersecurity", "databases"]` |
| industries | string[] | `["Information", "Finance"]` |
| countries | string[] | `["US", "CA"]` |
| employee_count | object | `{"min": 50, "max": 500}` |
| since | string | `"2023-01-01"` |

**Sorting**: `order_by_column` (employee_count, jobs_count, etc.) + `order_by_direction` (ASC/DESC)
**Pagination**: `limit` (1-200), `offset` (0-10000)
**Cost**: 5 credits per org per filter term (minimum 5)
