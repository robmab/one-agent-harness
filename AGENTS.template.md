<!--
TEMPLATE for AGENTS.md: copy it to the ROOT OF THE PROJECT REPO named AGENTS.md (if the repo is yours or the team agrees).
Claude Code and Copilot load it on their own at the start of every session: keep it short, an index and not a manual.
Rule for maintaining it: every line must be explained by a real failure or by something the agent can't guess.
Delete this comment when you copy it.
-->

# <PROJECT> — guide for agents

<!-- FILL-IN: one line on what it is and the main stack. -->

This is only the index. The detail lives in the skills and in `docs/`.

## Skills

| Skill | When |
|---|---|
| `code-conventions` | before writing or reviewing ANY code |
| `ui-design` | only layout, styles or UI components |
| <!-- FILL-IN: other skills in the repo, if any --> | |

## Agents

| Agent | When |
|---|---|
| `reviewer` | the only one: in-depth review (conventions, correctness, security, performance…); doesn't edit; with no files, it reviews the `git diff` |

## Commands

<!-- FILL-IN: only the ones an agent can't guess. Mark the dangerous ones. -->

```bash
# environment: how to activate it or which executable to use (is the one on PATH fine?)
# start the development server
# tests
# lint / format
# database migrations  → careful, touches the database: confirm first
```

- **Development database:** <!-- FILL-IN: where it is and whether it's a copy of production -->
- **Assets:** <!-- FILL-IN: is there a build or are they served as is? -->

## What isn't done without asking

<!-- FILL-IN: actions that always need permission (touching the database, installing dependencies, pushing…). -->
