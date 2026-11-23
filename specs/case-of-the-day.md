# Case of the day: everyone plays the same case on the same day, and the share card says which day

Extends specs/earlier-nights.md, specs/night-schedule.md, specs/campus-people-and-atmosphere.md (the share card) and specs/no-endings-on-start.md. Works together with specs/culprit-of-the-night.md: this spec picks the case from the date, that one says what each case changes. No change to `story.py`, `logic.py`, `game.py`, `app.py`, `db.py` or any reviewed test. The operation `open` keeps opening the classic case exactly as today.

> **Update (merge with specs/calendar-code.md):** the cover photo, its date (17 October) and the code `1710` are the same in every case, so the snapshot's `day` no longer carries `photo_date` and the cases no longer have a `code` or a `photo_date` (points 1 and 5 below say so). The "Case of 22 November" label now sits in the top bar of the case file, beside the game's name that specs/creator-after-name.md put there in place of "Case #005" (point 6).

## Why
With one fixed case, a player who has finished it can tell a friend every answer. With a case that changes every day, and the same case for everybody on that day, friends can compare their nights ("I got Case closed with 4 minutes left") without spoiling tomorrow's case, and a share card can say which day it was without saying anything about the answer.

## What
1. **The day of the case.** `campus_clock.py` gets `LISBON = ZoneInfo("Europe/Lisbon")`, `case_day()` (today's date in Lisbon: `datetime.now(LISBON).date()`) and `case_of_day(day)`: `CASE_ORDER[day.toordinal() % len(CASE_ORDER)]`. This spec is built first with `CASE_ORDER = ("outsider",)` and, in `campus_case.py`, `CASES = {"outsider": {...}}` holding the classic values in the shape of design-notes/texts-ideas.md, part B (order 1 to 5, nothing to accept or swap; the code and the photo belong to specs/calendar-code.md and are the same in every case); specs/culprit-of-the-night.md then adds `tomas` and `rita` and makes it `("outsider", "tomas", "rita")`. The ids never leave the server. The same date always gives the same case, for every player, and consecutive days walk through `CASE_ORDER` in turn (with the three cases, 22 November 2026 gives `tomas`, the 23rd `rita`, the 24th `outsider`). Lisbon time, so the case changes at midnight in Portugal whatever the host's own time zone is. `zoneinfo` is in Python's standard library; on Windows its time zone data comes from the `tzdata` package already installed through `uv.lock` (pandas), on the Linux host from the system.
2. **New operation `begin`**, with exactly `operation`, `player`, `language`, `names`. It is `open` plus the case of the day and the group's names (specs/your-own-group.md). `names` must be a list of exactly three strings (each can be empty); anything else is a `ValueError` and nothing is written.
   - A new game (no valid save): exactly what `open` does (a new save, the old night deleted), then the night's notes get `case = {"variant": case_of_day(case_day()), "date": "2026-11-22"}` and `names` (cleaned by specs/your-own-group.md; until that spec is built, `names` is only checked and not saved).
   - A continued game whose notes have a `case`: nothing changes and nothing is written; the names sent are ignored (a saved game keeps its case and its group).
   - A continued game with no `case` note (a save from before this feature, or a game started with `open`): its notes get `case = {"variant": "outsider", "date": ""}` and the names sent. It finishes as the classic case; from its next new game on it follows the day.
   - The reply is the snapshot, with the message of `open` (`started` or `continued`).
3. **`restart` keeps the kind of game.** Before the night is deleted, the server reads its `case`. If there was one, the new night gets today's case (`case_of_day(case_day())`, today's date) and the same `names`; if there was none (a classic game, as in every reviewed test), the restart is exactly as today and writes no notes. So "Play again" the next morning plays the next morning's case.
4. **The notes.** `campus_evidence.read_night` keeps `case` only when it is a dict with exactly `variant` (a key of `campus_case.CASES`) and `date` (`""` or a date `date.fromisoformat` can read); anything else counts as no case (the classic case). `write_night` writes `case` when there is one. The `games` row never holds the case: a save must keep exactly the story's flags (`logic.py:138`).
5. **The snapshot** gets `day`: `{"date": "2026-11-22", "label": "Case of 22 November"}`. `label` is `TEXT["case_of_day"]` with the day and `TEXT["months"]` (`"Caso de 22 de novembro"` in Portuguese), `""` when the date is empty. The torn photo has the same stamp in every case (17.10.2026, specs/calendar-code.md), so `day` has no stamp. `day` never carries the case's id, the code or the chat order; it is the same in every room.
6. **The start screen** shows "Case of 22 November" (`case_of_day`) in a new `<span id="case-day">` after `#caseNo` in the top bar of the case file (step 2 of specs/creator-after-name.md), where the game's name now stands: "● The Fifth Element · Case of 22 November". At phone width (520 px and below) the "Confidential" pill and the 22:15 clock give way to the label, which may go to a second line of the bar. The browser takes today's day and month from its own clock in Lisbon time (`Intl.DateTimeFormat("en-GB", { timeZone: "Europe/Lisbon", day: "numeric", month: "numeric" }).formatToParts(new Date())`) and writes them with the same `case_of_day` and `months` as the server, so both say exactly the same words; it is shown before the server knows the player. It is only a label: the server decides the case at `begin`. Nothing else is added to the start screen (no count of endings, specs/no-endings-on-start.md).
7. **The page** sends `begin` instead of `open` from `window.campusStart` (with the three names of specs/your-own-group.md, `["", "", ""]` until that spec is built). `send` treats `begin` like `open` (no time report first) and `applyNight` treats it like `open` when it decides that a fresh game at minute 0 starts with 30 minutes: both lines get `"begin"` added; the pinned lines (`const COUNTDOWN_MINUTES = 30`, the `night.minute === 0` line) are not touched. In the game, the eyebrow of the top bar shows `day.label` before ` · NOVA SBE` when it is not empty.
8. **The share card** gets one line after the title: `📅 Case of 22 November` (`day.label`), left out when the label is empty. It keeps the ending's emoji and title (the category, never a name: the four story titles and "22:46" name nobody), the clue squares (counts only), the time left and the collection. It never has a person's name, the case's id, a chat message or a code. Example:
   ```
   Plot Twist #005 🕵️
   📅 Case of 22 November
   🏆 Case closed
   🟩🟩🟩🟩🟨 · 4/4 clues
   ⏳ 04:12 · Endings found: 2/4
   ```
