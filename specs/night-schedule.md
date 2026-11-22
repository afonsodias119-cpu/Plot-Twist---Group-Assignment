# A campus that does not wait: a clock the server knows, two people who leave, and Duarte's rounds

Extends specs/harder-campus.md, specs/evidence-and-hearing.md, specs/pen-and-code.md and specs/campus-people-and-atmosphere.md. It reverses one line of specs/harder-campus.md ("Making the server know the time" was out of scope): from now on the server knows the campus minute. No change to `story.py`, `logic.py`, `db.py`, `game.py`, `app.py` or any reviewed test; the table `nights` already exists. The countdown stays 30 minutes, starts at 22:15 and still pauses while the game is closed.

## Why
The night has a countdown but nothing happens in it: everybody waits in their room until the player arrives, in any order, at any time. Thirty minutes should not be enough for everything. The player should have to choose who to see first, and a slow night should cost something real: a person who has gone home, a card missing at the hearing.

## What
1. **The campus minute.** `nights.minute` is a whole number from 0 (22:15) to 30 (22:45). It never goes down during a night; a confirmed restart deletes the row, so a new night starts at 0. It grows in two ways: the server charges an accepted action, and the page reports its own minute (point 3). A row that cannot be read counts as 0, and a number outside 0 to 30 is brought back inside.
2. **One cost table**, in the new module `campus_clock.py` (rules and numbers, no secrets):
   ```python
   COSTS = {"request_copy": 1, "ask_for_help": 1, "accuse": 1, "view_files": 1,   # an accepted story action
            "card_right": 0, "card_wrong": 2, "card_duarte": 1, "caught": 3}       # campus minutes, charged by the server
   PAGE_COSTS = {"rude_answer": 5, "wrong_spot": 1, "wrong_code": 1}               # taken by the page, as today
   NIGHT_MINUTES = 30
   LEAVES = {"amelia": 10, "leonor": 15}       # 22:25 and 22:30
   ROUNDS = (12, 19, 26)                       # 22:27, 22:34, 22:41
   MARKS = (5, 10, 11, 12, 15, 18, 19, 25, 26, 30)   # the minutes the page must report
   ```
   Everything that is not in `COSTS` is free on the server: walking (by a door or by a button), talking, the right place, opening and closing the chat, flagging a message, answering a claim. Reading is never punished; it takes the real time it takes. The six rude answers keep their 5 minutes and the wrong place and wrong code their 1, taken by the page as today (`talk` and the two wrong guesses must keep writing nothing) and reported with `time`. One helper charges after each accepted `game.play` of `campus_game.py` (so a right code and a direct `view_files` cost the same), and `confront` charges its card. A refused action costs nothing.
