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

1. **NO debugging in front of the user.** If a request fails, try ONE alternative silently. If it still fails, report the error cleanly.
2. **Do NOT echo, print, or test the API key.** Assume it's set.
3. **Do NOT show raw JSON responses.** Parse them and present clean formatted output only.
4. **Make exactly ONE curl call.** Do not retry with different auth formats or headers.
5. **Go straight to the API call.** Do not ask clarifying questions if you can infer from context.

## Your Task

1. Parse the user's request to identify the company (domain, LinkedIn URL, or name) and any technology filters
2. Build the JSON request body
3. Execute the curl command (using the EXACT format below)
4. Parse the JSON response and present clean formatted output

## Authentication — USE THIS EXACT FORMAT

```bash
curl -s -X POST https://api.sumble.com/v3/organizations/enrich \
  -H "Authorization: Bearer ${SUMBLE_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{ ... }'
```

**IMPORTANT**: Always use `${SUMBLE_API_KEY}` with curly braces. Do NOT test if the key is set — just use it.

## Endpoint Details

**Method:** POST
**URL:** `https://api.sumble.com/v3/organizations/enrich`
**Cost:** 5 credits per technology found

### Organization Identifier (provide ONE)

- `{"domain": "stripe.com"}` — Company domain
- `{"id": 1726684}` — Sumble organization ID
- `{"slug": "stripe"}` — Sumble organization slug
- `{"linkedin_url": "https://www.linkedin.com/company/stripe"}` — LinkedIn company URL

### Filter Options

- **technologies**: Array of specific technology names (e.g., `["python", "react", "postgresql"]`)
- **technology_categories**: Array of category names (e.g., `["cloud-infrastructure", "databases", "programming-languages"]`)
- **since**: Date filter (ISO format: `"2023-01-01"`)

**Default behavior**: If the user doesn't specify technologies, use broad categories:
`["programming-languages", "databases", "cloud-infrastructure", "web-frameworks", "cybersecurity"]`

## Example Execution (copy this pattern)

```bash
curl -s -X POST https://api.sumble.com/v3/organizations/enrich \
  -H "Authorization: Bearer ${SUMBLE_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "organization": {"domain": "stripe.com"},
    "filters": {
      "technologies": ["python", "react", "postgresql"],
      "technology_categories": ["cloud-infrastructure"]
    }
  }' | python3 -c "
import json, sys
data = json.load(sys.stdin)
if 'detail' in data:
    print(f'Error: {data[\"detail\"]}')
    sys.exit(1)
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

- Present results as a clean markdown list — NEVER show raw JSON
- Include: technology name, job count, people count, team count, last activity
- Show total technologies found and credits used/remaining
- Suggest follow-up: `/sumble-find-people` or `/sumble-find-jobs`
