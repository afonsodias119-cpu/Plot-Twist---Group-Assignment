"""Case of the day: everyone plays the same case on the same day (specs/case-of-the-day.md).

Written before the code: one test for every line under "Checks" in the spec, in the same order.

How to read this file:
- The day is never today's real date: `on(monkeypatch, day)` replaces `campus_game.case_day` with a
  function that gives `day`, exactly as the spec says. Only `test_the_day_is_lisbon_time` reads the
  real clock, to check `campus_clock.case_day` itself.
- `begin(...)` is the new operation, as the page sends it from the start screen: `open` plus the
  three names of specs/your-own-group.md. Until that spec is built the names are only checked, so
  no test here reads them back; the restart test only checks that a restart keeps whatever `names`
  the notes had.
- "saves nothing" means the database file has the same bytes before and after (`saved()`).
- A test that expects a ValueError first sends one valid `begin` and checks its reply, so it cannot
  pass only because the operation does not exist yet.
- The case ids, the order and the texts of each case belong to specs/culprit-of-the-night.md: here
  the tests ask `campus_clock.case_of_day` which case a date gives, so they hold with one case and
  with three.
"""

import importlib
import json
import sqlite3
import sys
from contextlib import closing
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import pytest

import db
import game
from story import STORIES, UI_TEXTS

PROJECT = Path(__file__).resolve().parents[1]
FOLDER = PROJECT / "prototypes" / "campus-3d"
sys.path.insert(0, str(FOLDER))
campus = importlib.import_module("campus_game")
TEXT = importlib.import_module("campus_text").TEXT

PLAYER = "detective"
NO_NAMES = ["", "", ""]
DAY = date(2026, 11, 22)
NEXT_DAY = date(2026, 11, 23)
# Part C of design-notes/texts-ideas.md, word for word.
CASE_OF_DAY = {"en": "Case of {d} {month}", "pt": "Caso de {d} de {month}"}
MONTHS = {"en": ["January", "February", "March", "April", "May", "June", "July", "August", "September",
                 "October", "November", "December"],
          "pt": ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro",
                 "outubro", "novembro", "dezembro"]}
LABEL = {"en": "Case of 22 November", "pt": "Caso de 22 de novembro"}
EMPTY_DAY = {"date": "", "label": ""}


# ---------- helpers ----------

def clock():
    """campus_clock.py, where the spec puts the day. Imported here so this file can be collected first."""
    return importlib.import_module("campus_clock")


def cases():
    """The cases of the case file (campus_case.CASES)."""
    return importlib.import_module("campus_case").CASES


def on(monkeypatch, day):
    """From now on the server believes that today is `day` (the spec's own way to control it)."""
    monkeypatch.setattr(campus, "case_day", lambda: day)


def call(operation="open", language="en", player=PLAYER, **extra):
    """One request to the server, exactly as the page sends it."""
    return campus.command(dict(operation=operation, language=language, player=player, **extra))


def begin(language="en", player=PLAYER, names=None):
    """The new operation `begin`, as the start screen sends it."""
    return call("begin", language, player, names=NO_NAMES if names is None else names)


def do(action, player=PLAYER, language="en"):
    """Play one story action (the `play` operation). It must be accepted."""
    result = call("play", language, player, action=action)
    assert result["accepted"], action
    return result


def restart(player=PLAYER, language="en"):
    """The confirmed "New game" (or "Play again")."""
    return call("restart", language, player, confirmed=True)


def saved():
    """The bytes of the database file: equal before and after means nothing was written."""
    return db.DB_PATH.read_bytes()


def notes(player=PLAYER):
    """The night's notes as they are saved, read straight from the file ({} when there is no row)."""
    return db.load_night(player)["notes"]


def night_rows(player=PLAYER):
    """How many rows of `nights` this player has (0 or 1)."""
    with closing(sqlite3.connect(db.DB_PATH)) as connection:
        return connection.execute("SELECT COUNT(*) FROM nights WHERE player = ?", (player,)).fetchone()[0]


