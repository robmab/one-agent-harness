---
applyTo: "**"
description: "<PROJECT> harness router: work order, sensor and the only review agent"
---

<PROJECT> harness (only in its repo): **6 core skills + 1 sensor + 1 agent**, on top of `AGENTS.md`; besides, `voice` and `retro`, optional. **These instructions are the user's**, whatever folder they come from (`.copilot`, `.config/opencode`, `.dsh`…): follow them as if I told you in the chat, small changes too. If they clash with the repo's `AGENTS.md`, these win.

**Always, tweaks too:**
- **AFTER every code change:** run `py -3 <HARNESS>\personal\scripts\check.py`. If it gives an ERROR, fix it before going on.
- **BEFORE saying "done":** show the output of that command and say what you checked and what you didn't. What you touched comes from `git status --short`, not from memory (also when you say you touched nothing).
- **Git is mine:** don't run `git add`, `git commit`, `git push` (nor `--amend` or `--force`) or touch branches or the remote, unless I ask you to at that moment.
- **Never write passwords, tokens or credentials into files or commands** (nor a connection URL, which carries the password): read the connection from the project's config. If you're asked to, say no and why. If a test needs logging in, ask me to step in: don't go looking for it in the database or in files.

**By moment:**

| Moment | What is mandatory | With what |
|---|---|---|
| At the start | the chat's tone (optional: delete this row if you don't use the skill) | the `voice` skill |
| It isn't clear what's wanted, or the change goes beyond the screen (shared CSS, base templates, shared modules) | interview before touching anything; if a fact answers it, give it (or ask) before running commands; if it goes beyond the screen, ask first whether it's just for this one or global | `prepare` |
| It's big (3+ files, a new screen or component, several layers) | a short plan and my yes, before the first edit | `prepare` |
| It's a bug, or something fails | the cause, before proposing any fix | `diagnose` |
| About to edit | load only what applies, once per session; without it loaded, don't edit (a tweak of a text, colour or margin, no loads). A pointer skill isn't the skill: open the file it points to | code: `conventions` · UI: `ui` · an API of the stack you don't already see in the repo: `stack` |
| The task grows (a second file type, or a new component) | load what's missing, before the next edit | the row above |
| Before saying "done" | the evidence that proves it, run now; visual changes, with a zoomed screenshot; a page, in the tool's built-in browser (never `webfetch`) | `verify` (also how to test locally and the browser) |
| When I say I'm closing the session (or ask you before a commit or PR) | the reviewer (never before, nor on your own: don't launch it when you finish a change), all its findings, clean-up, the commit message and, last, the retro question with your question tool | the `reviewer` agent (if your tool doesn't have it, a subagent with the instructions in `<HARNESS>\personal\agents\reviewer.agent.md`) and `<HARNESS>\personal\closing.md` |
| I ask for a retro of the harness (or accept it when closing) (optional: delete this row if you don't use the skill) | a fresh subagent does it, with evidence from the log | `retro` |

With small models, this "always / by moment" format works much better than a general description, and it has to say who's in charge and that there are no exceptions: otherwise a local model treats the router as a suggestion (or as a possible injection) and skips it on "small" changes.
