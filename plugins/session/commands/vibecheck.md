---
allowed-tools: Task
argument-hint: [hours] [--share] [--timeline] [--quality] [--full] (default: 5 hours)
description: Analyze your vibecoding session - what you accomplished and engineering team equivalent
---

Use the Task tool to spawn a subagent that analyzes git commit history.

**Hours to analyze:** If $ARGUMENTS is empty or not provided, default to 5 hours. Otherwise parse the first number from $ARGUMENTS as hours.

**Flags to check in $ARGUMENTS:**
- `--share` → Include shareable summary section
- `--timeline` → Include timeline visualization and energy curve
- `--quality` → Include commit quality and ship readiness
- `--full` → Include all optional sections

**Subagent configuration:**
- subagent_type: "general-purpose"
- model: "opus"
- description: "vibecheck"

**Subagent prompt (replace HOURS with the value - default 5 if $ARGUMENTS is empty):**

Analyze the git commit history from the last HOURS hours in this repository.

## Step 1: Gather Data

Run these git commands (replace HOURS with the actual number):
1. `git log --since="HOURS hours ago" --pretty=format:"%h|%ai|%s" --reverse` - get all commits
2. `git log --since="HOURS hours ago" --stat` - see files changed per commit
3. `git log --since="HOURS hours ago" --shortstat` - line count summary

## Step 2: Provide Analysis

### Session Overview

Provide a quick stats table:

| Metric | Value |
|--------|-------|
| Time Period | Last HOURS hours |
| Total Commits | X |
| Files Changed | X |
| Lines Added | +X |
| Lines Removed | -X |
| Net Change | +/- X |

### Session Summary
A 2-3 sentence high-level summary of what was accomplished. Make it satisfying to read - this person has been grinding.

### Key Accomplishments
Bullet points of the main things built, fixed, or improved. Group by theme if multiple areas were touched. Be specific about what was actually done.

### Files Impact

| Area | Files | Changes |
|------|-------|---------|
| Backend | 5 | +200/-50 |
| Frontend | 3 | +150/-30 |
| Config/Docs | 2 | +50/-10 |

### Technical Complexity Assessment

| Complexity | Rating |
|------------|--------|
| Architecture Changes | Low/Med/High |
| New Features | Low/Med/High |
| Bug Fixes | Low/Med/High |
| Research Required | Low/Med/High |
| **Overall** | **Simple / Moderate / Complex / Deep** |

Explain why you rated it this way.

### Decisions Made
List key architectural or design decisions made during this session. These are useful for future reference - why was X approach chosen over Y?

### Dependencies & Integrations
Note any new packages added, APIs integrated, or external services connected. Include version numbers if visible in the diff.

### Technical Debt & TODOs
List any TODOs added, shortcuts taken, or known issues introduced. Be honest - what was deferred for later?

### Breaking Changes
Flag anything that could affect existing behavior - API changes, schema changes, config changes, etc. If none, say "None identified."

### Risk Assessment
What could go wrong with these changes? What needs manual testing? What assumptions were made?

### What's Next
Based on the work done, what are the logical next steps for the next session?

### Traditional Engineering Team Estimate

Consider ALL enterprise overhead:

| Phase | Traditional Time |
|-------|------------------|
| Planning & Design | X days |
| Sprint Planning | X days |
| Development | X days |
| Code Review | X days |
| Testing & QA | X days |
| Documentation | X days |
| Deployment | X days |
| **Total** | **X-Y days** |

```
┌─────────────────────────────────────────┐
│  Vibecode time:     HOURS hours         │
│  Team equivalent:   X-Y days (Z engs)   │
│  Efficiency ratio:  ~Nx faster          │
└─────────────────────────────────────────┘
```

### Vibe Check

Rate the session vibe with an emoji scale:

| Vibe | Meaning |
|------|---------|
| 🔥🔥🔥 | Absolutely cracked - mass shipping |
| 🔥🔥 | Solid grind - real progress |
| 🔥 | Steady work - moving forward |
| 🌱 | Planting seeds - setup/research |

### Achievements Unlocked

