# Feature Map Analysis Methodology

This document is the analysis playbook for feature-map agents. Each agent reads this before analyzing their assigned feature category.

---

## The GTM Lens

You are not writing documentation. You are not writing a changelog. You are building a **buyer decision document** — something that makes a potential customer think "I need this" instead of "that's nice."

Every feature you analyze must pass through this filter:

### The 4 Questions (every feature, no exceptions)

1. **What can I do now that I couldn't before?** — Not "what does the code do" but "what changes in my day, my workflow, my team, my budget."

2. **What does this replace?** — Every feature replaces something. A tool ($X/mo). A person ($Y/mo salary). A process (Z hours/week). An agency ($W/mo retainer). Manual work (N minutes per occurrence). Name it and price it.

3. **What's the specific lift?** — Not "saves time." How much time? Not "reduces cost." Which cost? How much? Not "improves quality." Compared to what baseline? By what measure?

4. **Where do competitors fail at this?** — Not "they're bad." Specifically: they don't offer it, they charge extra for it, they require manual setup, they limit it to enterprise tiers, they depend on a third-party integration, they do it but without intelligence/automation.

---

## Analysis Framework by Feature Type

### API Endpoints & Routes

For each endpoint, document:
- **The buyer action** it enables (not the HTTP method)
- **The integration surface** — what can be automated against it
- **The alternative** — what the buyer does today without this endpoint (usually: manual work in a dashboard, or copying data between tools)

Example framing:
- BAD: "POST /api/ingest accepts an email address and triggers enrichment"
- GOOD: "Drop in an email address. Get back a research dossier, ICP score, and personalized email sequence in 60 seconds — the same work an SDR spends 30-60 minutes doing manually."

### Database Models / Schema

Each entity represents something the product **manages for the buyer**. Frame as:
- **What data does the buyer never have to track manually?**
- **What relationships does the system maintain automatically?**
- **What visibility does this give the buyer?** (dashboards, analytics, audit trails)

### Background Jobs / Cron Tasks

Every automation is **something the buyer doesn't have to remember to do**. Frame as:
- **What fires automatically?** (and when)
- **What would happen if the buyer had to do this manually?** (cost of forgetting, frequency of the task)
- **What tooling does this replace?** (Zapier automations, manual spreadsheet processes, ops team SOPs)

### AI/ML Components

AI features are the highest-lift items. Frame as:
- **What human judgment does this replicate?** (and how well — cite the model, the prompt strategy, the guardrails)
- **What's the quality baseline?** (e.g., "reads like your best AE wrote it after 20 minutes of research")
- **What's the consistency advantage?** (AI doesn't have bad Fridays, doesn't take shortcuts at 4:59pm)
- **What's the cost comparison?** (AI processing per lead vs. human time per lead)

### Integrations & Webhooks

Every integration point is a **connection the buyer doesn't have to build**. Frame as:
- **What data flows automatically?** (and between which systems)
- **What's the alternative?** (usually: Zapier at $20-50/mo, custom code, or manual copy-paste)
- **What events trigger real-time actions?** (webhooks = instant response vs. polling = delayed)

### Configuration & Settings

Every configuration option is a **lever the buyer can pull**. Frame as:
- **What control does this give the buyer?** (not "you can set X" but "you decide how aggressively to auto-send")
- **What's the default?** (smart defaults = less work for the buyer)
- **What would require code changes at a competitor?** (configurability vs. rigidity)

### Auth, Permissions & Compliance

Security features are **risk removers**. Frame as:
- **What compliance requirement does this satisfy?** (SOC 2, GDPR, CAN-SPAM, HIPAA)
- **What would the buyer need to build/buy separately?** (compliance consulting, audit tools)
- **What protects the buyer from their own mistakes?** (guardrails, validation, loop prevention)

### CLI Tools / MCP Servers / Developer Tools

Developer-facing tools are **integration accelerators**. Frame as:
- **How fast can a developer integrate?** (minutes vs. days)
- **What workflows does this enable?** (especially AI-native workflows — MCP is a massive differentiator in 2025-2026)
- **What's the alternative?** (REST API + custom code vs. native tool support)

---

## Replacement Cost Estimation Guide

When pricing what a feature replaces, use these benchmarks:

