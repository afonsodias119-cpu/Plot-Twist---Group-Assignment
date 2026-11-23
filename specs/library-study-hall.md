# The library as a study hall, and Leonor coming with you

Extends specs/calendar-code.md (followers) and specs/campus-people-and-atmosphere.md. Only the 3D picture and one line of the screen change. No change to `story.py`, `logic.py`, `db.py`, `game.py`, `app.py`, the server or any reviewed test.

## Why
The library had one table and Leonor standing beside it: it did not look like a library at night before a deadline. And when Leonor agrees to help, nothing on the screen says that she is coming to the computer lab, although she follows the player there (specs/calendar-code.md) and remembers the day of the code.

## What
1. **A study hall.** The single table is replaced by two long tables and a small one, each with chairs, two desk lamps, open books, laptops (the lid opens around its back edge, the screen faces the person) and piles of books. The rug lies under the two long tables. The bookshelves, the globe, the noticeboard and the trolley of returned books stay where they were (the things to look at of specs/more-to-find.md are not moved).
2. **Students studying.** Six students sit at the tables, each with a book or a laptop in front of them, their heads moving slightly as they read. They are part of the picture only: they are not people you talk to, they have no name tag and no collision box of their own (the chairs and tables have theirs). A walkway from the door to the shelves stays free between the two long tables.
3. **Leonor studies at her place.** She sits at the second long table (`seat`), facing the door, and does not turn while sitting. When she follows the player (after `ask_for_help`) she stands up and walks behind them, as before; back at her place she sits again. Her collision box and her place (`home`) move with her chair.
4. **She says she is coming.** Right after "Show the photo and quietly ask for help" in the 3D game, Leonor adds one line: she closes her book, stands up and says she is coming to the computer lab, and that she remembers things about that day if computer 12 asks for a code (`leonor_follow`, both languages). It is read aloud like her other lines.

## Out of scope
Students you can talk to, new clues, moving the shelves, the plain game.

## Done when
- Existing tests pass unchanged.
- New tests (`tests/test_library.py`): the line exists in both languages and is shown right after `ask_for_help`; Leonor has a seat and sits only while at home and not walking; there are six students, sitting, with a book or a laptop each; the old single table is gone and the things to look at are still there.
- A browser check shows the study hall, Leonor sitting, the K note next to her, her line after asking for help, and her following the player.
