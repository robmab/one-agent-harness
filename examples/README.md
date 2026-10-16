# Examples: the complete method skills

🌐 **English** · [Español](README.es.md)

The template's skills (`personal\skills\`) come as **templates**: each one opens with its concept and leaves its sections as `FILL-IN`. Here are the **complete versions** of the four method skills, as they were in v0.4.0, so you can copy one or take ideas from it.

**No tool loads them:** `setup.py` only links `personal\skills\`. They are reference, not part of the harness.

| Example | What it covers | Comes from |
|---|---|---|
| `prepare` | clarify before building (one question at a time, with your guess) and, if it's big, a short plan the user approves; the interview detail in `interview.md` | addyosmani `interview-me` + the idea of superpowers `writing-plans` |
| `diagnose` | root cause before fixing: reproduce, follow the data through the layers, one hypothesis at a time | superpowers `systematic-debugging` |
| `verify` | no "done" without a check run and read; how to test locally and in the browser | superpowers `verification-before-completion` |
| `stack` | code for the stack's real versions: the repo first, then that version's docs | addyosmani `source-driven-development` |

`conventions`, `ui` and `voice` have no example: their content is the project's (or yours) from the first line.

## How to use one

1. **Copy it over the template** (with its side files): `examples\skills\<name>\` → `personal\skills\<name>\`.
2. **Fill in what's still marked `FILL-IN`** (the project's tables: layers, commands, versions) and replace `<PROJECT>` and `<HARNESS>`: `setup.py` doesn't touch this folder.
3. **Keep the `**CONCEPT:**` line** at the top, or write it if you start from your own: it's what tells the model why the rules are there.
4. **Trim what you don't use.** They're examples, not the rule: a shorter skill that fits your project works better than a complete one that doesn't.

With `setup.py --lang es` the Spanish versions are installed here, under their Spanish names (`preparar`, `diagnosticar`…).
