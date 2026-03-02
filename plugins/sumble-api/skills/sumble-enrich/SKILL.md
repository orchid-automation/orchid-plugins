---
name: sumble-enrich
description: Enrich a company profile with its technology stack — programming languages, frameworks, databases, cloud infrastructure, and tools found in job postings and team activity. Use for understanding company tech choices, competitive analysis, CRM enrichment, or sales intelligence.
user-invocable: true
disable-model-invocation: true
argument-hint: "[domain, e.g. 'stripe.com' or 'stripe.com python react']"
allowed-tools: Bash, Read
---

# Enrich Organization with Sumble

**User's request:** $ARGUMENTS

## Execution

1. Extract domain from request (the helper normalizes "stripe", "stripe.com", "https://www.stripe.com" automatically)
2. If user specifies technologies, use those as filters. Otherwise use broad categories.
3. Run the shared helper — **ONE call, no retries, no debugging**:

```bash
python3 "PLUGIN_DIR/scripts/sumble_api.py" "organizations/enrich" '{"organization": {"domain": "stripe.com"}, "filters": {"technology_categories": ["programming-languages", "databases", "cloud-infrastructure", "web-frameworks"]}}'
```

Replace `PLUGIN_DIR` with the absolute path to the `sumble-api` plugin directory.

**CRITICAL**: Do NOT use curl. Do NOT echo/test the API key. Do NOT show raw JSON. The helper handles auth, retries, errors, and formatting automatically.

## Filters Reference

| Filter | Type | Example |
|--------|------|---------|
| technologies | string[] | `["python", "react", "postgresql"]` |
| technology_categories | string[] | `["programming-languages", "databases"]` |
| since | string | `"2023-01-01"` |

**Organization ID**: domain (preferred), id, slug, or linkedin_url
**Cost**: 5 credits per technology found
**Default categories** (when user doesn't specify): `programming-languages`, `databases`, `cloud-infrastructure`, `web-frameworks`, `cybersecurity`
