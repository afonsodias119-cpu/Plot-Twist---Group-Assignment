# José's question, and a camera in every room

Replaces point 2 of specs/table-hint-and-guard-check.md, and extends specs/security-desk.md. Only the 3D screen changes (`play.js`, `game3d.html` and two texts in `campus_text.py`). No change to the story, the rules or the server.

## Why
- Once the cables are plugged in, José asks "We have a signal. Which camera do you want to see, and at what time?" The player should answer that question, not be asked a second one.
- Nothing in the rooms showed that there are cameras at all.

## What
1. **The answer to José.** After the cables, his question (`ready`) is answered with **"The computer lab one, at 23:47"** (`opt_ask_lab`).
   - He agrees: **"Okay, okay, you can watch. I will put the computer lab camera on 23:47 for you."** (`granted`).
   - **"Watch the recordings"** then opens them on the computer lab camera at 23:47 (`watch_lab`), where the picture can be kept as proof.
   - Once the picture is kept, "Watch the recordings again" opens them as before (`watch`).
2. **A camera in every room.** A security camera hangs high in a corner of each of the five rooms, and one hangs by the entrance:
   - a pole from the ceiling;
   - a white body looking down at the middle of the room;
   - a black lens;
   - a red light that blinks about once a second.

   They are scenery only: they cannot be clicked and do not block the way.

## Reviewed tests that change
- `tests/test_table_hint_and_guard_check.py` (Afonso): the texts and the path of José's conversation, now `opt_ask_lab` → `granted` → `watch_lab`. Was `confirm` and `opt_yes`.

## Done when
- The tests pass, with the change above.
- New tests (`tests/test_guard_answer_and_cameras.py`):
  - the texts exist in both languages;
  - `watch_lab` opens the computer lab at 23:47;
  - there are six cameras with one blinking light material.
- A browser check:
  - José's question;
  - the answer;
  - his agreement;
  - the recordings open on the computer lab at 23:47;
  - a camera with its red light visible in a room.
