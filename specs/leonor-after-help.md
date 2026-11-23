# Leonor after she agrees to help

Extends specs/leonor-two-answers.md. Only the 3D screen (`prototypes/campus-3d/play.js`) changes. No change to `story.py`, `logic.py`, `db.py`, `game.py`, `app.py`, the server or any reviewed test.

## Why
After the player shows Leonor the original photo she believes them and says she is coming to the computer lab. But the card then showed her usual questions again ("Ask whether she is sure…", "Say she is lying"…), which makes no sense once she is on the player's side.

## What
1. Once Leonor agreed to help (she is in the server's `followers`, i.e. `colleague_choice == "help"`, specs/calendar-code.md), her conversation card shows her lines but **no answers, no actions and no "📁 Show evidence"**. Only "End conversation" is left, highlighted as the way out.
2. This holds right after she agrees and every time the player talks to her again.
3. At computer 12 she still tells what she remembers (that is the computer's own flow, not her card).

## Out of scope
The plain game, other characters, the server dialogue.

## Done when
- Existing tests pass unchanged.
- New tests (`tests/test_leonor_after_help.py`): the page checks `followers` for Leonor, clears her options and actions, and hides "Show evidence" while she helps.
- A browser check: after the photo, and after closing and talking to her again, no answers and no evidence button.
