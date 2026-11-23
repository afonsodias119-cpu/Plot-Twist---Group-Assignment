# The security cameras in the list of clues

Extends specs/night-and-clues.md and specs/security-desk.md. Only the 3D screen changes (`play.js`, and two texts in `campus_text.py`). No change to `story.py`, `logic.py`, `db.py`, `game.py`, `app.py`, the server rules or any reviewed test.

## Why
The list of clues (the phone and the card at the start) did not say that José, the security guard, has the camera recordings. Those recordings show who was at computer 12 at 23:47.

## What
1. A clue **"Ask the guard for the 23:47 footage of the computer lab"**, in the room "Entrance (security)", comes after the photo in the phone's list, in the start card and on the share card. It sits there because the photo is what convinces José.
2. The clue is done when the picture of 23:47 has been kept as proof (`footage` of specs/security-desk.md, kept in this browser).
3. The security desk lives on the screen only, so the server does not know this clue: the auditorium door and the messages of the unknown number still count only the server's four clues. Making the footage a card for the professor is phase 2 of specs/security-desk.md.

## Done when
- Existing tests pass unchanged.
- New tests (`tests/test_camera_clue.py`):
  - the texts exist in both languages;
  - the page puts the cameras after the photo;
  - the clue is done from `footage`;
  - the phone list, the start card and the share card use it.
- A browser check: the start card shows five clues, the cameras third.
