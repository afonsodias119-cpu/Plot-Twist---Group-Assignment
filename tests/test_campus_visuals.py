"""Checks for the campus visuals preview (specs/campus-visuals.md).

app_campus.py is a copy of app.py with the new look. The fixture below makes the helpers of
test_smoke.py (open_app, start_game, click) open app_campus.py instead of app.py, for every
test in this file.
"""

from pathlib import Path

import pytest

import test_smoke
from campus_texts import CAMPUS_UI, TEASERS
from story import STORIES, UI_TEXTS
from test_images import assets, image_count, make_image  # noqa: F401  (assets is a fixture)
from test_smoke import STORY, click, shown_text, start_game, open_app

PROJECT_FOLDER = Path(__file__).resolve().parent.parent
PREVIEW_FILE = str(PROJECT_FOLDER / "app_campus.py")
STYLE_FILE = PROJECT_FOLDER / "style.css"

ENTERING = CAMPUS_UI["en"]["entering"]
ROOMS = ["print_shop", "library", "computer_lab", "auditorium"]


@pytest.fixture(autouse=True)
def use_the_preview(monkeypatch):
    """Every app opened in this file is app_campus.py, not app.py."""
    monkeypatch.setattr(test_smoke, "APP_FILE", PREVIEW_FILE)


def times_shown(at, text):
    """How many paragraphs on the screen contain this text."""
    return sum(text in paragraph for paragraph in shown_text(at))


# ---------- The existing screen tests, run again on the preview ----------
# Phase 2 of the spec: delete these two imports when app_campus.py replaces app.py.
# pytest runs every test_ function it finds in this file, including imported ones,
# and the fixture above makes them open app_campus.py. Nothing in them is changed.

from test_smoke import (  # noqa: E402, F401
    test_accepted_click_shows_its_result,
    test_app_opens_on_an_empty_database,
    test_blocked_click_is_explained,
    test_click_from_an_old_tab_is_judged_against_the_saved_game,
    test_finished_game_shows_only_new_game,
    test_invalid_name_shows_an_error,
    test_language_choice_changes_the_texts,
    test_missing_save_returns_to_start,
    test_new_game_asks_first,
    test_new_name_starts_and_same_name_continues,
    test_returning_player_keeps_the_saved_language,
)
from test_images import (  # noqa: E402, F401
    test_inventory_shows_item_pictures,
    test_screens_work_without_any_image,
    test_start_scene_and_ending_show_their_image,
)


# ---------- Start screen and entering moment ----------

def test_start_screen_shows_the_exterior_instead_of_the_cover(assets):
    """The campus at night replaces the cover; the cover is only the fallback."""
    assert image_count(open_app()) == 0
    make_image(assets, "campus_exterior")
    assert image_count(open_app()) == 1
    make_image(assets, "cover")
    assert image_count(open_app()) == 1


def test_play_shows_the_entering_moment_once():
    """Right after Play the entering text is shown once, under the scene title; then it is gone."""
    at = open_app()
    assert times_shown(at, ENTERING) == 0
    start_game("ana", at=at)
    assert times_shown(at, ENTERING) == 1
    assert at.header[0].value == STORY["scenes"]["study_room"]["title"]
    click(at, "action_open_drawer")
    assert times_shown(at, ENTERING) == 0


def test_entering_moment_after_continuing_a_game():
    """Playing again with the same name also enters the building, in the saved language."""
    at = start_game("ana", "pt")
    click(at, "action_go_library")
    again = start_game("ana")  # the radio is on English, the saved game is in Portuguese
    assert times_shown(again, CAMPUS_UI["pt"]["entering"]) == 1
    assert again.header[0].value == STORIES["pt"]["scenes"]["library"]["title"]


def test_invalid_name_shows_no_entering_moment():
    """A refused name keeps the Start screen and does not enter the building."""
    at = start_game("<b>")
    assert "play" in test_smoke.button_keys(at)
    assert times_shown(at, ENTERING) == 0


# ---------- Hallway ----------

def test_study_room_shows_one_door_per_room(assets):
    """Each room has a door card with its thumbnail; the action buttons keep their keys."""
    for name in ["study_room"] + ROOMS:
        make_image(assets, name)
    at = start_game("ana")
    assert image_count(at) == 5  # the study room and four thumbnails
    keys = test_smoke.action_keys(at)
    for room in ROOMS:
        assert f"action_go_{room}" in keys
    assert "action_open_drawer" in keys


def test_back_to_the_study_room_stays_a_button(assets):
    """In the library the way back is a plain button, with no thumbnail of the study room."""
    make_image(assets, "study_room")
    make_image(assets, "library")
    at = start_game("ana")
    click(at, "action_go_library")
    assert image_count(at) == 1
    assert "action_go_study_room" in test_smoke.action_keys(at)


def test_locked_door_shows_a_padlock_until_it_opens():
    """The auditorium door is locked until the files are viewed; a click explains why."""
    padlock = f"🔒 {STORY['scenes']['auditorium']['title']}"
    at = start_game("ana")
    assert times_shown(at, padlock) == 1
    click(at, "action_go_auditorium")
    blocked = STORY["scenes"]["study_room"]["actions"]["go_auditorium"]["blocked_text"]
    assert [box.value for box in at.warning] == [blocked]

    for action_id in ["open_drawer", "go_computer_lab", "view_files", "go_study_room"]:
        click(at, f"action_{action_id}")
    assert times_shown(at, padlock) == 0
    click(at, "action_go_auditorium")
    assert at.header[0].value == STORY["scenes"]["auditorium"]["title"]


def test_every_scene_has_a_teaser_in_both_languages():
    """The new texts exist in both languages, for every scene, and each door shows its teaser."""
    assert set(TEASERS) == set(CAMPUS_UI) == set(UI_TEXTS)
    assert set(CAMPUS_UI["en"]) == set(CAMPUS_UI["pt"])
    for language, story in STORIES.items():
        assert set(TEASERS[language]) == set(story["scenes"])
        for text in list(TEASERS[language].values()) + list(CAMPUS_UI[language].values()):
            assert isinstance(text, str) and text.strip() != ""

    at = start_game("ana")
    for room in ROOMS:
        assert TEASERS["en"][room] in at.caption.values


# ---------- Look ----------

def test_style_file_is_loaded_on_every_screen():
    """style.css exists and the Start, Scene and Ending screens each include it once."""
    first_line = STYLE_FILE.read_text(encoding="utf-8").splitlines()[0]
    at = open_app()
    assert times_shown(at, first_line) == 1
    start_game("ana", at=at)
    assert times_shown(at, first_line) == 1
    for action_id in test_smoke.P_SHORT:
        click(at, f"action_{action_id}")
    assert at.header[0].value == STORY["endings"][-1]["title"]
    assert times_shown(at, first_line) == 1
