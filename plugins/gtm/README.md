# Orchid GTM Engine

Go-to-market engine for Claude Code. Point it at any codebase and get a complete GTM package: ICP research, competitive analysis, positioning strategy, landing page, cold email sequences, and ABM target lists.

## Quick Start

```
/gtm:launch MyProduct
```

This runs all five phases in sequence and produces a complete package at `docs/gtm/`.

## Skills

| Skill | What It Does | Runs As |
|-------|-------------|---------|
| `/gtm:scan` | Map every capability in the codebase | Forked subagent (Explore) |
| `/gtm:market` | ICP research, competitor analysis, market sizing | Forked subagent (market-researcher) |
| `/gtm:position` | Value props, battle cards, messaging, pricing | Forked subagent (positioning-strategist) |
| `/gtm:activate` | Landing page, email copy, one-pager, sales docs | Forked subagent (asset-generator) |
| `/gtm:outbound` | ABM target lists, per-persona email sequences | Forked subagent |
| `/gtm:launch` | Orchestrates all five phases end-to-end | Inline (retains Skill tool) |

## Running Individual Skills

Each skill works standalone. Run any phase independently:

```
/gtm:scan MyProduct          # Just scan the codebase
/gtm:market                  # Research ICP and competitors (requires 01-scan.md)
/gtm:position                # Build positioning (requires 01-scan.md + 02-market.md)
/gtm:activate                # Generate assets (requires 01 + 02 + 03)
/gtm:outbound                # Build ABM lists (requires 02 + 03)
```

Skills 2-5 read from `docs/gtm/` files produced by previous phases. Run them in order, or run `/gtm:launch` to automate the full sequence.

## Output

```
docs/gtm/
├── 01-scan.md                 # Feature inventory with counts and file refs
├── 02-market.md               # ICP + competitors + TAM/SAM/SOM
├── 03-position.md             # Value props + battle cards + messaging
├── assets/
│   ├── landing-page.html      # Self-contained, deploy-ready (Tailwind CDN)
│   ├── cold-sequence.md       # 5-touch AIDA email sequence
│   ├── one-pager.md           # Single-page prospect summary
│   ├── objection-handler.md   # Sales enablement: objection responses
│   └── roi-calculator.md      # ROI justification template
└── outbound/
    ├── target-accounts.md     # ABM target list matching ICP
    └── sequences/             # Per-persona outbound sequences
```

## Recommended Ecosystem Skills

The GTM Engine works standalone. These optional skills enhance output quality if installed:

```bash
# Landing page design quality
npx skillsadd anthropics/skills          # includes /frontend-design + /copywriting

# Accessibility and UX audit
npx skillsadd vercel-labs/agent-skills   # includes /web-design-guidelines
```

## How It Works

1. **Scan** reads the codebase and builds a structured capability inventory
2. **Market** infers ICP from codebase signals, then researches competitors and sizes the market via web search
3. **Position** synthesizes scan + market intel into value props, battle cards, and messaging
4. **Activate** generates deploy-ready marketing assets from the positioning strategy
5. **Outbound** builds ABM target lists and personalized email sequences from ICP + positioning

Each phase writes to `docs/gtm/`. The orchestrator validates each output before proceeding to the next phase.

## License

MIT
