"""The torn photo of the print shop (specs/torn-photo.md)."""

import importlib
import json
import re
import sys
from pathlib import Path

import pytest

import db
import game

FOLDER = Path(__file__).resolve().parents[1] / "prototypes" / "campus-3d"
sys.path.insert(0, str(FOLDER))
campus = importlib.import_module("campus_game")
search = importlib.import_module("campus_search")
page3d = importlib.import_module("page3d")
TEXT = importlib.import_module("campus_text").TEXT

PLAYER = "jigsaw"
PHOTO_JS = (FOLDER / "photo.js").read_text(encoding="utf-8")
PLAY_JS = (FOLDER / "play.js").read_text(encoding="utf-8")
RIGHT = [[piece, 0] for piece in search.PHOTO_SOLUTION]


def call(operation="open", language="en", **extra):
    return campus.command(dict(operation=operation, language=language, player=PLAYER, **extra))


def at_the_print_shop():
    call()
    call("play", action="go_print_shop")


def test_a_wrong_photo_saves_nothing():
    at_the_print_shop()
    before = db.DB_PATH.read_bytes()
    swapped = [RIGHT[1], RIGHT[0]] + RIGHT[2:]
    turned = [[RIGHT[0][0], 90]] + RIGHT[1:]
    for pieces in (swapped, turned):
        result = call("assemble", pieces=pieces)
        assert result["assembled"] is False and not result["accepted"]
        assert result["message"] == TEXT["en"]["photo_wrong"]
    assert db.DB_PATH.read_bytes() == before


def test_the_right_photo_gives_the_original_photo_once():
    at_the_print_shop()
    result = call("assemble", pieces=RIGHT)
    assert result["assembled"] is True and result["accepted"]
    assert result["message"] == search.PHOTO_TEXT["en"]
    assert game.load(PLAYER)["inventory"] == ["original_photo"]
    again = call("assemble", pieces=RIGHT)
    assert again["assembled"] is False and game.load(PLAYER)["inventory"] == ["original_photo"]


def test_outside_the_print_shop_nothing_happens():
    call()
    before = db.DB_PATH.read_bytes()
    result = call("assemble", pieces=RIGHT)
    assert result["assembled"] is False and not result["accepted"]
    assert db.DB_PATH.read_bytes() == before


@pytest.mark.parametrize("pieces", [
    RIGHT[:8], RIGHT + [RIGHT[0]], [[RIGHT[0][0], 0]] * 9, [["z", 0]] + RIGHT[1:], [[RIGHT[0][0], 45]] + RIGHT[1:],
    [[RIGHT[0][0], "0"]] + RIGHT[1:], [[RIGHT[0][0], True]] + RIGHT[1:], [tuple(p) for p in RIGHT], "q,w,a", None,
])
def test_bad_arrangements_are_rejected(pieces):
    at_the_print_shop()
    with pytest.raises(ValueError):
        call("assemble", pieces=pieces)


def test_extra_fields_are_rejected():
    at_the_print_shop()
    with pytest.raises(ValueError):
        call("assemble", pieces=RIGHT, extra=1)


def test_the_solution_and_the_rebuilt_text_are_not_in_the_page():
    page = page3d.build_page(playable=True, inline=True)
    for language in ("en", "pt"):
        assert search.PHOTO_TEXT[language] not in page
    assert "PHOTO_SOLUTION" not in page and json.dumps(list(search.PHOTO_SOLUTION)) not in page
    snapshot = json.dumps(call("open"))
    assert search.PHOTO_TEXT["en"] not in snapshot


def test_photo_js_draws_nine_torn_pieces_and_the_date_stamp():
    pieces = dict(re.findall(r'(\w): \[(\d, \d)\]', PHOTO_JS[PHOTO_JS.index("const PIECES = {"):PHOTO_JS.index("};", PHOTO_JS.index("const PIECES = {"))]))
    assert set(pieces) == set(search.PHOTO_PIECES) and len(set(pieces.values())) == 9
    assert "17.10.2026" in PHOTO_JS
    assert "submit" in PHOTO_JS and "send(" not in PHOTO_JS   # it only draws; play.js talks to the server


def test_asking_the_clerk_for_the_copy_opens_the_pieces():
    assert 'const isPhoto = action.id === "request_copy";' in PLAY_JS
    assert "isPhoto ? openPhoto(line, action)" in PLAY_JS   # the button keeps the story's label
    assert "addSaid(t.photo_intro);" in PLAY_JS and 'send("assemble", { pieces })' in PLAY_JS


def test_the_texts_exist_in_both_languages():
    for language in ("pt", "en"):
        for key in ("photo_intro", "photo_title", "photo_hint", "photo_wrong", "photo_close"):
            assert TEXT[language][key].strip()
        assert search.PHOTO_TEXT[language].strip() and "17.10" in search.PHOTO_TEXT[language]


def test_the_page_carries_photo_js():
    assert "window.campusPhoto" in page3d.build_page(playable=True, inline=True)
    assert 'src="/photo.js"' in page3d.build_page(playable=True)
    assert '"/photo.js": "text/javascript"' in (FOLDER / "server3d.py").read_text(encoding="utf-8")
    assert '"photo.js"' in (FOLDER.parents[1] / "app_3d.py").read_text(encoding="utf-8")
