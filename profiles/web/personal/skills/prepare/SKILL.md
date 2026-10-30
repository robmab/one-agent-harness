---
name: prepare
description: "Before coding: find out what really has to be done (one question at a time, each with your own guess) and, if it hurts when it goes wrong, turn it into a short plan the user approves. Use when: you're asked to ('interview me', 'ask me', 'is this clear?', 'plan it', 'make me a plan'); a ticket doesn't make clear who it's for, why or when it's done; or the task is expensive or irreversible if it goes wrong, or work would be lost if the session were cut. NOT for tasks that barely hurt (rename, move, a tweak) or for bugs (that's diagnose)."
---

# Prepare

**CONCEPT:** everything that happens before writing code, in one skill: find out what is really wanted and, if it hurts when it goes wrong, a short plan the user approves. It stops the agent from filling gaps by inventing them.

> **PROFILE · web.** General web rules, valid for most stacks. Adjust the lines marked `TUNE` to yours and then remove the mark.

**First, the zone** you gave when reading the task (if you didn't, give it now). It decides how much of this skill applies:

| If it goes wrong, it hurts… | What you do |
|---|---|
| Almost nothing | Nothing from here: straight in |
| Annoying | One line of plan; interview only if in doubt |
| Expensive | The whole **Plan**: goal, limits and evidence, and the user's yes |
| Irreversible | The same, plus what can go wrong, how to go back and what the user runs |

**The test:** if the session were cut now, could someone else finish it from the request and the diff? If not, it's at least expensive. File counts don't decide the zone.

Pick the branch and **read only its detail**:

| Situation | Branch | Detail |
|---|---|---|
| It isn't clear what's wanted | **Interview** | [interview.md](./interview.md) |
| It's expensive or irreversible | **Plan** | [plan.md](./plan.md) |
| Both | Interview and, with the yes, plan | both, in that order |
| It's a bug | `diagnose`; if the fix is expensive or irreversible, then **Plan** | [plan.md](./plan.md) |
| Almost nothing, or annoying and clear | Neither: straight in (if annoying, with its line of plan) | — |

**Always open the branch's detail before starting:** that's where how it's done lives.

---
Interview adapted from `interview-me` of [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) @ `1be8e34` (2026-10-10) (MIT). Plan inspired by `writing-plans` of [obra/superpowers](https://github.com/obra/superpowers) @ `bb92a77` (MIT).
