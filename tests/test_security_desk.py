"""The security desk: a guard, five cables and last night's recordings (specs/security-desk.md)."""

import importlib
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "prototypes" / "campus-3d"))
TEXT = importlib.import_module("campus_text").TEXT
page3d = importlib.import_module("page3d")
PAGE = page3d.build_page(playable=True, inline=True)
CSS = (REPO / "prototypes" / "campus-3d" / "play.css").read_text(encoding="utf-8")
HTML = (REPO / "prototypes" / "campus-3d" / "game3d.html").read_text(encoding="utf-8")
ROOMS = ("print_shop", "study_room", "library", "computer_lab", "auditorium")
CAMERAS = ("entrance",) + ROOMS


def section():
    start = PAGE.index("// ---------- the security desk: a guard, five cables and the cameras")
    return PAGE[start:PAGE.index("// ---------- the phone: a map")]


def test_the_texts_exist_in_both_languages_with_the_same_keys():
    pt, en = TEXT["pt"]["security"], TEXT["en"]["security"]
    assert set(pt) == set(en)
    assert all(isinstance(v, str) and v.strip() for v in list(pt.values()) + list(en.values()))
    for room in ROOMS:
        assert pt[f"cable_{room}"] and en[f"cable_{room}"]
    for camera in CAMERAS:
        assert pt[f"cctv_{camera}"] and en[f"cctv_{camera}"]


def building_centres():
    """The centre of each room in the 3D building: x to the right, z down (above the corridor is a smaller z)."""
    found = {}
    for match in re.finditer(r'\{ id: "(\w+)",[^}]*?minX: (-?[\d.]+),\s*maxX: (-?[\d.]+),\s*minZ: (-?[\d.]+)', HTML):
        if match.group(1) in ROOMS:
            found[match.group(1)] = ((float(match.group(2)) + float(match.group(3))) / 2, float(match.group(4)))
    return found


def test_the_monitor_ports_are_placed_like_the_rooms_of_the_3d_building():
    """The player works the cables out from where the rooms are: the plan on the screen must match the 3D building."""
    centres = building_centres()
    ports = {m.group(1): (int(m.group(2)), int(m.group(3))) for m in re.finditer(r'\{ room: "(\w+)", x: (\d+), y: (\d+) \}', PAGE)}
    assert set(centres) == set(ROOMS) and set(ports) == set(ROOMS)
    for first in ROOMS:
        for second in ROOMS:
            if first == second:
                continue
            # above or below the corridor
            assert (centres[first][1] < centres[second][1]) == (ports[first][1] < ports[second][1]), (first, second)
            # to the left or to the right, for rooms on the same side of the corridor
            if (centres[first][1] < 0) == (centres[second][1] < 0):
                assert (centres[first][0] < centres[second][0]) == (ports[first][0] < ports[second][0]), (first, second)


def test_only_the_photo_or_the_old_files_convince_the_guard_and_a_wrong_card_costs_time():
    code = section()
    assert 'card.id === "original_photo" || card.id === "files"' in code
    assert "penalize(1)" in code and "cost: 2" in code        # a wrong card 1 minute, a rude demand 2


def test_the_guard_and_the_recordings_never_call_the_server():
    code = section()
    for call in ("request(", "send(", "fetch(", "campusBridge"):
        assert call not in code, call


def test_what_is_read_from_the_browser_must_be_exactly_true_and_a_new_game_forgets_it():
    for field in ("convinced", "wired", "footage"):
        assert f"saved.{field} === true" in PAGE
    assert "localStorage.removeItem(securityKey())" in PAGE


def test_the_page_has_the_desk_the_cables_and_the_recordings():
    for needle in ("guardStep", "guardMenu", "WIRE_PORTS", "drawWires", "drawCctvFrame", "campusFigure", "campusDeskPower",
                   "plot-twist-security", "deskScreens", 'near = "guard"', '"José"', "novaLetters"):
        assert needle in PAGE, needle
    assert ".wires-dialog.sparks" in CSS and ".cctv-dialog" in CSS


def test_the_hooded_figure_is_seen_from_behind_and_the_proof_goes_to_the_diary():
    code = section()
    assert "Math.PI" in code and "saveDiary(t.cctv_diary_title, t.cctv_proof)" in code
    assert "23 * 60 + 46, 23 * 60 + 49" in code        # the proof is in the minutes around 23:47


def test_the_guard_talks_in_the_same_card_as_everybody_else():
    """José is drawn by showLine like the other people: the same bubbles, the same "Show evidence" and the same answers."""
    assert 'id="guard-card"' not in PAGE and "campusGuardOpen" not in PAGE and "openGuard" not in PAGE
    code = section()
    assert "showLine(guardLine(" in code and "addBubble(" in code and "showTyping()" in code
    assert 'if (npc === "guard") { guardStep(node); return; }' in PAGE          # the ordinary talk hands him his own lines
    assert 'if (line.npc === "guard") { guardShown(card); return; }' in PAGE   # "Show evidence" works on him
    assert 'talking !== "guard" && !state.ending' in PAGE                       # the schedule never sends him home


def test_the_guard_is_jose_in_both_languages_has_a_voice_and_the_uniform_and_counter_are_in_the_scene():
    assert TEXT["pt"]["security"]["guard_name"] == "José" and TEXT["en"]["security"]["guard_name"] == "José"
    assert "Anselmo" not in PAGE
    assert 'guard: ["m"' in PAGE                                               # a voice of his own
    for needle in ("cap: 0x14233a", "badge: 0xd4a650", "belt: true", "epaulettes: 0xd4a650", "if (o.cap)"):
        assert needle in PAGE, needle
    # the counter copies the letters of the big sign, small and black
    assert "novaLetters(cx," in PAGE and "mat(0x15171b" in PAGE
