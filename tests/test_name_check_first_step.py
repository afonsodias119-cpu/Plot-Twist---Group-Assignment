"""The name is checked where it is typed (specs/name-check-first-step.md)."""

import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
FOLDER = PROJECT / "prototypes" / "campus-3d"
sys.path.insert(0, str(FOLDER))

from campus_text import TEXT  # noqa: E402
from story import UI_TEXTS  # noqa: E402

PLAY = (FOLDER / "play.js").read_text(encoding="utf-8")
HTML = (FOLDER / "game3d.html").read_text(encoding="utf-8")
EMPTY_CHECK = "if (!name.value.trim()) { startError.textContent = ui().name_needed; name.focus(); return; }"


def test_next_checks_the_name_right_after_the_empty_check():
    start = PLAY.index("window.campusNext = () => {")
    body = PLAY[start:PLAY.index("};", start)]
    assert EMPTY_CHECK in body
    after = body[body.index(EMPTY_CHECK) + len(EMPTY_CHECK):]
    assert after.index("NAME_RULE.test(name.value.trim())") < after.index("goStep(")
    assert "startError.textContent = ui().name_invalid; name.focus(); return;" in after


def test_the_page_rule_is_the_servers_rule():
    assert r"const NAME_RULE = /^[\p{L}\p{N}_ -]{1,20}$/u;" in PLAY


def test_the_texts_are_the_servers_words():
    for language in ("en", "pt"):
        assert TEXT[language]["name_invalid"] == UI_TEXTS[language]["invalid_name"]


def test_the_typewriter_leaves_the_focus_in_a_field():
    start = HTML.index("function finish() {")
    body = HTML[start:HTML.index("function type(", start)]
    assert 'if (document.activeElement?.tagName !== "INPUT") $("accept").focus({ preventScroll: true });' in body
