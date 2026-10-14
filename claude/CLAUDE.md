<PROJECT> harness (only in its repo): **6 skills + 1 sensor + 1 agent**, on top of `AGENTS.md`. (Optional, delete it if you don't use the skill) At the start, load `project:comment-style` and read its detail (`<HARNESS>\personal\skills\comment-style\details.md`) once.

Work order: understand (if it isn't clear or it's a bug) → build → check → review. At each moment:

- **BEFORE writing code:** load `project:code-conventions`. If it's UI, also `project:ui-design`; if it touches an API or library of the stack, also `project:official-sources`.
- **AFTER every code change:** the sensor (`check`) runs on its own through the hook. If it gives an ERROR, fix it before going on.
- **BEFORE saying "done":** check with `project:verify-before-done` and say what you checked and what you didn't.
- **To review:** the only agent is `project:reviewer` (clean context, doesn't edit).

Each skill says when to use it; this only sets the order.