### People
| Role | Monthly Cost (US) | Typical Capacity |
|------|------------------|-----------------|
| SDR/BDR | $5,000-7,000 | 50-100 leads/day outreach |
| AE (closing) | $8,000-12,000 | 20-40 qualified opps/month |
| Ops/RevOps | $7,000-10,000 | Tool management, reporting |
| Deliverability consultant | $500-1,500 setup + $200-500/mo | Domain setup, monitoring |
| Agency retainer (GTM) | $10,000-25,000/mo | Full campaign management |
| Freelance copywriter | $500-2,000/mo | 50-200 emails/month |

### Tools
| Category | Monthly Cost | Examples |
|----------|-------------|---------|
| Enrichment | $500-2,500/mo | Clay, Clearbit, Apollo, ZoomInfo |
| Email sending | $400-1,000/mo | Instantly, Smartlead, Outreach |
| Warmup services | $30-50/inbox/mo | Warmup Inbox, Instantly warmup |
| CRM | $50-300/mo | HubSpot, Salesforce, Pipedrive |
| Automation | $20-100/mo | Zapier, Make, n8n |
| Lead scoring | Included in CRM or $200-500/mo | Madkudu, HubSpot scoring |
| Reply management | $50-200/mo | Front, Intercom, or manual |

### Processes
| Manual Process | Time Cost | Frequency |
|---------------|-----------|-----------|
| Lead research | 30-60 min/lead | Per lead |
| Email personalization | 15-30 min/email | Per email |
| ICP qualification | 2-5 min/lead | Per lead |
| Inbox rotation management | 1-2 hrs/week | Weekly |
| Bounce list cleanup | 1-2 hrs/week | Weekly |
| Reply classification | 30 min-1 hr/day | Daily |
| Reporting/analytics | 2-4 hrs/week | Weekly |

---

## Competitive Positioning Rules

1. **Always include pricing** — "$X/mo" or "$X/yr" — make the comparison concrete
2. **Name what they don't do** — not "they're limited" but "no ICP scoring, no per-lead personalization, no MCP server"
3. **Name what they charge extra for** — "requires a separate $97/mo add-on" or "enterprise tier only ($25K+/yr)"
4. **Name the setup cost** — "2-8 week implementation" or "requires a dedicated ops person"
5. **Name the maintenance burden** — "you maintain the workflow when APIs change" or "manual configuration per campaign"
6. **Never say "better" or "worse"** — show the gap and let the reader decide

---

## Writing Style Guide

### DO:
- Write in second person ("you", "your") — talk directly to the buyer
- Use concrete numbers (time, cost, percentages)
- Use analogies to things they already understand
- Name specific tools, roles, and processes being replaced
- Write section headers as statements the buyer can nod along with
- Keep paragraphs to 2-3 sentences max
- Use tables for scannable comparisons

### DON'T:
- Use "leverage," "robust," "scalable," "cutting-edge," "seamless," "empower," "unlock," "harness"
- Start sentences with "Our product..." or "The system..."
- Write from the company's perspective — always from the buyer's
- Use technical jargon without immediately translating it to a buyer outcome
- Make claims without backing them up (no "10x your pipeline" without showing the math)
- Write feature descriptions that could apply to any product (specificity is everything)

### Tone:
- Confident but not arrogant
- Direct but not aggressive
- Technical enough to be credible, accessible enough to be useful
- Like a smart friend who's done the research and is giving you the breakdown

---

## Output File Format

Each agent writes a markdown file to `docs/feature-map-{category}.md` with this structure:

```markdown
# {Product Name} Feature Map: {Category Name}

> {X} features that {buyer outcome summary}.

---

## 1. {Feature Name}

**What it does:** {One paragraph — buyer-focused, not technical}

**Why it matters:** {What changes. What risk is removed. What time/cost is saved.}

**The lift:** {Specific replacement — tool, person, process, cost}

**vs. competitors:**
- **{Competitor A}:** {Gap description}
- **{Competitor B}:** {Gap description}

---

## 2. {Next Feature}
...

---

## Summary: What This Stack Replaces

| What you're paying for today | Cost | {Product} equivalent |
|------------------------------|------|---------------------|
| {Item} | ${X}/mo | {Feature name} |
| ... | ... | ... |
| **Total replaced** | **${sum}/mo** | **Built-in** |
```
