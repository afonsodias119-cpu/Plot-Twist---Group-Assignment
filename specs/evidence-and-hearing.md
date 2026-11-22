# Evidence and the hearing: show people what you found, and answer Duarte's three claims

Extends specs/campus-people-and-atmosphere.md, specs/chat-dialogues.md, specs/harder-campus.md and specs/pen-and-code.md. No change to `story.py`, `logic.py`, `game.py`, `app.py` or any reviewed test: no new flag, action or ending, so every saved game stays valid and the plain game plays as before. `db.py` gains one table and three small functions. The existing operations keep their exact fields, and `talk` still writes nothing.

## Why
The player collects proof and never uses it. Nobody can be shown the photo or a flagged message, and the whole case ends with one click on "Present the evidence": the game cannot tell a player who understood the lie from one who walked through the rooms. Evidence should be something you put in front of a person, and the auditorium should be the place where Duarte fights back.

## What
1. **A night's notes, kept by the server.** `db.init_db` also creates the table `nights` (`player TEXT PRIMARY KEY`, `minute INTEGER NOT NULL`, `notes TEXT NOT NULL`, a JSON object), beside `games` and in the same call, so no read ever creates a table (reviewed tests compare the database file byte for byte). New in `db.py`: `load_night(player)` (returns `{"minute": 0, "notes": {}}` when there is no row or it cannot be read; it never writes), `save_night(player, minute, notes)` and `delete_night(player)`. Example row: `("ana", 0, '{"cracked": ["tomas"], "hearing": ["files", "concede"], "verdict": ""}')`. `minute` stays 0 in this feature (specs/night-schedule.md uses it). A confirmed `restart`, and an `open` that starts a new game, delete the row. The save itself cannot hold these notes: a save must have exactly the story's flags (`logic.py:138`) and a restart replaces it (`game.py:89`).
2. **What is read is cleaned.** `campus_evidence.read_night(player, state)` keeps only what it understands: `cracked` is a list of people who have a confrontation (others are dropped); `hearing` is absent or a list of at most three answers, each `"concede"` or a card id, and only while the saved scene is the auditorium or the game has ended; `verdict` is kept only when the game has ended and the caps of point 10 could have produced it. Anything else counts as empty. A damaged row can neither raise an error nor help the player. Cleaning happens in memory; nothing is written until the next operation that saves.
3. **The case file, on the server only.** New module `campus_case.py` (data only, like `campus_search.py`; never imported by `page3d.py`): `EVIDENCE` (card id and the story condition that holds it, checked with `logic._condition_met`), `FACTS`, `CONFRONT`, `HEARING` and `CASE_TEXT` (labels, reveals, rebuffs, claims, the professor's lines and the verdict lines, in `en` and `pt` with the same keys). Short example:
   ```python
   EVIDENCE = {"original_photo": {"has": ["original_photo"]}, "files": {"flags": {"files_viewed": True}},
               "leonor_messages": {"flags": {"colleague_choice": "help"}}, "msg_5": {"flags": {"flagged_5": True}}}   # and msg_1 to msg_4
   FACTS = {"tomas": "tomas_word", "rita": "rita_word"}
   CONFRONT = {"tomas": {"node": "slides", "breaks": ["msg_5"]}, "rita": {"node": "five", "breaks": ["files", "original_photo"]},
               "leonor": {"node": "sure", "breaks": ["tomas_word"]}}
   HEARING = [{"id": "name", "accepts": ["files"]}, {"id": "photo", "accepts": ["original_photo", "rita_word"]},
              {"id": "messages", "accepts": ["leonor_messages", "tomas_word"]}]
   ```
   New module `campus_evidence.py` holds the rules that read it (`read_night`, `held`, `confront`, `hearing`, `hearing_view`, `shown_ending`).
4. **Evidence cards.** The server decides what the player holds, from the save plus the night's notes, and every snapshot carries it as `evidence`: a list of `{"id", "label"}` with only the cards held now, in this order. Ten ids: `original_photo` (the item), `files` (`files_viewed`), `leonor_messages` (while `colleague_choice` is `help`), `msg_1` to `msg_5` (each flagged chat message; the label is `🚩` and the story's own text of that message) and the two facts won by cracking people, `tomas_word` and `rita_word`. The diary lines stay hints: the server never sees them.
5. **"📁 Show evidence" in every conversation with a person.** Not at computer 12 and not during the hearing. The button (`evidence_show`) is on every line of every person, lie or not, so the player has to notice the lie. It replaces the answers with the cards held (the technique of the code field, `askCode`); choosing one adds a bubble on the right and sends `confront` with the line on the screen. It is drawn inside the conversation card, so the text mode has it too.
6. **New operation `confront`** with exactly `operation`, `player`, `language`, `npc`, `node`, `evidence`.
   - Refused with `ValueError`, nothing written: `npc` is not a text, is unknown or is computer 12; `node` is unknown or is a line `talk` would not give now (not reachable yet, or a claim already broken); the person is not in the saved room; the game has ended; `evidence` is not a text or not one of the ten ids; a card the player does not hold; a hearing is open; missing or extra fields.
   - The right card on the claim line of a person not yet cracked: the person is added to `cracked` (the only write), and their fact, if they have one, is a card from now on.
   - Any other card, or any other line: nothing changes.
   - Reply: the snapshot plus `"confront": {"npc", "name", "cracked", "text", "trust", "note", "minutes"}`. `text` is the reveal or the rebuff; `note` is a diary line (empty for a rebuff); `minutes` is 0 for the right card, 2 for a rebuff and 1 for any card shown to Duarte. In this feature the page takes `minutes` off its countdown exactly as it does for a rude answer (`penalize`); specs/night-schedule.md moves the charge to the server. The reply never says which card would have been right.
