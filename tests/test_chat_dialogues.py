"""Chat-style conversations and room plaques (specs/chat-dialogues.md)."""

import importlib
import sys
from pathlib import Path

FOLDER = Path(__file__).resolve().parents[1] / "prototypes" / "campus-3d"
sys.path.insert(0, str(FOLDER))
people = importlib.import_module("campus_people")
campus_text = importlib.import_module("campus_text")
page3d = importlib.import_module("page3d")

ASK_SOMETHING_ELSE = {"ask something else", "perguntar outra coisa"}


def source(name):
    return (FOLDER / name).read_text(encoding="utf-8")


# ---------- no "Ask something else" ----------

def test_no_answer_asks_something_else():
    for language in ("en", "pt"):
        for person, data in people.PEOPLE[language].items():
            for node, line in data["nodes"].items():
                for option in line["options"]:
                    assert option["label"].lower() not in ASK_SOMETHING_ELSE, (language, person, node)


def test_every_line_still_offers_an_answer():
    for language in ("en", "pt"):
        for data in people.PEOPLE[language].values():
            for line in data["nodes"].values():
                assert line["options"]


def test_after_an_action_the_conversation_does_not_offer_to_continue():
    for language in ("en", "pt"):
        assert "talk_continue" not in campus_text.TEXT[language]
    assert "talk_continue" not in source("play.js")


# ---------- chat bubbles ----------

def test_the_conversation_is_a_message_log_with_bubbles():
    page = page3d.build_page(playable=True, inline=True)
    assert 'id="talk-log"' in page and 'id="talk-avatar"' in page
    css = source("play.css")
    for rule in (".bubble.them", ".bubble.me", ".bubble.typing", ".chat-replies"):
        assert rule in css, rule


# ---------- room plaques ----------

def test_room_signs_are_plaques_with_only_the_name():
    html = source("game3d.html")
    assert 'r.sign = label(SCENES[r.id].title, cx, 2.6, doorZ, "room");' in html   # the name, no emoji, no number
    assert "${r.icon} ${SCENES[r.id].title}" not in html and "data-code" not in html
    assert ".sign.room" in html


def test_computer_12_has_no_label():
    assert 'label("💻 12"' not in source("game3d.html")


# ---------- only what is said goes in a bubble ----------

def test_lines_are_split_into_speech_bubbles_and_narration():
    js = source("play.js")
    assert "function partsOf(text)" in js and "function addSaid(text)" in js
    assert "addSaid(line.text)" in js                      # every line of a person goes through the split
    assert "quotesOf = text => partsOf(text)" in js        # the voices use the same rule
    assert ".narration" in source("play.css")


def test_the_scene_description_is_hidden_outside_the_text_mode():
    assert "body:not(.text-mode) #scene-paragraphs { display: none; }" in source("play.css")


# ---------- only the people of the group have names ----------

def test_the_print_shop_clerk_has_no_name():
    assert people.PEOPLE["en"]["amelia"]["name"] == "Print shop clerk"
    assert people.PEOPLE["pt"]["amelia"]["name"] == "Funcionária da reprografia"
    html = source("game3d.html")
    assert "Amélia" not in html and 'const CLERK_LABEL = { pt: "Funcionária da reprografia", en: "Print shop clerk" };' in html