3. **New operation `time`** with exactly `operation`, `player`, `language`, `minute`. `minute` must be an `int` (not a `bool`) from 0 to 30; anything else, a missing field or an extra one is a `ValueError` and nothing is written. The server keeps the larger of the saved minute and the reported one. A minute that is not larger, or any report after an ending, changes nothing and writes nothing. Reply: the snapshot.
4. **How the page follows.** It keeps drawing its own countdown. After every reply it takes `night.charged` minutes off its time and then sets its time left to the smaller of its own and 30 minutes minus `night.minute`, so a cleared browser or another device no longer gets 30 new minutes. It sends `time` with its own whole minute: before a command, when it is ahead of `night.minute`; when it reaches `night.report_at`; and when the time is up. It never polls. The header shows the campus time before the countdown (`22:27 · ⏳ 18:04`). The page no longer takes `confront.minutes` off by itself: the same minutes arrive in `night.charged`. `const COUNTDOWN_MINUTES = 30`, the `const running = ...` line and `if (option.cost) penalize(option.cost)` are not touched.
5. **Two people leave.** The clerk is at the print shop until minute 10 (22:25, as her first line has always said: "We close in ten minutes."). Leonor is in the library until minute 15 (22:30), unless she is helping: then she stays, saving her screenshots. After that the room can still be entered, but the person is not in `people`, `talk` and `confront` refuse as for anyone who is not there, and the story action (`request_copy`; `ask_for_help` and `accuse`) is refused with a schedule sentence and nothing is saved: "The shutter is down and the counter is dark. The clerk went home at 22:25." / "Leonor's chair is empty. Her book is still open at the same page." In `texts` (what the text mode shows) that sentence is the first paragraph of the room, in place of the story's opening paragraph, which would say the opposite. `people_in_room(scene, state, language, gone=())` gets an optional last argument; `leonor_present` is also false once she has left.
6. **A clue that can no longer be got is lost, and a lost clue does not lock the auditorium.** The original photo is lost at minute 10 if it is not held. Leonor is lost at minute 15 if she is undecided, or at once when the photo is lost (her decision needs it). The door rule becomes: every clue done or lost; the story's own rule (the old files) stays. `missing_clues_note(state, language, minute=0)` keeps its two reviewed arguments. So every night can end; a night that lost a clue usually ends in `stolen_credits`. Each clue row of the snapshot gains `until` (`"22:25"`, `"22:30"` or `""`) and `lost`. The phone's Clues app shows both closing times from the start and "Too late" on a lost clue; the map unlocks the auditorium when every clue is found or lost.
7. **The unknown number keeps the time.** `night.messages` lists the messages due now as `{"id", "text"}`; the page shows each id once, with its other messages. `shop`: from minute 5 while the photo is not held ("The print shop closes at 22:25. You are still talking."). `leonor`: from minute 10 while she is undecided and not lost. `lost`: when a clue is lost ("Too late for that tonight. I will keep the light on for you tomorrow."). `round-12`, `round-19`, `round-26`: the minute before each round, unless Tomás has cracked; the text is impersonal ("Someone is walking the corridor. Do not be at computer 12 when he passes."). The texts are in `TEXT["schedule"]`; `TEXT["notices"]` keeps its four entries.
8. **Duarte's rounds.** A round is a moment: minutes 12, 19 and 26. If the minute reaches a round (by a report or by a charge) while the saved scene is the group chat and Tomás has not cracked, the player is caught: the server plays the story's own `go_computer_lab` (the chat closes; the flags already made stay), charges 3 minutes, and remembers the round in the notes (`caught`). The reply is not accepted and its message is Duarte's line, which ends with the existing notice sentence: "Those messages are not for you." A player who was caught starts the hearing with one doubt, however many times it happened, and the professor says why before the first claim. If Tomás has cracked he stands in the lab door: the round passes, nothing is charged, and the message says so. Outside the chat a round changes nothing.
9. **22:45.** When the minute is 30 and there is no ending, the night is closed (`night.closed`): every operation except `open`, `restart` and `time` is refused with "The faculty is closed" and nothing is written. The page shows its existing time-up card.
10. **The snapshot.** New object `night`: `{"minute": 12, "time": "22:27", "charged": 1, "report_at": 15, "gone": ["amelia"], "duarte": "lab_door", "caught": false, "closed": false, "messages": [{"id": "round-12", "text": "..."}]}`. `charged` is what this command cost (a catch included); `report_at` is the next mark after `minute`; `gone` are the people who have left; `duarte` is `"lab_door"` in the minute before a round and in its minute, otherwise `"auditorium"`. The old field `clock` (computed from progress, specs/campus-people-and-atmosphere.md) stays exactly as it is for the reviewed tests and is still not shown.
11. **The 3D picture only illustrates.** The clerk's body and name tag are hidden by id when she is in `night.gone` (the two existing rules for Leonor and Duarte stay); the print shop gets a shutter picture behind the counter; Duarte is placed at the lab door, with his name tag, while `night.duarte` says so. No walking animation, no new collider, no new light. Every rule above is on the server, so the text mode loses nothing.
12. **Files.** `campus_clock.py` goes in `CODE_MODULES` after `campus_case` and before `campus_evidence`; not in `PAGE_FILES`. New texts in `campus_text.py`, both languages (`schedule`, `todo_until`, `todo_lost`, `todo_hint_lost`, `time_charged`; `map_locked` is reworded). `docs/guiao-conversas.md` gets the schedule section.
13. **The balance is proved, and stays proved.** A throwaway script played these tables through the real rules (the story, the saved game, the dialogue trees, the door rule) with one command every 15, 30, 45 and 60 seconds. A command is one request a person sends: an answer in a conversation, a door, a search, a code, a flag, a card, an answer at the hearing; closing computer 12 counts as 5 seconds. The campus minute at the ending (the night has 30):

    | Route | commands, charged | 15 s | 30 s | 45 s | 60 s |
    |---|---|---|---|---|---|
    | `stolen_credits`: accuses Leonor | 16, 3 | 7.0 | 11.0 | 15.0 | 19.0 |
    | `impostor`: Leonor helps, nothing flagged | 16, 3 | 7.0 | 11.0 | 15.0 | 19.0 |
    | `full_case`: the three fake messages flagged | 22, 3 | 8.3 | 13.6 | 18.8 | 24.1 |
    | `fifth_element`: every clue, five flags | 24 to 27, 3 | 8.8 | 16.6 | 20.3 | 29.1 |
    | `fifth_element`: lab only, the photo and Leonor lost (2 doubts) | 18 to 21, 1 | 11.5 | 13.0 | 14.5 | 21.1 |
    | `full_case`, still reading the chat at a round: caught (1 doubt) | 24, 6 | 17.8 | 20.6 | no | no |
    | A careful first night: every hint, one wrong place, no confrontation (`full_case`) | 30, 4 | 11.3 | 18.6 | **25.8** | no |
    | A first night that talks first and tries three wrong places | 32 to 40, 4 to 6 | 16.5 (`impostor`) | 19.6 (`stolen_credits`) | 27.3 (`stolen_credits`) | no |
    | The best night: `full_case`, Tomás's word, Rita's word, no doubt | 34 to 37, 3 | 11.2 | 20.7 | **27.2** | no |
    | The same with the two memory shortcuts of specs/earlier-nights.md | 32 to 35, 3 | 10.7 | 20.2 | **25.7** | no |
    | Everything: every clue, three confrontations, a card to Duarte, five flags, every polite line | 82, 4 | 24.2 | **no** (22:45 at command 54) | no | no |

    What it shows. Every story ending has a route at all four paces. A careful first night with no confrontation ends at 22:40 at 45 seconds a command, with 4.2 minutes left. The best night fits at 45 seconds (2.8 minutes left on a first night, 4.3 with the shortcuts) and not at 60. A night that reaches the print shop too late still ends, in `stolen_credits`. Being caught costs exactly 3 more minutes and one doubt. Doing everything is impossible at 30 seconds a command whatever the order: the 32 polite lines and the 24 other commands that cannot be skipped are 56 commands, 28 minutes, plus at least 4 charged minutes. Only somebody who clicks every 15 seconds without reading can do it all.