7. **Three confrontations** (every line is in the dialogue script; the specs name them by id).
   - Tomás, line `slides` (new, from `kind`: "Ask who made the slides"): "the chat says Duarte did them, under my name. So maybe he did, and I only tidied up." Broken only by `msg_5`, the flagged message with his name. He reads its arrival line: "At 11:49 I was sitting right here, two computers away from the one in the hood. I did not type a word." Gives `tomas_word`.
   - Rita, line `five` (new, from `photo`: "Ask why the photo in the folder shows five"): "Then I counted wrong. A photo cannot change. My memory can." Broken by `files` or `original_photo`. Gives `rita_word`.
   - Leonor, her existing line `sure`, broken by `tomas_word`: trust 3 and a diary line, no fact. It is optional; her two story decisions are unchanged.
   - Once a claim is broken the answer that leads to its line is not offered again, and the line cannot be asked for.
   - Everybody else has one rebuff line; Duarte has one line for any card ("Keep it for the professor.").
   - Each teammate vouches only for their own chat message: Tomás for the one with his name, Rita for "four of us, finally", Leonor (new line `mine`, offered only once she is helping) for the one about the study room. Nobody lists the fake messages.
8. **Dialogue changes in `campus_people.py`**, both languages, same ids and conditions: new lines `slides` (Tomás), `five` (Rita), `mine` (Leonor) and the three answers that lead to them; Tomás's existing line `msg5` is reworded (it is under his name and he does not remember writing it) so that it never contradicts `slides`. Its id, condition, trust and note stay. No new answer has a `cost`. Tomás's `kind` and Rita's `start` can now show four answers.
9. **The hearing replaces the one-click presentation.** On the 3D page the professor's "▶ Present the evidence to the professor" (with the hint `hearing_hint`) starts the hearing instead of playing `present_evidence`; the page hides the story button with one line beside the `open_drawer` one (`play.js:604`), and the server still offers and accepts it. The hearing is played inside the professor's conversation card: the server sends the log as entries with `who`, so each bubble has the right name and voice, and the doubt is the existing hearts (three minus the doubts). The answers are the cards held and "Say nothing". There is no new overlay: the card is the same in the text mode. If the card is closed or the page is reloaded, talking to the professor again shows the hearing where it stopped.
10. **New operation `hearing`** with exactly `operation`, `player`, `language`, `answer`; `answer` is `"start"`, `"concede"` or a card id.
    - `ValueError`, nothing written: `answer` is not a text, is not one of those, or is a card the player does not hold; missing or extra fields.
    - Refused with `accepted: false`, nothing written: the saved scene is not the auditorium; the game has ended (so a fourth answer is refused); `"start"` when the hearing has started; an answer before `"start"`.
    - Duarte makes three claims, in this order: `name` (broken by `files`), `photo` (he is "the one on the right, next to the window"; broken by `original_photo` or `rita_word`) and `messages` (broken by `leonor_messages` or `tomas_word`). A flagged message alone does not break `messages`, and the professor says why: "You flagged it. That is your opinion of it."
    - One answer per claim, no retry. A card that does not break the claim is a doubt; `"concede"` is always a doubt.
    - Each accepted answer is saved in the notes (`hearing`), so closing the card or reloading cannot give a heart back.
    - After the third answer the server itself plays the story's `present_evidence`, so the saved ending is still "the first ending whose condition is true". Then the verdict caps what is shown: three doubts show `stolen_credits` whatever the story's ending was; two doubts show `impostor` when the story's ending is `full_case`; otherwise the story's ending is shown. The shown id is saved as `verdict`.
    - Reply: the snapshot plus `"heard"` (true when the answer was saved). While a hearing is open the snapshot has `"hearing": {"step": 2, "doubts": 1, "said": [{"who": "duarte", "name": "Duarte", "text": "..."}, {"who": "you", "name": "", "text": "📁 ..."}, {"who": "professor", "name": "Professor", "text": "..."}]}`, rebuilt from the saved answers; otherwise `"hearing": None`.
