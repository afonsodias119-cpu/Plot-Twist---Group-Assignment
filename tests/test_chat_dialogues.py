"""Chat-style conversations and room plaques (specs/chat-dialogues.md)."""

import importlib
import re
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

def test_room_signs_are_plaques_with_a_code_and_no_emoji():
    html = source("game3d.html")
    rooms = re.search(r"const ROOMS = \[(.*?)\];", html, re.S).group(1)
    assert len(re.findall(r'code: "0\.0[1-5]"', rooms)) == 5
    assert "${r.icon} ${SCENES[r.id].title}" not in html   # the old sign text with an emoji
    assert ".sign.room" in html