## Reviewed tests that change
None. With no report the minute is the sum of the charges, and the reviewed paths charge at most 3 minutes in a night (the copy, the decision, the files, each once): measured over the 201 existing tests with a throwaway plugin that only counts these charges, the counter is used at minute 0, Leonor at minute 1 and the chat at minute 1 at the latest, and no test passes minute 3, so none meets minute 10, 12 or 15. The old operations keep their field sets; `talk`, wrong places, wrong codes and refused actions still write nothing; `people_in_room` and `missing_clues_note` keep their reviewed arguments; `clock` keeps its value; `notices` keeps four entries; the three pinned lines of `play.js` stay.

## Limits
- The server learns the real time only from the page. A hand-made client that never sends `time` pays only the charged minutes: it skips the waiting, the rude answers and the wrong guesses. It cannot undo a charge, bring a person back, or get a lost clue. A client that sends `time 30` only hurts itself.
- Between two reports the server's minute can be up to a minute behind the page's.
- `present_evidence`, `open_drawer` and `view_files` played directly are still accepted, as in specs/pen-and-code.md.
- The balance is a model of people, not a play test: 15 to 60 seconds a command are assumptions. The numbers are in one small file so they can be retuned, and the tests below fail if a retune breaks a claim.
- A first night can lose the photo and Leonor by minute 10. That is intended (the closing times are in the Clues app from the start, and the night still ends), but it is harsh.
- Duarte's seat in the auditorium is never empty for the rules: the picture at the lab door only illustrates.
- The public host forgets the night with the saves when it restarts.

