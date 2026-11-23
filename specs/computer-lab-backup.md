# The computer lab: save the backup of the original conversations (no chat puzzle, no fifth ending)

> **Update (specs/three-proofs.md):** the endings of point 3 are replaced. `accuse` and "The impostor" are gone; the proofs decide: the photo, the files and the backup → "Case closed", anything missing → "Stolen credit". The auditorium of point 2 is always open, and the true ending is removed.

Changes `story.py` (both games: the plain game of `app.py` and the 3D game) and the 3D server. Replaces specs/archive/spot-the-fake.md (the group chat puzzle) and removes specs/archive/fifth-element-ending.md. Every text exists in Portuguese and English.

## Before writing the spec

- **Product and user:** a player of either game who has opened the files on computer 12.
- **Trigger:** the computer lab, after the old files are seen.
- **Before:** computer 12 opens a group chat with five messages; the player flags the ones they think are fake. The flags decide the endings: flagging exactly 2, 4 and 5 with Leonor's help gives "Case closed", Leonor's help with any other flags gives "The impostor", and flagging every message gives the secret ending "The fifth element". The flagged messages are also cards for the hearing, and Duarte's rounds catch a player who is in the chat.
- **Rule:** the player saves the original conversations for the professor; nothing is flagged, and the chat is not an ending. Leonor's choice decides the story's ending.
- **After:**
  1. **Computer 12.** After the files, computer 12 offers "Save a backup of the original conversations" / "Guardar o backup das conversas originais" (story action `save_backup`, new flag `backup_saved`). It copies the group's conversations, as they were before last night, onto the USB stick. The lab then says the backup is saved, and the diary keeps the text. There is no group chat scene, no `open_chat`, no `flag_n` and no `flagged_n` flags.
  2. **The auditorium** needs the files **and** the backup (`go_auditorium` requires both flags). In 3D, the clue list is unchanged: the computer-12 clue is done once the files are seen; the backup is the extra step the door asks for.
  3. **The endings** are three, chosen by Leonor's choice, in both games:
     - she helps (`ask_for_help`) → **Case closed** (new text: the backup and her messages prove it);
     - she is accused (`accuse`) → **The impostor** (new text: the professor crosses the name out, but Leonor went home and Duarte says the group did his job for him; three of them present);
     - no choice (in 3D: the photo or Leonor was lost before it) → **Stolen credit** (new text: with no teammate there, Duarte says the backup could have been made by anyone).
     "The fifth element" no longer exists. The true ending of earlier nights (specs/earlier-nights.md) now opens once the **three** story endings were seen; the unknown number's dare says "Three endings, and still here."
  4. **The hearing (3D).** The five flagged-message cards are gone (and the professor's line for them). Tomás's claim line ("the chat says Duarte did them") is broken by `files`, the history of the slides; his reveal line says so. Two doubts on a "Case closed" night now show **Stolen credit** (the professor's line `two` is the same), because "The impostor" now means Leonor was accused. The professor's `no_originals` line says nobody from the group is there to confirm the backup.
  5. **Duarte's rounds (3D)** catch a player who is **at computer 12 with the files open and the backup not saved yet** (it was: in the chat). A catch only costs its 3 minutes and its doubt; nothing else is saved. His line says he closes the window: "Those conversations are not for you."
  6. **The page** loses the chat screen, the 🟨 square of the share card, the unknown number's message about the first flag, the fifth ending's colours, flickering lights and stamp. After the right code, computer 12's card offers the backup.

7. **The proofs for the professor (after the merge with #53–#56, agreed with the team).** The cards are the USB stick's history (`files`), the original photo and the **backup** (new card `backup`, held once `backup_saved`). Duarte's claims: `name` ← `files`, `photo` ← `original_photo`, `messages` ← `backup`. Leonor's screenshots and the words of Tomás and Rita are no longer cards: cracking Tomás or Rita is kept in the night's notes (Tomás still stands in the lab door, and the true ending still needs both), and Leonor is no longer cracked with a card. The security camera will be the fourth proof, with a fourth claim, added by Afonso (specs/security-desk.md, phase 2).
8. **No culprit cases.** The cases "tomas" and "rita" of specs/archive/culprit-of-the-night.md changed the fake chat messages; they are removed and the culprit is always Duarte. The case of the day keeps only the classic case, so the start screen and the share card still show the date. The friends' names of specs/your-own-group.md still work. The lies of specs/trust-has-consequences.md are now contradicted by the backup.

## What

- [ ] `story.py`: start flags (`backup_saved` instead of `flagged_1`…`flagged_5`); computer lab text and `save_backup`; `go_auditorium` requires `backup_saved`; no `group_chat` scene; three endings with new texts (EN and PT).
- [ ] `campus_game.py`: no chat view, chat notes or `flagged`; `at_computer_12(state)` for the rounds; the backup in the notebook.
- [ ] `campus_case.py` / `campus_evidence.py`: no `msg_n` cards; Tomás broken by `files`; the 2-doubt cap gives `stolen_credits`; texts.
- [ ] `campus_people.py`: `save_backup` is done at computer 12; Rita's note and Tomás's `help` line no longer point to the chat.
- [ ] `campus_text.py`: rules, catch line, dare, voices and stamps; no chat texts.
- [ ] `play.js`, `play.css`, `game3d.html`: no chat screen, no fifth ending; computer 12 offers the backup after the code.
- [ ] `docs/guiao-conversas.md`, `docs/plano-do-projeto.md`.

## Reviewed tests that change

Approved by the team (the decision to remove the chat and the fifth ending was taken with them).

- `tests/test_fifth_element_ending.py`: **deleted** (it tested only the removed ending).
- `tests/test_base_game.py`: the paths save the backup; Leonor's choice decides the ending (help → full_case, accuse → impostor, none → stolen_credits); the reachable endings are three; the group chat tests are replaced by tests of the backup; an old save with the chat flags is no longer valid.
- `tests/test_smoke.py`, `tests/test_images.py`: the short path saves the backup.
- `tests/test_campus_3d.py`: the paths save the backup; the endings follow Leonor's choice; the chat test becomes the backup test.
- `tests/test_campus_people.py`: the chat tests become backup tests (diary, walking, who offers it, no chat in the snapshot or the page).
- `tests/test_evidence_and_hearing.py`: no message cards; Tomás is cracked with `files`; the hearing cases follow Leonor's choice (`leonor=None` lets her leave at 22:30 for "Stolen credit"); two doubts on "Case closed" show "Stolen credit".
- `tests/test_earlier_nights.py`: three story endings; the dare and the night numbers follow; a catch happens at computer 12 before the backup.
- `tests/test_night_schedule.py`: the balance model's "chat 5 2 4" step becomes "backup" (and the careful player waits before the code, not before the chat); the routes lose the chat and the fifth ending; the catch tests happen at computer 12 before the backup; "doing everything" lost 7 commands (26 → 20): the estimate still does not fit at 30 seconds, and route 11 now fits up to 31 seconds a command and no longer at 32.

- After the merge with #53–#56: `tests/test_culprit_of_the_night.py` **deleted** (only the removed cases); `tests/test_evidence_and_hearing.py` (the three cards, the facts are notes, Leonor is not cracked, the backup answers `messages`), `tests/test_earlier_nights.py` and `tests/test_night_schedule.py` (the hearings answer with the backup; "doing everything" is 19 commands, route 11 now fits up to 32 seconds a command and no longer at 33), `tests/test_more_to_find.py`, `tests/test_trust_has_consequences.py` (the backup contradicts the lies; Leonor's half of `test_cracking_forgives` is gone) and `tests/test_your_own_group.py` (no chat, no cases).

## Done when

- [ ] Every test passes (520 after the merge with #53–#56).
- [ ] In the browser: computer 12 asks for the code, then offers the backup; the backup text appears and goes to the diary; there is no chat screen.
