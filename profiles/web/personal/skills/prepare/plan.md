# Plan: how to do it

Detail of the "Plan" branch of `prepare`. Read it when the zone is expensive or irreversible. **Before the first edit**, and with the tool's plan mode if it has one.

## 1. Look for what already exists

The project's shared components and a similar screen. Reuse before creating.

## 2. Write the plan, 10 to 20 lines and no code

```
GOAL: <one line; if you come from the interview, its "What">
STEPS (in layer order, drop the ones that don't apply):
1. migration             → files · how it's checked
2. model                 → …
3. endpoint (permission) → …
4. template              → …
5. front-end code        → …
6. styles                → …
REUSES: <shared components or code that already exists>
NOT TOUCHED: <what stays out>
EVIDENCE: <what shows it's done; if it can't be checked, it isn't defined>
RISKS: <which other screen it may break>
WAY BACK: <only if irreversible: how it's undone and what the user runs>
```

Each step has to be checkable (the sensor, the screen, a query), with no "we'll see".

## 3. Check it against the project

Does it reuse shared components?; cache-busting of every CSS or JS touched; visible text translatable; the endpoint's permission, the same as its screen's; a migration if there is new data; empty, loading and error states; mobile. <!-- TUNE: what else usually gets forgotten in your project. -->

## 4. Check it against the request

Point by point: nothing more, nothing less.

## 5. Show it and wait for a clear yes

As in the interview. No code or edits in that turn.

## While building and when done

- **One step at a time:** check it the way the plan says before starting the next. If it fails, fix it there, not at the end.
- If a step changes, say so before going on.
- **When done, check what was built against the STEPS:** each thing where the plan put it; if something ended up elsewhere, say so before closing.
- When closing, the GOAL and the plan's files are the scope and intent you hand to the `reviewer`.

## Red flags

- Code in the plan, or steps like "adjust whatever is needed" or with no way to check them.
- A new component without looking at what's shared.
- Editing before the yes.
- Planning what doesn't hurt: "almost nothing" goes straight in.
