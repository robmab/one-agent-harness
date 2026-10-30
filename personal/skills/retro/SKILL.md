---
name: retro
description: "Retrospective of a session: how the harness worked, piece by piece and with evidence from the log, and what to change for next time. Use when: the user asks for it ('do a retro', 'how did the harness do?', 'harness report') or says yes when it's offered at closing. NOT during the work, nor on your own initiative."
---

# Retro

> **CONCEPT:** the harness looking at itself. A fresh subagent reads the session's log and says, for each piece that took part, whether it helped, did nothing or got in the way, with the evidence. Without it, rules pile up and nobody checks whether they still earn their place, above all when the model starts doing on its own what it once had to be told.

> **OPTIONAL · READY.** Outside the core: it improves the harness, not the code. Ready as is; the paths are set by `setup.py`. If you don't want it, delete the folder, its row in both routers and step 5 of `closing.md`.

The retro is done by **a fresh subagent** (never a fork), one that didn't do the session: whoever did it is its worst judge. You only hand over the task, save what comes back and tell the user: don't read the log yourself first, that's its job.

## 1. The task

Launch the subagent **in the foreground**, waiting for its answer (one launched in the background got lost in a real session), with **only** this (none of your opinion of how it went):

```
Read and follow <HARNESS>\personal\skills\retro\report.md.
Tool: <claude | copilot | copilot-cli | opencode | dsh>
Session: <id>
Since: <HH:MM when what's being reviewed started, or "the whole session">
Intent: <what the session was meant to do, in one line>
```

- **The id, never "the most recent":** take it from `py -3 <HARNESS>\personal\scripts\read_session.py <tool> --list` (the main session, not a subagent's). In some tools the retro's own subagent would become "the most recent".
- **Tool:** `copilot` is Copilot chat; Copilot's agent (and its CLI) is `copilot-cli`. If in doubt, the one whose `--list` shows the id.
- **Intent:** the one of what's being reviewed, taken from the user's messages in that stretch; not the session's first message, which in a long chat can be from another day.
- **Since:** a Copilot chat can last weeks. Pass the time when what's being reviewed started (today's work, or the task's), so it doesn't read days that don't apply. It's the start time, never the time of the retro itself; for all of it, "the whole session".

If your tool has no subagents, do the retro yourself following `report.md`, and tell the user you did it with the session's context on top.

## 2. What comes back

- **Save it as is, with your file-creating tool** (not PowerShell 5.1's `Set-Content`/`Out-File`, which breaks accented characters) in `<HARNESS>\personal\retros\YYYY-MM-DD-<tool>.md` (if it exists, add `-2`, `-3`…). **Build the name before creating it**, listing that day's files (`Get-ChildItem` or `ls`), and save it as soon as it arrives, before answering the user. The history is what shows a piece failing **several sessions in a row**, not just once.
- **To the user:** the verdict and the improvement candidates, by severity, and the report's path.
- **Nothing changes on its own:** the retro proposes and the user decides. Don't touch the harness, not even the obvious, without their yes.

---
Adapted from `retro` in [mattpocock/skills](https://github.com/mattpocock/skills) @ `a7d038f` (2026-09-24) (MIT): the subagent, the piece-by-piece evidence and the history are this harness's own.
