# People Endpoint

## TL;DR

Find people at organizations with `/v3/people/find` (1 credit/person). Filter by job function, job level, location, and tech skills. Returns LinkedIn profiles, titles, and job details. Perfect for finding decision-makers, building contact lists, or talent intelligence.

## Find People at an Organization

Find people working at a specific organization, filtered by role, seniority, location, and technology skills.

**Method:** POST
**Path:** `/v3/people/find`

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| Authorization | header (string) | Yes | Bearer token: `Bearer YOUR_API_KEY` |
| organization | body (object) | Yes | Organization identifier (domain, id, slug, or LinkedIn URL) |
| filters | body (object) | Yes | Search filters (job functions, levels, etc.) |
| limit | body (integer) | No | Max people to return (1-250, default: 10) |
| offset | body (integer) | No | Number of results to skip (max: 10000, default: 0) |

### Organization Identifier Options

Provide ONE of the following:
- `{"domain": "sumble.com"}` - Company domain
- `{"id": 1726684}` - Sumble organization ID
- `{"slug": "sumble"}` - Sumble organization slug
- `{"linkedin_url": "https://www.linkedin.com/company/sumble"}` - LinkedIn company URL

### Filter Options

The `filters` object supports:
- **job_functions**: Array of job function names (e.g., ["Engineer", "Operations", "Sales"])
- **job_levels**: Array of seniority levels (e.g., ["Individual Contributor", "Manager", "Director", "VP", "C-Level"])
- **countries**: Array of country codes (e.g., ["US", "CA", "GB"])
- **technologies**: Array of technology names (filters by people working with these technologies)
- **since**: Date filter for when person started (ISO format: "2023-01-01")

**Important**: Use job function and job level values exactly as they appear in the Sumble web application. Common values include:
- **Functions**: Engineer, Software Engineer, Frontend Engineer, Backend Engineer, Data Engineer, DevOps Engineer, Sales, Marketing, Operations, Product, Design
- **Levels**: Individual Contributor, Manager, Senior Manager, Director, Senior Director, VP, Senior VP, C-Level

### CURL Example

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
      "countries": ["US"],
      "since": "2023-01-01"
    },
    "limit": 50
  }'
```

### Response Example

```json
{
  "id": "019980d2-bc85-7571-9d60-7bc1d3084249",
  "credits_used": 3,
  "credits_remaining": 69164,
  "organization": {
    "id": 1726684,
    "slug": "sumble",
    "name": "Sumble",
    "domain": "sumble.com"
  },
  "people_count": 3,
  "people_data_url": "https://sumble.com/l/org/xhXARFaWtJL/people",
  "people": [
    {
      "id": 181438858,
      "url": "https://sumble.com/l/person/MBwjfWREd8Pz",
      "linkedin_url": "https://www.linkedin.com/in/akashagajjar",
      "name": "Akash Gajjar",
      "job_title": "Software Engineer",
      "job_function": "Software Engineer",
      "job_level": "Individual Contributor",
      "location": "Gainesville, Florida, United States",
      "country": "United States",
      "country_code": "US",
      "start_date": "2024-08"
    }
  ]
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| id | string (uuid) | Unique request identifier |
| credits_used | integer | Credits consumed by this request |
| credits_remaining | integer | Remaining credits in your account |
| organization | object | Matched organization details |
| people_count | integer | Number of people returned |
| people_data_url | string | Sumble web app URL to view these results |
| people | array | Array of person objects |

**Person object fields:**
- **id**: Sumble person ID
- **url**: Sumble profile URL
- **linkedin_url**: LinkedIn profile URL (when available)
- **name**: Full name
- **job_title**: Current job title
- **job_function**: Standardized job function category
- **job_level**: Seniority level
- **location**: Full location string
- **country**: Country name
- **country_code**: ISO country code
- **start_date**: When they started this role (YYYY-MM format)

## Use Cases

- **Build Contact Lists**: Find decision-makers at target accounts for outbound sales campaigns. Filter by Director+ level and relevant job functions to identify key stakeholders.
- **Talent Intelligence**: Analyze team composition and hiring patterns at competitors or target companies. Identify which roles companies are filling and where they're located.
- **Account Mapping**: Build comprehensive org charts for strategic accounts. Identify all relevant stakeholders across different departments and seniority levels.
