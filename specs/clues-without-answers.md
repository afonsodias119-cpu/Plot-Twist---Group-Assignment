# The clues say what to find, not where or how

Changes only texts and the start card of the 3D game (`prototypes/campus-3d/campus_text.py`, `play.js`). Extends specs/night-and-clues.md and specs/camera-clue.md. No change to the server's rules, `story.py`, `logic.py`, `db.py`, `game.py` or `app.py`.

## Before writing the spec

- **Product and user:** a new player of the 3D game reading the clue card at the start (and the phone's list).
- **Before:** each clue said where and with whom to get it ("on the table", "with the clerk", "computer 12 with the group's help", "Ask the guard for the 23:47 footage"), and the start card added the room of each one. That gives the solutions away.
- **Rule (decided by the team):** the list says only what to get. There are four clues: the USB stick, the photo, the footage and the files.
- **After:**
  - The start card shows only the clue, without its room.
  - The labels (both languages):
    - "Find the group's USB stick" / "Encontrar a pen do grupo";
    - "Get the group's original photo" / "Arranjar a fotografia original do grupo";
    - "Find the footage of the computer lab's camera" / "Encontrar as imagens da câmara da sala de informática";
    - "See the history of the group's files" / "Ver o histórico dos ficheiros do grupo".
  - The order and the count stay as before: four clues, the cameras after the photo.

## Reviewed tests that change

- `tests/test_camera_clue.py` (Afonso): the cameras' label no longer gives the minute (was: "23:47" in the label).

## Done when

- [ ] Every test passes.
- [ ] In the browser: the start card lists four clues, with no rooms and no hints of where they are.
