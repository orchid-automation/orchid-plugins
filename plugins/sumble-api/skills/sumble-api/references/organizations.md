# Organizations Endpoints

## TL;DR

Two organization endpoints: `/find` searches companies by tech stack/filters (5 credits/org/filter), `/enrich` adds tech data to a specific company (5 credits/tech found). Use find for discovery, enrich for targeted enrichment. Both support extensive filtering by technologies, industries, location, and firmographics.

## Find Organizations

Search for companies matching specific criteria including technology stack, industry, size, and location.

**Method:** POST
**Path:** `/v3/organizations/find`

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| Authorization | header (string) | Yes | Bearer token: `Bearer YOUR_API_KEY` |
| filters | body (object) | Yes | Search filters (technologies, industries, etc.) |
| order_by_column | body (string) | No | Column to sort by: industry, employee_count, first_activity_time, last_activity_time, jobs_count, teams_count, people_count, jobs_count_growth_6mo, cloud_spend_estimate_millions_usd |
| order_by_direction | body (string) | No | Sort direction: ASC or DESC |
| limit | body (integer) | No | Max results to return (1-200, default: 10) |
| offset | body (integer) | No | Number of results to skip (max: 10000, default: 0) |

### Filter Options

The `filters` object supports:
- **technologies**: Array of technology names (e.g., ["python", "react"])
- **technology_categories**: Array of category names (e.g., ["cybersecurity", "ci-cd", "crm"]). Valid values include: `cybersecurity`, `cloud-security`, `edr`, `siem`, `sast`, `dast`, `ci-cd`, `mlops`, `etl`, `olap`, `data-lake`, `vector-database`, `event-streaming`, `business-intelligence`, `crm`, `hris`, `payroll`, `ccaas`, `payment-processing`, `design`, `headless-cms`, `javascript`, `content-delivery-network`, `ipaas`. WARNING: categories expand to all technologies within them and can be expensive.
- **industries**: Array of industry names
- **job_functions**: Array of job function names
- **countries**: Array of country codes (e.g., ["US", "CA"])
- **employee_count**: Range filters (min/max)
- **since**: Date filter (ISO format: "2023-01-01")

### CURL Example

```bash
curl -X POST https://api.sumble.com/v3/organizations/find \
  -H "Authorization: Bearer $SUMBLE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "filters": {
      "technologies": ["python", "react"],
      "technology_categories": ["cybersecurity"],
      "countries": ["US"],
      "since": "2023-01-01"
    },
    "order_by_column": "employee_count",
    "order_by_direction": "DESC",
    "limit": 20
  }'
```

### Response Example

```json
{
  "id": "0199f400-4123-7eca-9082-be2c94676bfc",
  "credits_used": 100,
  "credits_remaining": 9900,
  "organizations": [
    {
      "id": 1726684,
      "name": "Sumble",
      "url": "https://sumble.com/l/org/TH2y9mGkRr1q",
      "industry": "Information",
      "total_employees": 12,
      "matching_people_count": 1,
      "matching_teams_count": 1,
      "matching_job_posts_count": 1,
      "headquarters_country": "US",
      "headquarters_state": "California",
      "domain": "sumble.com",
      "linkedin_organization_url": "https://www.linkedin.com/company/sumble",
      "matching_tags": ["digital_native"],
      "matching_entities": [
        {
          "type": "technologies",
          "term": "react",
          "job_post_count": 1,
          "people_count": 1,
          "team_count": 1
        }
      ]
    }
  ],
  "source_data_url": "https://sumble.com/l/org/...",
  "total": 1
}
```

## Enrich Organization

Enrich a specific organization with technology data. Provide a company identifier and technology filters to see which technologies appear in their job posts and team activity.

**Method:** POST
**Path:** `/v3/organizations/enrich`

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| Authorization | header (string) | Yes | Bearer token: `Bearer YOUR_API_KEY` |
| organization | body (object) | Yes | Organization identifier (domain, id, slug, or LinkedIn URL) |
| filters | body (object) | Yes | Technology filters to check for |

### Organization Identifier Options

Provide ONE of the following:
- `{"domain": "sumble.com"}` - Company domain
- `{"id": 1726684}` - Sumble organization ID
- `{"slug": "sumble"}` - Sumble organization slug
- `{"linkedin_url": "https://www.linkedin.com/company/sumble"}` - LinkedIn company URL

### CURL Example

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
      "technology_categories": ["cybersecurity"],
      "since": "2023-01-01"
    }
  }'
```

### Response Example

```json
{
  "id": "01998090-e970-732b-9d68-740f1a830902",
  "credits_used": 10,
  "credits_remaining": 69258,
  "organization": {
    "id": 1726684,
    "slug": "sumble",
    "name": "Sumble",
    "domain": "sumble.com"
  },
  "technologies_found": "Python, React",
  "technologies_count": 2,
  "source_data_url": "https://sumble.com/l/org/fa82oqKqXpW",
  "technologies": [
    {
      "name": "Python",
      "last_job_post": "2025-09-23",
      "jobs_count": 1,
      "jobs_data_url": "https://sumble.com/l/org/t5BLxGT4tLs/jobs",
      "people_count": 0,
      "people_data_url": "https://sumble.com/l/org/t5BLxGT4tLs/people",
      "teams_count": 1,
      "teams_data_url": "https://sumble.com/l/org/t5BLxGT4tLs/teams"
    },
    {
      "name": "React",
      "last_job_post": "2025-09-23",
      "jobs_count": 1,
      "jobs_data_url": "https://sumble.com/l/org/8nQuDcManoc/jobs",
      "people_count": 0,
      "people_data_url": "https://sumble.com/l/org/8nQuDcManoc/people",
      "teams_count": 1,
      "teams_data_url": "https://sumble.com/l/org/8nQuDcManoc/teams"
    }
  ]
}
```

## Use Cases

- **Competitive Intelligence**: Identify companies using similar or competing technology stacks. Use organizations/find with your competitors' tech stacks to find similar companies in the market.
- **Lead Qualification**: Enrich your CRM with technology data to qualify leads. Use organizations/enrich to check if prospects use technologies compatible with your product.
- **Market Segmentation**: Segment markets by technology adoption. Use organizations/find with technology categories to identify early adopters, laggards, or specific tech communities.
