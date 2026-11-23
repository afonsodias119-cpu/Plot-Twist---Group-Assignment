# The order of the clues, and Leonor back in the list

Changes the list of clues of the 3D game: the start card and the phone's Clues app (`play.js`, texts in `campus_text.py`). Extends specs/clues-without-answers.md, specs/camera-clue.md and specs/three-proofs.md. No change to the server's rules: the server's clues stay the photo, the USB stick and the files, and Leonor is still not a proof.

## Why
The team wants the list to follow the order in which the night is best played, and to remind the player to ask Leonor for help, because her memory is needed at computer 12.

## What
The start card and the phone show five clues, in this order. The labels below are Portuguese / English.
1. "Encontrar a fotografia original do grupo" / "Find the group's original photo" (server).
2. "Encontrar a pen do grupo" / "Find the group's USB stick" (server).
3. "Falar com a Leonor e pedir a sua ajuda" / "Talk to Leonor and ask for her help" (page only, `clue_leonor`). It is done once she follows the player (the server's `followers`).
4. "Encontrar as imagens da câmara de vigilância junto do segurança" / "Find the surveillance camera footage with the security guard" (page only). It is done once the picture is kept (`footage`).
5. "Ver o histórico dos ficheiros do grupo" / "See the history of the group's files" (server).

"At the end, show the evidence to the professor, in the auditorium." stays under the list.

## Reviewed tests that change
- `tests/test_camera_clue.py` (Afonso; last changed by Mariana): the order of the list. Was: the cameras right after the photo, in the server's order.

## Done when
- The tests pass, with the change above.
- New tests (`tests/test_clue_order.py`):
  - the five labels exist in both languages;
  - the page builds the list in this order;
  - Leonor is done from `followers`.
- A browser check: the start card and the phone list the five clues in this order.