## Out of scope
A night longer or shorter than 30 minutes, charging for talking or walking, closing a door (the print shop can always be entered), Duarte walking, new people, sounds for the rounds, a schedule in the plain game. If time is short, cut in this order and keep the rest: Duarte at the lab door in 3D, the shutter picture. Never cut the lost-clue rule.

## Done when
- Existing tests pass unchanged.
- The tests below were written first and pass.
- A browser check, in 3D and in text mode, shows the campus time, a charged minute, the clerk gone at 22:25 with the photo marked "Too late", the auditorium opening without it, and a catch at computer 12.

## Checks
`tests/test_night_schedule.py`, written before the code. `at(minute)` is `call("time", minute=minute)`; "saves nothing" means the same database bytes before and after.

The minute and its costs
- `test_a_new_night_starts_at_2215`: `night` is minute 0, time `22:15`, nobody gone, not caught, not closed, no message; `clock` still says `22:15`.
- `test_the_copy_the_decision_and_the_files_cost_one_minute_each`: `night.charged` is 1 after each of `request_copy`, `ask_for_help`, `accuse`, the right code and a direct `view_files`, and the minute is their sum.
- `test_walking_talking_flagging_and_the_hearing_cost_nothing`: the minute does not move after `enter` (by door and by buttons), `talk`, the right place, `open_chat`, a flag, closing the chat and the four `hearing` commands.
- `test_refused_actions_cost_nothing_and_save_nothing`: a blocked action, a wrong place, a wrong code, a refused door.
- `test_cards_cost_what_the_table_says`: 0 for the right card, 2 for a rebuff, 1 for Duarte; `confront.minutes` equals `night.charged`.
- `test_the_cost_table_is_whole_minutes_and_matches_the_rude_answers`: every value of `COSTS` and `PAGE_COSTS` is an `int` from 0 to 5, and every `cost` in `campus_people.PEOPLE` equals `PAGE_COSTS["rude_answer"]`.

The `time` operation
- `test_time_keeps_the_larger_minute_and_never_goes_down`: 7 gives 7; then 3 and 7 again give 7 and save nothing.
- `test_a_charge_is_added_to_the_reported_minute`: `at(4)` then the copy gives 5.
- `test_time_rejects_bad_minutes_and_extra_fields_and_saves_nothing`: `"5"`, `5.0`, `True`, `None`, `[5]`, `-1`, `31`, no `minute`, an extra field.
- `test_time_needs_a_game_and_changes_nothing_after_an_ending`.
- `test_a_damaged_minute_in_the_table_is_brought_back_between_0_and_30`: rows written by hand with minute `99`, `-5` and `'x'` give a snapshot with a minute from 0 to 30 and no error.
- `test_report_at_is_the_next_mark`: 5 at the start, 10 at minute 5, 30 at minute 26.
- `test_a_restart_brings_the_night_back_to_2215`.

The two departures and the lost clues
- `test_the_clerk_is_gone_at_2225`: at minute 9 she is in `people` and gives the copy; at 10 `people` is empty, `talk` and `confront` raise, `request_copy` is not accepted with the schedule sentence and saves nothing, and the room can still be entered.
- `test_leonor_leaves_at_2230_unless_she_is_helping`: undecided, she is gone at 15 and both decisions are refused with her sentence; helping, she is still there at 29.
- `test_the_room_text_starts_with_the_schedule_sentence`: both rooms, both languages: after the time, `texts[0]` is the sentence and the story's opening paragraph is not in `texts`; before it, `texts` are the story's.
- `test_the_closing_times_are_on_the_clue_rows_from_the_start`: `until` is `22:25` for the photo, `22:30` for Leonor, empty for the other two; nothing is lost at minute 0.
- `test_a_lost_photo_loses_leonor_too_and_no_longer_locks_the_auditorium`: at minute 10 without the photo both rows are `lost` and not `done`; with the stick and the files the auditorium is entered by the door and by the button.
- `test_leonor_alone_is_lost_at_2230_when_the_photo_is_held`.
- `test_the_story_rule_still_needs_the_old_files`: with both clues lost and no files, the door is refused.
- `test_a_night_that_lost_the_print_shop_ends_in_stolen_credit`: through the hearing, saying nothing to the two claims that cannot be answered.
- `test_the_reviewed_paths_never_meet_the_schedule`: the usual path (stick, copy, help, files, chat, auditorium) with no report ends at minute 3, and the door note for a new game is unchanged.

