# Extending: another tool, and the checks

🌐 **English** · [Español](EXTENDING.es.md)

How to add a tool the harness doesn't cover yet, and what the CI checks on every push.

## 1. Adding another tool (OpenCode, Cursor…)

1. **Find out where it looks,** in its official docs: instructions, skills and agents, at user and workspace level. And whether it reads **other** tools' paths (as VS Code reads `~/.claude`).
2. **Cross-check what already reaches it:** `AGENTS.md`? `.github/`? `~/.claude` or `~/.copilot`? Whatever already reaches it is **not** linked again. Also watch what it finds **walking up** from the repo (OpenCode goes all the way to your home).
3. **Personal pieces:** if its user folder is empty, one junction for the whole `personal\{skills,agents}`; otherwise, one per skill.
4. **Format:** `SKILL.md` is a standard. If it doesn't accept Claude's agent frontmatter, give it its own `<tool>\agents\` folder with pointers.
5. **Global instructions:** via hook or user config, never with an instructions file in a folder above the repo.
6. **Verify** in a new session that it sees everything and that the other tools don't start showing duplicates.

OpenCode is the worked example ([A.5](SETUP.md#a5-wire-up-opencode-for-each-user-optional)): step 2 uncovered the walk up to your home (skill allowlist), and step 4 that it doesn't accept Claude's agent frontmatter (generated copy). DeepSeek Harness is the second ([A.6](SETUP.md#a6-wire-up-deepseek-harness-for-each-user-optional)): step 2 showed that it reads the global router as mere guidance and has no agent files (the router falls back to a subagent); step 5, that the agent preset shadows its global persona, which only the system prompt in the log revealed. Check there that a setting really reaches the model.

## 2. Checks (CI)

On every push, [CI](../.github/workflows/ci.yml) validates the template itself:
- **Structure** ([`validate.py`](../.github/scripts/validate.py)): skill and agent frontmatter (every skill with a `Use when` in its description and a `**CONCEPT:**` line; `name` equal to the folder, no `_`; the original agent with Claude's tool names), no BOM, valid JSON, no `strict`/`version` in the marketplace, the hook's script exists, well-formed SVGs, `VERSION` in SemVer, Markdown links and anchors, and no real user paths. And for OpenCode: the config parses, the allowlist covers every skill in `personal\skills`, the generated agent copies are up to date (OpenCode's without `tools:`, Copilot's with VS Code's names), and the script the plugin runs exists. And the translations in `i18n\`: one for every piece the model reads, with the same lines and headings as the English one (so a change in one shows up in the other), and the names they get after `setup.py`.
- **Sensor:** `check.py --selftest` on Ubuntu and Windows (well-formed `RULES`, engine on sample files), in both languages.
- **`setup.py`** ([`test_setup.py`](../.github/scripts/test_setup.py), on Windows, Linux and macOS): on a temporary copy and fake profiles, one of them already in use, in every language: install, run again without changes, `--check` repairing a broken hardlink and a missing junction (and not touching a copy with other text), `--uninstall` leaving the profiles as they were.

Publishing a release also checks that `VERSION` matches the tag ([release.yml](../.github/workflows/release.yml)). Locally: `python .github/scripts/validate.py`.
