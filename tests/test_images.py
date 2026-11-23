"""Checks for the scene images and the theme (specs/scene-images.md).

A fixture points game.ASSETS_DIR at a throwaway folder, so no test depends on the real
pictures in assets/. The screen helpers come from test_smoke.py.
"""

import tomllib
from pathlib import Path

import pytest
from PIL import Image

import game
from test_smoke import P_SHORT, click, open_app, start_game

PROJECT_FOLDER = Path(__file__).resolve().parent.parent


# ---------- helpers ----------

@pytest.fixture
def assets(tmp_path, monkeypatch):
    """An empty assets folder that game.image_file will use."""
    folder = tmp_path / "assets"
    folder.mkdir()
    monkeypatch.setattr(game, "ASSETS_DIR", folder)
    return folder


def make_image(folder, name):
    """Save a tiny real JPG as <name>.jpg."""
    Image.new("RGB", (8, 8), "navy").save(folder / f"{name}.jpg")


def image_count(at):
    """How many pictures are on the screen."""
    return len(at.get("image"))


# ---------- Images ----------

def test_image_file_returns_the_file_when_it_exists(assets):
    """The path of an existing picture comes back as text; a missing one gives None."""
    make_image(assets, "study_room")
    assert game.image_file("study_room") == str(assets / "study_room.jpg")
    assert game.image_file("library") is None


def test_image_file_refuses_names_that_are_not_ids(assets, tmp_path):
    """Only lower-case ids are accepted, even if a file exists one folder up."""
    make_image(assets, "study_room")
    make_image(tmp_path, "secret")
    for name in ["../secret", "..\\secret", "a/b", "Study_Room", "study room", "", None, 7]:
        assert game.image_file(name) is None, name


def test_screens_work_without_any_image(assets):
    """With no picture at all, every screen opens and plays, and no image is shown."""
    at = open_app()
    assert image_count(at) == 0
    start_game("ana", at=at)
    assert image_count(at) == 0
    click(at, "action_open_drawer")
    assert image_count(at) == 0
    for action_id in P_SHORT[1:]:
        click(at, f"action_{action_id}")
    assert action_ids_gone(at)
    assert image_count(at) == 0


def action_ids_gone(at):
    """True on the ending screen: no action buttons are left."""
    return not [button.key for button in at.button if button.key.startswith("action_")]


def test_start_scene_and_ending_show_their_image(assets):
    """The Start screen shows the cover, each scene its own picture, the ending its picture."""
    for name in ["cover", "study_room", "ending_stolen_credits"]:
        make_image(assets, name)

    at = open_app()
    assert image_count(at) == 1  # the cover

    start_game("ana", at=at)
    assert image_count(at) == 1  # the study room
    click(at, "action_go_library")
    assert image_count(at) == 0  # the library has no picture here
    click(at, "action_go_study_room")
    assert image_count(at) == 1

    for action_id in ["open_drawer", "go_computer_lab", "view_files", "save_backup", "go_study_room", "go_auditorium", "present_evidence"]:   # specs/computer-lab-backup.md
        click(at, f"action_{action_id}")
    assert image_count(at) == 1  # the ending of this game: stolen_credits


def test_inventory_shows_item_pictures(assets):
    """Holding the USB stick, the screen shows the scene picture and the item picture."""
    make_image(assets, "study_room")
    make_image(assets, "usb_stick")
    at = start_game("ana")
    assert image_count(at) == 1
    click(at, "action_open_drawer")
    assert image_count(at) == 2


def test_theme_file_is_a_dark_theme():
    """.streamlit/config.toml can be read and sets a dark theme with an accent colour."""
    config_file = PROJECT_FOLDER / ".streamlit" / "config.toml"
    config = tomllib.loads(config_file.read_text(encoding="utf-8"))
    assert config["theme"]["base"] == "dark"
    assert config["theme"]["primaryColor"]
