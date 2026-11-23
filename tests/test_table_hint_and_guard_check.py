"""The table note, and José checks what you want to see (specs/table-hint-and-guard-check.md)."""

import importlib
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
FOLDER = REPO / "prototypes" / "campus-3d"
sys.path.insert(0, str(FOLDER))
TEXT = importlib.import_module("campus_text").TEXT
PLAY = (FOLDER / "play.js").read_text(encoding="utf-8")
HTML = (FOLDER / "game3d.html").read_text(encoding="utf-8")


def test_the_texts_exist_in_both_languages():
    for language in ("pt", "en"):
        t = TEXT[language]
        assert t["press_table"].strip() and "K" in t["press_table"], language
        assert "23:47" in t["security"]["confirm"], language
        assert t["security"]["opt_yes"].strip(), language


def test_the_table_is_near_only_while_searching_and_within_one_metre():
    assert "if (canSearch()) {" in HTML
    assert 'if (d < 1 && d < nearDistance) { nearDistance = d; near = "table"; }' in HTML


def test_k_opens_the_table():
    assert 'const sentence = table ? t.press_table' in PLAY
    assert 'else if (window.campusNear === "table") window.campusOpenTable();' in PLAY


def test_jose_asks_before_the_recordings():
    assert 'if (state.wired) return [{ label: t.opt_watch, next: "confirm" }];' in PLAY
    assert ': node === "confirm" ? [{ label: t.opt_yes, next: "watch" }] : [];' in PLAY
    assert 'if (state.footage) return [{ label: t.opt_rewatch, next: "watch" }];' in PLAY   # watching again: no question
