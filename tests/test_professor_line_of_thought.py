"""The professor's one line of thought, and what to do when Duarte speaks (specs/professor-line-of-thought.md)."""

import importlib
import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
FOLDER = PROJECT / "prototypes" / "campus-3d"
sys.path.insert(0, str(FOLDER))
people = importlib.import_module("campus_people")
TEXT = importlib.import_module("campus_text").TEXT

PLAY_JS = (FOLDER / "play.js").read_text(encoding="utf-8")


def leads(language, node):
    """The lines the answers of one of the professor's lines lead to (None is a goodbye)."""
    return [option["next"] for option in people.PEOPLE[language]["professor"]["nodes"][node]["options"]]


def test_the_professor_follows_one_line_of_thought_in_both_languages():
    for language in ("en", "pt"):
        # start → list ("Five") → evidence ("only four") → proof ("I will bring proof"); his memory line stays.
        assert leads(language, "start") == ["list", "again", None], language
        assert leads(language, "list") == ["evidence"], language
        assert leads(language, "evidence") == ["proof"], language
        assert leads(language, "proof") == [None], language


def test_the_labels_say_the_steps():
    labels = {language: {node: [option["label"] for option in line["options"]]
                         for node, line in people.PEOPLE[language]["professor"]["nodes"].items()}
              for language in ("en", "pt")}
    assert labels["en"]["evidence"] == ["Say you will bring proof"]
    assert labels["pt"]["evidence"] == ["Dizer que vais trazer provas"]
    assert "Say you will bring proof" not in labels["en"]["start"]
    assert "Dizer que vais trazer provas" not in labels["pt"]["start"]


def test_show_evidence_is_only_on_his_first_line():
    # Changed by specs/select-the-proofs.md ("Reviewed tests that change"): the professor's first line offers "Show
    # evidence" (select the proofs) and "Ask how many members"; the story's own button is gone. Was: the
    # button "Present the evidence" only on `proof`.
    assert 'const professorWaits = line.npc === "professor" && line.node !== "start";' in PLAY_JS
    assert "const present = " not in PLAY_JS


def test_the_hearing_says_what_to_do_when_duarte_speaks():
    for language in ("en", "pt"):
        assert TEXT[language]["hearing_how"].strip(), language
    assert "Duarte" in TEXT["en"]["hearing_how"] and "Duarte" in TEXT["pt"]["hearing_how"]
    assert "t.hearing_how" in PLAY_JS
    # specs/hearing-show-evidence.md: the proofs are behind "Show evidence", as in every conversation.
    assert "replaceChildren(step, how, doubt, show, silent)" in PLAY_JS
