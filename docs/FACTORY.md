# Factory: unattended ticket intake (optional)

🌐 **English** · [Español](FACTORY.es.md)

By default you drive every session: you open it, talk to the agent and approve at the end (**manual**). With `factory\intake.py`, new tickets open their own session, without a window and in their own branch, and wait for you in a tray. That's the step from harness to *software factory*: the harness is the same, what changes is who starts the work.

## 1. When it pays off

- **Clear, small tickets:** a text, a translation, a style fix, a bug with steps to reproduce it. A label decides which ones go in: you put it on, so nothing enters by surprise.
- **A project you can check without someone looking:** tests, or at least the sensor and the reviewer. If checking is mostly visual, stop before the code (§2) and keep the building for your session.
- **Not worth it** for vague tickets (`prepare` needs to ask you) or for changes to the database, shared code or permissions: those go by hand.

## 2. Where it stops

| `--stop` | What the session does | What you get |
|---|---|---|
| `before-code` (default) | reads the ticket, finds the cause or the files involved (`diagnose`) and writes the questions `prepare` would ask | a report to start your session halfway through; no diff to review |
| `after-review` | builds it and closes as `closing.md` says: reviewer, fixes, findings table and commit message | branch `ai/<id>` ready for you to review, test and commit |

If the tool can rename, a `before-code` session leaves ⚪ in its title (analysed and waiting to start), and one that gets stuck leaves 🔴 (the states, in `closing.md` §6). Either way it never commits or pushes, and it doesn't ask: questions go in the report. The retro question waits too: the report ends with "Retro: pending", and the agent asks it when you approve that branch.

## 3. Setting it up

1. **Where the tickets come from:** fill in `fetch_tickets()` in `factory\intake.py`. The example reads GitHub issues with `gh`; for another tracker (Jira, Mantis…), its API or its export, returning `id`, `title` and `body`. And `LABEL`, the label that lets a ticket in.
2. **The tool:** `--tool copilot` (default), `claude` or `opencode`. Without a window it can't ask for permission: `TOOLS` gives it up front, minus `git push`, `commit`, `branch` and `checkout`. Review that list for your project. The guard (hooks) still blocks credentials, and lets the reviewer run without a "closing" message thanks to `HARNESS_UNATTENDED=1`, which only the script sets.
3. **Try it by hand** from the repo: `py -3 <HARNESS>\factory\intake.py --dry-run` (lists what it would take), then without `--dry-run` on one ticket (`--max 1`).
4. **Schedule it,** every 15 minutes for example:
   - Windows: `schtasks /Create /SC MINUTE /MO 15 /TN harness-intake /TR "py -3 <HARNESS>\factory\intake.py --repo <repo>"`
   - Linux / macOS (cron): `*/15 * * * * cd <repo> && python3 <HARNESS>/factory/intake.py`

## 4. The tray, day to day

- **What's waiting:** `factory\reports\<id>.md` (the report), `<id>.log` (what the tool printed) and `factory\state.json` (each ticket's branch, folder and exit code). A ticket that's already there isn't taken again.
- **Picking one up:** open the worktree (`<repo>-ai-<id>`, next to the repo) in your editor, read the report and carry on in a normal session, or review the diff and commit it if it's done.
- **Cleaning up:** `git worktree remove <folder>` and `git branch -d ai/<id>` when you've merged it or thrown it away.

## 5. Risks

- **Permissions:** an unattended session does what its permissions allow. Keep `TOOLS` tight and the guard hooked in the tool you use.
- **Shared things:** every worktree uses the same development database and the same ports as you. The router's rule still applies (no writing to the database without permission), but there's no one to give it: the session must stop.
- **Cost:** each ticket is a full session. `--max` caps how many per run (default 3).
