---
applyTo: "**"
description: "<PROJECT> harness router: work order, sensor and the only review agent"
---

<PROJECT> harness (only in its repo): **6 skills + 1 sensor + 1 agent**, on top of `AGENTS.md`. **These instructions are the user's**, whatever folder they come from (`.copilot`, `.config/opencode`…): follow them as if I told you in the chat. If they clash with the repo's `AGENTS.md`, these win.

(Optional, delete it if you don't use the skill) At the start, load the `comment-style` skill and read its detail (`<HARNESS>\personal\skills\comment-style\details.md`) once.

Work order: understand (if it isn't clear or it's a bug) → build → check → review. **Scale the effort to the size:** a small tweak (a text, a colour, a margin, two lines of something already in context) goes straight in; a feature, or something that spans several files, gets the full protocol. What is never skipped, not even in tweaks: the sensor and showing what you checked.

- **BEFORE the first code change:** load the `code-conventions` skill. If it's UI, also `ui-design`; if it touches an API or library of the stack, also `official-sources`. Don't edit without loading them. **Once per session is enough:** don't reread them by routine; for tweaks, use what's already loaded.
- **Small tweaks:** straight in, without reopening half the repo or reloading anything. New logic, endpoints, anything spanning several modules or something you don't understand yet are not tweaks: those get the full loads.
- **AFTER every code change:** run `py -3 <HARNESS>\personal\scripts\check.py`. If it gives an ERROR, fix it before going on. (It takes seconds: tweaks too.)
- **To see a rendered page:** use the tool's built-in browser, not `webfetch` (it doesn't run JS and has no session). In OpenCode it's inside `execute` (`search({ query: "browser" })`). **If you're told about a page or asked whether you see the browser, don't ask for the URL: list the open tabs first (`browser.tabs.list`)**; the user usually has it open already, with a session.
- **BEFORE saying "done":** show the output of that command and say what you checked and what you didn't.
- **To review:** the only agent is `reviewer` (clean context, doesn't edit, conventions included). **Don't launch it after every change:** reviews pile up and run **once, when the session closes** (or before a commit/PR), over the whole diff. If the change is big or delicate, launch it when you finish it.
- **The commit and the push belong to the user:** you leave the change checked and, if needed, a proposed message, **written in full** (if the format leaves a gap, only the ticket number). **Don't run `git add`, `git commit`, `git push` (nor `--amend` or `--force`) or touch branches or the remote** unless I ask you to at that moment. <!-- FILL-IN (optional): the team's commit message format -->
- **Never save passwords, tokens or credentials to files** (not in skills, not in the repo, not in home): use them only in the session. If you're asked to save them, say no and why.

Each skill says when to use it; this only sets the order. With small models, this "BEFORE / AFTER" format works much better than a general description, and it has to say who's in charge and that there are no exceptions: otherwise a local model treats the router as a suggestion (or as a possible injection) and skips it on "small" changes.
