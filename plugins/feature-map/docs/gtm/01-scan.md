# Codebase Scan: Feature Map

> A Claude Code plugin that turns any codebase into a buyer-focused GTM feature map — deploying parallel AI agents to analyze technical capabilities through a replacement-cost lens.

**Scan date:** 2026-02-25
**Total capabilities mapped:** 14

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Platform | Claude Code Plugin System (`.claude-plugin`) |
| Language | Markdown skill definitions (SKILL.md format) |
| Runtime | Claude Code CLI (agent orchestration) |
| AI Engine | Claude models via Task tool (parallel agent spawning) |
| Tools Used | Task, Read, Glob, Grep, Write, Edit, Bash, TeamCreate, TeamDelete, TaskCreate, TaskUpdate, TaskList, SendMessage, WebSearch, WebFetch |
| Output Format | Structured Markdown documents |

---

## Capability Inventory

### AI/ML Components (5)

| Component | Model/Provider | What it does | Source file |
|-----------|---------------|-------------|-------------|
| Parallel Agent Orchestration | Claude (via Task tool) | Deploys 3-4 AI agents simultaneously to analyze different feature categories across a codebase | skills/feature-map/SKILL.md:149-174 |
| ICP Inference Engine | Claude + WebSearch | Analyzes codebase signals (schema, UI copy, integrations, pricing tiers) to automatically identify the target buyer profile | skills/feature-map/SKILL.md:77-144 |
| Competitor Research Agent | Claude + WebSearch + WebFetch | Runs multi-query competitor research including pricing pages, G2 comparisons, and feature gap analysis | skills/feature-map/SKILL.md:109-143 |
| Feature-to-Outcome Translator | Claude (per-agent) | Transforms raw technical capabilities into buyer-outcome statements using the 4-question methodology | skills/feature-map/methodology.md:12-22 |
| Master Document Synthesizer | Claude (synthesis phase) | Combines all agent outputs into a single buyer-focused document organized by outcomes, not engineering modules | skills/feature-map/SKILL.md:178-243 |

### CLI Tools / Plugin System (3)

| Tool | Interface | What it enables | Source file |
|------|-----------|----------------|-------------|
| `/feature-map` slash command | Claude Code CLI skill | One-command GTM feature map generation from any codebase | skills/feature-map/SKILL.md:1-8 |
| Argument parsing (product, buyer, competitors) | CLI arguments | Customizable analysis targeting — specify product name, buyer persona, and competitor list | skills/feature-map/SKILL.md:26-35 |
| Plugin distribution via `.claude-plugin` | Claude Code plugin registry | Install once, use across any project — portable GTM analysis | .claude-plugin/plugin.json |

### Configuration (3)

| Setting | Default | What the buyer controls |
|---------|---------|------------------------|
| Product name | Required argument | Names the output documents and sets analysis context |
| Target buyer (ICP) | Auto-inferred from codebase | Override the buyer persona to reframe the entire document for a different audience |
| Competitor list | Auto-researched via web search | Specify exact competitors to position against, or let the system discover them |

### Methodology & Frameworks (3)

| Framework | What it encodes | Source file |
|-----------|----------------|-------------|
| 4-Question Analysis Framework | Every feature must answer: what can I do, what does this replace, what's the lift, where do competitors fail | skills/feature-map/methodology.md:12-22 |
| Replacement Cost Benchmarks | Pre-built pricing tables for roles ($5K-25K/mo), tools ($20-2,500/mo), and manual processes (2-60 min each) | skills/feature-map/methodology.md:92-125 |
| Competitive Positioning Rules | 6 rules: always include pricing, name what they don't do, name setup cost, name maintenance burden, never say "better" | skills/feature-map/methodology.md:128-136 |

---

## Summary

- **14 total capabilities** mapped across 4 categories
- **5** AI/ML components, **3** CLI/plugin tools, **3** configuration options, **3** methodology frameworks
- **Categories present:** AI/ML Components, CLI Tools / Plugin System, Configuration, Methodology & Frameworks
- **Categories absent:** API Endpoints, Database Models, Background Jobs, Integrations, Auth & Permissions, UI Pages

### Signals for ICP Inference

- **Tool surface is CLI-first with plugin distribution** → technical buyer or technical founder who lives in the terminal
- **Output is marketing/GTM documents** → the buyer straddles product and go-to-market — likely a founder, head of product marketing, or growth lead
- **Methodology encodes sales benchmarks (SDR salaries, agency retainers)** → targets B2B SaaS companies with outbound GTM motions
- **"Any codebase" universality** → horizontal tool, not vertical — buyer could be at any B2B SaaS company
- **Parallel agent architecture** → buyer values speed and is willing to pay for AI-generated first drafts over manual work
- **Competitor research built in** → buyer doesn't have an existing competitive intelligence function (no dedicated product marketing team yet)
