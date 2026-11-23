# The table note, and José checks what you want to see

Extends specs/hidden-object-table.md, specs/more-to-find.md (the K note) and specs/security-desk.md. Only the 3D screen changes (`game3d.html`, `play.js` and three texts in `campus_text.py`). No change to the story, the rules, the server or any reviewed test.

## Why
- Players walked past the study room's table without knowing that the USB stick is hidden there.
- With José, the recordings opened straight away. The team wants him to check first what the player wants to see, so that the player says it out loud: 23:47, in the computer lab.

## What
1. **The table note.** While the USB stick is still to be found, a player within 1 m of the table's edge in the study room sees the near note **"Press the K key to search the table for the USB stick"** (`press_table`).
   - K, or a tap on the note, opens the table's close-up, as a click on the table does.
   - A person closer than the table's edge still comes first.
   - Once the stick is found the note no longer appears.
2. **José checks.** *(Replaced by specs/guard-answer-and-cameras.md: now the player answers his question "Which camera, and at what time?".)* After the cables are plugged in, "Watch the recordings" no longer opens them straight away. José asks **"So you want to see who was in the computer lab at 23:47, right?"** (`confirm`). Only the answer **"Yes, exactly"** (`opt_yes`) opens the recordings. Once the picture is kept, "Watch the recordings again" opens them directly, as before.

## Done when
- Existing tests pass unchanged.
- New tests (`tests/test_table_hint_and_guard_check.py`):
  - the texts exist in both languages;
  - the 3D adds "table" only while searching is possible and within 1 m;
  - K opens the table;
  - José's "Watch the recordings" goes to `confirm`, and only "Yes" goes to `watch`.
- A browser check:
  - the note beside the table;
  - K opens the close-up;
  - José's question, then "Yes", then the recordings.
