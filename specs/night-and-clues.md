# The night and the clues

> **Update (specs/three-proofs.md, merged after this spec):** Leonor is not a clue of the phone, so the list has three clues (the USB stick, the photo, computer 12) plus the cameras of specs/camera-clue.md; "accuse" no longer exists. She still helps at computer 12 and still leaves at 22:45 if undecided.

Changes the 3D game only (`prototypes/campus-3d/`): campus_clock.py, campus_game.py, campus_text.py, campus_case.py, play.js, play.css and game3d.html. No change to `story.py`, `logic.py`, `db.py`, `game.py` or `app.py`. Extends specs/night-schedule.md, specs/case-of-the-day.md, specs/earlier-nights.md and specs/campus-3d-streamlit.md.

## Why
The team played the game and asked for these changes:
- The night should run from 22:30 to 23:00.
- Finding a clue should never cost time. Only wrong choices should.
- The print shop should not close in the middle of the night.
- The date of the case ("Case of 23 November") and the start-screen note "Night 2. The fifth figure…" add noise.
- New players did not know that the clues are on the phone, or in which order to do them.
- In English, "torch" should be "flashlight".

## What
1. **The clock.** Minute 0 is 22:30 and minute 30 is 23:00 (`campus_clock.START`, `NIGHT_STARTS` in play.js). Every text that names the times says 22:30 and 23:00. The rounds are now at 22:42, 22:49 and 22:56. Leonor leaves at 22:45 while she is undecided, and her warning says "a quarter to eleven". The true ending's clock reads 23:01.
2. **Only wrong choices cost time.** These now cost 0 minutes: the copy of the photo (`request_copy`), asking Leonor for help (`ask_for_help`) and the files of computer 12 (`view_files`). These still cost time: accusing Leonor (1), a wrong card (2), a card shown to Duarte (1), being caught at computer 12 (3), a rude answer (5), a wrong place on the table (1), a wrong code (2), and the order book, the red herring (2).
3. **The print shop does not close.** The clerk stays all night:
   - `LEAVES` has only Leonor;
   - there is no `warn_shop` message and no shutter sentence;
   - the photo can never be lost.

   Leonor's clue is lost only when she leaves undecided.
4. **No date of the case on screen.** The case file, the top bar and the share card no longer show "Case of {day} {month}". The server still keeps the date of each game (`day`).
5. **No night line on the start screen.** The photo still changes from night to night, but the line "Night {n}. …" is not shown.
6. **The clues, in order.** The phone's list (`CLUES`) is in the order the clues have to be done, and its labels say what to do:
   1. Find the group's USB stick on the table (study room).
   2. Put the original photo back together with the clerk (print shop).
   3. Show Leonor the photo and ask her for help (library).
   4. Unlock computer 12 with the group's help (computer lab).

   When the game starts, and after "New game", a card "📱 Your clues" lists them in this order, each with its room, and ends with "At the end, show the evidence to the professor, in the auditorium."
   - "Got it" (or Esc) closes the card, and "Clues" opens the same list in the phone.
   - While the card is open, the character stands still and the countdown waits.
   - In a continued game, the clues already done are crossed out.
7. **Flashlight.** In English the menu button and the rules say "Flashlight". The Portuguese "Lanterna" stays.

## Reviewed tests that change
Each changed line keeps a comment "changed by specs/night-and-clues.md" and what it was.
- `tests/test_night_schedule.py` (Guilherme): the times; the clerk no longer leaves (no `warn_shop`, no shutter, the photo is never lost); the new costs.
- `tests/test_campus_3d.py` (Maria): the order of the clues.
- `tests/test_case_of_the_day.py` (Guilherme): the page no longer shows the date.
- `tests/test_creator_after_name.py` (Mariana): the brief says 22:30 and 23:00.
- `tests/test_earlier_nights.py` (Guilherme): the true ending says 23:01, and the start screen has no night line.
- `tests/test_rules_and_character.py` (Afonso): nothing changes in it, because the keys stay `torch_on` and `torch_off`.
- Other tests the full run shows, listed in the pull request.

**Needs the approval of Guilherme, Maria and Mariana in the pull request.**

## Done when
- The tests pass, with the changes above.
- New tests (`tests/test_night_and_clues.py`):
  - the clock starts at 22:30 and ends at 23:00;
  - finding a clue costs nothing;
  - the clerk never leaves;
  - the clues are in order;
  - the start card exists in both languages;
  - no date and no night line are on screen;
  - "Flashlight" is used in English.
- A browser check:
  - the card at the start, then "Got it";
  - the clock at 22:30;
  - no date on the case file;
  - the print shop still open after 22:40.
