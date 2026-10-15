---
name: ui-design
description: "<PROJECT> design system: components, colours, typography, spacing, screen states and layout. Use when: ONLY layout, styles or UI components. NOT for logic or backend."
---

# UI design — <PROJECT>

**CONCEPT:** the project's design system (tokens, components, patterns), loaded only when the UI is touched. Without it the agent invents components and colours that already exist.

> **PROFILE · web.** General web rules, valid for most stacks. Adjust the lines marked `TUNE` to yours and then remove the mark.

If you're not in the <PROJECT> repo, ignore this skill.

## Principles
- **Reuse before creating:** look for the component or the pattern in the project before writing a new one.
- **Variables, not values:** colours, typography, spacing, radii and shadows come from the design tokens.
- **Mobile first:** it has to work on a narrow screen; the wide one adds, it doesn't fix.
- **Every state designed:** empty, loading, error and no permission, not only the happy path.
- **Accessible:** AA contrast, visible focus, touch targets of at least 40px, nothing that only works on hover.

## Tokens
<!-- TUNE: where the variables live and their names (colours, typography, spacing scale, radii, shadows). -->

## Canonical components

| Component | Where it lives | When to use it |
|---|---|---|
| <!-- TUNE: buttons, cards, modals, tables, forms, badges, empty state… --> | | |

## Screen patterns
- List with filters, record with tabs, form, dashboard: each one with a reference screen in the project.
<!-- TUNE: the reference screen for each pattern. -->

## Responsive
- Check it at phone width (~375px) and on desktop: no horizontal scroll, and wide tables scroll inside their container.
<!-- TUNE: the project's breakpoints and what changes on mobile. -->

## What isn't done
- Inline styles, loose colours, `!important` to win a fight, or pure greys when the palette has its own.
- A second version of a component (`button-v2`) instead of a variant of the first one.
- Libraries of a different major version from the project's.
