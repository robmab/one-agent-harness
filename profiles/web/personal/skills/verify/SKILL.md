---
name: verify
description: "Before saying something is done, fixed or working, run the check and show the result; if it can't be checked, say so. Use when: you're about to finish a task, say a bug is fixed or that something passes, say something is already done, already exists or is already in production, or before a commit or PR."
---

# Verify before done

**CONCEPT:** no "done" without a check run in this very message. If you haven't just run the command and read its output, you can't claim it.

> **PROFILE · web.** General web rules, valid for most stacks. Adjust the lines marked `TUNE` to yours and then remove the mark.

## Before claiming anything

1. **What proves it:** pick the command or test that confirms the claim (table below).
2. **Run it in full**, now; don't trust an earlier run.
3. **Read the whole output:** exit code, errors and warnings.
4. **Does it confirm what you were going to say?** If yes, say it with the evidence. If not, say the real state.

## What proves each thing in <PROJECT>

| Claim | Evidence | Doesn't count |
|---|---|---|
| Fits the stack and compiles | `py -3 <HARNESS>\personal\scripts\check.py [files]`: 0 errors; review the warnings | "I did it carefully" |
| Audit a **whole** file, old code included ("audit this file", before refactoring) | the same command with `--all <file>`; if there are many, **summarise them by rule** | reviewing only what changed |
| Tests pass | <!-- TUNE: test command --> with 0 failures | "they should pass" |
| The screen works | load it with the server running: no errors in the console and no failed requests in Network | the template compiling |
| It looks right (borders, shadows, overlaps) | a zoomed screenshot, at rest and in the state that was touched (open, hover, error) | measurements only |
| A control you can't photograph (an open `<select>`, a default value) | the DOM (`options`, `selected`, `value`) and a clean console | "it looks fine" |
| It works on mobile | the same screen at phone width (~375px): no horizontal scroll, nothing overlapping | "it's responsive" |
| The endpoint answers | its response in Network: the expected status and body | "the screen shows it" |
| Permissions hold | a user without the permission doesn't get in: the endpoint refuses, not only the button hides | "the button is hidden" |
| Bug fixed | a test that failed before the fix and passes now; without tests, repeat the steps of the original symptom | "I changed the code" |
| Same as something that exists (function, endpoint, query) | compared with **that one**, called or copied as is, on a case that isn't 0 | a hand-rewritten query |
| A subagent did it | look at the `git diff` yourself | trusting its report |
| It does what was asked | reread the request point by point | it compiling |
| Something is "already there", even in production | `git branch -a --contains <sha>`: say which branch | the commit on your branch |
| <!-- TUNE: lint, build, migrations, translations… --> | | |

**Careful:** touching the database or a shared environment is valid evidence, but **ask first**.

## Testing locally

No credentials here: if a test needs a password, ask the user to step in.
- **App:** <!-- TUNE: local URL; who starts the server -->
- **Database:** <!-- TUNE: where its connection is read from -->: never print it.
- **Useful data and tricks:** <!-- TUNE: users with each role, records that cover the edge cases -->

## In the browser

- **The tab is the user's**: don't resize it or leave it on another view.
- **Intercepting requests:** in another tab, removed when done (`page.unrouteAll()`).
- **Three failed attempts at the same thing: stop** and look for the root cause (`diagnose`) or ask.

## If it can't be checked

**Say it clearly**, separating what was checked from what wasn't:

```
Checked: syntax of services/orders.py (check.py OK).
Not checked: the edit screen, the server isn't running. To see it: <steps>.
```

## Signs you're skipping this

- Writing "should work", "probably", "it seems" or "in principle".
- A "Done!" or "Perfect!" before running anything.
- Going for a commit or PR without checking.
- Thinking "just this once it's not needed".

If so, stop: back to step 1.

---
Adapted from `verification-before-completion` of [obra/superpowers](https://github.com/obra/superpowers) @ `bb92a77` (2026-10-10) (MIT).
