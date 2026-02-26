# Cold Email Frameworks

Vendored reference for the `/gtm:activate` skill. Use these templates when generating `cold-sequence.md`. Build the sequence from the ICP personas in `02-market.md` and battle cards in `03-position.md`.

---

## Table of Contents

- [5-Touch Cold Email Sequence](#5-touch-cold-email-sequence)
- [AIDA Applied to Cold Email](#aida-applied-to-cold-email)
- [Subject Line Formulas](#subject-line-formulas)
- [Personalization Hooks](#personalization-hooks)
- [Follow-Up Cadence](#follow-up-cadence)
- [Breakup Email Template](#breakup-email-template)

---

## 5-Touch Cold Email Sequence

Each touch has a distinct purpose and angle. Never repeat the same pitch twice.

### Touch 1: Value-First Intro (Day 0)

**Purpose:** Establish relevance. Show you understand their world. Offer value without asking.

**Structure:**
```
Subject: [Personalization hook -- see formulas below]

Hi [First Name],

[One sentence connecting to their specific situation -- trigger event,
company signal, or role-specific pain.]

[One sentence about the problem you solve. Use their language from
02-market.md persona map, not product jargon.]

[One sentence of proof -- a specific metric, customer result, or
comparison that makes the claim credible.]

[Soft CTA -- ask for interest, not a meeting.]

[Your name]
```

**Example:**
```
Subject: Quick question about [Company]'s outbound setup

Hi Sarah,

Noticed [Company] just opened 3 SDR roles -- congrats on the growth.
Scaling outbound usually means scaling the tool chaos too.

Most sales teams we talk to spend 4+ hours/day on admin work that
has nothing to do with selling.

We helped Ramp's SDR team cut that to 23 minutes/day and book 3x
more meetings from the same headcount.

Worth a look? Happy to share how it works.

Alex
```

### Touch 2: Pain + Proof Point (Day 3)

**Purpose:** Dig into a specific pain from the persona map. Back it up with evidence.

**Structure:**
```
Subject: Re: [Previous subject] OR [New pain-specific subject]

Hi [First Name],

[Name a specific problem they face -- pulled from 02-market.md
persona pains. Be concrete, not generic.]

[Agitate: what this costs them. Time, money, missed opportunities.
Use specific numbers if available from 03-position.md.]

[One proof point from battle cards. "Companies like [peer] solved
this by..." or "Teams using [Product] see [metric]".]

[Direct CTA -- "worth 15 minutes?" or "want me to show you the
math?"]

[Your name]
```

### Touch 3: Competitor Comparison (Day 7)

**Purpose:** If they use a known competitor, differentiate. If not, compare to the status quo (manual process, spreadsheets, nothing).

**Structure:**
```
Subject: [Product] vs. [their current approach]

Hi [First Name],

[If they use a competitor: "Saw you're using [Competitor]. Solid
tool for [what it does well]. Most teams outgrow it when [specific
limitation from battle cards]."]

[If no competitor: "Most [ICP title]s handle this with [manual
approach]. It works until [breaking point]."]

[Two-line comparison: what they get today vs. what they'd get. Pull
directly from the battle card "Their Claim / Our Counter" rows.]

[Specific CTA: "I can show you the side-by-side in 10 minutes."]

[Your name]
```

### Touch 4: ROI / Case Study (Day 14)

**Purpose:** Make the business case. Show the math or tell a customer story.

**Structure:**
```
Subject: How [similar company] [achieved specific result]

Hi [First Name],

[Brief customer story or ROI calculation. Use replacement cost data
from 01-scan.md and pricing from 03-position.md.]

[The "before" state: what the customer was doing, what it cost them.]

[The "after" state: specific metrics after using your product.]

[The time to value: how fast they got results.]

[CTA: offer to walk through the ROI math for their specific
situation.]

[Your name]
```

### Touch 5: Breakup (Day 21)

**Purpose:** Create urgency through finality. Respectful close that leaves the door open.

See the [Breakup Email Template](#breakup-email-template) section below.

---

## AIDA Applied to Cold Email

Adapt the AIDA framework for the constraints of cold email: short, scannable, one CTA.

### Cold Email AIDA Rules

| Stage | Cold Email Constraint | Max Length |
|-------|----------------------|-----------|
| **Attention** | Subject line + first sentence. Must earn the second sentence. | 1 sentence |
| **Interest** | Connect to THEIR problem, not your product. Use persona language. | 1-2 sentences |
| **Desire** | Proof point or specific result. One metric, one customer, one comparison. | 1-2 sentences |
| **Action** | One CTA. Low friction. Never "book a 30-min demo." | 1 sentence |

### Total email length

- **Target:** 75-125 words
- **Absolute max:** 150 words
- **Formatting:** Short paragraphs (1-2 sentences each). White space between paragraphs. No bullet lists in touch 1.

### What to avoid

- Opening with "I" ("I wanted to reach out..." -- delete this)
- Opening with "Hope you're well" (wastes the most valuable line)
- Mentioning your company name before the value prop
- More than one link per email
- More than one CTA per email
- Attachments (triggers spam filters)
- HTML formatting in the first touch (plain text converts better)

---

## Subject Line Formulas

Keep under 50 characters. No ALL CAPS. No exclamation marks. Aim for curiosity or relevance.

### Formula 1: The Question

`[Thing about their company]?`

- "scaling outbound this quarter?"
- "[Company]'s data pipeline"

### Formula 2: The Mutual Connection

`[Name] suggested I reach out`

- "Sarah from Ramp suggested we chat"
- "Saw your talk at SaaStr"

### Formula 3: The Trigger Event

`congrats on [recent event]`

- "congrats on the Series B"
- "saw the new VP Sales hire"

### Formula 4: The Metric

`[surprising number] re: [their problem]`

- "68% re: SDR admin time"
- "$47K re: manual data entry"

### Formula 5: The Comparison

`[product] vs. [their current approach]`

- "automation vs. 3 more SDR hires"
- "[Product] vs. doing it manually"

### Formula 6: The Peer Reference

`how [similar company] [did thing]`

- "how Ramp cut outbound setup by 80%"
- "how Notion ships landing pages same-day"

### Formula 7: The Quick Ask

`quick question about [topic]`

- "quick question about [Company]'s GTM"
- "quick question re: outbound tooling"

### Subject line rules

1. Lowercase first letter (looks like a real email, not marketing)
2. No brackets or [COMPANY] tokens in the actual send -- fill everything in
3. A/B test two variants when possible
4. Thread the follow-ups: "Re: [original subject]" for touches 2-3, new subjects for 4-5
5. Never use "follow up" as a subject -- it signals low value

---

## Personalization Hooks

Generic emails get ignored. Every email needs at least one personalization signal. Sources ranked by conversion impact:

### Tier 1: Trigger Events (highest response rates)

| Signal | Where to Find | How to Use |
|--------|--------------|-----------|
| New funding round | Crunchbase, press releases | "Congrats on the raise. Most teams scaling from [stage] hit [problem] around month 3." |
| New exec hire | LinkedIn, press releases | "Saw you just hired a [VP title]. Usually means [initiative] is a priority." |
| Job postings | Company careers page | "You're hiring 5 SDRs -- that usually means outbound is working but not scaling." |
| Product launch | Product Hunt, company blog | "Saw the launch of [feature]. How's the go-to-market side going?" |
| Bad quarter / layoffs | News, SEC filings | Handle carefully. "Sounds like efficiency is top of mind. Here's how [peer] did more with less." |

### Tier 2: Company Signals

| Signal | Where to Find | How to Use |
|--------|--------------|-----------|
| Tech stack | BuiltWith, job posts, GitHub | "Noticed you're on [technology]. Most [tech] teams run into [specific problem]." |
| Company size / stage | LinkedIn, Crunchbase | Match the pain to their stage. Seed-stage vs. Series C problems are different. |
| Industry vertical | Company website | Use industry-specific language and benchmarks. |
| Competitor usage | G2, review sites, case studies | "Teams that outgrow [competitor] usually do so because of [limitation]." |

### Tier 3: Personal Signals

| Signal | Where to Find | How to Use |
|--------|--------------|-----------|
| LinkedIn post | LinkedIn | "Loved your post about [topic]. We see the same thing with our customers." |
| Conference talk | YouTube, event sites | "Caught your talk at [event] about [topic]." |
| Mutual connection | LinkedIn | Reference by name in subject line (with permission). |
| Career history | LinkedIn | "Coming from [previous company], you probably know [shared context]." |

### Personalization rules

1. **One hook per email.** Do not stack 3 personalization signals -- it looks stalkerish.
2. **First sentence only.** Personalization goes in the opening. Then move to value.
3. **If you can't personalize, don't fake it.** A generic-but-relevant email beats a forced "I see you breathe oxygen too!"

---

## Follow-Up Cadence

### Recommended Timing

| Touch | Day | Purpose | Channel |
|-------|-----|---------|---------|
| 1 | Day 0 | Value-first intro | Email |
| 2 | Day 3 | Pain + proof | Email |
| 3 | Day 7 | Competitor comparison | Email |
| 4 | Day 14 | ROI / case study | Email |
| 5 | Day 21 | Breakup | Email |

### Cadence Rules

1. **Never send more than one email per day** to the same person
2. **Space touches 3-7 days apart** -- tighter early, wider later
3. **Thread touches 2-3** on the original email (Re: subject). New thread for touch 4-5
4. **Vary send times** -- if touch 1 was 9am Tuesday, touch 2 should be 2pm Friday
5. **Stop immediately** if they reply with "not interested" -- one respectful acknowledgment, then silence
6. **Restart the sequence** only if a new trigger event occurs (funding, new hire, etc.) -- minimum 60 days gap

### After the sequence

If all 5 touches get no response:
- Add to a monthly newsletter or content nurture list (if they didn't explicitly opt out)
- Set a 90-day reminder to check for new trigger events
- Never run the same 5-touch sequence twice on the same person

---

## Breakup Email Template

The breakup email uses reverse psychology and finality to prompt a response. It's consistently the highest-replied email in most sequences.

### Structure

```
Subject: closing the loop

Hi [First Name],

[Acknowledge you've reached out a few times without being
apologetic. One sentence.]

[Restate the core value prop in one sentence -- the single most
compelling reason to respond.]

[Give them an easy out that also leaves the door open.]

[Sign off -- shorter than usual.]

[Your name]
```

### Example

```
Subject: closing the loop

Hi Sarah,

I've reached out a few times and haven't heard back, so I'll
assume the timing isn't right.

If reducing your SDR admin time from 4 hours/day to 23 minutes
ever becomes a priority, the offer stands.

No hard feelings either way. I'll stop filling up your inbox.

Alex

P.S. If someone else on your team owns this, happy to be
redirected.
```

### Breakup email rules

1. **Never guilt trip.** "I've emailed 5 times and..." makes you the villain.
2. **Restate value, not features.** One sentence, outcome-focused.
3. **Provide a P.S. redirect.** Often the person you emailed isn't the decision maker. The P.S. gives them an easy way to point you to the right person without committing to anything.
4. **Actually stop.** If you send a breakup and then email again 2 weeks later, you destroy all credibility.
5. **Keep it under 75 words.** The shortest email in the sequence.
