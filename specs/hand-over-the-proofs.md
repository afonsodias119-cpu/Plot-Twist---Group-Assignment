# The professor: present the evidence or ask, then hand over every proof at once

> **Update (specs/missing-proof-is-a-warning.md):** a missing proof no longer ends the night. Point 3 (the ending names the missing proofs) is replaced: the professor says only how many are missing and the night goes on.

Changes the 3D server (`campus_evidence.py`), the page (`play.js`) and two texts in `campus_text.py`. Extends specs/professor-line-of-thought.md and specs/hearing-show-evidence.md. No change to `story.py`, `logic.py`, `db.py`, `game.py` or `app.py`. Every text exists in Portuguese and English.

## Before writing the spec

- **Product and user:** a player of the 3D game who reaches the professor.
- **Before:** the button to present the evidence appeared only after the chain "how many → five → only four → I will bring proof". Then Duarte made four claims and the player chose a proof for each one.
- **Rule (decided by the team):**
  1. The professor's first line offers two things: present the evidence, or ask how many members the group has. The chain that ends in "I will bring proof" offers nothing more.
  2. Presenting the evidence hands over every proof the player holds, at once. If one is missing, the game says which.
- **After:**
  1. "Present the evidence to the professor" is on his `start` line, beside "Ask how many members…" (and, from night 4, his memory answer). Under it: "You hand over every proof you have, at once." / "Entregas de uma vez todas as provas que tens." The chain how many → five → only four → bring proof ends on `proof`, with no answer but the end of the conversation.
  2. The button sends `hearing` with the new answer `"all"`. The server answers every claim still waiting with a held card that breaks it, or with "concede" when none is held, and ends the night exactly as after the last answer (same verdict, same row of `runs`). It is refused before the auditorium, after the ending and at 22:45, like any answer. The old answers ("start", a card, "concede") still work.
  3. The ending carries `missing`: the labels of the proofs that would have broken the claims left without one (empty when the case is closed). The ending card shows them above the verdict: "Missing proofs: …" / "Faltam provas: …".

## Reviewed tests that change

- `tests/test_professor_line_of_thought.py`: the hearing button is on the professor's first line (was: only on `proof`).

## Done when

- [ ] Every test passes, and the `.cjs` checks.
- [ ] `tests/test_hand_over_the_proofs.py`: every proof closes the case with nothing missing; without the backup and the recording, Stolen credit with both named (both languages); refused before the auditorium and twice; a bad answer raises; the page sends "all" and shows what is missing.
- [ ] In the browser: the professor offers the two options; the chain ends on "I will bring proof"; presenting hands everything over; a missing proof is named on the ending card.
