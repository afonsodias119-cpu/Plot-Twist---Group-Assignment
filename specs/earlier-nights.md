# Earlier nights: the game remembers, and one night can finally end

Extends specs/evidence-and-hearing.md, specs/night-schedule.md, specs/fifth-element-ending.md and specs/campus-people-and-atmosphere.md. No change to `story.py`, `logic.py`, `game.py`, `app.py` or any reviewed test: the story keeps its four endings in the same order, and the plain game plays as before. `db.py` gains one table and two small functions.

## Why
Every new game is the same night again, and the game does not notice. A player who has seen an ending starts the next night knowing the pizza box, the date and the lie, while everybody else acts as if it were the first time. The secret ending already says that the fifth element is whoever appears "when four people stop believing each other": the game should remember each finished night, start the next one slightly wrong, and keep one last ending for the night where the player gets everything right.

## What
1. **One row per finished night.** `db.init_db` also creates the table `runs` (`id INTEGER PRIMARY KEY AUTOINCREMENT`, `player TEXT NOT NULL`, `ending TEXT NOT NULL`), beside `games` and `nights`. New in `db.py`: `add_run(player, ending)` and `load_runs(player)` (the endings of that name, oldest first; it never writes). Example: `(7, "ana", "stolen_credits")`. The game never deletes a row.
2. **When a night is counted.** Exactly once, when it finishes: at the verdict of the hearing; when `present_evidence` is played directly; or when the campus minute reaches 30 with no ending (the row then says `time_up`). The note `run` in the night's notes says it was written, so a reload or a second report cannot write it again. The ending recorded is the one that was shown (after the caps of the hearing). A plain "New game" on a night that did not finish is never counted, however many times it is pressed.
3. **What the server remembers of a name.** New module `campus_memory.py` (`night_number`, `seen`, `record`, `memory_view`). Every snapshot has `"memory": {"night": 3, "seen": ["impostor", "stolen_credits"], "open": false, "over": false}`: `night` is the number of rows plus 1 (a night whose row is already written keeps its number until the restart); `seen` are the story endings seen, each once, in the order of the story's list; `open` is true when all four are there; `over` is true once the true ending was recorded.
4. **The unknown number remembers too.** The snapshot has `whispers`: the messages due as this night starts, as `{"id", "text"}` (an empty list on night 1, after an ending and once `over`). Night 2 opens with "You again?". Nights 3, 4 and 5-and-later have their own line ("I have stopped counting the nights. You have not."); once `open`, the line of the night is replaced by a dare that says what is still missing. From night 3 the three round warnings of specs/night-schedule.md carry "Close the computer. He is walking." instead of the impersonal text (same ids; `campus_game` passes the night number to `campus_clock`). All these texts are in `campus_case.py`, because `campus_text.TEXT["notices"]` must keep exactly four entries and everything in `campus_text.py` is copied into the page.
5. **Answers you have heard before.** A dialogue answer can carry a campus-only key, `"night"`: the first night on which it is offered, the same in both languages and kept apart from the story's `"if"`. Example: `{"label": "Say the date before she does", "next": "again", "night": 2}`. `talk(state, language, person, node, night=1)` offers it only from that night, marks it `"memory": true` in the reply (the page draws a small ↺ in front of it), and refuses a direct request for a line that only such answers lead to. `talk` still writes nothing, and no memory answer has a `cost`. Six answers, all on `start` lines: the clerk (night 2: "Odd. I do not remember you leaving."), Tomás (night 2, straight to his claim line `slides`), Duarte (night 2), Rita (night 3, straight to her claim line `five`), Leonor (night 3) and the professor (night 4: "Never the same group. Always the same name."). The two shortcuts are what earlier nights buy: fewer commands on the night that needs them all.
6. **The fifth figure grows on the case-file photo.** No new image file: shapes drawn by `play.js` inside `.photo`, under the red box. Night 2: a dark silhouette; night 3: plus a long coat; night 4: plus a scarf; night 5: plus a hat (the detective's own colours); from night 6 the "?" on the red box becomes the first letter of the player's name. A short line under the name box says which night it is (`night_lines`), also on narrow screens, where the photo is hidden. After the true ending the figure is gone and the line says so. The start screen is drawn before the server knows the player, so the stage comes from a display copy in the browser (`plot-twist-night`: the night and `over` the server last reported): the night shown is the larger of that number and one more than the story endings in the existing `plot-twist-endings` list. The rules never read this copy.
7. **"You again?" survives the new game.** Today the fresh snapshot is drawn before the old messages are deleted (`play.js:1105-1112`), so a message of the new night would be shown and then wiped. The restart handler sets a `restarting` mark, `checkNotices` waits while it is set, and it runs again after the stores are cleared and the time is back to 30 minutes.
8. **The true ending, `night_over` ("22:46").** A campus layer over a saved `full_case`, decided by the server at the third answer of the hearing. All of: the rows of earlier nights hold the four story endings (tonight's row is not written yet); tonight's story ending is `full_case`; the hearing had no doubt (so the player was not caught); `tomas_word` and `rita_word` were both won tonight. Then the notes get `verdict: "night_over"`, the row says `night_over`, and the snapshot's `ending` is `{"id", "title", "text", "stamp", "emoji", "voices", "verdict"}` taken from `campus_case.py`. The row in `games` still says `full_case`, so the save stays valid for `logic.is_valid_state` and for `app.py`. A reload shows it again, because the verdict is saved; a damaged verdict is believed only when the saved ending, the three answers and the two words agree with it. With any condition missing the night ends as before.
9. **The page names nothing.** The page uses `ending.stamp`, `ending.emoji` and `ending.voices` when the ending carries them and gives the card the neutral class `ending-extra`; Duarte is hidden as in `impostor`. The id, the title, the stamp and the text exist only in `campus_case.py` and in the reply of the night that earned them. The collection keeps "n/4" and gains a ★ after the true ending. The text keeps its spoken quotes and its `voices` list (`rita`, `duarte`, `duarte`, `professor`) aligned in both languages: under Duarte's hood are the player's own hat, scarf and coat, and the last message comes from a sender who is no longer unknown.
10. **Files.** Final `CODE_MODULES` of `app_3d.py`: `story`, `logic`, `db`, `game`, `campus_text`, `campus_people`, `campus_search`, `campus_case`, `campus_clock`, `campus_memory`, `campus_evidence`, `campus_game`, `page3d`. None of the new modules is in `PAGE_FILES`. New texts in `campus_text.py`, both languages (`night_lines`, `night_done`, `memory_answer`). `docs/guiao-conversas.md` gets the memory answers, the whispers and the true ending.

## Reviewed tests that change
None. The story's endings list, `stamps` and `ending_voices` are not touched; `page3d.language_data` still lists exactly the story's four endings; `notices` keeps four entries and the case file four names; the node shapes compared by the reviewed test (`next`, `if`, trust, note) stay equal in both languages; exactly six answers have a `cost`; `talk` writes nothing; no existing operation gets a field.

## Limits
- Nights and runs live in the same database file as the saves: when the public host restarts, it forgets them, and the true ending needs the four endings found again.
- Endings already in a browser's collection are not imported by the server. A returning player can see 4/4 on the screen while the server's gate is closed. The browser is never trusted.
- `present_evidence`, `open_drawer` and `view_files` played directly are still accepted, as in specs/pen-and-code.md, and a direct `present_evidence` writes a row: a hand-made request can record runs and collect the four story endings in seconds. The true ending itself still needs the hearing with no doubt and the two words, which only the server can give.
- Memory belongs to the typed name, and a name is not a password: anyone who types it inherits its nights. The display copy belongs to the browser: two people on one computer see the same figure.
- `db.init_db` also creates `nights` and `runs` in the plain game's database file, where nothing uses them.
- A hand-made `talk` can still read a memory line only from its night on; the two shortcuts lead to lines that are reachable anyway.
- The figure and the ending card are page code, checked only by needles: they need the browser check.

## Out of scope
A fifth ending in `story.py`, importing endings from the browser, accounts or passwords, new image files, a "night" card after the restart, changing the four endings or the secret ending, the plain game. If time is short, cut the professor's and Leonor's memory lines first; keep the count of nights, "You again?", the figure and the true ending.

## Done when
- Existing tests pass unchanged.
- The tests below were written first and pass.
- A browser check shows night 2 after an ending ("You again?" still in the phone after the new game, the silhouette and the line on the start screen, a ↺ answer), and, with the four endings recorded, the true ending with its voices, a reload of it, and the empty photo afterwards.

## Checks
`tests/test_earlier_nights.py`, written before the code. `finish(ending)` plays a night to that story ending through the hearing with no doubt; "saves nothing" means the same database bytes before and after.

Counting nights
- `test_the_database_has_a_runs_table_and_old_files_get_it`: `init_db` twice; a file with only `games` gets `nights` and `runs` and keeps its rows.
- `test_the_first_night_is_night_1_with_nothing_seen`: `memory` is night 1, `seen` empty, `open` and `over` false, and `whispers` is empty.
- `test_a_finished_night_is_recorded_once`: after the verdict there is one row; `open`, a fourth `hearing` answer and a `time` report add none.
- `test_presenting_directly_records_the_night_too`.
- `test_the_faculty_closing_is_recorded_once_as_time_up`: `time` 30 twice gives one row `time_up`; it is not in `seen`.
- `test_a_plain_restart_is_not_a_night`: five confirmed restarts with no ending leave night 1 and no row.
- `test_the_night_number_grows_only_after_the_restart`: night 1 while the ending is on screen, night 2 after the new game.
- `test_the_shown_ending_is_the_one_remembered`: a `full_case` capped by three doubts records `stolen_credits`.
- `test_memory_belongs_to_the_name`: another name is still on night 1.
- `test_a_damaged_run_note_cannot_count_a_night_twice_or_raise`: notes written by hand with `run` as `"yes"`, `7` or missing.

The unknown number
- `test_night_2_opens_with_you_again_in_both_languages`: `whispers` is one entry with id `night-2`.
- `test_each_night_has_its_line_and_four_endings_change_it`: nights 3, 4, 5 and 9; with `open` the dare replaces the line.
- `test_from_night_3_the_round_warning_changes`: on nights 1 and 2 the text of `round-12` is the impersonal one; from night 3 it is the whisper, with the same id.
- `test_no_whisper_after_an_ending_and_none_after_the_true_ending`.

Answers heard before
- `test_memory_answers_appear_only_from_their_night`: for each of the six, absent the night before, present and marked `memory` on its night, in both languages; ordinary answers are not marked.
- `test_a_memory_line_cannot_be_asked_for_before_its_night`: `talk` to the clerk's `again` raises on night 1 and answers on night 2.
- `test_both_languages_have_the_same_nights_and_no_new_cost`: the `night` values are equal in `en` and `pt`, and the answers with a `cost` are still the six rude ones.
- `test_talking_on_a_later_night_still_saves_nothing`.

The true ending
- `test_the_true_ending_needs_the_four_endings_seen_before_tonight`: the perfect night with three endings seen shows `full_case`, even when it is the night that completes the four.
- `test_the_true_ending_needs_no_doubt_and_both_words`: one wrong answer, one catch, no Tomás, no Rita, or the wrong flags: never `night_over`.
- `test_the_true_ending_is_shown_saved_and_recorded`: the ending has `id`, `title`, `text`, `stamp`, `emoji` and `voices`; the saved game says `full_case`; `open` shows it again; the row says `night_over`; `memory.over` is true.
- `test_presenting_directly_never_gives_the_true_ending`.
- `test_the_four_story_endings_stay_reachable_after_the_gate_opens`.
- `test_a_damaged_verdict_cannot_give_the_true_ending`: `verdict` `night_over` written by hand on a night that ended in `stolen_credits`, and on a `full_case` with no hearing: the story's ending is shown.
- `test_the_true_ending_says_who_speaks_each_line_in_both_languages`: with the rule of `partsOf`, both texts have four spoken quotes and `voices` has four known speakers.
- `test_the_secret_texts_are_never_in_the_page_nor_in_an_early_snapshot`: the built page and a night-1 snapshot contain neither `night_over`, `22:46`, the two stamps, any whisper, nor any sentence of the true ending; `page3d.language_data` still lists the four story endings.
- `test_the_story_still_has_its_four_endings_in_the_same_order`.

The texts, the page and the files
- `test_the_night_texts_exist_in_both_languages`: `night_lines` has five lines with `{n}`, `night_done` and `memory_answer` are there; `notices` still has four entries and the case file four names.
- `test_the_page_draws_the_fifth_figure_and_keeps_you_again_through_a_new_game`: the page has `fifth-figure`, `plot-twist-night`, `function nightStage(`, `ending-extra`, `restarting` and `memory_answer`, and still has the options filter line.
- `test_old_operations_still_refuse_extra_fields`: `open` with `night`, `talk` with `night`, `restart` with `seen` raise `ValueError` and save nothing.
- `test_app_3d_reloads_every_module_in_the_final_order`: `CODE_MODULES` is exactly the list of point 10, and no new module is in `PAGE_FILES`.
