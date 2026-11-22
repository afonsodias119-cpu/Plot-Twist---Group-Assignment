"""The USB stick is hidden in the mess of the table (specs/hidden-object-table.md)."""

import importlib
import re
import sys
from pathlib import Path

FOLDER = Path(__file__).resolve().parents[1] / "prototypes" / "campus-3d"
sys.path.insert(0, str(FOLDER))
search = importlib.import_module("campus_search")
page3d = importlib.import_module("page3d")
TEXT = importlib.import_module("campus_text").TEXT

TABLE_JS = (FOLDER / "table.js").read_text(encoding="utf-8")
PLAY_JS = (FOLDER / "play.js").read_text(encoding="utf-8")
GAME_HTML = (FOLDER / "game3d.html").read_text(encoding="utf-8")
LOOK_ALIKES = {"eraser", "gum", "lighter", "sd_card", "charger"}   # removed: they made no sense on the table


def drawn_kinds():
    """The kind of every object in the ITEMS list of table.js, in order."""
    items = TABLE_JS[TABLE_JS.index("const ITEMS = ["):TABLE_JS.index("];", TABLE_JS.index("const ITEMS = ["))]
    return re.findall(r'\["([a-z_]+)",', items)


def test_the_stick_is_one_of_the_objects_of_the_table():
    assert search.PEN_SPOT == "usb_stick" and search.PEN_SPOT in search.SPOTS


def test_the_old_places_of_the_room_are_gone():
    for old in ("drawer", "coat", "backpack", "books", "bin", "plant", "pizza"):
        assert old not in search.SPOTS


def test_every_kind_has_a_label_and_the_table_texts_exist_in_both_languages():
    for language in ("pt", "en"):
        assert set(TEXT[language]["spots"]) == set(search.SPOTS)
        for key in ("table_open", "table_title", "table_hint", "table_close"):
            assert TEXT[language][key].strip()


def test_every_kind_is_drawn_and_only_those_kinds():
    kinds = drawn_kinds()
    assert set(kinds) == set(search.SPOTS)
    assert kinds.count("usb_stick") == 1
    assert len(kinds) >= 40   # a real mess
    for kind in search.SPOTS:
        assert f"    {kind}: () =>" in TABLE_JS   # each kind has its own drawing


def test_there_are_no_objects_made_to_look_like_the_stick():
    assert not LOOK_ALIKES & set(search.SPOTS)
    assert not LOOK_ALIKES & set(drawn_kinds())


def test_the_stick_is_half_under_a_napkin():
    kinds = drawn_kinds()
    assert kinds[kinds.index("usb_stick") + 1] == "napkin"


def test_table_js_draws_but_knows_no_rules():
    for word in ("send(", "fetch(", "penalize", "SEARCH_TEXT", "found:"):
        assert word not in TABLE_JS


def test_the_page_carries_table_js():
    inline = page3d.build_page(playable=True, inline=True)
    assert "window.campusTable" in inline
    assert 'src="/table.js"' in page3d.build_page(playable=True)
    server = (FOLDER / "server3d.py").read_text(encoding="utf-8")
    assert '"/table.js": "text/javascript"' in server
    app = (FOLDER.parents[1] / "app_3d.py").read_text(encoding="utf-8")
    assert '"table.js"' in app


def test_the_side_panel_opens_the_table_instead_of_listing_places():
    assert "t.table_open" in PLAY_JS and "window.campusOpenTable()" in PLAY_JS
    assert "Object.entries(t.spots)" not in PLAY_JS


def test_in_3d_only_the_table_can_be_clicked_to_search():
    assert "spotGroup" not in GAME_HTML and "campus-found" not in GAME_HTML
    assert "window.campusOpenTable()" in GAME_HTML
    assert "raycaster.intersectObject(mess, true)" in GAME_HTML


def test_no_text_says_where_the_stick_is():
    for language in ("pt", "en"):
        texts = TEXT[language]
        assert "search_hint" not in texts and "search_title" not in texts
        hint = texts["table_hint"].lower()
        assert "1 minut" not in hint and "mesa" not in hint and "table" not in hint
    assert "t.search_hint" not in PLAY_JS and "t.search_title" not in PLAY_JS


def test_the_magnifier_is_a_picture_the_player_drags():
    assert '<use href="#table-content" class="lens-view"/>' in TABLE_JS and "LENS_ZOOM" in TABLE_JS
    assert '<g clip-path="url(#lens-clip)" pointer-events="none">' in TABLE_JS   # the glass lets clicks through
    assert 'class="lens-grab"' in TABLE_JS and 'class="lens-handle"' in TABLE_JS   # the ring and the handle are dragged
    assert 'id="table-lens"' not in TABLE_JS   # no button any more
    for language in ("pt", "en"):
        assert TEXT[language]["table_lens"].strip()


def test_objects_can_be_dragged_and_a_drag_is_not_a_click():
    assert 'view.addEventListener("pointerdown", down);' in TABLE_JS
    assert "if (was && was.item && !was.moving) pick(was.item);" in TABLE_JS   # only a press without moving is checked
    assert '.addEventListener("click", pick)' not in TABLE_JS


def test_the_floor_of_the_study_room_is_clear():
    study = GAME_HTML[GAME_HTML.index("// ---- The study room (specs/hidden-object-table.md)"):GAME_HTML.index("const mess = new THREE.Group();")]
    for thing in ("backpack", "books", "a bin", "papers on the floor"):
        assert thing not in study


def test_the_signs_of_the_3d_never_cover_the_windows():
    assert 'pointerEvents: "none", zIndex: "1" });' in GAME_HTML


def test_a_refused_door_never_moves_the_character_to_another_room():
    # From another room the walk to the auditorium goes through the study room (saved, as the reviewed
    # tests want); the 3D must keep the character by the door, not move it to the study room.
    assert "if (now.scene === state.scene || now.accepted === false) {" in GAME_HTML
    assert "state.room !== savedScene && !(entering && state.accepted === false)" in GAME_HTML
