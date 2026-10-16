# Day to day

🌐 **English** · [Español](DAY-TO-DAY.es.md)

Adding pieces, what goes in each instruction file, how to write a skill that works, and the gotchas learnt the hard way.

## 1. Adding pieces

- **New skill:** `personal\skills\<name>\SKILL.md`. Every user and every tool see it right away; **for OpenCode, also add it to the allowlist** in `opencode\opencode.jsonc`.
- **New agent: in principle, no.** The harness has **a single agent**, `reviewer`. A "reviewer for X" becomes a skill with its checklist, added to the `reviewer`'s checklist table (see [SKILLS-GUIDE [gotchas](#4-gotchas-learnt-the-hard-way)](SKILLS-GUIDE.md#6-before-adding-something-new)). Another agent only pays off for fresh eyes, different permissions or isolating heavy work that nothing else covers. If it ever comes to that: `personal\agents\<name>.agent.md` with **Claude** frontmatter (`name`, `description`, `tools: Read, Grep…`); Copilot picks it up too (tested). For OpenCode, then run `py -3 <HARNESS>\opencode\sync.py`.
- **Review from the OpenCode CLI:** from the repo, `& <HARNESS>\opencode\scripts\review-pending.ps1` runs the `reviewer` on uncommitted changes (or `-Branch main` for the branch) and leaves a dated report in `opencode\reports\`. With no code changes it exits without waking the model. Run it by hand, from an alias, scheduled, or from a local `pre-push` hook. In script mode anything on `ask` is rejected: the report says so.
- **Before adding anything, apply the filter** in [SKILLS-GUIDE [gotchas](#4-gotchas-learnt-the-hard-way)](SKILLS-GUIDE.md#6-before-adding-something-new):
  - knowledge the model can't have,
  - or a failure you've seen and that keeps happening.

  If a regex can check it, a new rule in `RULES` beats a skill. **Before trusting it, run it over the whole repo (`--all`) and over the lines added in recent history**: a rule with false positives blocks the agent or ends up ignored.
- **New checklist for the reviewer** (something only useful when reviewing) → `personal\checklists\<name>.md` plus a row in the `reviewer` sources table, with its axes.

## 2. What goes in each instruction file

Each file has one job; anything repeated between them costs context in every session and they end up contradicting each other.

| File | Who reads it | What goes in | What does NOT |
|---|---|---|---|
| `AGENTS.md` (repo root) | Claude and Copilot, always | the repo index: what it is, commands nobody can guess, which skill or agent to use for what. Short: every line backed by a real failure | personal pieces, skill details, the work order |
| `claude\CLAUDE.md` (harness) | Claude, always (`SessionStart` hook) | the **router**: what holds always (sensor, showing what was checked, git, credentials) and a table of moments, each with what's mandatory and the skill or piece it uses. Short; the detail of each moment lives in its skill or in `personal\closing.md` | the *when* of each skill (already in its `description`); anything `AGENTS.md` says |
| `copilot\<project>.instructions.md` (harness) | Copilot and OpenCode, always: VS Code chat, Copilot CLI (hardlink in `~/.copilot`) and OpenCode (hardlink `~/.config/opencode/AGENTS.md`) | the same router, without prefixes, with the sensor run by hand, saying whose instructions they are and that tweaks count too (with small models, the difference between following it or not) | same as `CLAUDE.md` |
| each skill's `SKILL.md` | the model, when the `description` matches | the *what* and *how*; the `description`, the *when* | rules that always apply (those go to `AGENTS.md` or the conventions) |

Rules:
- **No `CLAUDE.md` in the repo or any folder above it** (not even `~/.claude/CLAUDE.md` if the repo lives under your home): Claude would stop loading `AGENTS.md`. That's why the router goes through a hook.
- **When the pieces change** (new skill, another agent), update both the Claude and the Copilot routers; `AGENTS.md` only if it's a repo piece.
- **If the logs show the model skipping a phase**, improve the skill's `description` first; if it's the router, rewrite that instruction as an imperative tied to the moment ("BEFORE writing code…", "AFTER every change…"). The router only grows with failures you've seen.

## 3. Writing a skill that works

- **`name`** equal to the folder name, lowercase letters, digits and hyphens, **no `_`**: otherwise it fails silently.
- **Concept first:** a `**CONCEPT:**` line saying what the skill is for and what it prevents. The model follows a rule better when it knows why.
- **The `description` is all the model sees** until it decides to load the skill. It must say **when** to use it, not summarise what it does, and include **concrete words** from real requests ("component", "slot", "query"…). If it's generic, it won't trigger.
- **Short:** 600 words max, tables over paragraphs. If it needs more, an index plus side files read on demand.
- **If it's project-specific**, first line: "If you're not in the <PROJECT> repo, ignore this skill". Claude skills apply across all projects.
- **It must not write into the repo** (plans, intents, scratch files) and must ask before touching the database.
- **If it's adapted,** credit at the bottom with the source commit ("Adapted from X of [repo] @ `sha` (date) (MIT)") and add its notice to `THIRD-PARTY-NOTICES.md`.
- **Check upstream** (every few months): for each adapted skill, diff its repo since the commit in its footer (`git diff <sha>..HEAD -- skills/<name>/`). Only what passes the SKILLS-GUIDE [gotchas](#4-gotchas-learnt-the-hard-way) filter gets in; if you apply something, update the commit in the footer.
- **Test it in both tools,** in a new session and without invoking it by hand: does it kick in on its own when it should? And check the result, not just that it loaded. With small local models, expect to invoke it by hand (`/name`).

## 4. Gotchas (learnt the hard way)

- **No `CLAUDE.md` in any folder above the repo,** including `~/.claude/CLAUDE.md` if the repo lives under your home: Claude stops loading `AGENTS.md`. That's why global instructions go through a hook.
- **Nothing in `~/.claude/skills`, `~/.claude/agents` or the workspace's `.claude/`** that already arrives some other way: VS Code reads it and shows duplicates. There's no setting to prevent it.
- **Don't junction the whole `~/.claude/skills`:** Claude keeps per-user files there.
- **Marketplace:** `"strict": false` or `"version"` on the entry of a plugin without `plugin.json` broke loading of the **whole** marketplace, with no visible error.
- **Hook on forks:** when forking or resuming a conversation, if the hook's text is already in the history it isn't injected again. In new sessions it always is.
- **Deleting junctions without wiping the target:** `(Get-Item path -Force).Delete()` or `rmdir path` (without `/s`). Never `Remove-Item -Recurse` on a junction. From Git Bash, `rmdir` refuses ("Not a directory": it sees the junction as a symlink): use `cmd //c rmdir "C:\path"`.
- **Hardlinks (router and OpenCode config):** the original and each user's links are the same file. But if a program saves it by *replacing* it (delete and create), the link breaks silently. Check: `fsutil hardlink list <file>` lists every path; if one is missing, `setup.py --check` restores it (if the text is still the same). **Agents' own editors do it too.**
- **OpenCode silently ignores a whole agent if its frontmatter has `tools: Read, Grep…`** (the Claude and Copilot format): that's why `opencode\agents\` is a generated copy.
- **OpenCode walks up looking for skills all the way to your home:** if the repo lives under your user folder, it picks up those in `~/.claude/skills` (e.g. the ones the Claude app syncs) and they bloat every turn's prompt. The allowlist stops it.
- **`opencode run` can't approve permissions:** anything on `ask` is rejected. Desktop and the TUI do ask you.
- **Copying the harness:** junctions may arrive as plain folders or broken. `setup.py --check` points them out.
- **Hooks inside the plugin:** `hooks\hooks.json` at the plugin root loads on its own, and `${CLAUDE_PLUGIN_ROOT}` resolves fine through the junction.
- **`py -3`, not `python`** (Windows; on Linux and macOS, `python3`): the launcher lives in `C:\Windows` and works for every user. Set `PROJECT_PYTHON` so `.py` files compile with the project's Python, not the system one.
- **Detected isn't loaded:** in VS Code, a skill existing doesn't mean the model uses it; it decides from the `description`, and local models miss more often. Force it by typing `/name`.
- **Team docs in a git-ignored folder** (e.g. `docs/` in `.gitignore`): Copilot's search doesn't see them, so a grep there comes back empty. Search with `includeIgnoredFiles: true` or read them by path; if your skills point there, say so in the router.
- **Windows paths inside `sed` or `python -c`** in Git Bash: `\a`, `\r`… are read as escapes and corrupt the text. Use a separate script.
- **Repos owned by another Windows user:** git reports *dubious ownership* → `git config --global --add safe.directory <path>`.
