---
name: outbound
description: Build ABM target account lists and personalized cold email sequences from ICP and positioning strategy. Researches companies matching ICP signals via web search, filters by tech stack and hiring patterns, and generates per-persona outbound sequences with trigger-based emails.
user-invocable: true
disable-model-invocation: true
allowed-tools: Read, Glob, Grep, Bash, Write, Edit, WebSearch, WebFetch
---

# Outbound: ABM Target Lists & Personalized Sequences

Build an ABM target list and per-persona outbound sequences. Write all output to `docs/gtm/outbound/`.

For sequence templates, see [sequence-templates.md](references/sequence-templates.md).

---

## Inputs

Read these files before doing anything else:

1. **`docs/gtm/02-market.md`** -- ICP (company profile, persona map), competitive landscape, market sizing
2. **`docs/gtm/03-position.md`** -- value propositions (per persona), battle cards, messaging pillars, objection map

<critical_requirement>
Both files must exist and contain real data. If either is missing or empty, stop immediately and report the error. Do not fabricate ICP or positioning data.
</critical_requirement>

---

## Phase 1: Extract ICP Signals

From `02-market.md`, extract:

- **Company profile**: industry, revenue range, employee count, stage, tech maturity
- **Persona map**: buyer, user, champion -- titles, pains, language, objections
- **Competitor landscape**: who they currently use (these are replacement targets)

From `03-position.md`, extract:

- **Value props per persona**: what each persona hears
- **Battle card counters**: how to position against each competitor
- **Messaging pillars**: claims + proof points to weave into sequences

---

## Phase 2: Build ABM Target List

### Research Strategy

Use WebSearch to find companies matching ICP signals. Run searches for:

1. **Tech stack signals**: companies using competitors identified in `02-market.md`
   - `"[competitor] alternative" site:reddit.com OR site:g2.com`
   - `"switching from [competitor]" [industry]`
2. **Hiring signals**: job postings that reveal pain
   - `"[pain-related job title]" hiring [industry]`
   - Job posts for roles your product replaces or augments
3. **Funding signals**: recently funded companies in target segment
   - `"series [A/B/C]" [industry] funding [current year]`
4. **Tech adoption signals**: companies adopting adjacent technologies
   - `"[related tech]" [industry] case study`
5. **Competitor reviews**: unhappy users of competitors
   - `"[competitor]" review site:g2.com OR site:capterra.com`

### Filtering Criteria

For each candidate company, verify at least 3 of these signals:

| Signal | How to Check |
|--------|-------------|
| Industry match | Company description matches ICP industry |
| Revenue/size range | Employee count or funding stage aligns |
| Tech stack fit | Uses technologies that indicate need |
| Hiring for pain | Job posts reveal the problem you solve |
| Uses competitor | Currently paying for an inferior solution |
| Recent trigger | Funding, leadership change, expansion, or tech migration |

### Target List Size

Research **15-25 target accounts**. Quality over quantity. Each account needs enough context for personalized outreach.

---

## Phase 3: Build Personalized Sequences

For each persona from the ICP (buyer, user, champion), generate a complete outbound sequence using positioning from `03-position.md`.

### What to Generate Per Persona

1. **5-touch cold email sequence** using AIDA framework
2. **LinkedIn connection request** message
3. **Trigger-based emails** for: funding announcement, hiring surge, tech adoption, competitor switch
4. **Breakup email** (final touch)
5. **Subject line bank** (5-8 subject lines per persona)

### Personalization Rules

- Reference the prospect's actual company, role, and pain
- Use the persona-specific value prop from `03-position.md`
- Weave in battle card counters when the prospect uses a known competitor
- Match the persona's language from `02-market.md` (how they describe their own pain)
- Keep emails under 125 words. No fluff, no buzzwords.

<critical_requirement>
Every email must have a clear, single CTA. Never ask for a "quick chat" -- propose a specific value exchange: a relevant insight, a benchmark, a comparison, or a free audit.
</critical_requirement>

---

## Output Format

Create the `docs/gtm/outbound/` directory if it does not exist. Write these files:

### File 1: `docs/gtm/outbound/target-accounts.md`

