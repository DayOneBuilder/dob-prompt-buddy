---
name: dob-prompt-buddy
description: Prompt-coaching skill for tightening crypto research prompts before you send them to an agent.
---

Use this skill when the user has a weak crypto prompt and wants help turning it into a sharper request before sending it to an agent.

Workflow:
1. Read `references/usage.md` first.
2. Load only the relevant checklist from `references/checklists/`.
3. Use `references/examples/weak-to-strong.md` when the user needs a rewrite pattern.
4. If the user wants the local bundle files, run `scripts/scaffold-prompt-buddy.sh` inside the repo or inside the installed standalone skill.
5. Keep the output practical: identify what is missing, why it matters, and provide a stronger prompt the user can send immediately.
