# Tests

The tests are the acceptance checks of the game: **588 tests** in 54 files, all passing on `main`. Each one was written from a spec in [`specs/`](../specs/), before the code.
GitHub runs them on every push and pull request ([`.github/workflows/tests.yml`](../.github/workflows/tests.yml)); the badge at the top of the main README shows the result for `main`.

## How to run them

```sh
uv run pytest                              # every Python test
uv run pytest tests/test_base_game.py      # one file
uv run pytest -k hearing                   # only the tests whose name contains "hearing"
node tests/continuous-conversations.cjs    # the JavaScript checks of the page (needs Node)
node tests/tomas-password-end.cjs
```

The tests never touch your saved games: [`conftest.py`](conftest.py) points the database at a throwaway file for each test.

## How the folder is organised

- **One file per spec, with the same name.** `specs/guard-explain-first.md` is tested by `tests/test_guard_explain_first.py`.
  The first line of almost every file names its spec (`test_campus_3d.py` is the exception: its specs are playable-campus-3d and campus-3d-streamlit). The few files with a different name are marked in the tables below.
- **Some specs are tested inside another spec's file**, because they change that feature: see [Specs tested in another file](#specs-tested-in-another-file).
- **Inside a file, one test per check of the spec**, in the order the spec lists them.
- **When a later spec changes an older test, the test says so** in a comment: `# Changed by specs/<spec>.md ("Reviewed tests that change")`, followed by what it was before.
  A reviewed test is never deleted or weakened to make it pass. A few test names are older than the spec that changed them; the comment inside explains what changed.

## Kinds of checks

| Kind | How it works | Example |
|---|---|---|
| Rules | Calls `logic.py` directly and checks the new state | `test_base_game.py` |
| Server commands | Sends the same requests as the 3D page to `campus_game.command` and checks the reply. For a refused request, it checks that the database file has the same bytes before and after | `test_evidence_and_hearing.py` |
| Screens of the plain game | Opens `app.py` with Streamlit's `AppTest` and clicks buttons like a player | `test_smoke.py` |
| Page checks | Reads `play.js`, `game3d.html` or the built page and checks that the code a feature needs is there, and that no answer or secret is in it | `test_pen_and_code.py` |
| JavaScript in Node | Runs part of `play.js` in Node with a fake page | `continuous-conversations.cjs` |

## What each file covers

### The base game (the course brief)

| File | What it checks | Spec |
|---|---|---|
| `test_base_game.py` | Scenes, items, locked actions, both endings reachable, saving and resuming, invalid names, both languages | base-game |
| `test_smoke.py` | The screens of the plain game (`app.py`): start, language, errors, new game confirmation, ending | base-game, section 7 *(different name)* |
| `test_images.py` | The scene pictures, a game without pictures, the dark theme | scene-images *(different name)* |

### Security and the project itself

| File | What it checks | Spec |
|---|---|---|
| `test_name_belongs_to_browser.py` | A name belongs to the browser that started it; only a hash of its key is stored; someone else's key is refused before anything changes | name-belongs-to-browser |
| `test_name_check_first_step.py` | The page checks the name with the same rule as the server | name-check-first-step |
| `test_safe_dependencies.py` | Libraries pinned and minimal; Three.js and the QR library have integrity hashes | safe-dependencies |
| `test_warm_start.py` | The warm-up request writes nothing and never reaches the game | warm-start |
| `test_code_refresh.py` | After a deploy, the app loads the new code instead of old code in memory | fresh-code-after-deploy *(different name)* |
| `test_tests_on_github.py` | The GitHub workflow exists, runs on every push, can only read the repository | tests-on-github |

### The 3D game: server, page and interface

| File | What it checks | Spec |
|---|---|---|
| `test_campus_3d.py` | The 3D server uses the original rules: doors, resume, bad requests, the HTTP server, the app inside Streamlit | playable-campus-3d, campus-3d-streamlit *(different name)* |
| `test_campus_people.py` | People in each room, conversations without dead ends, who offers each action | campus-people-and-atmosphere *(different name)* |
| `test_chat_dialogues.py` | Conversations as speech bubbles and narration, room plaques | chat-dialogues |
| `test_cleaner_interface.py` | The menu, no emojis in the top bar, no hearts in conversations | cleaner-interface |
| `test_creator_after_name.py` | The detective step after the name, the case file, the closing warning | creator-after-name |
| `test_rules_and_character.py` | The menu (Rules, Torch, Sound), the character creator, browser values checked before use | rules-and-character |
| `test_touch_card_qr.py` | Phone joystick, the detective card and the QR code | touch-card-qr |
| `test_flashlight_voices_howto.py` | The torch, the voices and the "How it was made" window | flashlight-voices-howto |
| `test_sounds_that_tell.py` | Footsteps, the shutter and message sounds | sounds-that-tell |
| `test_no_endings_on_start.py` | No count of endings on the start or ending screen | no-endings-on-start, no-endings-count |
| `test_your_own_group.py` | The player's own teammates' names in the story; bad names fall back safely | your-own-group |

### Puzzles and clues

