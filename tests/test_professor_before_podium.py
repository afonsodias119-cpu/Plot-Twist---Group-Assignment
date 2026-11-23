"""The professor, not the podium (specs/professor-before-podium.md)."""

import importlib
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "prototypes" / "campus-3d"))
HTML = (REPO / "prototypes" / "campus-3d" / "game3d.html").read_text(encoding="utf-8")
search = importlib.import_module("campus_search")


def test_the_auditorium_has_nothing_to_look_at():
    assert search.FINDS["auditorium"] == ()
    for language in ("en", "pt"):
        assert "podium" not in search.FIND_TEXT[language]
    assert 'id: "podium"' not in HTML


def test_a_person_close_by_comes_before_the_things_to_look_at():
    assert "const someone = near !== null && !USABLE.some(o => o.id === near) && !followerList().ids.includes(near);" in HTML
    assert "if (someone || !finds.some(f => f.id === o.id)) continue;" in HTML
