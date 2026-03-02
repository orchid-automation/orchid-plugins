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

## Your Task

1. Parse the user's request to identify target company (if any) and filter criteria
2. Build the appropriate JSON request body — set `organization` to `null` for broad searches
3. Execute the curl command against `/v3/jobs/find`
4. Present results showing job titles, technologies, and hiring patterns

## Authentication

```bash
# API key must be set as environment variable
# Header: Authorization: Bearer $SUMBLE_API_KEY
```

If `$SUMBLE_API_KEY` is not set, ask the user to provide it.

## Endpoint Details

**Method:** POST
**URL:** `https://api.sumble.com/v3/jobs/find`
**Cost:** 3 credits per job returned

### Organization Identifier (optional — set to `null` for broad search)

- `{"domain": "stripe.com"}` — Company domain
- `{"id": 1726684}` — Sumble organization ID
- `{"slug": "stripe"}` — Sumble organization slug
- `{"linkedin_url": "https://www.linkedin.com/company/stripe"}` — LinkedIn company URL
- `null` — Search across ALL organizations

### Filter Options

- **technologies**: Array of technology names (e.g., `["python", "react", "kubernetes"]`)
- **technology_categories**: Array of category names (e.g., `["cloud-infrastructure", "databases", "artificial-intelligence"]`)
- **job_functions**: Array of job function names (e.g., `["Engineer", "Data Scientist", "Machine Learning Engineer"]`)
- **countries**: Array of country codes (e.g., `["US", "CA"]`)
- **since**: Date filter for when job was posted (ISO format: `"2024-01-01"`)

### Pagination

- **limit**: 1-100 (default: 10)
- **offset**: 0-10000 (default: 0)

## Example Request — Single Company

```bash
curl -X POST https://api.sumble.com/v3/jobs/find \
  -H "Authorization: Bearer $SUMBLE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "organization": {
      "domain": "stripe.com"
    },
    "filters": {
      "technologies": ["python", "react"],
      "job_functions": ["Engineer"],
      "since": "2024-01-01"
    },
    "limit": 25
  }'
```

## Example Request — Broad Search (All Companies)

```bash
curl -X POST https://api.sumble.com/v3/jobs/find \
  -H "Authorization: Bearer $SUMBLE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "organization": null,
    "filters": {
      "technology_categories": ["artificial-intelligence"],
      "job_functions": ["Machine Learning Engineer"],
      "countries": ["US"]
    },
    "limit": 50
  }'
```

## Response Format

Each job includes:
- `job_title` — Job title from posting
- `primary_job_function` — Standardized job function
- `organization_name` / `organization_domain` — Company info
- `matched_technologies` — Technologies from filters found in this posting
- `location` — Job location
- `teams` — Team names extracted from posting
- `datetime_pulled` — When Sumble scraped this job
- `description` — Job description text
- `url` — Sumble job detail page URL

## Output Instructions

Present results as:
1. Job title and company
2. Matched technologies
3. Location
4. Date posted
5. Total results and credits used

For trend analysis, summarize:
- Most common technologies across postings
- Geographic distribution
- Team/function patterns

Suggest follow-up actions:
- `/sumble-enrich` to check the company's full tech stack
- `/sumble-find-people` to find people at hiring companies
