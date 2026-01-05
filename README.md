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

## Available Plugins

### session

Developer productivity tools for analyzing coding sessions.

```bash
/plugin install session@orchid-plugins
```

**Commands:**
- `/session:vibecheck` - Analyze git history and get a productivity report with team estimate comparison

[View documentation](./plugins/session/README.md)

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
