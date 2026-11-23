"""Hand over every proof at once, and the system says what is missing (specs/hand-over-the-proofs.md)."""

import importlib
import sys
from pathlib import Path

import pytest

PROJECT = Path(__file__).resolve().parents[1]
FOLDER = PROJECT / "prototypes" / "campus-3d"
sys.path.insert(0, str(FOLDER))
campus = importlib.import_module("campus_game")
case = importlib.import_module("campus_case")
TEXT = importlib.import_module("campus_text").TEXT
PLAY_JS = (FOLDER / "play.js").read_text(encoding="utf-8")


def call(operation="open", language="en", player="detective", **extra):
    return campus.command(dict(operation=operation, language=language, player=player, **extra))


def night(player="detective", language="en", backup=True, footage=True):
    """A night up to the auditorium with the USB stick, the photo, Leonor's help and the files; the backup
    and the recording only when asked."""
    call(language=language, player=player)
    for action in ("open_drawer", "go_print_shop", "request_copy", "go_study_room", "go_library", "ask_for_help",
                   "go_study_room", "go_computer_lab", "view_files") + (("save_backup",) if backup else ()):
        assert call("play", language, player, action=action)["accepted"], action
    if footage:
        assert call("footage", language, player, camera="computer_lab", minute=23 * 60 + 47)["footage"] is True
    call("enter", language, player, room="auditorium")


def hand_over(player="detective", language="en"):
    return call("hearing", language, player, answer="all")


def test_every_proof_closes_the_case():
    night()
    ended = hand_over()
    assert ended["accepted"] and ended["heard"] is True
    assert ended["ending"]["id"] == "full_case" and ended["hearing"]["doubts"] == 0


def test_a_missing_proof_is_only_a_warning_with_how_many(tmp_path):
    # specs/missing-proof-is-a-warning.md: the professor says how many proofs are missing, never which,
    # nothing is saved, and the night goes on.
    import db
    for language in ("en", "pt"):
        one = f"one {language}"
        night(one, language, footage=False)
        before = db.DB_PATH.read_bytes()
        warned = hand_over(one, language)
        assert not warned["accepted"] and warned["heard"] is False and warned["ending"] is None
        assert warned["message"] == TEXT[language]["hearing_short_one"]
        assert db.DB_PATH.read_bytes() == before
        for label in case.CASE_TEXT[language]["labels"].values():
            assert label not in warned["message"]
        # The night goes on: keep the recording, then hand everything over again.
        assert call("footage", language, one, camera="computer_lab", minute=23 * 60 + 47)["footage"] is True
        assert hand_over(one, language)["ending"]["id"] == "full_case"

        two = f"two {language}"
        night(two, language, backup=False, footage=False)
        warned = hand_over(two, language)
        assert warned["message"] == TEXT[language]["hearing_short_many"].replace("{n}", "2")


def test_handing_over_twice_or_before_the_auditorium_is_refused():
    call()
    refused = hand_over()
    assert not refused["accepted"] and refused["heard"] is False
    night("twice")
    hand_over("twice")
    again = hand_over("twice")
    assert not again["accepted"] and again["heard"] is False


def test_a_bad_answer_still_raises():
    night()
    with pytest.raises(ValueError):
        call("hearing", answer="everything")


def test_the_page_hands_everything_over_and_shows_the_warning():
    assert 'send("hearing", { answer: "all" })' in PLAY_JS
    assert 'if (!current.heard && current.message) { addHeard({ who: "professor", name: "Professor", text: current.message }); return; }' in PLAY_JS
