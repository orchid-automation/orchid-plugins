---
name: sumble-find-people
description: Find people at a company by role, seniority, location, and tech skills using Sumble API. Returns LinkedIn profiles, titles, and employment details.
user-invocable: true
argument-hint: "[domain and criteria, e.g. 'stripe.com engineers managers US']"
allowed-tools: Bash, Read
---

# Find People with Sumble

Find people at a specific organization using the Sumble API.

**User's request:** $ARGUMENTS

---

## CRITICAL: Execution Rules

1. **NO debugging in front of the user.** If a request fails, try ONE alternative silently. If it still fails, report the error cleanly.
2. **Do NOT echo, print, or test the API key.** Assume it's set.
3. **Do NOT show raw JSON responses.** Parse them and present clean formatted output only.
4. **Make exactly ONE curl call.** Do not retry with different auth formats or headers.
5. **Go straight to the API call.** Do not ask clarifying questions if you can infer from context.

## Your Task

1. Parse the user's request to identify the target company and filter criteria
2. Build the JSON request body
3. Execute the curl command (using the EXACT format below)
4. Parse the JSON response with `python3 -c` and present a clean markdown table

## Authentication — USE THIS EXACT FORMAT

```bash
curl -s -X POST https://api.sumble.com/v3/people/find \
  -H "Authorization: Bearer ${SUMBLE_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{ ... }'
```

**IMPORTANT**: Always use `${SUMBLE_API_KEY}` with curly braces. Do NOT test if the key is set — just use it.

## Endpoint Details

**Method:** POST
**URL:** `https://api.sumble.com/v3/people/find`
**Cost:** 1 credit per person returned

### Organization Identifier (provide ONE)

- `{"domain": "stripe.com"}` — Company domain
- `{"id": 1726684}` — Sumble organization ID
- `{"slug": "stripe"}` — Sumble organization slug
- `{"linkedin_url": "https://www.linkedin.com/company/stripe"}` — LinkedIn company URL

### Filter Options

- **job_functions**: `Engineer`, `Software Engineer`, `Frontend Engineer`, `Backend Engineer`, `Data Engineer`, `DevOps Engineer`, `Sales`, `Marketing`, `Operations`, `Product`, `Design`
- **job_levels**: `Individual Contributor`, `Manager`, `Senior Manager`, `Director`, `Senior Director`, `VP`, `Senior VP`, `C-Level`
- **countries**: Array of country codes (e.g., `["US", "CA", "GB"]`)
- **technologies**: Array of technology names
- **since**: ISO date (e.g., `"2023-01-01"`)

### Pagination

- **limit**: 1-250 (default: 10)
- **offset**: 0-10000 (default: 0)

## Mapping User Intent to Filters

| User says | job_functions | job_levels |
|-----------|--------------|------------|
| "engineers" | `["Engineer"]` | — |
| "engineering managers" | `["Engineer"]` | `["Manager", "Director"]` |
| "decision makers" | — | `["Director", "VP", "C-Level"]` |
| "leadership" | — | `["VP", "Senior VP", "C-Level"]` |
| "sales team" | `["Sales"]` | — |
| "VPs of Sales" | `["Sales"]` | `["VP", "Senior VP"]` |
| "product managers" | `["Product"]` | `["Manager", "Director"]` |
| "C-suite" | — | `["C-Level"]` |

## Example Execution (copy this pattern)

```bash
curl -s -X POST https://api.sumble.com/v3/people/find \
  -H "Authorization: Bearer ${SUMBLE_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "organization": {"domain": "stripe.com"},
    "filters": {
      "job_functions": ["Engineer"],
      "job_levels": ["Manager", "Director"],
      "countries": ["US"]
    },
    "limit": 50
  }' | python3 -c "
import json, sys
data = json.load(sys.stdin)
if 'detail' in data:
    print(f'Error: {data[\"detail\"]}')
    sys.exit(1)
print(f'Found {data.get(\"people_count\", 0)} people | Credits used: {data.get(\"credits_used\", 0)} | Remaining: {data.get(\"credits_remaining\", \"?\")}')
print()
for p in data.get('people', []):
    print(f'- **{p[\"name\"]}** — {p.get(\"job_title\", \"N/A\")} ({p.get(\"job_level\", \"\")})')
    print(f'  Location: {p.get(\"location\", \"N/A\")} | Started: {p.get(\"start_date\", \"N/A\")}')
    if p.get('linkedin_url'):
        print(f'  LinkedIn: {p[\"linkedin_url\"]}')
    print()
"
```

## Output Instructions

- Present results as a clean markdown list or table — NEVER show raw JSON
- Include: name, title, level, location, start date, LinkedIn URL
- Show total people found and credits used/remaining
- If 0 results: suggest broadening the search (remove function filter, or try different levels)
- Suggest follow-up: `/sumble-enrich` or `/sumble-find-jobs`
