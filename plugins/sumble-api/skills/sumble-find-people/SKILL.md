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

1. **NO debugging in front of the user.** Do not echo, print, or test the API key.
2. **Do NOT show raw JSON responses.** Parse and present clean formatted output only.
3. **Make exactly ONE API call.** Do not retry with different formats.
4. **Go straight to the API call.** Do not ask clarifying questions if you can infer from context.
5. **ALWAYS use python3 for API calls.** NEVER use curl — it has shell interpolation issues with the Bearer token.

## Your Task

1. Parse the user's request to identify the target company and filter criteria
2. Build the JSON request body
3. Execute the python3 script below (using the EXACT pattern)
4. Present the parsed output — never show raw JSON

## IMPORTANT: Use python3, NOT curl

Curl has shell interpolation issues with the Sumble API key. Always use python3 with urllib:

```python
python3 -c "
import os, json, urllib.request
key = os.environ.get('SUMBLE_API_KEY', '')
if not key:
    print('Error: SUMBLE_API_KEY not set. Run: export SUMBLE_API_KEY=\"your-key\"')
    exit(1)
payload = json.dumps({
    'organization': {'domain': 'DOMAIN_HERE'},
    'filters': {FILTERS_HERE},
    'limit': 50
}).encode()
req = urllib.request.Request('https://api.sumble.com/v3/people/find', data=payload, headers={
    'Authorization': f'Bearer {key}',
    'Content-Type': 'application/json'
})
resp = json.loads(urllib.request.urlopen(req).read())
# ... parse and print
"
```

## Endpoint Details

**URL:** `https://api.sumble.com/v3/people/find`
**Cost:** 1 credit per person returned

### Organization Identifier (provide ONE)

- `{"domain": "stripe.com"}` — Company domain
- `{"id": 1726684}` — Sumble organization ID
- `{"linkedin_url": "https://www.linkedin.com/company/stripe"}` — LinkedIn company URL

### Filter Options

- **job_functions**: `Engineer`, `Software Engineer`, `Frontend Engineer`, `Backend Engineer`, `Data Engineer`, `DevOps Engineer`, `Sales`, `Marketing`, `Operations`, `Product`, `Design`
- **job_levels**: `Individual Contributor`, `Manager`, `Senior Manager`, `Director`, `Senior Director`, `VP`, `Senior VP`, `C-Level`
- **countries**: Array of country codes (e.g., `["US", "CA", "GB"]`)
- **technologies**: Array of technology names
- **since**: ISO date (e.g., `"2023-01-01"`)
- **limit**: 1-250 (default: 10)

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
        'job_functions': ['Engineer'],
        'job_levels': ['Manager', 'Director'],
        'countries': ['US']
    },
    'limit': 50
}).encode()

req = urllib.request.Request('https://api.sumble.com/v3/people/find', data=payload, headers={
    'Authorization': f'Bearer {key}',
    'Content-Type': 'application/json'
})

try:
    data = json.loads(urllib.request.urlopen(req).read())
except urllib.error.HTTPError as e:
    err = json.loads(e.read())
    print(f'Error: {err.get(\"detail\", str(e))}')
    exit(1)

print(f'Found {data.get(\"people_count\", 0)} people | Credits used: {data.get(\"credits_used\", 0)} | Remaining: {data.get(\"credits_remaining\", \"?\")}')
print()
for p in data.get('people', []):
    name = p.get('name', 'Unknown')
    title = p.get('job_title', 'N/A')
    level = p.get('job_level', '')
    loc = p.get('location', 'N/A')
    start = p.get('start_date', 'N/A')
    li = p.get('linkedin_url', '')
    print(f'- **{name}** — {title} ({level})')
    print(f'  Location: {loc} | Started: {start}')
    if li: print(f'  LinkedIn: {li}')
    print()
"
```

## Output Instructions

- Present the python3 output directly — it's already formatted as clean markdown
- If 0 results: suggest broadening the search (remove function filter, or try different levels)
- Suggest follow-up: `/sumble-enrich` or `/sumble-find-jobs`
