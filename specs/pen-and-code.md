# The hidden USB stick and the code of computer 12

> **Update (specs/calendar-code.md):** the cover photo is now dated Saturday 17 October, so the code of computer 12 is `1710`, the photo's stamp says 17.10 and the slip on the shutter says 17 October. The clerk's `order` line no longer says the date.

Extends specs/harder-campus.md and specs/campus-people-and-atmosphere.md. Option A of the team discussion: everything happens in the 3D game. No change to `story.py`, `logic.py`, `db.py`, `game.py`, `app.py` or any reviewed test; the plain game (`app.py`) plays as before.

## Why
Getting the two key clues is one click each: Rita opens the drawer, computer 12 shows the files. The player should have to look and to think: find the USB stick among the mess of the study room, and work out the password of computer 12 from what people say.

## What
1. **Search the study room.** The study room is full of things: the group drawer, a coat on a chair, a mug, a backpack, a pile of books, scattered papers, a bin, a plant pot and a pizza box. In the 3D game the player clicks them (the pointer becomes a hand over them). The USB stick is in one of them; each wrong one shows what is there instead ("Cold coffee. Nothing inside.") and **costs 1 minute** of the countdown. The text mode shows the same places as buttons.
2. **Where the answer lives.** New operation `search` (`player`, `language`, `spot`). The server checks that the spot exists, that the saved scene is the study room and that the stick was not found yet. The right spot (`PEN_SPOT`) and the texts of each spot are in `campus_search.py`, which is read only by the server and never put in the page, so the page cannot give the answer away. A wrong spot changes nothing and answers `found: false`; the right spot plays the story's own `open_drawer` action (so the stick is saved exactly as before) and answers `found: true`.
3. **Rita gives a hint, not the stick.** The conversation no longer offers "▶ Open the group drawer" (the server still offers it, so the reviewed tests do not change; the screen leaves it out). Rita has a new answer: asked about the USB stick, she says it is not in the drawer and that the group stayed late eating pizza.
4. **Computer 12 asks for a code.** "▶ Look at the old project files" is replaced on the screen by "Enter the code": a small field for 4 digits inside the computer's menu. New operation `unlock` (`player`, `language`, `code`). The server compares the code with `PC12_CODE` (1411, in `campus_search.py`, never sent to the page). A wrong code changes nothing, answers `unlocked: false` and costs 1 minute; the right code plays the story's own `view_files` action (which still needs the USB stick) and answers `unlocked: true`.
5. **The clues for the code.** Tomás (asked kindly) says the password is the day and month the cover photo was taken. The clerk of the print shop says the group took the photo and had it printed on the same day, 14 November. So the code is 1411. Both lines go to the diary.

## Limits
The search and the code are puzzles, not security: the reviewed tests still play `open_drawer` and `view_files` directly, so the server keeps accepting them, and a hand-made request could skip both puzzles. The 1-minute costs are taken in the browser, like the countdown.

## Out of scope
Changing the story or its rules, other hidden objects, a code for anything else, the plain game.

## Done when
- Existing tests pass unchanged.
- New tests (`tests/test_pen_and_code.py`): a wrong spot finds nothing and saves nothing; the right spot gives the stick once; searching outside the study room is refused; unknown spots and extra fields are rejected; a wrong code saves nothing; the right code views the files with the stick and is still refused without it; the page never contains the code, the right spot or the texts of the spots; the hints of Tomás and the clerk exist in both languages; the spots have labels in both languages.
- A browser check shows clicking the objects (wrong and right), the hint of Rita, and the code field (wrong and right).
