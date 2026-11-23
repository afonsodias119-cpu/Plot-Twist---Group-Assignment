"""A lived-in study room (specs/study-room-detail.md)."""

from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
HTML = (REPO / "prototypes" / "campus-3d" / "game3d.html").read_text(encoding="utf-8")
START = "// A lived-in study room (specs/study-room-detail.md)"
BLOCK = HTML[HTML.index(START):HTML.index("// ---- The study room (specs/hidden-object-table.md)")]


def test_the_new_furniture_comes_before_the_table_that_is_searched():
    assert HTML.index(START) < HTML.index("const mess = new THREE.Group();")


def test_every_piece_of_furniture_is_there():
    for comment in ("a low cabinet", "the printer", "a tray of paper", "const cork", "student lockers", "the seat",
                    "the coffee table", "a floor lamp", "const poster", "const clockFace", "a water cooler",
                    "a small round table", "a coat stand", "two radiators"):
        assert comment in BLOCK, comment


def test_the_big_pieces_cannot_be_walked_through():
    for box in ("block(-4.13, -9.0, 0.45, 3.0);", "block(-4.13, -6.55, 0.45, 1.5);", "block(3.98, -9.5, 0.85, 2.0);",
                "block(2.95, -9.5, 0.6, 1.0);", "block(4.0, -8.2, 0.35, 0.35);", "block(4.1, -4.6, 0.4, 0.4);",
                "block(-2.6, -5.4, 0.85, 0.85);", "block(-3.95, -3.75, 0.45, 0.45);"):
        assert box in BLOCK, box


def test_no_new_light_and_nothing_new_to_search():
    assert "lamp(" not in BLOCK.replace("floor lamp", "")
    assert "mess" not in BLOCK
