---
name: activate
description: Generate landing pages, sales collateral, and marketing assets from positioning strategy. Creates deploy-ready HTML, email copy, and sales enablement docs. Reads codebase scan, market research, and positioning to produce a complete asset package.
context: fork
agent: asset-generator
disable-model-invocation: true
allowed-tools: Read, Glob, Grep, Bash, Write, Edit
---

# Asset Generation

Generate deploy-ready marketing assets from the GTM positioning strategy.

Read all three upstream files before generating anything:

1. `docs/gtm/01-scan.md` -- feature inventory and tech stack
2. `docs/gtm/02-market.md` -- ICP, competitors, market sizing
3. `docs/gtm/03-position.md` -- value props, battle cards, messaging, objection map

<critical_requirement>
All three input files MUST exist and contain real data. If any file is missing or empty, stop immediately and report the error.
</critical_requirement>

---

## Reference Files

Use these vendored references for patterns and frameworks:

- [Landing page patterns](references/landing-page-patterns.md) -- hero sections, feature layouts, social proof, CTAs
- [Copywriting patterns](references/copywriting-patterns.md) -- AIDA, PAS, BAB frameworks
- [Headline formulas](references/headline-formulas.md) -- 20+ proven fill-in-the-blank templates
- [Cold email frameworks](references/cold-email-frameworks.md) -- 5-touch sequence templates

---

## Ecosystem Skill Integration

Before generating assets, check if ecosystem skills are available:

1. **Landing page polish**: If the `/frontend-design` skill is available, use it after generating the initial `landing-page.html` to improve visual design, spacing, and responsiveness. Otherwise, use [landing-page-patterns.md](references/landing-page-patterns.md).

2. **Headline sharpening**: If the `/copywriting` skill is available, use it to refine headlines, CTAs, and value prop copy across all assets. Otherwise, use [headline-formulas.md](references/headline-formulas.md) and [copywriting-patterns.md](references/copywriting-patterns.md).

3. **Accessibility review**: If the `/web-design-guidelines` skill is available, use it to audit the landing page for accessibility and UX. Otherwise, follow the mobile-first and accessibility notes in [landing-page-patterns.md](references/landing-page-patterns.md).

To check availability, use Glob to look for these skills in the skills directory. If not found, proceed with the vendored reference files -- they contain everything needed.

---

## Assets to Generate

Create `docs/gtm/assets/` directory. Generate all 5 files below.

### 1. `landing-page.html`

Self-contained, deploy-ready HTML page with embedded CSS (Tailwind CDN). No external dependencies beyond the CDN link.

**Structure:**

- **Hero**: Value prop headline (from 03-position.md one-liner) + subheadline + primary CTA
- **Problem section**: The pain the ICP faces (from 02-market.md persona pains)
- **Features**: Organized by buyer outcomes, not technical specs. Use the messaging pillars from 03-position.md. 3-4 features max with icons (use emoji or SVG)
- **Social proof**: Metrics from 01-scan.md (capabilities count, integration count). If competitor pricing exists, show cost comparison
- **Pricing**: Tiers from 03-position.md pricing strategy. Keep it simple -- free/pro/enterprise or starter/growth
- **FAQ**: Convert every row from the objection map in 03-position.md into a question/answer
- **Footer CTA**: Repeat the primary call-to-action

**Technical requirements:**
- Tailwind CSS via CDN (`<script src="https://cdn.tailwindcss.com"></script>`)
- Mobile-responsive (test with Tailwind responsive classes)
- System font stack, no custom fonts
- Smooth scroll navigation
- All content from upstream files, no placeholder text

### 2. `cold-sequence.md`

5-touch cold email sequence targeting the primary buyer persona from 02-market.md.

**Structure per email:**
- Subject line (use formulas from cold-email-frameworks.md)
- Body copy using AIDA framework
- Personalization hooks (where to insert company-specific details)
- CTA (one clear ask per email)
- Timing note (days since previous touch)

**Sequence flow:**
1. Value-first intro (Day 0)
2. Pain + proof point (Day 3)
3. Competitor comparison angle (Day 7)
4. Case study / ROI angle (Day 14)
5. Breakup email (Day 21)

Use the battle cards from 03-position.md for competitive angles. Use the persona language from 02-market.md for tone.

### 3. `one-pager.md`

Single-page sales collateral a rep can share with a prospect. Markdown formatted for easy conversion to PDF.

**Structure:**
- Product name + one-liner value prop
- The problem (2-3 sentences from ICP pain)
- The solution (what the product does, mapped to outcomes)
- Key differentiators (3 bullets from battle cards)
- Social proof / metrics
- Pricing snapshot
- Next step CTA

<critical_requirement>
Must fit on one printed page. Keep total content under 400 words.
</critical_requirement>

### 4. `objection-handler.md`

Sales enablement document. Convert the objection map from 03-position.md into a usable quick-reference.

**Structure:**
- Organized by objection category (price, trust, switching cost, technical, timing)
- Each objection: the objection text, why they say it, the response, the proof point
- Quick-reference table at the top for scanning
- Detailed responses below

### 5. `roi-calculator.md`

Template that helps prospects justify the purchase internally.

**Structure:**
- Current cost section (what they spend today: headcount, tools, time, opportunity cost)
- Product cost section (pricing tiers from 03-position.md)
- Savings calculation (time saved, headcount avoided, tool consolidation)
- Revenue impact (if applicable: faster time-to-market, conversion improvements)
- Payback period formula
- Fill-in-the-blank format so prospects can plug in their own numbers

Use replacement cost data from 01-scan.md and pricing from 03-position.md.

---

## Generation Process

1. **Read all three input files** completely. Extract: value prop, personas, competitors, battle cards, messaging pillars, objection map, pricing strategy, feature inventory
2. **Generate landing-page.html** first -- it requires the most synthesis
3. **Generate cold-sequence.md** -- uses persona language and battle card angles
4. **Generate one-pager.md** -- distills the landing page into one printed page
5. **Generate objection-handler.md** -- restructures the objection map for sales use
6. **Generate roi-calculator.md** -- combines replacement cost math with pricing

---

## Quality Checks Before Finalizing

- [ ] Landing page has no placeholder text -- every section has real content from upstream files
- [ ] Landing page HTML is valid and self-contained (opens in browser without errors)
- [ ] Cold sequence has 5 distinct emails with different angles, not repetitive
- [ ] One-pager is under 400 words
- [ ] Objection handler covers every objection from 03-position.md
- [ ] ROI calculator has fill-in-the-blank fields, not hardcoded numbers
- [ ] No buzzwords: never use "leverage," "robust," "scalable," "seamless," "cutting-edge," "best-in-class"
- [ ] All CTAs have a clear, specific next step
- [ ] Persona language matches 02-market.md (use their words, not yours)

---

## Output Summary

After writing all 5 files, report:

```
Assets generated at docs/gtm/assets/:
- landing-page.html ({lines} lines) -- deploy-ready landing page
- cold-sequence.md -- 5-touch outbound sequence
- one-pager.md -- shareable sales one-pager
- objection-handler.md -- sales objection quick-reference
- roi-calculator.md -- prospect-facing ROI template
```