| File | What it checks | Spec |
|---|---|---|
| `test_pen_and_code.py` | The hidden USB stick and the code of computer 12; the answers never reach the page | pen-and-code |
| `test_hidden_object_table.py` | The USB stick hidden among the objects of the study room table; a refused door does not move the character | hidden-object-table, auditorium-door-keeps-room |
| `test_study_room_detail.py` | The study room furniture | study-room-detail |
| `test_table_hint_and_guard_check.py` | The note near the table; José asks before showing the recordings | table-hint-and-guard-check |
| `test_torn_photo.py` | The torn photo puzzle of the print shop; the solution is not in the page | torn-photo |
| `test_calendar_code.py` | The code of computer 12 from the group's memories and the phone apps; a wrong code costs time | calendar-code |
| `test_more_to_find.py` | Things to look at in the rooms, and two red herrings | more-to-find |
| `test_library.py` | The library as a study hall; Leonor comes with you | library-study-hall *(different name)* |
| `test_clue_order.py` | The order of the clues | clue-order |
| `test_camera_clue.py` | The security cameras in the list of clues; the clues say what to find, not where | camera-clue, clues-without-answers |
| `test_night_and_clues.py` | The night from 22:30 to 23:00; only wrong choices cost time | night-and-clues |

### People and conversations

| File | What it checks | Spec |
|---|---|---|
| `test_two_answers.py` | Tomás and Rita: one right and one wrong answer per line; "Show evidence" with José only when he asks | two-answers, evidence-after-monitors |
| `test_leonor_two_answers.py` | Leonor: one right and one wrong answer | leonor-two-answers |
| `test_leonor_after_help.py` | Leonor after she agrees to help | leonor-after-help |
| `test_actions_when_they_make_sense.py` | Leonor's decision and the clerk's copy appear only when they make sense | actions-when-they-make-sense |
| `test_trust_has_consequences.py` | People you were rude to answer less, warn others or lie | trust-has-consequences |
| `test_guard_explain_first.py` | José first hears why you came | guard-explain-first |
| `test_guard_answer_and_cameras.py` | José's question about the camera, a camera in every room | guard-answer-and-cameras |
| `test_security_desk.py` | The security desk, the cables and the recordings | security-desk |
| `test_professor_before_podium.py` | The professor, not the podium, is reached first | professor-before-podium |
| `test_professor_line_of_thought.py` | The professor's line of thought; what to do when Duarte speaks | professor-line-of-thought |
| `test_duarte_only_in_the_hearing.py` | Duarte only speaks in the hearing | duarte-only-in-the-hearing |

### The clock, the proofs, the hearing and the endings

| File | What it checks | Spec |
|---|---|---|
| `test_night_schedule.py` | The campus clock, what costs time, people who leave, Duarte's rounds, the faculty closing at 23:00 | night-schedule |
| `test_harder_campus.py` | No list of missing clues; the countdown | harder-campus |
| `test_evidence_and_hearing.py` | Evidence cards, confrontations and the hearing; refused requests save nothing | evidence-and-hearing |
| `test_hearing_show_evidence.py` | Answering a claim with "Show evidence" or "Say nothing" | hearing-show-evidence |
| `test_hand_over_the_proofs.py` | Ticking the proofs to hand over; a missing proof is a warning that says how many, never which | hand-over-the-proofs, select-the-proofs, missing-proof-is-a-warning |
| `test_camera_proof.py` | The security recording as the fourth proof | camera-proof |
| `test_earlier_nights.py` | A new night with the same name: the night count, the messages and the memory answers | earlier-nights |
| `test_case_of_the_day.py` | The case is chosen by the date (Lisbon time). Only one case is left, so every day plays the same case | case-of-the-day |

### JavaScript checks

| File | What it checks | Spec |
|---|---|---|
| `continuous-conversations.cjs` | A conversation stays open after each answer, so the player can change subject without closing it (run on GitHub) | continuous-conversations |
| `tomas-password-end.cjs` | Tomás ends the exchange after explaining the password of computer 12 (run by hand, not yet on GitHub) | tomas-password-end |

## Specs tested in another file

| Spec | Where its tests are |
|---|---|
| select-the-proofs, missing-proof-is-a-warning | `test_hand_over_the_proofs.py` |
| no-endings-count | `test_no_endings_on_start.py` |
| evidence-after-monitors | `test_two_answers.py` |
| clues-without-answers | `test_camera_clue.py` |
| auditorium-door-keeps-room | `test_hidden_object_table.py` |
| fresh-code-after-deploy | `test_code_refresh.py` |
| library-study-hall | `test_library.py` |
| scene-images | `test_images.py` |
| playable-campus-3d, campus-3d-streamlit | `test_campus_3d.py` |
| combined-start-briefing | the tests it changed (`test_creator_after_name.py`, `test_night_and_clues.py` and others), each with a comment |
| three-proofs, computer-lab-backup | they changed the rules of the whole game, so their changes are in many files, each marked `# Changed by specs/<spec>.md` |

## What the tests do not cover

- How the 3D scene looks and feels, the sounds, and the touch controls. The team checks these by playing in the browser, on a computer and at phone size, in both languages, before each merge.
- The page checks confirm that the code is in `play.js`, not that it behaves correctly in a browser. The behaviour of the rules is tested on the server, where every decision is made.
