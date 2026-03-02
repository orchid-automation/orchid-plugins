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

## Your Task

1. Parse the user's request to identify the target company and filter criteria (job functions, levels, countries, technologies)
2. Build the appropriate JSON request body
3. Execute the curl command against `/v3/people/find`
4. Present results in a clean, readable format with LinkedIn links

## Authentication

```bash
# API key must be set as environment variable
# Header: Authorization: Bearer $SUMBLE_API_KEY
```

If `$SUMBLE_API_KEY` is not set, ask the user to provide it.

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

- **job_functions**: Array of job function names
  - Common values: `Engineer`, `Software Engineer`, `Frontend Engineer`, `Backend Engineer`, `Data Engineer`, `DevOps Engineer`, `Sales`, `Marketing`, `Operations`, `Product`, `Design`
- **job_levels**: Array of seniority levels
  - Values: `Individual Contributor`, `Manager`, `Senior Manager`, `Director`, `Senior Director`, `VP`, `Senior VP`, `C-Level`
- **countries**: Array of country codes (e.g., `["US", "CA", "GB"]`)
- **technologies**: Array of technology names (filters by people working with these technologies)
- **since**: Date filter for when person started (ISO format: `"2023-01-01"`)

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
| "product managers" | `["Product"]` | `["Manager", "Director"]` |
| "C-suite" | — | `["C-Level"]` |

## Example Request

```bash
curl -X POST https://api.sumble.com/v3/people/find \
  -H "Authorization: Bearer $SUMBLE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "organization": {
      "domain": "stripe.com"
    },
    "filters": {
      "job_functions": ["Engineer", "Operations"],
      "job_levels": ["Manager", "Director"],
      "countries": ["US"]
    },
    "limit": 50
  }'
```

## Response Format

Each person includes:
- `name` — Full name
- `linkedin_url` — LinkedIn profile URL
- `job_title` — Current job title
- `job_function` — Standardized function
- `job_level` — Seniority level
- `location` — Full location string
- `country_code` — ISO country code
- `start_date` — When they started (YYYY-MM format)

## Output Instructions

Present results as a clean table:
1. Name (with LinkedIn link)
2. Job title and level
3. Location
4. Start date
5. Total people found and credits used

Suggest follow-up actions:
- `/sumble-enrich` to check what technologies this company uses
- `/sumble-find-jobs` to see what they're hiring for
