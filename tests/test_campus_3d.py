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
server3d = importlib.import_module("server3d")
page3d = importlib.import_module("page3d")

SHORT = ["open_drawer", "go_computer_lab", "view_files", "go_study_room", "go_auditorium", "present_evidence"]
HELP = ["open_drawer", "go_print_shop", "request_copy", "go_study_room", "go_library", "ask_for_help", "go_study_room", "go_computer_lab", "view_files", "go_study_room", "go_auditorium", "present_evidence"]


def call(operation="open", language="pt", player="test detective", **extra):
    return campus.command(dict(operation=operation, language=language, player=player, **extra))


@pytest.mark.parametrize("language", ["en", "pt"])
@pytest.mark.parametrize("path,ending", [(SHORT, "stolen_credits"), (HELP, "impostor"), (["accuse" if a == "ask_for_help" else a for a in HELP], "stolen_credits")])
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
