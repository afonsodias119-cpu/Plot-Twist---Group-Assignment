# The professor: "Show evidence" or ask; select the proofs to hand over

Changes `campus_evidence.py` (the hearing takes a list of cards), `play.js` and texts in `campus_text.py`. Replaces the button of specs/hand-over-the-proofs.md (point 1) and keeps the warning of specs/missing-proof-is-a-warning.md. No change to `story.py`, `logic.py`, `db.py`, `game.py` or `app.py`. Every text exists in Portuguese and English.

## Before writing the spec

- **Product and user:** a player of the 3D game who reaches the professor.
- **Before:** his first line had the story's button "Present the evidence to the professor" with the line "You hand over every proof you have, at once.", and the "Show evidence" row of every conversation (a wrong card cost 2 minutes).
- **Rule (decided by the team):** the professor's first line offers only "📁 Show evidence" and "Ask how many members your group has". The chain how many → five → only four → "Say you will bring proof" ends there. "Show evidence" lets the player select the proofs they have and hand them over: a proof missing → he says how many and the player can still go and get it; every proof → the case is closed.
- **After:**
  1. On the professor's `start` line: the row "📁 Show evidence" and the answer "Ask how many members…" (and, from night 4, his memory answer). No other line of his has the evidence row. The story's button and the line `hearing_hint` are gone.
  2. "Show evidence" opens the tray "Which proofs do you hand the professor?" / "Que provas entregas ao professor?": one box (☐/☑) for each proof held, "Hand them to the professor" / "Entregar ao professor" (only with at least one ticked), and "Put it away". With no proof, "You have nothing to show yet."
  3. Handing over sends `hearing` with the list of the ticked cards. The server checks every card (known, held, no repeats, not empty) and answers each claim with a handed card that breaks it. A claim with none: the warning of specs/missing-proof-is-a-warning.md (how many, never which), nothing saved, and the tray goes back to his first line. Every claim broken: the night ends in "Case closed".

## Reviewed tests that change

- `tests/test_evidence_and_hearing.py`: no `hearing_hint` among the texts; a list of held cards is now a valid answer, so the bad list in the rejection test is `["knife"]` (was `["files"]`).
- `tests/test_professor_line_of_thought.py`: "Show evidence" only on his first line, and no story button.

## Done when

- [ ] Every test passes, and the `.cjs` checks.
- [ ] `tests/test_hand_over_the_proofs.py`: a held proof left out counts as missing; with all four the case is closed; bad selections raise; the page sends the ticked ids and goes back after the warning.
- [ ] In the browser: the professor offers "Show evidence" and "Ask how many members"; the tray ticks proofs; a missing one gives the warning; all four close the case.
