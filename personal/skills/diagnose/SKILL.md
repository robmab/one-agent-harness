---
name: diagnose
description: "Debug by finding the root cause before touching anything: reproduce, follow the data through the application layers and one hypothesis at a time. Use when: a bug, an error or stack trace, something that doesn't work, comes out empty or behaves oddly, an install or environment error (pip, venv, DLL, wrong interpreter), a tool that's missing or won't connect, or a previous fix didn't work; before proposing any fix."
---

# Systematic debugging

> **CONCEPT:** no root cause, no fix. Patching the symptom is a failure even if it goes away; without this, the agent piles up guesses and breaks something else by the third try.

> **TEMPLATE · FILL-IN** each section. Full example: [examples/skills/diagnose](../../../examples/skills/diagnose/SKILL.md). Once filled in, delete this block.

**First, the zone** you gave when reading the bug (if you didn't, give it now). No cause means no fix in any of them; what changes is how much you have to show:

| If it goes wrong, it hurts… | What you require |
|---|---|
| Almost nothing | The cause, seen and said in one sentence |
| Annoying | Reproducing it and showing the cause |
| Expensive | The above, which fact of the case it explains, and written evidence before fixing |
| Irreversible | The same, how to go back, and the fix waits for the user's yes |

## 1. Investigate

| Layer | How to look at it |
|---|---|
| <!-- FILL-IN: e.g. Database --> | <!-- e.g. a read-only query --> |
| <!-- FILL-IN: e.g. API --> | <!-- e.g. the response in the Network tab --> |

<!-- FILL-IN: before the layers, e.g.: read the whole error, reproduce it, look at what changed (git log), and ask before swapping a field the ticket names that doesn't exist. -->

## 2. Compare with something that works
<!-- FILL-IN: e.g. find something similar in the repo that works and list every difference. -->

## 3. One hypothesis at a time
<!-- FILL-IN: e.g. "I think it's X because Y", tested with the smallest change; before calling it the bug, which fact of the case it explains. -->

## 4. Fix
<!-- FILL-IN: e.g. one change at the source; if the project has tests, the reproduction becomes a regression test; after 3 failed fixes, stop and rethink. -->

## Project traps
<!-- FILL-IN: what fails silently here (cache, data, a server that stays down…). -->

## Red flags
<!-- FILL-IN: 2-3. E.g.: "let me try X and see"; several changes at once. -->
