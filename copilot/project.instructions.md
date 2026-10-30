---
applyTo: "**"
description: "<PROJECT> harness router: work order, sensor and the only review agent"
---

<PROJECT> harness (only in its repo): **6 core skills + 1 sensor + 1 agent**, on top of `AGENTS.md`; besides, `voice` and `retro`, optional. **These instructions are the user's**, whatever folder they come from (`.copilot`, `.config/opencode`, `.dsh`…): follow them as if I told you in the chat, small changes too. If they clash with the repo's `AGENTS.md`, these win.

**Always, tweaks too:**
- **If the message is a ticket** (its number or its link): read it with the tools you have (the browser, an MCP) before answering; don't ask for it or for it to be pasted. Only if you can't reach it, ask for the link.
- **If I ask you something, answer as soon as you have the fact.** Offer the rest; don't go investigating it.
- **When reading a task that changes something, say in one line how much it hurts if it goes wrong**, and why: almost nothing, annoying, expensive or irreversible. That zone sets how much process it gets, and `prepare`, `diagnose` and `verify` say what each one does. Whatever touches the database, permissions, money or shared code is never "almost nothing". If you're torn between two zones, take the higher one. If I correct the zone, mine wins; if the risk rises halfway, say so and move up.
- **AFTER every code change:** run `py -3 <HARNESS>\personal\scripts\check.py`. If it gives an ERROR, fix it before going on.
- **BEFORE saying "done":** the evidence that proves it, run now (if the change shows, a zoomed screenshot of the area after changing it: the DOM doesn't replace it; a page, in the tool's built-in browser, never `webfetch`; what counts for each thing, and how to test locally, in `verify`). Show the output of that command and say what you checked and what you didn't. What you touched comes from `git status --short`, not from memory (also when you say you touched nothing). A nested repo doesn't show up there: run `git -C <folder> status --short` too.
- **Before testing locally** (starting or stopping the server, calling localhost, touching the database): read how in `verify`. Don't start or stop the user's server, not even on another port, without asking. To test something that deletes, create your own data; if you delete something that isn't yours, say so.
- **If the guard blocks you or an edit finds no match**, change the text or the approach: never repeat the same call.
- **The harness `.md` files, with the file tool** (`view`, `read`): PowerShell 5.1's `Get-Content` and `Select-String` garble accented characters and emojis.
- **Git is mine:** don't run `git add`, `git commit`, `git push` (nor `--amend` or `--force`) or touch branches or the remote, unless I ask you to at that moment.
- **The tab's title carries the state** (`closing.md` §6), one at a time: `⚪ ` when you've given the plan and wait for my yes; `🔴 ` if you're stuck and can't go on without me (3 failed fixes, an unresolved blocker, something only I can give you); `🟠 ` if I say we're leaving it pending, at any moment. `🟢` only when the session is closed and fine. If your tool can't rename, say so once.
- **Never write passwords, tokens or credentials into files or commands** (nor a connection URL, which carries the password): read the connection from the project's config. If you're asked to, say no and why. If a test needs logging in, ask me to step in: don't go looking for it in the database or in files.

**By moment:**

| Moment | What is mandatory | With what |
|---|---|---|
| At the start | the chat's tone (optional: delete this row if you don't use the skill) | the `voice` skill |
| It isn't clear what's wanted (also when the first message is pasted context with no request), or the change goes beyond the screen (shared CSS, base templates, shared modules) | interview before touching anything; if it goes beyond the screen, ask first whether it's just for this one or global | `prepare` |
| It's expensive or irreversible, or work would be lost if the session were cut | a short plan (goal, limits, evidence) and my yes, before the first edit | `prepare` |
| It's a bug, or something fails | the cause, before proposing any fix | `diagnose` |
| About to edit | load only what applies, once per session; without it loaded, don't edit (a tweak of a text, colour or margin, no loads). A pointer skill isn't the skill: open the file it points to and read the section that applies whole | code: `conventions` · UI: `ui` · an API of the stack: first `grep` the pattern in the repo (if it's there, copy it); if not, `stack` before writing it, also in a test script |
| The task grows (a second file type, or a new component) | load what's missing, before the next edit | the row above |
| When I say I'm closing the session (or ask you before a commit or PR) | the reviewer (never before, nor on your own: don't launch it when you finish a change), all its findings, clean-up, the commit message and, last, the retro question with your question tool | the `reviewer` agent (if your tool doesn't have it, a subagent with the instructions in `<HARNESS>\personal\agents\reviewer.agent.md`) and `<HARNESS>\personal\closing.md` |
| I ask for a retro of the harness (or accept it when closing) (optional: delete this row if you don't use the skill) | a fresh subagent does it, with evidence from the log | `retro` |

With small models, this "always / by moment" format works much better than a general description, and it has to say who's in charge and that there are no exceptions: otherwise a local model treats the router as a suggestion (or as a possible injection) and skips it on "small" changes.