Check which apply and list them:
- 🏗️ **Architect** - Made structural/architecture changes
- 🐛 **Bug Squasher** - Fixed bugs
- ✨ **Feature Factory** - Shipped new features
- 📚 **Documentarian** - Wrote docs/comments
- 🧪 **Test Writer** - Added tests
- 🔧 **Refactorer** - Cleaned up code
- 🚀 **Deployer** - Pushed to prod
- 🌅 **Early Bird** - Coding before 8am
- 🦉 **Night Owl** - Coding after 10pm
- 📦 **Dependency Wrangler** - Updated packages
- 🎨 **UI Polish** - Frontend improvements
- 🔌 **Integrator** - Connected systems/APIs
- 📈 **10x Moment** - Single commit with huge impact

### Session Tempo

| Metric | Value |
|--------|-------|
| Commits/hour | X |
| Lines/hour | X |
| Flow state? | Yes/No (based on commit clustering) |

### Permission to Touch Grass 🌿

Based on what was accomplished, give a compelling and specific reason to step away. Reference the actual things that were built to make it feel earned. Be celebratory - they shipped real stuff.

Include a break suggestion based on session length:
- < 2 hours: "Quick stretch and water break"
- 2-4 hours: "Take a walk, grab coffee"
- 4-6 hours: "Proper meal break, touch actual grass"
- 6+ hours: "You're cooked. Log off. Go outside. Now."

End with:
```
┌────────────────────────────────────────────────┐
│  🌿 You've earned it. Go touch grass. 🌿      │
└────────────────────────────────────────────────┘
```

---

## OPTIONAL SECTIONS (include based on flags in $ARGUMENTS)

### If --share OR --full flag is present, include:

### Share-Ready Summary

📣 **For Slack/Twitter:**
> "Just shipped [main accomplishment] in [X] hours: [2-3 key things]. Traditional estimate: [Y] days."

📋 **For Standup:**
> Yesterday: [accomplishments]. Today: [what's next]. Blockers: [none/list].

---

### If --timeline OR --full flag is present, include:

### Session Timeline

Create ASCII visualization of commit distribution by hour:
```
Hour 1: ████████ (X commits) - [assessment: heavy start/slow start/etc]
Hour 2: ████ (X commits) - [assessment]
Hour 3: ██████ (X commits) - [second wind/steady/etc]
...
```

Run `git log --since="HOURS hours ago" --format="%ai"` to get timestamps.

Identify flow states: clusters of 3+ commits within 30 minutes.

### Energy Curve

| Phase | Indicator |
|-------|-----------|
| Start | 🟢/🟡/🔴 [assessment from commit patterns] |
| Middle | 🟢/🟡/🔴 [assessment] |
| End | 🟢/🟡/🔴 [assessment] |

Signs of fatigue to look for:
- More "fix" or "typo" commits toward the end
- Longer gaps between commits
- Shorter commit messages
- More debug/cleanup commits

### Blockers & Stuck Time

Analyze gaps > 20 minutes between commits:

| Gap | Duration | Likely Cause |
|-----|----------|--------------|
| Between commit X-Y | Z min | Possible debugging/research/distraction |

Total "stuck time": ~X hours
Effective coding time: ~Y hours of Z hours

---

### If --quality OR --full flag is present, include:

### Commit Quality

| Aspect | Assessment |
|--------|------------|
| Atomic Commits | Yes/No - are commits well-scoped or mixing concerns? |
| Message Quality | Good/Needs Work - descriptive, follows conventions? |
| WIP/Fixup Count | X commits that should be squashed before PR |
| Logical Progression | Yes/No - does commit history tell a coherent story? |

Look for:
- "WIP", "wip", "fix", "fixup", "temp", "test" in messages
- Very short messages like "update" or "changes"
- Commits that should have been combined

### Ship Readiness

| Check | Status |
|-------|--------|
| No WIP commits | ✅/❌ |
| No obvious debug code visible in diff | ✅/❌/⚠️ |
| Breaking changes documented | ✅/❌/N/A |
| Commit history clean | ✅/❌ |

**Ready to PR:** Yes / Almost (minor cleanup) / Needs work (squash/rebase needed)

### Focus Analysis

| Metric | Value |
|--------|-------|
| Primary Goal | [inferred from first 2-3 commits] |
| Directories Touched | X |
| Scope Creep Level | Low/Med/High |
| Yak Shaves | X commits on tangential work |

Scope creep indicators:
- Commits unrelated to the apparent main goal
- Work spread across many unrelated directories
- "While I'm here..." type changes

---

**Tone:** Celebratory but honest. This is a productivity reality check that should feel good and validate stepping away.
