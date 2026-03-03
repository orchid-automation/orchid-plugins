---
name: sumble-research
description: Run a full company research workflow — enrich tech stack, find key people, and analyze hiring trends in one command. Returns a comprehensive intelligence brief. Use for deep-dive account research, meeting prep, competitive analysis, or building a complete company profile.
user-invocable: true
disable-model-invocation: true
argument-hint: "[domain, e.g. 'stripe.com' or 'datadog.com engineering leaders']"
allowed-tools: Bash(python3 *), Read
---

# Company Research with Sumble

**User's request:** $ARGUMENTS

## Script path

!`find ~/.claude/plugins -path "*/sumble-api/scripts/sumble_api.py" 2>/dev/null | head -1`

## Workflow

Run these **three** commands sequentially using the script path above. Save all results to `.sumble/` with `--save` to keep context clean.

### Step 1: Enrich tech stack

```bash
python3 "<script path>" "organizations/enrich" '{
  "organization": {"domain": "DOMAIN"},
  "filters": {"technologies": ["python", "react", "typescript", "java", "go", "ruby", "postgresql", "mysql", "redis", "mongodb", "elasticsearch", "kafka", "aws", "gcp", "azure", "docker", "kubernetes", "terraform"]}
}' --save
```

### Step 2: Find key people (leadership + engineering managers)

```bash
python3 "<script path>" "people/find" '{
  "organization": {"domain": "DOMAIN"},
  "filters": {"job_levels": ["Director", "VP", "Senior VP", "C-Level"]},
  "limit": 25
}' --save
```

### Step 3: Recent hiring activity

```bash
python3 "<script path>" "jobs/find" '{
  "organization": {"domain": "DOMAIN"},
  "filters": {},
  "limit": 25
}' --save
```

The script handles auth, retries, errors, domain normalization, and output formatting.

## After all three steps complete

Read the saved `.sumble/*.md` files and synthesize a **Company Intelligence Brief** with these sections:

1. **Company Overview** — name, domain, industry, size
2. **Technology Stack** — grouped by category, highlight key technologies and adoption signals
3. **Leadership & Key Contacts** — decision-makers with titles and LinkedIn URLs
4. **Hiring Trends** — what roles they're filling, what technologies appear in job postings, growth signals
5. **Key Takeaways** — 3-5 bullet points summarizing the most actionable intelligence

## Customization

If the user specifies a focus area (e.g., "engineering leaders", "sales team", "AI stack"), adjust the filters:

- **Engineering focus**: Step 2 filters → `{"job_functions": ["Engineer"], "job_levels": ["Manager", "Director", "VP"]}`
- **Sales focus**: Step 2 filters → `{"job_functions": ["Sales"], "job_levels": ["Manager", "Director", "VP", "C-Level"]}`
- **Specific tech**: Step 1 filters → `{"technologies": ["specific-tech-here"]}`

## Cost estimate

~15-30 credits per research (5/tech + 1/person + 3/job)

For API details, see [common.md](references/common.md). For troubleshooting, see [troubleshooting.md](../sumble-api/references/troubleshooting.md).
