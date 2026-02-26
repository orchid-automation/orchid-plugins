# Outbound Sequence Templates

Per-persona outbound templates with personalization hooks, trigger-based emails, and cadence timing.

---

## Table of Contents

1. [Personalization Variables](#personalization-variables)
2. [Buyer Persona Sequences](#buyer-persona-sequences)
   - [Cold Email Sequence (5-Touch)](#buyer-cold-email-sequence)
   - [LinkedIn Messages](#buyer-linkedin-messages)
   - [Subject Line Bank](#buyer-subject-line-bank)
3. [User Persona Sequences](#user-persona-sequences)
   - [Cold Email Sequence (5-Touch)](#user-cold-email-sequence)
   - [LinkedIn Messages](#user-linkedin-messages)
   - [Subject Line Bank](#user-subject-line-bank)
4. [Champion Persona Sequences](#champion-persona-sequences)
   - [Cold Email Sequence (5-Touch)](#champion-cold-email-sequence)
   - [LinkedIn Messages](#champion-linkedin-messages)
   - [Subject Line Bank](#champion-subject-line-bank)
5. [Trigger-Based Email Templates](#trigger-based-email-templates)
   - [Funding Announcement](#funding-announcement)
   - [Hiring Surge](#hiring-surge)
   - [Tech Adoption](#tech-adoption)
   - [Competitor Switch](#competitor-switch)
6. [Breakup Email Variations](#breakup-email-variations)
7. [Follow-Up Cadence](#follow-up-cadence)

---

## Personalization Variables

Use these placeholders throughout all templates. Replace with real data from ICP research and target account intel.

| Variable | Description | Example |
|----------|-------------|---------|
| `{{company}}` | Target company name | Acme Corp |
| `{{name}}` | Contact's first name | Sarah |
| `{{pain_point}}` | Persona-specific pain from ICP | "spending 20 hours/week on manual reporting" |
| `{{competitor}}` | Their current solution | Competitor X |
| `{{trigger_event}}` | Recent event creating urgency | "your Series B announcement" |
| `{{industry}}` | Target company's industry | fintech |
| `{{title}}` | Contact's job title | VP of Engineering |
| `{{metric}}` | Relevant performance number | "40% faster deployment cycles" |
| `{{proof_point}}` | Specific claim with evidence | "cut onboarding from 6 weeks to 3 days" |
| `{{value_prop}}` | Persona-specific value prop from positioning | "eliminate manual reconciliation entirely" |
| `{{cta_asset}}` | The specific thing you're offering | "a 3-minute benchmark comparing your stack" |

---

## Buyer Persona Sequences

The buyer signs the check. They care about ROI, risk reduction, and competitive advantage. Speak in dollars, percentages, and business outcomes.

### Buyer Cold Email Sequence

#### Touch 1: Pain Hook (Day 1)

**Subject:** {{pain_point}} at {{company}}?

{{name}},

Most {{title}}s in {{industry}} tell me the same thing -- {{pain_point}}.

The ones who fixed it did one thing differently: they stopped treating it as an ops problem and started treating it as a tooling problem.

We built the fix. {{proof_point}}.

I put together {{cta_asset}} for {{company}}. Worth 3 minutes of your time?

---

#### Touch 2: Insight Drop (Day 3)

**Subject:** What {{industry}} teams miss about {{pain_point}}

{{name}},

Quick data point: teams that {{value_prop}} see an average of {{metric}} improvement in the first 90 days.

The reason most {{industry}} companies still struggle with {{pain_point}} is they're patching the symptom, not the cause.

Here's a one-page breakdown of what the fix actually looks like for a team your size. Want me to send it over?

---

#### Touch 3: Social Proof (Day 7)

**Subject:** How a {{industry}} team solved this

{{name}},

A team similar to {{company}} -- same size, same stack, same problem with {{pain_point}} -- switched their approach 6 months ago.

Result: {{proof_point}}.

They were using {{competitor}} before. The switch took less than a week.

Happy to share what they did differently. Takes 10 minutes to walk through.

---

#### Touch 4: Competitor Angle (Day 12)

**Subject:** {{competitor}} vs. the alternative

{{name}},

If {{company}} is using {{competitor}}, you've probably noticed {{pain_point}}.

The gap most teams find: {{competitor}} does X well but falls short on Y. That gap costs the average {{industry}} team Z hours per week.

We built specifically for that gap. {{proof_point}}.

I can show you a side-by-side in 10 minutes -- no pitch, just the comparison. Interested?

---

#### Touch 5: Direct Ask (Day 18)

**Subject:** 15 minutes, {{name}}?

{{name}},

I've sent a few notes about {{pain_point}} at {{company}}. I'll keep this one short.

If this is a problem worth solving this quarter, I'd like 15 minutes to show you how we address it. {{proof_point}} -- and I can prove it with {{cta_asset}}.

If the timing's off, no worries. Just let me know and I'll follow up next quarter instead.

---

### Buyer LinkedIn Messages

**Connection Request (under 300 chars):**

{{name}}, I work with {{title}}s in {{industry}} solving {{pain_point}}. Saw {{company}} is growing fast -- would love to connect and share a benchmark I put together for teams your size.

**Follow-Up After Connection (Day 5):**

Thanks for connecting, {{name}}. I mentioned a benchmark for {{industry}} teams -- here's the short version: teams that {{value_prop}} see {{metric}} improvement. Happy to send the full breakdown if useful.

**Post-Engagement DM (after they like/comment on a post):**

Appreciate the engagement on that post, {{name}}. Since {{company}} is in {{industry}}, thought you might find this relevant -- {{cta_asset}}. Want me to send it over?

---

### Buyer Subject Line Bank

1. {{pain_point}} at {{company}}?
2. Quick question about {{company}}'s {{pain_point}}
3. {{metric}} -- how {{industry}} teams are doing it
4. The {{competitor}} gap most teams don't see
5. {{name}}, 15 minutes this week?
6. What I'd tell {{company}}'s board about {{pain_point}}
7. {{company}} + {{pain_point}} -- one idea
8. Why {{industry}} teams are ditching {{competitor}}

---

## User Persona Sequences

The user works with the product daily. They care about workflow speed, reliability, and reducing tedium. Speak in hours saved, steps eliminated, and frustration removed.

### User Cold Email Sequence

#### Touch 1: Workflow Pain (Day 1)

**Subject:** That {{pain_point}} thing

{{name}},

Are you still {{pain_point}}? Most {{title}}s I talk to in {{industry}} spend way too many hours on this.

We automate the entire workflow. {{proof_point}}.

I built {{cta_asset}} -- it takes 2 minutes to see if it applies to your setup. Want the link?

---

#### Touch 2: How It Works (Day 3)

**Subject:** How {{industry}} {{title}}s are fixing {{pain_point}}

{{name}},

Three things that change when you stop {{pain_point}} manually:

1. You get back ~{{metric}} per week
2. The error rate drops to near-zero
3. You stop being the bottleneck for the rest of the team

Here's a 90-second walkthrough of what the workflow looks like after the switch. Interested?

---

#### Touch 3: Before/After (Day 7)

**Subject:** Before vs. after fixing {{pain_point}}

{{name}},

Before: {{pain_point}}, manual steps, waiting on other teams.
After: {{value_prop}}, automated, self-serve.

A {{title}} at a similar {{industry}} company told me the biggest surprise wasn't the time saved -- it was how much less stressful the work became.

Want to see a sandbox with your use case pre-loaded? Takes 5 minutes.

---

#### Touch 4: Technical Proof (Day 12)

**Subject:** Under the hood -- how it handles {{pain_point}}

{{name}},

If you're evaluating tools for {{pain_point}}, here's what matters technically:

- Integrates with your existing stack (no rip-and-replace)
- Handles edge cases that {{competitor}} misses
- Setup takes hours, not weeks

{{proof_point}}. Happy to give you sandbox access so you can test it yourself. No sales call required.

---

#### Touch 5: Free Trial (Day 18)

**Subject:** Try it, {{name}} -- no call needed

{{name}},

I know {{title}}s prefer to test things themselves rather than sit through demos.

Here's a free trial link with your use case pre-configured: [link]. Takes 5 minutes to see if it solves {{pain_point}} for {{company}}.

If you have questions, I'm here. If not, the product speaks for itself.

---

### User LinkedIn Messages

**Connection Request (under 300 chars):**

{{name}}, I build tools for {{title}}s dealing with {{pain_point}}. No pitch -- just thought you'd find our approach interesting given what {{company}} is doing in {{industry}}.

**Follow-Up After Connection (Day 5):**

Thanks for connecting. I know {{pain_point}} is a daily grind for {{title}}s. We built something that cuts that workflow down to minutes. Happy to share sandbox access if you want to test it.

---

### User Subject Line Bank

1. That {{pain_point}} thing
2. {{title}}s shouldn't have to {{pain_point}}
3. 5-minute fix for {{pain_point}}
4. Your {{pain_point}} workflow, automated
5. Sandbox access -- see it yourself
6. How {{title}}s at {{industry}} companies fixed this
7. {{pain_point}}: before vs. after
8. Free trial, no call required

---

## Champion Persona Sequences

The champion fights for the product internally. They need ammunition to sell upward. Speak in terms of internal credibility, ROI justification, and easy wins they can present to leadership.

### Champion Cold Email Sequence

#### Touch 1: Arm the Champion (Day 1)

**Subject:** Ammo for your {{pain_point}} business case

{{name}},

You probably already know {{company}} needs to fix {{pain_point}}. The hard part isn't finding the solution -- it's getting budget approved.

I built a one-page business case template that {{title}}s in {{industry}} are using to get sign-off. It includes the ROI math, risk analysis, and a 90-day rollout plan.

Want me to send it over? No strings attached.

---

#### Touch 2: Internal Selling Kit (Day 3)

**Subject:** The deck that got {{industry}} teams funded

{{name}},

When a {{title}} at a similar {{industry}} company pitched this internally, they led with three numbers:

- Cost of {{pain_point}} today: $X/month
- Cost after the fix: $Y/month
- Time to value: Z days

Their CFO approved it in one meeting. I have the framework they used -- happy to customize it for {{company}}'s numbers.

---

#### Touch 3: Objection Pre-Handling (Day 7)

**Subject:** What your CTO will ask about {{pain_point}}

{{name}},

Every time a {{title}} brings this to leadership, they get the same three questions:

1. "What about {{competitor}}?" -- here's why teams are switching
2. "How long is migration?" -- average is X days, not months
3. "What if it breaks?" -- {{proof_point}}

I put together a one-page FAQ that answers all three with data. Want it?

---

#### Touch 4: Comparison Doc (Day 12)

**Subject:** {{competitor}} vs. us -- the honest comparison

{{name}},

If you're building a case to move off {{competitor}} (or evaluating alongside it), here's a side-by-side comparison I put together for {{industry}} teams.

No spin. Includes where {{competitor}} is actually better, where we win, and what the switch costs.

Most {{title}}s share this with their buying committee. Want the doc?

---

#### Touch 5: ROI Calculator (Day 18)

**Subject:** ROI calculator for {{company}}

{{name}},

I built an ROI calculator pre-loaded with {{industry}} benchmarks. Plug in {{company}}'s numbers and it generates the business case automatically.

Takes 3 minutes. Gives you a PDF you can drop into your next budget review.

Link here: [link]. Let me know if you want me to walk through the assumptions.

---

### Champion LinkedIn Messages

**Connection Request (under 300 chars):**

{{name}}, I help {{title}}s build internal business cases for solving {{pain_point}}. Have a one-page ROI template that's worked well for {{industry}} teams. Happy to share.

**Follow-Up After Connection (Day 5):**

Appreciate the connection, {{name}}. That ROI template I mentioned -- I just updated it with {{industry}}-specific benchmarks. Want me to send it? No pitch, just the math.

---

### Champion Subject Line Bank

1. Ammo for your {{pain_point}} business case
2. The ROI math on fixing {{pain_point}}
3. What your CFO will ask (and the answers)
4. Internal pitch template for {{company}}
5. {{competitor}} vs. us -- honest comparison
6. How {{title}}s get budget for this
7. One-page business case for {{pain_point}}
8. ROI calculator, pre-loaded for {{industry}}

---

## Trigger-Based Email Templates

Send these when a specific event creates urgency. These override the regular cadence -- pause the sequence for 5 days after sending a trigger email.

### Funding Announcement

**Subject:** Congrats on the round, {{name}}

{{name}},

Saw {{company}} just closed {{trigger_event}}. Congrats -- that's a big milestone for the team.

Most {{industry}} companies at your new stage hit the same scaling wall: {{pain_point}} gets worse with headcount, not better.

The teams that fix it pre-scale save 3-6 months of pain later. I have a quick playbook for post-funding {{industry}} teams -- want it?

---

### Hiring Surge

**Subject:** Noticed {{company}} is hiring {{title}}s

{{name}},

{{company}} has {{trigger_event}} -- looks like {{pain_point}} is getting real.

Here's what I've seen: hiring more people to manage a broken process just makes the process more expensive. The teams that scale well fix the tooling first, then hire.

We helped a similar {{industry}} team do exactly that. {{proof_point}}.

Worth a 10-minute look before the new hires start?

---

### Tech Adoption

**Subject:** {{company}} + [new tech] -- one thought

{{name}},

Saw {{company}} is adopting {{trigger_event}}. Smart move for {{industry}}.

One thing teams discover after that switch: {{pain_point}} gets amplified because the new stack exposes gaps in the old workflow.

We integrate natively with [new tech] and solve that exact gap. {{proof_point}}.

Want to see how it plugs in? Takes 5 minutes.

---

### Competitor Switch

**Subject:** Leaving {{competitor}}? Here's what to know

{{name}},

Heard {{company}} might be moving away from {{competitor}}. If that's true, you're not alone -- we've seen a wave of {{industry}} teams making the same move.

The common reasons: {{pain_point}}, pricing surprises, and missing features on the roadmap.

I put together a migration checklist specifically for teams leaving {{competitor}}. Covers data export, timeline, and the gaps to watch for.

Want the checklist?

---

## Breakup Email Variations

Send one of these as the final touch (Day 25). Pick the variation that fits the situation.

### Variation 1: Graceful Close

**Subject:** Closing the loop, {{name}}

{{name}},

I've reached out a few times about {{pain_point}} at {{company}}. I don't want to be noise in your inbox.

Three possibilities:
1. Bad timing -- happy to check back in [Q+1]
2. Wrong person -- point me to the right one and I'll stop bugging you
3. Not a priority -- totally fair, I'll close this out

Either way, no hard feelings. The door's open whenever {{pain_point}} becomes urgent.

---

### Variation 2: Value Leave-Behind

**Subject:** One last thing for {{company}}

{{name}},

Last email from me. Before I go, I wanted to leave you with something useful regardless of whether we talk:

[Link to relevant resource: benchmark report, ROI template, or industry playbook]

It covers how {{industry}} teams are solving {{pain_point}} -- no pitch, just the data.

If {{company}} ever needs help with this, you know where to find me.

---

### Variation 3: Direct and Short

**Subject:** Should I stop reaching out?

{{name}},

I've sent a few emails about {{pain_point}}. If it's not relevant, just reply "stop" and I will.

If the timing is just off, reply "later" and I'll check back in 3 months.

Either way -- I respect your inbox.

---

## Follow-Up Cadence

### Standard Sequence Timing

| Touch | Day | Channel | Type | Purpose |
|-------|-----|---------|------|---------|
| 1 | 1 | Email | Cold open | Hook with pain or trigger |
| 2 | 3 | Email | Value add | Share insight, data, or proof |
| 3 | 5 | LinkedIn | Connection | Request with context |
| 4 | 7 | Email | Social proof | Show what others achieved |
| 5 | 12 | Email | Competitor angle | Position against their current tool |
| 6 | 18 | Email | Direct ask | Clear proposal with deadline |
| 7 | 25 | Email | Breakup | Graceful close with open door |

### Trigger Override Rules

- If a trigger event fires during an active sequence, **pause the sequence**
- Send the trigger-based email immediately
- Wait 5 days, then resume the sequence where you left off
- If the trigger fires after Touch 5, skip to breakup and use Variation 2 (value leave-behind)

### Re-Engagement Rules

- After a breakup with no reply: wait 90 days, then restart with Touch 1 using new pain data
- After a "later" reply: wait the requested time, then send a fresh Touch 1 referencing the previous conversation
- After any reply (even negative): respond personally, do not automate the follow-up

### Cadence by Persona Priority

| Persona | Start With | Frequency | Total Touches |
|---------|-----------|-----------|---------------|
| Buyer | Email | 7 touches over 25 days | 7 |
| User | Email or LinkedIn | 7 touches over 25 days | 7 |
| Champion | Email with asset | 7 touches over 25 days | 7 |

When targeting the same company with multiple personas, stagger sequences by 3-5 days. Never hit buyer and champion on the same day.
