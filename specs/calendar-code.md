# The code of computer 12: the group remembers the day, the phone checks it

Extends specs/pen-and-code.md and specs/night-schedule.md. No change to `story.py`, `logic.py`, `db.py`, `game.py` or `app.py`. The server only gains one read-only field in the snapshot; nothing new is saved. Every text exists in Portuguese and English.

## Before writing the spec

- **Product and user:** a player of the 3D game who reaches computer 12.
- **Trigger:** the player finds the USB stick (Rita), convinces Leonor to help, and then uses computer 12 in the computer lab.
- **Before:** Tomás says the code is "the day and month of the cover photo" and the clerk simply says the date ("On 14 November…"). The player only has to remember two lines; there is nothing to work out. A wrong code costs 1 minute.
- **Rule:** nobody says the date, and the date moves to **Saturday 17 October 2026** (code `1710`), so the phone can show the whole month: October is over when the game is played, in November.
  The people whose clue the player solved come along to the computer lab. There the player asks them what they remember of the day of the photo; each remembers one thing, and the phone's Weather and Calendar apps turn those memories into one day.
- **After:**
  1. **Who comes along.** Rita follows the player once the USB stick is found; Leonor follows once she has agreed to help (`ask_for_help`). Tomás is already in the computer lab. The clerk stays at the print shop (she goes home at 22:25). In 3D, a follower walks a few steps behind the character, along the character's own path; once the saved room is the computer lab (or the files were seen) they wait beside computer 12. Back in their own room they can still be talked to, as before. It is only a picture: the server decides who follows, from the saved game.
  2. **The clerk no longer says the date.** Her `order` line keeps the order file and the four people, without the date. Her memory line (`again`, night 2 and later) still says the date (now "The seventeenth of October"): by then the player already knows it from an earlier night. The date stamp on the original photo (now "17.10", specs/torn-photo.md) and the slip on the shutter after 22:25 (now "order of 17 October", specs/night-schedule.md) stay: an attentive player does not need the rest.
  3. **A live conversation at computer 12.** Before the files, the conversation with computer 12 offers "Ask the group what they remember about the day of the photo" (once per conversation). The question goes out as the player's message; then each person present answers in turn, as a speech bubble with their name, with the typing dots in between:
     - Tomás: the sun was incredible (→ the Weather app: a sunny day).
     - Rita: it was a Saturday (→ three sunny Saturdays: 3, 10 and 17).
     - Leonor: it was after the Finance test, on 15 October (→ only Saturday 17 is left).
     When someone is missing, a line says that whoever did not come cannot remember anything. A last line says that the phone keeps the whole month in the Weather and Calendar apps.
  4. **Two new phone apps, both for October 2026** (the whole month). **Weather** (Carcavelos, October): sunny, cloudy or rain for each of the 31 days; the sunny Saturdays are the 3rd, 10th and 17th (the 24th rains, the 31st is cloudy). **Calendar**: October 2026 (Monday first), the days with an event marked, and the list: group meetings (6, 13, 20, 27), the Finance test (15), the Microeconomics test (22) and an interim report hand-in (30).
  5. **The code.** "🔒 Enter the code" opens the usual 4-digit field, with the line "Every wrong code costs 2 minutes." The server checks the code as before. A wrong code costs **2 minutes** (it was 1; `PAGE_COSTS["wrong_code"]` follows). After **3 wrong codes** a line points to the date stamp on the original photo. The wrong codes are counted in this browser for this name and this night.

## What

- [ ] `prototypes/campus-3d/campus_people.py`: `FOLLOWERS` and `followers(state)` (Rita with `usb_stick`, Leonor with `colleague_choice == "help"`); the clerk's `order` text and note without the date (both languages); Tomás's `password` line ends with "between all of us we can work it out".
- [ ] `prototypes/campus-3d/campus_game.py`: the snapshot gains `followers: {"ids": [...], "at_lab": bool}`; `at_lab` is true when the files were seen or the saved room is the computer lab.
- [ ] `prototypes/campus-3d/campus_clock.py`: `PAGE_COSTS["wrong_code"]` is 2; `SHUTTER` says 17 October.
- [ ] `prototypes/campus-3d/campus_search.py`: `PC12_CODE = "1710"`; `PHOTO_TEXT` says 17.10; `photo.js` stamps 17.10.2026. The clerk's `again` line says 17 October.
- [ ] `prototypes/campus-3d/campus_text.py`: `group_ask`, `group_clues` (tomas, rita, leonor), `group_alone`, `group_phone`, `code_cost`, `code_hint`, `app_weather`, `weather_title`, `weather_place`, `weather_kinds`, `app_calendar`, `calendar_title`, `calendar_weekdays`, `calendar_events`.
- [ ] `prototypes/campus-3d/play.js`: the group question in the conversation with computer 12 (`askGroup`); `askCode` keeps the 4-digit field, costs 2 minutes and shows the hint after 3 wrong codes; the phone gets `drawWeather` and `drawCalendar` (the weather table `WEATHER` is in the page: it is a fact of the month, not the answer).
- [ ] `prototypes/campus-3d/game3d.html`: `updateFollowers` moves Rita and Leonor along the character's trail, or to their places beside computer 12; their small collision box goes with them.

## Reviewed tests that change

All approved by the team. Only the date changes in the last four.

- `tests/test_pen_and_code.py::test_tomas_and_the_clerk_give_the_two_halves_of_the_code` asked for "14" in the clerk's `order` line. That is exactly what this feature removes. It becomes `test_tomas_gives_the_rule_of_the_code_and_the_clerk_no_longer_says_the_date`: Tomás still gives the rule, the clerk's line has no day (now "17"), and the original photo still shows the date (now "17.10").
- `tests/test_pen_and_code.py::test_the_code_is_1411` becomes `test_the_code_is_1710`.
- `tests/test_torn_photo.py`: the photo's stamp is "17.10.2026" and the text says "17.10" (was 14.11).
- `tests/test_night_schedule.py::test_the_date_of_the_code_can_still_be_read_after_2225`: the slip shows "17" (was "14").
- `tests/test_earlier_nights.py`: `CLERK_AGAIN` says "The seventeenth of October" (was "The fourteenth of November").

## Out of scope

- The campus minutes charged for the copy (0.5) and for the files (1) stay as specs/night-schedule.md says: changing them breaks seven reviewed tests of that spec and needs its own decision with the team.

## Done when

- [ ] Every other test passes unchanged.
- [ ] `tests/test_calendar_code.py`: who follows and when; `at_lab`; the clerk without the date and the photo with it; the texts in both languages; the memories, the weather and the calendar leave exactly the day of the code (and three sunny Saturdays without Leonor); the group question and the 4-digit field; a wrong code costs 2 minutes and the third shows the hint; the phone has the two apps.
- [ ] In the browser: after finding the USB stick Rita walks behind the character; in the lab she stands beside computer 12; asking the group shows each answer in turn; the phone's Weather and Calendar apps show October; a wrong code costs 2 minutes; after three the photo hint appears; 1710 opens the files.
