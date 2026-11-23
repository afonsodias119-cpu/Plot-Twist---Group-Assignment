# The professor: one line of thought, then the evidence; and what to do when Duarte speaks

Changes the professor's tree in `prototypes/campus-3d/campus_people.py`, the page (`play.js`) and one text in `campus_text.py`. No change to the server's rules, `story.py`, `logic.py`, `db.py`, `game.py` or `app.py`. Every text exists in Portuguese and English.

## Before writing the spec

- **Product and user:** a player of the 3D game who reaches the professor in the auditorium.
- **Before:** his first line offers "Ask how many members…" and "Say you will bring proof" side by side, and "Present the evidence to the professor" is there from the first line. The chain "five / only four" ends with a goodbye. In the hearing, Duarte speaks and the player sees cards with no word on what they are for.
- **Rule:** one line of thought, in this order: the professor asks about tomorrow's presentations → the player asks how many members the group has → "Five" → the player says there are only four → he asks for proof → only now the player says they will bring proof → "Present it when you are ready" → only now the button to present the evidence. In the hearing a short line says what to do when Duarte speaks.
- **After:**
  1. `start`: "Ask how many members your group has on the list" (and, from night 4, his memory answer), and "Goodbye". "Say you will bring proof" is no longer there.
  2. `list` ("Five, according to the cover…") → "Say there are only four of you" → `evidence`.
  3. `evidence` (new text): "Then I need evidence, not a feeling: who did the work, who is in the photo, who wrote in the group." (the three claims of the hearing). Its one answer is "Say you will bring proof" → `proof`. The diary note follows.
  4. `proof`: "Evidence is welcome. Present it when you are ready." Only on this line does the card show "Present the evidence to the professor" (the hearing) and its line "Once you start, you cannot leave the auditorium."
  5. The hearing card shows, under "Claim n of 3", the line `hearing_how`: "Duarte makes a claim. Answer with the proof that shows it is false, or say nothing." / "O Duarte faz uma afirmação. Responde com a prova que mostra que é falsa, ou não digas nada."

The server still accepts the `hearing` and `present_evidence` requests as before (the tests play them directly); only the page waits for the `proof` line.

## Reviewed tests that change

None.

## Done when

- [ ] Every test passes, and `node tests/continuous-conversations.cjs`.
- [ ] `tests/test_professor_line_of_thought.py`: the order of the lines in both languages, the labels, the button only on `proof`, and `hearing_how`.
- [ ] In the browser: the professor's conversation goes how many → five → only four → bring proof → present the evidence; the hearing card shows the line about Duarte's claim.
