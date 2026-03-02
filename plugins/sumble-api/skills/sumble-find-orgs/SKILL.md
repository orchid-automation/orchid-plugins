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

## Your Task

1. Parse the user's request to identify filter criteria (technologies, industries, countries, employee count, etc.)
2. Build the appropriate JSON request body
3. Execute the curl command against `/v3/organizations/find`
4. Present results in a clean, readable format

## Authentication

```bash
# API key must be set as environment variable
# Header: Authorization: Bearer $SUMBLE_API_KEY
```

If `$SUMBLE_API_KEY` is not set, ask the user to provide it.

## Endpoint Details

**Method:** POST
**URL:** `https://api.sumble.com/v3/organizations/find`
**Cost:** 5 credits per organization, per filter term (minimum 5)

### Filter Options

The `filters` object supports:
- **technologies**: Array of technology names (e.g., `["python", "react"]`)
- **technology_categories**: Array of category names (e.g., `["cybersecurity", "databases"]`)
- **industries**: Array of industry names
- **job_functions**: Array of job function names
- **countries**: Array of country codes (e.g., `["US", "CA"]`)
- **employee_count**: Range filters (min/max)
- **since**: Date filter (ISO format: `"2023-01-01"`)

### Sorting Options

- **order_by_column**: `industry`, `employee_count`, `first_activity_time`, `last_activity_time`, `jobs_count`, `teams_count`, `people_count`, `jobs_count_growth_6mo`, `cloud_spend_estimate_millions_usd`
- **order_by_direction**: `ASC` or `DESC`

### Pagination

- **limit**: 1-200 (default: 10)
- **offset**: 0-10000 (default: 0)

## Example Request

```bash
curl -X POST https://api.sumble.com/v3/organizations/find \
  -H "Authorization: Bearer $SUMBLE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "filters": {
      "technologies": ["python", "react"],
      "countries": ["US"]
    },
    "order_by_column": "employee_count",
    "order_by_direction": "DESC",
    "limit": 20
  }'
```

## Response Format

Each organization includes:
- `name`, `domain`, `industry`
- `total_employees`, `headquarters_country`, `headquarters_state`
- `linkedin_organization_url`
- `matching_people_count`, `matching_teams_count`, `matching_job_posts_count`
- `matching_entities` — array of matched technologies with counts

## Output Instructions

Present results as a clean table or list showing:
1. Company name and domain
2. Industry and employee count
3. Location (country/state)
4. Matched technologies and counts
5. Total results and credits used

If the user wants to dig deeper into a specific company, suggest using `/sumble-enrich` with that domain.
