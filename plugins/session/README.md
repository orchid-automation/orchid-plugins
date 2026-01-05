# Session Plugin

Developer productivity tools for analyzing coding sessions, tracking accomplishments, and knowing when to take a break.

## Installation

```bash
# Add the Orchid Plugins marketplace
/plugin marketplace add orchid-automation/orchid-plugins

# Install the session plugin
/plugin install session@orchid-plugins
```

## Commands

### `/session:vibecheck`

Analyze your git commit history and get a comprehensive productivity report.

```bash
# Analyze the last 5 hours (default)
/session:vibecheck

# Analyze a specific time period
/session:vibecheck 3        # Last 3 hours
/session:vibecheck 8        # Last 8 hours

# Include optional sections
/session:vibecheck --share      # Add shareable summaries for Slack/Twitter
/session:vibecheck --timeline   # Add timeline visualization and energy curve
/session:vibecheck --quality    # Add commit quality and ship readiness checks
/session:vibecheck --full       # Include all optional sections

# Combine options
/session:vibecheck 4 --share --timeline
/session:vibecheck 8 --full
```

## What You Get

### Always Included
- **Session Overview** - Commits, files changed, lines added/removed
- **Session Summary** - 2-3 sentence recap of accomplishments
- **Key Accomplishments** - Bullet points grouped by theme
- **Files Impact** - Breakdown by backend/frontend/config
- **Technical Complexity Assessment** - Architecture, features, bugs, research ratings
- **Decisions Made** - Architectural choices for future reference
- **Dependencies & Integrations** - New packages, APIs, services
- **Technical Debt & TODOs** - Shortcuts taken, known issues
- **Breaking Changes** - What could affect existing behavior
- **Risk Assessment** - What could go wrong
- **What's Next** - Logical next steps
- **Traditional Team Estimate** - Days vs your hours comparison
- **Vibe Rating** - 🔥🔥🔥, 🔥🔥, 🔥, or 🌱
- **Achievements Unlocked** - Badges for work type
- **Session Tempo** - Commits/hour, flow state detection
- **Permission to Touch Grass** - Personalized break recommendation

### With `--share`
- **Slack/Twitter-ready summary** - Copy-paste for social
- **Standup summary** - Yesterday/today/blockers format

### With `--timeline`
- **Session Timeline** - ASCII visualization of commit distribution
- **Energy Curve** - Start/middle/end assessment
- **Blockers & Stuck Time** - Gap analysis between commits

### With `--quality`
- **Commit Quality** - Atomic commits, message quality, WIP count
- **Ship Readiness** - Ready to PR or needs cleanup
- **Focus Analysis** - Scope creep detection, yak shave identification

## Requirements

- Git repository with commit history
- Claude Code with Task tool access

## Verify Installation

```bash
# Check installed plugins
/plugin list
```

You should see `session` in the list.

## Troubleshooting

```bash
# Remove and reinstall
/plugin uninstall session@orchid-plugins
/plugin install session@orchid-plugins

# Remove marketplace entirely and re-add
/plugin marketplace remove orchid-plugins
/plugin marketplace add orchid-automation/orchid-plugins
```

## License

MIT
