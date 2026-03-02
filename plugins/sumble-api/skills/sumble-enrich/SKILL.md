---
name: sumble-enrich
description: Enrich a company profile with its technology stack — programming languages, frameworks, databases, cloud infrastructure, and tools found in job postings and team activity. Use for understanding company tech choices, competitive analysis, CRM enrichment, or sales intelligence.
user-invocable: true
disable-model-invocation: true
argument-hint: "[domain, e.g. 'stripe.com' or 'stripe.com python react']"
allowed-tools: Bash(python3 *), Read
---

# Enrich Organization with Sumble

**User's request:** $ARGUMENTS

## Script path

!`find ~/.claude/plugins -path "*/sumble-api/scripts/sumble_api.py" 2>/dev/null | head -1`

## Execution

Run **one** command. Do not use curl. Do not test the API key.

```bash
python3 "<script path from above>" "organizations/enrich" '{
  "organization": {"domain": "stripe.com"},
  "filters": {"technology_categories": ["programming-languages", "databases", "cloud-infrastructure", "web-frameworks"]}
}'
```

The script handles auth, retries, errors, domain normalization, and output formatting.

## Default behavior

If user doesn't specify technologies, use broad categories:
`["programming-languages", "databases", "cloud-infrastructure", "web-frameworks", "cybersecurity"]`

## Available filters

| Filter | Type | Example |
|--------|------|---------|
| technologies | string[] | `["python", "react", "postgresql"]` |
| technology_categories | string[] | `["programming-languages", "databases"]` |
| since | string | `"2023-01-01"` |

**Organization ID**: domain (preferred), id, slug, or linkedin_url
**Cost**: 5 credits per technology found

For API details, see [common.md](references/common.md). For troubleshooting, see [troubleshooting.md](../sumble-api/references/troubleshooting.md).
