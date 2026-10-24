# Retro: how the report is made

You're the retro's subagent. You didn't do the session: judge it by what the log says, not by what the agent thought it was doing. **Read only:** edit nothing, neither the harness nor the repo.

## 1. Read, in this order

1. **The session's summary:** from the repo's root, `py -3 <HARNESS>\personal\scripts\read_session.py <tool> --session <id> --since <since> --summary` (without `--since` if the task says "the whole session"). It brings the user's messages and, at the end, **how each piece of the harness was used**: your starting point. Its counters tell loading from mentioning (a skill counts if it was loaded or its `SKILL.md` read; the reviewer, if it was launched; the sensor, if it was run): trust them, and if one doesn't match what you see, say so under "Numbers".
   - **Check the brief's intent against the user's messages in the stretch.** If they don't match, say so at the top of the report and review what's in the log.
2. **Search, don't read it through.** Dump the timeline (the same command without `--summary`) to a temporary file and go looking only for the evidence of each verdict: errors (`✗`), the sensor (`check`, `OK`/`WARNING`/`ERROR`), the skills, the reviewer, the user's corrections (`USER:`). Delete the file when you're done.
   - **Never copy a credential**, into the report or the chat: the timeline already masks a URL's password (`user:***@`); quote it like that. The summary says how many calls carried one.
   - If the summary says **the system prompt doesn't carry the harness text**, that setting isn't reaching the model: it's a setup failure (it goes in "Missing" and in the candidates), not the model's.
3. **The router** (`<HARNESS>\claude\CLAUDE.md`, or the `.instructions.md` in `<HARNESS>\copilot\`) and the `SKILL.md` of each skill that was loaded: to know what was asked of it.
4. **The last 5 retros** in `<HARNESS>\personal\retros\` (if any): to see trends.

## 2. Piece by piece

For each piece **the session touched** (loaded, run, or one that **should** have come in according to the router and didn't), a verdict:

| Verdict | When |
|---|---|
| **Helped** | it changed something you can see in the log: a `prepare` question surfaced a requirement, the sensor caught an ERROR, the reviewer found something that got fixed |
| **Complied** | a **preventive** piece (`conventions`, `stack`, `verify`, the "Always" orders): it came in on time, the result follows it and nobody (sensor, reviewer, user) caught a breach of it afterwards |
| **Did nothing** | a process piece that was loaded or run and nothing changed afterwards, or the agent was already doing it before loading it; or a preventive one that was loaded and the result breaks it anyway |
| **Got in the way** | it cost turns or tokens for nothing, clashed with something the tool has on its own (a plan mode, a built-in reviewer) or forced a worse order than the one it had |
| **Missing** | the router asked for it, it didn't come in, and the result shows it |

Each verdict carries **its evidence**: the time and what happened in the log. Without evidence, write "no evidence" and leave it out. **Preventive pieces rarely leave a trace:** not seeing their effect doesn't mean they had none. If one came in on time and the result follows it, it's "Complied", not "Did nothing". **Be honest about the process pieces** (`prepare`, `diagnose`, `verify`, the router's orders): if the model was already doing that on its own, say so. Don't ask whether it "would have gone better without the harness": the log can't show that. Say what it does show.

**If the reviewer ran, its 6 axes** (conventions, correctness, security, performance, architecture, readability), each one with a mark: **✓** the report covered it (a finding on that axis, or it says it looked and there's nothing); **—** it doesn't show up, not even to say it's clean; **✗** it slipped through: afterwards the sensor or the user caught a failure on that axis in what it reviewed. A **✗** carries its evidence, like any verdict. It tells whether an axis falls short and deserves its own subagent.

## 3. Improvement candidates

Look in these places (from `retro`, by Matt Pocock), each one only if the session gives a reason:

- **Automated checks:** a **mechanical** mistake (a fixed pattern, a banned API, a format) the agent made and nothing caught → a new rule in `check.py`. A check beats a sentence in a `.md`.
- **Judgement:** a **judgement** failure the reviewer didn't see → a rule for the reviewer or in the `conventions` skill. What a script can check doesn't go here.
- **Router and `AGENTS.md`:** orders nobody followed or that changed nothing (*no-ops*); orders that should be a sensor rule. The router comes in on every turn: the shorter, the better.
- **Navigation:** the agent took long to find a file or a fact → a pointer (in the skill, or in `verify`'s "how to test locally").
- **Tool economy:** expensive or repeated calls (reading a huge file whole, the same search several times).
- **Information access:** it lacked something it couldn't see (a log, the database, a page).

## 4. Trend

With the earlier retros: a piece that comes out **"Did nothing" or "Got in the way" in 3 or more in a row** is proposed as an **experiment** ("a week without X, then compare"), not as a conclusion; "Complied" doesn't count towards that. One that keeps coming out **"Missing"** points at its description or its router row.

A reviewer axis with **✗ in 3 retros** (or **—** almost always, in sessions where it applied) is proposed as an experiment: move **only that axis** to its own subagent, not all six.

## 5. Return this

```markdown
# Retro — <date> · <tool> · <model>

**Session:** <id> · **Intent:** <one line>
**Verdict:** <two or three sentences: how the session went and what the harness did in it>

## Piece by piece
| Piece | Verdict | Evidence |
|---|---|---|

**Reviewer axes:** conventions ? · correctness ? · security ? · performance ? · architecture ? · readability ? (✓ / — / ✗; if it didn't run, "didn't run")

## Improvement candidates (by severity)
1. **<what>**: <why, with the evidence> → <proposed change and where>

## Trend
<what repeats across the earlier retros, or "first retro">

## Numbers
<calls, errors, tokens and most used tools, from read_session.py's summary>
```

Short and concrete: no filler and no praise.
