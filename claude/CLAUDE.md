<PROJECT> harness (only in its repo): **6 skills + 1 sensor + 1 agent**, on top of `AGENTS.md`. (Optional, delete it if you don't use the skill) At the start, load only `project:comment-style`: its page already sets the chat's tone. Read its detail (`<HARNESS>\personal\skills\comment-style\details.md`) once, when you write the first code comment.

Work order: understand (if it isn't clear or it's a bug) → build → check → review. **If it's big** (3 or more files, a new screen or component, or it crosses layers): before the first edit, a short plan with `interview-me`, and wait for the user's yes. At each moment:

- **BEFORE writing code:** load `project:code-conventions`. If it's UI, also `project:ui-design`; if it touches an API or library of the stack, also `project:official-sources`. If a skill is only a pointer ("Read `<path>`…"), open the file it points to. If a tweak grows (a second file type, a new component), load what's missing before the next edit.
- **AFTER every code change:** the sensor (`check`) runs on its own through the hook and leaves a line (`OK`, warnings or ERROR). If it gives an ERROR, fix it before going on.
- **BEFORE saying "done":** check with `project:verify-before-done` and say what you checked and what you didn't.
- **To review:** the only agent is `project:reviewer` (clean context, doesn't edit), once when the session closes (or before a commit/PR), over the whole diff. When you launch it, give it only the scope (the session's files or commits) and what was meant to be done, in 2-4 lines: not what you already checked or where to look.
- **In the browser:** the tab is the user's: don't resize it, and intercept requests in another tab, removing it when done. Visual changes are checked with a zoomed screenshot. How to test locally: the "Testing locally" section of `project:verify-before-done`.
- **The commit and the push belong to the user:** leave the change checked and propose the message in full. Don't run `git add`, `git commit`, `git push` (nor `--amend` or `--force`) or touch branches unless asked at that moment.
- **Never save passwords, tokens or credentials to files** (skills, repo or home): use them only in the session. If a test needs a user or a password, ask the user to step in.

Each skill says when to use it; this only sets the order.
