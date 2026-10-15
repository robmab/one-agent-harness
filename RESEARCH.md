# Research: where this template comes from

🌐 **English** · [Español](RESEARCH.es.md)

Research done on 2026-10-10 (the stars are from the GitHub API that day). It explains what a harness is, what's on GitHub and why the template carries exactly these pieces. How to set it up is in the [README](README.md); what each piece does, in the [SKILLS-GUIDE](SKILLS-GUIDE.md).

---

## 1. What a "harness" is

Agent = model + harness. The harness is everything around the model, and it has two kinds of pieces (Martin Fowler):

| Type | What it is | Examples | In the template |
|---|---|---|---|
| **Guides** | what reaches the agent *before* it acts | `AGENTS.md`, skills | knowledge and process skills |
| **Judgement sensors** | another model reviews *afterwards* | reviewer agent | `reviewer` (just one) |
| **Automatic sensors** | fixed, cheap and deterministic checks *afterwards* | linters, tests, hooks | `check.py` + hook |

Key ideas from the sources:
- **You need both:** guides alone give rules nobody checks; sensors alone, an agent that repeats mistakes.
- **`AGENTS.md` is already the cross-tool standard** (a study of 2,853 repos). Keep it short and add each rule only after a real failure.
- **What's portable** between tools is `AGENTS.md`, the `SKILL.md` files, linters and CI. The less that depends on a single tool, the better.
- **The harness matters more than the model:** changing it moves results more than many model changes, and what works with one model doesn't carry over to the next. With small models, less is more.
- **Skills load through their `description`:** at first only the name and description go up; the rest, when the model decides it applies. The `description` is what rules.

## 2. The GitHub landscape

### Skill and methodology packages

| Repo | ⭐ | What it is | When it fits |
|---|---|---|---|
| obra/superpowers | 297k | a complete method: brainstorming, plan, mandatory TDD, subagents, review (MIT) | projects with tests; piece by piece if there are none |
| affaan-m/ECC | 276k | a mega-package: 284 skills and 68 subagents | almost never: it eats the context |
| anthropics/skills | 180k | reference skills for the format and for documents | to learn the format |
| garrytan/gstack | 136k | 23 roles (CEO, QA, release…) | a solo product, Claude only |
| addyosmani/agent-skills | 104k | 25 engineering skills, portable to over 70 agents (MIT) | almost always, taking loose pieces |
| wshobson/agents | 40k | an agent marketplace for several tools | to take the odd agent |
| SuperClaude | 24k | personas and commands | an old approach |

### Spec-driven development (SDD)

| Repo | ⭐ | What it is | When it fits |
|---|---|---|---|
| github/spec-kit | 141k | GitHub's own, native to Copilot; adds `.specify/` to the repo | new projects; Python 3.11 + uv |
| Fission-AI/OpenSpec | 72k | lightweight, designed for existing code; adds `openspec/` | legacy code with big features; a team decision |
| gsd-build/get-shit-done | 64k | plans in waves with a clean context | stalled since May 2026 |
| BMAD-METHOD | 54k | simulates a whole agile team | very heavy (people talk of months to master it) |

**Conclusion:** no whole framework. The pieces that pay off are few, short and adapted to the project, plus an automatic sensor. SDD (spec-kit, OpenSpec) only if the whole team adopts it, because it writes into the repo.

## 3. The template's pieces

**Why these:** the knowledge skills (conventions, design, style) say **how code is written** and **how to talk**. None covers **how the agent works**: understanding before building, diagnosing before fixing, proving before saying "done", or reviewing correctness, security or performance. That's what the adapted pieces add.

| Piece | Source | Gap it fills | Adaptation |
|---|---|---|---|
| `verify-before-done` | superpowers `verification-before-completion` | the agent says "done" without having run anything | a table of the project's commands and an honest «Not checked» |
| `systematic-debugging` | superpowers `systematic-debugging` | blind fixes, patches over the symptom | no mandatory test: a reproduction will do; a table of the project's layers |
| `interview-me` | addyosmani `interview-me` + the idea of superpowers `writing-plans` | ambiguous tickets the agent fills in by inventing; big tasks discovered on the fly | look at the repo first; questions for the customer; no files in the repo; a short plan without code for big tasks, inside the same skill |
| `official-sources` | addyosmani `source-driven-development` | code from memory for the wrong version | the repo as the first source; a table of versions and traps |
| `reviewer` (the only agent) | addyosmani `code-review-and-quality` | nobody reviews correctness, security or performance | 6 axes with the conventions included; reads the knowledge skills as checklists; clean context; doesn't edit; runs the sensor first |
| `check.py` + hook | our own | important rules depended on the model's memory | stack regexes + syntax, after every edit |

**A single agent:** the trend of having many specialised reviewers is rejected. Every subagent starts with no context, spends more tokens and goes over the same diff again. A new agent only pays off for fresh eyes, different permissions or to isolate heavy work. A "reviewer for X" is written as a skill (checklist) that the `reviewer` reads.

**In the template they ship as ideas, not as finished skills** (since v0.4.1): each one keeps its concept (the gap it fills, from the table above) and leaves its sections as `FILL-IN`. No harness is good for every project, but the structure is; the adapted versions stay complete in [examples](examples/README.md), as the starting point.

**Tested in practice** (in the project where the template was born):
- a local model wrote syntax from a later version even though the skill forbade it: it only followed it when invoked by hand;
- a strong model got it right, but said "validated" without checking anything;
- with Claude and the skills, the result came out right and checked in the browser;
- the hook caught the error on the exact line, with no false positives.

### Discarded
- `brainstorming`: it's "MUST before anything creative", too invasive; `interview-me` covers the useful part.
- `test-driven-development`, `writing-plans`, `executing-plans`, `subagent-driven-development`: mandatory TDD, worktrees and heavy plans. They may make sense in a project with a good test base. From `writing-plans` only the idea came in: a short plan for big tasks, inside `interview-me`.
- `doubt-driven-development`: relies on the Codex and Gemini CLIs.
- `constraint-driven-development`: writes `CONSTRAINTS.md` into the repo.
- `context-engineering`: it's what this template does.
- `code-simplification`, `incremental-implementation`, `deprecation-and-migration`: they overlap or are for one-off use.
- Receiving reviews, commits and ticket plans: noise for the daily flow. On hold until something really fails.

### Rules for adapting an outside skill
- In the language you talk to the model in and cut down (the originals run from 600 to 3,300 words; target ≤ 600), with the `description` tuned so it fires when it should and not always.
- Credit at the bottom: "Adapted from <skill> of <repo> (MIT)".
- It must not write anything into the repo (no plans, intents or worktrees).
- Test it in Claude and in Copilot, with a local model too, before trusting the next one.

## Sources
- Martin Fowler, *Harness engineering for coding agent users*: https://martinfowler.com/articles/harness-engineering.html
- Addy Osmani, *Agent Harness Engineering*: https://addyosmani.com/blog/agent-harness-engineering/
- arXiv, *Harness Engineering for Agentic AI Coding Tools*: https://arxiv.org/html/2602.14690v5
- best-of-Agent-Harnesses: https://github.com/ryanalberts/best-of-agent-harnesses (and its skill pack comparison)
- Spec Kit vs BMAD vs OpenSpec: https://dev.to/willtorber/spec-kit-vs-bmad-vs-openspec-choosing-an-sdd-framework-in-2026-d3j
- Repos: obra/superpowers, addyosmani/agent-skills, github/spec-kit, Fission-AI/OpenSpec