11. **The ending that is shown.** The snapshot's `ending` is the verdict's ending (id, title and text of that story ending) with one more field, `verdict`: a line of the professor shown above the text when a cap applied (three doubts; three doubts with Leonor helping: "The professor closes the list before Leonor reaches the door."; two doubts on a full case), or when `stolen_credits` follows a broken `messages` claim; empty otherwise. The row in `games` keeps the story's own ending. The collection of endings and the share card use the shown ending.
12. **Nothing else during the hearing.** From `"start"` until the ending, `play`, `enter`, `search` and `unlock` are refused with `hearing_locked` ("You cannot walk out in the middle of your own case.") and `talk` and `confront` raise it; `open`, `restart` and `hearing` work.
13. **Files.** `app_3d.py`: `CODE_MODULES` becomes `story`, `logic`, `db`, `game`, `campus_text`, `campus_people`, `campus_search`, `campus_case`, `campus_evidence`, `campus_game`, `page3d` (a module after the ones it imports from); neither new module goes in `PAGE_FILES`. `campus_game.py`: the two operations in `allowed_fields` (`campus_game.py:231`), `evidence` and `hearing` in the snapshot, the answers to broken claims taken out of a `talk` reply (reading the notes writes nothing), the row wiped on restart. `play.js` and `play.css`: the tray, the hearing, the verdict line on the ending card; new lines beside the pinned ones, none of them edited. New texts in `campus_text.py`, both languages. `docs/guiao-conversas.md` and the status table of `docs/plano-do-projeto.md` are updated in the same pull request.

## Reviewed tests that change
None. The old operations keep their exact field sets; `talk`, refused actions, wrong places and wrong codes still write nothing; the new table is created together with `games`; no option gets a `cost`; `msg5` keeps its id, condition, trust and note; the professor still offers exactly `present_evidence`; a direct `present_evidence` still gives the story's ending and text.

## Limits
- The hearing and the tray are puzzles, not security. The server keeps accepting `present_evidence`, `open_drawer` and `view_files` played directly, because reviewed tests play them: a hand-made request can skip the hearing before it starts. That path gives the story's own ending, never a cap.
- In this feature the minutes of a rebuff are taken in the browser, like the rude answers: a hand-made request can show cards without losing time. It still cannot show a card the player does not hold, and no reply says which card is right.
- The shown ending can differ from the ending saved in `games` (the caps). The story decides the best the player earned; the hearing can only lose it. The plain game is not affected.
- The notes live in the same database file as the saves, so the public host forgets both when it restarts. A name is not a password: whoever types it continues that night.
- Tomás's promise to stand in the door has no effect until specs/night-schedule.md.
- The page code is checked only by needles in its source; the tray and the hearing need the browser check, in 3D and in text mode.

## Out of scope
The clerk's reprint slip, any new story flag, action or ending, a card or overlay of its own for the hearing, lights or camera for the hearing in 3D, answering a claim twice, a server clock (specs/night-schedule.md), memory of earlier nights and a fifth ending (specs/earlier-nights.md), the plain game.

## Done when
- Existing tests pass unchanged.
- The tests below were written first and pass.
- A browser check, in 3D and in text mode and in both languages, shows a rebuff, Tomás cracking, the hearing with a doubt, a reload in the middle of it, and a capped ending with its verdict line.

