---
name: Bug report
about: A skill, agent or hook doesn't load, doesn't trigger, or behaves differently than documented
title: ""
labels: bug
assignees: ""
---

## What happened

<!-- A clear description of the problem. -->

## Steps to reproduce

1. 
2. 
3. 

## What you expected

## Environment

- Template version: <!-- content of VERSION in your harness, e.g. 0.1.0 -->
- Tool: <!-- Claude Code (version) / VS Code + GitHub Copilot (model, e.g. a local BYOK model) -->
- Windows version: <!-- e.g. Windows 11 24H2 -->
- Several projects wired at the same time? <!-- yes / no -->

## Diagnostics

<details>
<summary>Skills and agents the tool lists</summary>

<!-- Claude: ask "which skills and agents do you have?" in a new session. VS Code: type / in the chat. -->

```
paste here
```
</details>

<details>
<summary><code>py -3 personal/scripts/check.py --selftest</code></summary>

```
paste here
```
</details>

<details>
<summary>Junctions</summary>

<!-- In PowerShell: Get-Item "$HOME\.copilot\skills", "<HARNESS>\claude\plugins\<project>" | Select-Object FullName, LinkType, Target -->

```
paste here
```
</details>

<details>
<summary>The relevant part of <code>~/.claude/settings.json</code></summary>

<!-- The harness marketplace, enabledPlugins and hooks. Remove anything private, such as personal paths. -->

```json
paste here
```
</details>

## Anything else

<!-- What you already tried, whether it happens in a fresh session (not a fork), whether another model behaves differently. -->
