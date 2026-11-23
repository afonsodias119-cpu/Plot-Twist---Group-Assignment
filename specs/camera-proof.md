# The security recording is the fourth proof (phase 2 of the security desk)

Phase 2 of specs/security-desk.md, building on Afonso's desk (the guard José, the cables and the recordings). Changes the 3D server (`campus_case.py`, `campus_evidence.py`, `campus_game.py`, `campus_text.py`, `campus_people.py`), the page (`play.js`) and the text of "Case closed" in `story.py`. No change to `logic.py`, `db.py`, `game.py` or `app.py`. Every text exists in Portuguese and English.

## Before writing the spec

- **Product and user:** a player of the 3D game who has convinced José, plugged in the cables and found the hooded figure at computer 12 at 23:47.
- **Trigger:** "Keep this picture as proof" in the recordings; then the hearing.
- **Before:** the picture goes only to the diary, kept in the browser. The server knows nothing about it, so it is not a card and cannot be shown to the professor. Three proofs close the case (specs/three-proofs.md).
- **Rule (decided by the team):** the recording is needed to close the case. Duarte has a fourth claim, "I was not even here last night", and only the recording breaks it. The night keeps its 30 minutes.
- **After:**
  1. **The `footage` operation.** "Keep this picture as proof" sends `{"operation": "footage", "camera", "minute"}` (the camera on screen and the minute of last night, in minutes after midnight). The server checks that the player holds what convinces José (the original photo or the old files, as specs/security-desk.md says) and that the picture is the proof (`computer_lab`, 23:46 to 23:49, `FOOTAGE` in `campus_case.py`). Then it writes the night's note `footage: true`; anything else writes nothing and is refused with `footage_wrong` or `footage_unconvinced`. It is refused during the hearing, after the ending and after 22:45, and it costs nothing. The reply has `footage` (true or false). The page puts the picture in the diary only when the server says yes. A request sent while José talks only reports the time (he is not one of the server's people and never leaves).
  2. **The card.** `footage` is the last card of the hand, held through the note (read only when exactly `true`). Label: "The security recording: a hooded figure at computer 12 at 23:47" / "A gravação da câmara: uma figura de capuz no computador 12 às 23h47".
  3. **The fourth claim** (`here`, broken only by `footage`):
     - Duarte: "And who changed the folder at 23:47? Not me. I was not even here last night." / "E quem mudou a pasta às 23h47? Eu não. Nem cá estive ontem à noite."
     - Right: the professor recognises computer 12 at 23:47, the hood and the long coat, and the same coat at the entrance at 23:38: "You were here, Duarte." / "Esteve cá, Duarte."
     - Wrong: "That does not tell me who was in the building last night." / "Isso não me diz quem estava no edifício ontem à noite."
     The hearing card says "Claim n of 4". The doubts still stop at three; any claim without its proof gives "Stolen credit" with the line `missing`.
  4. **Texts.** The professor's `evidence` line also asks who was in the building last night. "Case closed" says "your proofs" instead of "the three proofs" (the plain game has no guard and still closes with three).

## Reviewed tests that change

To be approved by the team in the review of the pull request. Each change has a comment `Changed by specs/camera-proof.md ("Reviewed tests that change")`.

- `tests/test_security_desk.py` (Afonso): `test_the_guard_and_the_recordings_never_call_the_server` now allows exactly one request, `send("footage", ...)`, when the picture is kept. This is phase 2 as the spec described it.
- `tests/test_evidence_and_hearing.py`: four claims (`here` ← `footage`); the hand of every card includes the recording; saying nothing four times; the hearing ends after four answers (the `three answers` and `fourth time` tests become `four answers` and `fifth time`).
- `tests/test_earlier_nights.py`, `tests/test_your_own_group.py`: the nights that close the case keep the recording and give four answers; the third claim is one reply earlier.
- `tests/test_night_schedule.py`: the costs, the lost print shop and the caught player give four answers. The balance model gains the step `camera` (nine commands without a request, 25 seconds of hands, then `footage`). With the night still at 30 minutes, the balance limits move (measured): "Case closed" fits up to 52 seconds a command (no longer at 60, so the endings test checks 15, 30 and 45 and Stolen credit at 60); the careful first night fits with two minutes left up to 37 seconds (the test checks 33, 35, 37; was 43, 45, 47); the best night fits at 35 (was 45); "doing everything" is 30 commands; route 11 fits up to 27 seconds and no longer at 28.

## Done when

- [ ] Every test passes, and the `.cjs` checks.
- [ ] `tests/test_camera_proof.py`: the right picture is the last card (both languages); only computer 12 from 23:46 to 23:49; José must be convinced; bad requests raise; refused during the hearing, after the ending and at 22:45; a damaged note gives no card; the fourth claim; without the recording, no "Case closed"; with it, "Case closed"; the page asks the server before the diary.
- [ ] In the browser: convince José, plug in the cables, find 23:47 on the lab's camera, keep the picture; the card appears; the hearing has four claims and the fourth is broken by the recording.
