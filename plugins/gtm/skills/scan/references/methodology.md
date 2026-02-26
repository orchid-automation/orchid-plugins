# Scan Methodology: Replacement Cost Framework

This document defines how to analyze each capability for GTM value. Every feature found during the codebase scan must be evaluated through this lens before it reaches downstream skills.

---

## Table of Contents

1. [The 4 Questions](#the-4-questions)
2. [Analysis Framework by Feature Type](#analysis-framework-by-feature-type)
3. [Replacement Cost Estimation](#replacement-cost-estimation)
4. [Competitive Positioning Rules](#competitive-positioning-rules)
5. [Writing Style Rules](#writing-style-rules)

---

## The 4 Questions

Every feature, no exceptions. If a feature cannot answer all 4, flag it but do not skip it.

### 1. What can I do now that I couldn't before?

Not "what does the code do" -- what changes in the buyer's day, workflow, team, or budget. Frame as an outcome the buyer experiences.

### 2. What does this replace?

Every feature replaces something:
- A tool ($X/mo)
- A person ($Y/mo salary)
- A process (Z hours/week)
- An agency ($W/mo retainer)
- Manual work (N minutes per occurrence)

Name it. Price it.

### 3. What's the specific lift?

Not "saves time." How much time? Not "reduces cost." Which cost, how much? Not "improves quality." Compared to what baseline, by what measure?

### 4. Where do competitors fail at this?

Be specific: they don't offer it, they charge extra, they require manual setup, they limit it to enterprise tiers, they depend on a third-party integration, they do it but without intelligence/automation.

---

## Analysis Framework by Feature Type

### API Endpoints & Routes

For each endpoint, identify:
- **The buyer action** it enables (not the HTTP method)
- **The integration surface** -- what can be automated against it
- **The alternative** -- what the buyer does today without it

Framing example:
- BAD: "POST /api/ingest accepts an email and triggers enrichment"
- GOOD: "Drop in an email address. Get back a research dossier, ICP score, and personalized sequence in 60 seconds -- work an SDR spends 30-60 minutes doing manually."

### Database Models / Schema

Each entity = something the product manages for the buyer:
- What data does the buyer never have to track manually?
- What relationships does the system maintain automatically?
- What visibility does this give the buyer? (dashboards, analytics, audit trails)

### Background Jobs / Cron Tasks

Every automation = something the buyer doesn't have to remember:
- What fires automatically, and when?
- What would happen if the buyer did this manually? (cost of forgetting, frequency)
- What tooling does this replace? (Zapier, spreadsheet processes, ops team SOPs)

### AI/ML Components

AI features are the highest-lift items:
- What human judgment does this replicate? (cite the model, prompt strategy, guardrails)
- What's the quality baseline? (e.g., "reads like your best AE wrote it after 20 minutes of research")
- What's the consistency advantage? (AI doesn't have bad Fridays)
- What's the cost comparison? (AI per-unit cost vs. human time per-unit)

### Integrations & Webhooks

Every integration = a connection the buyer doesn't have to build:
- What data flows automatically, between which systems?
- What's the alternative? (Zapier at $20-50/mo, custom code, manual copy-paste)
- What events trigger real-time actions vs. polling?

### Configuration & Settings

Every config option = a lever the buyer can pull:
- What control does this give the buyer?
- What's the smart default? (less work for buyer)
- What would require code changes at a competitor?

### Auth, Permissions & Compliance

Security features = risk removers:
- What compliance requirement does this satisfy? (SOC 2, GDPR, CAN-SPAM, HIPAA)
- What would the buyer need to build/buy separately?
- What protects the buyer from their own mistakes? (guardrails, validation)

### CLI Tools / MCP Servers / Developer Tools

Developer-facing tools = integration accelerators:
- How fast can a developer integrate? (minutes vs. days)
- What workflows does this enable? (MCP is a massive differentiator in 2025-2026)
- What's the alternative? (REST API + custom code vs. native tool support)

---

## Replacement Cost Estimation

Use these benchmarks when pricing what a feature replaces.

### People

| Role | Monthly Cost (US) | Typical Capacity |
|------|------------------|-----------------|
| SDR/BDR | $5,000-7,000 | 50-100 leads/day outreach |
| AE (closing) | $8,000-12,000 | 20-40 qualified opps/month |
| RevOps / Ops | $7,000-10,000 | Tool management, reporting, data hygiene |
| Deliverability consultant | $500-1,500 setup + $200-500/mo | Domain setup, monitoring |
| GTM agency retainer | $10,000-25,000/mo | Full campaign management |
| Freelance copywriter | $500-2,000/mo | 50-200 emails/month |
| Data analyst | $6,000-9,000/mo | Reporting, dashboards, data pulls |
| DevOps engineer | $10,000-15,000/mo | Infrastructure, CI/CD, monitoring |

### Tools

| Category | Monthly Cost | Examples |
|----------|-------------|---------|
| Enrichment | $500-2,500/mo | Clay, Clearbit, Apollo, ZoomInfo |
| Email sending | $400-1,000/mo | Instantly, Smartlead, Outreach |
| Warmup services | $30-50/inbox/mo | Warmup Inbox, Instantly warmup |
| CRM | $50-300/mo | HubSpot, Salesforce, Pipedrive |
| Automation/iPaaS | $20-100/mo | Zapier, Make, n8n |
| Lead scoring | $200-500/mo | Madkudu, HubSpot scoring |
| Reply management | $50-200/mo | Front, Intercom |
| Analytics/BI | $100-500/mo | Mixpanel, Amplitude, Looker |
| Monitoring/APM | $200-800/mo | Datadog, New Relic, Sentry |
| Auth provider | $50-500/mo | Auth0, Clerk, WorkOS |
| AI/LLM API | $100-2,000/mo | OpenAI, Anthropic (usage-based) |
| Vector DB | $50-300/mo | Pinecone, Weaviate, Qdrant |

### Processes (Time Cost)

| Manual Process | Time Cost | Frequency |
|---------------|-----------|-----------|
| Lead research | 30-60 min/lead | Per lead |
| Email personalization | 15-30 min/email | Per email |
| ICP qualification | 2-5 min/lead | Per lead |
| Inbox rotation management | 1-2 hrs/week | Weekly |
| Bounce list cleanup | 1-2 hrs/week | Weekly |
| Reply classification | 30 min-1 hr/day | Daily |
| Reporting/analytics | 2-4 hrs/week | Weekly |
| Deployment & release | 1-4 hrs/release | Per release |
| Incident response triage | 30-60 min/incident | Per incident |
| Data migration/sync | 2-8 hrs/job | Per job |

---

## Competitive Positioning Rules

When noting competitor gaps during the scan, follow these rules:

1. **Always include pricing** -- "$X/mo" or "$X/yr" makes comparisons concrete
2. **Name what they don't do** -- not "they're limited" but "no ICP scoring, no per-lead personalization, no MCP server"
3. **Name what they charge extra for** -- "requires $97/mo add-on" or "enterprise tier only ($25K+/yr)"
4. **Name the setup cost** -- "2-8 week implementation" or "requires a dedicated ops person"
5. **Name the maintenance burden** -- "you maintain the workflow when APIs change"
6. **Never say "better" or "worse"** -- show the gap, let the reader decide

---

## Writing Style Rules

### DO

- Write in second person ("you", "your") -- talk directly to the buyer
- Use concrete numbers (time, cost, percentages)
- Name specific tools, roles, and processes being replaced
- Write section headers as statements the buyer nods along with
- Keep paragraphs to 2-3 sentences max
- Use tables for scannable comparisons

### DON'T

- Use "leverage," "robust," "scalable," "cutting-edge," "seamless," "empower," "unlock," "harness," "best-in-class"
- Start sentences with "Our product..." or "The system..."
- Write from the company's perspective -- always from the buyer's
- Use jargon without immediately translating to a buyer outcome
- Make claims without math ("10x your pipeline" needs the calculation)
- Write descriptions so generic they could apply to any product

### Tone

- Confident, not arrogant
- Direct, not aggressive
- Technical enough to be credible, accessible enough to be useful
- Like a smart friend who's done the research and is giving you the breakdown
