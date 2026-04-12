# Market Intelligence: Feature Map

## Ideal Customer Profile

### Company Profile
- **Industry**: B2B SaaS, developer tools, AI/ML platforms — any company that ships software and needs to sell it
- **Revenue range**: $0 - $5M ARR (pre-revenue to early growth)
- **Employee count**: 1-50 (founder-led through first GTM hires)
- **Stage**: Pre-seed through Series B
- **Tech maturity**: High — they already use Claude Code, live in the terminal, and ship fast. Their bottleneck is marketing, not engineering
- **Key signal**: "They have a product worth talking about but no dedicated product marketing function to translate it into buyer language"

### Persona Map

#### Primary Buyer (signs the check)
- **Title**: Technical Founder / CEO at early-stage B2B SaaS
- **Pain**: Built the product, but the website says "we do everything" and nobody converts. Knows the product is good but can't articulate why in buyer language. Doesn't have $10-25K/mo for a GTM agency or $8-12K/mo for a product marketer
- **Language they use**: "We need to figure out our positioning." "I keep explaining what we do differently but it doesn't land." "We're engineers, not marketers." "How do I turn this into a landing page that converts?"
- **Objections**: "I can just use ChatGPT for this." "My product is too technical to explain to buyers." "Will it actually understand my codebase or give generic output?"

#### Primary User (uses it daily)
- **Title**: Developer / Technical Co-founder
- **Pain**: Getting pulled into marketing tasks they're not good at. Writing landing page copy, feature descriptions, competitor comparisons — all of it takes hours and the result reads like documentation, not marketing
- **Language they use**: "I just want to ship code, not write marketing copy." "Every time I describe what we built, it sounds like a README." "I need something I can run in the terminal, not another SaaS dashboard"
- **Objections**: "Is this another AI tool that produces generic garbage?" "Will it understand our monorepo?" "How long does it take to run?"

#### Blocker (says no)
- **Title**: Head of Marketing / CMO (at slightly larger companies with existing marketing teams)
- **Pain**: Concerned that AI-generated positioning won't match brand voice or strategy. Worried about inconsistency with existing messaging. Doesn't trust a CLI tool to do what their team does
- **Language they use**: "We already have our messaging framework." "AI can't understand our market nuances." "This looks like an engineering tool, not a marketing tool"
- **Objections**: "Our positioning needs human judgment, not automation." "How does this integrate with our existing content workflow?" "We already pay for [Jasper/Copy.ai/agency]"

#### Champion (fights for it internally)
- **Title**: Growth Engineer / Developer Advocate / First GTM Hire
- **Pain**: Stuck between engineering and marketing. Needs to produce GTM assets fast but doesn't have the budget for consultants or the time to do it from scratch. Sees the codebase every day and knows there are features nobody talks about
- **Language they use**: "We have 50 features and our landing page mentions 3." "I can generate a feature map in 10 minutes instead of spending a week on it." "This gives me the first draft — I just need to edit, not write from zero"
- **Internal pitch**: "For the cost of running Claude Code for 10 minutes, we get positioning, battle cards, and a landing page that would take a consultant 2-3 weeks and $5-15K. I'll still review everything, but we go from blank page to 80% in minutes instead of weeks."

## Competitive Landscape

### ChatGPT / Claude (Direct Prompting)
- **What they do**: General-purpose AI that can write marketing copy, analyze competitors, and draft positioning documents when given the right prompts
- **What they don't do**: No codebase analysis. No parallel agent orchestration. No structured methodology. No replacement cost framework. No automated competitive research pipeline. The user must manually copy-paste code, write custom prompts for each section, and stitch the outputs together
- **Pricing**: ChatGPT Plus $20/mo, Claude Pro $20/mo, API usage varies
- **Setup complexity**: Zero — but the work to get good output is 2-8 hours of prompt engineering per product
- **Key gap**: Can't read a codebase directly. Requires the user to know what to ask, what to include, and how to structure the output. Every session starts from zero — no methodology, no benchmarks, no competitive positioning framework built in

### Jasper AI
- **What they do**: AI-powered marketing copy platform. Templates for landing pages, emails, ads, blog posts. Brand voice customization. Team collaboration features
- **What they don't do**: No codebase analysis. No competitive research. No ICP inference. No replacement cost analysis. No battle cards. No per-feature outcome mapping. Content is template-driven, not intelligence-driven
- **Pricing**: $49/mo (Creator), $125/mo (Pro), custom Enterprise pricing
- **Setup complexity**: Self-serve, but requires manual input of product information, brand voice training, and template selection per asset
- **Key gap**: Produces marketing copy, not marketing strategy. Can't start from a codebase. Doesn't know your competitors, doesn't calculate replacement costs, doesn't build battle cards. You still need to know what to say — Jasper helps you say it faster

### GTM Agencies / Consultants
- **What they do**: Full-service GTM strategy — ICP research, competitive analysis, positioning, messaging framework, landing pages, sales collateral, outbound sequences
- **What they don't do**: Can't read your codebase directly. Analysis based on interviews and demos, not actual code. Deliverables take 2-8 weeks. Can't iterate instantly when the product changes. Not available at 2am when you're shipping
- **Pricing**: $10,000-25,000/mo retainer for a GTM agency; $5,000-15,000 per project for a freelance product marketing consultant
- **Setup complexity**: 1-2 week discovery process, 4-8 weeks to first deliverable, ongoing retainer for updates
- **Key gap**: Cost and speed. A startup spending $50K+ on GTM strategy before finding product-market fit is burning runway. Agencies don't update when you ship new features — you're paying for another engagement every time the product changes

