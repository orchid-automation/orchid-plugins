# Attribution

Linear Swarm is heavily inspired by, and designed to interoperate with, [Every Inc's compound-engineering-plugin](https://github.com/EveryInc/compound-engineering-plugin) (MIT license, © Every Inc).

## Patterns borrowed from CE

| Pattern | Source | How we use it |
|---|---|---|
| **Plan → Work → Review → Compound** cycle | [every.to/guides/compound-engineering](https://every.to/guides/compound-engineering) | Same 4-phase loop inside `linear-swarm` Phases 1-9, extended with Deploy + Prod Verify |
| **Parallel specialist reviewers** | CE's 14+ `agents/review/*.md` fleet | Bundled 3 fallback reviewers (correctness/security/simplicity). Delegate to CE's full fleet when installed. |
| **Structural git-worktree isolation** | CE `git-worktree` skill | `linear-swarm` uses worktree isolation for local workers; mirrors CE's primitive |
| **Compound learnings to `docs/solutions/`** | CE `/workflows:compound` | `linear-swarm` Phase 9 writes learnings to CE's `docs/solutions/` if CE is installed, else to `docs/swarm/solutions/` directly |
| **Review + triage + parallel resolve** | CE `/triage` + `/resolve_todo_parallel` | Phase 2-3 fix-up loop uses the same shape; delegates to CE's version when installed |
| **Conditional skill delegation** | CE's graceful-enhancement language in SKILL.md | Phase 2 / Phase 9 detect CE at runtime and use it if present |

## What we add that CE doesn't have

- **Linear API as the entry point** (CE reads from `docs/brainstorms/` on disk — we read parent tasks + subtasks from Linear)
- **Sandcastle + Vercel Sandbox workers with cheap-tier models** via Vercel AI Gateway (CE uses local worktrees exclusively)
- **Phase 8 prod verify** — call the live deployed service through a real authenticated client to catch ops-config regressions that every structural test misses
- **Model escalation ladder** (GLM 5.1 → Kimi K2.5 → Haiku 4.5 → Opus) when cheap-tier workers fail structural smoke
- **`--fresh`/`--resume` discipline** for `codex:rescue` calls so the automation never halts on `AskUserQuestion`

## If you want the full compound-engineering experience

```bash
/plugin marketplace add EveryInc/compound-engineering-plugin
/plugin install compound-engineering@EveryInc-compound-engineering-plugin
```

Then install Linear Swarm too — `linear-swarm` detects CE at runtime and automatically uses their full 14+ specialist reviewer fleet, their battle-tested `/workflows:plan` and `/workflows:compound`, and their `git-worktree` skill.

The two plugins are **complementary, not competitive**. Install both.

## License note

This plugin is MIT-licensed. Any pattern names or phase names borrowed from CE are attributed here in good faith; all code in this plugin is original to Orchid Automation. If any specific agent prompt or skill markdown is adapted from CE's source, the individual file will carry its own attribution in a header comment.

Thanks to Dan Shipper, Kieran Klaassen, and the Every Inc team for making the compound engineering pattern legible and shippable for the rest of us.
