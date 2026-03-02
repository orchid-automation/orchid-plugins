---
name: sumble-enrich
description: Enrich a specific company with technology intelligence using Sumble API. Provide a domain to see which technologies appear in their job posts and team activity.
user-invocable: true
argument-hint: "[domain, e.g. 'stripe.com' or 'stripe.com python react postgresql']"
allowed-tools: Bash, Read
---

# Enrich Organization with Sumble

Enrich a specific company with technology data using the Sumble API.

**User's request:** $ARGUMENTS

---

## CRITICAL: Execution Rules

1. **NO debugging in front of the user.** Do not echo, print, or test the API key.
2. **Do NOT show raw JSON responses.** Parse and present clean formatted output only.
3. **Make exactly ONE API call.** Do not retry with different formats.
4. **Go straight to the API call.** Do not ask clarifying questions if you can infer from context.
5. **ALWAYS use python3 for API calls.** NEVER use curl — it has shell interpolation issues with the Bearer token.

## Your Task

1. Parse the user's request to identify the company and any technology filters
2. Build the JSON request body
3. Execute the python3 script below (using the EXACT pattern)
4. Present the parsed output — never show raw JSON

## Endpoint Details

**URL:** `https://api.sumble.com/v3/organizations/enrich`
**Cost:** 5 credits per technology found

### Organization Identifier (provide ONE)

- `{"domain": "stripe.com"}` — Company domain
- `{"id": 1726684}` — Sumble organization ID
- `{"linkedin_url": "https://www.linkedin.com/company/stripe"}` — LinkedIn company URL

### Filter Options

- **technologies**: Array of specific names (e.g., `["python", "react", "postgresql"]`)
- **technology_categories**: Array of categories (e.g., `["cloud-infrastructure", "databases", "programming-languages"]`)
- **since**: Date filter (ISO format)

**Default**: If user doesn't specify technologies, use broad categories:
`["programming-languages", "databases", "cloud-infrastructure", "web-frameworks", "cybersecurity"]`

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
        'technologies': ['python', 'react', 'postgresql'],
        'technology_categories': ['cloud-infrastructure']
    }
}).encode()

req = urllib.request.Request('https://api.sumble.com/v3/organizations/enrich', data=payload, headers={
    'Authorization': f'Bearer {key}',
    'Content-Type': 'application/json'
})

try:
    data = json.loads(urllib.request.urlopen(req).read())
except urllib.error.HTTPError as e:
    err = json.loads(e.read())
    print(f'Error: {err.get(\"detail\", str(e))}')
    exit(1)

org = data.get('organization', {})
print(f'# {org.get(\"name\", \"Unknown\")} ({org.get(\"domain\", \"\")})')
print(f'Technologies found: {data.get(\"technologies_count\", 0)} | Credits used: {data.get(\"credits_used\", 0)} | Remaining: {data.get(\"credits_remaining\", \"?\")}')
print()
for t in data.get('technologies', []):
    print(f'- **{t[\"name\"]}** — Jobs: {t.get(\"jobs_count\", 0)} | People: {t.get(\"people_count\", 0)} | Teams: {t.get(\"teams_count\", 0)} | Last post: {t.get(\"last_job_post\", \"N/A\")}')
print()
"
```

## Output Instructions

- Present the python3 output directly — it's already formatted as clean markdown
- Suggest follow-up: `/sumble-find-people` or `/sumble-find-jobs`
