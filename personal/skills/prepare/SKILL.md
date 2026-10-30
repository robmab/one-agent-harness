---
name: prepare
description: "Before coding: find out what really has to be done (one question at a time, each with your own guess) and, if it hurts when it goes wrong, turn it into a short plan the user approves. Use when: you're asked to ('interview me', 'ask me', 'is this clear?', 'plan it'); a ticket doesn't make clear who it's for, why or when it's done; or the task is expensive or irreversible if it goes wrong, or work would be lost if the session were cut. NOT for tasks that barely hurt or for bugs (that's diagnose)."
---

# Interview me (and plan)

> **CONCEPT:** everything that happens before writing code, in one skill. What's asked for and what's needed rarely match, and the cheap moment to find out is before coding; if it hurts when it goes wrong, it gets a short plan the user approves before the first edit. It stops the agent from filling gaps by inventing them.

> **TEMPLATE · FILL-IN** each section. Full example: [examples/skills/prepare](../../../examples/skills/prepare/SKILL.md). Once filled in, delete this block.

**First, the zone** you gave when reading the task (if you didn't, give it now). It decides how much of this skill applies:

| If it goes wrong, it hurts… | What you do |
|---|---|
| Almost nothing | Nothing from here: straight in |
| Annoying | One line of plan; interview only if in doubt |
| Expensive | The whole **Plan**: goal, limits and evidence, and the user's yes |
| Irreversible | The same, plus what can go wrong, how to go back and what the user runs |

**The test:** if the session were cut now, could someone else finish it from the request and the diff? If not, it's at least expensive. File counts don't decide the zone.

| Situation | What you do |
|---|---|
| It isn't clear what's wanted | **Interview** |
| It's expensive or irreversible | **Plan** |
| It's a bug | `diagnose`; if the fix is expensive or irreversible, then **Plan** |

## Interview
<!-- FILL-IN: how to ask. E.g.: look in the repo first at what it does today; one question at a time, each with your guess; a summary with an "Out" line; an explicit yes, then stop. -->

## What's usually missing
<!-- FILL-IN: what this project's tickets leave out. E.g.: which role, which customers, a new field (migration), how we'll know it's right. -->

## Plan
<!-- FILL-IN: always goal, limits and evidence (what shows it's done), and one step at a time, each checked before the next. the shape of a plan. E.g.: 10-20 lines, no code; steps in layer order, each with how it's checked; what it reuses; what isn't touched; the user's yes before editing; when done, what was built checked against the steps. -->

## Red flags
<!-- FILL-IN: 2-3. E.g.: two questions in one message; coding before the yes; planning a one-file tweak. -->
