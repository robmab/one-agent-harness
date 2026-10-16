<PROJECT> harness (only in its repo): **6 skills + 1 sensor + 1 agent**, on top of `AGENTS.md`.

**Always, tweaks too:**
- **After every edit** the sensor (`check`) runs through the hook and leaves a line (`OK`, warnings or ERROR). If it gives an ERROR, fix it before going on.
- **Before saying "done"**, show what you checked and what you didn't.
- **Git belongs to the user:** no `git add`, `commit`, `push` (nor `--amend` or `--force`) and no touching branches, unless asked at that moment.
- **Never save passwords, tokens or credentials to files.** If a test needs one, ask the user to step in.

**By moment:**

| Moment | What is mandatory | With what |
|---|---|---|
| At the start | the chat's tone (optional: delete this row if you don't use the skill) | `project:voice` (its detail, `<HARNESS>\personal\skills\voice\details.md`, when you write the first comment) |
| It isn't clear what's wanted | interview before touching anything | `project:prepare` |
| It's big (3+ files, a new screen or component, several layers) | a short plan and the user's yes, before the first edit | `project:prepare` |
| It's a bug, or something fails | the cause, before proposing any fix | `project:diagnose` |
| About to edit | load only what applies (a tweak of a text, colour or margin, no loads); if a skill is a pointer, open the file it points to | code: `project:conventions` · UI: `project:ui` · an API of the stack you don't already see in the repo: `project:stack` |
| The task grows (a second file type, or a new component) | load what's missing, before the next edit | the row above |
| Before saying "done" | the evidence that proves it, run now; visual changes, with a zoomed screenshot | `project:verify` (also how to test locally and the browser) |
| When closing (or before a commit or PR) | the reviewer, all its findings to the user, clean-up and the commit message | `project:reviewer` and `<HARNESS>\personal\closing.md` |
