"""A cleaner and more intuitive interface (specs/cleaner-interface.md)."""

import importlib
import re
import sys
from pathlib import Path

FOLDER = Path(__file__).resolve().parents[1] / "prototypes" / "campus-3d"
sys.path.insert(0, str(FOLDER))
page3d = importlib.import_module("page3d")
campus_text = importlib.import_module("campus_text")

PLAY_JS = (FOLDER / "play.js").read_text(encoding="utf-8")
# Emojis and pictographs (the arrows and dashes used in normal text are below this range).
EMOJI = re.compile("[⌀-⏿☀-➿\U0001F000-\U0001FAFFℹ️]")


def top_bar():
    """The markup of the top bar of the game."""
    return PLAY_JS[PLAY_JS.index('<header class="case-bar">'):PLAY_JS.index("</header>")]


def test_the_group_label_does_not_repeat_that_there_are_four():
    # Changed by specs/combined-start-briefing.md ("Reviewed tests that change"): the group box is gone, so there is no
    # label to repeat it. Was: the label had no "four", "quatro" or "(".
    for texts in page3d.EXTRA.values():
        assert "group_label" not in texts


def test_the_menu_text_exists_in_both_languages():
    assert campus_text.TEXT["pt"]["menu"] and campus_text.TEXT["en"]["menu"]


def test_the_top_bar_has_no_emojis():
    assert not EMOJI.search(top_bar())
    labels = [line for line in PLAY_JS.splitlines()
              if re.search(r'\$\("(phone-open|menu-toggle|howto-open|torch-toggle|sound-toggle)"\)\.textContent', line)]
    # Changed by specs/rules-and-character.md: the voices follow the Sound button, so there is no separate voice item.
    assert len(labels) == 5
    assert not any(EMOJI.search(line) for line in labels)


def test_the_three_tools_are_inside_the_menu():
    bar = top_bar()
    menu = bar[bar.index('id="menu-list"'):]
    for tool in ("howto-open", "torch-toggle", "sound-toggle"):   # changed by specs/rules-and-character.md (was four, with the voices)
        assert f'id="{tool}"' in menu
    assert 'id="phone-open"' in bar and 'id="phone-open"' not in menu
    assert 'id="menu-toggle"' in bar and 'aria-expanded="false"' in bar


def test_the_menu_closes_on_a_click_outside_and_on_escape():
    assert '.closest(".tool-menu")) setMenu(false)' in PLAY_JS
    assert 'e.key === "Escape" && !$("menu-list").hidden' in PLAY_JS


def test_the_clue_list_does_not_say_where_the_clues_are():
    draw_todo = PLAY_JS[PLAY_JS.index("function drawTodo("):PLAY_JS.index("function drawTodo(") + 1200]
    assert "clue.room" not in draw_todo and "todo_where" not in PLAY_JS


def test_conversations_show_no_hearts():
    assert "talk-trust" not in PLAY_JS and "♥" not in PLAY_JS


def test_backspace_shows_the_whole_typed_text():
    html = (FOLDER / "game3d.html").read_text(encoding="utf-8")
    assert 'e.key !== "Backspace" || done' in html
    for texts in page3d.EXTRA.values():
        assert "Backspace" in texts["skip"]
