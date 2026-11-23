"""Screen checks for the base game (specs/base-game.md, section 7, "Screens").

Each test opens app.py with Streamlit's AppTest, clicks buttons like a player and checks
what is on the screen and what is saved. Every test starts from an empty database
(see tests/conftest.py). In these tests STORY means STORIES["en"] and UI means UI_TEXTS["en"].
"""

import sqlite3
from pathlib import Path

from streamlit.testing.v1 import AppTest

import db
import logic
from story import STORIES, UI_TEXTS

APP_FILE = str(Path(__file__).resolve().parent.parent / "app.py")

STORY = STORIES["en"]
UI = UI_TEXTS["en"]

# Changed by specs/computer-lab-backup.md ("Reviewed tests that change"): the backup is saved after the files.
P_SHORT = ["open_drawer", "go_computer_lab", "view_files", "save_backup", "go_study_room", "go_auditorium", "present_evidence"]


# ---------- helpers ----------

def open_app():
    """A new browser session: opens app.py on the Start screen."""
    at = AppTest.from_file(APP_FILE, default_timeout=10).run()
    assert not at.exception
    return at


def start_game(name, language="en", at=None):
    """On the Start screen, choose a language, type the name and click Play."""
    at = at or open_app()
    if language != "en":
        at.radio(key="language").set_value(language).run()
    at.text_input(key="player_name").set_value(name)
    at.button(key="play").click().run()
    assert not at.exception
    return at


def click(at, key):
    """Click the button with this key and run the app again."""
    at.button(key=key).click().run()
    assert not at.exception
    return at


def button_keys(at):
    return [button.key for button in at.button]


def action_keys(at):
    return [key for key in button_keys(at) if key.startswith("action_")]


def shown_text(at):
    """Every paragraph written with st.write or st.markdown."""
    return [element.value for element in at.markdown]


def count_rows():
    db.init_db()
    connection = sqlite3.connect(db.DB_PATH)
    rows = connection.execute("SELECT COUNT(*) FROM games").fetchone()[0]
    connection.close()
    return rows


# ---------- Screens ----------

def test_app_opens_on_an_empty_database():
    """The Start screen shows the language choice (English) and the Play button."""
    at = open_app()
    assert at.radio(key="language").value == "en"
    assert "play" in button_keys(at)


def test_language_choice_changes_the_texts():
    """Choosing Português changes the Start screen and the game; English players see English."""
    at = open_app()
    at.radio(key="language").set_value("pt").run()
    assert at.title[0].value == UI_TEXTS["pt"]["title"]
    assert UI_TEXTS["pt"]["premise"] in shown_text(at)
    assert at.button(key="play").label == UI_TEXTS["pt"]["play"]

    start_game("ana", "pt", at)
    pt_story = STORIES["pt"]
    assert at.header[0].value == pt_story["scenes"]["study_room"]["title"]
    labels = {button.key: button.label for button in at.button}
    assert labels["action_open_drawer"] == pt_story["scenes"]["study_room"]["actions"]["open_drawer"]["label"]

    at = start_game("rui", "en")
    assert at.header[0].value == STORY["scenes"]["study_room"]["title"]


def test_returning_player_keeps_the_saved_language():
    """Brief A4: a player who started in Portuguese continues in Portuguese, whatever the radio shows."""
    at = start_game("ana", "pt")
    click(at, "action_open_drawer")

    again = start_game("ana")  # a new session, language left on the default English
    assert [box.value for box in again.success] == [UI_TEXTS["pt"]["continued"]]
    assert again.header[0].value == STORIES["pt"]["scenes"]["study_room"]["title"]
    assert "action_open_drawer" not in action_keys(again)
    assert STORIES["pt"]["items"]["usb_stick"] in "\n".join(shown_text(again))


def test_invalid_name_shows_an_error():
    """A name with markup gets one error, keeps the Start screen and saves nothing."""
    at = start_game("<b>")
    assert [box.value for box in at.error] == [UI["invalid_name"]]
    assert "play" in button_keys(at)
    assert count_rows() == 0


def test_new_name_starts_and_same_name_continues():
    """A new name starts a game; the same name later continues it, without the item already taken."""
    at = start_game("ana")
    assert [box.value for box in at.success] == [UI["started"]]
    click(at, "action_open_drawer")

    again = start_game("ana")
    assert [box.value for box in again.success] == [UI["continued"]]
    assert "action_open_drawer" not in action_keys(again)
    assert STORY["items"]["usb_stick"] in "\n".join(shown_text(again))


def test_missing_save_returns_to_start():
    """If the saved game disappears, the next click goes back to the Start screen with an error."""
    at = start_game("ana")
    connection = sqlite3.connect(db.DB_PATH)
    connection.execute("DELETE FROM games WHERE player = ?", ("ana",))
    connection.commit()
    connection.close()

    click(at, "action_open_drawer")
    assert "play" in button_keys(at)
    assert len(at.error) == 1


def test_accepted_click_shows_its_result():
    """An accepted action shows its result text once, and its button is gone."""
    at = start_game("ana")
    click(at, "action_open_drawer")
    expected = STORY["scenes"]["study_room"]["actions"]["open_drawer"]["result_text"]
    assert [box.value for box in at.success] == [expected]
    assert "action_open_drawer" not in action_keys(at)


def test_blocked_click_is_explained():
    """A blocked action is shown; clicking it explains why and leaves the scene as it was."""
    at = start_game("ana")
    # Changed by specs/three-proofs.md ("Reviewed tests that change"): the auditorium always opens, so the
    # blocked action is asking Leonor for help without the photo.
    click(at, "action_go_library")
    click(at, "action_ask_for_help")
    expected = STORY["scenes"]["library"]["actions"]["ask_for_help"]["blocked_text"]
    assert [box.value for box in at.warning] == [expected]
    assert at.header[0].value == STORY["scenes"]["library"]["title"]


def test_new_game_asks_first():
    """New game asks for confirmation; Cancel keeps the progress, Yes starts again."""
    at = start_game("ana")
    click(at, "action_open_drawer")

    click(at, "new_game")
    assert "confirm_yes" in button_keys(at)
    assert "confirm_cancel" in button_keys(at)
    assert action_keys(at) == []

    click(at, "confirm_cancel")
    assert db.load_game("ana")["inventory"] == ["usb_stick"]

    click(at, "new_game")
    click(at, "confirm_yes")
    assert db.load_game("ana") == logic.new_game(STORY)
    assert "action_open_drawer" in action_keys(at)


def test_finished_game_shows_only_new_game():
    """After an ending the screen shows its title and only the New game button."""
    at = start_game("ana")
    for action_id in P_SHORT:
        click(at, f"action_{action_id}")
    ending = STORY["endings"][-1]
    assert at.header[0].value == ending["title"]
    assert action_keys(at) == []
    assert "new_game" in button_keys(at)


def test_click_from_an_old_tab_is_judged_against_the_saved_game():
    """Two tabs, one player: a click on a button that is already out of date changes nothing."""
    first = start_game("ana")
    second = start_game("ana")
    click(second, "action_open_drawer")

    click(first, "action_open_drawer")
    assert len(first.warning) == 1
    assert db.load_game("ana")["inventory"] == ["usb_stick"]