def write_notes(player, **changes):
    """Rewrite this player's night notes by hand, the way a damaged file would have them."""
    night = db.load_night(player)
    written = dict(night["notes"], **changes)
    db.init_db()
    with closing(sqlite3.connect(db.DB_PATH)) as connection, connection:
        connection.execute("INSERT OR REPLACE INTO nights (player, minute, notes) VALUES (?, ?, ?)",
                           (player, night["minute"], json.dumps(written)))


def expected_case(day):
    """The note `case` a new game begun on `day` must have."""
    return {"variant": clock().case_of_day(day), "date": day.isoformat()}


# ---------- Checks ----------

def test_the_same_date_gives_the_same_case_and_days_walk_through_the_order():
    rules = clock()
    order = rules.CASE_ORDER
    assert isinstance(order, tuple) and len(order) >= 1
    assert rules.case_of_day(DAY) == rules.case_of_day(date(2026, 11, 22))
    walked = [rules.case_of_day(DAY + timedelta(days=step)) for step in range(len(order))]
    assert sorted(walked) == sorted(order)   # every case once
    first = order.index(walked[0])
    assert walked == [order[(first + step) % len(order)] for step in range(len(order))]   # in its order
    # The rule of the spec: the date's ordinal number picks the place in the order.
    for step in range(10):
        day = DAY + timedelta(days=step)
        assert rules.case_of_day(day) == order[day.toordinal() % len(order)]


def test_case_order_lists_exactly_the_cases_of_the_case_file():
    assert set(clock().CASE_ORDER) == set(cases())
    assert "outsider" in cases()


def test_the_day_is_lisbon_time():
    rules = clock()
    assert rules.LISBON == ZoneInfo("Europe/Lisbon")
    assert rules.case_day() == datetime.now(ZoneInfo("Europe/Lisbon")).date()


def test_begin_starts_a_new_game_with_the_case_of_the_day(monkeypatch):
    on(monkeypatch, DAY)
    for language in ("en", "pt"):
        player = f"daily {language}"
        result = begin(language, player)
        assert result["message"] == UI_TEXTS[language]["started"], language
        assert game.load(player) == STORIES[language]["start"], language
        assert notes(player)["case"] == expected_case(DAY), language
        assert result["day"]["date"] == "2026-11-22", language
        assert result["day"]["label"] == LABEL[language], language
        # Every later snapshot has it too.
        assert do("go_print_shop", player, language)["day"]["label"] == LABEL[language], language


def test_begin_rejects_bad_names_and_extra_fields_and_saves_nothing(monkeypatch):
    on(monkeypatch, DAY)
    assert begin()["day"]["label"] == LABEL["en"]   # a valid `begin`
    assert begin(names=["Ana", "", "João"])["day"]["date"] == "2026-11-22"   # names may be empty or not
    before = saved()
    bad_requests = [dict(operation="begin"),                                    # `names` missing
                    dict(operation="begin", names="x"),
                    dict(operation="begin", names=[1, 2, 3]),
                    dict(operation="begin", names=["Ana", "Bea"]),
                    dict(operation="begin", names=["Ana", "Bea", "João", "Rui"]),
                    dict(operation="begin", names=NO_NAMES, night=2)]           # an extra field
    for player in (PLAYER, "newcomer"):
        for bad in bad_requests:
            with pytest.raises(ValueError):
                campus.command(dict(bad, player=player, language="en"))
    assert saved() == before
    assert game.load("newcomer") is None   # no game was started for a new name either


def test_a_continued_game_keeps_its_case_on_another_day(monkeypatch):
    on(monkeypatch, DAY)
    begin()
    do("go_print_shop")
    case = notes()["case"]
    on(monkeypatch, NEXT_DAY)
    before = saved()
    result = begin(names=["Ana", "Bea", "João"])   # the names sent are ignored too
    assert result["message"] == UI_TEXTS["en"]["continued"]
    assert result["scene"] == "print_shop"
    assert result["day"]["date"] == "2026-11-22" and result["day"]["label"] == LABEL["en"]
    assert notes()["case"] == case == expected_case(DAY)
    assert saved() == before