9. **Files.** `campus_clock.py` (the day), `campus_evidence.py` (the note), `campus_game.py` (`begin`, `restart`, `day`), `campus_text.py` (`case_of_day`, `months`, both languages), `play.js` (start screen label, `begin`, the eyebrow, the share line), `docs/plano-do-projeto.md`. No new Python module: `CODE_MODULES` of `app_3d.py` is pinned by a reviewed test (`tests/test_earlier_nights.py`, `test_app_3d_reloads_every_module_in_the_final_order`).

## Reviewed tests that change
None. Every reviewed test opens with `open`, which keeps the classic case and writes no notes; a classic `restart` still leaves no row (`test_a_restart_and_a_new_game_wipe_the_night`); `day` is empty in every classic snapshot, so no snapshot gains a date; the new snapshot key `day` is beside the others and no test compares a snapshot's keys.

## Limits
- The day comes from the server's clock. Around midnight the start screen (browser clock) and the case given (server clock) can differ by one day; the top bar shows the right one.
- A saved game keeps its case for as long as it is continued, even days later; only a new game takes today's.
- A hand-made client can use `open` and always get the classic case. The page never does.
- Everyone on one day has the same answers, so friends can still spoil today's case. They cannot spoil tomorrow's.
- The public host forgets saves and notes when it restarts, as before.

## Out of scope
Choosing a case by hand, a calendar of past cases, a leaderboard, the plain game (`app.py` stays the classic case).

## Done when
- Existing tests pass unchanged (the 388 pytest tests and `tests/continuous-conversations.cjs`, run with VS Code as Node); `play.js` passes `--check`.
- The tests below were written first and pass.
- A browser check in both languages: the start screen says "Case of <today>", a new game shows it in the top bar, a reload continues it, the share card has the 📅 line and no name, and "Play again" after changing the date by hand in a scratch database keeps working.

## Checks
`tests/test_case_of_the_day.py`, written before the code. `day` is controlled by replacing `campus_game.case_day` with `monkeypatch`; "saves nothing" means the same database bytes before and after.
- `test_the_same_date_gives_the_same_case_and_days_walk_through_the_order`: the same date twice gives the same case; for `len(CASE_ORDER)` consecutive days `case_of_day` gives every case of `CASE_ORDER` once, in its order (so the test holds with one case and with three).
- `test_case_order_lists_exactly_the_cases_of_the_case_file`: `set(CASE_ORDER) == set(campus_case.CASES)`.
- `test_the_day_is_lisbon_time`: `case_day()` equals `datetime.now(ZoneInfo("Europe/Lisbon")).date()`.
- `test_begin_starts_a_new_game_with_the_case_of_the_day`: the note `case` has `case_of_day` of that date and the date; `day.label` is `Case of 22 November` / `Caso de 22 de novembro`.
- `test_begin_rejects_bad_names_and_extra_fields_and_saves_nothing`: `names` missing, `"x"`, `[1, 2, 3]`, two strings, four strings, an extra field.
- `test_a_continued_game_keeps_its_case_on_another_day`: begun on the 22nd, continued on the 23rd: same case, nothing written.
- `test_an_old_save_is_marked_classic_and_follows_the_day_after_its_restart`: `open`, then `begin`: case `outsider` with an empty date; after `restart` the case of the day.
- `test_restart_of_a_daily_game_takes_todays_case_and_keeps_the_names`.
- `test_open_and_its_restart_stay_classic_and_write_no_notes`: no row after `open` and after a confirmed `restart`.
- `test_a_damaged_case_note_counts_as_the_classic_case`: notes written by hand with `case` as `"tomas"`, `{"variant": "nobody", "date": ""}`, `{"variant": "rita", "date": "yesterday"}`: no error, classic texts.
- `test_the_day_never_names_the_case`: `set(day) == {"date", "label"}`, with neither the case's id nor the code; the same `day` in the study room, in the print shop and once the photo is held; empty in a classic game.
- `test_the_page_shows_the_day_and_the_share_line`: `play.js` has `case-day`, `Europe/Lisbon`, `send("begin"` and `day.label`; `case_of_day` and `months` exist in both languages, with `{d}` and `{month}`, and 12 months each.
