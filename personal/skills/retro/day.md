# The day's summary

When the user asks for the day (or several days) instead of one session, you do it yourself, from the retros and the logs:

- **Sources:** that day's retros in `retros\` count as they are. The sessions without one, read them with `read_session.py <tool> --list --since YYYY-MM-DD` and then `--session <id> --since YYYY-MM-DD --summary` (the full log only where the summary leaves doubts). Leave out the session writing the summary.
- **Save it** in `<HARNESS>\personal\retros\YYYY-MM-DD-day.md`, with: the sources; the verdict in 3 or 4 lines (how the work went and where the harness failed); a table of sessions (session · time · what · the harness in one line, or "retro `<file>`"); what repeats that day, with evidence (time and session); what went well, so nobody touches it; the improvement candidates by severity (file and change); the trend against the previous retros; and the day's numbers (sessions, calls, reviewer launches, sensor ERRORs).
- **What the user asked for the harness from a work session** (a rule, a report column, a format) goes in as a candidate: otherwise it's lost.
- It isn't a piece-by-piece retro: one line per session, and the detail stays in each retro. Nothing changes on its own here either. For a month, the same from the day summaries.
