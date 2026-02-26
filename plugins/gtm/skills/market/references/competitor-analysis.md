# Competitive Research Playbook

How to find, evaluate, and map competitors for any product category.

## Table of Contents

1. [Search Strategy](#search-strategy)
2. [Search Query Templates](#search-query-templates)
3. [Evaluation Criteria](#evaluation-criteria)
4. [Competitor Profile Template](#competitor-profile-template)
5. [Market Gap Identification](#market-gap-identification)
6. [Pricing Intelligence](#pricing-intelligence)
7. [Worked Example](#worked-example)

---

## Search Strategy

Run searches in three waves. Each wave narrows the focus.

### Wave 1: Category Discovery

Find the market category and top players. Use broad searches.

```
WebSearch("{product-category} software alternatives 2025")
WebSearch("best {product-category} tools for {buyer-type}")
WebSearch("{product-category} market map")
```

**What to extract**: Category name (how analysts describe this market), top 5-10 names that keep appearing, any market maps or landscape graphics.

### Wave 2: Direct Comparison

Find head-to-head comparisons and review aggregators.

```
WebSearch("{closest-competitor} vs alternatives")
WebSearch("{product-category} G2 comparison grid")
WebSearch("{product-category} Capterra top rated 2025")
WebSearch("{competitor-A} vs {competitor-B} vs {competitor-C}")
```

**What to extract**: Pricing tiers, feature comparison tables, user complaints, switching triggers ("I left X because...").

### Wave 3: Deep Dives

Research each competitor individually for gaps and sentiment.

```
WebSearch("{competitor} pricing 2025")
WebSearch("{competitor} G2 reviews complaints")
WebSearch("{competitor} funding crunchbase")
WebSearch("{competitor} integrations list")
WebSearch("{competitor} vs {this-product-category} limitations")
```

**What to extract**: Exact pricing, common complaints, funding/headcount trajectory, missing integrations, enterprise vs. self-serve positioning.

---

## Search Query Templates

Copy-paste these and fill in the blanks.

### Finding Competitors

| Query Pattern | When to Use |
|--------------|-------------|
| `"{category} software" alternatives 2025` | Starting from scratch |
| `best {category} tools for {buyer-title}` | When ICP is known |
| `{category} market map landscape` | Finding analyst views |
| `"{known-competitor}" vs` | Expanding from one known player |
| `{category} G2 grid report` | Getting structured comparisons |
| `{category} open source alternative` | Finding free/OSS competitors |
| `{category} for {company-size}` | Segment-specific players |
| `switch from {incumbent} to` | Finding displacement competitors |
| `"{category}" startup funding 2024 2025` | Finding emerging players |

### Evaluating Competitors

| Query Pattern | What You Get |
|--------------|-------------|
| `{competitor} pricing page` | Current pricing tiers |
| `{competitor} G2 reviews` | User sentiment, star rating |
| `{competitor} Capterra reviews` | Alternative sentiment source |
| `{competitor} crunchbase funding` | Funding stage and amount |
| `{competitor} integrations` | Integration coverage |
| `{competitor} API documentation` | Technical depth |
| `{competitor} onboarding setup time` | Implementation complexity |
| `{competitor} limitations complaints reddit` | Unfiltered user pain |
| `site:reddit.com "{competitor}" frustrating OR annoying OR limited` | Reddit-specific complaints |

---

## Evaluation Criteria

Score each competitor across these dimensions.

### 1. Pricing

| Data Point | How to Find | Why It Matters |
|-----------|-------------|----------------|
| Entry price | Pricing page or WebSearch | Sets the floor for positioning |
| Top tier price | Pricing page | Sets the ceiling |
| Per-seat vs. flat | Pricing page | Affects cost at scale |
| Free tier / trial | Pricing page | Indicates PLG motion |
| Hidden costs | G2 reviews ("surprised by...") | Reveals real TCO |
| Contract requirements | Pricing page fine print | Annual lock-in = switching opportunity |

**Example output:**
> Clay: $149/mo (Starter) to $720/mo (Pro). Per-credit pricing means costs scale unpredictably. No free tier. Annual contract for Enterprise.

### 2. Feature Gaps

Compare against capabilities found in `01-scan.md`.

| Question | How to Answer |
|----------|---------------|
| What do WE do that they don't? | Compare feature lists from their site vs. our scan |
| What do THEY do that we don't? | Same comparison, reversed |
| What do we BOTH do but we do better? | Check implementation depth |
| What's their weakest area per G2? | Read 1-2 star reviews |

### 3. Setup Complexity

| Level | Indicators | Buyer Impact |
|-------|-----------|--------------|
| Self-serve (minutes) | "Sign up and start", no sales call | PLG, low friction, easy to switch TO |
| Guided (days) | Onboarding call, setup wizard | Medium friction |
| Implementation (weeks) | Dedicated CSM, data migration, training | High friction, hard to switch FROM |
| Enterprise (months) | Custom deployment, SOW, professional services | Very high friction, long sales cycle |

### 4. G2/Capterra Sentiment

| Signal | What It Means |
|--------|---------------|
| 4.5+ stars, 500+ reviews | Established, hard to displace on quality |
| 4.0-4.4 stars, 100+ reviews | Good but has known weaknesses to exploit |
| 3.5-3.9 stars, any review count | Clear pain points, users are looking for alternatives |
| < 3.5 stars | Vulnerable, active churn |
| "Easy to use" as top praise | UX is their moat |
| "Great support" as top praise | Product has gaps, support compensates |
| "Expensive for what you get" | Pricing vulnerability |
| "Hard to set up" | Onboarding vulnerability |
| "Missing features" recurring | Feature gap opportunity |

### 5. Funding and Momentum

| Signal | What It Means |
|--------|---------------|
| Recent Series B/C (last 12 months) | Growing fast, will add features quickly |
| No funding in 2+ years | Bootstrapped (stable) or stalled |
| Large headcount growth | Investing in go-to-market |
| Layoffs or headcount shrink | Potential instability, customer churn |
| Recently acquired | Product may stagnate or pivot |

### 6. Integration Gaps

Cross-reference competitor integrations with what `01-scan.md` shows.

| Check | Significance |
|-------|-------------|
| Do they integrate with the same tools? | Table stakes -- must match |
| Do they miss integrations we have? | Differentiation opportunity |
| Do they have integrations we lack? | Risk -- may need to add |
| Is their API well-documented? | Technical buyers compare API quality |

---

## Competitor Profile Template

Use this structure for each competitor in the output document.

```markdown
### {Competitor Name}
- **What they do**: {one sentence positioning}
- **What they don't do**: {specific gaps relevant to this product}
- **Pricing**: ${X}/mo (Starter) to ${Y}/mo (Enterprise)
  - Pricing model: {per-seat / per-credit / flat / usage-based}
  - Free tier: {yes/no}
  - Contract: {monthly / annual required / custom}
- **Setup complexity**: {self-serve / guided / implementation / enterprise}
  - Typical time to value: {minutes / days / weeks}
- **G2 sentiment**: {X.X}/5 ({N} reviews)
  - Top praise: "{quoted theme}"
  - Top complaint: "{quoted theme}"
- **Funding / momentum**: {last round, amount, date} | {headcount trend}
- **Key gap**: {the single biggest weakness relative to this product}
```

---

## Market Gap Identification

After profiling all competitors, synthesize gaps across four dimensions.

### 1. What NOBODY does well

Look for complaints that appear across multiple competitors' reviews.

```
WebSearch("{category} software frustrations reddit")
WebSearch("{category} tools missing features")
```

**Example**: "Every outbound tool requires you to manually research each lead before writing the email. Nobody automates the research-to-personalization pipeline end-to-end."

### 2. What everyone charges extra for

Look for features gated behind enterprise tiers or add-on pricing.

**Common patterns:**
- API access only on highest tier
- Integrations as paid add-ons
- Analytics/reporting behind paywall
- SSO as enterprise-only feature (the "SSO tax")
- Custom fields / workflows on premium plans

**Example**: "Every competitor charges $200+/mo extra for CRM sync. Including it in the base tier is a differentiation play."

### 3. Where onboarding is painful

Look for setup-related complaints and long time-to-value.

**Signals:**
- "Took 3 weeks to get started" in reviews
- Required implementation partner
- Complex data migration
- Training sessions required
- "Steep learning curve" mentioned repeatedly

**Example**: "Clay requires 2-8 weeks of workflow building before a single lead is enriched. Instant setup is a wedge."

### 4. Self-serve gap

Features that require contacting sales when they should be self-serve.

**Signals:**
- "Contact us for pricing" on core features
- "Book a demo" as only CTA
- No public documentation or API reference
- Trial requires credit card + sales call

**Example**: "Three of five competitors require a demo call before you can see the product. Offering instant access with a free tier captures the 'I want to try it now' buyer."

---

## Pricing Intelligence

### Price Positioning Options

| Strategy | When to Use | Risk |
|----------|-------------|------|
| **Undercut** (30-50% below leader) | When product is comparable, buyer is price-sensitive | Race to bottom, signals "cheap" |
| **Match** (within 10% of leader) | When differentiation is on features, not price | Must prove feature superiority |
| **Premium** (20-50% above leader) | When product has unique capabilities | Must justify with clear ROI math |
| **Value anchor** (price against replacement cost) | When replacing multiple tools or manual work | Requires credible replacement math |

### Replacement Cost Math

The most powerful pricing argument is: "You're already spending more than this."

```
Current cost = Tool A ($X/mo) + Tool B ($Y/mo) + Z hours/week of manual work ($W/hr)
Our price = ${total} — less than what you're spending on Tool A alone
```

---

## Worked Example

**Product category**: AI-powered outbound sales platform

**Wave 1 searches:**
- `"outbound sales platform" software alternatives 2025`
- `"best outbound tools for B2B sales teams"`
- `"sales engagement platform market map"`

**Competitors found**: Clay, Instantly, Apollo, Outreach, Salesloft, Smartlead

**Gap synthesis:**

| Gap Type | Finding |
|----------|---------|
| Nobody does well | End-to-end lead research to personalized email without manual workflow building |
| Charged extra for | CRM sync, AI features, API access -- all gated on premium tiers |
| Onboarding pain | Clay: 2-8 weeks to build workflows. Outreach: dedicated implementation. |
| Self-serve gap | Outreach and Salesloft require demo calls. No instant trial. |

**Pricing positioning**: Value anchor at $799/mo against $3,200/mo combined stack (Clay $720 + Instantly $600 + enrichment tools $400 + 20 hrs/mo manual work at $75/hr).
