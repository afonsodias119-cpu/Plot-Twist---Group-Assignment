"""Leonor after she agrees to help (specs/leonor-after-help.md)."""

import importlib
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "prototypes" / "campus-3d"))
PLAY = (REPO / "prototypes" / "campus-3d" / "play.js").read_text(encoding="utf-8")
people = importlib.import_module("campus_people")


def test_the_page_knows_leonor_helps_from_the_followers():
    assert 'const leonorHelping = line.npc === "leonor" && (current?.followers?.ids || []).includes("leonor");' in PLAY


def test_she_has_nothing_more_to_be_asked():
    assert "if (leonorHelping) line = { ...line, options: [], actions: [] };" in PLAY
    assert "&& !(current && current.hearing) && !leonorHelping;" in PLAY   # and no "Show evidence"


def test_followers_include_leonor_only_after_she_chose_to_help():
    state = {"inventory": [], "flags": {"colleague_choice": None}}
    assert "leonor" not in people.followers(state)
    state["flags"]["colleague_choice"] = "help"
    assert "leonor" in people.followers(state)
