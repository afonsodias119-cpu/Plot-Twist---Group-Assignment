"""Plot Twist — the screens (Streamlit).

This is the only file that uses Streamlit. It shows the screens, reads what the player
clicks and calls game.py. The rules are in logic.py and the saving in db.py
(see specs/base-game.md, section 6).

Streamlit runs this whole file again after every click. What must survive between runs is
kept in st.session_state: "player" (the name), "lang" (the language of the game), "message"
(the last result or error) and "confirming" (the New game question is open).
"""

import streamlit as st

import game
import logic
from story import LANGUAGES, STORIES, UI_TEXTS

MESSAGE_BOXES = {"success": st.success, "warning": st.warning, "error": st.error}


# ---------- what happens when the player clicks ----------

def set_message(kind, text):
    """Remember a message ("success", "warning" or "error") to show on the next run."""
    st.session_state["message"] = {"kind": kind, "text": text}


def back_to_start(text):
    """Forget the player and show the Start screen again, with an error message."""
    st.session_state["player"] = None
    st.session_state["lang"] = None
    st.session_state["confirming"] = False
    set_message("error", text)


def start_game():
    """Play button: start the game of the typed name, or continue it if it was saved."""
    language = st.session_state["language"]
    name = game.clean_name(st.session_state["player_name"])
    if name is None:
        set_message("error", UI_TEXTS[language]["invalid_name"])
        return
    result = game.open_game(name, language)
    st.session_state["player"] = name
    st.session_state["lang"] = result["language"]
    st.session_state["confirming"] = False
    sentence = "continued" if result["continued"] else "started"
    set_message("success", UI_TEXTS[result["language"]][sentence])


def take_action(action_id):
    """An action button: play it on the saved game and show what happened."""
    result = game.play(st.session_state["player"], action_id, st.session_state["lang"])
    st.session_state["confirming"] = False
    if result["reason"] == "no_game":
        back_to_start(result["message"])
    elif result["accepted"]:
        set_message("success", result["message"])
    else:
        set_message("warning", result["message"])


def ask_new_game():
    """New game button: ask for confirmation first. Nothing is written yet."""
    st.session_state["confirming"] = True
    st.session_state["message"] = None


def cancel_new_game():
    st.session_state["confirming"] = False


def confirm_new_game():
    """Yes button: replace the saved game with a new one (the language is kept)."""
    game.restart(st.session_state["player"])
    st.session_state["confirming"] = False
    st.session_state["message"] = None


# ---------- what is drawn ----------

def show_message():
    message = st.session_state["message"]
    if message and message["text"]:
        MESSAGE_BOXES[message["kind"]](message["text"])


def show_image(name):
    """Draw assets/<name>.jpg if the file exists. A missing picture draws nothing, never an error."""
    picture = game.image_file(name)
    if picture:
        st.image(picture, width="stretch")


def show_inventory(story, ui, state):
    st.subheader(ui["inventory"])
    if not state["inventory"]:
        st.write(ui["inventory_empty"])
    for item_id in state["inventory"]:
        picture = game.image_file(item_id)
        if picture:
            picture_column, name_column = st.columns([1, 5], vertical_alignment="center")
            picture_column.image(picture, width=80)
            name_column.write(story["items"][item_id])
        else:
            st.write(f"- {story['items'][item_id]}")


def show_new_game(ui):
    """The New game button, or its confirmation question while it is open."""
    if st.session_state["confirming"]:
        st.warning(ui["confirm_question"])
        st.button(ui["confirm_yes"], key="confirm_yes", on_click=confirm_new_game)
        st.button(ui["confirm_cancel"], key="confirm_cancel", on_click=cancel_new_game)
    else:
        st.button(ui["new_game"], key="new_game", on_click=ask_new_game)


def show_start():
    """Start screen: language, premise and the name box."""
    # The label has both languages, so it never changes and the choice is not reset.
    language = st.radio("Language / Língua", list(LANGUAGES), format_func=LANGUAGES.get, key="language", horizontal=True)
    ui = UI_TEXTS[language]
    st.title(ui["title"])
    show_image("cover")
    st.write(ui["premise"])
    st.write(ui["continue_hint"])
    show_message()
    with st.form("start"):
        st.text_input(ui["name_label"], key="player_name", max_chars=20)
        st.form_submit_button(ui["play"], key="play", on_click=start_game)


def show_game(state):
    """Scene screen while the story goes on, ending screen once it is over."""
    story = STORIES[st.session_state["lang"]]
    ui = UI_TEXTS[st.session_state["lang"]]
    st.title(ui["title"])

    if state["ending"] == "none":
        st.header(story["scenes"][state["scene"]]["title"])
        show_image(state["scene"])
        show_message()
        for paragraph in logic.scene_text(story, state):
            st.write(paragraph)
        show_inventory(story, ui, state)
        if not st.session_state["confirming"]:
            # Blocked actions are shown too: clicking one explains why it is blocked.
            for action in logic.available_actions(story, state):
                st.button(action["label"], key=f"action_{action['id']}", on_click=take_action, args=(action["id"],))
    else:
        ending = next(e for e in story["endings"] if e["id"] == state["ending"])
        st.header(ending["title"])
        show_image(f"ending_{state['ending']}")
        st.write(ending["text"])
        st.subheader(ui["the_end"])
        show_inventory(story, ui, state)
    show_new_game(ui)


# ---------- the page ----------

st.set_page_config(page_title="Plot Twist")
for key, value in {"player": None, "lang": None, "message": None, "confirming": False}.items():
    st.session_state.setdefault(key, value)

player = st.session_state["player"]
saved_state = game.load(player) if player else None
if player and saved_state is None:
    # The saved game disappeared or is broken: back to the Start screen, never an error page.
    back_to_start(STORIES[st.session_state["lang"]]["messages"]["no_game"])

if saved_state is None:
    show_start()
else:
    show_game(saved_state)
