# Interview: how to do it

Detail of the "Interview" part of `prepare`. Read it every time you are about to interview.

What's asked for and what's needed rarely match: "a list" may turn out to be "knowing which customers haven't paid". The cheap moment to find out is **before** writing code.

## 0. Look before you guess

If the ticket names a screen, a piece of data or a feature, find it in the repo and see **what it does now**. That way your guesses have a basis: "right now the report adds both columns; I guess they want them separate". Read only: don't touch code or the database.

## 1. Hypothesis with a number

Before asking, write in one line what you think is wanted and how confident you are:

```
HYPOTHESIS: you want the manager to see open incidents without opening them one by one.
CONFIDENCE: ~40% (missing: which role exactly and whether it's for every user)
```

Below ~70%, say what's missing.

## 2. One question at a time, with your guess

```
Q: Is this for every user or only for whoever opened the ticket?
I GUESS: for everyone, but only visible with the manager permission.
```

**Wait for the answer before the next one.** No lists of questions: the third one usually depends on the first. Sometimes guessing against the obvious helps, so you don't get a polite yes.

## What's usually missing

Ask only what isn't clear:

- **Who:** which role uses it and from where (desktop or mobile).
- **Scope:** for everyone, for one customer, or configurable.
- **Data:** is a new field or table needed? That means a migration.
- **Success:** how we'll know it's right: what the user sees or what stops happening.
- **Limits:** deadline, performance, not breaking something that exists.
- **Out of scope:** what is NOT done now.
- **Screen states:** what is shown empty, while loading and on error, and on a phone.
<!-- TUNE: what this project's tickets usually leave out. -->

**If you don't know the answer** (it depends on the customer or on whoever opened the ticket), don't make it up: it goes on a list of **questions for the customer** and we carry on with the rest.

## 3. Watch out for "textbook" answers

"It should be scalable", "the standard way", "like everyone does it"… sound good but say nothing. Ask: *"if you didn't have to justify it to anyone, what would you really want?"*.

## 4. Give it back as a summary

When you can **predict my answers to your next 3 questions**, stop and summarise:

```
This is what I understand:
- What:              ...
- For whom:          ...
- Why now:           ...
- Done when:         ...
- Limit:             ...
- Out:               ...
- Questions for the customer: ... (if any)
Yes, no, or adjust?
```

The **"Out"** line is never skipped: half the misunderstandings are about what isn't done.

## 5. Explicit yes, then stop

- **A "whatever you think" or an "ok, go on" is not a yes:** ask again with two concrete options.
- **With a clear yes, deliver the summary, offer the next step** (a plan if it's big, code, or asking the customer) **and stop.** No code or tools in that same turn.
- **If after several questions your confidence doesn't go up,** say so: "something basic is missing; shall we stop and look at it from another angle?".

## Red flags

- Two or more questions in the same message.
- A question without your guess.
- Accepting a textbook answer without digging.
- Starting to plan or code before the yes.
- Making up what only the customer knows.
- Saving the summary to a file in the repo: it stays in the chat unless asked.
