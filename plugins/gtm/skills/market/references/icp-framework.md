# ICP Inference Framework

How to determine the Ideal Customer Profile from codebase signals alone.

## Table of Contents

1. [Signal Types](#signal-types)
2. [Signal-to-ICP Mapping Table](#signal-to-icp-mapping-table)
3. [Company Profile Template](#company-profile-template)
4. [Persona Map Template](#persona-map-template)
5. [Worked Example](#worked-example)

---

## Signal Types

Five signal categories in the codebase reveal who the product is built for.

### 1. Schema Entity Signals

Database models and data structures reveal the domain and buyer.

| Entity Pattern | Inferred Domain | Likely Buyer |
|---------------|-----------------|--------------|
| `leads`, `contacts`, `accounts`, `campaigns`, `sequences` | Sales / GTM | VP Sales, Head of Growth, RevOps |
| `deployments`, `services`, `pods`, `clusters`, `logs` | Infrastructure / DevOps | VP Engineering, Platform Lead |
| `patients`, `providers`, `appointments`, `claims` | Healthcare | CTO at health-tech, Compliance Officer |
| `listings`, `properties`, `agents`, `showings` | Real Estate | Brokerage ops, Real Estate CTO |
| `orders`, `products`, `inventory`, `carts`, `SKUs` | E-commerce | Head of E-commerce, DTC founder |
| `students`, `courses`, `enrollments`, `grades` | EdTech | Head of Product, Academic Director |
| `tenants`, `workspaces`, `organizations`, `seats` | Multi-tenant SaaS | Any B2B buyer (segment by pricing) |
| `tickets`, `incidents`, `SLAs`, `escalations` | Support / ITSM | VP Support, Head of CX |

**How to extract**: Grep for model definitions, schema files, migration files, ORM declarations.

```
Grep(pattern="class.*Model|schema|table|entity|migration", glob="*.{py,rb,ts,js,prisma,sql}")
```

### 2. Integration Signals

External service connections reveal the buyer's existing stack and budget.

| Integration | Inferred Segment | Signal |
|-------------|-----------------|--------|
| Salesforce, HubSpot, Dynamics | Enterprise / Mid-market Sales | Budget for CRM = budget for tools |
| Stripe, Paddle, Chargebee | SaaS billing | Product is monetized, buyer thinks in MRR |
| Shopify, WooCommerce, BigCommerce | E-commerce | Merchant buyer, cares about conversion |
| Slack, Teams, Discord | Team collaboration | Team-based product, PLG potential |
| AWS, GCP, Azure (deep integration) | Enterprise infra | Technical buyer, long sales cycle |
| Twilio, SendGrid, Mailgun | Communication | Transactional product, scale matters |
| Segment, Mixpanel, Amplitude | Analytics-driven | Data team involved in buying decision |
| Okta, Auth0, SAML | Enterprise auth | Enterprise buyer, security-conscious |

**How to extract**: Grep for API keys, SDK imports, webhook URLs, config references.

```
Grep(pattern="import.*stripe|require.*salesforce|SHOPIFY|HUBSPOT|SENDGRID", glob="*.{py,rb,ts,js}")
```

### 3. Feature Signals

What the product does reveals which team benefits.

| Feature Pattern | Target Team | Buyer Signal |
|----------------|-------------|--------------|
| API-first, SDK, MCP server, CLI | Developers | Technical buyer, bottom-up adoption |
| Email sequences, CRM sync, lead scoring | Sales | Sales leader, measured on pipeline |
| Dashboards, reports, analytics | Data / Growth | Measured on metrics, needs visibility |
| RBAC, audit logs, SSO, SOC 2 | Enterprise | Security review required, longer sales cycle |
| Self-serve onboarding, freemium | SMB / PLG | Low-touch, volume play |
| White-label, multi-tenant, branding | Agency / Platform | Reseller motion, per-client pricing |
| Workflow builder, automations, triggers | Ops / RevOps | Process-oriented buyer, replaces manual work |

### 4. Pricing Tier Signals

Price points in the codebase reveal market segment.

| Price Range | Segment | Typical Buyer |
|------------|---------|---------------|
| Free / $0-29/mo | Individual / Hobbyist | Solo practitioner, freelancer |
| $49-199/mo | SMB | Founder, department head |
| $299-999/mo | Mid-market | VP-level, needs ROI justification |
| $1,000-4,999/mo | Upper mid-market | C-suite or VP with budget authority |
| $5,000+/mo or custom pricing | Enterprise | Procurement process, legal review |

**How to extract**: Grep for pricing constants, plan names, tier definitions.

```
Grep(pattern="price|tier|plan|subscription|STARTER|PRO|ENTERPRISE", glob="*.{py,rb,ts,js,json,yaml}")
```

### 5. UI Copy Signals

Marketing language in the codebase reveals intended positioning.

| Copy Pattern | Inferred Positioning |
|-------------|---------------------|
| "for teams" | Team-based pricing, collaboration focus |
| "for developers" | Technical audience, bottom-up adoption |
| "for enterprise" | High-touch sales, security features |
| "save X hours" | Productivity tool, time ROI |
| "replace your {tool}" | Displacement play, cost ROI |
| "no-code" / "without engineers" | Non-technical buyer |
| "AI-powered" / "intelligent" | Innovation buyer, early adopter |

**How to extract**: Read landing pages, onboarding copy, README, marketing directories.

```
Grep(pattern="for teams|for developers|for enterprise|save.*hours|replace|no.code", glob="*.{html,tsx,jsx,md}")
```

---

## Signal-to-ICP Mapping Table

Combine signals to build a composite profile.

| Signal Combination | ICP | Confidence |
|-------------------|-----|------------|
| `leads` + Salesforce + email sequences + $299-999/mo | Mid-market Sales team | High |
| `deployments` + AWS + CLI + API-first + $1K+/mo | Platform Engineering at Series B+ | High |
| `orders` + Shopify + Stripe + $49-199/mo | SMB e-commerce merchant | High |
| `patients` + HIPAA mentions + SSO + custom pricing | Healthcare enterprise | High |
| `tenants` + white-label + Stripe + $999+/mo | SaaS platform / Agency | Medium |
| API-first + no UI + SDK + free tier | Developer tool, PLG | Medium |
| Dashboards + Segment + analytics + $199-499/mo | Growth / Data team at mid-market | Medium |

When signals conflict (e.g., SMB pricing but enterprise auth features), the pricing signal usually wins for primary ICP. The enterprise features indicate an upsell path.

---

## Company Profile Template

Fill every field. No "various" or "multiple" -- be specific.

```markdown
### Company Profile
- **Industry**: {2-3 specific verticals, ranked by fit}
- **Revenue range**: ${X}M - ${Y}M ARR
- **Employee count**: {range, e.g., "50-500"}
- **Stage**: {Seed / Series A / Series B / Series C+ / Growth / Public}
- **Tech maturity**: {Low / Medium / High}
  - Low = no engineering team, uses no-code tools
  - Medium = small eng team, uses standard SaaS stack
  - High = platform team, builds internal tools, evaluates on API quality
- **Key signal**: "They have {problem} but not {solution}"
  - Example: "They have 10+ SDRs doing manual research but no automated enrichment pipeline"
  - Example: "They have Kubernetes in production but no cost visibility across clusters"
```

---

## Persona Map Template

Four personas. Each must be specific enough that a salesperson could find this person on LinkedIn.

### Primary Buyer (signs the check)

The person with budget authority who approves the purchase.

```markdown
- **Title**: {VP of Sales, Head of Engineering, CTO -- pick ONE most common}
- **Pain**: {the business problem they own, stated as they'd say it}
  - Example: "Pipeline is flat but the board wants 3x growth without 3x headcount"
- **Language they use**: {exact phrases from their world}
  - Example: "pipeline coverage", "cost per meeting", "ramp time", "quota attainment"
- **Objections**:
  1. {Budget: "We already spend $X on tools, why add another?"}
  2. {Risk: "What if it breaks our existing workflow?"}
  3. {Timing: "We're mid-migration, can we do this next quarter?"}
```

### Primary User (uses it daily)

The person who lives in the product 8 hours a day.

```markdown
- **Title**: {SDR, DevOps Engineer, Data Analyst -- the daily operator}
- **Pain**: {the daily friction, stated as they'd complain about it}
  - Example: "I spend 45 minutes per lead just finding the right email and writing a personalized opener"
- **Language they use**: {operational terms}
  - Example: "bounce rate", "sequence replies", "warm leads", "manual enrichment"
- **Objections**:
  1. {Learning curve: "I just learned the last tool, now another?"}
  2. {Trust: "Will it actually work or is it another demo that looks good?"}
```

### Blocker (says no)

The person who can kill the deal. Usually IT, Security, Legal, or Finance.

```markdown
- **Title**: {CISO, IT Director, Legal Counsel, CFO}
- **Pain**: {the risk they're paid to prevent}
  - Example: "Every new vendor is a potential data breach and a compliance headache"
- **Language they use**: {risk and compliance terms}
  - Example: "SOC 2 report", "data residency", "vendor assessment", "budget cycle"
- **Objections**:
  1. {Security: "Where is data stored? Who has access?"}
  2. {Compliance: "Is this GDPR/CCPA compliant?"}
  3. {Budget: "This wasn't in the approved budget for this quarter"}
```

### Champion (fights for it internally)

The person who discovered the product and sells it up the chain.

```markdown
- **Title**: {Senior SDR, Lead Engineer, RevOps Manager -- mid-level with influence}
- **Pain**: {what they're tired of doing the old way}
  - Example: "I've built 6 spreadsheet automations to work around our current tool's limitations"
- **Language they use**: {problem-aware terms}
  - Example: "there has to be a better way", "I saw a demo of X", "what if we could automate Y"
- **Internal pitch**: {how they'd sell it to their VP}
  - Example: "This replaces 3 tools we're paying $4K/mo for and cuts lead research from 45 min to 2 min"
```

---

## Worked Example

**Codebase signals found in 01-scan.md:**

- Models: `Lead`, `Contact`, `Account`, `Sequence`, `EmailStep`, `Enrichment`
- Integrations: Salesforce, HubSpot, Clearbit, OpenAI, SendGrid, Slack
- Features: Lead scoring, email sequence builder, AI email generation, CRM sync, analytics dashboard
- Pricing: Starter ($299/mo), Growth ($799/mo), Scale ($1,999/mo)
- UI copy: "for GTM teams", "replace your outbound agency"

**Resulting ICP:**

- **Industry**: B2B SaaS, Professional Services, Recruiting/Staffing
- **Revenue range**: $5M - $100M ARR
- **Employee count**: 50-500
- **Stage**: Series A through Series C
- **Tech maturity**: Medium (uses Salesforce, some automation, no internal tools team)
- **Key signal**: "They have 5-20 SDRs doing manual outbound but no AI enrichment or automated personalization"

**Primary Buyer**: VP of Sales -- "Pipeline coverage is at 2x but the board wants 4x. I can't hire fast enough."

**Primary User**: SDR -- "I spend an hour per lead doing research before I can even write the first email."

**Blocker**: IT Director -- "Our Salesforce instance is already a mess. I don't want another tool writing to it."

**Champion**: Senior SDR -- "I found this tool that auto-researches leads and writes personalized emails. It could save the team 20 hours a week."
