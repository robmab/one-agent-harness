# Closing the session

Read it when closing the session, or before a commit or a PR. In this order.

## 1. The reviewer

**Only when the user says they're closing the session** (or asks before a commit or a PR). Not when you finish a change: it goes in the close, not at the end of each task. Once, over the session's whole diff. Give it **only** this:

```
Scope: <the session's files or commits>
Intent: <what was meant to be done, in one line>
```

Nothing more: not what you checked, not where to look, not a list of things to review. Let it find out.

**If the diff is big** (`git diff HEAD --stat` over ~30 files, e.g. one change repeated across many templates), the scope names the logic files and, for the rest, a sample of 3 or 4 and the pattern of the change. Check on it after 3 minutes: if after 5 it hasn't taken a single turn, stop it and relaunch it narrowed.

<!-- CHOOSE: how the review runs. By default, one reviewer goes through the 6 axes (above). The alternative, one subagent per axis, focuses each one and lets each axis use its own model, but costs about 6 times the tokens and adds noise: try it only if the retros show an axis that keeps falling short. A subagent can't launch others in Claude Code (check it in your tool), so you launch them all from here. To use it, swap the sentence "Once, over the session's whole diff." in the paragraph above for this one:
**Once, over the session's whole diff, one reviewer per axis, all at once:** six launches with the same task plus `Axis: <1-6>`. For a different model per axis, make a copy of the agent per model (`reviewer-<model>`, see the note at the top of the reviewer). When all six are back, **you join them** before §2: one report, duplicates merged (the same `file:line` from two axes is one finding, with both axes and the higher severity), and the verdict and the second pass of the strictest. -->

**Don't wait for it in a loop** (`Start-Sleep`, `sleep`, listing agents over and over): if your tool tells you when the subagent finishes, end the turn or get on with something else and pick it up from the notice. If it hangs, say so and launch it again with the same task, without replacing it with a review of your own.

## 2. What it found, all of it

- Fix what's yours and check it again.
- **Approver, manual (one pass):** if a fix changes logic (not just a text, a comment or a name; a new guard, a condition or a calculation **are** logic), don't rerun the reviewer on your own: say it in the table (what went unreviewed, and whether it touches a shared file) and ask the user whether they want another pass over it. If the reviewer recommended a second pass, say so in the same question; if it said it isn't needed, don't offer it. If it runs, it covers what the fixes changed, not the whole diff.
  <!-- CHOOSE: the approver's mode. Manual (above) suits a human who reviews the diff anyway: one pass is enough. For an unattended flow, swap the bullet above for this one:
  - **Approver, automatic (in rounds):** after your fixes, launch the reviewer again with the same task, scoped to what the fixes changed. Repeat until no 🔴 or 🟠 are left, **at most 3 rounds**; then stop and tell the user what's still open. Findings outside the task never enter the loop: they go to the table. Each round goes in the table. -->
- **If a finding clashes with something the user decided in the session** (a name, a location, an approach), don't apply it: it goes to the table, next to what they decided, and they choose.
- **If a finding goes to another ticket**, give it already written in the table: title and two lines of description.
- **Tell the user every finding, in a table:** finding · severity (blocking, important, minor) · status (fixed; not, and why; already decided). One per row, the ones you don't fix too, and the reviewer's **questions** (💭) as well, with what you saw or "not looked at". Before closing, check the table against the reviewer's report: none must be left out.
- **Below the table, always, an "Out of scope (not touched)" row**: what was left for another ticket or another time, or you said was still to do, during the whole session, not just the reviewer's (go back over your messages), each with its title and two lines; or "none".

## 3. Clean-up

Delete **every** temporary script you created, whatever you cloned or copied into a temp folder (a repo, a backup), and any test data you weren't asked to keep (or say which stays and how to remove it). **What the user asked you to create stays** while they keep testing: to delete it, ask first. Then run `git status --short` (and that of every nested repo you touched) and show it: the list of what you touched comes from there, not from memory. Say which new files are left without `git add`. If a file is one the user decided not to change, undo it or ask. If you touched the router, tell the user to restart the tool (it loads it at start) and that next session `read_session.py --summary` shouldn't report missing rows. If something is in the index (`git add`) that you didn't put there, say so as is, without guessing who did it: the reviewer doesn't write.

**Below it, one line if something touches a sensitive area:** the database (models, SQL, migrations), shared code, permissions or authentication, configuration. For example: "Look carefully at: `app/models/order.py` (database)". It only tells the user where to look: it changes nothing else in the closing. If nothing like that is touched, leave the line out.

**And another if something is left to do when deploying** (translations, a migration, an environment variable). Say it even if you already did earlier.

<!-- TUNE: this project's sensitive areas (core folders, shared CSS or base templates, billing…). -->

## 4. The commit message

Only now, with the reviewer done and its fixes made, **and as soon as they are**: don't wait for the user to say again that they're closing. If the diff changes afterwards, or a repo you hadn't seen turns up, propose it again. The commit and the push are the user's: don't run `git add`, `git commit` or `git push`.

- **Format:** <!-- FILL-IN: the team's format, e.g. `[fix] #<ticket>: <title as is>. <short, non-technical description>` -->
- What you don't know (the ticket, say) stays as a `<…>` gap, never invented.
- Propose the message in full, with the description already written, even if you're asked for "just the structure".

## 5. The retro, if they want it

**It's the last step but one of the close: without this question, the close isn't done.** After the closing message, ask it **with your question tool**, not as text: `vscode_askQuestions` in Copilot chat, `ask_user` in Copilot CLI, `ask_user_question` in DeepSeek Harness, `question` in OpenCode (if you have none, in a message of its own that holds only the question). The question: **"Do you want a retro of the harness for this session?"**. If yes, load the `retro` skill. If no, or no answer, nothing more. **In a factory session** (unattended, from `factory/intake.py`) there's no one to ask: end the report with "Retro: pending". When the user later approves that branch, ask it then, about the session the report names.

## 6. The state, in the title

A circle before the tab's title shows at a glance how each session stands, and what's the user's turn. Leave the title as it is and only add, change or remove the prefix; one at a time. No circle means the agent is working: when you pick up a ⚪ or a 🔴, remove it.

| State | When |
|---|---|
| ⚪ | analysed and waiting to start: you've given the plan and wait for the user's yes, or a factory session stopped at `before-code` |
| 🔴 | stuck: you can't go on without the user (3 failed fixes, an unresolved blocker, something only they can give you). Say in the message what you need. An ordinary question isn't 🔴: just ask |
| 🟠 | pending: the user says they're leaving it, at any moment, not just when closing. When it's picked up and closed, it goes to 🟢 |
| 🟢 | closed and fine: reviewer settled, fixes made and, if they asked for it, retro finished |

If your tool can't rename, say so once.
