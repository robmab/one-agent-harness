---
name: official-sources
description: "Write <PROJECT> code for the REAL versions of its stack, checking it in the repo or in the official docs for that version, not from memory. Use when: creating or touching components, styles, queries or any API of the project's libraries that you don't already see used in the repo; also when reviewing code that uses them."
---

# Official sources: the version rules

> **CONCEPT:** models write for the latest version of every library; if the project lags behind, what they know from memory is probably from another version. Check it in the repo or in that version's docs, and say when it couldn't be checked.

> **TEMPLATE · FILL-IN** each section. Full example: [examples/skills/official-sources](../../../examples/skills/official-sources/SKILL.md). Once filled in, delete this block.

If you're not in the <PROJECT> repo, ignore this skill.

## The real stack

| Library | Version | Where it shows | Docs for that version |
|---|---|---|---|
| <!-- FILL-IN: e.g. Vue --> | | <!-- package.json, the .min.js header… --> | |

## Typical traps
<!-- FILL-IN: what a model writes from memory that doesn't exist in this version, with what IS used here. -->

## How to do it
<!-- FILL-IN: the order. E.g.: the repo first; then the traps above; then the official docs for that version; cite in the chat, not in the code; if unchecked, say "UNVERIFIED". -->

## Red flags
<!-- FILL-IN: 2-3. E.g.: an API "because that's how it's done"; a class that appears nowhere else in the repo. -->
