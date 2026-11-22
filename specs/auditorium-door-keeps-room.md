# A refused door does not move the character

A bug fix in the 3D game. No change to the server, `story.py`, `logic.py`, `db.py`, `game.py`, `app.py` or any reviewed test.

## Before writing the spec

- **Product and user:** a player of the 3D game who walks to the auditorium before having every clue.
- **Trigger:** the player walks from the library, the print shop or the computer lab through the auditorium door.
- **Before:** every room connects only to the study room, so the server walks library → study room → auditorium. The first step is saved (the reviewed test `test_a_blocked_second_step_leaves_you_in_the_study_room` asks for this), then the auditorium refuses. The 3D sees that the saved room changed and moves the character to the study room, the first room of the game: it feels like being sent back to the start.
- **Rule:** a refused door never moves the character; it only steps back into the corridor, by that door.
- **After:** the player sees "You do not have all the evidence yet…" and stands in the corridor in front of the auditorium. The saved room is the study room, as the server decided; walking back into any room works as usual.

## What

- [ ] `prototypes/campus-3d/game3d.html`, `checkEnter`: when the answer is refused (`accepted` is false) or the scene did not change, the character steps back into the corridor and the 3D remembers the new saved room without moving there.
- [ ] `syncCampus` does not move the character while a refused door is being handled.

## Done when

- [ ] Existing tests pass unchanged.
- [ ] `tests/test_hidden_object_table.py`: the two conditions above are in `game3d.html`.
- [ ] In the browser: from the library, walking into the auditorium without the clues leaves the character in the corridor by the auditorium door.
