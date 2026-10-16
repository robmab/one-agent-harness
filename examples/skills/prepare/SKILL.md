---
name: prepare
description: "Before coding: find out what really has to be done (one question at a time, each with your own guess) and, if the task is big, turn it into a short plan the user approves. Use when: you're asked to ('interview me', 'ask me', 'is this clear?', 'plan it', 'make me a plan'); a ticket doesn't make clear who it's for, why or when it's done; or the task touches 3 or more files, creates a screen or a component, or crosses layers. NOT for clear, small tasks (rename, move, a tweak) or for bugs (that's diagnose)."
---

# Interview me (and plan)

Two steps before writing code; use whichever fits:

| Situation | What you do |
|---|---|
| It isn't clear what's wanted | **Interview** |
| It's clear, but big | **Plan** |
| Both | Interview and, with the yes, plan |
| It's a bug | Neither: `diagnose` |

## Interview

What's asked for and what's needed rarely match. The essentials:

1. **Look in the repo first** at what that screen or data does today (read only).
2. **Hypothesis with a confidence %**; below ~70%, say what's missing.
3. **One question at a time, with your guess**, and wait for the answer.
4. **Summary** (what, for whom, why, done when, limit, out) once you can predict my next 3 answers.
5. **Explicit yes, then stop.**

How to do it, what's usually missing and the red flags: [interview.md](./interview.md). Read it **every time you are about to interview**.

## Plan

When it's clear what to do but it's big. **Before the first edit**, and with the tool's plan mode if it has one.

1. **Look for what already exists:** the project's shared components and a similar screen. Reuse before creating.
2. **Write the plan, 10 to 20 lines and no code:**

   ```
   GOAL: <one line; if you come from the interview, its "What">
   STEPS (in layer order, drop the ones that don't apply):
   1. migration             → files · how it's checked
   2. model                 → …
   3. endpoint (permission) → …
   4. template              → …
   5. front-end code        → …
   6. styles                → …
   REUSES: <shared components or code that already exists>
   NOT TOUCHED: <what stays out>
   RISKS: <which other screen it may break>
   ```

   Each step has to be checkable (the sensor, the screen, a query), with no "we'll see".
3. **Check it against the project:** <!-- FILL-IN: what usually gets forgotten here, e.g. cache-busting of CSS/JS, translations, the endpoint's permission, a migration --> does it reuse shared pieces?
4. **Check it against the request**, point by point: nothing more, nothing less.
5. **Show it and wait for a clear yes**, as in the interview. No code or edits in that turn.

If a step changes while building, say so before going on. When closing, the GOAL and the plan's files are the scope and intent you hand to the `reviewer`.

## Plan red flags

- Code in the plan, or steps like "adjust whatever is needed" or with no way to check them.
- A new component without looking at what's shared.
- Editing before the yes.
- Planning a tweak: one or two clear files go straight in.

---
Interview adapted from `interview-me` of [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) @ `1be8e34` (2026-10-10) (MIT). Plan inspired by `writing-plans` of [obra/superpowers](https://github.com/obra/superpowers) @ `bb92a77` (MIT).
