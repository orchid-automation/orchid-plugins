# Quickstart

## TL;DR

Get started with the Sumble API in three steps: generate an API key, make your first request to find organizations, and explore additional endpoints for people and jobs data. All endpoints use Bearer authentication and return JSON responses.

## Getting Started with Sumble API

The Sumble API enables programmatic access to sales intelligence data including company technology stacks, employee information, and job postings. This guide will walk you through your first API call and common workflows.

### Step 1: Generate Your API Key

1. Navigate to https://sumble.com/account/api-keys
2. Click "Create New API Key"
3. Give your key a descriptive name
4. Copy the key immediately - it won't be shown again
5. Store it securely (e.g., in environment variables)

```bash
export SUMBLE_API_KEY="your_api_key_here"
```

### Step 2: Make Your First Request

Let's find companies using Python and React:

```bash
curl -X POST https://api.sumble.com/v3/organizations/find \
  -H "Authorization: Bearer $SUMBLE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "filters": {
      "technologies": ["python", "react"]
    },
    "limit": 5
  }'
```

**Response:**
```json
{
  "id": "0199f400-4123-7eca-9082-be2c94676bfc",
  "credits_used": 25,
  "credits_remaining": 9975,
  "organizations": [
    {
      "id": 1726684,
      "name": "Sumble",
      "domain": "sumble.com",
      "industry": "Information",
      "total_employees": 12,
      "matching_people_count": 1,
      "matching_teams_count": 1,
      "headquarters_country": "US"
    }
  ],
  "total": 1
}
```

### Step 3: Explore Additional Endpoints

**Check what technologies a specific company uses:**
```bash
curl -X POST https://api.sumble.com/v3/organizations/enrich \
  -H "Authorization: Bearer $SUMBLE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "organization": {
      "domain": "stripe.com"
    },
    "filters": {
      "technology_categories": ["programming-languages", "databases"]
    }
  }'
```

**Find engineers at a company:**
```bash
curl -X POST https://api.sumble.com/v3/people/find \
  -H "Authorization: Bearer $SUMBLE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "organization": {
      "domain": "stripe.com"
    },
    "filters": {
      "job_functions": ["Engineer"],
      "job_levels": ["Manager", "Director"]
    },
    "limit": 10
  }'
```

## Use Cases

**Lead Generation**: Find companies matching your ideal customer profile based on technology stack, industry, size, and location. Use filters to narrow down to companies actively using complementary or competing technologies.

**CRM Enrichment**: Enhance existing company records with up-to-date technology intelligence. Identify which technologies prospects are using to personalize outreach and qualify leads more effectively.

**Market Research**: Analyze technology adoption trends across industries. Discover which companies are hiring for specific roles or technologies to identify market opportunities and competitive dynamics.

**Account-Based Marketing**: Build comprehensive profiles of target accounts including technology stack, key personnel, and hiring trends. Use this intelligence to craft highly targeted campaigns and prioritize high-value accounts.
