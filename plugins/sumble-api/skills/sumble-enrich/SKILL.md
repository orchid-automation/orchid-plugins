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

## Execution rules

- Run exactly **one** python3 command. No curl. No API key testing. No retries.
- For large queries, add `--save` to write results to `.sumble/` and keep context clean.
- The script handles auth, retries, errors, domain normalization, and output formatting.
- Present the formatted output directly to the user. Do not reformat or wrap in code blocks.

```bash
python3 "<script path from above>" "organizations/enrich" '{
  "organization": {"domain": "stripe.com"},
  "filters": {"technologies": ["python", "react", "typescript", "java", "go", "ruby", "postgresql", "mysql", "redis", "mongodb", "elasticsearch", "kafka", "aws", "gcp", "azure", "docker", "kubernetes", "terraform"]}
}'
```

## Default behavior

If user doesn't specify technologies, use a broad set of individual technology slugs:
`["python", "react", "typescript", "java", "go", "ruby", "postgresql", "mysql", "redis", "mongodb", "elasticsearch", "kafka", "aws", "gcp", "azure", "docker", "kubernetes", "terraform"]`

Prefer `technologies` over `technology_categories` — individual slugs are predictable (5 credits each) and won't surprise with hidden expansions.

## Available filters

| Filter | Type | Example |
|--------|------|---------|
| technologies | string[] (preferred) | `["python", "react", "postgresql"]` |
| technology_categories | string[] | `["cybersecurity", "ci-cd", "crm", "etl"]` |
| since | string | `"2023-01-01"` |

**Valid technology_categories** (partial list): `cybersecurity`, `cloud-security`, `edr`, `siem`, `sast`, `dast`, `ci-cd`, `mlops`, `etl`, `olap`, `data-lake`, `vector-database`, `event-streaming`, `business-intelligence`, `crm`, `hris`, `payroll`, `ccaas`, `payment-processing`, `design`, `headless-cms`, `javascript`, `content-delivery-network`, `ipaas`

**WARNING**: Categories expand to ALL technologies within them. A single category can contain 50+ technologies at 5 credits each. Use individual `technologies` for predictable costs.

**Organization ID**: domain (preferred), id, slug, or linkedin_url
**Cost**: 5 credits per technology found

For API details, see [common.md](references/common.md). For troubleshooting, see [troubleshooting.md](../sumble-api/references/troubleshooting.md).
