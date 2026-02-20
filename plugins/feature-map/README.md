# Feature Map

Point at any codebase and generate a comprehensive, GTM-focused feature map that makes potential customers want to buy.

## What it does

1. **Deep codebase exploration** — reads schema, routes, agents, crons, integrations, configs. Counts every distinct capability.
2. **ICP & competitor research** — if not provided, infers the target buyer from codebase signals and researches competitors via web search.
3. **Parallel agent team** — deploys 3-4 agents to analyze features across categories (AI, infrastructure, platform, integrations, etc.) through the GTM lens.
4. **Master document synthesis** — combines all agent outputs into one buyer-focused document organized by outcomes, not engineering modules.

## Usage

```bash
# Point at current codebase (auto-infers ICP + competitors)
/feature-map ProductName

# With explicit buyer and competitors
/feature-map ProductName "Series A-D GTM teams" "Clay, Instantly, Smartlead"
```

## Output

- `docs/feature-map-{category}.md` — per-agent analysis files
- `docs/{product}-feature-map.md` — master combined document

Every feature includes:
- **What can I do?** — buyer outcome, not technical implementation
- **What does this replace?** — tool, person, process, with $ cost
- **What's the specific lift?** — time saved, cost eliminated, risk removed
- **Where do competitors fall short?** — gaps with pricing context

## Methodology

The skill encodes a GTM analysis methodology with:
- **4 Questions** every feature must answer
- **Replacement cost benchmarks** (SDR salaries, agency retainers, tool costs, manual process hours)
- **Competitive positioning rules** (always include pricing, name what they don't do, name setup cost)
- **Banned words** ("leverage," "robust," "scalable," "cutting-edge," "seamless")
- **Writing style** (second person, buyer perspective, concrete numbers)

See [methodology.md](skills/feature-map/methodology.md) for the full analysis framework.
