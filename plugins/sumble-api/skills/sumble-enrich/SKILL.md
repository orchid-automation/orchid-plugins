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

## Your Task

1. Parse the user's request to identify the company (domain, LinkedIn URL, or name) and any technology filters
2. Build the appropriate JSON request body
3. Execute the curl command against `/v3/organizations/enrich`
4. Present results showing which technologies were found, with counts and details

## Authentication

```bash
# API key must be set as environment variable
# Header: Authorization: Bearer $SUMBLE_API_KEY
```

If `$SUMBLE_API_KEY` is not set, ask the user to provide it.

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

The `filters` object supports:
- **technologies**: Array of specific technology names to check for (e.g., `["python", "react", "postgresql"]`)
- **technology_categories**: Array of category names (e.g., `["cloud-infrastructure", "databases", "programming-languages"]`)
- **since**: Date filter (ISO format: `"2023-01-01"`)

**Tip:** If the user doesn't specify technologies, use broad technology_categories to get a comprehensive view: `["programming-languages", "databases", "cloud-infrastructure", "web-frameworks", "cybersecurity"]`

## Example Request

```bash
curl -X POST https://api.sumble.com/v3/organizations/enrich \
  -H "Authorization: Bearer $SUMBLE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "organization": {
      "domain": "stripe.com"
    },
    "filters": {
      "technologies": ["python", "react", "postgresql"],
      "technology_categories": ["cloud-infrastructure"],
      "since": "2023-01-01"
    }
  }'
```

## Response Format

Returns:
- `organization` — matched company details (id, slug, name, domain)
- `technologies_found` — comma-separated list of matched technologies
- `technologies_count` — number of technologies found
- `technologies` — array with per-technology details:
  - `name` — technology name
  - `last_job_post` — date of most recent job posting mentioning it
  - `jobs_count` — number of job postings
  - `people_count` — number of people with this skill
  - `teams_count` — number of teams using it

## Output Instructions

Present results as:
1. Company name and domain
2. Technologies found (with counts for jobs, people, teams)
3. Most recent activity dates
4. Credits used

Suggest follow-up actions:
- `/sumble-find-people` to find people at this company
- `/sumble-find-jobs` to see their job postings
