"""The security recording is the fourth proof (specs/camera-proof.md).

The guard's desk (specs/security-desk.md) gives a picture of computer 12 at 23:47. Keeping it asks the
server (the `footage` operation), which writes the note `footage`; then the card is in the hand and it
breaks Duarte's fourth claim ("I was not even here last night"). Without it, "Case closed" cannot be reached.
"""

import importlib
import json
import sqlite3
import sys
from contextlib import closing
from pathlib import Path

import pytest

import db
from story import STORIES

PROJECT = Path(__file__).resolve().parents[1]
FOLDER = PROJECT / "prototypes" / "campus-3d"
sys.path.insert(0, str(FOLDER))
campus = importlib.import_module("campus_game")
case = importlib.import_module("campus_case")
TEXT = importlib.import_module("campus_text").TEXT
PLAY_JS = (FOLDER / "play.js").read_text(encoding="utf-8")

PLAYER = "detective"
AT_2347 = 23 * 60 + 47


def call(operation="open", language="en", player=PLAYER, **extra):
    return campus.command(dict(operation=operation, language=language, player=player, **extra))


def play(*actions, player=PLAYER, language="en"):
    result = call(language=language, player=player)
    for action in actions:
        result = call("play", language, player, action=action)
        assert result["accepted"], action
    return result


def investigate(player=PLAYER, language="en"):
    """Every proof the save can hold: the USB stick, the photo, Leonor's help, the files and the backup."""
    return play("open_drawer", "go_print_shop", "request_copy", "go_study_room", "go_library", "ask_for_help",
                "go_study_room", "go_computer_lab", "view_files", "save_backup", player=player, language=language)


def keep(camera="computer_lab", minute=AT_2347, player=PLAYER, language="en"):
    return call("footage", language, player, camera=camera, minute=minute)


def saved():
    return db.DB_PATH.read_bytes()


def ids(reply):
    return [card["id"] for card in reply["evidence"]]


def hear(*answers, player=PLAYER):
    result = call("hearing", player=player, answer="start")
    assert result["accepted"]
    for value in answers:
        result = call("hearing", player=player, answer=value)
        assert result["heard"] is True, value
    return result


# ---------- keeping the picture ----------

def test_the_right_picture_becomes_the_last_card_of_the_hand():
    investigate()
    assert "footage" not in ids(call())
    kept = keep()
    assert kept["accepted"] and kept["footage"] is True
    assert ids(kept) == ["original_photo", "files", "backup", "footage"]
    assert db.load_night(PLAYER)["notes"]["footage"] is True
    again = keep(minute=23 * 60 + 46)   # keeping it twice changes nothing
    assert again["footage"] is True and ids(again) == ids(kept)
    for language in ("en", "pt"):   # a game keeps its own language, so one player for each
        player = f"label {language}"
        investigate(player, language)
        shown = keep(player=player, language=language)["evidence"]
        label = next(card["label"] for card in shown if card["id"] == "footage")
        assert label == case.CASE_TEXT[language]["labels"]["footage"]


def test_every_minute_from_2346_to_2349_and_only_computer_12_is_the_proof():
    for minute in range(23 * 60 + 40, 23 * 60 + 55):
        player = f"minute {minute}"
        investigate(player)
        assert keep(minute=minute, player=player)["footage"] is (23 * 60 + 46 <= minute <= 23 * 60 + 49), minute
    for camera in ("entrance", "print_shop", "study_room", "library", "auditorium"):
        player = f"camera {camera}"
        investigate(player)
        before = saved()
        refused = keep(camera=camera, player=player)
        assert not refused["accepted"] and refused["footage"] is False
        assert refused["message"] == TEXT["en"]["security"]["footage_wrong"]
        assert saved() == before and "footage" not in ids(refused)


def test_the_guard_must_have_been_shown_the_photo_or_the_files():
    call()   # nothing held
    before = saved()
    refused = keep()
    assert not refused["accepted"] and refused["footage"] is False
    assert refused["message"] == TEXT["en"]["security"]["footage_unconvinced"]
    assert saved() == before
    play("go_print_shop", "request_copy", player="photo only")
    assert keep(player="photo only")["footage"] is True
    play("open_drawer", "go_computer_lab", "view_files", player="files only")
    assert keep(player="files only")["footage"] is True


