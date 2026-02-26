---
name: scan
description: Scan a codebase and map all capabilities into a structured feature inventory with counts and file references.
user-invocable: true
disable-model-invocation: true
allowed-tools: Read, Glob, Grep, Bash
---

# Codebase Scan

Scan this codebase and produce a structured capability inventory at `docs/gtm/01-scan.md`.

The product name is: **$ARGUMENTS**

For replacement cost framework, see [methodology.md](references/methodology.md).

---

## Dynamic Context

!`cat package.json 2>/dev/null || cat Gemfile 2>/dev/null || cat pyproject.toml 2>/dev/null || cat Cargo.toml 2>/dev/null || cat go.mod 2>/dev/null || cat pom.xml 2>/dev/null || echo "No package manifest found"`

---

## What to Scan

Explore the full codebase. Find and count every instance of:

### 1. API Endpoints
- REST routes, GraphQL resolvers, gRPC services, tRPC routers
- Search: route files, controllers, `app.get/post/put/delete`, `@app.route`, `router.`, `@Controller`

### 2. Database Models
- ORM models, schema definitions, migrations, Prisma schema, SQLAlchemy models
- Document entities, fields, and relationships between models

### 3. Background Jobs
- Cron tasks, queue workers, scheduled functions, pub/sub consumers
- Anything that runs without a user request

### 4. Integrations
- Third-party API calls, SDK imports, OAuth flows, webhook handlers
- Every external service the product connects to

### 5. AI/ML Components
- LLM calls, model inference, embedding generation, vector search, prompt templates
- AI agents, tool use, RAG pipelines, fine-tuned models

### 6. Auth & Permissions
- Auth providers, RBAC/ABAC, API keys, OAuth scopes, session management
- Compliance features: rate limiting, audit logs, encryption

### 7. CLI Tools / MCP Servers
- Command-line interfaces, MCP tool definitions, SDK exports
- Developer-facing integration surfaces

### 8. Configuration & Settings
- Feature flags, environment variables, admin settings, tenant config
- Every lever the buyer can pull

### 9. UI / Frontend
- Pages, components, dashboards, forms
- What the user actually sees and interacts with

---

## How to Scan

1. **Start broad**: Read the manifest, README, and entry points to understand the stack
2. **Map the architecture**: Identify the framework, directory conventions, and patterns
3. **Scan systematically**: Use Glob and Grep to find every capability type above
4. **Count precisely**: Hard numbers for every category. Aim for 30-100+ total capabilities
5. **Reference files**: Note the source file for each capability so downstream skills can verify

<critical_requirement>
Only report categories that actually have features. If the codebase has no AI/ML, skip that section entirely. Do not pad empty categories.
</critical_requirement>

---

## Output Format

Create `docs/gtm/` directory if it does not exist. Write the following to `docs/gtm/01-scan.md`:

```markdown
# Codebase Scan: {Product Name}

> {One-line summary: what this product does, in plain language}

**Scan date:** {YYYY-MM-DD}
**Total capabilities mapped:** {N}

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | {e.g., TypeScript 5.x} |
| Framework | {e.g., Next.js 14, FastAPI} |
| Database | {e.g., PostgreSQL + Prisma} |
| Auth | {e.g., NextAuth, Clerk, custom JWT} |
| Hosting | {inferred from config, e.g., Vercel, Docker} |
| Key Dependencies | {top 5-10 non-trivial deps} |

---

## Capability Inventory

### API Endpoints ({count})

| Endpoint | Method | What it does | Source file |
|----------|--------|-------------|-------------|
| /api/... | POST | ... | src/routes/... |

### Database Models ({count})

| Model | Key Fields | Relationships | Source file |
|-------|-----------|---------------|-------------|
| User | email, role, plan | has_many: Projects | ... |

### Background Jobs ({count})

| Job | Trigger | What it automates | Source file |
|-----|---------|------------------|-------------|
| ... | cron/queue/event | ... | ... |

### Integrations ({count})

| Service | Type | What data flows | Source file |
|---------|------|----------------|-------------|
| Stripe | Payment | Billing, subscriptions | ... |

### AI/ML Components ({count})

| Component | Model/Provider | What it does | Source file |
|-----------|---------------|-------------|-------------|
| ... | GPT-4/Claude/custom | ... | ... |

### Auth & Permissions

| Mechanism | What it protects | Compliance relevance |
|-----------|-----------------|---------------------|
| ... | ... | ... |

### CLI Tools / MCP Servers ({count})

| Tool | Interface | What it enables | Source file |
|------|-----------|----------------|-------------|
| ... | CLI/MCP/SDK | ... | ... |

### Configuration ({count})

| Setting | Default | What the buyer controls |
|---------|---------|------------------------|
| ... | ... | ... |

### UI Pages / Components ({count})

| Page/Component | What the user does here |
|---------------|------------------------|
| /dashboard | ... |

---

## Summary

- **{X} total capabilities** mapped across {Y} categories
- **{A}** endpoints, **{B}** models, **{C}** jobs, **{D}** integrations
- **Categories present:** {list}
- **Categories absent:** {list}

### Signals for ICP Inference

{Brief notes on what the codebase reveals about the target buyer:}
- Schema entities suggest: ...
- Integrations suggest: ...
- Pricing/plan tiers suggest: ...
- UI copy suggests: ...
- Feature patterns suggest: ...
```

---

## Quality Checks Before Writing

- Every table has real data from the codebase, not placeholders
- Counts in section headers match actual table rows
- Source files are real paths that exist in the codebase
- Summary totals are arithmetic sums, not estimates
- ICP signals section has at least 3 concrete observations
- No empty categories included
- No buzzwords in descriptions -- plain language only
