---
name: sumble-find-people
description: Discover people at specific companies by role, seniority, location, and technical skills. Returns LinkedIn profiles and employment details. Use for identifying decision-makers, finding engineers, researching team structure, building prospect lists, or account mapping.
user-invocable: true
disable-model-invocation: true
argument-hint: "[domain and criteria, e.g. 'stripe.com engineers managers US']"
allowed-tools: Bash(python3 *), Read
---

# Find People with Sumble

**User's request:** $ARGUMENTS

## Script path

!`find ~/.claude/plugins -path "*/sumble-api/scripts/sumble_api.py" 2>/dev/null | head -1`

## Execution

Run **one** command. Do not use curl. Do not test the API key.

```bash
python3 "<script path from above>" "people/find" '{
  "organization": {"domain": "DOMAIN"},
  "filters": {FILTERS},
  "limit": 50
}'
```

The script handles auth, retries, errors, domain normalization, and output formatting.

## Intent → Filters

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

## Available filters

- **job_functions**: `Engineer`, `Software Engineer`, `Frontend Engineer`, `Backend Engineer`, `Data Engineer`, `DevOps Engineer`, `Sales`, `Marketing`, `Operations`, `Product`, `Design`
- **job_levels**: `Individual Contributor`, `Manager`, `Senior Manager`, `Director`, `Senior Director`, `VP`, `Senior VP`, `C-Level`
- **countries**: ISO codes like `["US", "CA", "GB"]`
- **technologies**: `["python", "react"]`
- **since**: `"2023-01-01"`
- **limit**: 1-250

**Organization ID**: domain (preferred), id, slug, or linkedin_url
**Cost**: 1 credit per person

For API details, see [common.md](references/common.md). For troubleshooting, see [troubleshooting.md](../sumble-api/references/troubleshooting.md).
