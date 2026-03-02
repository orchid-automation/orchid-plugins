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

1. **NO debugging in front of the user.** Do not echo, print, or test the API key.
2. **Do NOT show raw JSON responses.** Parse and present clean formatted output only.
3. **Make exactly ONE API call.** Do not retry with different formats.
4. **Go straight to the API call.** Do not ask clarifying questions if you can infer from context.
5. **ALWAYS use python3 for API calls.** NEVER use curl — it has shell interpolation issues with the Bearer token.

## Your Task

1. Parse the user's request to identify target company (if any) and filter criteria
2. Build the JSON request body — use `None` for organization in broad searches
3. Execute the python3 script below (using the EXACT pattern)
4. Present the parsed output — never show raw JSON

## Endpoint Details

**URL:** `https://api.sumble.com/v3/jobs/find`
**Cost:** 3 credits per job returned

### Organization Identifier (optional — use `None` for broad search)

- `{"domain": "stripe.com"}` — Company domain
- `{"id": 1726684}` — Sumble organization ID
- `None` — Search across ALL organizations

### Filter Options

- **technologies**: Array of technology names (e.g., `["python", "react", "kubernetes"]`)
- **technology_categories**: Array of categories (e.g., `["cloud-infrastructure", "artificial-intelligence"]`)
- **job_functions**: Array of job function names (e.g., `["Engineer", "Data Scientist"]`)
- **countries**: Array of country codes (e.g., `["US", "CA"]`)
- **since**: Date filter (ISO format: `"2024-01-01"`)
- **limit**: 1-100 (default: 10)

## Complete Example (COPY THIS PATTERN EXACTLY)

```bash
python3 -c "
import os, json, urllib.request

key = os.environ.get('SUMBLE_API_KEY', '')
if not key:
    print('Error: SUMBLE_API_KEY not set. Run: export SUMBLE_API_KEY=\"your-key\"')
    exit(1)

payload = json.dumps({
    'organization': {'domain': 'stripe.com'},
    'filters': {
        'technologies': ['python', 'react'],
        'job_functions': ['Engineer'],
        'since': '2024-01-01'
    },
    'limit': 25
}).encode()

req = urllib.request.Request('https://api.sumble.com/v3/jobs/find', data=payload, headers={
    'Authorization': f'Bearer {key}',
    'Content-Type': 'application/json'
})

try:
    data = json.loads(urllib.request.urlopen(req).read())
except urllib.error.HTTPError as e:
    err = json.loads(e.read())
    print(f'Error: {err.get(\"detail\", str(e))}')
    exit(1)

print(f'Found {data.get(\"total\", 0)} jobs | Credits used: {data.get(\"credits_used\", 0)} | Remaining: {data.get(\"credits_remaining\", \"?\")}')
print()
for j in data.get('jobs', []):
    title = j.get('job_title', 'N/A')
    org = j.get('organization_name', '')
    domain = j.get('organization_domain', '')
    loc = j.get('location', 'N/A')
    techs = j.get('matched_technologies', 'N/A')
    posted = j.get('datetime_pulled', 'N/A')[:10]
    url = j.get('url', '')
    print(f'- **{title}** at {org} ({domain})')
    print(f'  Location: {loc} | Technologies: {techs} | Posted: {posted}')
    if url: print(f'  Details: {url}')
    print()
"
```

## Output Instructions

- Present the python3 output directly — it's already formatted as clean markdown
- For trend analysis, summarize: most common technologies, geographic distribution
- Suggest follow-up: `/sumble-enrich` or `/sumble-find-people`
