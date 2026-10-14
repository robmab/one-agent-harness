<PROJECT> harness (only in its repo): **6 skills + 1 sensor + 1 agent**, on top of `AGENTS.md`. (Optional, delete it if you don't use the skill) At the start, load `project:comment-style` and read its detail (`<HARNESS>\personal\skills\comment-style\details.md`) once.

Work order: understand (if it isn't clear or it's a bug) → build → check → review. At each moment:

- **BEFORE writing code:** load `project:code-conventions`. If it's UI, also `project:ui-design`; if it touches an API or library of the stack, also `project:official-sources`. If a skill is only a pointer ("Read `<path>`…"), open the file it points to.
- **AFTER every code change:** the sensor (`check`) runs on its own through the hook. If it gives an ERROR, fix it before going on.
- **BEFORE saying "done":** check with `project:verify-before-done` and say what you checked and what you didn't.
- **To review:** the only agent is `project:reviewer` (clean context, doesn't edit), once when the session closes (or before a commit/PR), over the whole diff.
- **The commit and the push belong to the user:** leave the change checked and propose the message in full. Don't run `git add`, `git commit`, `git push` (nor `--amend` or `--force`) or touch branches unless asked at that moment.
- **Never save passwords, tokens or credentials to files** (skills, repo or home): use them only in the session.

Each skill says when to use it; this only sets the order.
