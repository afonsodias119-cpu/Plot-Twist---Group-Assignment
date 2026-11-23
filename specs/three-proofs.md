# Three proofs decide the ending: no accusing Leonor, no true ending

Changes `story.py` (both games: the plain game of `app.py` and the 3D game) and the 3D server and page. Replaces the endings of specs/computer-lab-backup.md (point 3) and removes the true ending of specs/earlier-nights.md (points 8 and 9 and the dare of point 4). Every text exists in Portuguese and English.

## Before writing the spec

- **Product and user:** a player of either game who reaches the professor.
- **Trigger:** the hearing in the auditorium (3D) or "Present the evidence" (plain game).
- **Before:** Leonor's choice decides the ending: she helps → "Case closed", she is accused → "The impostor", no choice → "Stolen credit". The auditorium opens only when every clue on the phone is done or lost (Leonor is one of them). After seeing the three story endings, a perfect night gives a secret fourth one ("22:46", the true ending), and the unknown number dares the player.
- **Rule:** there are only three ways for a night to end:
  1. the player reaches the professor with **all three proofs** (the USB stick's history, the original photo, the backup of the conversations) and answers every claim of Duarte → **Case closed**;
  2. the player reaches the professor with a proof missing (or answers a claim wrongly) → **Stolen credit**;
  3. the clock reaches 22:45 → the faculty closes (unchanged).
  Accusing Leonor no longer applies. Leonor stays in the game, because she helps at computer 12 (her memory of the Finance test, specs/calendar-code.md), but she is not a clue of the phone.
- **After:**
  1. **Leonor** has one decision, "Ask for help" (`ask_for_help`). The `accuse` action is gone from both languages, with its texts, its cost and its 3D person. She still leaves at 22:30 if she is not helping, and the unknown number still warns about it, but her leaving loses no clue.
  2. **The auditorium is always open** (`go_auditorium` has no `requires`). In 3D, the phone's clue list has three rows (USB stick, original photo, old files); the map no longer draws a lock and the door has no "missing clues" note.
  3. **The story's endings** are two:
     - `full_case` when the original photo is held, the files were seen and the backup is saved (new text: the three proofs on the professor's desk);
     - `stolen_credits` otherwise (new text: not every proof the professor needs; "I cannot cross out a name on a hunch").
  4. **The hearing (3D)** keeps its three claims (`name` ← `files`, `photo` ← `original_photo`, `messages` ← `backup`). If every answer is right the story's ending is shown; if any answer is wrong or "Say nothing", the ending is **Stolen credit** with the professor's line `missing` ("one of his claims has no proof against it, and I write down only what I am sure of"). A catch by Duarte still costs its 3 minutes and opens the hearing with the professor's doubt, but it no longer changes the ending by itself.
  5. **No true ending.** `night_over`, its text, its stamp, its voices and the dare are gone. The snapshot's `memory` is only `{"night", "seen"}`. The fifth figure still grows on the case-file photo night after night; the "four people" picture and the line "No more nights" are gone, and so is the ★ in the collection count.
  6. **The page** loses the impostor's emoji, confetti, colours and stamp, and the notice "I know you suspect her" (three notices are left).

## What

- [ ] `story.py`: no `accuse`; `go_auditorium` always open; two endings with new texts (EN and PT).
- [ ] `campus_game.py`: three `CLUES`; no `missing_clues_note`; `leonor_present`; the notebook.
- [ ] `campus_evidence.py`: `verdict_of` gives `("stolen_credits", "missing")` for any wrong answer; no `perfect_night` or true ending.
- [ ] `campus_case.py`: no `TRUE_ENDING`; the verdict line `missing`; `NIGHT_TEXT` without the dare.
- [ ] `campus_memory.py`: `memory_view` without `open` and `over`; whispers without the dare.
- [ ] `campus_people.py`, `campus_clock.py`: no `accuse`.
- [ ] `campus_text.py`: no impostor stamp or voices, three notices, no `night_done`, no `map_locked`, no auditorium note.
- [ ] `play.js`, `game3d.html`, `play.css`: no impostor, no "night over", no lock on the map.
- [ ] `docs/guiao-conversas.md`, `docs/plano-do-projeto.md`.

## Reviewed tests that change

To be approved by the team in the review of the pull request (they change what the game is). Each change has a comment `Changed by specs/three-proofs.md ("Reviewed tests that change")` in the test.

- `tests/test_base_game.py`: the paths no longer accuse; a path without the backup ends in `stolen_credits`; the auditorium always opens; the reachable endings are two.
- `tests/test_smoke.py`: the blocked click is now `ask_for_help` outside the library (the auditorium is never blocked).
- `tests/test_campus_3d.py`, `tests/test_campus_people.py` (Leonor stays after helping; the clock; after the merge with specs/night-and-clues.md, `test_phone_texts_exist_in_both_languages` has no label for Leonor), `tests/test_actions_when_they_make_sense.py`, `tests/test_harder_campus.py`, `tests/test_trust_has_consequences.py`: no `accuse`.
- `tests/test_evidence_and_hearing.py`: the verdict line `missing` in both languages; any wrong answer gives Stolen credit; a catch costs time but not the ending; the damaged-notes and no-photo tests use a night without the photo.
- `tests/test_earlier_nights.py`: two story endings; `memory` without `open` and `over`; no dare; the eight tests of the true ending are **deleted** and replaced by `test_there_is_no_true_ending_any_more`; three notices; no `night_done`.
- `tests/test_night_schedule.py`: no `accuse` cost or decision; Leonor is not a clue row and her leaving is not `lost`; the auditorium opens without any proof (the old "still needs the old files" and "lost photo locks" tests are rewritten); route 1 gets the code but not the backup (Stolen credit); the endings test asks for two endings; the verdict `missing`; three notices and no `map_locked`; the door note is gone.
- After the merge with specs/night-and-clues.md: `tests/test_night_and_clues.py` (Afonso): no "accuse" among the wrong choices, and the clues are three (no Leonor). `tests/test_night_schedule.py`: the charge test uses a wrong card instead of accusing; a night that says nothing still saves "full_case" as the story's own ending; the balance limits are measured again.
- `tests/test_your_own_group.py`: the impostor night becomes a night without the backup; the true night is gone; the endings name nobody of the group.

## Done when

- [ ] Every test passes, and `node tests/continuous-conversations.cjs`.
- [ ] In the browser: Leonor offers only "Ask for help"; the auditorium opens at any time; all three proofs and right answers give "Case closed"; a night without the backup gives "Stolen credit" with the professor's `missing` line; 22:45 still closes the faculty.
