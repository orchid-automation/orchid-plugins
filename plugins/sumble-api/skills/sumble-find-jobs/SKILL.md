---
name: sumble-find-jobs
description: Search job postings by company, technologies, job functions, and location using Sumble API. Returns structured job data with extracted tech stacks for hiring trend analysis.
user-invocable: true
argument-hint: "[domain or criteria, e.g. 'stripe.com python' or 'AI startups US']"
allowed-tools: Bash, Read
---

# Find Jobs with Sumble

Search job postings using the Sumble API.

**User's request:** $ARGUMENTS

---

## CRITICAL: Execution Rules

1. **NO debugging in front of the user.** If a request fails, try ONE alternative silently. If it still fails, report the error cleanly.
2. **Do NOT echo, print, or test the API key.** Assume it's set.
3. **Do NOT show raw JSON responses.** Parse them and present clean formatted output only.
4. **Make exactly ONE curl call.** Do not retry with different auth formats or headers.
5. **Go straight to the API call.** Do not ask clarifying questions if you can infer from context.

## Your Task

1. Parse the user's request to identify target company (if any) and filter criteria
2. Build the JSON request body — set `organization` to `null` for broad searches
3. Execute the curl command (using the EXACT format below)
4. Parse the JSON response and present clean formatted output

## Authentication — USE THIS EXACT FORMAT

```bash
curl -s -X POST https://api.sumble.com/v3/jobs/find \
  -H "Authorization: Bearer ${SUMBLE_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{ ... }'
```

**IMPORTANT**: Always use `${SUMBLE_API_KEY}` with curly braces. Do NOT test if the key is set — just use it.

## Endpoint Details

**Method:** POST
**URL:** `https://api.sumble.com/v3/jobs/find`
**Cost:** 3 credits per job returned

### Organization Identifier (optional — set to `null` for broad search)

- `{"domain": "stripe.com"}` — Company domain
- `{"id": 1726684}` — Sumble organization ID
- `null` — Search across ALL organizations

### Filter Options

- **technologies**: Array of technology names (e.g., `["python", "react", "kubernetes"]`)
- **technology_categories**: Array of category names (e.g., `["cloud-infrastructure", "artificial-intelligence"]`)
- **job_functions**: Array of job function names (e.g., `["Engineer", "Data Scientist"]`)
- **countries**: Array of country codes (e.g., `["US", "CA"]`)
- **since**: Date filter (ISO format: `"2024-01-01"`)

### Pagination

- **limit**: 1-100 (default: 10)
- **offset**: 0-10000 (default: 0)

## Example Execution (copy this pattern)

```bash
curl -s -X POST https://api.sumble.com/v3/jobs/find \
  -H "Authorization: Bearer ${SUMBLE_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "organization": {"domain": "stripe.com"},
    "filters": {
      "technologies": ["python", "react"],
      "job_functions": ["Engineer"],
      "since": "2024-01-01"
    },
    "limit": 25
  }' | python3 -c "
import json, sys
data = json.load(sys.stdin)
if 'detail' in data:
    print(f'Error: {data[\"detail\"]}')
    sys.exit(1)
print(f'Found {data.get(\"total\", 0)} jobs | Credits used: {data.get(\"credits_used\", 0)} | Remaining: {data.get(\"credits_remaining\", \"?\")}')
print()
for j in data.get('jobs', []):
    print(f'- **{j.get(\"job_title\", \"N/A\")}** at {j.get(\"organization_name\", \"\")} ({j.get(\"organization_domain\", \"\")})')
    print(f'  Location: {j.get(\"location\", \"N/A\")} | Technologies: {j.get(\"matched_technologies\", \"N/A\")}')
    print(f'  Posted: {j.get(\"datetime_pulled\", \"N/A\")[:10]}')
    if j.get('url'):
        print(f'  Details: {j[\"url\"]}')
    print()
"
```

## Output Instructions

- Present results as a clean markdown list — NEVER show raw JSON
- Include: job title, company, location, matched technologies, date posted
- Show total results and credits used/remaining
- For trend analysis, summarize: most common technologies, geographic distribution
- Suggest follow-up: `/sumble-enrich` or `/sumble-find-people`
