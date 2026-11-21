"""The secret ending and the ending screen (specs/fifth-element-ending.md)."""

import importlib
import sys
from pathlib import Path

import pytest

import logic
from story import STORIES

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "prototypes" / "campus-3d"))
campus_text = importlib.import_module("campus_text")
page3d = importlib.import_module("page3d")

TO_THE_CHAT = ["open_drawer", "go_print_shop", "request_copy", "go_study_room", "go_library", "ask_for_help",
               "go_study_room", "go_computer_lab", "view_files", "open_chat"]
TO_THE_END = ["go_computer_lab", "go_study_room", "go_auditorium", "present_evidence"]


def play(story, actions):
    state = logic.new_game(story)
    for action in actions:
        result = logic.apply_action(story, state, action)
        assert result["accepted"], action
        state = result["state"]
    return state


def flags(*numbers):
    return [f"flag_{n}" for n in numbers]


@pytest.mark.parametrize("language", ["en", "pt"])
def test_flagging_every_message_reaches_the_fifth_element(language):
    assert play(STORIES[language], TO_THE_CHAT + flags(1, 2, 3, 4, 5) + TO_THE_END)["ending"] == "fifth_element"


@pytest.mark.parametrize("language", ["en", "pt"])
def test_the_secret_ending_does_not_need_leonors_help(language):
    path = ["accuse" if a == "ask_for_help" else a for a in TO_THE_CHAT] + flags(1, 2, 3, 4, 5) + TO_THE_END
    assert play(STORIES[language], path)["ending"] == "fifth_element"


@pytest.mark.parametrize("flagged,ending", [((1, 2, 3, 4), "impostor"), ((2, 4, 5), "full_case"), ((), "impostor"),
                                            ((1, 3), "impostor")])
def test_anything_less_than_all_five_does_not_reach_it(flagged, ending):
    assert play(STORIES["en"], TO_THE_CHAT + flags(*flagged) + TO_THE_END)["ending"] == ending


@pytest.mark.parametrize("language", ["en", "pt"])
def test_it_is_first_and_the_last_ending_is_still_the_catch_all(language):
    endings = STORIES[language]["endings"]
    assert endings[0]["id"] == "fifth_element" and endings[-1]["when"] == {}
    assert endings[0]["text"].strip() and endings[0]["title"].strip()


def test_every_ending_has_a_stamp_in_both_languages():
    for language in ("en", "pt"):
        for ending in STORIES[language]["endings"]:
            assert campus_text.TEXT[language]["stamps"][ending["id"]].strip()


def test_the_page_has_the_ending_screen_and_the_buttons():
    page = page3d.build_page(playable=True, inline=True)
    for needle in ('id="ending-card"', 'id="ending-again"', 'id="ending-hide"', "showEnding", "fifth_element"):
        assert needle in page


def test_the_character_is_put_outside_only_at_the_start_of_a_game_or_after_a_restart():
    """Walking back to an untouched study room must not throw the character out again (it looks like a new game)."""
    page = page3d.build_page(playable=True, inline=True)
    assert "placedOutside" in page and "campus-restarted" in page and "wasFresh" not in page
