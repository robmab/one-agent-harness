# Closing the session

Read it when closing the session, or before a commit or a PR. In this order.

## 1. The reviewer

Once, over the session's whole diff (if the change is big or delicate, when you finish it, without waiting for the close). Give it **only** this:

```
Scope: <the session's files or commits>
Intent: <what was meant to be done, in one line>
```

Nothing about what you checked or where it should look: let it find out.

## 2. What it found, all of it

- Fix what's yours and check it again.
- **Tell the user every finding**, including the ones you don't fix (already decided, pre-existing): they mustn't stay buried in the reviewer's report.

## 3. Clean-up

Delete **every** temporary script you created, and any test data you weren't asked to keep (or say which stays and how to remove it).

## 4. The commit message

Only now, with the reviewer done. The commit and the push are the user's: don't run `git add`, `git commit` or `git push`.

- **Format:** <!-- FILL-IN: the team's format, e.g. `[fix] #<ticket>: <title as is>. <short, non-technical description>` -->
- What you don't know (the ticket, say) stays as a `<…>` gap, never invented.
- Propose the message in full, with the description already written, even if you're asked for "just the structure".
