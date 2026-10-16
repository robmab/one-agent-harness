# Setting up a project

🌐 **English** · [Español](SETUP.es.md)

From copying the template to checking that every tool sees it, plus how to live with other projects and how to do it all by hand.

Requirements: Claude Code (it uses Git Bash for hooks on Windows), VS Code with Copilot, OpenCode 2 if you use it, and Python 3: the `py` launcher on Windows, `python3` on Linux and macOS. Nothing needs admin rights. The commands below are the Windows ones; on Linux and macOS, `python3 <HARNESS>/setup.py` with the same options.

> **Linux and macOS:** `setup.py` links with symlinks and writes `python3` and `/` paths where the template has `py -3` and `\`. CI runs it end to end on both systems (with fake profiles), but it hasn't been tried yet on a real machine with the tools: if something fails, [open an issue](https://github.com/robmab/one-agent-harness/issues).

## 1. Copy

```powershell
git clone <this-repo-url> '<HARNESS>'
Remove-Item '<HARNESS>\.git', '<HARNESS>\.github' -Recurse -Force
```

```bash
git clone <this-repo-url> <HARNESS> && rm -rf <HARNESS>/.git <HARNESS>/.github   # Linux and macOS
```

`.git` is removed so the project's harness isn't tied to the template, and `.github` because it only holds this repo's CI. Even simpler: download **Source code (zip)** from the [latest release](https://github.com/robmab/one-agent-harness/releases/latest), which already comes without either. **Keep `VERSION`:** it records which template release the harness came from, so later you can check what changed since (see the [releases](https://github.com/robmab/one-agent-harness/releases)). If you want to version it, run your own `git init` afterwards. If you already have the template locally, `Copy-Item <template> '<HARNESS>' -Recurse` works too (remove its `.git` as well).

**Put it wherever you like.** On Windows, **on the same drive as the user profiles** (usually `C:`): the router and OpenCode's config are linked with hardlinks, which don't cross drives. On Linux and macOS everything is a symlink, so anywhere. Your repos can live anywhere.

## 2. Run setup.py

```powershell
py -3 <HARNESS>\setup.py --project "My Project"
```

```bash
python3 <HARNESS>/setup.py --project "My Project"   # Linux and macOS
```

It does what used to be five manual steps (the [appendix](#appendix-manual-setup) has them, to see what it does or repeat one by hand):

- **Names:** `<PROJECT>` and `<HARNESS>` in every file (without BOM, and with `/` in JSON and TypeScript, where a `\` would be an escape); the marketplace and the plugin (`harness-my-project`, `my-project`: the skill prefix in Claude); the router, renamed to `my-project.instructions.md`. On Linux and macOS, also `python3` for `py -3` and `/` in the paths.
- **Language** (`--lang es`): the pieces the model reads (skills, agent, router, `CLAUDE.md`, checklist, `AGENTS.template.md` and the sensor's messages) in Spanish, with Spanish names (`convenios`, `revisor`…). Default `en`. **It's chosen once**, before filling it in: what you write afterwards is yours and can't be translated for you.
- **Profile** (`--profile web`): copies the profile's filled-in skills, security checklist and sensor `RULES` over the template, before naming. Without it, the clean template. **It's chosen once**, like the language. What a profile can't know (your stack's versions, folders, commands) stays marked `TUNE`.
- **Links,** for each tool and user (junctions and hardlinks on Windows, symlinks on Linux and macOS): the plugin link, Claude's `settings.json` (marketplace, plugin and `SessionStart` hook), Copilot's `~/.copilot` and OpenCode's `~/.config/opencode`. If a folder already holds other things (another project's skills), it links skill by skill and leaves the rest alone; if a file is in the way (another router), it stops and tells you ([coexisting](#6-coexisting-with-other-projects)).
- **The rest:** the agent's generated copies (`sync.py`), the sensor's `--selftest`, and the list of what's left to fill in (`FILL-IN`) or to tune (`TUNE`).

| Option | What for |
|---|---|
| `--tools claude,copilot` | only some tools (default: `claude,copilot,opencode`) |
| `--users rober,ana` | Windows: other users on the PC (default: you); their profiles must be on the harness's drive. On Linux and macOS, run it as each user instead (`sudo -u ana python3 <HARNESS>/setup.py`; that user needs write access to the harness folder) |
| `--lang es` | the pieces in Spanish (first run only) |
| `--vscode-permissions` | VS Code reads the harness and runs the sensor without asking ([keeping it in shape](#5-keeping-it-in-shape)) |
| `--dry-run` | says what it would do, without touching anything |
| `--force` | replaces a file in the way, after backing it up |

What it set up is saved in `.setup.json`, next to it. Running it again is safe: whatever is already right is left as is. Before changing a `settings.json` for the first time it keeps a copy alongside (`settings.json.before-harness`), only that one.

## 3. Fill in

To list everything pending:

```powershell
Select-String -Path '<HARNESS>\*' -Pattern 'FILL-IN' -Recurse
```

Each skill opens with its **concept** and leaves its sections as `FILL-IN`. For the method ones (`prepare`, `diagnose`, `verify`, `stack`) you can start from their complete version in [examples](../examples/README.md) and adapt it.

Recommended order (most used first):

1. **`conventions`:** used the most. If the team already has its conventions in the repo, just a pointer here.
2. **`stack`:** the stack table with real versions, and the traps.
3. **`check.py`:**
   - `MARKER`: a file that only exists in that repo. **Mandatory if you work on other projects too** ([coexisting](#6-coexisting-with-other-projects)).
   - `PROJECT_PYTHON`, if there's Python.
   - `RULES`: the traps from step 2 that a regex can catch. Then `py -3 <HARNESS>\personal\scripts\check.py --selftest` checks they are well written.
4. **`verify`:** the real test, lint and build commands.
5. **`diagnose`:** the application layers and their traps.
6. **`ui`:** if there's a UI.
7. **`AGENTS.template.md`:** to the repo root as `AGENTS.md`, if the repo is yours or the team agrees.

(With `--lang es`, the same pieces under their Spanish names: `convenios`, `preparar`, `comprobar`…)

## 4. Verify

1. **Claude**, in a **new session** from the repo (not a fork): "which skills and agents do you have, did the hook reach you and do you have AGENTS.md?". You should see `<project>:*`, the text of `CLAUDE.md` and `AGENTS.md`.
2. **The sensor:** with a rule already in `RULES`, ask Claude to write something that breaks it into a test file in the repo. Right after the edit it should get the `ERROR`. Then delete the file.
3. **VS Code:** reload the window. The skills (`/prepare`…) and the `reviewer` agent should show up in the picker, **only once**.
4. **The router in VS Code:** command palette → "Chat: Configure Instructions" → `copilot-instructions` should be listed **only once**. In a new chat, "which is the only review agent and in what order do you work?" → `reviewer` and the phases.
5. **OpenCode**, from the repo: `opencode run "without touching files: which is the only review agent, what do you run after every change and which skills do you have"` → `reviewer`, the sensor command and **only** the harness skills. `opencode plugin list` → `sensor-<PROJECT>`. For the sensor, the same test as with Claude: the `write` result should carry the `ERROR`.

## 5. Keeping it in shape

- **`py -3 <HARNESS>\setup.py --check`** checks every link and setting and repairs what is safe to repair: a missing link, a hardlink broken by an editor that saved by replacing the file (if the text is still the same) or an out-of-date agent copy. If the copy outside has other text, it doesn't choose for you: it tells you which one is newer.
- **Another user or tool later:** `setup.py --users ana` or `setup.py --tools opencode`.
- **VS Code permission prompts** (`--vscode-permissions`): the harness lives outside the workspace, so Copilot asks for confirmation every time it reads something from it (in real use, around ten per session) and whenever the sensor runs chained to another command. The option adds two settings to each user's VS Code `settings.json`: `github.copilot.chat.additionalReadAccessPaths` with the harness folder, and a `chat.tools.terminal.autoApprove` rule for the sensor script alone. Reload the window afterwards. It only trusts **reading** the harness, not changing it: a model rewriting its own rules is something you should see. Don't use `chat.tools.global.autoApprove` (approve everything): it would also drop the prompts that protect you (database, deletes, push).
- **`setup.py --uninstall`** (`--tools` and `--users` narrow it down): removes the links and settings, only those pointing to this harness. The harness itself stays as it is.

## 6. Coexisting with other projects

The tools don't separate projects. Watch out for this:

- **Claude: plugins apply everywhere.** Each project's skills load in any repo. Therefore:
  - each plugin has a different name, and so a different prefix (`project-a:`, `project-b:`);
  - project skills start with "if you're not in repo X, ignore";
  - the hook's `CLAUDE.md` starts with "if you're in repo X…". Every project's `SessionStart` runs in every session.

  Untested alternative: enable the plugin only in that repo, in its `.claude/settings.local.json` (local, not committed), instead of the user's `settings.json`.
- **The sensor:** each plugin's hook fires on **every** edit. With `MARKER = None` it would also run in other projects' repos. **Always set a `MARKER`** so it only acts on its own.
- **Copilot has no prefixes, and `~/.copilot/skills` is a single folder:**
  - **The method pieces** (`prepare`, `diagnose`, `verify`, `voice`) are the same in every project: link **a single copy**.
  - **The project pieces** (`conventions`, `ui`, `stack`) would clash by name. Better in the repo's `.github/` if possible; otherwise rename them with a prefix (`<project>-conventions`).
  - **The `reviewer`** is a method piece too, but it reads its checklists by path: with several projects, make one copy per project (`<project>-reviewer`) pointing to its own.
  - To mix projects, `~/.copilot/skills` becomes a regular folder with **one junction per skill**:

    ```powershell
    New-Item -ItemType Junction -Path "$HOME\.copilot\skills\<skill>" -Target "<HARNESS>\personal\skills\<skill>"
    ```
- **OpenCode:** `~/.config/opencode` holds a single `AGENTS.md`, a single config and one skills folder, like `~/.copilot`: merge the routers into one file, merge the configs (the allowlist with every project's skills) and use one junction per skill. Plugins do coexist: each has its own `id` (`sensor-<PROJECT>`) and `MARKER`.
- **If the team already has skills and agents in the repo** (`.github/`): Copilot already sees them; **don't copy them into `personal\`**. For Claude, create a separate plugin in `claude\plugins\<project>-repo\` (with its `.claude-plugin\plugin.json`) holding **pointers**: a `SKILL.md` with the same `description` and the body "Read `<path in the repo>` from the repo root and follow it; if it doesn't exist, say so". Never in `~/.claude/skills` or the repo's `.claude/`, because VS Code would show duplicates.

## Appendix: manual setup

What `setup.py` does, step by step: to understand it or to repeat one step by hand. Written for Windows; on Linux and macOS, symlinks (`ln -s`) instead of junctions and hardlinks, `python3` instead of `py -3`, and `/` in the paths. The order: A.1 and A.2 once, A.3 to A.5 for each user.

### A.1 Naming

1. **Marketplace and plugin** (`claude\.claude-plugin\marketplace.json`): `harness-project` → `harness-<project>` and `project` → `<project>`, lowercase with hyphens. Change `owner` too.
   - The plugin name is the **skill prefix in Claude** (`<project>:conventions`), so it must be different for each project.
   - **Don't add `"strict"` or `"version"`** to that entry ([gotchas](DAY-TO-DAY.md#4-gotchas-learnt-the-hard-way)).
2. **In `claude\CLAUDE.md`**, replace the `project:` prefix with the new one.
3. **`<PROJECT>` and `<HARNESS>` in every file.** Save **without BOM**: a BOM in front of the frontmatter's `---` silently breaks the skill. That's why PowerShell 5.1's `Set-Content` won't do:

```powershell
$h = 'REAL_HARNESS_PATH'   # the real path, no placeholders: this is what gets written into the files
$utf8 = New-Object System.Text.UTF8Encoding($false)
Get-ChildItem $h -Recurse -File -Include *.md,*.py,*.ts,*.json,*.jsonc,*.ps1 | ForEach-Object {
  $t = [IO.File]::ReadAllText($_.FullName)
  # in JSON and TypeScript a \ starts an escape: there the path goes with /
  $p = if ($_.Extension -in '.json', '.jsonc', '.ts') { $h.Replace('\', '/') } else { $h }
  $n = $t.Replace('<PROJECT>', 'RealName').Replace('<HARNESS>', $p)
  if ($n -ne $t) { [IO.File]::WriteAllText($_.FullName, $n, $utf8) }
}
```

### A.2 Plugin junction

```powershell
$a = '<HARNESS>'
New-Item -ItemType Junction -Path "$a\claude\plugins\<project>" -Target "$a\personal"
```

(If `claude\plugins` doesn't exist, create it first. The junction name must match the marketplace `source`.)

### A.3 Wire up Claude (for each user)

`C:\Users\<user>\.claude\settings.json`, merged with whatever is already there:

```json
{
  "extraKnownMarketplaces": {
    "harness-<project>": {
      "source": { "source": "directory", "path": "<HARNESS>\\claude" }
    }
  },
  "enabledPlugins": {
    "<project>@harness-<project>": true
  },
  "hooks": {
    "SessionStart": [
      { "hooks": [ { "type": "command", "command": "cat \"<HARNESS>/claude/CLAUDE.md\"" } ] }
    ]
  }
}
```

Mind the slashes: in `"path"` they're **double** (`C:\\path\\to\\harness\\claude`) because it's JSON; in the hook's `cat` they're **forward** (`C:/path/to/harness/claude/CLAUDE.md`) because Git Bash runs it.

The sensor hook doesn't go here: the plugin brings it (`personal\hooks\hooks.json`).

### A.4 Wire up Copilot (for each user)

**If `~/.copilot/skills` and `~/.copilot/agents` are empty or don't exist:**

```powershell
$a = '<HARNESS>'
$u = 'USER_NAME'
foreach ($d in @{ skills = "$a\personal\skills"; agents = "$a\copilot\agents" }.GetEnumerator()) {
  $l = "C:\Users\$u\.copilot\$($d.Key)"
  if (Test-Path $l) { [IO.Directory]::Delete($l) }   # fails if not empty: check what's there first
  New-Item -ItemType Junction -Path $l -Target $d.Value   # agents: the generated copy with VS Code's tool aliases
}
```

`copilot\agents\` is generated by `opencode\sync.py`: VS Code doesn't know Claude's tool names (`Read, Grep…`) and leaves the agent **with no tools**, so its copy says `tools: [read, search, execute]`. Never edit `personal\agents\` from Copilot: VS Code can later restore its own copy of the file with its tool names, and Claude's agent is left with no tools (`sync.py` refuses to run and CI fails if that happens).

**If they already point to another project**, you can't link them twice: see §5.

**The Copilot router** (`copilot\project.instructions.md`; rename it to `<project>.instructions.md`) has `applyTo: "**"`. Both **VS Code chat** and Copilot CLI read `~/.copilot/copilot-instructions.md`, so one hardlink there is enough. Don't also put it in the profile's `prompts\`: VS Code would load it twice. It's a single file: a junction won't do (folders only) and a symlink needs admin or Developer Mode. Link it with **hardlinks**, which need neither (same drive), keeping the original in the harness:

```powershell
$r = '<HARNESS>\copilot\<project>.instructions.md'
foreach ($l in @("C:\Users\$u\.copilot\copilot-instructions.md")) {   # read by VS Code chat and Copilot CLI
  if (Test-Path $l) { Remove-Item -LiteralPath $l }   # plain files, not junctions
  New-Item -ItemType HardLink -Path $l -Target $r
}
```

`~/.copilot` fits only one: with several projects, merge their routers into that file (each block with its "only if you're in repo X").

**Optional: stop the permission prompts for the harness** (what `--vscode-permissions` does, [keeping it in shape](#5-keeping-it-in-shape)). In each user's VS Code `settings.json` (`%APPDATA%\Code\User\settings.json`), for example with `<HARNESS>` = `C:\Harness\Project` (in JSON every `\` is doubled, and inside the regex doubled again):

```jsonc
// read the harness without asking; edits stay limited to the workspace
"github.copilot.chat.additionalReadAccessPaths": [
  "C:\\Harness\\Project"
],
// the sensor (only that script, with or without files) without asking
"chat.tools.terminal.autoApprove": {
  "/^py -3 C:\\\\Harness\\\\Project\\\\personal\\\\scripts\\\\check\\.py(\\s|$)/": true
}
```

Reload the window afterwards.

### A.5 Wire up OpenCode (for each user, optional)

For OpenCode 2 (CLI and Desktop share one server and config). First, in `opencode\opencode.jsonc`, fill in the model and provider (it comes ready for a local OpenAI-compatible server such as llama.cpp; for a cloud one, delete both) and, if the team keeps skills in the repo, their path in `"skills"`.

```powershell
$a = '<HARNESS>'
$c = "C:\Users\$u\.config\opencode"   # OpenCode creates it on first run; keep service.json, delete v1 leftovers (package.json, node_modules)
New-Item -ItemType HardLink -Path "$c\opencode.jsonc" -Target "$a\opencode\opencode.jsonc"
New-Item -ItemType HardLink -Path "$c\AGENTS.md"      -Target "$a\copilot\<project>.instructions.md"   # the same router as Copilot
New-Item -ItemType Junction -Path "$c\skills"         -Target "$a\personal\skills"
New-Item -ItemType Junction -Path "$c\agents"         -Target "$a\opencode\agents"
New-Item -ItemType Junction -Path "$c\plugins"        -Target "$a\opencode\plugins"
```

- **The router** is Copilot's: OpenCode 2 only reads `AGENTS.md`, and the global one is `~/.config/opencode/AGENTS.md`, outside the repo. The `applyTo` frontmatter reaches it as plain text and does no harm.
- **The `reviewer`** in `opencode\agents\` is a **generated copy**: OpenCode ignores the whole agent if its frontmatter has `tools:`. The same script writes Copilot's copy (`copilot\agents\`, with VS Code's tool names). After touching `personal\agents\`, run `py -3 <HARNESS>\opencode\sync.py` (CI warns if you forget). OpenCode-specific settings (subagent, steps, no edits) go in the config's `agents`.
- **The sensor** is the `opencode\plugins\sensor.ts` plugin: after every `write`/`edit`/`patch` it runs `check.py --hook` and appends its output to the tool result, like Claude's hook.
- **The skill allowlist** (`permissions`, action `skill`) lets through only the harness skills: OpenCode walks up from the repo to your home looking for `.claude/skills` and `.agents/skills`, and picks up other tools' skills. **Every new skill goes on the list** (CI checks it).
- **Free web search:** the `ddg-search` MCP (DuckDuckGo, through `uvx`; install `uv` for each user with `winget install astral-sh.uv`). Searching doesn't ask; **reading pages does**, because a page can hide instructions for the model. Add your stack's official docs to the `webfetch` `allow` rules.
- **With a single-slot local model** (llama.cpp with `parallel = 1`): the `title` agent is disabled, because its request evicted the main turn's cache on every new session (14-22 s measured).
