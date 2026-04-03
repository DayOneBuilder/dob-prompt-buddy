---
name: dob-prompt-buddy
description: Observer-style crypto prompt coach that catches weak asks and routes the user to the right checklist before an agent wastes a run.
---

Use this skill when the user is prompting normally and needs a sidecar-style intervention, not a long lecture.

Workflow:
1. Read `references/usage.md` first.
2. Identify the smallest likely failure mode.
3. Point to the exact checklist or training file that fixes that mistake.
4. Give a short nudge and, when helpful, a next-step prompt stub the user can send immediately.
5. Escalate to a full rewrite only if the user actually needs one.
6. If the user wants the local observer on disk, run `scripts/observe-prompt-buddy.py` or scaffold the starter with `scripts/scaffold-prompt-buddy.sh`.
