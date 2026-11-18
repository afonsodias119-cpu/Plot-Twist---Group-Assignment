"""Plot Twist — one turn of the game: load the save, ask the rules, save if accepted.

The screens (app.py) call these functions. The rules are in logic.py and the saving
is in db.py. See specs/base-game.md, section 5.
"""

import re
from pathlib import Path

import db
import logic
from story import LANGUAGES, STORIES

DEFAULT_LANGUAGE = "en"

# 1 to 20 characters: letters (accented ones too), digits, space, "-" and "_".
NAME_PATTERN = re.compile(r"[\w -]{1,20}")

# The illustrations. Read every time image_file runs, so the tests can point it elsewhere.
ASSETS_DIR = Path(__file__).resolve().parent / "assets"

# An image name is a story id: lower-case letters, digits and "_" only.
IMAGE_NAME_PATTERN = re.compile(r"[a-z0-9_]+")


def clean_name(text) -> str | None:
    """The name trimmed and in lower case, or None if it is not a valid name."""
    if not isinstance(text, str):
        return None
    name = text.strip().lower()
    return name if NAME_PATTERN.fullmatch(name) else None


def _language_or_default(language) -> str:
    """The language if the game has it, otherwise the default."""
    return language if language in LANGUAGES else DEFAULT_LANGUAGE


def load(player: str) -> dict | None:
    """The saved state if it exists and fits the story; otherwise None."""
    state = db.load_game(player)
    # Both stories have the same structure, so one of them is enough to check a save.
    if state is None or not logic.is_valid_state(STORIES[DEFAULT_LANGUAGE], state):
        return None
    return state


def open_game(player: str, language: str) -> dict:
    """Continue the player's saved game, or start and save a new one.

    Returns {"state", "continued", "language"}. A saved game keeps its own language;
    the language given is used only for a new game, or if the saved one is unknown.
    """
    state = load(player)
    saved_language = db.load_language(player)
    if state is None:
        language = _language_or_default(language)
        state = logic.new_game(STORIES[language])
        db.save_game(player, state, language)
        return {"state": state, "continued": False, "language": language}

    if saved_language not in LANGUAGES:
        language = _language_or_default(language)
        db.save_game(player, state, language)
    else:
        language = saved_language
    return {"state": state, "continued": True, "language": language}


def play(player: str, action_id, language: str = DEFAULT_LANGUAGE) -> dict:
    """Play one action on the player's saved game and save it only if it was accepted.

    The story is the one in the language saved with the game. The language given is
    used only when there is no saved game, to write the "no_game" message.
    """
    state = load(player)
    if state is None:
        story = STORIES[_language_or_default(language)]
        return {"accepted": False, "reason": "no_game", "message": story["messages"]["no_game"], "state": None}

    saved_language = db.load_language(player)
    language = saved_language if saved_language in LANGUAGES else _language_or_default(language)
    result = logic.apply_action(STORIES[language], state, action_id)
    if result["accepted"]:
        db.save_game(player, result["state"], language)
    return result


def restart(player: str) -> dict:
    """Replace the player's game with a new one, keeping the saved language. Returns the new state."""
    language = db.load_language(player)
    language = language if language in LANGUAGES else DEFAULT_LANGUAGE
    state = logic.new_game(STORIES[language])
    db.save_game(player, state, language)
    return state


def image_file(name) -> str | None:
    """The path of assets/<name>.jpg as text, or None if the name is not an id or the file is missing.

    The names come from story ids, never from what the player types. Anything that is not
    lower-case letters, digits and "_" (such as "../secret") is refused, so a name can never
    point outside the assets folder.
    """
    if not isinstance(name, str) or not IMAGE_NAME_PATTERN.fullmatch(name):
        return None
    path = ASSETS_DIR / f"{name}.jpg"
    return str(path) if path.is_file() else None
