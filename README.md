# DayOneBuilder Prompt Buddy by Ben Ison

Prompt-coaching skill for tightening crypto research prompts before you send them to an agent.

- Product page: https://dayonebuilder.online/products/prompt-buddy/
- Direct bundle: https://dayonebuilder.online/downloads/dayonebuilder-prompt-buddy-starter.zip
- Support future updates: https://checkout.dayonebuilder.online/donate/prompt-buddy

> Shorthand phrase: `Install dayonebuilder/dob-prompt-buddy by Ben Ison.`
>
> Treat that phrase as a convenience prompt, not as the only documented install contract.

## The least noisy setup

### Codex

```bash
git clone https://github.com/DayOneBuilder/dob-prompt-buddy.git
cd dob-prompt-buddy
codex
```

Codex auto-discovers the repo-scoped skill from `.agents/skills/` when you launch Codex inside this repository.

This repo also ships:
- `.codex-plugin/plugin.json`
- `.agents/plugins/marketplace.json`

So if you prefer Codex's plugin directory, you can load this repo as a local plugin source instead of copying files into your home directory.

### Claude Code

```bash
git clone https://github.com/DayOneBuilder/dob-prompt-buddy.git
cd dob-prompt-buddy
claude --plugin-dir .
```

Claude Code loads the plugin from `.claude-plugin/plugin.json` when you launch it with `--plugin-dir .`.

## Optional personal install

If you want a standalone personal install outside the repo, use:

```bash
./install.sh
```

What it does:
- detects `~/.codex/skills` vs `~/.agents/skills` for Codex standalone installs
- installs the self-contained skill into the detected Codex location
- installs the same self-contained skill into `~/.claude/skills/`
- installs a helper launcher into `~/.local/bin/dob-prompt-buddy`

Personal uninstall:

```bash
./uninstall.sh
```

## Why this repo is structured this way

The product has to work in three ways without surprise:
1. **Repo-scoped Codex use** with no global writes
2. **Claude plugin use** with `--plugin-dir .`
3. **Optional standalone install** when you really want a personal global copy

To make that work, the skill is self-contained under `skills/dob-prompt-buddy/`. The helper script and required files live with the skill instead of depending on a separate asset copy in `~/.dayonebuilder/`.

## Quick checks

Repo-local helper:

```bash
bin/scaffold-prompt-buddy.sh ./research/prompt-buddy
```

Standalone launcher after `./install.sh`:

```bash
~/.local/bin/dob-prompt-buddy --help
```
