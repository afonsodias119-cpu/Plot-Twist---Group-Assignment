"""The code of computer 12: the group remembers the day of the photo, the phone's Weather and Calendar apps
turn it into one date (specs/calendar-code.md)."""

import datetime
import importlib
import re
import sys
from pathlib import Path

FOLDER = Path(__file__).resolve().parents[1] / "prototypes" / "campus-3d"
sys.path.insert(0, str(FOLDER))
campus = importlib.import_module("campus_game")
search = importlib.import_module("campus_search")
people = importlib.import_module("campus_people")
TEXT = importlib.import_module("campus_text").TEXT
campus_clock = importlib.import_module("campus_clock")

PLAY = (FOLDER / "play.js").read_text(encoding="utf-8")
GAME = (FOLDER / "game3d.html").read_text(encoding="utf-8")
PLAYER = "calendar"


def call(operation="open", language="en", **extra):
    return campus.command(dict(operation=operation, language=language, player=PLAYER, **extra))


# ---------- who comes along ----------

def test_nobody_follows_at_the_start():
    assert call()["followers"] == {"ids": [], "at_lab": False}


def test_rita_follows_once_the_usb_stick_is_found_and_they_wait_in_the_lab():
    call()
    found = call("search", spot=search.PEN_SPOT)
    assert found["followers"] == {"ids": ["rita"], "at_lab": False}
    lab = call("enter", room="computer_lab")
    assert lab["room"] == "computer_lab" and lab["followers"] == {"ids": ["rita"], "at_lab": True}


def test_leonor_follows_when_she_helps_and_not_when_accused():
    for choice, expected in (("help", ["leonor"]), ("accused", [])):
        state = {"inventory": [], "flags": {"colleague_choice": choice}}
        assert people.followers(state) == expected
    assert people.followers({"inventory": ["usb_stick"], "flags": {"colleague_choice": "help"}}) == ["rita", "leonor"]


# ---------- the clerk and the date ----------

def test_the_clerk_no_longer_says_the_date_but_the_photo_still_shows_it():
    for language in ("en", "pt"):
        order = people.PEOPLE[language]["amelia"]["nodes"]["order"]
        for word in ("17", "October", "outubro"):
            assert word not in order["text"] and word not in order["note"], (language, word)
        assert "17.10" in search.PHOTO_TEXT[language]


# ---------- the group's memories, and the phone's Weather and Calendar ----------

def weather_in_page():
    """The WEATHER table of play.js, as {day: kind}."""
    block = re.search(r"const WEATHER = \{(.*?)\};", PLAY, flags=re.S).group(1)
    return {int(day): kind for day, kind in re.findall(r"(\d+): \"(\w+)\"", block)}


def test_the_texts_exist_in_both_languages_with_the_same_shape():
    for language in ("en", "pt"):
        t = TEXT[language]
        for key in ("group_ask", "group_alone", "group_phone", "code_cost", "code_hint", "app_weather", "weather_title",
                    "weather_place", "app_calendar", "calendar_title"):
            assert t[key].strip(), (language, key)
        assert set(t["group_clues"]) == {"tomas", "rita", "leonor"}
        assert set(t["weather_kinds"]) == {"sun", "cloud", "rain"}
        assert len(t["calendar_weekdays"]) == 7
        assert search.PC12_CODE not in str(t)
    assert set(TEXT["en"]["calendar_events"]) == set(TEXT["pt"]["calendar_events"])


def test_the_memories_and_the_apps_leave_exactly_the_day_of_the_code():
    # Tomás: it was sunny (Weather). Rita: it was a Saturday (Weather or Calendar). Leonor: after the Finance
    # test on 15 October (and the Calendar shows the test on the 15th). October 2026, the whole month.
    weather = weather_in_page()
    sunny = {day for day, kind in weather.items() if kind == "sun"}
    saturdays = {day for day in range(1, 32) if datetime.date(2026, 10, day).weekday() == 5}
    test_day = next(int(day) for day, text in TEXT["en"]["calendar_events"].items() if text == "Finance test")
    assert test_day == 15 and TEXT["pt"]["calendar_events"]["15"] == "Teste de Finanças"
    for language in ("en", "pt"):
        assert "15" in TEXT[language]["group_clues"]["leonor"]
    assert set(weather) == set(range(1, 32))                # the whole of October
    assert sunny & saturdays == {3, 10, 17}                 # three sunny Saturdays: without Leonor, three to try
    assert {day for day in sunny & saturdays if day > test_day} == {int(search.PC12_CODE[:2])}
    assert search.PC12_CODE[2:] == "10"                     # the month: October
    assert set(weather.values()) <= set(TEXT["en"]["weather_kinds"])
    assert "const MONTH = 9;" in PLAY                       # the apps draw October


def test_the_group_is_asked_at_computer_12_and_the_code_is_typed_in_the_field():
    assert 'line.npc === "computer12" && (line.actions || []).some(action => action.id === "view_files")' in PLAY
    assert "askGroup(button)" in PLAY
    assert 'current.people.some(person => person.id === "tomas")' in PLAY
    assert "current.followers?.ids" in PLAY
    assert "inputMode: \"numeric\", maxLength: 4" in PLAY
    assert 'send("unlock", { code })' in PLAY


def test_a_wrong_code_costs_2_minutes_and_the_third_points_to_the_photo():
    assert "penalize(2, t.time_penalty_code)" in PLAY
    assert "if (wrong === 3) addSaid(t.code_hint);" in PLAY
    assert campus_clock.PAGE_COSTS["wrong_code"] == 2


def test_the_phone_has_the_weather_and_calendar_apps():
    assert '["weather", "🌦️", t.app_weather, ""], ["calendar", "📅", t.app_calendar, ""]' in PLAY
    assert 'else if (view === "weather") drawWeather(screen, t);' in PLAY
    assert 'else if (view === "calendar") drawCalendar(screen, t);' in PLAY


def test_the_3d_followers_only_follow_the_server():
    assert "window.campusState?.followers" in GAME
    assert "updateFollowers(dt, t);" in GAME
    assert "LAB_SPOTS" in GAME
