---
name: sumble-api
description: Search companies by technology stack, enrich organization data, find people by role/seniority, and discover job postings with extracted technologies. Use for lead generation, CRM enrichment, market research, and competitor analysis. Requires API key with credit-based usage.
user-invocable: false
---

## How to Use This Skill

This skill enables Claude to access Sumble's sales intelligence data programmatically. Use it to find organizations by their tech stack, enrich company data with technology insights, identify people at target companies, and discover relevant job postings - all essential for go-to-market research, lead generation, and competitive analysis.

## Decision Tree

1. **User wants to find companies using specific technologies or matching criteria** → Use `/v3/organizations/find`
2. **User wants to check what technologies a specific company uses** → Use `/v3/organizations/enrich`
3. **User wants to find people at a company (by role, seniority, location)** → Use `/v3/people/find`
4. **User wants to find job postings (to understand hiring trends or tech stack)** → Use `/v3/jobs/find`
5. **User wants comprehensive data about a company** → Start with `/v3/organizations/enrich`, then use `/v3/people/find` and `/v3/jobs/find` for deeper insights

## When to Use

- **Lead generation**: Find companies matching specific technology or firmographic criteria
- **CRM enrichment**: Add technology stack data to existing company records
- **Competitor research**: Identify companies in similar markets or using similar technologies
- **Talent intelligence**: Find people with specific roles or skills at target organizations
- **Market analysis**: Analyze hiring trends, technology adoption, and team structures
- **Account-based marketing**: Build detailed profiles of target accounts with tech stack and personnel data

## Quick Examples

**Find companies using Python and React:**
```bash
curl -X POST https://api.sumble.com/v3/organizations/find \
  -H "Authorization: Bearer $SUMBLE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "filters": {
      "technologies": ["python", "react"]
    },
    "limit": 10
  }'
```

**Check what technologies Sumble uses:**
```bash
curl -X POST https://api.sumble.com/v3/organizations/enrich \
  -H "Authorization: Bearer $SUMBLE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "organization": {
      "domain": "sumble.com"
    },
    "filters": {
      "technologies": ["python", "react", "postgresql"]
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
      "domain": "sumble.com"
    },
    "filters": {
      "job_functions": ["Engineer"],
      "job_levels": ["Individual Contributor"]
    },
    "limit": 20
  }'
```

## Common Workflows

### Build a target account list for cybersecurity product
1. Use `/v3/organizations/find` with technology_categories filter for "cybersecurity"
2. Filter by employee count and industry to narrow results
3. Use `/v3/people/find` to identify security decision-makers at top matches
4. Export results to CRM or outreach tool

### Enrich CRM with technology intelligence
1. For each company in your CRM, use `/v3/organizations/enrich` with their domain
2. Specify technologies relevant to your product in the filters
3. Update CRM records with matched technologies and counts
4. Prioritize outreach based on technology fit score

### Competitive hiring analysis
1. Use `/v3/jobs/find` for competitor domains
2. Filter by technology categories and job functions of interest
3. Analyze which technologies competitors are hiring for
4. Identify market trends and talent gaps

## Available References

- **references/quickstart.md**: Step-by-step guide to making your first API call and common workflows for lead generation and enrichment
- **references/common.md**: Authentication setup, base URL, error codes, rate limits, credits system, and troubleshooting guidance
- **references/organizations.md**: Complete documentation for finding and enriching organization data, including all filter options and response structures
- **references/people.md**: Documentation for finding people at organizations with job function, level, and location filters
- **references/jobs.md**: Documentation for searching job postings with technology and team filters

## Authentication

All API requests require a Bearer token in the Authorization header:
- Environment variable: `SUMBLE_API_KEY`
- Header format: `Authorization: Bearer $SUMBLE_API_KEY`
- Generate keys at: https://sumble.com/account/api-keys

**Important**: The API uses a credit-based system. Check your remaining credits in API responses and monitor usage to avoid 402 errors.
