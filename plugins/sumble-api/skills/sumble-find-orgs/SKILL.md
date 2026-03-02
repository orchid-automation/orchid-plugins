---
name: sumble-find-orgs
description: Search for companies by technology stack, industry, employee count, location, and hiring trends using Sumble's sales intelligence database. Use when building target account lists, finding competitors, analyzing market segments, or researching companies that match specific tech criteria.
user-invocable: true
disable-model-invocation: true
argument-hint: "[technologies or criteria, e.g. 'python react US' or 'cybersecurity startups']"
allowed-tools: Bash(python3 *), Read
---

# Find Organizations with Sumble

**User's request:** $ARGUMENTS

## Script path

!`find ~/.claude/plugins -path "*/sumble-api/scripts/sumble_api.py" 2>/dev/null | head -1`

## Execution

Run **one** command. Do not use curl. Do not test the API key.

```bash
python3 "<script path from above>" "organizations/find" '{
  "filters": {"technologies": ["python", "react"], "countries": ["US"]},
  "order_by_column": "employee_count",
  "order_by_direction": "DESC",
  "limit": 20
}'
```

The script handles auth, retries, errors, and output formatting.

## Available filters

| Filter | Type | Example |
|--------|------|---------|
| technologies | string[] | `["python", "react"]` |
| technology_categories | string[] | `["cybersecurity", "databases"]` |
| industries | string[] | `["Information", "Finance"]` |
| countries | string[] | `["US", "CA"]` |
| employee_count | object | `{"min": 50, "max": 500}` |
| since | string | `"2023-01-01"` |

**Sorting**: `order_by_column` (employee_count, jobs_count, people_count, jobs_count_growth_6mo, cloud_spend_estimate_millions_usd) + `order_by_direction` (ASC/DESC)
**Pagination**: `limit` (1-200), `offset` (0-10000)
**Cost**: 5 credits per org per filter term (minimum 5)

For API details, see [common.md](references/common.md). For troubleshooting, see [troubleshooting.md](../sumble-api/references/troubleshooting.md).
