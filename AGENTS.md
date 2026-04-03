# AGENTS.md

This repository is a shared agent product repo for `dob-prompt-buddy`.

Packaging contract:
- Codex repo-scoped path: `.agents/skills/dob-prompt-buddy`
- Codex plugin manifest: `.codex-plugin/plugin.json`
- Codex local marketplace: `.agents/plugins/marketplace.json`
- Claude plugin manifest: `.claude-plugin/plugin.json`
- Self-contained skill logic lives under `skills/dob-prompt-buddy/`

When changing this repo:
1. Keep the skill self-contained. If someone installs only the skill folder, it should still work.
2. Do not hardcode a single Codex home path. Fallback installers must handle `~/.codex/skills` and `~/.agents/skills`.
3. Keep repo-scoped use as the least noisy path: Codex in-repo, Claude with `--plugin-dir .`.
4. Treat `install.sh` as optional convenience, not the only way the product works.
5. Keep git author identity as `Ben Ison <ben@dayonebuilder.online>`.
