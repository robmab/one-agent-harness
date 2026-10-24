<PROJECT> harness (only in its repo): **6 core skills + 1 sensor + 1 agent**, on top of `AGENTS.md`; besides, `voice` and `retro`, optional.

**Always, tweaks too:**
- **After every edit** the sensor (`check`) runs through the hook and leaves a line (`OK`, warnings or ERROR). If it gives an ERROR, fix it before going on. Don't rerun it by hand: to show it, its last output is enough.
- **Before saying "done"**, show what you checked and what you didn't. What you touched comes from `git status --short`, not from memory (also when you say you touched nothing).
- **Git belongs to the user:** no `git add`, `commit`, `push` (nor `--amend` or `--force`) and no touching branches, unless asked at that moment.
- **Never write passwords, tokens or credentials into files or commands** (nor a connection URL): read the connection from the project's config. If a test needs one, ask the user to step in.

**By moment:**

| Moment | What is mandatory | With what |
|---|---|---|
| At the start | the chat's tone (optional: delete this row if you don't use the skill) | `project:voice` |
| It isn't clear what's wanted, or the change goes beyond the screen (shared CSS, base templates, shared modules) | interview before touching anything; if a fact answers it, give it (or ask) before running commands; if it goes beyond the screen, ask first whether it's just for this one or global | `project:prepare` |
| It's big (3+ files, a new screen or component, several layers) | a short plan and the user's yes, before the first edit | `project:prepare` |
| It's a bug, or something fails | the cause, before proposing any fix | `project:diagnose` |
| About to edit | load only what applies (a tweak of a text, colour or margin, no loads); if a skill is a pointer, open the file it points to | code: `project:conventions` · UI: `project:ui` · an API of the stack you don't already see in the repo: `project:stack` |
| The task grows (a second file type, or a new component) | load what's missing, before the next edit | the row above |
| Before saying "done" | the evidence that proves it, run now; visual changes, with a zoomed screenshot | `project:verify` (also how to test locally and the browser) |
| When the user says they're closing (or asks before a commit or PR) | the reviewer (never before: the guard blocks it), all its findings to the user, clean-up, the commit message and, last, the retro question with `AskUserQuestion` | `project:reviewer` and `<HARNESS>\personal\closing.md` |
| The user asks for a retro of the harness (or accepts it when closing) (optional: delete this row if you don't use the skill) | a fresh subagent does it, with evidence from the log | `project:retro` |
