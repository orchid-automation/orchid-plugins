---
name: sumble-find-jobs
description: Search job postings by company, technologies, job functions, and location using Sumble's sales intelligence database. Returns structured job data with extracted tech stacks. Use for hiring trend analysis, tech stack discovery, competitive intelligence, market sizing, or identifying companies scaling specific teams.
user-invocable: true
disable-model-invocation: true
argument-hint: "[domain or criteria, e.g. 'stripe.com python' or 'AI engineers US']"
allowed-tools: Bash(python3 *), Read
---

# Find Jobs with Sumble

**User's request:** $ARGUMENTS

## Script path

!`find ~/.claude/plugins -path "*/sumble-api/scripts/sumble_api.py" 2>/dev/null | head -1`

## Execution rules

- Run exactly **one** python3 command. No curl. No API key testing. No retries.
- For large queries (limit > 25), add `--save` to write results to `.sumble/` and keep context clean.
- The script handles auth, retries, errors, domain normalization, and output formatting.
- Present the formatted output directly to the user. Do not reformat or wrap in code blocks.

**Single company:**
```bash
python3 "<script path from above>" "jobs/find" '{
  "organization": {"domain": "stripe.com"},
  "filters": {"technologies": ["python"], "job_functions": ["Engineer"]},
  "limit": 25
}'
```

**Broad search (no specific company):**
```bash
python3 "<script path from above>" "jobs/find" '{
  "organization": null,
  "filters": {"technology_categories": ["mlops"], "countries": ["US"]},
  "limit": 25
}'
```

## Available filters

| Filter | Type | Example |
|--------|------|---------|
| technologies | string[] | `["python", "react", "kubernetes"]` |
| technology_categories | string[] | `["cybersecurity", "ci-cd", "mlops", "etl"]` |
| job_functions | string[] | `["Engineer", "Data Scientist"]` |
| countries | string[] | `["US", "CA"]` |
| since | string | `"2024-01-01"` |

**Organization**: domain, id, slug, linkedin_url, or `null` (all companies)
**Pagination**: `limit` (1-100), `offset` (0-10000)
**Cost**: 3 credits per job

For API details, see [common.md](references/common.md). For troubleshooting, see [troubleshooting.md](../sumble-api/references/troubleshooting.md).
