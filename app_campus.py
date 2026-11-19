"""Plot Twist — PREVIEW of the campus visuals (specs/campus-visuals.md).

A copy of app.py with a new look, so the team can try it without changing app.py.
Run it next to the real game (both use the same saved games):
    uv run streamlit run app_campus.py --server.port 8502

What is new compared with app.py (search for "NEW" to find each part):
- style.css is loaded on every screen;
- the Start screen shows the campus at night (the cover is only the fallback);
- after Play, a short "entering the building" moment fades in and out by itself;
- in the study room, the ways to other rooms are door cards along a hallway;
- inventory items are small cards.
The rules, the buttons, their keys and the calls to game.py are the same as in app.py.

Streamlit runs this whole file again after every click. What must survive between runs is
kept in st.session_state: "player", "lang", "message", "confirming" (as in app.py) and
"entering" (NEW: the entering moment must be drawn on the next run).
"""

import base64
from pathlib import Path

import streamlit as st

import game
import logic
from campus_texts import CAMPUS_UI, TEASERS
from story import LANGUAGES, STORIES, UI_TEXTS

MESSAGE_BOXES = {"success": st.success, "warning": st.warning, "error": st.error}
STYLE_FILE = Path(__file__).resolve().parent / "style.css"  # NEW


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
    st.session_state["entering"] = True  # NEW: show the entering moment on the next run
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

def load_style():
    """NEW: put the CSS of style.css into the page. It only changes how things look."""
    css = STYLE_FILE.read_text(encoding="utf-8")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def show_message():
    message = st.session_state["message"]
    if message and message["text"]:
        MESSAGE_BOXES[message["kind"]](message["text"])


def show_image(name):
    """Draw assets/<name>.jpg if the file exists. A missing picture draws nothing, never an error.

    NEW: returns True when a picture was drawn, so a fallback can be written with "or".
    """
    picture = game.image_file(name)
    if picture:
        st.image(picture, width="stretch")
        return True
    return False


def image_as_data_url(name):
    """NEW: the picture as text that HTML can show ("data:image/jpeg;base64,..."), or None.

    HTML written with st.markdown cannot open files from the assets folder, so the bytes of
    the picture are turned into text (base64) and put straight into the page.
    """
    picture = game.image_file(name)
    if not picture:
        return None
    encoded = base64.b64encode(Path(picture).read_bytes()).decode("ascii")
    return f"data:image/jpeg;base64,{encoded}"


def show_entering(language):
    """NEW: the "entering the building" moment, drawn only on the run right after Play.

    It is one HTML block on top of the page. style.css (.entering) makes it fade in, stay
    and fade out by itself, and lets clicks go through it. Without entrance_hall.jpg it is
    just the text on a dark background.
    """
    if not st.session_state["entering"]:
        return
    st.session_state["entering"] = False  # so the next run does not draw it again
    picture = image_as_data_url("entrance_hall")
    picture_html = f'<img src="{picture}" alt="">' if picture else ""
    text = CAMPUS_UI[language]["entering"]
    st.markdown(f'<div class="entering">{picture_html}<p>{text}</p></div>', unsafe_allow_html=True)


def show_inventory(story, ui, state):
    st.subheader(ui["inventory"])
    if not state["inventory"]:
        st.write(ui["inventory_empty"])
    for item_id in state["inventory"]:
        # NEW: each item is a small card. The key gives the card a CSS class (st-key-item_...).
        with st.container(border=True, key=f"item_{item_id}"):
            picture = game.image_file(item_id)
            if picture:
                picture_column, name_column = st.columns([1, 5], vertical_alignment="center")
                picture_column.image(picture, width=80)
                name_column.write(story["items"][item_id])
            else:
                st.write(story["items"][item_id])


def show_door(story, language, action, room):
    """NEW: one door card: thumbnail, room name (with a padlock if locked), teaser and button.

    The button is the same action button as in app.py (same key, same take_action), so a
    locked door is still clickable and explains why it is locked.
    """
    locked = not action["allowed"]
    # The key becomes a CSS class, so style.css can draw locked doors differently.
    key = f"door_{room}_locked" if locked else f"door_{room}"
    with st.container(border=True, key=key):
        show_image(room)
        padlock = "🔒 " if locked else ""
        st.markdown(f"**{padlock}{story['scenes'][room]['title']}**")
        st.caption(TEASERS[language][room])
        st.button(action["label"], key=f"action_{action['id']}", on_click=take_action,
                  args=(action["id"],), width="stretch")


def show_actions(story, state, language):
    """NEW: the actions of the scene: plain buttons first, then the doors along the hallway.

    An action that goes to another room is a door, except going back to the starting room
    (the study room), which stays a plain button.
    """
    scene_actions = story["scenes"][state["scene"]]["actions"]
    start_scene = story["start"]["scene"]
    doors = []
    for action in logic.available_actions(story, state):
        room = scene_actions[action["id"]].get("go_to")
        if room and room != start_scene:
            doors.append((action, room))
        else:
            st.button(action["label"], key=f"action_{action['id']}", on_click=take_action, args=(action["id"],))

    if doors:
        st.subheader(CAMPUS_UI[language]["hallway"])
        # Two doors per row: wide enough for the thumbnail and the text.
        for first in range(0, len(doors), 2):
            columns = st.columns(2)
            for column, (action, room) in zip(columns, doors[first:first + 2]):
                with column:
                    show_door(story, language, action, room)


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
    show_image("campus_exterior") or show_image("cover")  # NEW: the campus at night, else the cover
    st.write(ui["premise"])
    st.write(ui["continue_hint"])
    show_message()
    with st.form("start"):
        st.text_input(ui["name_label"], key="player_name", max_chars=20)
        st.form_submit_button(ui["play"], key="play", on_click=start_game)


def show_game(state):
    """Scene screen while the story goes on, ending screen once it is over."""
    language = st.session_state["lang"]
    story = STORIES[language]
    ui = UI_TEXTS[language]
    show_entering(language)  # NEW
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
            show_actions(story, state, language)  # NEW: buttons and hallway
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
for key, value in {"player": None, "lang": None, "message": None, "confirming": False, "entering": False}.items():
    st.session_state.setdefault(key, value)
load_style()  # NEW

player = st.session_state["player"]
saved_state = game.load(player) if player else None
if player and saved_state is None:
    # The saved game disappeared or is broken: back to the Start screen, never an error page.
    back_to_start(STORIES[st.session_state["lang"]]["messages"]["no_game"])

if saved_state is None:
    show_start()
else:
    show_game(saved_state)