```markdown
# ABM Target Accounts

> {X} accounts researched, {Y} qualified based on ICP fit from 02-market.md

**Generated:** {YYYY-MM-DD}
**ICP match criteria:** {1-line summary of target company profile}

---

## Tier 1: High Fit (strong signal match)

### {Company Name}

| Attribute | Detail |
|-----------|--------|
| Industry | {industry} |
| Size | {employee count or range} |
| Stage | {seed/A/B/C/growth/public} |
| Current solution | {competitor or manual process} |
| ICP signals matched | {list which signals: tech stack, hiring, funding, etc.} |
| Trigger event | {what happened recently that creates urgency} |
| Key pain | {the specific problem, in their language} |
| Target persona | {title of the person to contact} |
| Source | {where you found this info} |

**Outreach angle:** {1-2 sentences on how to open the conversation}

---

{Repeat for each Tier 1 account}

## Tier 2: Medium Fit (partial signal match)

{Same format, fewer accounts}

---

## Research Notes

- Search queries used: {list the searches that found results}
- Total companies evaluated: {N}
- Qualification rate: {qualified / evaluated}
- Common patterns: {what Tier 1 accounts have in common}
```

### File 2: `docs/gtm/outbound/sequences/buyer-sequence.md`

```markdown
# Outbound Sequence: {Buyer Persona Title}

> Pain: {their primary pain from 02-market.md}
> They hear: "{value prop from 03-position.md}"

---

## Subject Line Bank

1. {subject line 1}
2. {subject line 2}
3. {subject line 3}
4. {subject line 4}
5. {subject line 5}

---

## 5-Touch Cold Email Sequence

### Email 1: Open (Day 1)
**Subject:** {subject}
**Framework:** Attention -- hook with a pain or trigger

{email body, under 125 words}

**CTA:** {specific value exchange}

---

### Email 2: Value (Day 3)
**Subject:** {subject}
**Framework:** Interest -- share an insight or proof point

{email body}

**CTA:** {specific value exchange}

---

### Email 3: Social Proof (Day 7)
**Subject:** {subject}
**Framework:** Desire -- show what others achieved

{email body}

**CTA:** {specific value exchange}

---

### Email 4: Competitor Angle (Day 12)
**Subject:** {subject}
**Framework:** Battle card counter from 03-position.md

{email body}

**CTA:** {specific value exchange}

---

### Email 5: Direct Ask (Day 18)
**Subject:** {subject}
**Framework:** Action -- clear, direct proposal

{email body}

**CTA:** {specific next step}

---

## LinkedIn Connection Request

{connection message, under 300 characters}

---

## Trigger-Based Emails

### Funding Announcement
**Subject:** {subject}
**Send when:** Company announces new funding round

{email body referencing the funding event}

### Hiring Surge
**Subject:** {subject}
**Send when:** 3+ job posts for roles related to the pain you solve

{email body referencing their hiring}

### Tech Adoption
**Subject:** {subject}
**Send when:** Company adopts a technology adjacent to your product

{email body referencing the tech decision}

### Competitor Switch
**Subject:** {subject}
**Send when:** Company shows signs of leaving a competitor

{email body positioning against the competitor using battle card}

---

## Breakup Email

**Subject:** {subject}
**Send:** Day 25 (final touch)

{email body, graceful close with open door}
```

### File 3: `docs/gtm/outbound/sequences/user-sequence.md`

Same structure as buyer sequence, but:
- Pain and value prop are the **user persona's** from `02-market.md` and `03-position.md`
- Emails emphasize daily workflow improvement, not ROI
- CTAs offer demos, free trials, or sandbox access instead of meetings
- Language is more technical, less executive

### File 4: `docs/gtm/outbound/sequences/champion-sequence.md`

Same structure as buyer sequence, but:
- Pain and value prop are the **champion persona's** from `02-market.md` and `03-position.md`
- Emails arm the champion with internal selling ammunition
- CTAs offer comparison docs, ROI calculators, and internal pitch decks
- Language helps them sell up to the buyer

---

## Follow-Up Cadence

All sequences follow this timing:

| Touch | Day | Type | Purpose |
|-------|-----|------|---------|
| 1 | 1 | Cold email | Open with pain/trigger |
| 2 | 3 | Email | Deliver value/insight |
| 3 | 5 | LinkedIn | Connection request |
| 4 | 7 | Email | Social proof |
| 5 | 12 | Email | Competitor angle |
| 6 | 18 | Email | Direct ask |
| 7 | 25 | Email | Breakup |

Trigger-based emails override the sequence -- if a trigger fires, send the trigger email and pause the cadence for 5 days.

---

## Quality Checks Before Writing

- Every target account has at least 3 ICP signals verified
- Every email is under 125 words
- Every email has a single, specific CTA (no "quick chat")
- Persona-specific value props match `03-position.md` exactly
- Battle card angles match competitor counters from `03-position.md`
- No buzzwords: no "leverage," "synergy," "robust," "cutting-edge," "best-in-class"
- Subject lines are under 50 characters
- LinkedIn messages are under 300 characters
- Trigger emails reference the specific trigger event, not generic outreach
- All personalization placeholders are filled with real data from research