## Checks
`tests/test_evidence_and_hearing.py`, written before the code. `PAGE` is `page3d.build_page(playable=True, inline=True)`; "saves nothing" means the database file has the same bytes before and after.

The table and the notes
- `test_the_database_has_a_nights_table_beside_games`: `init_db` twice makes both tables; a file that only had `games` gets `nights` and keeps its rows.
- `test_reading_a_night_that_was_never_saved_gives_an_empty_one_and_saves_nothing`: `db.load_night` of an unknown name is minute 0 and `{}`.
- `test_a_damaged_notes_row_counts_as_empty_and_cannot_help`: rows written by hand with notes `not json`, `[]`, `{"cracked": ["duarte", 7], "hearing": "x", "verdict": "full_case"}`: `open` raises nothing, `evidence` has no fact, `hearing` is `None`, and an ended game still shows the story's ending.
- `test_a_restart_and_a_new_game_wipe_the_night`: after cracking Tomás, a confirmed restart leaves no row and no `tomas_word`; an unconfirmed one changes nothing.

The cards
- `test_the_hand_lists_only_what_the_player_holds`: empty at the start; each of the ten ids appears exactly when its condition becomes true, in the order of point 4; a flagged message's label ends with the story's text.
- `test_card_labels_follow_the_saved_language`: a game saved in `pt` gets the Portuguese labels whatever language the request names.
- `test_no_card_shows_a_clue_before_it_is_found`: the snapshot of a new game contains no label of `campus_case` and not `23h47`.

Confronting
- `test_the_right_card_on_the_claim_line_cracks_tomas_and_it_is_saved`: `msg_5` at `slides` gives `cracked` true, the reveal text, a note, trust 3, minutes 0; `tomas_word` is in `evidence` and still there after `open`.
- `test_rita_cracks_with_the_file_history_or_with_the_original_photo`: both cards, each in its own game, give `rita_word`.
- `test_leonor_doubts_only_when_shown_what_tomas_said`: `tomas_word` at `sure` gives `cracked` true, trust 3, a note and no new card; `original_photo` at `sure` gives her rebuff.
- `test_a_broken_claim_is_not_offered_again`: `kind` no longer offers `slides`; `talk` to `slides` and a second `confront` there raise `ValueError` and save nothing.
- `test_any_other_card_gets_the_rebuff_and_costs_two_minutes`: `files` at `slides` gives `cracked` false, Tomás's rebuff, an empty note, minutes 2, and no fact.
- `test_the_right_card_on_another_line_does_not_crack`: `msg_5` at `start`, `kind` and `msg5` gives the rebuff and minutes 2.
- `test_duarte_answers_any_card_with_one_line_for_one_minute`: every card held, on `start` and on `part`.
- `test_the_clerk_and_the_professor_only_rebuff`: minutes 2 and never cracked.
- `test_a_card_the_player_does_not_hold_is_rejected_and_saves_nothing`: `msg_5` before it is flagged, `tomas_word` before Tomás cracks.
- `test_unknown_person_card_and_line_are_rejected_and_save_nothing`: `npc` `"nobody"`, `"computer12"` and `7`; `evidence` `"knife"` and `["msg_5"]`; `node` `"nope"` and a line not reachable yet.
- `test_confront_needs_the_person_in_the_saved_room_no_ending_and_exact_fields`: Tomás from the study room, anyone after an ending, a missing and an extra field.
- `test_the_reply_never_says_which_card_is_right`: after a rebuff the reply contains no reveal text, and the only card ids in it are the ones in `evidence`.

The dialogue
- `test_the_new_lines_have_the_same_shape_in_both_languages`: `slides`, `five` and `mine` exist in `en` and `pt`; every `node` of `CONFRONT` is a line of that person; no new answer has a `cost`.
- `test_tomas_never_says_he_did_not_write_it_before_he_is_shown_the_proof`: `msg5` keeps its id, trust 3, note and `files_viewed` condition, and its text has neither "never wrote" nor "nunca escrevi".
- `test_leonor_says_which_message_is_hers_only_after_helping`: `mine` is offered and can be asked for only when `colleague_choice` is `help`.
- `test_nobody_lists_the_fake_messages`: no text of `CASE_TEXT` and no new line contains "message 2", "message 4", "mensagem 2" or "mensagem 4".
- `test_every_quote_of_the_case_file_is_a_spoken_line_in_both_languages`: with the rule of `partsOf` (more than three words, or `.`, `!`, `?`, `…`), every reveal, rebuff, claim, professor line and verdict line has the same number of spoken quotes in `en` and `pt`, and `CASE_TEXT["en"]` and `CASE_TEXT["pt"]` have the same keys.

