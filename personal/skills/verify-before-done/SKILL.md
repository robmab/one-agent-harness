---
name: verify-before-done
description: "Before saying something is done, fixed or working, run the check and show the result; if it can't be checked, say so. Use when: you're about to finish a task, say a bug is fixed or that something passes, or before a commit or PR."
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
| Bug fixed | repeat the steps of the original symptom and it no longer shows | "I changed the code" |
| A subagent did it | look at the `git diff` yourself | trusting its report |
| It does what was asked | reread the request point by point | it compiling |
| <!-- FILL-IN: lint, build, migrations, translations… --> | | |

**Careful:** anything that touches the database or a shared environment is valid evidence, but **always ask for permission first**.

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
