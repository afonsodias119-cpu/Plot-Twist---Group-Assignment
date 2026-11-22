# More to find in the rooms: student life on the walls, and two red herrings

Extends specs/hidden-object-table.md (the table of the study room), specs/pen-and-code.md (the search and the code), specs/night-schedule.md (the server charges minutes) and specs/campus-people-and-atmosphere.md (walking up and pressing K). No change to `story.py`, `logic.py`, `game.py`, `app.py`, `db.py` or any reviewed test. Texts in design-notes/texts-ideas.md, part E.

## Why
Outside the table, the rooms have only people and computer 12: every thing you can touch is a clue, so the player never has to decide what matters. A few objects that only make you smile about student life, and two that look like clues and are not, make the rooms feel lived in and make the player think before spending time.

## What
1. **Three more kinds on the study room table.** `student_card`, `timetable` and `receipt` join `campus_search.SPOTS`, each with its "nothing" text in `SEARCH_TEXT`, its label in `campus_text.TEXT["spots"]` and its own drawing in `table.js` (`    student_card: () =>`), drawn once each in `ITEMS` away from the stick. They follow the table's own rule: a wrong object costs 1 minute and is marked. The receipt says four pizzas, split four ways (it also quietly contradicts Rita in the `rita` case of specs/culprit-of-the-night.md). None looks like the stick: the card is twice its size, white, with a photo and the NOVA stripe; the other two are paper.
2. **Things to look at in the other rooms**, kept in `campus_search.py` (server only):
   ```python
   FINDS = {"print_shop": ("price_list", "order_book"), "library": ("noticeboard", "returns_trolley"),
            "computer_lab": ("lab_whiteboard", "computer7"), "auditorium": ("podium",)}
   FIND_MINUTES = {"order_book": 2}                   # the one that wastes time on purpose
   FIND_LATER = {"order_book": {"has": ["original_photo"]}, "computer7": {"flags": {"files_viewed": True}}}
   ```
   `FIND_TEXT[language][thing]` has `name`, `text` and, for the two red herrings, `later`: the text once the condition of `FIND_LATER` is true (checked with `logic._condition_met`, like the cards).
