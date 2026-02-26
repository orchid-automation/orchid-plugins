---
name: launch
description: Run the full GTM pipeline — scan, market research, positioning, assets, and outbound — end to end.
argument-hint: "[product-name]"
user-invocable: true
disable-model-invocation: true
allowed-tools: Skill, Read, Glob, Write, Bash
---

# GTM Launch Orchestrator

Run the complete Orchid GTM Engine pipeline for **$ARGUMENTS**.

This skill orchestrates five phases in sequence. Each phase runs as an isolated subagent that writes its output to `docs/gtm/`. This orchestrator validates each output before invoking the next phase.

<critical_requirement>
This skill runs INLINE (no fork). Do NOT add context: fork. The Skill tool is only available in inline mode. Losing it means the pipeline cannot invoke subskills.
</critical_requirement>

---

## Phase 0: Setup

Create the output directory:

```
mkdir -p docs/gtm/assets docs/gtm/outbound/sequences
```

Print to the user:

```
=== ORCHID GTM ENGINE ===
Product: $ARGUMENTS
Starting full pipeline...
```

---

## Phase 1: Codebase Scan

Invoke the scan skill:

```
Skill("gtm:scan $ARGUMENTS")
```

Wait for it to complete, then validate:

```
Read("docs/gtm/01-scan.md")
```

**Fail-fast gate**: If `docs/gtm/01-scan.md` does not exist or is empty, STOP and report:

```
FAILED: Phase 1 (scan) did not produce docs/gtm/01-scan.md
The pipeline cannot continue without a codebase scan.
```

If valid, print:

```
Phase 1 COMPLETE: Codebase scan written to docs/gtm/01-scan.md
```

---

## Phase 2: Market Research

Invoke the market skill:

```
Skill("gtm:market")
```

Wait for it to complete, then validate:

```
Read("docs/gtm/02-market.md")
```

**Fail-fast gate**: If `docs/gtm/02-market.md` does not exist or is empty, STOP and report:

```
FAILED: Phase 2 (market) did not produce docs/gtm/02-market.md
The pipeline cannot continue without market intelligence.
```

If valid, print:

```
Phase 2 COMPLETE: Market intelligence written to docs/gtm/02-market.md
```

---

## Phase 3: Positioning Strategy

Invoke the position skill:

```
Skill("gtm:position")
```

Wait for it to complete, then validate:

```
Read("docs/gtm/03-position.md")
```

**Fail-fast gate**: If `docs/gtm/03-position.md` does not exist or is empty, STOP and report:

```
FAILED: Phase 3 (position) did not produce docs/gtm/03-position.md
The pipeline cannot continue without positioning strategy.
```

If valid, print:

```
Phase 3 COMPLETE: Positioning strategy written to docs/gtm/03-position.md
```

---

## Phase 4: Asset Generation

Invoke the activate skill:

```
Skill("gtm:activate")
```

Wait for it to complete. Print:

```
Phase 4 COMPLETE: Marketing assets generated in docs/gtm/assets/
```

---

## Phase 5: Outbound Sequences

Invoke the outbound skill:

```
Skill("gtm:outbound")
```

Wait for it to complete. Print:

```
Phase 5 COMPLETE: Outbound sequences generated in docs/gtm/outbound/
```

---

## Phase 6: Final Summary

After all phases complete, use Glob to list every file in `docs/gtm/`:

```
Glob("docs/gtm/**/*")
```

Then print a final summary to the user in this format:

```
=== GTM PACKAGE COMPLETE ===

Product: $ARGUMENTS

Files created:
  docs/gtm/01-scan.md              - Codebase capability inventory
  docs/gtm/02-market.md            - ICP, competitors, market sizing
  docs/gtm/03-position.md          - Value props, battle cards, messaging
  docs/gtm/assets/
    landing-page.html              - Deploy-ready landing page
    cold-sequence.md               - 5-touch cold email sequence
    one-pager.md                   - Shareable prospect summary
    objection-handler.md           - Sales enablement objection map
    roi-calculator.md              - ROI justification template
  docs/gtm/outbound/
    target-accounts.md             - ABM target list
    sequences/                     - Per-persona email sequences

Next steps:
  1. Review docs/gtm/02-market.md for ICP accuracy
  2. Open docs/gtm/assets/landing-page.html in a browser
  3. Customize docs/gtm/outbound/ sequences with real prospect names
  4. Run individual skills to regenerate any section:
     /gtm:scan    /gtm:market    /gtm:position
     /gtm:activate    /gtm:outbound
```

List the actual files found by Glob, not just the template above. Include file sizes where possible.

---

## Rules

1. Run phases 1-5 in strict sequential order. Never skip a phase.
2. Phases 1-3 have fail-fast gates. If validation fails, stop immediately.
3. Phases 4-5 do not have hard gates because their outputs are multiple files.
4. Always pass `$ARGUMENTS` to the scan skill so the product name propagates.
5. Do not pass arguments to skills 2-5. They read from `docs/gtm/` files.
6. Print clear progress markers so the user can track which phase is running.
7. If any Skill invocation errors, report the error and stop. Do not retry.
