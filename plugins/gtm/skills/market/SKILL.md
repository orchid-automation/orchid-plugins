---
name: market
description: Research ICP, competitors, and market sizing for a product based on its codebase scan. Determines who buys, who competes, and how big the opportunity is. Reads the scan output and produces a structured market intelligence document.
context: fork
agent: market-researcher
disable-model-invocation: true
allowed-tools: Read, Glob, Grep, Bash, WebSearch, WebFetch
---

# Market Intelligence Skill

You are running the market research phase of the Orchid GTM Engine. Your job is to read the codebase scan, determine who buys this product, who competes with it, and how big the opportunity is.

## Input

Read the scan output first:

```
Read("docs/gtm/01-scan.md")
```

If `$ARGUMENTS` is provided, use it as the product name. Otherwise, extract the product name from the scan document header.

---

## Three Research Tracks

Run these in sequence. Each track builds on the previous.

### Track 1: ICP Research

Infer the ideal customer from codebase signals found in `01-scan.md`.

For ICP inference methodology, see [icp-framework.md](references/icp-framework.md).

**Signal analysis** -- work through these from the scan:

1. **Schema entities** -- what the product manages reveals who uses it
2. **Integration signals** -- connected tools reveal the buyer's stack
3. **Feature signals** -- capabilities reveal the team that benefits
4. **Pricing tiers** -- price points reveal market segment
5. **UI copy** -- language like "for teams" or "for developers" reveals positioning

**Build two outputs:**

- **Company profile**: industry, revenue range, employee count, stage, tech maturity, and the key signal ("They have THIS problem but not THIS solution")
- **Persona map**: four roles (buyer, user, blocker, champion) each with title, pain, language they use, and objections

### Track 2: Competitor Research

For competitive research playbook, see [competitor-analysis.md](references/competitor-analysis.md).

**Search strategy** -- run multiple WebSearch queries:

```
WebSearch("{product-category} software alternatives 2025")
WebSearch("best {product-category} tools for {inferred-buyer}")
WebSearch("{product-category} G2 comparison")
WebSearch("{closest-competitor} vs alternatives pricing")
```

**For each competitor found, gather:**

| Data Point | How to Find |
|------------|-------------|
| What they do / don't do | WebFetch their homepage + features page |
| Pricing | WebFetch their pricing page |
| Setup complexity | Look for "get started" flow, onboarding docs |
| G2/Capterra sentiment | WebSearch "{competitor} G2 reviews" |
| Funding / momentum | WebSearch "{competitor} funding crunchbase" |
| Integration gaps | Compare their integrations to what 01-scan.md shows |

Target 3-6 competitors. More if the market is crowded.

**Identify market gaps:**

- What NOBODY does well
- What everyone charges extra for
- Where onboarding is painful
- What requires enterprise contracts that should be self-serve

### Track 3: Market Sizing

Build bottoms-up estimates when data is available, top-down as fallback.

**Data to find:**

```
WebSearch("{product-category} market size 2025 2026")
WebSearch("{buyer-segment} spending on {category} tools")
WebSearch("number of {buyer-type} companies {region}")
```

**Calculate:**

- **TAM**: Total addressable market -- every company that could buy this
- **SAM**: Serviceable -- companies matching the ICP profile
- **SOM**: Obtainable -- realistic capture in year 1-2
- **Revenue math**: "If you capture X% of SAM at $Y/mo = $Z ARR"
- **Adjacent markets**: Categories worth expanding into

**Pricing anchors**: Use competitor pricing data to recommend price positioning (undercut, match, or premium -- and why).

---

## Output

Write the complete market intelligence document to `docs/gtm/02-market.md`.

<critical_requirement>
Every claim needs a source or explicit reasoning. Never say "large market" -- say "$2.4B TAM based on [source]". Never say "many competitors" -- name them and price them.
</critical_requirement>

### Output Template

Use this exact structure:

```markdown
# Market Intelligence: {Product Name}

## Ideal Customer Profile

### Company Profile
- **Industry**: {specific verticals, not "technology"}
- **Revenue range**: ${X}M - ${Y}M ARR
- **Employee count**: {range}
- **Stage**: {Seed / Series A / Series B / Growth / Enterprise}
- **Tech maturity**: {Low / Medium / High -- and what that means for them}
- **Key signal**: "They have {THIS problem} but not {THIS solution}"

### Persona Map

#### Primary Buyer (signs the check)
- **Title**: {specific title, e.g., "VP of Sales" not "executive"}
- **Pain**: {what keeps them up at night, specific to this product}
- **Language they use**: "{exact phrases they'd say in a meeting}"
- **Objections**: {top 2-3 reasons they'd say no}

#### Primary User (uses it daily)
- **Title**: {specific title}
- **Pain**: {daily friction this product removes}
- **Language they use**: "{phrases}"
- **Objections**: {adoption concerns}

#### Blocker (says no)
- **Title**: {specific title, often IT/Security/Legal/Finance}
- **Pain**: {risk they're protecting against}
- **Language they use**: "{phrases}"
- **Objections**: {security, compliance, budget concerns}

#### Champion (fights for it internally)
- **Title**: {specific title}
- **Pain**: {what they're tired of doing manually}
- **Language they use**: "{phrases}"
- **Internal pitch**: "{how they'd sell it to the buyer}"

## Competitive Landscape

### {Competitor A}
- **What they do**: {one sentence}
- **What they don't do**: {gaps relevant to this product}
- **Pricing**: ${X}/mo ({tier details})
- **Setup complexity**: {self-serve / guided / implementation required}
- **G2 sentiment**: {star rating + common praise and complaints}
- **Funding / momentum**: {last round, headcount trend}
- **Key gap**: {the thing this product does that they can't}

### {Competitor B}
{same structure}

### {Competitor C}
{same structure}

{repeat for each competitor}

### Market Gaps
- **What NOBODY does well**: {gap}
- **What everyone charges extra for**: {gap}
- **Where onboarding is painful**: {gap}
- **Self-serve gap**: {what requires enterprise sales that shouldn't}

## Market Sizing

### TAM (Total Addressable Market)
- **Size**: ${X}B
- **Basis**: {how calculated, with source}
- **Includes**: {what segments}

### SAM (Serviceable Addressable Market)
- **Size**: ${X}M
- **Basis**: {ICP-filtered calculation}
- **Companies matching ICP**: ~{N} companies

### SOM (Serviceable Obtainable Market)
- **Size**: ${X}M
- **Basis**: {realistic Year 1-2 capture rate}
- **Revenue math**: "{N} customers x ${Y}/mo = ${Z} ARR"

### Pricing Anchors
| Competitor | Price | What's Included |
|------------|-------|-----------------|
| {name} | ${X}/mo | {tier details} |
| {name} | ${X}/mo | {tier details} |

**Recommended positioning**: {undercut / match / premium} because {reasoning}

### Adjacent Markets
- {Market 1}: ${X}B -- {why it's adjacent, what feature unlocks it}
- {Market 2}: ${X}B -- {same}
```

---

## Quality Gate

Before writing the file, verify:

- [ ] Company profile has all 6 fields filled with specifics
- [ ] All 4 personas have title, pain, language, and objections
- [ ] At least 3 competitors with pricing data
- [ ] Market gaps section has concrete gaps, not generalities
- [ ] TAM/SAM/SOM have dollar figures with sources or reasoning
- [ ] Revenue math is included with specific numbers
- [ ] No buzzwords: "robust", "scalable", "cutting-edge", "best-in-class"
- [ ] Every claim has a source or explicit reasoning chain

Once validated, write to `docs/gtm/02-market.md` and return a summary of key findings.
