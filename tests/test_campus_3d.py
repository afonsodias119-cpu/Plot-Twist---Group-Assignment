"""Acceptance checks for the new 3D adapter; existing tests stay unchanged."""

import importlib
import json
import sys
import threading
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

import pytest

import db
import game
from story import STORIES

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "prototypes" / "campus-3d"))
campus = importlib.import_module("campus_game")
TEXT = importlib.import_module("campus_text").TEXT
server3d = importlib.import_module("server3d")
page3d = importlib.import_module("page3d")

SHORT = ["open_drawer", "go_computer_lab", "view_files", "go_study_room", "go_auditorium", "present_evidence"]
HELP = ["open_drawer", "go_print_shop", "request_copy", "go_study_room", "go_library", "ask_for_help", "go_study_room", "go_computer_lab", "view_files", "go_study_room", "go_auditorium", "present_evidence"]


def call(operation="open", language="pt", player="test detective", **extra):
    return campus.command(dict(operation=operation, language=language, player=player, **extra))


@pytest.mark.parametrize("language", ["en", "pt"])
# In the 3D version the auditorium needs every clue, so the short path (no photo, no Leonor) is not played here.
@pytest.mark.parametrize("path,ending", [(HELP, "impostor"), (["accuse" if a == "ask_for_help" else a for a in HELP], "stolen_credits")])
def test_both_endings_and_accusation_use_the_original_rules(language, path, ending):
    call(language=language)
    for action in path:
        result = call("play", language, action=action)
        assert result["accepted"]
    assert result["ending"]["id"] == ending
    assert result["ending"]["text"] == next(e["text"] for e in STORIES[language]["endings"] if e["id"] == ending)
    assert result["actions"] == []
    before = game.load("test detective")
    assert not call("play", language, action="go_study_room")["accepted"]
    assert game.load("test detective") == before


def test_blocked_route_and_duplicate_leave_save_unchanged():
    call()
    before = db.DB_PATH.read_bytes()
    result = call("play", action="go_auditorium")
    assert not result["accepted"] and result["scene"] == "study_room"
    assert db.DB_PATH.read_bytes() == before
    call("play", action="open_drawer")
    before = db.DB_PATH.read_bytes()
    result = call("play", action="open_drawer")
    assert not result["accepted"] and len(result["inventory"]) == 1
    assert db.DB_PATH.read_bytes() == before


def test_resume_restores_room_item_decision_language_and_notebook():
    call()
    for action in HELP[:6]:
        result = call("play", action=action)
    resumed = call(language="en")
    for key in ["scene", "inventory", "notebook", "language", "actions"]:
        assert resumed[key] == result[key]
    assert resumed["scene"] == "library" and resumed["language"] == "pt"
    assert len(resumed["notebook"]) == 3


def test_notebook_never_reveals_undiscovered_clues():
    result = call()
    assert result["notebook"] == [] and result["ending"] is None
    assert "23h47" not in json.dumps(result)
    result = call("play", action="open_drawer")
    assert len(result["notebook"]) == 1
    assert "23h47" not in json.dumps(result)
    assert all(a["id"] != "open_drawer" for a in result["actions"])


def test_restart_requires_explicit_confirmation_and_keeps_language():
    call(); call("play", action="open_drawer")
    before = db.DB_PATH.read_bytes()
    for confirmed in [False, "true", 1, None]:
        with pytest.raises(ValueError):
            call("restart", confirmed=confirmed)
        assert db.DB_PATH.read_bytes() == before
    result = call("restart", language="en", confirmed=True)
    assert result["scene"] == "study_room" and result["inventory"] == []
    assert result["notebook"] == [] and result["ending"] is None
    assert result["language"] == "pt"


@pytest.mark.parametrize("payload", [None, [], {}, {"operation": []},
    {"operation": "open", "language": "pt", "player": "<script>"},
    {"operation": "open", "language": {}, "player": "maria"},
    {"operation": "open", "language": "pt", "player": "maria", "state": {"ending": "impostor"}},
    {"operation": "play", "language": "pt", "player": "maria", "action": "open_drawer"}])
def test_bad_requests_never_create_a_saved_game(payload):
    with pytest.raises(ValueError):
        campus.command(payload)
    assert db.load_game("maria") is None


def saved_bytes():
    return db.DB_PATH.read_bytes()


