"""Checks for the phone map (specs/phone-map.md).

The map is drawn from game.campus_map, which only reads the saved game. The screen checks
reuse the helpers of tests/test_smoke.py.
"""

import copy

import game
import logic
from story import CAMPUS_MAP, MAP_LOCATION, STORIES, UI_TEXTS
from test_smoke import click, open_app, start_game

STORY = STORIES["en"]
UI = UI_TEXTS["en"]
P_SHORT = ["open_drawer", "go_computer_lab", "view_files", "go_study_room", "go_auditorium", "present_evidence"]


def play_path(path, story=STORY):
    state = logic.new_game(story)
    for action_id in path:
        result = logic.apply_action(story, state, action_id)
        assert result["accepted"], action_id
        state = result["state"]
    return state


def rooms(campus_map):
    """Every room of the map, row by row, without the empty cells."""
    return [cell for row in campus_map for cell in row if cell is not None]


def test_map_shows_every_scene_once():
    """Each scene is either a place on the map or shown on another room, never both, never twice."""
    placed = [cell for row in CAMPUS_MAP for cell in row if cell is not None]
    assert len(CAMPUS_MAP) == 3 and all(len(row) == 3 for row in CAMPUS_MAP)
    assert len(placed) == len(set(placed))
    assert set(placed) | set(MAP_LOCATION) == set(STORY["scenes"])
    assert not set(placed) & set(MAP_LOCATION)
    assert all(room in placed for room in MAP_LOCATION.values())


def test_new_game_is_in_the_study_room():
    """At the start only the study room is marked as "here"."""
    campus_map = game.campus_map("en", logic.new_game(STORY))
    assert [cell["id"] for cell in rooms(campus_map) if cell["here"]] == ["study_room"]
    assert [[cell and cell["id"] for cell in row] for row in campus_map] == CAMPUS_MAP


def test_the_chat_is_shown_in_the_computer_lab():
    """While reading the group chat, the player is shown in the computer lab."""
    state = play_path(P_SHORT[:3] + ["open_chat"])
    assert state["scene"] == "group_chat"
    assert [cell["id"] for cell in rooms(game.campus_map("en", state)) if cell["here"]] == ["computer_lab"]


def test_auditorium_is_locked_until_the_files_are_viewed():
    """Only the auditorium is locked at the start; viewing the files opens it."""
    locked_at_start = [cell["id"] for cell in rooms(game.campus_map("en", logic.new_game(STORY))) if cell["locked"]]
    assert locked_at_start == ["auditorium"]
    after_files = play_path(P_SHORT[:3])
    assert not [cell["id"] for cell in rooms(game.campus_map("en", after_files)) if cell["locked"]]


def test_map_uses_the_language_of_the_game():
    """Room names are the scene titles of the chosen language."""
    for language, story in STORIES.items():
        for cell in rooms(game.campus_map(language, logic.new_game(story))):
            assert cell["title"] == story["scenes"][cell["id"]]["title"]


def test_map_never_changes_the_game():
    """Drawing the map leaves the state and the story exactly as they were."""
    state = play_path(P_SHORT[:3] + ["open_chat"])
    state_before, story_before = copy.deepcopy(state), copy.deepcopy(STORIES)
    game.campus_map("en", state)
    assert state == state_before
    assert STORIES == story_before


def test_phone_map_is_on_the_scene_screen():
    """The scene screen has the phone panel, with the player's room marked."""
    at = start_game("ana")
    phone = [expander for expander in at.expander if expander.label == UI["phone"]]
    assert len(phone) == 1
    texts = [element.value for element in phone[0].markdown]
    here = [text for text in texts if "📍" in text]
    assert len(here) == 1 and STORY["scenes"]["study_room"]["title"] in here[0]
    assert any("🔒" in text and STORY["scenes"]["auditorium"]["title"] in text for text in texts)


def test_ending_screen_has_no_map():
    """Once the story is over, the phone panel is gone."""
    at = start_game("rui")
    for action_id in P_SHORT:
        click(at, f"action_{action_id}")
    assert not [expander for expander in at.expander if expander.label == UI["phone"]]
