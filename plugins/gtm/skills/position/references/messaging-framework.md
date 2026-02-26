# Messaging Framework

## Table of Contents

- [Building Messaging Pillars](#building-messaging-pillars)
- [Pillar Structure](#pillar-structure)
- [Headline Bank](#headline-bank)
- [Proof Point Pairing](#proof-point-pairing)
- [Words to USE vs NEVER USE](#words-to-use-vs-never-use)

---

## Building Messaging Pillars

Messaging pillars are the 3-5 claims your product can own. Every piece of marketing, sales conversation, and product description should reinforce one of these pillars.

### How to identify pillars

1. **Look at the market gaps from 02-market.md.** What nobody does well is your first pillar candidate.
2. **Look at the capability clusters from 01-scan.md.** Group features by the outcome they deliver, not the technology behind them. Each outcome cluster is a pillar candidate.
3. **Look at competitor weaknesses.** If every competitor is slow to set up, your pillar is speed. If they all charge for add-ons, your pillar is all-inclusive pricing.
4. **Filter to 3-5.** More than 5 pillars means you have not made choices. Cut the weakest. A pillar you cannot prove with specific evidence is not a pillar.

### Pillar selection criteria

Each pillar must pass three tests:

| Test | Question | Fail example |
|------|----------|-------------|
| Provable | Can you back this with a number, feature, or comparison? | "We care about customers" — no metric |
| Differentiating | Would a competitor hesitate to claim the same thing? | "Easy to use" — everyone says this |
| Relevant | Does the buyer persona in 02-market.md care about this? | "Built with Rust" — buyer does not care about implementation |

### Pillar count by product stage

- **Pre-PMF / MVP:** 2-3 pillars. You do not know enough yet.
- **Growth stage:** 3-4 pillars. Core identity is clear.
- **Mature product:** 4-5 pillars. Broader surface area, more claims to own.

---

## Pillar Structure

Every pillar follows this format:

```markdown
### Pillar {N}: {Theme}
- **Claim:** {One sentence. What you are asserting. Must be specific enough that a competitor could disagree.}
- **Proof:** {The evidence. A number, a feature name, a comparison, a customer result.}
- **One-liner:** "{A quotable version for landing pages, decks, and social. Under 15 words.}"
```

### Examples

```markdown
### Pillar 1: Speed to Value
- **Claim:** Teams go from signup to first results in under 15 minutes, with no implementation partner required.
- **Proof:** Self-serve onboarding flow with pre-built templates; median time-to-first-value is 11 minutes (internal analytics).
- **One-liner:** "Live in 15 minutes. No implementation partner. No training budget."

### Pillar 2: Replace the Stack
- **Claim:** One tool replaces 4-6 point solutions that together cost $3,000-8,000/mo.
- **Proof:** Built-in enrichment, sequencing, CRM sync, and analytics — each replacing a standalone tool (see replacement cost table in 03-position.md).
- **One-liner:** "One subscription instead of six invoices."

### Pillar 3: Intelligence, Not Templates
- **Claim:** AI that adapts to your data from day one, not rules engines that require 6 months of training data.
- **Proof:** Pre-trained on anonymized B2B patterns; personalization accuracy improves with each send (measured by reply rate uplift).
- **One-liner:** "AI that works on day one, not after six months of training."
```

### How pillars map to content

| Pillar | Landing page | Sales deck | Email sequence | Social post |
|--------|-------------|------------|----------------|-------------|
| Speed to Value | Hero section headline | Slide 3 (demo) | Email 1 hook | "We went live in..." story |
| Replace the Stack | Pricing section | ROI slide | Email 3 (cost comparison) | Replacement cost infographic |
| Intelligence | Feature section | Demo section | Email 2 (differentiation) | Before/after comparison |

---

## Headline Bank

Use these formulas to generate headlines for landing pages, ads, emails, and decks. Replace bracketed placeholders with specifics from the positioning document.

### Problem-first formulas

1. `Stop [painful activity]. Start [desired outcome].`
2. `[Pain point] is costing you [specific amount]. Here's the fix.`
3. `Your team spends [X hours/week] on [task]. What if it took [Y minutes]?`
4. `[X]% of [role]s say [pain point] is their #1 challenge.`
5. `The [old way] is broken. [New way] works.`

### Outcome-first formulas

6. `[Outcome] in [timeframe]. No [common barrier].`
7. `From [before state] to [after state] in [time].`
8. `[X] [metric] in [timeframe] — without [sacrifice].`
9. `The fastest way to [outcome] for [audience].`
10. `[Audience]: [outcome] without [pain].`

### Comparison formulas

11. `[Competitor] charges $[X] for [subset]. We include it at $[Y].`
12. `Everything [competitor] does, plus [thing they don't], at [fraction] of the price.`
13. `[Competitor] takes [X weeks] to set up. We take [Y minutes].`
14. `Switch from [old tool] and save [amount] in the first [timeframe].`
15. `Why [X] teams switched from [competitor] this quarter.`

### Social proof formulas

16. `[Company name] cut [metric] by [X]% with [product].`
17. `"[Customer quote — short, specific, from a real title]"`
18. `[X] teams use [product] to [outcome]. Here's why.`
19. `Rated [X]/5 on [platform] by [Y]+ [role]s.`
20. `[Company] went from [before] to [after]. In [timeframe].`

### Curiosity formulas

21. `What [X] [role]s know about [topic] that you don't.`
22. `The [X]-minute [task] that replaced our [expensive alternative].`
23. `We deleted [tool/process] and [metric] went up [X]%.`
24. `The real cost of [thing everyone accepts as normal].`

### How to use the bank

1. Pick 2-3 formulas per pillar.
2. Fill in specifics from 01-scan.md (capabilities), 02-market.md (personas, competitors, pricing), and 03-position.md (value props).
3. Write 3 variations of each. Pick the one that is most specific.
4. Test: read it aloud. If it sounds like it could be any product, rewrite.

---

## Proof Point Pairing

Every claim needs a proof point. Proof without a claim is a feature list. A claim without proof is a slogan.

### Proof point types (ranked by strength)

| Rank | Type | Example | When to use |
|------|------|---------|-------------|
| 1 | Customer result | "Acme Co reduced pipeline build time from 4 hours to 12 minutes" | When you have customer data or case studies |
| 2 | Direct comparison | "Our setup takes 15 min; theirs takes 2-6 weeks (per their own docs)" | When competitor data is public |
| 3 | Product metric | "Processes 10,000 leads/hour with <200ms response time" | When the capability is measurable |
| 4 | Replacement cost | "Replaces $4,200/mo in tools (Clay + Instantly + Apollo)" | When competitor pricing is known |
| 5 | Third-party validation | "SOC 2 Type II certified; rated 4.8/5 on G2" | When external credibility matters (enterprise) |
| 6 | Architectural fact | "Open-source core; no vendor lock-in; data exportable at any time" | When the buyer fears switching costs |

### Pairing methodology

For each claim in a messaging pillar:

1. **Find the strongest proof type available.** Use the ranking above.
2. **Be specific.** "Fast" is not proof. "11-minute median time to first result" is proof.
3. **Cite the source.** Where did this number come from? Internal analytics, G2 reviews, competitor pricing page, customer interview.
4. **Test the counter.** Could a competitor make the same claim with the same proof? If yes, find a different proof point.

### Pairing template

```
Claim: {What you assert}
Proof: {Evidence}
Source: {Where the evidence comes from}
Counter-test: {Could a competitor say the same?} → {Yes/No + why}
```

---

## Words to USE vs NEVER USE

### NEVER USE

These words signal that you have nothing specific to say. They are fillers. Cut them every time.

| Word | Why it fails |
|------|-------------|
| leverage | Means "use." Just say "use." |
| robust | Means nothing. What makes it robust? Say that instead. |
| scalable | Every SaaS product claims this. Quantify it or drop it. |
| seamless | Nothing is seamless. Name the specific integration or workflow. |
| cutting-edge | Self-congratulatory. The product proves itself through results. |
| best-in-class | Says "we are the best" without evidence. Prove it or remove it. |
| synergy | Banned since 2003. |
| holistic | Means "we do a lot of things." List them instead. |
| end-to-end | Acceptable only if you define both ends with specifics. |
| innovative | Let the product speak. If you have to say it, it probably is not. |
| empower | Corporate filler. Say what the person can now do. |
| transform | Overused. Describe the before and after instead. |
| disrupt | Let analysts say this about you. Never say it about yourself. |
| next-generation | Compared to what? Name the previous generation or drop it. |
| state-of-the-art | Academic term. Does not belong in sales copy. |

### USE INSTEAD

| Instead of... | Write... |
|---------------|----------|
| "Leverage AI to..." | "AI [specific action]: [specific result]" |
| "Robust platform" | "[X] uptime, handles [Y] requests/sec, recovers in [Z]ms" |
| "Scalable solution" | "Handles 100 to 100,000 [units] on the same plan" |
| "Seamless integration" | "Connects to [tool] in [X] minutes with [Y] clicks" |
| "End-to-end" | "From [first step] to [last step] in one tool" |
| "Empowers teams" | "Teams can now [specific action] without [previous blocker]" |
| "Transforms workflows" | "Before: [old process]. After: [new process]. Difference: [metric]." |

### Domain-specific word choices

Build a product-specific vocabulary list during positioning. Pull terms from:

- 02-market.md persona language ("what they say" fields)
- Competitor marketing pages (adopt their buyer's vocabulary, not their brand language)
- G2/Capterra reviews (how real users describe the problem)
- Job postings in the ICP (how companies describe the role responsible for this problem)

The goal: write in the buyer's language, not yours.
