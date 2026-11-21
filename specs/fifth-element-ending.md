# The fifth element: a secret ending and a proper ending screen

Extends specs/spot-the-fake.md and specs/campus-people-and-atmosphere.md. No change to `logic.py`, `db.py`, `game.py` or `app.py`.

## Why
After "Present the evidence" the 3D game only changed the text of a side panel, which the player may have closed, so the game looked stuck. A story this twisty also deserves one ending nobody expects.

## What
1. **A fourth ending, `fifth_element` ("The fifth element" / "O quinto elemento")**, in both languages, first in the list. Its condition is that **all five** chat messages are flagged (`flagged_1` to `flagged_5` true), whoever the player trusted. It is a surreal twist: flagging everything makes the professor doubt the fifth name itself, Duarte reveals that the fifth element is whoever appears "when four people stop believing each other", disappears in the spotlight, and the printed photo now shows five silhouettes, the fifth one in the detective's hat, scarf and coat. It uses only the existing flags and rules; the other three endings keep their conditions (`full_case` needs `flagged_1` and `flagged_3` false, so the two never overlap).
2. **An ending screen over the 3D picture**, for every ending: a stamp (CASE CLOSED, IMPOSTOR EXPOSED, STOLEN CREDIT, THE FIFTH ELEMENT), the ending's title and text, falling confetti, and two buttons: "Play again" (opens the usual new-game confirmation) and "See the scene" (hides the screen; the text stays in the side panel, which opens by itself). The colour follows the ending.
3. In the 3D campus Duarte disappears in the `impostor` and `fifth_element` endings, and in `fifth_element` the lights of the auditorium flicker.

## Reviewed tests that change
One assertion of `tests/test_base_game.py` changes because the requirement changes: in `test_every_ending_is_reachable_from_a_new_game` the endings found become exactly `impostor`, `stolen_credits`, `full_case` and `fifth_element`. Its author (Guilherme) must approve it in the pull request. No test is skipped or deleted.

## Out of scope
Sound or animation files, a new scene, new items or flags. A game saved before this change stays valid (no flag was added).

## Done when
- Existing tests pass, apart from the assertion above.
- New tests: the new ending is reached by flagging all five messages (both languages, with and without Leonor's help); flagging four, or the right three, does not reach it; it is first in the list and the last ending is still the catch-all; every ending has a stamp in both languages; the ending screen exists in the page.
- A browser check shows the ending screen for the new ending and for an old one, with the side panel closed.