def test_entering_a_room_uses_the_original_travel_actions():
    """Walking through a door is a request to travel: the server uses the story's own go_ action."""
    call()
    result = call("enter", room="library")
    assert result["accepted"] and result["scene"] == "library"
    assert game.load("test detective")["scene"] == "library"
    assert game.load("test detective")["inventory"] == []


def test_walking_between_two_rooms_goes_through_the_study_room():
    """Every room connects only to the study room, so the walk is two saved moves."""
    call(); call("play", action="go_print_shop")
    result = call("enter", room="library")
    assert result["accepted"] and result["scene"] == "library"
    assert call("enter", room="print_shop")["scene"] == "print_shop"


def test_entering_the_auditorium_is_refused_without_the_clues():
    """The door explains itself with a note that lists every missing clue, and nothing is saved."""
    call()
    before = saved_bytes()
    result = call("enter", room="auditorium")
    t = TEXT["pt"]
    assert not result["accepted"] and result["scene"] == "study_room"
    assert result["message"].startswith(t["auditorium_note"])
    assert all(t["clues"][clue] in result["message"] for clue in t["clues"])   # all four are missing
    assert saved_bytes() == before


def test_a_blocked_second_step_leaves_you_in_the_study_room():
    """From the library to the locked auditorium: the first move is accepted, the second is refused."""
    call(); call("play", action="go_library")
    result = call("enter", room="auditorium")
    assert not result["accepted"] and result["scene"] == "study_room"
    assert result["message"].startswith(TEXT["pt"]["auditorium_note"])
    assert game.load("test detective")["scene"] == "study_room"


def test_the_story_rule_alone_is_not_enough_for_the_auditorium():
    """With the old files viewed (the story's own rule) but no photo and no talk with Leonor, it stays closed."""
    call()
    for action in SHORT[:3]:
        call("play", action=action)
    before = game.load("test detective")
    result = call("enter", room="auditorium")
    t = TEXT["pt"]
    assert not result["accepted"] and result["scene"] == "study_room"   # the walk went through the hub, then stopped
    assert t["clues"]["original_photo"] in result["message"] and t["clues"]["leonor"] in result["message"]
    assert t["clues"]["usb_stick"] not in result["message"] and t["clues"]["files_viewed"] not in result["message"]
    after = game.load("test detective")
    assert after["scene"] == "study_room" and dict(after, scene=None) == dict(before, scene=None)   # only the room changed


def test_the_auditorium_opens_once_every_clue_is_done():
    """Pen, photo, old files and Leonor: then the same door opens, even coming from another room."""
    call()
    for action in HELP[:9]:
        call("play", action=action)
    result = call("enter", room="auditorium")
    assert result["accepted"] and result["scene"] == "auditorium"


def test_the_auditorium_button_needs_every_clue_too():
    """The on-screen travel button follows the same rule as walking in through the door."""
    call()
    for action in SHORT[:4]:
        call("play", action=action)
    before = saved_bytes()
    result = call("play", action="go_auditorium")
    assert not result["accepted"] and result["scene"] == "study_room"
    assert result["message"].startswith(TEXT["pt"]["auditorium_note"])
    assert saved_bytes() == before


def test_the_clue_list_and_the_auditorium_button_follow_the_progress():
    """The snapshot carries the phone's to-do list, and locks the auditorium button until it is complete."""
    start = call()
    assert [c["id"] for c in start["clues"]] == ["usb_stick", "original_photo", "files_viewed", "leonor"]
    assert not any(c["done"] for c in start["clues"])
    assert [c["room"] for c in start["clues"]] == [STORIES["pt"]["scenes"][r]["title"]
                                                    for r in ["study_room", "print_shop", "computer_lab", "library"]]
    button = next(a for a in start["actions"] if a["id"] == "go_auditorium")
    assert button["allowed"] is False and button["blocked_text"].startswith(TEXT["pt"]["auditorium_note"])

    for action in HELP[:9]:
        done = call("play", action=action)
    assert all(c["done"] for c in done["clues"])
    study = call("play", action="go_study_room")
    assert next(a for a in study["actions"] if a["id"] == "go_auditorium")["allowed"] is True


def test_leonor_counts_whether_you_ask_for_help_or_accuse():
    """The clue is the conversation: both choices complete it (the choice only changes the ending)."""
    call()
    for choice, path in [("help", HELP[:6]), ("accused", ["accuse" if a == "ask_for_help" else a for a in HELP[:6]])]:
        call("restart", confirmed=True)
        for action in path:
            result = call("play", action=action)
        assert next(c for c in result["clues"] if c["id"] == "leonor")["done"], choice


