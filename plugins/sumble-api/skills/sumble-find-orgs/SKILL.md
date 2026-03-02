---
name: sumble-find-orgs
description: Search for companies by technology stack, industry, employee count, and location using Sumble API. Returns matching organizations with tech usage data and firmographics.
user-invocable: true
argument-hint: "[technologies or criteria, e.g. 'python react cybersecurity US']"
allowed-tools: Bash, Read
---

# Find Organizations with Sumble

Search for companies matching the user's criteria using the Sumble API.

**User's request:** $ARGUMENTS

---

## CRITICAL: Execution Rules

1. **NO debugging in front of the user.** If a request fails, try ONE alternative silently. If it still fails, report the error cleanly.
2. **Do NOT echo, print, or test the API key.** Assume it's set.
3. **Do NOT show raw JSON responses.** Parse them and present clean formatted output only.
4. **Make exactly ONE curl call.** Do not retry with different auth formats or headers.
5. **Go straight to the API call.** Do not ask clarifying questions if you can infer from context.

## Your Task

1. Parse the user's request to identify filter criteria (technologies, industries, countries, employee count, etc.)
2. Build the JSON request body
3. Execute the curl command (using the EXACT format below)
4. Parse the JSON response with `python3 -c` and present a clean markdown table

## Authentication — USE THIS EXACT FORMAT

```bash
curl -s -X POST https://api.sumble.com/v3/organizations/find \
  -H "Authorization: Bearer ${SUMBLE_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{ ... }'
```

**IMPORTANT**: Always use `${SUMBLE_API_KEY}` with curly braces. Do NOT test if the key is set — just use it.

## Endpoint Details

**Method:** POST
**URL:** `https://api.sumble.com/v3/organizations/find`
**Cost:** 5 credits per organization, per filter term (minimum 5)

### Filter Options

- **technologies**: Array of technology names (e.g., `["python", "react"]`)
- **technology_categories**: Array of category names (e.g., `["cybersecurity", "databases"]`)
- **industries**: Array of industry names
- **job_functions**: Array of job function names
- **countries**: Array of country codes (e.g., `["US", "CA"]`)
- **employee_count**: Range filters (min/max)
- **since**: Date filter (ISO format: `"2023-01-01"`)

### Sorting

- **order_by_column**: `industry`, `employee_count`, `first_activity_time`, `last_activity_time`, `jobs_count`, `teams_count`, `people_count`, `jobs_count_growth_6mo`, `cloud_spend_estimate_millions_usd`
- **order_by_direction**: `ASC` or `DESC`

### Pagination

- **limit**: 1-200 (default: 10)
- **offset**: 0-10000 (default: 0)

## Example Execution (copy this pattern)

```bash
curl -s -X POST https://api.sumble.com/v3/organizations/find \
  -H "Authorization: Bearer ${SUMBLE_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "filters": {
      "technologies": ["python", "react"],
      "countries": ["US"]
    },
    "order_by_column": "employee_count",
    "order_by_direction": "DESC",
    "limit": 20
  }' | python3 -c "
import json, sys
data = json.load(sys.stdin)
if 'detail' in data:
    print(f'Error: {data[\"detail\"]}')
    sys.exit(1)
print(f'Found {data.get(\"total\", 0)} organizations | Credits used: {data.get(\"credits_used\", 0)} | Remaining: {data.get(\"credits_remaining\", \"?\")}')
print()
for org in data.get('organizations', []):
    techs = ', '.join([e['term'] for e in org.get('matching_entities', []) if e.get('type') == 'technologies'])
    print(f'- **{org[\"name\"]}** ({org.get(\"domain\", \"\")})')
    print(f'  Industry: {org.get(\"industry\", \"N/A\")} | Employees: {org.get(\"total_employees\", \"?\")} | HQ: {org.get(\"headquarters_country\", \"?\")}, {org.get(\"headquarters_state\", \"\")}')
    if techs:
        print(f'  Matched technologies: {techs}')
    if org.get('linkedin_organization_url'):
        print(f'  LinkedIn: {org[\"linkedin_organization_url\"]}')
    print()
"
```

## Output Instructions

- Present results as a clean markdown list or table — NEVER show raw JSON
- Include: company name, domain, industry, employee count, location, matched technologies
- Show total results and credits used/remaining
- If the user wants to dig deeper, suggest `/sumble-enrich` with a specific domain
