# Orchid Plugins

A collection of Claude Code plugins by [Orchid Automation](https://github.com/orchid-automation).

## Installation

Add this marketplace to Claude Code:

```bash
/plugin marketplace add orchid-automation/orchid-plugins
```

Then browse and install plugins:

```bash
/plugin
```

Or install directly:

```bash
/plugin install <plugin-name>@orchid-plugins
```

## Verify Installation

```bash
# Check installed plugins
/plugin list
```

## Troubleshooting

```bash
# Remove and reinstall a plugin
/plugin uninstall <plugin-name>@orchid-plugins
/plugin install <plugin-name>@orchid-plugins

# Remove marketplace entirely and re-add
/plugin marketplace remove orchid-plugins
/plugin marketplace add orchid-automation/orchid-plugins
```

## Available Plugins

### session

Developer productivity tools for analyzing coding sessions.

```bash
/plugin install session@orchid-plugins
```

**Commands:**
- `/session:vibecheck` - Analyze git history and get a productivity report with team estimate comparison

[View documentation](./plugins/session/README.md)

### feature-map

Point at any codebase and generate a GTM-focused feature map. Translates technical capabilities into buyer outcomes, business lift, and competitive positioning using a team of parallel agents.

```bash
/plugin install feature-map@orchid-plugins
```

**Skills:**
- `/feature-map ProductName` - Auto-infers ICP and competitors from codebase, deploys 3-4 agents in parallel, produces a master buyer-focused document
- `/feature-map ProductName "target buyer" "Competitor1, Competitor2"` - With explicit buyer and competitor context

[View documentation](./plugins/feature-map/README.md)

---

## Contributing

We welcome contributions! To add a plugin:

1. Create a new directory under `plugins/`
2. Add `.claude-plugin/plugin.json` manifest
3. Add your commands/skills/agents
4. Update this README
5. Submit a PR

## License

MIT