def test_an_old_save_is_marked_classic_and_follows_the_day_after_its_restart(monkeypatch):
    on(monkeypatch, DAY)
    call("open")
    do("go_print_shop")
    result = begin()
    assert result["message"] == UI_TEXTS["en"]["continued"] and result["scene"] == "print_shop"
    assert notes()["case"] == {"variant": "outsider", "date": ""}
    assert result["day"] == EMPTY_DAY
    restarted = restart()
    assert notes()["case"] == expected_case(DAY)
    assert restarted["day"]["label"] == LABEL["en"] and restarted["scene"] == STORIES["en"]["start"]["scene"]


def test_restart_of_a_daily_game_takes_todays_case_and_keeps_the_names(monkeypatch):
    on(monkeypatch, DAY)
    begin(names=["Ana", "Bea", "João"])
    do("open_drawer")
    names_before = notes().get("names")
    on(monkeypatch, NEXT_DAY)
    result = restart()
    assert notes()["case"] == expected_case(NEXT_DAY)
    assert notes().get("names") == names_before   # the same group (nothing yet, until specs/your-own-group.md)
    assert result["day"]["date"] == "2026-11-23" and result["day"]["label"] == "Case of 23 November"
    # It is still a new night: a new game at 22:15, nobody cracked, no hearing.
    assert game.load(PLAYER) == STORIES["en"]["start"]
    assert result["night"]["minute"] == 0 and result["hearing"] is None and result["evidence"] == []


def test_open_and_its_restart_stay_classic_and_write_no_notes(monkeypatch):
    on(monkeypatch, DAY)
    result = call("open")
    assert result["day"] == EMPTY_DAY
    assert night_rows() == 0
    do("open_drawer")
    restarted = restart()
    assert restarted["day"] == EMPTY_DAY
    assert night_rows() == 0


def test_a_damaged_case_note_counts_as_the_classic_case(monkeypatch):
    on(monkeypatch, DAY)
    classic = call("open", player="classic")
    do("go_print_shop", player="classic")
    classic_line = call("talk", player="classic", npc="amelia", node="order")
    for number, damaged in enumerate(("tomas", {"variant": "nobody", "date": ""},
                                      {"variant": "rita", "date": "yesterday"})):
        player = f"damaged {number}"
        call("open", player=player)
        do("go_print_shop", player=player)
        write_notes(player, case=damaged)
        result = do("go_study_room", player=player)
        assert result["day"] == EMPTY_DAY, damaged
        do("go_print_shop", player=player)
        line = call("talk", player=player, npc="amelia", node="order")
        assert line["text"] == classic_line["text"] and line["note"] == classic_line["note"], damaged
    assert classic["day"] == EMPTY_DAY


def test_the_day_never_names_the_case(monkeypatch):
    on(monkeypatch, DAY)
    variant = clock().case_of_day(DAY)
    result = begin()
    assert set(result["day"]) == {"date", "label"}
    shown = json.dumps(result["day"])
    code = importlib.import_module("campus_search").PC12_CODE
    assert variant not in shown and code not in shown
    # Every case has the same photo (specs/calendar-code.md): the day is the same in every room.
    assert do("go_print_shop")["day"] == result["day"]
    assert do("request_copy")["day"] == result["day"]
    assert do("go_study_room")["day"] == result["day"]
    call("open", player="classic")
    assert do("go_print_shop", player="classic")["day"] == EMPTY_DAY


def test_the_page_shows_the_day_and_the_share_line():
    play_js = (FOLDER / "play.js").read_text(encoding="utf-8")
    # Changed by specs/night-and-clues.md ("Reviewed tests that change"): the page no longer shows the day
    # (was: "case-day", "Europe/Lisbon" and "day.label" in the page). It still sends `begin`; the server
    # still keeps the day and its words, checked below.
    assert 'send("begin"' in play_js
    for needle in ("case-day", "day.label"):
        assert needle not in play_js, needle
    for language in ("en", "pt"):
        t = TEXT[language]
        assert t["case_of_day"] == CASE_OF_DAY[language], language
        assert "{d}" in t["case_of_day"] and "{month}" in t["case_of_day"], language
        assert t["months"] == MONTHS[language] and len(t["months"]) == 12, language
