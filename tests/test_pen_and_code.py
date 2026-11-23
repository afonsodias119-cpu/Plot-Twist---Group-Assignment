"""The hidden USB stick and the code of computer 12 (specs/pen-and-code.md)."""

import importlib
import json
import sys
from pathlib import Path

import pytest

import db
import game

FOLDER = Path(__file__).resolve().parents[1] / "prototypes" / "campus-3d"
sys.path.insert(0, str(FOLDER))
campus = importlib.import_module("campus_game")
search = importlib.import_module("campus_search")
people = importlib.import_module("campus_people")
page3d = importlib.import_module("page3d")
TEXT = importlib.import_module("campus_text").TEXT

PLAYER = "seeker"
WRONG_SPOT = next(spot for spot in search.SPOTS if spot != search.PEN_SPOT)


def call(operation="open", language="en", **extra):
    return campus.command(dict(operation=operation, language=language, player=PLAYER, **extra))


def saved():
    return db.DB_PATH.read_bytes()


# ---------- searching the study room ----------

def test_a_wrong_spot_finds_nothing_and_saves_nothing():
    call()
    before = saved()
    result = call("search", spot=WRONG_SPOT)
    assert result["found"] is False and not result["accepted"]
    assert result["message"] == search.SEARCH_TEXT["en"]["nothing"][WRONG_SPOT]
    assert saved() == before


def test_the_right_spot_gives_the_stick_once():
    call()
    result = call("search", spot=search.PEN_SPOT)
    assert result["found"] is True and result["accepted"]
    assert game.load(PLAYER)["inventory"] == ["usb_stick"]
    again = call("search", spot=search.PEN_SPOT)
    assert again["found"] is False and not again["accepted"]
    assert game.load(PLAYER)["inventory"] == ["usb_stick"]


def test_searching_outside_the_study_room_is_refused():
    call()
    call("play", action="go_library")
    before = saved()
    result = call("search", spot=search.PEN_SPOT)
    assert result["found"] is False and not result["accepted"]
    assert saved() == before


def test_unknown_spots_and_extra_fields_are_rejected():
    call()
    for bad in (dict(spot="sofa"), dict(spot=7), dict(spot=search.PEN_SPOT, extra=1)):
        with pytest.raises(ValueError):
            call("search", **bad)


# ---------- the code of computer 12 ----------

def test_a_wrong_code_saves_nothing():
    call()
    call("search", spot=search.PEN_SPOT)
    call("play", action="go_computer_lab")
    before = saved()
    for code in ("0000", "1114", "141", "abcd"):
        result = call("unlock", code=code)
        assert result["unlocked"] is False and not result["accepted"]
        assert result["message"] == TEXT["en"]["code_wrong"]
    assert saved() == before
    with pytest.raises(ValueError):
        call("unlock", code=1411)


def test_the_right_code_views_the_files_with_the_stick():
    call()
    call("search", spot=search.PEN_SPOT)
    call("play", action="go_computer_lab")
    result = call("unlock", code=search.PC12_CODE)
    assert result["unlocked"] is True and result["accepted"]
    assert game.load(PLAYER)["flags"]["files_viewed"] is True


def test_the_right_code_without_the_stick_is_still_refused():
    call()
    call("play", action="go_computer_lab")
    before = saved()
    result = call("unlock", code=search.PC12_CODE)
    assert result["unlocked"] is True and not result["accepted"]   # the story's own rule: the backup copy is needed
    assert saved() == before


def test_the_code_is_1710():
    assert search.PC12_CODE == "1710"   # Saturday 17 October (specs/calendar-code.md)


# ---------- nothing in the page gives the answers away ----------

def test_the_page_never_contains_the_answers():
    page = page3d.build_page(playable=True, inline=True)
    assert search.PC12_CODE not in page
    # Every spot has its id and label in the page (the 3D draws them all); what is under each one is not.
    for language in ("en", "pt"):
        texts = search.SEARCH_TEXT[language]
        assert texts["found"] not in page
        assert not any(text in page for text in texts["nothing"].values())


def test_snapshots_never_contain_the_answers():
    call()
    text = json.dumps(call("search", spot=WRONG_SPOT))
    assert search.PC12_CODE not in text and search.SEARCH_TEXT["en"]["found"] not in text


# ---------- texts ----------

def test_every_spot_has_a_label_and_a_text_in_both_languages():
    for language in ("en", "pt"):
        assert set(TEXT[language]["spots"]) == set(search.SPOTS)
        assert set(search.SEARCH_TEXT[language]["nothing"]) == set(search.SPOTS) - {search.PEN_SPOT}
        assert search.SEARCH_TEXT[language]["found"].strip()


def test_tomas_gives_the_rule_of_the_code_and_the_clerk_no_longer_says_the_date():
    # Changed with the team's approval (specs/calendar-code.md): the day is worked out on the calendar of
    # computer 12, so the clerk's `order` line no longer says it. The original photo still shows it.
    for language in ("en", "pt"):
        nodes_tomas = people.PEOPLE[language]["tomas"]["nodes"]
        nodes_clerk = people.PEOPLE[language]["amelia"]["nodes"]
        assert "password" in nodes_tomas and nodes_tomas["password"]["note"]
        assert "17" not in nodes_clerk["order"]["text"] and nodes_clerk["order"]["note"]
        assert "17.10" in search.PHOTO_TEXT[language]
        assert "pen" in people.PEOPLE[language]["rita"]["nodes"]
    play_js = (FOLDER / "play.js").read_text(encoding="utf-8")
    assert 'action.id === "open_drawer"' in play_js and 'action.id === "view_files"' in play_js
