---
name: prepare
description: "Before coding: find out what really has to be done (one question at a time, each with your own guess) and, if the task is big, turn it into a short plan the user approves. Use when: you're asked to ('interview me', 'ask me', 'is this clear?', 'plan it', 'make me a plan'); a ticket doesn't make clear who it's for, why or when it's done; or the task touches 3 or more files, creates a screen or a component, or crosses layers. NOT for clear, small tasks (rename, move, a tweak) or for bugs (that's diagnose)."
---

# Prepare

**CONCEPT:** everything that happens before writing code, in one skill: find out what is really wanted and, if the task is big, a short plan the user approves. It stops the agent from filling gaps by inventing them.

> **PROFILE · web.** General web rules, valid for most stacks. Adjust the lines marked `TUNE` to yours and then remove the mark.

Pick the branch and **read only its detail**:

| Situation | Branch | Detail |
|---|---|---|
| It isn't clear what's wanted | **Interview** | [interview.md](./interview.md) |
| It's clear, but big (3+ files, a new screen or component, several layers) | **Plan** | [plan.md](./plan.md) |
| Both | Interview and, with the yes, plan | both, in that order |
| It's a bug | Neither: `diagnose` | — |
| A clear tweak (one or two files) | Neither: straight in | — |

**Always open the branch's detail before starting:** that's where how it's done lives.

---
Interview adapted from `interview-me` of [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) @ `1be8e34` (2026-10-10) (MIT). Plan inspired by `writing-plans` of [obra/superpowers](https://github.com/obra/superpowers) @ `bb92a77` (MIT).