The unknown number
- `test_the_warnings_come_at_minute_5_and_10_and_when_a_clue_is_lost`: ids `shop`, `leonor` and `lost`, each only inside its minutes and its condition (no `shop` once the photo is held), in both languages.
- `test_the_warning_comes_one_minute_before_each_round_and_is_impersonal`: `round-12` at 11, `round-19` at 18, `round-26` at 25; not once Tomás has cracked; the text has no "I ".

Duarte's rounds
- `test_duarte_catches_the_player_in_the_group_chat`: in the chat, `at(12)`: not accepted, the scene is the lab, the flags are kept, the minute is 15, `night.caught` is true, and the message ends with `notice_chat` and a quotation mark, in both languages.
- `test_a_charge_that_reaches_a_round_catches_too`: in the chat at minute 10, a rebuff from Tomás.
- `test_outside_the_chat_a_round_changes_nothing`.
- `test_tomas_at_the_door_prevents_the_catch`: with Tomás cracked the chat stays open, nothing is charged and the message is the doorway line.
- `test_being_caught_twice_costs_six_minutes_and_one_doubt`: the hearing starts with 1 doubt and the professor's line about the messages comes before the first claim.
- `test_duarte_is_at_the_lab_door_only_around_a_round`: `night.duarte` is `lab_door` at 11 and 12, `auditorium` at 10 and 13.

22:45
- `test_the_faculty_closes_at_2245`: `at(30)` gives `night.closed`; `play`, `enter`, `search`, `unlock` and `hearing` are not accepted with `time_up_title`, `talk` and `confront` raise, all save nothing; `open`, `time` and `restart` work.

The balance, over the real tables (`paced(seconds)` plays a route through `campus.command` and, before each command, reports the whole minutes of real time plus the minutes charged so far)
- `test_every_story_ending_has_a_route_at_15_30_45_and_60_seconds`: the first five routes of the table; each ending is shown at each pace by at least one of them.
- `test_a_careful_first_night_fits_at_45_seconds_with_three_minutes_left`.
- `test_the_best_night_fits_at_45_seconds`: `full_case`, both words, no doubt, before minute 28.
- `test_being_caught_costs_three_minutes_and_one_doubt_and_the_night_still_ends`.
- `test_doing_everything_does_not_fit_at_30_seconds`: the polite lines counted from the real `PEOPLE`, plus the 24 other commands, at half a minute each, plus the smallest charges, is more than `NIGHT_MINUTES`; and the route that tries it is closed before its ending.

The texts, the page and the files
- `test_the_schedule_texts_exist_in_both_languages`: the same keys in `TEXT["schedule"]`, the four other new keys, `{time}` in `todo_until`, `{n}` in `time_charged`; `notices` still has four.
- `test_the_page_follows_the_server_clock`: the page has `function reportTime(`, `function applyNight(`, `night.charged`, `report_at`, `todo_until` and `todo_lost`, and still has `const COUNTDOWN_MINUTES = 30`, `const running = !current.ending && !document.hidden && !shell.hidden` and `if (option.cost) penalize(option.cost)`.
- `test_old_operations_still_refuse_extra_fields`: `play`, `talk`, `enter` and `open` with `minute` raise `ValueError`.
- `test_app_3d_reloads_campus_clock_before_the_modules_that_use_it`: in `CODE_MODULES` it comes after `campus_case` and before `campus_evidence`; it is not in `PAGE_FILES`.
