# Battle Card Template

## Table of Contents

- [Card Structure](#card-structure)
- [How to Build Each Row](#how-to-build-each-row)
- [Trap Questions](#trap-questions)
- [Demo Moments](#demo-moments)
- [ROI Math Per Competitor](#roi-math-per-competitor)
- [Example Battle Cards](#example-battle-cards)

---

## Card Structure

Every battle card follows the same layout. One card per competitor.

```
### vs. {Competitor} ({their price}/mo)

| Their Claim | Our Counter | Proof Point |
|-------------|-------------|-------------|
| row 1 | | |
| row 2 | | |
| row 3 | | |
| row 4 | | |

Trap question: "..."
Demo moment: "..."
ROI math: ...
```

Aim for 4-6 rows per competitor. Each row targets a different buying criterion.

---

## How to Build Each Row

### Column 1: Their Claim

What the competitor says on their website, in sales calls, or on G2. Use their actual language. Sources:

- Their pricing page headline
- G2/Capterra "pros" section (what customers praise)
- Their case studies or testimonials
- Sales decks or demo recordings if available

Do not paraphrase into something weaker. Use their strongest version. The counter is more convincing when the claim is real.

### Column 2: Our Counter

What we do differently that makes their claim incomplete, misleading, or irrelevant. Rules:

- **Never say "we're better."** Say what we do and let the contrast speak.
- **Be specific.** Not "faster setup" but "live in 15 minutes vs. their 2-week implementation."
- **Reframe when possible.** If they claim "500+ integrations," counter with "3 integrations that matter, pre-configured" if that is the actual advantage.
- **Acknowledge what they do well** if it is something we do not compete on. Credibility comes from honesty.

### Column 3: Proof Point

Evidence that makes the counter verifiable. Acceptable proof:

- A feature that exists in 01-scan.md (with the endpoint or capability name)
- A metric from your product (setup time, API response time, user count)
- A direct comparison (their pricing page says X, ours does Y)
- A customer quote or case study reference
- A technical fact (open source, SOC 2 certified, no vendor lock-in)

Unacceptable proof: opinions, future roadmap items, vague claims like "our customers love it."

---

## Trap Questions

Trap questions are discovery call questions designed so that an honest answer reveals the competitor's weakness. They work because:

1. The prospect already has the competitor's pitch in their head
2. The question makes them verify a specific claim
3. When they check, the answer favors you

### How to write trap questions

**Pattern:** "Ask them {specific question about a capability we have and they lack or do poorly}."

**Rules:**
- The question must be fair. If a prospect asked us the same question, we should have a strong answer.
- Frame it as genuine due diligence, not a gotcha.
- Focus on the gap that matters most to the buyer persona. A CTO cares about architecture; a VP Sales cares about time-to-value.

**Formula options:**

1. **The "how" question:** "Ask them how they handle {thing we automate but they require manual work for}."
2. **The "show me" question:** "Ask them to demo {capability we have that they do not list on their features page}."
3. **The "what happens when" question:** "Ask what happens when {edge case that breaks their approach but not ours}."
4. **The "who else" question:** "Ask how many customers use {feature they claim but rarely deliver}."
5. **The pricing trap:** "Ask them for the total cost including {add-on they charge extra for that we include}."

---

## Demo Moments

A demo moment is the single feature or workflow you show that makes the prospect say "wait, it does that?" It is the visual proof that the battle card rows are real.

### Selecting demo moments

For each competitor, pick the moment where:

1. **The gap is visible.** The prospect can see the difference, not just hear about it.
2. **The outcome is immediate.** Show a result, not a configuration screen.
3. **The competitor cannot replicate it easily.** Something architectural, not just a missing checkbox.

### Format

```
Demo moment: "Show {specific action} → {visible result} — their product requires {manual steps or workaround}."
```

Keep it to one sentence. The sales rep needs to remember it mid-call.

---

## ROI Math Per Competitor

ROI math answers: "If I switch from {competitor} to you, what do I save?"

### Framework

```
Current competitor cost:
  Base price:              ${X}/mo
  Required add-ons:        ${Y}/mo (list each: analytics, API access, etc.)
  Implementation/setup:    ${Z} one-time (amortized over 12 months = ${Z/12}/mo)
  Labor to operate:        {N} hours/week x ${hourly rate} = ${labor}/mo
  ─────────────────────────────────────────
  Total competitor cost:   ${total}/mo

Our cost:
  Plan price:              ${A}/mo
  Setup:                   ${B} one-time (or $0 if self-serve)
  Labor to operate:        {M} hours/week x ${hourly rate} = ${labor}/mo
  ─────────────────────────────────────────
  Total our cost:          ${our_total}/mo

Monthly savings:           ${total - our_total}/mo
Annual savings:            ${(total - our_total) * 12}/yr
Payback period:            {switching cost / monthly savings} months
```

Use real numbers from 02-market.md competitor pricing. Estimate labor hours conservatively — overblown ROI math destroys credibility.

---

## Example Battle Cards

### Example 1: CRM Tool vs. Legacy Enterprise CRM

```markdown
### vs. LegacyCRM ($150/user/mo)

| Their Claim | Our Counter | Proof Point |
|-------------|-------------|-------------|
| "Most customizable CRM on the market" | Every field is configurable, but so is ours — without a $40K implementation partner | Self-serve field builder, zero implementation fee, live in 1 day vs. their 6-8 week average |
| "500+ integrations" | We integrate with the 12 tools sales teams actually use, pre-configured out of the box | Slack, Gmail, Salesforce, HubSpot, Outreach, Gong, Zoom, LinkedIn connected in <5 min each |
| "Enterprise-grade security" | We are SOC 2 Type II certified too — plus we do not require on-prem deployment | SOC 2 Type II audit report available; cloud-native, encrypted at rest and in transit |
| "AI-powered insights" | Their AI requires 6 months of data before it produces anything useful; ours works on day 1 | Pre-trained models on anonymized B2B sales patterns; first recommendations within 24 hours |

**Trap question:** "Ask them what the total cost of implementation is, including partner fees and the timeline before your team is fully onboarded."

**Demo moment:** "Import a CSV of 100 contacts → show enriched profiles, auto-created deals, and suggested next actions in under 2 minutes. Their product would show you a blank pipeline."

**ROI math:** LegacyCRM at $150/user/mo + $40K implementation + $2K/mo admin labor = ~$190/user/mo effective. Our $49/user/mo self-serve with no admin overhead saves $141/user/mo. 50-person team saves $84,600/year.
```

### Example 2: Analytics Platform vs. Open-Source Stack

```markdown
### vs. DIY Analytics (Metabase + dbt + Snowflake)

| Their Claim | Our Counter | Proof Point |
|-------------|-------------|-------------|
| "Free and open source" | Free to download, but costs $3-8K/mo in engineering time to maintain | Average data team spends 15-20 hrs/week on pipeline maintenance (dbt Slack community survey) |
| "Complete control over your stack" | Control also means you own every outage, migration, and breaking change | We handle infra, updates, and scaling; 99.95% uptime SLA |
| "No vendor lock-in" | Your dashboards are locked into whoever maintains the SQL; our export works everywhere | One-click export to CSV, Parquet, or API; all queries saved as standard SQL |
| "Works with any data source" | So do we — 40+ native connectors vs. writing custom dbt models per source | Pre-built connectors with schema detection vs. 2-4 weeks per new source in dbt |

**Trap question:** "Ask how many hours per week your data engineers spend on pipeline maintenance vs. building new dashboards."

**Demo moment:** "Connect a Postgres database → see auto-generated dashboards with anomaly detection in 3 minutes. Their stack requires writing dbt models, testing, and building charts manually."

**ROI math:** DIY stack: Snowflake $2K/mo + 0.5 FTE data engineer ($5K/mo) + Metabase hosting ($300/mo) = $7,300/mo. Our $1,500/mo plan replaces all three. Saves $5,800/mo ($69,600/year).
```

### Example 3: Status Quo (Doing Nothing)

```markdown
### vs. Doing Nothing (Manual Process)

| Current State | What It Costs | What Changes |
|---------------|---------------|--------------|
| SDR manually researches each lead on LinkedIn | 30-45 min/lead x 20 leads/day = 10-15 hrs/day | Auto-enrichment runs in <5 seconds per lead |
| Copy-paste from 4 tools into CRM | 5 min/lead, error-prone | Single-click sync across all connected tools |
| Weekly pipeline review in spreadsheets | 3 hrs/week building reports nobody trusts | Real-time dashboard with auto-flagged at-risk deals |
| Manager reviews cold email drafts | 2 hrs/day approving and editing outreach | AI-generated sequences with manager-approved templates |

**Total cost of inaction:** $0/mo in software but 25+ hours/week in labor ($6,250/mo at $60/hr blended rate) plus missed pipeline from slow follow-up.

**Trap question:** "How many qualified leads per week does your team currently reach out to, and how many could they reach if research and writing took zero time?"
```

---

These examples show the format. Adapt row count, specificity, and tone to match the actual product and competitors found in the input documents.
