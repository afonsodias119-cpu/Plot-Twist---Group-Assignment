"""The night's clock of the 3D game (specs/night-schedule.md): what costs campus minutes, when the
clerk and Leonor leave, and when Duarte does his rounds. Rules and numbers.

SERVER ONLY (point 5): this file is never put in the page (page3d.py does not import it). Its only
text is the clerk's schedule sentence, SHUTTER, because it names the date of the code of computer 12.
Every other text of the schedule is in campus_text.py.

The campus minute goes from 0 (22:15) to 30 (22:45). It is a whole number or a whole number and a
half: only the copy costs half a minute (point 1). Every mark below is a whole minute, so a half
never changes a rule.

At the end, the day of the case (specs/case-of-the-day.md): which case a date gives.
"""

from datetime import datetime
from zoneinfo import ZoneInfo

# Campus minutes charged by the server (point 2): an accepted story action, a card, being caught.
# The copy costs half a minute because the torn photo already takes its own real time (point 13).
COSTS = {"request_copy": 0.5, "ask_for_help": 1, "accuse": 1, "view_files": 1,
         "card_right": 0, "card_wrong": 2, "card_duarte": 1, "caught": 3}
# Campus minutes the page takes off by itself, as before, and reports with `time`.
PAGE_COSTS = {"rude_answer": 5, "wrong_spot": 1, "wrong_code": 2}   # a wrong date on the calendar: 2 (specs/calendar-code.md)
NIGHT_MINUTES = 30
# The minute at which each person leaves by the schedule: 22:25 and 22:30 (point 5).
LEAVES = {"amelia": 10, "leonor": 15}
# The unknown number warns this many minutes before a person leaves: `shop` from minute 5 to 9,
# `leonor` from minute 10 to 14 (point 7).
WARNING = 5
# Duarte's rounds: 22:27, 22:34, 22:41 (point 8).
ROUNDS = (12, 19, 26)
# The minutes the page must report (point 4): a warning, a departure, a round and the minute after it, the end.
MARKS = (5, 10, 11, 12, 13, 15, 18, 19, 20, 25, 26, 27, 30)
# Minute 0 is 22:15, in minutes after midnight.
START = 22 * 60 + 15

# The clerk's schedule sentence (design-notes/texts-2-schedule.md, A1). The slip on the shutter gives
# the date of the code a second source, so it must never reach the page source.
SHUTTER = {
    "en": "The shutter is down and the counter is dark. The clerk went home at 22:25. A slip is taped to the shutter: cover photo, order of 17 October, collect tomorrow.",
    "pt": "A grade está descida e o balcão às escuras. A funcionária foi para casa às 22:25. Há um papel colado na grade: fotografia da capa, pedido de 17 de outubro, levantar amanhã.",
}


def time_text(minute):
    """The campus time of a minute, as the interface writes it: 12.5 is "22:27" (the whole minutes)."""
    total = START + int(minute)
    return f"{total // 60:02d}:{total % 60:02d}"


def next_mark(minute):
    """The first mark after `minute`, and 30 once the night is over (point 10, `report_at`)."""
    return next((mark for mark in MARKS if mark > minute), NIGHT_MINUTES)


def round_reached(old, new):
    """The first round that a move of the clock from `old` to `new` reaches, or None (point 8).

    A round is reached when the old minute is below it and the new one at or above it.
    """
    return next((mark for mark in ROUNDS if old < mark <= new), None)


def duarte_place(minute):
    """Where Duarte stands: at the lab door in the minute before a round and in its minute (point 10)."""
    whole = int(minute)
    return "lab_door" if any(whole in (mark - 1, mark) for mark in ROUNDS) else "auditorium"


# ---------- the case of the day (specs/case-of-the-day.md, point 1) ----------
# The day is Lisbon's, so the case changes at midnight in Portugal whatever the host's own time zone is.
LISBON = ZoneInfo("Europe/Lisbon")
# The cases in the order the days walk through them (the ids of campus_case.CASES). Only the classic
# case is left (specs/computer-lab-backup.md): every day plays it, and the page still shows the date.
CASE_ORDER = ("outsider",)


def case_day():
    """Today's date in Lisbon."""
    return datetime.now(LISBON).date()


def case_of_day(day):
    """The case of a date: the same date always gives the same case, for every player, and
    consecutive days take the cases of CASE_ORDER in turn."""
    return CASE_ORDER[day.toordinal() % len(CASE_ORDER)]
