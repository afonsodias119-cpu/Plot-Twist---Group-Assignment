"""The professor before the podium (specs/professor-before-podium.md)."""

import math
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
HTML = (REPO / "prototypes" / "campus-3d" / "game3d.html").read_text(encoding="utf-8")


def test_a_person_close_by_comes_before_the_things_to_look_at():
    assert "const someone = near !== null && !USABLE.some(o => o.id === near) && !followerList().ids.includes(near);" in HTML
    assert "if (someone || !finds.some(f => f.id === o.id)) continue;" in HTML


def test_the_podium_can_be_read_away_from_the_professor():
    podium = re.search(r'\{ id: "podium", x: (-?[\d.]+), z: (-?[\d.]+) \}', HTML)
    professor = re.search(r'placeNpc\(\{[^}]*\}, (-?[\d.]+), (-?[\d.]+), [^,]+, "Professor"', HTML)
    spot = (float(podium.group(1)), float(podium.group(2)))
    teacher = (float(professor.group(1)), float(professor.group(2)))
    assert math.dist(spot, teacher) > 2.4   # 2.4 m is how close a person must be to be talked to
