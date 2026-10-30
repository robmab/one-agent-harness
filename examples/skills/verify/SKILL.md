---
name: verify
description: "Before saying something is done, fixed or working, run the check and show the result; if it can't be checked, say so. Use when: you're about to finish a task, say a bug is fixed or that something passes, say something is already done, already exists or is already in production, or before a commit or PR."
---

# Verify before done

**Iron rule: no "done" without a check run in this very message.** If you haven't just run the command and read its output, you can't claim it.

> **TEMPLATE · FILL-IN** the table rows with the project's real commands. The rest works as is. Once filled in, delete this block.

## Before claiming anything

1. **What proves it:** pick the command or test that confirms the claim (table below).
2. **Run it in full**, now; don't trust an earlier run.
3. **Read the whole output:** exit code, errors and warnings.
4. **Does it confirm what you were going to say?** If yes, say it with the evidence. If not, say the real state.

## What proves each thing in <PROJECT>

| Claim | Evidence | Doesn't count |
|---|---|---|
| Fits the stack and compiles | `py -3 <HARNESS>\personal\scripts\check.py [files]` (no files: what changed in git; only the changed lines): 0 errors; review the warnings | "I did it carefully" |
| Audit a **whole** file, old code included ("audit this file", "what breaks the conventions?", before refactoring) | the same command with `--all <file>`; if there are many, **summarise them by rule** instead of listing them one by one | reviewing only what changed |
| Tests pass | <!-- FILL-IN: test command --> with 0 failures | "they should pass" |
| The screen works | load the page with the server running and look at the browser console | the template compiling |
| It looks right (borders, shadows, overlaps) | a zoomed screenshot, at rest and in the failing state | measurements only |
| A control you can't photograph (an open `<select>`, a default value) | the DOM (`options`, `selected`, `value`) and a clean console | "it looks fine" |
| Bug fixed | repeat the steps of the original symptom and it no longer shows | "I changed the code" |
| It gives the same as something that already exists (another function, an endpoint, a query) | compare with **that** one by calling it, or with its query copied as is; and with a case that doesn't give 0 | a query rewritten by hand "in the style of": it tests your reading of the code, not the code |
| A subagent did it | look at the `git diff` yourself | trusting its report |
| It does what was asked | reread the request point by point | it compiling |
| Something is "already there", even in production | `git branch -a --contains <sha>`: say which branch | the commit on your branch |
| <!-- FILL-IN: lint, build, migrations, translations… --> | | |

**Careful:** anything that touches the database or a shared environment is valid evidence, but **always ask for permission first**.

## Testing locally

<!-- FILL-IN: no credentials here (if a test needs a password, ask the user to step in). -->
- **App:** <!-- FILL-IN: local URL; who starts the server -->
- **Database:** <!-- FILL-IN: where its connection is read from -->
- **Useful data and tricks:** <!-- FILL-IN -->
- **Throwaway scripts** (a query, a check): in the temp folder, reading the connection from the config file; **never print it** (it carries the password). Delete them all when the task is done. To tweak one, use Edit (it fails if it doesn't find the text), not a `str.replace` from another script (silent if nothing changes).

## In the browser

- **The tab is the user's**: don't resize it or leave it on another view.
- **Intercepting requests:** in another tab, removed when done (`page.unrouteAll()`). If something hangs, suspect your instrumentation first.
- **Three failed attempts at the same thing: stop** and look for the root cause (`diagnose`) or ask.

## If it can't be checked

It happens a lot: there are no tests, the server isn't running or data is missing. That's fine, but **say it clearly** and separate what was checked from what wasn't:

```
Checked: syntax of services/orders.py (check.py OK).
Not checked: the edit screen, the server isn't running. To see it: <steps>.
```

## Signs you're skipping this

- Writing "should work", "probably", "it seems" or "in principle".
- A "Done!" or "Perfect!" before running anything.
- Going for a commit or PR without checking.
- Thinking "just this once it's not needed".
- Accepting a subagent's report without looking at the diff.

If you catch yourself in one, stop and go back to step 1.

| Excuse | Reality |
|---|---|
| "I'm sure" | Being sure isn't evidence |
| "It's a small change" | Small ones break things too |
| "I already tested it" | Before doesn't count; it has to be after the last change |
| "It compiles" or "the editor doesn't complain" | Compiling isn't working |

---
Adapted from `verification-before-completion` of [obra/superpowers](https://github.com/obra/superpowers) @ `bb92a77` (2026-10-10) (MIT).
