# Jobs Endpoint

## TL;DR

Search job postings with `/v3/jobs/find` (3 credits/job). Filter by organization, technologies, job functions, and location. Returns structured job data with extracted tech stacks, teams, and descriptions. Use for hiring trend analysis, tech stack discovery, and competitive intelligence.

## Find Job Postings

Search for job postings by organization and filters. Jobs can be scoped to a specific organization or searched broadly across all companies.

**Method:** POST
**Path:** `/v3/jobs/find`

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| Authorization | header (string) | Yes | Bearer token: `Bearer YOUR_API_KEY` |
| organization | body (object) | No | Organization identifier (domain, id, slug, or LinkedIn URL). Null to search all organizations. |
| filters | body (object) | Yes | Search filters (technologies, job functions, etc.) |
| limit | body (integer) | No | Max jobs to return (1-100, default: 10) |
| offset | body (integer) | No | Number of results to skip (max: 10000, default: 0) |

### Organization Identifier Options

Provide ONE of the following (or null to search all organizations):
- `{"domain": "sumble.com"}` - Company domain
- `{"id": 1726684}` - Sumble organization ID
- `{"slug": "sumble"}` - Sumble organization slug
- `{"linkedin_url": "https://www.linkedin.com/company/sumble"}` - LinkedIn company URL

### Filter Options

The `filters` object supports:
- **technologies**: Array of technology names (e.g., ["python", "react", "kubernetes"])
- **technology_categories**: Array of category names (e.g., ["cybersecurity", "ci-cd", "mlops"]). See organizations.md for the full list of valid category slugs.
- **job_functions**: Array of job function names (e.g., ["Engineer", "Data Scientist"])
- **countries**: Array of country codes (e.g., ["US", "CA"])
- **since**: Date filter for when job was posted (ISO format: "2023-01-01")

### CURL Example - Single Organization

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

### CURL Example - Search All Organizations

```bash
curl -X POST https://api.sumble.com/v3/jobs/find \
  -H "Authorization: Bearer $SUMBLE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "organization": null,
    "filters": {
      "technology_categories": ["mlops"],
      "job_functions": ["Machine Learning Engineer"],
      "countries": ["US"]
    },
    "limit": 50
  }'
```

### Response Example

```json
{
  "id": "019c9529-9d27-7e16-b721-76d18c339e3e",
  "credits_used": 6,
  "credits_remaining": 9994,
  "jobs": [
    {
      "id": 95107725,
      "organization_id": 1726684,
      "organization_name": "Sumble",
      "organization_domain": "sumble.com",
      "job_title": "gtm engineer",
      "datetime_pulled": "2026-02-20T12:20:03.687777Z",
      "location": "United States",
      "teams": "",
      "matched_technologies": "Python",
      "description": "Sumble helps go-to-market teams win...",
      "url": "https://sumble.com/l/job/fdYksIHVnJ"
    },
    {
      "id": 85817801,
      "organization_id": 1726684,
      "organization_name": "Sumble",
      "organization_domain": "sumble.com",
      "job_title": "frontend engineer",
      "datetime_pulled": "2025-09-23T06:16:05.231145Z",
      "primary_job_function": "Frontend Engineer",
      "location": "United States",
      "teams": "",
      "matched_technologies": "Python, React",
      "description": "Sumble is building a knowledge graph...",
      "url": "https://sumble.com/l/job/M6KG6K3aQ3"
    }
  ],
  "source_data_url": "https://sumble.com/l/org/MIkfQDbGSbraK/jobs",
  "total": 2
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| id | string (uuid) | Unique request identifier |
| credits_used | integer | Credits consumed by this request |
| credits_remaining | integer | Remaining credits in your account |
| jobs | array | Array of job objects |
| source_data_url | string | Sumble web app URL to view results |
| total | integer | Total number of matching jobs |

**Job object fields:**
- **id**: Sumble job ID
- **organization_id**: Sumble organization ID
- **organization_name**: Company name
- **organization_domain**: Company domain
- **job_title**: Job title from posting
- **primary_job_function**: Standardized job function
- **datetime_pulled**: When Sumble scraped this job
- **location**: Job location
- **teams**: Team names extracted from posting
- **matched_technologies**: Technologies found that match your filters
- **description**: Job description text
- **url**: Sumble job detail page URL

## Use Cases

- **Technology Adoption Trends**: Analyze which technologies companies are hiring for to identify emerging trends. Search jobs across all organizations filtered by specific technologies or categories.
- **Competitive Intelligence**: Monitor competitor hiring activity to understand their strategic priorities. Track which roles and technologies they're investing in.
- **Tech Stack Discovery**: Discover what technologies a target company uses by analyzing their job postings. Job descriptions often reveal tech stacks more completely than company websites.
