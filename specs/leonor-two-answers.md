# Leonor: one right answer, one wrong answer

Extends specs/continuous-conversations.md and specs/library-study-hall.md. Only the 3D screen (`prototypes/campus-3d/play.js`) changes. No change to `story.py`, `logic.py`, `db.py`, `game.py`, `app.py` or the server dialogue (`campus_people.py`).

## Why
When the player meets Leonor with the original photo, the card showed many answers and decisions at once (be sure, have doubts, accuse her, say it is mine, ask again, goodbye, show the photo, ask for help). Too many choices, and the photo could be shown before anything was said, so the conversation did not feel like a decision.

## What
1. **Two answers.** While Leonor can still be asked for help (`ask_for_help` is among the line's actions), the card shows only two answers: "Tell her you have doubts" (right, `soft`) and "Say she is lying" (wrong, `harsh`). The other answers and the decision buttons (`decision` actions) are hidden.
2. **The wrong answer** keeps the server's `harsh` node as it is: it costs time, and she offers "Apologise" (back to the right answer) or "Insist" (closes the conversation).
3. **The evidence button waits.** "📁 Show a piece of evidence" appears only after the right answer was chosen in this conversation.
4. **Showing the photo is asking for help.** Showing `original_photo` to Leonor at that point plays `ask_for_help` (she agrees, says she is coming, and follows the player, as in specs/library-study-hall.md). Other evidence is answered by the server as before.

## Out of scope
The "accuse Leonor" decision no longer appears in the 3D game (the plain game keeps it). Other characters' conversations.

## Reviewed tests that change
- `tests/continuous-conversations.cjs` (Maria): the block "Leonor decisions" expected her decisions to show once they could be taken. Now it expects no decision buttons, only `soft` and `harsh` at the start with the evidence row hidden, and the evidence row visible after `soft`. **Needs Maria's approval in the pull request.**

## Done when
- Existing tests pass, with the change above.
- New tests (`tests/test_leonor_two_answers.py`): the page filters Leonor's answers to `soft`/`harsh`/`closed`, hides her decisions, keeps the evidence row hidden until `soft`, and routes the original photo to `ask_for_help`.
- A browser check: two answers at the start, no evidence button; after the right answer the evidence button appears and showing the photo makes her help and follow; after the wrong answer the clock moves and the evidence button stays hidden.
