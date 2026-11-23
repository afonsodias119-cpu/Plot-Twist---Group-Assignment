"""The library as a study hall, and Leonor coming with you (specs/library-study-hall.md)."""

import importlib
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "prototypes" / "campus-3d"))
TEXT = importlib.import_module("campus_text").TEXT
page3d = importlib.import_module("page3d")
PAGE = page3d.build_page(playable=True, inline=True)
HTML = (REPO / "prototypes" / "campus-3d" / "game3d.html").read_text(encoding="utf-8")


def test_leonor_says_she_is_coming_in_both_languages_right_after_she_agrees_to_help():
    for language in ("pt", "en"):
        line = TEXT[language]["leonor_follow"]
        assert line.strip() and line.count('"') == 2   # a description, then what she says between quotation marks
    assert 'if (action.id === "ask_for_help") { addSaid(ui().leonor_follow); speak(ui().leonor_follow, "leonor"); }' in PAGE


def test_leonor_has_a_seat_and_sits_only_at_home_and_not_walking():
    assert re.search(r'"Leonor", 0, "leonor"\);\nnpcs\[npcs\.length - 1\]\.userData\.seat = true;', HTML)
    assert "if (n.userData.seat && atHome && !n.userData.walking) { seatPose(n);" in HTML


def test_six_students_sit_with_a_book_or_a_laptop_each():
    block = HTML[HTML.index("const students = [];"):HTML.index("const USABLE = [")]
    rows = re.findall(r'\[\{ topColor: 0x[0-9a-f]+[^\]]*?\}, [\d.]+, -[\d.]+, (?:0|Math\.PI), "(book|laptop)"\]', block)
    assert len(rows) == 6 and set(rows) == {"book", "laptop"}
    assert "seatPose(p);" in block and "students.push(p);" in block
    assert "label(" not in block and "block(" not in block           # not people you talk to: no name tag, no box of their own


def test_the_old_table_is_gone_and_the_things_to_look_at_stay():
    assert "table(8.75, -7.6, 2.6, 1.2, oak);" not in HTML
    assert "table(7.2, -8.9, 2.4, 1.0, oak); table(10.6, -8.9, 2.4, 1.0, oak);" in HTML
    assert "rbox(0.04, 0.9, 1.4, 4.66, 1.0, -8.0," in HTML       # the noticeboard
    assert "block(6.0, -4.95, 0.9, 0.5);" in HTML                # the trolley of returned books
