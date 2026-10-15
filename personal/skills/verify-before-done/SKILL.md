---
name: verify-before-done
description: "Before saying something is done, fixed or working, run the check and show the result; if it can't be checked, say so. Use when: you're about to finish a task, say a bug is fixed or that something passes, or before a commit or PR."
---

# Verify before done

> **CONCEPT:** no "done" without a check run in that same message and its output read; what can't be checked is said out loud. It stops the agent from claiming a success it never saw.

> **TEMPLATE · FILL-IN** each section. Full example: [examples/skills/verify-before-done](../../../examples/skills/verify-before-done/SKILL.md). Once filled in, delete this block.

## Before claiming anything
<!-- FILL-IN: the steps. E.g.: pick the check that proves it, run it now, read the whole output, say it with the evidence. -->

## What proves each thing

| Claim | Evidence | Doesn't count |
|---|---|---|
| Fits the stack and compiles | `py -3 <HARNESS>\personal\scripts\check.py` (no files: what changed in git): 0 errors | "I did it carefully" |
| <!-- FILL-IN: e.g. Tests pass --> | <!-- the test command, 0 failures --> | <!-- "they should pass" --> |
| Bug fixed | a test that failed before the fix and passes now (if the project has tests); if not, the original steps | "I changed the code" |

## Testing locally
<!-- FILL-IN: no credentials (if a test needs a password, ask the user to step in). Local URL and who starts the server, where the database connection is read from, useful data. -->

## In the browser
<!-- FILL-IN (if the agent uses one). E.g.: the tab is the user's; intercept requests in another tab; after 3 failed attempts, stop. -->

## If it can't be checked
<!-- FILL-IN: how to say it. E.g. "Checked: … / Not checked: …, because …". -->

## Red flags
<!-- FILL-IN: 2-3. E.g.: "should work"; "Done!" before running anything; trusting a subagent without the diff. -->