def test_phone_texts_exist_in_both_languages():
    """Every label of the phone, the map and the panel button exists in English and in Portuguese."""
    assert set(TEXT["pt"]) == set(TEXT["en"])
    assert set(TEXT["pt"]["clues"]) == set(TEXT["en"]["clues"]) == {"usb_stick", "original_photo", "files_viewed", "leonor"}
    for language in TEXT:
        assert all(isinstance(v, (str, dict)) and v for v in TEXT[language].values())


def test_entering_the_current_room_changes_nothing():
    call()
    before = saved_bytes()
    result = call("enter", room="study_room")
    assert result["accepted"] and result["scene"] == "study_room" and result["message"] == ""
    assert saved_bytes() == before


def test_entering_after_an_ending_is_refused():
    call()
    for action in HELP:
        call("play", action=action)
    before = saved_bytes()
    result = call("enter", room="library")
    assert not result["accepted"] and result["ending"]["id"] == "impostor"
    assert saved_bytes() == before


@pytest.mark.parametrize("extra", [{"room": "cafeteria"}, {"room": 7}, {"room": None}, {"room": ["library"]},
                                   {}, {"room": "library", "state": {"scene": "auditorium"}}])
def test_enter_rejects_bad_rooms_and_extra_fields(extra):
    call()
    before = saved_bytes()
    with pytest.raises(ValueError):
        call("enter", **extra)
    assert saved_bytes() == before


def test_a_new_game_is_marked_fresh_until_something_is_saved():
    """The 3D scene starts the character outside only while the game is untouched."""
    assert call()["fresh"] is True
    assert call("enter", room="study_room")["fresh"] is True              # walking into the hub changes nothing
    assert call("enter", room="auditorium")["fresh"] is True              # a refused door changes nothing
    assert call("play", action="go_library")["fresh"] is False            # any accepted move ends it
    assert call(language="en")["fresh"] is False                          # and a resumed game is not fresh
    assert call("restart", confirmed=True)["fresh"] is True               # a restart makes it fresh again


def test_generated_pages_preserve_walkthrough_and_escape_script_data(monkeypatch):
    monkeypatch.setitem(page3d.EXTRA["pt"], "mission", "</script><script>alert(1)</script>")
    preview = page3d.build_page()
    playable = page3d.build_page(playable=True)
    assert '/play.js' not in preview and '/play.js' in playable
    assert "</script><script>alert(1)</script>" not in playable
    assert "\\u003c/script>" in playable


@pytest.fixture
def http_server():
    with server3d.make_server(0) as server:
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        yield f"http://127.0.0.1:{server.server_port}"
        server.shutdown(); thread.join()


def post(base, payload, origin=None):
    headers = {"Content-Type": "application/json"}
    if origin:
        headers["Origin"] = origin
    request = Request(base + "/api/command", data=json.dumps(payload).encode(), headers=headers)
    return urlopen(request)


def test_http_serves_only_screen_files_and_rejects_foreign_origin(http_server):
    assert urlopen(http_server).status == 200
    assert urlopen(http_server + "/play.js").status == 200
    for path in ["/db.py", "/data/campus3d.db", "/../story.py"]:
        with pytest.raises(HTTPError) as error:
            urlopen(http_server + path)
        assert error.value.code == 404
    with pytest.raises(HTTPError) as error:
        post(http_server, {"operation": "open", "language": "pt", "player": "maria"}, "https://example.com")
    assert error.value.code == 403
    assert db.load_game("maria") is None


def test_http_commands_save_and_resume_after_server_restart(http_server):
    payload = {"operation": "open", "language": "pt", "player": "maria"}
    with post(http_server, payload) as response:
        assert json.load(response)["scene"] == "study_room"
    with post(http_server, dict(payload, operation="play", action="open_drawer")) as response:
        assert len(json.load(response)["inventory"]) == 1
    # A new server instance and a new connection load the same SQLite file.
    with server3d.make_server(0) as second:
        thread = threading.Thread(target=second.serve_forever, daemon=True); thread.start()
        try:
            with post(f"http://127.0.0.1:{second.server_port}", payload) as response:
                assert json.load(response)["inventory"][0]["id"] == "usb_stick"
        finally:
            second.shutdown(); thread.join()
