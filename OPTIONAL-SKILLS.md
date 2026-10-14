# Optional skills: the catalogue

Skills that are **interesting but not needed**, taken mostly from the two repos that fit best: [obra/superpowers](https://github.com/obra/superpowers) and [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills), both MIT-licensed. They were reviewed one by one (2026-10-11): what they add, **what signal** says it's worth adding one, and **what noise** it brings if added without need.

> **By default, none.** The core (6 skills + 1 sensor + 1 agent, see [SKILLS-GUIDE §2](SKILLS-GUIDE.md#2-what-the-core-is)) covers daily work. Every skill you add:
> - **always takes up room:** its `description` is in the catalogue even when unused;
> - **competes with the others:** the more there are, the more often the wrong one fires, especially with local models;
> - **can contradict the core:** another way of debugging, planning, reviewing…;
> - **is heavy:** the originals run from 400 to 4,900 words.
>
> An optional skill only comes in with a **concrete signal**: a failure that keeps happening or a situation that keeps coming back. Never "just in case".

---

## How to add one (if there's a signal)

1. **One at a time.** If you add three and something gets worse, you won't know which one it was.
2. **Adapt it, don't copy it:**
   - in the language you talk to the model in, and cut down to 600 words max;
   - with a narrow `description` that says **when**, with concrete words;
   - without writing into the repo;
   - with the credit "Adapted from X (MIT)" at the bottom and its copyright notice in `THIRD-PARTY-NOTICES.md`.
3. **If only the reviewer will use it** (a security or performance checklist), don't put it in `skills\`. Keep it in `personal\checklists\`, outside the catalogue, and add it to the `reviewer`'s checklist table. That way it adds no noise to the main agent.
4. **Try it for two weeks** on real work: does it come in when it should? Does it fire when it shouldn't? Is the result better?
5. **If it adds nothing, out.** Removing it costs nothing.

---

## 1. Already covered by the core: don't add

They would duplicate something that's already there, and two skills for the same moment step on each other.

| Skill (source) | Already covered by | Why not |
|---|---|---|
| `debugging-and-error-recovery` (addy) | `systematic-debugging` | same method; the core's comes from the superpowers version, which is stricter |
| `code-review-and-quality`, `requesting-code-review` (addy, sp) | `reviewer` agent | the reviewer already uses its axes |
| `interview-me` (addy) | `interview-me` | it's its source |
| `source-driven-development` (addy) | `official-sources` | it's its source |
| `verification-before-completion` (sp) | `verify-before-done` | it's its source |
| `context-engineering`, `using-agent-skills` (addy) | the harness itself | they're skills for building what's already built |

---

## 2. Optional skills that make sense

### Before coding: define and plan

| Skill (source) · words | What it adds | Add it if… | Noise otherwise |
|---|---|---|---|
| `planning-and-task-breakdown` (addy) · 1,700 | splits the work into ordered, checkable tasks | big tickets come in and the agent tries to do everything at once | on normal tickets, it plans what takes ten minutes to do |
| `writing-plans` (sp) · 1,600 | very detailed plans, with file, code and check per task | you hand long tasks to an agent that works alone | writes plans to files in the repo; lots of ceremony |
| `spec-driven-development` (addy) · 2,000 | writes the specification (PRD) before the code | big new features, with several people involved | duplicates `interview-me` on small things; paperwork |
| `idea-refine` (addy) · 1,300 | generates variants of an idea and then narrows them | you're designing something new from scratch, with no requirements | in maintenance, it opens options nobody asked for |
| `api-and-interface-design` (addy) · 2,200 | stable contracts between modules or between front and back, endpoints | you're designing a public API or an integration | in internal code, over-design |

### While coding

| Skill (source) · words | What it adds | Add it if… | Noise otherwise |
|---|---|---|---|
| `incremental-implementation` (addy) · 1,500 | changes in thin slices, each one checkable | the agent touches 15 files at once and then doesn't know what it broke | slows small changes down |
| `code-simplification` (addy) · 2,000 | simplifying without changing behaviour | there are legacy modules that get refactored often | starts "improving" what it wasn't asked to |
| `frontend-ui-engineering` (addy) · 1,600 | accessible UI (WCAG), responsive, with state handled well | accessibility is a requirement | overlaps with `ui-design`; take only the accessibility part |
| `test-driven-development` (addy or sp) · 1,500-2,400 | mandatory red-green-refactor | **there's a working test suite** and the team maintains it | without tests it's harmful: the superpowers one **deletes code written before its test** |
| `performance-optimization` (addy) · 2,500 | measure, profile and optimise (N+1, Core Web Vitals…) | there's a **measured** performance problem | optimises without measuring; better as a reviewer checklist |

### Review and close

| Skill (source) · words | What it adds | Add it if… | Noise otherwise |
|---|---|---|---|
| `receiving-code-review` (sp) · 900 | checks every review comment before applying it; no "you're right!" | you get lots of PR comments or comments from other reviewers and the agent applies them blindly | you already decide what gets applied from the `reviewer` |
| `security-and-hardening` (addy) · 2,500 | threat model, OWASP, secrets, file uploads, AI features | the project handles sensitive data or payments, or exposes APIs | the reviewer already has a security axis; better as its **checklist** |
| `git-workflow-and-versioning` (addy) · 2,200 | atomic commits, branches, splitting messy work into clean commits | you hand commits and branches to the agent | its `description` says "any code change": it would always fire |
| `finishing-a-development-branch` (sp) · 1,300 | when done: merge, PR, keep or discard the branch | you work with many short branches | assumes there are tests and worktrees |
| `documentation-and-adrs` (addy) · 1,600 | writing down architecture decisions (ADRs) | big decisions get made that later nobody remembers | documents trivial things |

### Production and infrastructure

| Skill (source) · words | What it adds | Add it if… | Noise otherwise |
|---|---|---|---|
| `deprecation-and-migration` (addy) · 2,000 | retiring code or APIs; zero-downtime database migrations (expand/contract) | a big migration is under way (of version, schema, system) | doesn't apply day to day |
| `observability-and-instrumentation` (addy) · 2,200 | logs, metrics, traces and alerts | there are production problems that can't be diagnosed | fills the code with logs |
| `ci-cd-and-automation` (addy) · 1,600 | pipelines, quality gates in CI | CI is being set up or changed | if there's no CI to touch, doesn't apply |
| `shipping-and-launch` (addy) · 1,800 | go-live checklist, phased rollout, rollback | there are risky launches | if deployment is routine, doesn't apply |
| `browser-testing-with-devtools` (addy) · 2,100 | testing in a real browser: DOM, console, network, performance | Copilot or a tool with no browser, **with the chrome-devtools MCP** installed | Claude already has its own browser; without the MCP it doesn't work |

### Meta: for writing skills

| Skill (source) · words | What it adds | Recommended use |
|---|---|---|
| `writing-skills` (sp) · 3,800 | how to write skills that fire well; testing them as if they were tests | **reading only**, when writing a new skill; the essentials are already in README §4 |
| `skill-creator` ([anthropics/skills](https://github.com/anthropics/skills)) | the official format guide | same: as reading; check its licence before copying anything (not all of that repo is MIT) |

---

## 3. Discouraged: they hurt

Even though they come from very popular repos, they clash with this harness's design:

| Skill (source) | Why not |
|---|---|
| `brainstorming` (sp) | its `description` is "**MUST** before any creative work": it fires on almost everything and slows things down |
| `using-superpowers` (sp) | forces skills to be invoked **before any answer**, even to ask a question; pure noise |
| `subagent-driven-development`, `executing-plans`, `dispatching-parallel-agents` (sp) | a multi-agent flow with plans in files (the first has 4,900 words): the exact opposite of "a single agent" |
| `using-git-worktrees` (sp) | creates worktrees and branches on its own |
| `constraint-driven-development` (addy) | writes a `CONSTRAINTS.md` into the repo and watches the diff; 3,500 words |
| `doubt-driven-development` (addy) | does the adversarial review by calling the Codex or Gemini CLIs; that's what the `reviewer` is for |
| `diagnosing-superpowers` (sp) | only useful if you use all of superpowers |
| **Whole packages** (superpowers, ECC, BMAD, GStack, SuperClaude) | hundreds of skills or a complete method that replaces yours; see [RESEARCH](RESEARCH.md) |

---

## 4. Our own, on hold

They don't come from any repo: they're ideas that came up while designing the harness and stay out **until something really fails**:

| Idea | It would be done if… |
|---|---|
| **Commit messages** in the team's format | you hand commits to the agent and there's an agreed format (if everyone writes them their own way, there's nothing to pin down) |
| **Ticket plan** in slices, in stack order | big tickets go wrong from being done all at once (see `planning-and-task-breakdown`) |
| **Translations** (extract, edit and compile) | the cycle fails often (quotes, catalogues not recompiled) |
| **Migration or new database field**, end to end | the agent skips steps when adding fields |
| **Skills for one module or screen** | you work on that screen often and the agent reinvents its components: an on-demand pointer with a very precise `description` |

Before writing any of these, see whether the failure fits as a **rule in `check.py`**: it's more reliable and takes no context.
