---
name: diagnose
description: "Debug by finding the root cause before touching anything: reproduce, follow the data through the application layers and one hypothesis at a time. Use when: a bug, an error or stack trace, something that doesn't work, comes out empty or behaves oddly, an install or environment error (pip, venv, DLL, wrong interpreter), a tool that's missing or won't connect, or a previous fix didn't work; before proposing any fix."
---

# Systematic debugging

**Iron rule: no root cause, no fix.** Patching the symptom is a failure, even if the symptom goes away.

> **TEMPLATE · FILL-IN** the layer table and the project's traps. The method works as is. Once filled in, delete this block.

## 1. Investigate (before proposing anything)

- **Read the whole error:** the server trace, the browser console and the Network tab. The line and file usually give the answer.
- **If the ticket names a field or table that doesn't exist under that name**, ask the user before picking the one that looks equivalent: if they meant another, the fix changes nothing.
- **Reproduce it:** exact steps, with which user and which data. If it doesn't reproduce, gather more data; don't guess.
- **Look at what changed:** `git log`, `git diff`, `git log -S "text"` to see when something came in.
- **Follow the data through the layers** until you see where it goes wrong:

| Layer | How to look at it |
|---|---|
| Database | a **read-only** query |
| <!-- FILL-IN: model / service --> | what it returns: a temporary print or log |
| <!-- FILL-IN: controller / API --> | what comes out; if it's JSON, the response in Network |
| <!-- FILL-IN: template --> | the rendered HTML, not the template |
| <!-- FILL-IN: frontend --> | `console.log` and the console |

## 2. Compare with something that works

Find something similar in the repo that does work. Write down **every** difference, even the silly-looking ones.

## 3. One hypothesis at a time

- Write it down: "I think it's X because Y".
- Test it with the **smallest** change, one variable only.
- If that's not it, a new hypothesis; don't pile fixes on top of each other.
- **Before saying "that's the bug", say which fact of the case it explains.** If it explains none, it's a separate fault: being in the code doesn't make it the cause.
- If you don't understand it, say so: "I don't understand X".

## 4. Fix

- **First, have the reproduction at hand.** A test is better if possible, but a list of steps, a script or a query that shows the failure and then shows it's gone will do.
- **One change, at the source.** No "while I'm at it, I'll fix this other thing".
- **Check with `verify`** and remove the temporary prints and logs.
- **After 3 failed fixes, stop.** The problem is probably in the design, not the line. Explain it and decide before a fourth attempt.

## Typical traps

- **No writes without permission** to the database or shared environments.
- **Cache:** the browser caches JS and CSS; reload with Ctrl+F5 before judging a change broken.
- **Data:** if the development database is a copy of production or of a customer, the failure may depend on that data. Try with other data.
- **Silences:** an auto-reloading server can stay down after an import error; check its console.
<!-- FILL-IN: the project's own traps (libraries that fail silently, files processed before being served, logs whose level must be raised…). -->

## Signs you're skipping this

- "Let me try changing X and see."
- "It's probably X", without having seen it.
- Several changes at once and "let's see now".
- A list of fixes without having investigated.
- "One more try" when you're already at two.

If you catch yourself in one, go back to step 1.

---
Adapted from `systematic-debugging` of [obra/superpowers](https://github.com/obra/superpowers) @ `bb92a77` (2026-10-10) (MIT).
