# Intervention ladder

Use the lightest intervention that keeps the user from wasting the run.

## Level 1 — Tiny nudge
Use this when the prompt is close.

Examples:
- "Add the output format."
- "Add one verification line."
- "Name the chain."

## Level 2 — Route to one checklist
Use this when the failure mode is obvious.

Examples:
- vague wallet ask → `checklists/wallet-review.md`
- shallow token DD ask → `checklists/token-dd.md`
- APY-chasing yield ask → `checklists/yield-scan.md`

## Level 3 — Give a next-step prompt stub
Use this when the user needs a sharper prompt immediately and a checklist alone is too abstract.

Keep the stub short enough that they will actually paste it.

## Level 4 — Ask for plan mode first
Use this when the user is trying to do too much in one shot.

Typical signs:
- many tasks bundled together
- implementation requested before scope is clear
- no sequence, no milestones, no verification path

The move here is not "more wording."
The move is: split, sequence, or plan first.
