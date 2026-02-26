# Orchid GTM Engine — Architecture & Design Document

> **Status**: Planning
> **Date**: 2026-02-25
> **Author**: Brandon Guerrero / Orchid Automation
> **Repo**: orchid-plugins (to be restructured)

---

## Vision

**Take any vibe-coded project and go to market the same day.**

The Orchid GTM Engine is a Claude Code plugin that scans any codebase, determines the best ICP, researches competitors and market opportunity, builds positioning and battle cards, generates landing pages and sales assets, and produces cold email sequences with ABM target lists — all automated, all from a single command.

```
/gtm:launch MyProduct
```

Nobody on the skills ecosystem has this. Individual pieces exist (copywriting, frontend design, cold email). The orchestration from code to market doesn't. That's the product.

---

## Table of Contents

1. [Current State](#1-current-state)
2. [The 6-Skill Architecture](#2-the-6-skill-architecture)
3. [How Skills Communicate (The File Protocol)](#3-how-skills-communicate-the-file-protocol)
4. [Plugin Directory Structure](#4-plugin-directory-structure)
5. [Runtime Flow](#5-runtime-flow)
6. [Skill Specifications](#6-skill-specifications)
7. [Custom Agents](#7-custom-agents)
8. [External Skills Integration (The Layer Cake)](#8-external-skills-integration-the-layer-cake)
9. [Reference Files (Vendored Knowledge)](#9-reference-files-vendored-knowledge)
10. [Design Rules From Official Docs](#10-design-rules-from-official-docs)
11. [Compound Engineering Patterns Applied](#11-compound-engineering-patterns-applied)
12. [What's Novel (Our Moat)](#12-whats-novel-our-moat)
13. [Build Order](#13-build-order)
14. [Open Questions](#14-open-questions)

---

## 1. Current State

The repo currently ships as `orchid-plugins` with two plugins:

| Plugin | What It Does | Status |
|--------|-------------|--------|
| `session` | `/session:vibecheck` — Git-based productivity analysis | Shipped v1.0.0 |
| `feature-map` | `/feature-map` — GTM codebase analysis with parallel agents | Shipped v1.0.0, needs rearchitect |

### Problems with current feature-map

| Issue | Impact |
|-------|--------|
| Phase 1 (codebase scan) runs inline | Bloats main context window |
| Agents spawned for ALL categories | Wastes tokens on empty categories (e.g., "AI/ML" agent when there's no ML code) |
| Each agent writes its own file | Fragmented output, no quality control |
| Uses `TeamCreate` (experimental API) | Not the stable, documented pattern |
| ICP + competitor research buried in Phase 1.5 | Should be its own dedicated phase with deep research |
| No quality validation | Buzzwords, missing replacement costs, and gaps slip through |
| 298-line SKILL.md loaded fully every time | Exceeds the "keep SKILL.md under 500 lines" best practice when methodology is included |
| No separation of concerns | One monolithic skill tries to do everything |

---

## 2. The 6-Skill Architecture

```
 SKILL 1                SKILL 2               SKILL 3
 /gtm:scan              /gtm:market           /gtm:position
 ─────────              ──────────            ────────────
 "What did we build?"   "Who cares?"          "Why us?"


 SKILL 4                SKILL 5               SKILL 6
 /gtm:activate          /gtm:outbound         /gtm:launch
 ──────────             ────────────          ──────────
 "Build the assets"     "Cold email & ABM"    "Full pipeline"
                                               (runs 1-5)
```

Each skill is standalone. Users can run any skill individually:

```
/gtm:scan              ← Just map the codebase
/gtm:market            ← Just do market research
/gtm:position          ← Just build positioning
/gtm:activate          ← Just generate assets
/gtm:outbound          ← Just build ABM lists
/gtm:launch            ← Run everything end-to-end
```

### Key architectural decisions

| Decision | Rationale |
|----------|-----------|
| Skills 1-5 use `context: fork` | Each runs as an isolated subagent, doesn't bloat main context |
| Skill 6 (`launch`) runs INLINE (no fork) | Keeps the Skill tool so it can invoke skills 1-5 sequentially |
| Each forked skill writes to `docs/gtm/*.md` | File-based communication between phases (forked skills have no chat history) |
| Custom agents define personas + tool access | Each phase gets a specialist agent type |
| Vendored reference files as fallbacks | Works even without external skills installed |
| `disable-model-invocation: true` on all skills | User-triggered only — you don't want Claude auto-running a market analysis |

---

## 3. How Skills Communicate (The File Protocol)

Forked skills have **no access to conversation history**. They communicate through files on disk:

```
/gtm:scan writes ──────→ docs/gtm/01-scan.md
                              │
/gtm:market reads ◄───────────┘
/gtm:market writes ─────→ docs/gtm/02-market.md
                              │
/gtm:position reads ◄────────┘ (also reads 01-scan.md)
/gtm:position writes ───→ docs/gtm/03-position.md
                              │
/gtm:activate reads ◄────────┘ (also reads 01 + 02)
/gtm:activate writes ───→ docs/gtm/assets/
                              │
/gtm:outbound reads ◄────────┘ (reads 02 + 03)
/gtm:outbound writes ───→ docs/gtm/outbound/
```

### Final output tree

```
docs/gtm/
├── 01-scan.md                 ← Feature inventory
├── 02-market.md               ← ICP + competitors + sizing
├── 03-position.md             ← Value props + battle cards
├── assets/
│   ├── landing-page.html      ← Deploy-ready page
│   ├── cold-sequence.md       ← Paste into outbound tool
│   ├── one-pager.md           ← Share with prospects
│   ├── objection-handler.md   ← Sales enablement
│   └── roi-calculator.md      ← Justify the purchase
└── outbound/
    ├── target-accounts.md     ← ABM list
    └── sequences/             ← Per-persona email sequences
```

---

## 4. Plugin Directory Structure

```
orchid-gtm/                              ← renamed from feature-map
├── .claude-plugin/
│   └── plugin.json
├── README.md
│
├── agents/                              ← CUSTOM AGENT PERSONAS
│   ├── market-researcher.md             ← ICP + competitor + sizing agent
│   ├── positioning-strategist.md        ← Strategy + battle cards agent
│   └── asset-generator.md               ← Copy + landing page agent
│
└── skills/
    │
    ├── scan/                            ─── PHASE 1 ───
    │   ├── SKILL.md                     context: fork, agent: Explore
    │   └── references/
    │       └── methodology.md           ← replacement cost framework
    │
    ├── market/                          ─── PHASE 2 ───
    │   ├── SKILL.md                     context: fork, agent: market-researcher
    │   └── references/
    │       ├── icp-framework.md         ← how to determine ICP
    │       └── competitor-analysis.md   ← competitive research playbook
    │
    ├── position/                        ─── PHASE 3 ───
    │   ├── SKILL.md                     context: fork, agent: positioning-strategist
    │   └── references/
    │       ├── battle-card-template.md  ← vs competitor format
    │       ├── messaging-framework.md   ← pillars + proof points
    │       └── pricing-patterns.md      ← tier structures + anchoring
    │
    ├── activate/                        ─── PHASE 4 ───
    │   ├── SKILL.md                     context: fork, agent: asset-generator
    │   └── references/
    │       ├── landing-page-patterns.md ← vendored (hero, social proof, CTA)
    │       ├── copywriting-patterns.md  ← vendored (AIDA, PAS, BAB)
    │       ├── headline-formulas.md     ← 20+ proven formulas
    │       └── cold-email-frameworks.md ← 5-touch sequence templates
    │
    ├── outbound/                        ─── PHASE 5 ───
    │   ├── SKILL.md                     context: fork, agent: general-purpose
    │   └── references/
    │       └── sequence-templates.md    ← per-persona outbound templates
    │
    └── launch/                          ─── ORCHESTRATOR ───
        └── SKILL.md                     NO FORK (inline), orchestrates 1-5
```

---

## 5. Runtime Flow

```
User: /gtm:launch MyProduct
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│  launch/SKILL.md loads INLINE (no fork)                      │
│  Claude keeps the Skill tool + conversation context          │
│                                                              │
│  Step 1: Claude invokes Skill("gtm:scan MyProduct")         │
│          ┌──────────────────────────────┐                    │
│          │ FORKED SUBAGENT (Explore)    │                    │
│          │ Scans entire codebase        │                    │
│          │ Maps all capabilities        │                    │
│          │ Counts endpoints, models,    │                    │
│          │   jobs, integrations         │                    │
│          │ Writes docs/gtm/01-scan.md   │                    │
│          │ Returns summary text         │──┐                 │
│          └──────────────────────────────┘  │                 │
│                                            ▼                 │
│  Step 2: Claude invokes Skill("gtm:market")                  │
│          ┌────────────────────────────────────┐              │
│          │ FORKED SUBAGENT (market-researcher) │             │
│          │ Reads docs/gtm/01-scan.md          │              │
│          │ Infers ICP from codebase signals    │             │
│          │ WebSearch + Perplexity for:         │              │
│          │   - Competitor landscape            │              │
│          │   - Market sizing (TAM/SAM/SOM)     │             │
│          │   - Pricing intelligence            │              │
│          │   - G2/Capterra sentiment           │             │
│          │ Writes docs/gtm/02-market.md       │              │
│          │ Returns summary text               │──┐           │
│          └────────────────────────────────────┘  │           │
│                                                  ▼           │
│  Step 3: Claude invokes Skill("gtm:position")                │
│          ┌──────────────────────────────────────────┐        │
│          │ FORKED SUBAGENT (positioning-strategist)  │       │
│          │ Reads 01-scan.md + 02-market.md          │        │
│          │ Synthesizes:                              │        │
│          │   - Value propositions (per persona)      │       │
│          │   - Battle cards (per competitor)          │       │
│          │   - Messaging pillars + proof points      │       │
│          │   - Pricing strategy                      │        │
│          │   - Objection handling map                │        │
│          │ Writes docs/gtm/03-position.md           │        │
│          │ Returns summary text                     │──┐     │
│          └──────────────────────────────────────────┘  │     │
│                                                        ▼     │
│  Step 4: Claude invokes Skill("gtm:activate")                │
│          ┌──────────────────────────────────┐                │
│          │ FORKED SUBAGENT (asset-generator) │               │
│          │ Reads 01 + 02 + 03               │                │
│          │                                   │                │
│          │ If /frontend-design installed →   │                │
│          │   uses it for landing page        │               │
│          │ If /copywriting installed →       │                │
│          │   uses it for headlines           │               │
│          │ Otherwise → vendored references   │                │
│          │                                   │                │
│          │ Writes docs/gtm/assets/           │               │
│          │   landing-page.html               │                │
│          │   cold-sequence.md                │                │
│          │   one-pager.md                    │                │
│          │   objection-handler.md            │               │
│          │   roi-calculator.md               │                │
│          │ Returns summary text              │──┐            │
│          └──────────────────────────────────┘  │            │
│                                                 ▼            │
│  Step 5: Claude invokes Skill("gtm:outbound")               │
│          ┌──────────────────────────────────┐                │
│          │ FORKED SUBAGENT (general-purpose) │               │
│          │ Reads 02-market.md + 03-position.md│              │
│          │ WebSearch for target accounts      │               │
│          │ Builds ABM list matching ICP       │               │
│          │ Generates per-persona sequences    │              │
│          │ Writes docs/gtm/outbound/          │               │
│          │ Returns summary text               │──┐           │
│          └──────────────────────────────────┘  │           │
│                                                 ▼           │
│  Step 6: Claude prints final summary to user                 │
│          "GTM package ready at docs/gtm/"                    │
│          Lists all files created with descriptions           │
└─────────────────────────────────────────────────────────────┘
```

---

## 6. Skill Specifications

### 6.1 `/gtm:scan` — "What did we build?"

**Purpose**: Scan the entire codebase and produce a structured capability inventory.

**Frontmatter**:
```yaml
---
name: scan
description: Scan any codebase and map all technical capabilities into a structured inventory with counts, categories, and file references. Use when analyzing what a product does.
context: fork
agent: Explore
disable-model-invocation: true
allowed-tools: Read, Glob, Grep, Bash
---
```

**What it does**:
- Read package.json / Gemfile / pyproject.toml for tech stack
- Map every API endpoint, database model, background job, integration, webhook, config option, auth system, CLI tool, AI/ML component
- Count everything (target 30-100+ features)
- Categorize by type
- Reference methodology.md for replacement cost framework

**Input**: Codebase (current directory)
**Output**: `docs/gtm/01-scan.md`

**Output format**:
```markdown
# Codebase Scan: {Product Name}

## Tech Stack
- Language: ...
- Framework: ...
- Database: ...

## Capability Inventory

### API Endpoints ({count})
| Endpoint | Method | What it does |
|----------|--------|-------------|

### Database Models ({count})
| Model | Fields | Relationships |
|-------|--------|---------------|

### Background Jobs ({count})
...

### Integrations ({count})
...

### AI/ML Components ({count})
...

### Auth & Permissions
...

### CLI Tools / MCP Servers ({count})
...

## Summary
- {X} total capabilities mapped
- {Y} endpoints, {Z} models, {W} integrations
- Categories present: [list]
- Categories absent: [list]
```

---

### 6.2 `/gtm:market` — "Who cares?"

**Purpose**: Determine the ideal customer profile, research competitors, and size the market.

**Frontmatter**:
```yaml
---
name: market
description: Research ICP, competitors, and market sizing for a product based on its codebase scan. Determines who buys, who competes, and how big the opportunity is.
context: fork
agent: market-researcher
disable-model-invocation: true
allowed-tools: Read, Glob, Grep, Bash, WebSearch, WebFetch
---
```

**What it does**:

**ICP Research**:
- Read `docs/gtm/01-scan.md` for codebase signals
- Infer target buyer from:
  - Schema entities (leads → GTM teams; deployments → DevOps; patients → healthcare)
  - Integration signals (Salesforce → enterprise; Stripe → SaaS; Shopify → e-commerce)
  - Feature signals (API-first → developers; email + CRM → sales; analytics → data teams)
  - Pricing tiers → market segment
  - UI copy signals ("for teams," "for developers")
- Build company profile: industry, revenue range, employee count, tech maturity, stage
- Build persona map: buyer, user, blocker, champion — each with title, pain, language, objections

**Competitor Research**:
- WebSearch with multiple query patterns
- For each competitor found: what they do/don't do, pricing, setup complexity, G2/Capterra sentiment, funding/momentum, integration gaps
- Identify market gaps: what nobody does well, what everyone charges extra for, where onboarding is painful

**Market Sizing**:
- TAM / SAM / SOM estimates with sources
- Adjacent markets worth expanding into
- Pricing anchors from competitor data
- Revenue math: "If you capture X% of SAM at $Y/mo = $Z ARR"

**Input**: `docs/gtm/01-scan.md`
**Output**: `docs/gtm/02-market.md`

**Output format**:
```markdown
# Market Intelligence: {Product Name}

## Ideal Customer Profile

### Company Profile
- Industry: ...
- Revenue range: ...
- Employee count: ...
- Stage: ...
- Tech maturity: ...
- Signal: "They have THIS problem but not THIS solution"

### Persona Map

#### Primary Buyer (signs the check)
- Title: ...
- Pain: ...
- Language they use: ...
- Objections: ...

#### Primary User (uses it daily)
...

#### Blocker (says no)
...

#### Champion (fights for it internally)
...

## Competitive Landscape

### {Competitor A}
- What they do: ...
- Pricing: ${X}/mo
- Setup complexity: ...
- G2 sentiment: ...
- Key gaps: ...

### {Competitor B}
...

### Market Gaps
- What NOBODY does well: ...
- What everyone charges extra for: ...
- Where onboarding is painful: ...

## Market Sizing
- TAM: ...
- SAM: ...
- SOM: ...
- Revenue math: ...
- Adjacent markets: ...
```

---

### 6.3 `/gtm:position` — "Why us?"

**Purpose**: Synthesize scan + market intel into positioning, battle cards, messaging, and pricing strategy.

**Frontmatter**:
```yaml
---
name: position
description: Build positioning strategy, battle cards, messaging framework, and pricing strategy from codebase scan and market research.
context: fork
agent: positioning-strategist
disable-model-invocation: true
allowed-tools: Read, Glob, Grep, Bash
---
```

**What it does**:
- Read `docs/gtm/01-scan.md` + `docs/gtm/02-market.md`
- Build value propositions per persona
- Create battle cards per competitor
- Define messaging pillars with proof points
- Recommend pricing strategy based on competitor anchoring
- Map objections to responses

**Input**: `docs/gtm/01-scan.md` + `docs/gtm/02-market.md`
**Output**: `docs/gtm/03-position.md`

**Output format**:
```markdown
# Positioning Strategy: {Product Name}

## Value Proposition
- One-liner: "X for Y that Z"
- Elevator (30 sec): ...
- Full pitch (2 min): ...

### Per Persona
- Buyer hears: "Cut your [cost] by [amount]"
- User hears: "Never [pain] again"
- Blocker hears: "SOC2 ready, no migration risk"

## Battle Cards

### vs. {Competitor A} (${price}/mo)
| Their Claim | Our Counter | Proof Point |
|-------------|-------------|-------------|
| ... | ... | ... |

Trap question: "Ask them if they can do [thing we do]"

### vs. {Competitor B} (${price}/mo)
...

## Messaging Framework

### Pillar 1: {Theme}
- Claim: ...
- Proof: ...
- One-liner: ...

### Pillar 2: {Theme}
...

## Pricing Strategy
- Recommended tiers (based on competitor anchoring)
- What's free vs paid vs enterprise
- Replacement cost math
- Expansion triggers

## Objection Map
| Objection | Response | Proof |
|-----------|----------|-------|

## Words We Use vs. Words We Never Use
| USE | NEVER USE |
|-----|-----------|
```

---

### 6.4 `/gtm:activate` — "Build the assets"

**Purpose**: Generate deploy-ready marketing assets from the positioning strategy.

**Frontmatter**:
```yaml
---
name: activate
description: Generate landing pages, sales collateral, and marketing assets from positioning strategy. Creates deploy-ready HTML, email copy, and sales enablement docs.
context: fork
agent: asset-generator
disable-model-invocation: true
allowed-tools: Read, Glob, Grep, Bash, Write, Edit
---
```

**What it does**:
- Read `docs/gtm/01-scan.md` + `docs/gtm/02-market.md` + `docs/gtm/03-position.md`
- Generate landing page (HTML, self-contained, deploy-ready)
  - Hero with value prop
  - Feature sections (organized by buyer outcomes)
  - Social proof section
  - Pricing section
  - FAQ from objection map
  - CTA
- Generate cold email sequence (5-touch)
- Generate one-pager (shareable with prospects)
- Generate objection handler (sales enablement)
- Generate ROI calculator template

**Ecosystem skill integration**:
- If `/frontend-design` is installed → use it for landing page polish
- If `/copywriting` is installed → use it for headline sharpening
- If `/web-design-guidelines` is installed → use it for accessibility review
- Otherwise → use vendored reference files in `references/`

**Input**: `docs/gtm/01-scan.md` + `02-market.md` + `03-position.md`
**Output**: `docs/gtm/assets/`

---

### 6.5 `/gtm:outbound` — "Build the target list and sequences"

**Purpose**: Build ABM target lists and personalized outbound sequences from ICP + positioning.

**Frontmatter**:
```yaml
---
name: outbound
description: Build ABM target lists and personalized cold email sequences from ICP and positioning strategy. Researches companies matching ICP signals.
context: fork
agent: general-purpose
disable-model-invocation: true
allowed-tools: Read, Glob, Grep, Bash, Write, Edit, WebSearch, WebFetch
---
```

**What it does**:

**ABM Target List**:
- Read ICP from `docs/gtm/02-market.md`
- WebSearch for companies matching ICP signals
- Filter by tech stack signals, hiring patterns (job posts = pain), funding stage
- Output structured target list with research notes

**Personalized Sequences**:
- Per persona from `docs/gtm/02-market.md`
- Using positioning from `docs/gtm/03-position.md`
- Cold email templates (AIDA framework)
- LinkedIn connection message
- Follow-up sequence (5 touches)
- Trigger-based emails (funding, hiring, etc.)
- Breakup email

**Input**: `docs/gtm/02-market.md` + `docs/gtm/03-position.md`
**Output**: `docs/gtm/outbound/`

---

### 6.6 `/gtm:launch` — "Run everything"

**Purpose**: Orchestrate skills 1-5 sequentially. This is the only skill that runs INLINE.

**Frontmatter**:
```yaml
---
name: launch
description: Run the full GTM pipeline — scan codebase, research market, build positioning, generate assets, and create outbound sequences. End-to-end go-to-market automation.
argument-hint: "[product-name]"
disable-model-invocation: true
allowed-tools: Skill, Read, Glob, Write
---
```

**What it does**:
1. Create `docs/gtm/` directory
2. Invoke `/gtm:scan $ARGUMENTS` via the Skill tool → wait for completion
3. Read `docs/gtm/01-scan.md` → confirm it exists and has content
4. Invoke `/gtm:market` via the Skill tool → wait for completion
5. Read `docs/gtm/02-market.md` → confirm
6. Invoke `/gtm:position` via the Skill tool → wait for completion
7. Read `docs/gtm/03-position.md` → confirm
8. Invoke `/gtm:activate` via the Skill tool → wait for completion
9. Invoke `/gtm:outbound` via the Skill tool → wait for completion
10. Print summary: list all files created, file sizes, key highlights

**Critical**: This skill does NOT use `context: fork`. It runs inline so it retains access to the Skill tool and conversation context.

---

## 7. Custom Agents

Custom agents live in `agents/*.md` within the plugin. They define the persona, tools, and methodology for forked skills.

### 7.1 `market-researcher.md`

```
---
name: market-researcher
description: ICP research, competitive analysis, and market sizing specialist
---

You are a market research analyst specializing in B2B SaaS go-to-market.

When analyzing a product:
1. Start with the codebase scan to understand capabilities
2. Infer ICP from technical signals (schema entities, integrations, feature patterns)
3. Research competitors thoroughly — pricing, gaps, sentiment, momentum
4. Size the market with bottoms-up math, not top-down guesses
5. Every claim needs a source or explicit reasoning

Use WebSearch and Perplexity for research. Be specific with numbers.
Never say "large market" — say "$2.4B TAM based on [source]".
```

### 7.2 `positioning-strategist.md`

```
---
name: positioning-strategist
description: Positioning, messaging, and competitive strategy specialist
---

You are a B2B positioning strategist in the style of April Dunford.

When building positioning:
1. Start from the customer's problem, not the product's features
2. Every value prop must answer "so what?" for a specific persona
3. Battle cards must include trap questions and proof points
4. Messaging pillars are claims with evidence, not slogans
5. Pricing strategy anchors against competitor pricing

Write for someone deciding between this product and doing nothing.
Never use: leverage, robust, scalable, seamless, cutting-edge, best-in-class.
```

### 7.3 `asset-generator.md`

```
---
name: asset-generator
description: Marketing asset generator — landing pages, email copy, sales collateral
---

You are a conversion-focused copywriter and frontend designer.

When generating assets:
1. Landing pages must be self-contained HTML, mobile-responsive, deploy-ready
2. Headlines follow proven formulas (problem-agitate-solve, before-after-bridge)
3. Every CTA has a clear next step
4. Social proof sections use specific numbers, not vague claims
5. Email sequences follow AIDA framework with personalization hooks
6. One-pagers fit on a single printed page

Write copy that a non-technical buyer understands in 5 seconds.
```

---

## 8. External Skills Integration (The Layer Cake)

```
┌──────────────────────────────────────────────────────────┐
│  LAYER 3: ECOSYSTEM (optional, enhances if installed)     │
│                                                           │
│  /frontend-design        99K installs (anthropics/skills) │
│    → Landing page generation with high design quality     │
│                                                           │
│  /web-design-guidelines  128K installs (vercel-labs)      │
│    → Accessibility + UX audit                             │
│                                                           │
│  /copywriting            (anthropics/skills)              │
│    → Headlines, CTAs, marketing copy                      │
│                                                           │
│  /cold-email-copy        (locally installed)              │
│    → AIDA, PAS, BAB email frameworks                      │
│                                                           │
│  HOW IT WORKS:                                            │
│  /gtm:launch runs INLINE → has access to Skill tool      │
│  After /gtm:activate produces raw assets, /gtm:launch    │
│  can optionally invoke ecosystem skills to polish them.   │
│                                                           │
│  Forked skills reference ecosystem skills in their        │
│  instructions: "If /frontend-design is available, use it. │
│  Otherwise, use references/landing-page-patterns.md"      │
├───────────────────────────────────────────────────────────┤
│  LAYER 2: VENDORED KNOWLEDGE (always works, no deps)      │
│                                                           │
│  activate/references/                                     │
│  ├── landing-page-patterns.md   ← hero, features, CTA    │
│  ├── copywriting-patterns.md    ← AIDA, PAS, BAB         │
│  ├── headline-formulas.md       ← 20+ proven formulas     │
│  └── cold-email-frameworks.md   ← 5-touch sequences       │
│                                                           │
│  These ensure the plugin works standalone without any      │
│  external skills installed.                               │
├───────────────────────────────────────────────────────────┤
│  LAYER 1: OWNED SKILLS (our core, bundled in plugin)      │
│                                                           │
│  /gtm:scan     → Codebase → feature inventory            │
│  /gtm:market   → Features → ICP + competitors + sizing   │
│  /gtm:position → Intel → value props + battle cards      │
│  /gtm:activate → Strategy → landing pages + assets       │
│  /gtm:outbound → ICP → ABM lists + email sequences       │
│  /gtm:launch   → Orchestrates everything                 │
└───────────────────────────────────────────────────────────┘
```

### Install recommendations for users (README)

```bash
# Required
/plugin marketplace add orchid-automation/orchid-gtm

# Recommended (enhances output quality)
npx skillsadd anthropics/skills          # frontend-design + copywriting
npx skillsadd vercel-labs/agent-skills   # web-design-guidelines
```

---

## 9. Reference Files (Vendored Knowledge)

Each skill's `references/` directory contains lazy-loaded knowledge that SKILL.md links to. Claude only reads these files when needed.

### Reference files to create

| Skill | File | Content |
|-------|------|---------|
| scan | `methodology.md` | Replacement cost framework, the 4 questions, analysis by feature type (migrated from current feature-map) |
| market | `icp-framework.md` | ICP inference from codebase signals, company profile template, persona map template |
| market | `competitor-analysis.md` | Competitive research playbook: what to look for, how to evaluate, pricing intel gathering |
| position | `battle-card-template.md` | Their claim → our counter → proof point format |
| position | `messaging-framework.md` | Pillar structure, headline bank format, proof point pairing |
| position | `pricing-patterns.md` | Tier structures, competitor anchoring, expansion triggers |
| activate | `landing-page-patterns.md` | Hero patterns, feature sections, social proof, CTA variations |
| activate | `copywriting-patterns.md` | AIDA, PAS, BAB frameworks with B2B SaaS examples |
| activate | `headline-formulas.md` | 20+ proven headline templates |
| activate | `cold-email-frameworks.md` | 5-touch cold email sequence templates |
| outbound | `sequence-templates.md` | Per-persona outbound templates with personalization hooks |

### Rules for reference files (from official best practices)

- Keep each file focused on one topic
- Add a table of contents at the top if over 100 lines
- Reference files are ONE level deep only (SKILL.md → reference.md, never deeper)
- Name files descriptively (`battle-card-template.md`, not `doc2.md`)
- Include concrete examples, not abstract instructions
- Prefer concise patterns over verbose explanations

---

## 10. Design Rules From Official Docs

Based on scraping and analyzing:
- https://code.claude.com/docs/en/skills
- https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
- https://platform.claude.com/cookbook/skills-notebooks-01-skills-introduction

### Hard constraints

| Rule | Limit | Our Compliance |
|------|-------|---------------|
| SKILL.md body | Under 500 lines | Each phase skill is focused |
| Skill name | 64 chars, lowercase + hyphens only | `scan`, `market`, `position`, `activate`, `outbound`, `launch` |
| Description | Under 1024 chars, no XML tags | Short, specific descriptions |
| Token budget for descriptions | 2% of context window (~16K chars) | 6 skills x ~200 chars = ~1200 chars |
| Reference depth | ONE level from SKILL.md | All references direct from SKILL.md |
| Reference file TOC | Required if over 100 lines | All long files get TOCs |

### Best practices applied

| Practice | How We Apply It |
|----------|----------------|
| "Only add context Claude doesn't already have" | Don't explain what APIs are. Just say which files to read. |
| `context: fork` for isolated execution | All phase skills fork. Only launch runs inline. |
| `disable-model-invocation: true` for side-effect skills | All 6 skills are manual-only. |
| Progressive disclosure | SKILL.md is the TOC. References loaded on demand. |
| Concise descriptions in third person | "Scans codebase..." not "I can scan..." |
| `!`command`` for dynamic context | Can inject `!`ls src/`` or `!`cat package.json`` |
| `$ARGUMENTS` for user input | `/gtm:launch MyProduct` → `$ARGUMENTS` = "MyProduct" |
| Feedback loops | Quality gate validates output before finalizing |

### Key insight: `context: fork` + custom agents

From the official docs:

> Skills and subagents work together in two directions:
>
> | Approach | System prompt | Task | Also loads |
> |----------|--------------|------|------------|
> | Skill with `context: fork` | From agent type (Explore, Plan, etc.) | SKILL.md content | CLAUDE.md |
> | Subagent with `skills` field | Subagent's markdown body | Claude's delegation message | Preloaded skills + CLAUDE.md |

We use the first pattern: each skill's `context: fork` + `agent: market-researcher` means the market-researcher agent's persona becomes the system prompt, and the SKILL.md content becomes the task.

---

## 11. Compound Engineering Patterns Applied

Key patterns borrowed from the Compound Engineering plugin analysis:

### Pattern 1: Parallel Specialists → Sequential Pipeline

CE uses parallel specialists for code review (security + performance + architecture all at once). We use a **sequential pipeline** because each phase depends on the previous.

However, within `/gtm:market`, the ICP research and competitor research can run in parallel as separate Task calls.

### Pattern 2: Subagents Return Text, Orchestrator Writes

CE's critical rule: agents return TEXT, orchestrator writes ONE file.

We modify this slightly: each forked skill writes its OWN output file (since forked skills have filesystem access), but the orchestrator (`/gtm:launch`) validates each file exists before proceeding.

### Pattern 3: Conditional Agent Spawning

CE only spawns migration reviewers when `db/migrate/` files exist. We apply this in `/gtm:scan`: only report categories that actually have features. Downstream skills only process categories that exist in `01-scan.md`.

### Pattern 4: Token Budget Management

CE reduced context usage from 316% to 65% by:
- Trimming agent descriptions (1400 → 180 chars)
- Using `disable-model-invocation: true` on side-effect commands
- Moving detailed content to lazy-loaded references

We follow all three patterns.

### Pattern 5: XML Semantic Tags for Critical Instructions

CE uses `<critical_requirement>`, `<parallel_tasks>`, `<protected_artifacts>`. We use similar tags in skill content:

```markdown
<critical_requirement>
Every feature must answer the 4 questions from methodology.md.
If a feature can't answer all 4, flag it but don't skip it.
</critical_requirement>
```

### Pattern 6: Knowledge Compounding Loop

CE documents solutions to `docs/solutions/` and queries them during planning. We don't implement this yet, but the file-based output (`docs/gtm/`) is structured so a future `/gtm:refine` skill could read performance data and adjust positioning.

---

## 12. What's Novel (Our Moat)

Nobody on the skills ecosystem has:

| Capability | Status on skills.sh |
|-----------|-------------------|
| Codebase → ICP inference | Doesn't exist |
| Codebase → competitive landscape | Doesn't exist |
| Codebase → full GTM package | Doesn't exist |
| Replacement cost math from code analysis | Doesn't exist |
| End-to-end code → market orchestration | Doesn't exist |

The individual pieces exist separately:
- `/frontend-design` does landing pages (99K installs)
- `/copywriting` does marketing copy
- `/cold-email-copy` does outbound sequences
- Various SEO and content skills exist

**Our differentiation**: The pipeline from technical codebase to market-ready assets, fully automated.

---

## 13. Build Order

| Phase | Skill | Difficulty | Dependencies |
|-------|-------|------------|-------------|
| 1 | Plugin restructure (feature-map → orchid-gtm) | Easy | None |
| 2 | `/gtm:scan` | Medium | Migrate from current feature-map |
| 3 | `/gtm:launch` (initial: just scan) | Easy | Scan must work |
| 4 | `/gtm:market` | Hard | Heaviest research, needs Perplexity/WebSearch |
| 5 | `/gtm:position` | Medium | Synthesis skill, less research |
| 6 | `/gtm:activate` | Medium | Asset generation, vendored references needed |
| 7 | `/gtm:outbound` | Medium | Can leverage existing LeadKit patterns |
| 8 | Quality review agent | Easy | All phases complete |
| 9 | Ecosystem skill integration | Easy | Polish step |

### Incremental delivery

- **v0.1**: `/gtm:scan` + `/gtm:launch` (just scan phase)
- **v0.2**: Add `/gtm:market` (ICP + competitors)
- **v0.3**: Add `/gtm:position` (strategy + battle cards)
- **v0.4**: Add `/gtm:activate` (landing pages + assets)
- **v0.5**: Add `/gtm:outbound` (ABM + sequences)
- **v1.0**: Full pipeline with ecosystem skill integration + quality validation

---

## 14. Open Questions

| Question | Options | Recommendation |
|----------|---------|----------------|
| Landing page output format | Raw HTML? React? Tailwind? Framer copy blocks? | Start with self-contained HTML + Tailwind CDN. Most portable. |
| Outbound integration | Just templates? Or connect to LeadKit/Instantly? | Templates first. Integration later via LeadKit skills. |
| Market sizing depth | Back-of-napkin TAM or bottoms-up? | Bottoms-up when data exists, top-down as fallback. |
| Iteration loop | `/gtm:refine` that reads performance data? | Future v2 feature. Ship pipeline first. |
| Plugin naming | Keep `orchid-plugins` repo, rename plugin to `orchid-gtm`? Or new repo? | Keep marketplace repo. Rename plugin from `feature-map` to `gtm`. Session stays. |
| Marketplace structure | One marketplace with session + gtm? Or separate? | Keep together. More plugins = more value for marketplace install. |

---

## Appendix A: Comparison to Current Feature-Map

| Aspect | Current | Redesigned |
|--------|---------|-----------|
| Skills | 1 monolithic skill | 6 focused skills |
| Context management | All inline, bloats main context | Forked subagents, isolated contexts |
| Agent spawning | TeamCreate (experimental) | `context: fork` (official, documented) |
| Category handling | Spawns agents for all categories | Conditional — only categories that exist |
| Output | Multiple files + synthesis | Each phase writes one file, launch orchestrates |
| Market research | Inline Phase 1.5 | Dedicated skill with custom agent |
| ICP determination | Brief inline inference | Full research with WebSearch + Perplexity |
| Positioning | Bundled into synthesis | Dedicated skill with battle cards, messaging framework |
| Asset generation | None | Landing page, email sequences, one-pagers, ROI calculator |
| Outbound | None | ABM target lists + personalized sequences |
| Quality validation | Checklist in SKILL.md (no enforcement) | Orchestrator validates each phase output |
| External skills | None | Integrates frontend-design, copywriting, cold-email-copy |
| Token efficiency | 298-line SKILL.md + methodology always loaded | SKILL.md under 500 lines, references lazy-loaded |

---

## Appendix B: Skills.sh Ecosystem Map

Skills from skills.sh relevant to each GTM phase:

| Phase | Relevant Skills | Install Count | Integration |
|-------|----------------|---------------|-------------|
| Scan | None needed — we own this | — | Core |
| Market | None available — we own this | — | Core |
| Position | `/copywriting` | — | Reference |
| Activate | `/frontend-design` (anthropics) | 99K | Reference |
| Activate | `/web-design-guidelines` (vercel-labs) | 128K | Reference |
| Activate | `/vercel-react-best-practices` (vercel-labs) | 167K | Optional |
| Activate | `/pdf`, `/pptx` (anthropics) | — | Optional |
| Outbound | `/cold-email-copy` (local) | — | Reference |
| Outbound | `/social-content` | — | Optional |

---

*Last updated: 2026-02-25*