def test_bad_requests_raise_and_save_nothing():
    investigate()
    before = saved()
    for camera, minute in (("kitchen", AT_2347), (5, AT_2347), ("computer_lab", "23:47"),
                           ("computer_lab", True), ("computer_lab", 21 * 60), ("computer_lab", 24 * 60)):
        with pytest.raises(ValueError):
            keep(camera=camera, minute=minute)
    with pytest.raises(ValueError):
        call("footage", camera="computer_lab", minute=AT_2347, extra=1)
    assert saved() == before


def test_not_during_the_hearing_after_the_ending_or_after_2245():
    investigate()
    call("enter", room="auditorium")
    call("hearing", answer="start")
    locked = keep()
    assert not locked["accepted"] and locked["footage"] is False
    for _ in range(4):
        call("hearing", answer="concede")
    ended = keep()
    assert not ended["accepted"] and ended["footage"] is False
    assert ended["message"] == STORIES["en"]["messages"]["game_over"]

    investigate("late")
    call("time", player="late", minute=30)
    closed = keep(player="late")
    assert not closed["accepted"] and closed["footage"] is False


def test_a_damaged_note_gives_no_card():
    investigate()
    night = db.load_night(PLAYER)
    for damaged in ("yes", 1, [True]):
        notes = dict(night["notes"], footage=damaged)
        with closing(sqlite3.connect(db.DB_PATH)) as connection, connection:
            connection.execute("INSERT OR REPLACE INTO nights (player, minute, notes) VALUES (?, ?, ?)",
                               (PLAYER, night["minute"], json.dumps(notes)))
        assert "footage" not in ids(call()), damaged


# ---------- the fourth claim ----------

def test_duarte_has_a_fourth_claim_broken_only_by_the_recording():
    assert [claim["id"] for claim in case.HEARING] == ["name", "photo", "messages", "here"]
    assert case.HEARING[-1]["accepts"] == ["footage"]
    for language in ("en", "pt"):
        texts = case.CASE_TEXT[language]
        assert texts["claims"]["here"] and texts["right"]["here"]["footage"] and texts["wrong"]["here"]
        assert "Duarte" in texts["claims"]["here"]
        assert "4" in TEXT[language]["hearing_step"]


def test_without_the_recording_the_case_cannot_be_closed():
    investigate()
    call("enter", room="auditorium")
    ended = hear("files", "original_photo", "backup", "concede")
    assert ended["ending"]["id"] == "stolen_credits" and ended["hearing"]["doubts"] == 1


def test_with_the_recording_the_case_is_closed():
    investigate()
    keep()
    call("enter", room="auditorium")
    said = call("hearing", answer="start")
    for value in ("files", "original_photo", "backup"):
        said = call("hearing", answer=value)
    assert said["hearing"]["said"][-1]["text"] == case.CASE_TEXT["en"]["claims"]["here"]   # the fourth claim waits
    ended = call("hearing", answer="footage")
    assert ended["ending"]["id"] == "full_case" and ended["hearing"]["doubts"] == 0
    assert ended["hearing"]["said"][-1]["text"] == case.CASE_TEXT["en"]["right"]["here"]["footage"]


# ---------- the page ----------

def test_keeping_the_picture_asks_the_server_first():
    start = PLAY_JS.index('$("cctv-save").addEventListener("click"')
    handler = PLAY_JS[start:PLAY_JS.index('$("cctv-close")', start)]
    assert 'send("footage", { camera: cctvCamera, minute: cctvMinute })' in handler
    assert handler.index("send(") < handler.index("state.footage = true")   # the diary only after the server said yes
    assert "if (!current.footage)" in handler


def test_the_guard_never_stops_the_request_as_if_he_had_left():
    # catchUp checks that the person of the open card is still there; José is not one of the server's people.
    assert '!await catchUp(talking === "guard" ? null : talking)' in PLAY_JS
