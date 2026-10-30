<PROJECT> harness (only in its repo): **6 core skills + 1 sensor + 1 agent**, on top of `AGENTS.md`; besides, `voice` and `retro`, optional.

**Always, tweaks too:**
- **If the message is a ticket** (its number or its link): read it with the tools you have (the browser, an MCP) before answering; don't ask for it or for it to be pasted. Only if you can't reach it, ask for the link.
- **If the user asks something, answer as soon as you have the fact.** Offer the rest; don't go investigating it.
- **After every edit** the sensor (`check`) runs through the hook and leaves a line (`OK`, warnings or ERROR). If it gives an ERROR, fix it before going on. Don't rerun it by hand: to show it, its last output is enough.
- **Before saying "done"**, the evidence that proves it, run now (if the change shows, a zoomed screenshot of the area after changing it: the DOM doesn't replace it; what counts for each thing, and how to test locally, in `project:verify`), and what you checked and what you didn't. What you touched comes from `git status --short`, not from memory (also when you say you touched nothing). A nested repo doesn't show up there: run `git -C <folder> status --short` too.
- **Before testing locally** (starting or stopping the server, calling localhost, touching the database): read how in `project:verify`. Don't start or stop the user's server, not even on another port, without asking. To test something that deletes, create your own data; if you delete something that isn't yours, say so.
- **If the guard blocks you or an edit finds no match**, change the text or the approach: never repeat the same call.
- **Git belongs to the user:** no `git add`, `commit`, `push` (nor `--amend` or `--force`) and no touching branches, unless asked at that moment.
- **The tab's title carries the state** (`closing.md` §6), one at a time: `⚪ ` when you've given the plan and wait for the user's yes; `🔴 ` if you're stuck and can't go on without them (3 failed fixes, an unresolved blocker, something only they can give you); `🟠 ` if they say they're leaving it pending, at any moment. `🟢` only when the session is closed and fine. If your tool can't rename, say so once.
- **Never write passwords, tokens or credentials into files or commands** (nor a connection URL): read the connection from the project's config. If a test needs one, ask the user to step in.

**By moment:**

| Moment | What is mandatory | With what |
|---|---|---|
| At the start | the chat's tone (optional: delete this row if you don't use the skill) | `project:voice` |
| It isn't clear what's wanted (also when the first message is pasted context with no request), or the change goes beyond the screen (shared CSS, base templates, shared modules) | interview before touching anything; if it goes beyond the screen, ask first whether it's just for this one or global | `project:prepare` |
| It's big (3+ files, a new screen or component, several layers) | a short plan and the user's yes, before the first edit | `project:prepare` |
| It's a bug, or something fails | the cause, before proposing any fix | `project:diagnose` |
| About to edit | load only what applies (a tweak of a text, colour or margin, no loads); if a skill is a pointer, open the file it points to and read the section that applies whole | code: `project:conventions` · UI: `project:ui` · an API of the stack: first `grep` the pattern in the repo (if it's there, copy it); if not, `project:stack` before writing it, also in a test script |
| The task grows (a second file type, or a new component) | load what's missing, before the next edit | the row above |
| When the user says they're closing (or asks before a commit or PR) | the reviewer (never before: the guard blocks it), all its findings to the user, clean-up, the commit message and, last, the retro question with `AskUserQuestion` | `project:reviewer` and `<HARNESS>\personal\closing.md` |
| The user asks for a retro of the harness (or accepts it when closing) (optional: delete this row if you don't use the skill) | a fresh subagent does it, with evidence from the log | `project:retro` |
