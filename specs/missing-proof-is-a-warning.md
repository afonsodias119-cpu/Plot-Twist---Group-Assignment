# A missing proof is a warning, not an ending

Changes `campus_evidence.py` (the answer "all" of the hearing), `play.js` and two texts in `campus_text.py`. Replaces point 3 of specs/hand-over-the-proofs.md. No change to `story.py`, `logic.py`, `db.py`, `game.py` or `app.py`. Every text exists in Portuguese and English.

## Before writing the spec

- **Product and user:** a player of the 3D game who presents the evidence to the professor without every proof (for example, without the backup of computer 12).
- **Before:** the night ended at once in "Stolen credit", and the ending named the missing proofs.
- **Rule (decided by the team):** the professor only says how many proofs are missing, never which, and the game goes on.
- **After:**
  1. "Present the evidence" with a proof missing: the server answers with `accepted: false`, `heard: false` and the professor's line, and saves nothing. The hearing is not started, so the player can go and get the proof and present again.
     - One missing: "One of the proofs is missing. Come back when you have it." / "Falta-lhe uma das provas. Volte quando a tiver." (`hearing_short_one`).
     - More: "{n} proofs are missing. Come back when you have them." / "Faltam-lhe {n} provas. Volte quando as tiver." (`hearing_short_many`).
  2. The page shows the line in the professor's card, as his reply.
  3. With every proof, the night ends in "Case closed", as before. If the faculty closes at 23:00 first, the night ends with the closed faculty ("the fifth name is still on the cover"): Duarte keeps the credit.
  4. The ending no longer carries `missing`, and the text `hearing_missing` is gone.

## Reviewed tests that change

None outside this branch (`tests/test_hand_over_the_proofs.py` is new in the same pull request).

## Done when

- [ ] Every test passes, and the `.cjs` checks.
- [ ] `tests/test_hand_over_the_proofs.py`: one or two proofs missing give the warning with the number, name no proof and save nothing; after getting the proof, presenting again closes the case.
- [ ] In the browser: presenting without the backup shows the professor's warning and the game goes on.