The hearing
- `test_the_hearing_starts_only_in_the_auditorium_and_only_once`: `"start"` from the study room is not accepted and saves nothing; in the auditorium it gives step 1, 0 doubts and Duarte's first claim; a second `"start"` is not accepted.
- `test_an_answer_before_the_hearing_starts_is_refused_and_saves_nothing`.
- `test_each_claim_accepts_only_its_own_cards`: for the three claims, every card of `accepts` leaves the doubts unchanged and every other card held adds one.
- `test_a_flagged_message_alone_does_not_break_the_messages_claim`: `msg_5` on claim 3 is a doubt and the last line said is the one about an opinion, in both languages.
- `test_saying_nothing_is_always_a_doubt`.
- `test_one_answer_per_claim_and_no_retry`: after a wrong answer the step is the next claim.
- `test_a_reload_in_the_middle_keeps_the_step_the_doubts_and_the_log`: `open` after one wrong answer returns the same `hearing`.
- `test_nothing_else_can_be_done_during_the_hearing`: `play`, `enter`, `search` and `unlock` are not accepted with `hearing_locked`; `talk` and `confront` raise; all save nothing; `restart` works and clears it.
- `test_three_answers_end_the_game_with_the_story_ending_of_the_flags`: the four story endings, both languages, with no doubt or one: the shown id and the saved ending are the story's, and `verdict` is empty.
- `test_two_doubts_show_the_impostor_instead_of_case_closed`: the saved ending is still `full_case`, the shown one is `impostor` with the line `two`.
- `test_two_doubts_leave_the_other_endings_alone`: `impostor`, `stolen_credits` and `fifth_element`.
- `test_three_doubts_show_stolen_credit_whatever_the_flags`: from `full_case`, `impostor` and `fifth_element`; with Leonor helping the line is `three_help`.
- `test_stolen_credit_after_a_broken_messages_claim_says_why`: the line `no_originals`.
- `test_the_verdict_is_saved_and_a_reload_shows_it`.
- `test_the_hearing_cannot_be_answered_a_fourth_time`: not accepted, saves nothing.
- `test_a_card_not_held_or_unknown_is_rejected_at_the_hearing_and_saves_nothing`: also `answer` `7` and an extra field.
- `test_presenting_directly_still_gives_the_story_ending`: `play present_evidence` with no hearing: the story's ending, an empty `verdict`.

The old operations, the page and the files
- `test_talking_still_writes_nothing_and_old_operations_still_refuse_extra_fields`: `talk` on `slides` saves nothing; `talk` with `evidence`, `play` with `answer` and `open` with `npc` raise `ValueError`.
- `test_the_page_and_early_snapshots_never_contain_the_case_file`: `PAGE` contains no label, reveal, rebuff, claim, professor line or verdict line of either language; the snapshot of a new game neither; a hearing snapshot contains only the lines already said.
- `test_the_page_has_the_tray_and_the_hearing_inside_the_conversation_card`: `PAGE` has `function askEvidence(`, `function showHearing(`, `action.id === "present_evidence"`, `evidence_show` and `hearing_concede`, has no `id="hearing-card"`, and still has `action.id === "open_drawer"`, `if (option.cost) penalize(option.cost)` and the options filter line.
- `test_the_new_texts_exist_in_both_languages`: `evidence_show`, `evidence_title`, `evidence_empty`, `evidence_back`, `time_penalty_card`, `time_penalty_duarte`, `hearing_hint`, `hearing_concede`, `hearing_step`, `hearing_trust` and `hearing_locked` are non-empty in `en` and `pt`, with `{n}` in the two penalties and in `hearing_step`.
- `test_app_3d_reloads_the_new_modules_in_order`: `CODE_MODULES`, read from the source of `app_3d.py` without running it, has `campus_case` and `campus_evidence` after `campus_search` and before `campus_game`; neither file is in `PAGE_FILES`; `page3d.py` does not import them.
