"""Adapt the existing Python game for the 3D screen; never duplicate its rules."""

import db
import game
import logic
from story import LANGUAGES, STORIES, UI_TEXTS


def snapshot(player, language, message="", accepted=True):
    """Send the current scene, not the full mystery, to the browser."""
    state = game.load(player)
    if state is None:
        raise ValueError(UI_TEXTS[language]["no_game"])
    language = db.load_language(player) or language
    story = STORIES[language]
    scene = story["scenes"][state["scene"]]
    actions = []
    for action in logic.available_actions(story, state):
        definition = scene["actions"][action["id"]]
        actions.append(dict(
            action,
            kind="travel" if "go_to" in definition else "investigate",
            blocked_text=definition.get("blocked_text", "") if not action["allowed"] else "",
            decision="colleague_choice" in definition.get("sets", {}),
        ))

    # A notebook entry appears only once its evidence was actually discovered.
    sources = []
    if "usb_stick" in state["inventory"]:
        sources.append(("study_room", "open_drawer"))
    if "original_photo" in state["inventory"]:
        sources.append(("print_shop", "request_copy"))
    choice = state["flags"]["colleague_choice"]
    if choice != "none":
        sources.append(("library", "ask_for_help" if choice == "help" else "accuse"))
    if state["flags"]["files_viewed"]:
        sources.append(("computer_lab", "view_files"))
    notebook = [
        {"title": story["scenes"][room]["title"],
         "text": story["scenes"][room]["actions"][action]["result_text"]}
        for room, action in sources
    ]
    ending = next(({"id": e["id"], "title": e["title"], "text": e["text"]}
                   for e in story["endings"] if e["id"] == state["ending"]), None)
    return {
        "player": player, "language": language, "scene": state["scene"],
        "title": scene["title"], "texts": logic.scene_text(story, state),
        "inventory": [{"id": item, "label": story["items"][item]} for item in state["inventory"]],
        "actions": actions, "notebook": notebook, "ending": ending,
        "accepted": accepted, "message": message,
        "leonor_present": choice != "accused",
    }


def command(payload):
    """Validate browser input before calling the existing saved-game functions."""
    if not isinstance(payload, dict):
        raise ValueError("Invalid request / Pedido inválido.")
    operation = payload.get("operation")
    allowed_fields = {
        "open": {"operation", "player", "language"},
        "play": {"operation", "player", "language", "action"},
        "restart": {"operation", "player", "language", "confirmed"},
    }
    if not isinstance(operation, str) or operation not in allowed_fields:
        raise ValueError("Unknown operation / Operação desconhecida.")
    if set(payload) != allowed_fields[operation]:
        raise ValueError("Invalid request fields / Campos inválidos.")
    language = payload.get("language")
    if not isinstance(language, str) or language not in LANGUAGES:
        raise ValueError("Choose English or Português.")
    player = game.clean_name(payload.get("player"))
    if player is None:
        raise ValueError(UI_TEXTS[language]["invalid_name"])

    if operation == "open":
        result = game.open_game(player, language)
        language = result["language"]
        message = UI_TEXTS[language]["continued" if result["continued"] else "started"]
        return snapshot(player, language, message)
    if game.load(player) is None:
        raise ValueError(UI_TEXTS[language]["no_game"])
    if operation == "restart":
        if payload["confirmed"] is not True:
            raise ValueError(UI_TEXTS[language]["confirm_question"])
        game.restart(player)
        return snapshot(player, language)
    if not isinstance(payload["action"], str):
        raise ValueError("Invalid action / Ação inválida.")
    result = game.play(player, payload["action"], language)
    return snapshot(player, language, result["message"], result["accepted"])
