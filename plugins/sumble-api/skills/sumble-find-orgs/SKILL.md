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

1. **NO debugging in front of the user.** Do not echo, print, or test the API key.
2. **Do NOT show raw JSON responses.** Parse and present clean formatted output only.
3. **Make exactly ONE API call.** Do not retry with different formats.
4. **Go straight to the API call.** Do not ask clarifying questions if you can infer from context.
5. **ALWAYS use python3 for API calls.** NEVER use curl — it has shell interpolation issues with the Bearer token.

## Your Task

1. Parse the user's request to identify filter criteria (technologies, industries, countries, etc.)
2. Build the JSON request body
3. Execute the python3 script below (using the EXACT pattern)
4. Present the parsed output — never show raw JSON

## Endpoint Details

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

### Pagination: limit 1-200, offset 0-10000

## Complete Example (COPY THIS PATTERN EXACTLY)

```bash
python3 -c "
import os, json, urllib.request

key = os.environ.get('SUMBLE_API_KEY', '')
if not key:
    print('Error: SUMBLE_API_KEY not set. Run: export SUMBLE_API_KEY=\"your-key\"')
    exit(1)

payload = json.dumps({
    'filters': {
        'technologies': ['python', 'react'],
        'countries': ['US']
    },
    'order_by_column': 'employee_count',
    'order_by_direction': 'DESC',
    'limit': 20
}).encode()

req = urllib.request.Request('https://api.sumble.com/v3/organizations/find', data=payload, headers={
    'Authorization': f'Bearer {key}',
    'Content-Type': 'application/json'
})

try:
    data = json.loads(urllib.request.urlopen(req).read())
except urllib.error.HTTPError as e:
    err = json.loads(e.read())
    print(f'Error: {err.get(\"detail\", str(e))}')
    exit(1)

print(f'Found {data.get(\"total\", 0)} organizations | Credits used: {data.get(\"credits_used\", 0)} | Remaining: {data.get(\"credits_remaining\", \"?\")}')
print()
for org in data.get('organizations', []):
    name = org.get('name', 'Unknown')
    domain = org.get('domain', '')
    industry = org.get('industry', 'N/A')
    emp = org.get('total_employees', '?')
    hq = f'{org.get(\"headquarters_country\", \"?\")}, {org.get(\"headquarters_state\", \"\")}'.strip(', ')
    li = org.get('linkedin_organization_url', '')
    techs = ', '.join([e['term'] for e in org.get('matching_entities', []) if e.get('type') == 'technologies'])
    print(f'- **{name}** ({domain})')
    print(f'  Industry: {industry} | Employees: {emp} | HQ: {hq}')
    if techs: print(f'  Matched: {techs}')
    if li: print(f'  LinkedIn: {li}')
    print()
"
```

## Output Instructions

- Present the python3 output directly — it's already formatted as clean markdown
- To dig deeper into a specific company, suggest `/sumble-enrich`