3. **The two red herrings and how the player can tell.**
   - **The order book** (print shop). "Cover photo, 5 prints. Five." It looks like proof of a fifth person, and it costs **2 minutes** (leafing through a year of orders), charged by the server, at the print shop, before the clerk goes home at 22:25. Once the original photo is held the same look says the margin note: one print for each of you and one for the professor's file; five prints, not five people; and it then costs nothing.
   - **Computer 7** (computer lab). A sticky note: "pw 2311, presentation day!!". Looking costs nothing; typing 2311 on computer 12 is a wrong code, 1 minute each time (the page's existing cost). Tomás's rule (day and month of the cover photo) already says it is wrong, and once the files are viewed the look says so: someone's own computer, someone's own password. 2311 is never the code of any case.
   The red herrings name no person, no date of the photo and no code that works, so they fit every case and every group.
4. **Flavour only**: the price list, the noticeboard, the returns trolley, the lab whiteboard and the podium. Each costs nothing, has no note and changes nothing.
5. **New operation `examine`** (not `look`: tests/test_rules_and_character.py keeps that word for the character's appearance, which never reaches the server), with exactly `operation`, `player`, `language`, `thing`. `thing` must be a text and one of the things of `FINDS`; otherwise `ValueError`, nothing written. During the hearing it is refused like `search` (`hearing_locked`), at 22:45 like every operation (`time_up_title`), after an ending or outside the thing's room with `examine_where`; each of these is the snapshot with `"examine": null`, not accepted, and saves nothing. Otherwise the reply is the snapshot plus `"examine": {"id", "name", "text", "minutes"}`, and when `minutes` is not 0 the server charges them through the existing `charge` (so they appear in `night.charged` and can reach a round, specs/night-schedule.md). Nothing else is written.
6. **The snapshot** gets `finds`: `[{"id", "name"}]` for the things of the saved room (the 3D room of the scene: the group chat is in the lab), `[]` after an ending. The texts are never in it.
7. **On the page.** In 3D each thing has a spot near the furniture it belongs to (game3d.html, a list beside `USABLE`: the print shop counter, the library's shelves and trolley, the lab whiteboard and the desk of computer 7, the podium), at least 1.2 m from any person; walking up to it shows the near note with `press_look` ("Press the K key to look: Price list"), and K sends `examine`. In the side panel (and so in the text mode) a section "Look at" (`look_title`) has one button per thing of `finds`. The reply's text is shown as the note over the picture and kept in the diary under the thing's name (`saveDiary`); a charge shows the usual `time_charged` note.
8. **Files.** `campus_search.py`, `campus_text.py` (`spots` labels, `look_title`, `examine_where`, `press_look`), `table.js`, `campus_game.py` (`examine`, `finds`), `game3d.html`, `play.js`, `play.css`. `campus_clock.COSTS` is not touched: its keys are pinned by a reviewed test, so the herring's minutes live in `FIND_MINUTES`.

## Reviewed tests that change
None. The table tests compare `SPOTS` with the labels, the "nothing" texts and the drawn kinds as sets, so three more kinds that are in all four places keep them green; the stick is still drawn once with the napkin right after it, and nothing new looks like it; `COSTS` and `PAGE_COSTS` keep their keys; `people` of each room are unchanged (`tests/test_campus_people.py:62`): the things are a list of their own.

## Limits
- The order book is meant to be unfair once: it costs 2 minutes and the player learns why only later.
- The three new table objects cost a minute when clicked, like every object of the table: that is the table's rule.
- `examine` is free for the flavour things, so a hand-made client can read them all: they hold nothing.

## Out of scope
New clues, objects that give items or change flags, more red herrings, looking at things in the plain game.

## Done when
- Existing tests pass unchanged, and `tests/continuous-conversations.cjs`; `play.js`, `table.js` pass `--check`.
- The tests below were written first and pass.
- A browser check in 3D and in the text mode, both languages: each thing can be reached and read, the order book charges 2 minutes and reads differently with the photo, computer 7's code is refused at computer 12, and the three new table objects are drawn and marked.

## Checks
`tests/test_more_to_find.py`, written before the code; "saves nothing" means the same database bytes.
- `test_the_new_table_kinds_are_in_every_list`: each of the three is in `SPOTS`, `SEARCH_TEXT`, `TEXT["spots"]` and `ITEMS`, once in `ITEMS`, both languages.
- `test_looking_at_flavour_costs_nothing_and_saves_nothing`: every flavour thing in its room.
- `test_the_order_book_costs_two_minutes_and_reads_differently_with_the_photo`: `minutes` 2 and `night.charged` 2; with the photo, the `later` text and 0.
- `test_computer_7s_code_is_never_a_code`: 2311 is wrong at computer 12 in every case of `campus_case.CASES`; after the files, the `later` text.
- `test_look_needs_the_room_and_no_ending`: `examine_where` from another room and after an ending; saves nothing.
- `test_look_is_locked_during_the_hearing_and_closed_at_2245`.
- `test_look_rejects_unknown_things_and_extra_fields`: `"knife"`, `7`, `["podium"]`, an extra field.
- `test_finds_lists_only_the_saved_rooms_things_and_no_text`: the lab's things also in the group chat; no `text` in the snapshot; `[]` after an ending.
- `test_the_red_herrings_name_no_code_date_or_person`: no `1411`, `14`, `Duarte`, `Leonor`, `Rita`, `Tomás` in their texts.
- `test_find_texts_have_the_same_keys_in_both_languages_and_are_not_in_the_page`.
- `test_the_page_can_look`: `play.js` has `send("examine"` and `look_title`; `game3d.html` has a spot for each of the seven things of `FINDS`.
