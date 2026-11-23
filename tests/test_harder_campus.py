"""A harder campus: no list of missing clues, and a countdown (specs/harder-campus.md)."""

import importlib
import sys
from pathlib import Path

FOLDER = Path(__file__).resolve().parents[1] / "prototypes" / "campus-3d"
sys.path.insert(0, str(FOLDER))
campus = importlib.import_module("campus_game")
people = importlib.import_module("campus_people")
page3d = importlib.import_module("page3d")
TEXT = importlib.import_module("campus_text").TEXT

PLAYER = "hurry"

# (person, node the answer is in, node it leads to) for every answer that costs time
RUDE = {
    ("leonor", "start", "harsh"), ("leonor", "harsh", "closed"),
    ("tomas", "start", "hard"), ("tomas", "hard", "closed"),
    ("duarte", "start", "know"), ("duarte", "know", "closed"),
}


def call(operation="open", language="en", **extra):
    return campus.command(dict(operation=operation, language=language, player=PLAYER, **extra))


def costly_answers(language):
    return {(person, node, option["next"]): option["cost"]
            for person, data in people.PEOPLE[language].items()
            for node, line in data["nodes"].items()
            for option in line["options"] if "cost" in option}


# ---------- the door ----------

# Changed by specs/three-proofs.md ("Reviewed tests that change"): the door never refuses, so it has no note.
def test_the_door_does_not_list_the_missing_clues():
    call()
    result = call("enter", room="auditorium")
    assert result["accepted"] and result["message"] == ""
    for language in ("en", "pt"):
        assert "missing" not in TEXT[language] and "auditorium_note" not in TEXT[language]


# ---------- rude answers cost time ----------

def test_exactly_the_rude_answers_cost_five_minutes_in_both_languages():
    en, pt = costly_answers("en"), costly_answers("pt")
    assert en == pt
    assert set(en) == RUDE
    assert set(en.values()) == {5}


def test_talk_returns_the_cost_only_for_rude_answers():
    call()
    call("play", action="go_computer_lab")
    options = call("talk", npc="tomas", node="start")["options"]
    costs = {option["next"]: option.get("cost") for option in options}
    assert costs["hard"] == 5
    assert costs["kind"] is None and costs[None] is None


# ---------- countdown on the screen ----------

def test_the_countdown_texts_exist_in_both_languages():
    for language in ("en", "pt"):
        for key in ("time_aria", "time_penalty", "time_up_title", "time_up_text", "time_up_again"):
            assert TEXT[language][key].strip(), (language, key)
        assert "{n}" in TEXT[language]["time_penalty"]


def test_the_page_has_the_countdown_and_the_time_up_card():
    page = page3d.build_page(playable=True, inline=True)
    assert 'id="timeup-card"' in page and 'id="timeup-again"' in page
    js = (FOLDER / "play.js").read_text(encoding="utf-8")
    assert "const COUNTDOWN_MINUTES = 30" in js
    assert "plot-twist-time-left:" in js and "plot-twist-deadline:" not in js
    # the time goes down only while the game is on the screen, so a saved game can be continued later
    assert "const running = !current.ending && !document.hidden && !shell.hidden" in js
    assert "if (option.cost) penalize(option.cost)" in js
