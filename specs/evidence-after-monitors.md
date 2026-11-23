# "Show evidence" waits for the guard to ask for a proof, and is gone for Rita; Rita's photo after the USB stick

Changes specs/security-desk.md (on the page only), specs/two-answers.md and Rita's tree in `campus_people.py`. No change to the server's rules, `story.py`, `logic.py`, `db.py`, `game.py` or `app.py`. Every text exists in Portuguese and English.

## Before writing the spec

- **Product and user:** a player of the 3D game talking to José (the guard) and to Rita.
- **Before:** José's card shows "📁 Show evidence" from his first line, before the player knows why a proof matters. Rita's card shows it too, although her lie is broken by the right answer. Right after Rita says the USB stick could be anywhere ("with this mess"), the next right answer asks about the group photo, so the player is pulled away from looking for the stick.
- **Rule:**
  1. With José, "Show evidence" appears only once he has asked for a proof: after "Explain the situation" (his `explain` line, "Camera footage is not given to just anyone. Show me something that proves what you say."), and on the lines after it.
  2. Rita never shows "Show evidence" (her claim line is broken by its right answer, specs/two-answers.md).
  3. Rita's line about the USB stick (`pen`) has no answer: the player goes to look. Her first line (and `sorry`) asks about the stick while it is not found, and about the group photo once it is (`if` `lacks` / `has` `usb_stick`), each with its wrong answer.
- **After:** José: "Explain the situation" / "Ask about the monitors" with no evidence row; after "Explain the situation", the evidence row. Rita's line about the stick says it could be anywhere **on the table**, so the player knows where to look. Rita: "Ask where the USB stick is" → "…it could be anywhere" (no answers); once the stick is found, "Ask about the group photo" → "Ask why the photo in the folder shows five" → her claim, as before.

## What

- [ ] `prototypes/campus-3d/play.js`: `NO_EVIDENCE` gains `rita`; `guardWaits` hides the row for José until `explain`.
- [ ] `prototypes/campus-3d/campus_people.py`: Rita's `start` and `sorry` answers by `usb_stick`; `pen` has only its goodbye.
- [ ] `docs/guiao-conversas.md`, `docs/plano-do-projeto.md`.

## Reviewed tests that change

- `tests/test_night_schedule.py`: route 11 no longer asks Rita about the stick after finding it; it now fits up to 35 seconds a command and no longer at 36.

## Done when

- [ ] Every test passes, and `node tests/continuous-conversations.cjs`.
- [ ] `tests/test_two_answers.py`: Rita's first line by the stick, `pen` without answers, the photo then her claim; the evidence row rule for Rita and José.
- [ ] In the browser: Rita without the stick ("Ask where…", then no answers) and with it ("Ask about the group photo"); no evidence row with her. In 3D, José's evidence row appears only after "Explain the situation".
