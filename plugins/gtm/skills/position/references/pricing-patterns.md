# Pricing Patterns

## Table of Contents

- [Tier Structure Patterns](#tier-structure-patterns)
- [Competitor Anchoring Methodology](#competitor-anchoring-methodology)
- [Replacement Cost Math Framework](#replacement-cost-math-framework)
- [Expansion Triggers](#expansion-triggers)
- [Pricing Page Recommendations](#pricing-page-recommendations)

---

## Tier Structure Patterns

### Pattern 1: Freemium

Best for: developer tools, PLG products, products where usage drives upgrades.

```
Free         →  Pro           →  Enterprise
$0/mo           $X/mo            Custom
────────────    ──────────────   ──────────────
Core features   Free + ...       Pro + ...
Usage cap       Higher caps      Unlimited
Community       Email support    Dedicated CSM
                                 SSO, audit logs
                                 SLA
```

**When to use:** Product has a natural usage cap (API calls, seats, records). Free tier creates habit, paid tier removes friction.

**Risks:** Free tier too generous kills conversion. Free tier too stingy kills adoption. Test the cap.

**Conversion benchmarks:** 2-5% free-to-paid is healthy for PLG. Under 1% means the free tier solves the whole problem.

### Pattern 2: Good / Better / Best

Best for: B2B SaaS with clear feature tiers that map to company maturity.

```
Starter         →  Growth         →  Enterprise
$X/mo              $Y/mo             $Z/mo or custom
────────────       ──────────────    ──────────────
For individuals    For teams         For organizations
Core workflow      Starter + ...     Growth + ...
Basic reporting    Advanced reports  Custom reports
                   Team features     Admin controls
                   Integrations      SSO, SCIM
                                     Dedicated support
```

**When to use:** Features naturally cluster by sophistication. Starter solves the problem for one person, Growth for a team, Enterprise for a company.

**Pricing ratios:** Growth is typically 2-3x Starter. Enterprise is 3-5x Growth (or usage-based). If tiers are too close, the middle tier cannibalizes.

**The middle tier rule:** The middle tier should be where 60-70% of customers land. Price the outer tiers to push people toward the middle.

### Pattern 3: Usage-Based

Best for: infrastructure, API products, products where value scales linearly with consumption.

```
Pay as you go                    Committed
──────────────                   ──────────────
$X per [unit]                    $Y/mo for [volume]
No commitment                    Discounted rate
Scales up and down               Predictable billing
Metered billing                  Overage at PAYG rate
```

**When to use:** The value delivered is directly proportional to usage. Customers can predict their consumption. The unit is intuitive (API calls, records processed, emails sent).

**Unit selection:** The unit must be something the customer understands and can control. Good: emails sent, contacts enriched, API calls. Bad: "compute units," "credits" (opaque).

**Risks:** Revenue unpredictable. Customers may self-throttle to control costs. Consider a minimum commitment to stabilize.

### Pattern 4: Seat-Based

Best for: collaboration tools, CRM, anything where more users = more value.

```
Per seat pricing
──────────────
$X/user/mo
Volume discounts at thresholds
Minimum seat count (optional)
```

**When to use:** The product gets more valuable when more people use it. Each seat represents real usage.

**Risks:** Customers share logins to reduce cost. Shadow IT adopts free alternatives. Consider whether "viewer" seats should be free to maximize adoption.

### Pattern 5: Platform + Modules

Best for: products with distinct functional areas that not every customer needs.

```
Platform base     +  Module A      +  Module B      +  Module C
$X/mo                $Y/mo            $Z/mo            $W/mo
──────────────       ──────────────   ──────────────   ──────────────
Core features        Enrichment       Sequences        Analytics
Always included      Add if needed    Add if needed    Add if needed
```

**When to use:** Different personas buy different parts. Forces you to price each module against its specific competitor.

**Risks:** Complex pricing page. Customers cannot predict total cost. Works for enterprise sales, dangerous for PLG.

---

## Competitor Anchoring Methodology

Pricing does not happen in a vacuum. Every price is relative to an alternative.

### Step 1: Map the competitive price range

From 02-market.md, build this table:

```
| Competitor | Base Price | What's Included | What Costs Extra | Total Cost for Typical Customer |
|------------|-----------|-----------------|------------------|-------------------------------|
```

"Total Cost for Typical Customer" is the number that matters. Base price is misleading when competitors charge for add-ons, seats, overage, or implementation.

### Step 2: Identify your anchor position

Pick one:

| Strategy | When to use | Price relative to competitors |
|----------|-------------|-------------------------------|
| **Undercut** | Your costs are lower, you want volume, or you are entering a market with entrenched incumbents | 30-50% below market average |
| **Match** | You compete on features/experience, not price | Within 10-20% of market average |
| **Premium** | You deliver measurably more value, serve a higher segment, or replace multiple tools | 20-50% above market average, but below the combined tools you replace |
| **Value anchor** | Your product replaces a stack of tools; price against the stack, not individual competitors | Price at 30-50% of the total replacement cost |

### Step 3: Build the anchor into messaging

Do not just set a price. Explain why it is that price.

```
Instead of: "$99/mo"
Write:      "$99/mo — replaces $450/mo in tools (Clay + Instantly + Apollo)"

Instead of: "$499/mo"
Write:      "$499/mo — less than one SDR's daily salary for unlimited outreach"

Instead of: "Contact sales"
Write:      "Enterprise plans start at $2,000/mo — about what you spend on your current analytics stack"
```

### Step 4: Address the "is it worth it?" question

For every tier, have a ready answer to: "Why should I pay this instead of [alternative]?"

| Tier | Alternative | Answer |
|------|------------|--------|
| Free | Open source / DIY | "Same outcome, no maintenance, no DevOps hire" |
| Pro | Competitor's base plan | "Includes [X, Y, Z] that they charge extra for" |
| Enterprise | Competitor's enterprise + add-ons | "Single vendor, single invoice, lower total cost" |

---

## Replacement Cost Math Framework

Replacement cost is the most persuasive pricing argument in B2B. It answers: "What am I paying today that this product eliminates?"

### Step 1: Inventory what the product replaces

From 01-scan.md capabilities, identify everything the product can replace:

```
| Capability in 01-scan.md | What it replaces | Category |
|--------------------------|-----------------|----------|
| Built-in email sequencing | Outreach.io / Salesloft | Tool |
| Auto-enrichment pipeline | Clay / Clearbit | Tool |
| AI email writer | Copywriter or SDR time | Person |
| Automated lead scoring | Manual qualification | Process |
| Native CRM sync | Zapier + custom glue code | Tool + Process |
```

Categories: **Tool** (software subscription), **Person** (FTE or contractor time), **Process** (manual work that takes time but no direct cost), **Agency** (outsourced service).

### Step 2: Price each replacement

```
| Replacement | Monthly Cost | Source |
|------------|-------------|--------|
| Outreach.io | $100/user/mo x 5 users = $500/mo | Outreach pricing page |
| Clay | $500/mo (Professional plan) | Clay pricing page |
| Copywriter (part-time) | $2,500/mo | Average freelancer rate |
| Zapier (Premium) | $100/mo | Zapier pricing page |
| Manual qualification | 10 hrs/week x $50/hr = $2,000/mo | Estimated SDR time |
| **Total** | **$5,600/mo** | |
```

**Rules for honest math:**
- Use the plan tier the ICP would actually buy, not the most expensive one.
- For labor costs, use a blended rate that includes benefits (typically 1.3x base salary / 2080 hours).
- For "time saved," be conservative. Halving the time, not eliminating it, is more credible.
- Cite the source for every number. "Outreach pricing page, accessed Feb 2026."

### Step 3: Calculate the gap

```
Total replacement cost:  $5,600/mo
Your product price:      $  499/mo
─────────────────────────────────
Customer saves:          $5,101/mo ($61,212/year)
ROI:                     11.2x return on investment
Payback period:          < 1 month
```

### Step 4: Present it

Place the replacement cost table directly on the pricing page or in the sales deck. Format:

```
| What You're Paying Today | Monthly Cost | {Product} Equivalent |
|--------------------------|-------------|---------------------|
| Tool A | $500/mo | Built-in |
| Tool B | $500/mo | Built-in |
| Person/time | $2,500/mo | Automated |
| Glue code | $100/mo | Native |
| Manual work | $2,000/mo | Automated |
| **Total** | **$5,600/mo** | **$499/mo** |
```

---

## Expansion Triggers

Expansion triggers are signals that a customer should upgrade to a higher tier. Build these into the pricing structure so upgrades feel natural, not punitive.

### Trigger categories

**Usage-based triggers:**
- API calls or records processed exceed the current tier cap
- Storage or data volume approaches limit
- Number of active workflows or automations hits ceiling

**Team-based triggers:**
- Team grows past seat limit on current plan
- New department wants access (sales added, now marketing wants in)
- Need for role-based permissions or team-level analytics

**Feature-based triggers:**
- Customer requests SSO, SAML, or SCIM (enterprise security)
- Needs audit logs or compliance reporting
- Wants custom integrations or API access at higher rate limits
- Requests dedicated support or SLA guarantees

**Maturity-based triggers:**
- Customer moves from testing to production workload
- Expands from one use case to multiple
- Starts building internal processes around the product

### How to design tier boundaries around triggers

1. **Free → Paid:** The trigger should be success, not frustration. The customer upgrades because they got value and want more, not because they hit a wall. Good: "You've enriched 100 contacts this month — upgrade for unlimited." Bad: "Your trial expired."

2. **Paid → Enterprise:** The trigger should be organizational need, not individual need. SSO, audit logs, dedicated support, and custom contracts are natural enterprise triggers because they require org-level decision-making.

3. **Avoid punitive triggers:** Do not charge more for things that do not cost you more to deliver. Read-only seats, data exports, and basic API access should be free or cheap. Charging for them creates resentment.

### Expansion trigger checklist

For each tier boundary, answer:
- What usage or event signals the customer has outgrown this tier?
- Does the upgrade feel like a reward (more capability) or a penalty (paywall)?
- Can the customer predict when they will need to upgrade?
- Is the price delta justified by the additional value at the next tier?

---

## Pricing Page Recommendations

### Essential sections

Every pricing page needs these elements:

**1. Tier comparison table**
- 3-4 columns maximum (more causes decision paralysis)
- Highlight the recommended tier visually
- List features with checkmarks, not paragraphs
- Show the price per unit and billing frequency clearly

**2. Replacement cost anchor**
Place above or beside the tiers:
```
"Replaces $X,XXX/mo in tools. Starts at $XXX/mo."
```
This reframes the price from "cost" to "savings."

**3. FAQ section**
Address the top 5 pricing objections:
- "Can I switch plans?" (Yes, anytime, prorated)
- "What happens if I exceed my limit?" (Explain overage policy)
- "Do you offer annual discounts?" (If yes, state the percentage)
- "Is there a free trial?" (State the terms)
- "What's included in onboarding?" (Describe setup support)

**4. Social proof near the CTA**
A customer quote about value or ROI, placed directly next to the pricing CTA:
```
"We replaced 3 tools and cut our stack cost by 60%." — VP Sales, Acme Corp
```

**5. Enterprise callout**
If offering custom enterprise pricing:
```
Need SSO, custom contracts, or dedicated support?
Talk to sales →
```
Keep it simple. Do not hide enterprise behind a maze of forms.

### Common pricing page mistakes

| Mistake | Why it hurts | Fix |
|---------|-------------|-----|
| Too many tiers | Decision paralysis | 3 tiers (max 4 with free) |
| Feature list too long | Nobody reads 30 checkmarks | Top 5-7 differentiating features per tier |
| No anchor | Price feels expensive in isolation | Show replacement cost or competitor price |
| Hidden costs | Destroys trust when discovered later | List all costs upfront, including overage |
| No free option for PLG | Slows adoption | Add a free or trial tier with clear upgrade path |
| Annual pricing only | Creates commitment fear | Offer monthly with annual discount (15-20%) |
| "Contact sales" on every tier | Signals "expensive and opaque" | Show at least one self-serve price point |