### Productboard / Aha!
- **What they do**: Product management platforms for feature prioritization, roadmapping, and customer feedback collection. Internal-facing tools
- **What they don't do**: No GTM output. No buyer-facing feature maps. No competitive positioning. No marketing asset generation. These are tools for deciding what to build, not for selling what you've built
- **Pricing**: Productboard $20-80/user/mo; Aha! $59-149/user/mo
- **Setup complexity**: Multi-week onboarding, team rollout, data migration from existing tools
- **Key gap**: Entirely different job-to-be-done. These tools track features for the product team; Feature Map translates features for the buyer. There's no overlap in output — but there is in the perception of "feature management"

### Clay (Tangential — Outbound Intelligence)
- **What they do**: Workflow builder for enriching lead data and building outbound sequences. 100+ integrations. Manual workflow configuration per use case
- **What they don't do**: No codebase analysis. No positioning strategy. No feature mapping. No landing page generation. Clay enriches people data; Feature Map enriches product data for GTM use
- **Pricing**: $149/mo (Starter) to $720/mo (Pro), with credits consumed per enrichment
- **Setup complexity**: 2-4 hours per workflow. Requires understanding of data enrichment APIs and waterfall logic. No pre-built "codebase to GTM" workflow exists
- **Key gap**: Solves a different problem. Clay helps you find and enrich leads; Feature Map helps you know what to say to them. They're complementary, not competitive — but budget-constrained startups treat them as either/or

### Market Gaps
- **What NOBODY does well**: Translating a live codebase into buyer-ready positioning. Every tool in this space starts with human input (interviews, briefs, prompts). Nobody starts with the code itself
- **What everyone charges extra for**: Competitive analysis, battle cards, and replacement cost math. These are either manual (agency) or absent (AI tools). Feature Map includes them by default
- **Where onboarding is painful**: Agencies require weeks of discovery. AI writing tools require hours of prompt setup. Feature Map requires one command
- **Self-serve gap**: Getting a complete GTM package (ICP + positioning + battle cards + landing page + email sequences) requires either $10K+ in agency fees or stitching together 4-5 separate tools. Nobody offers this as a single self-serve command

## Market Sizing

### TAM (Total Addressable Market)
- **Size**: ~$12B
- **Basis**: Global AI writing and content generation market projected at $12.1B in 2025 (Grand View Research), growing at 25%+ CAGR. Includes AI marketing tools, content platforms, and copywriting automation
- **Includes**: Every company that produces marketing content from product features — B2B SaaS, developer tools, marketplaces, fintech, healthcare SaaS

### SAM (Serviceable Addressable Market)
- **Size**: ~$800M
- **Basis**: Subset focused on B2B SaaS companies at Seed through Series B stage with technical founding teams. ~160,000 B2B SaaS companies globally (SaaS Capital data). ~25% are early-stage with technical founders and limited marketing = ~40,000 companies. Average spend on GTM tools + consultants: $2,000/mo = $800M annual market
- **Companies matching ICP**: ~40,000 companies globally

### SOM (Serviceable Obtainable Market)
- **Size**: ~$2.4M (Year 1)
- **Basis**: Claude Code users who install plugins represent a narrow but high-intent audience. Conservative estimate: 2,000 active feature-map users in Year 1 (Claude Code crossed $1B ARR in 2026, with an active plugin ecosystem emerging). At an estimated $100/mo effective usage cost = $2.4M ARR potential in Year 1
- **Revenue math**: "2,000 active users x $100/mo average usage = $2.4M ARR in Year 1"

### Pricing Anchors
| Competitor/Alternative | Price | What's Included |
|------------------------|-------|-----------------|
| ChatGPT/Claude Pro subscription | $20/mo | General AI, no methodology or codebase analysis |
| Jasper Creator | $49/mo | Template-based copy, no strategy |
| Jasper Pro | $125/mo | Brand voice + templates, no codebase input |
| GTM consultant (one-time) | $5,000-15,000 | Full positioning package, 4-8 week delivery |
| GTM agency retainer | $10,000-25,000/mo | Ongoing strategy + asset creation |
| Clay Pro | $720/mo | Lead enrichment workflows, no positioning |

**Recommended positioning**: Premium over generic AI tools, massive undercut vs. agencies. Feature Map as a plugin costs only Claude Code usage ($20/mo Pro subscription + per-token costs per run, estimated $5-15 per full pipeline execution). Position against the $5-15K consultant engagement: "Get 80% of the output in 10 minutes for 0.1% of the cost. Edit and ship, don't start from scratch."

### Adjacent Markets
- **Sales enablement tools**: $3.2B — Feature Map's battle cards, objection handlers, and ROI calculators are sales enablement outputs. Expand to generate full sales playbooks from codebases
- **Developer marketing / DevRel**: $1.5B (est.) — Developer tool companies need feature maps translated for technical buyers. Expand with developer-specific output templates (API docs → GTM, changelog → feature announcement)
- **Product-led growth tools**: $2.1B — PLG companies need self-serve positioning that updates as the product evolves. Feature Map could run in CI/CD to auto-update marketing when code ships
