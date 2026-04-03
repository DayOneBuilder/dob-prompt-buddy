# DayOneBuilder Prompt Buddy by Ben Ison

Observer-style prompt coach for crypto work.
It is a terminal sidecar/TUI that sits beside the user in the terminal, notices when the prompt is slipping, and points them to the exact fix before an agent wastes a run.

- Product page: https://dayonebuilder.online/products/prompt-buddy/
- Direct bundle: https://dayonebuilder.online/downloads/dayonebuilder-prompt-buddy-starter.zip
- Support future updates: https://checkout.dayonebuilder.online/donate/prompt-buddy

> Shorthand phrase: `Install dayonebuilder/dob-prompt-buddy by Ben Ison.`
>
> Treat that phrase as a convenience prompt, not as the only documented install contract.

## What is shipped right now

Prompt Buddy does **not** pretend to be a desktop overlay or full graphical on-screen pet UI.

The real shipped slice today is:
- a terminal sidecar/TUI MVP for typing or pasting prompts and getting an immediate intervention report
- a local observer CLI that inspects a prompt
- readable routing heuristics for common failure modes
- a training pack with the exact checklists the observer should point at
- a packaging layout that keeps it installable from agent workflows

That means the product direction is now:
- not a generic prompt rewrite bundle
- not a big wall of prompt theory
- a sidecar-style observer that intervenes only when needed

## Quick start

### Repo-local sidecar TUI

```bash
bin/sidecar-prompt-buddy.sh
```

Paste or type a multi-line prompt, then press `Ctrl-G` to analyze it.

Repo-local plain one-shot:

```bash
bin/sidecar-prompt-buddy.sh --plain "review this token"
```

### Installed sidecar TUI

```bash
./install.sh
dob-prompt-buddy sidecar
```

Installed plain one-shot:

```bash
dob-prompt-buddy sidecar --plain "review this token"
```

### Repo-local observer

```bash
bin/observe-prompt-buddy.sh "look at this wallet"
```

### Scaffold the starter pack

```bash
dob-prompt-buddy scaffold ./prompt-buddy-starter
```

## What the observer and sidecar catch

The current heuristics look for avoidable failures such as:
- missing concrete goal or success criteria
- missing output format
- missing evidence or verification rules
- missing chain / repo / environment context
- giant ambiguous asks that should be split or planned first
- execution requests that should start in plan mode

The output is intentionally short and honest:
- severity
- domain guess
- likely slips
- one concise nudge
- exact local files/checklists to open next
- a next-step prompt stub when useful

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

After install, these are the useful commands:

```bash
dob-prompt-buddy --help
dob-prompt-buddy sidecar
dob-prompt-buddy sidecar --plain "review this token"
dob-prompt-buddy observe "review this token"
dob-prompt-buddy scaffold ./prompt-buddy-starter
```

Personal uninstall:

```bash
./uninstall.sh
```

## Why this repo is structured this way

The product has to work in three ways without surprise:
1. **Repo-scoped Codex use** with no global writes
2. **Claude plugin use** with `--plugin-dir .`
3. **Optional standalone install** when you really want a personal global copy

To make that work, the skill is self-contained under `skills/dob-prompt-buddy/`. The observer CLI, terminal sidecar, and training files live with the skill instead of depending on a second hidden asset copy.

## What this sidecar is and is not

What it is:
- a terminal sidecar/TUI you can keep beside your normal prompting flow
- a lightweight observer that points to the smallest useful fix
- a stdlib-only MVP that reuses the same analysis logic as the observer CLI

What it is not:
- a desktop overlay
- a graphical floating pet
- a promise that the prompt becomes "magic" once it passes the check

## Quick checks

Repo-local sidecar in plain mode:

```bash
bin/sidecar-prompt-buddy.sh --plain "Analyze this wallet"
```

Repo-local observer:

```bash
bin/observe-prompt-buddy.sh "Analyze this wallet"
```

Repo-local starter scaffold:

```bash
bin/scaffold-prompt-buddy.sh ./research/prompt-buddy
```

Standalone launcher after `./install.sh`:

```bash
~/.local/bin/dob-prompt-buddy --help
~/.local/bin/dob-prompt-buddy sidecar --plain "review this token"
```
