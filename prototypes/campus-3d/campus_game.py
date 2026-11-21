"""Adapt the existing Python game for the 3D screen; never duplicate its rules."""

import db
import game
import logic
from campus_people import ROOM_OF_PERSON, people_in_room, room_of_scene, talk
from campus_text import TEXT
from story import LANGUAGES, STORIES, UI_TEXTS

# The clues the player has to collect, and the room where each one is found. In this 3D version the
# auditorium opens only when all of them are done. (The Streamlit game keeps the story's own, looser
# rule: the old files must have been viewed.)
CLUES = [("usb_stick", "study_room"), ("original_photo", "print_shop"),
         ("files_viewed", "computer_lab"), ("leonor", "library")]
FINAL_ROOM = "auditorium"
# The scenes the 3D campus can show. The five rooms have their own place in game3d.html (ROOMS); the
# group chat is played inside the computer lab (see campus_people.ROOM_OF_SCENE).
ROOMS_3D = {"study_room", "print_shop", "library", "computer_lab", "auditorium", "group_chat"}


def leads_outside_3d(definition):
    """True when the action moves the player to a scene that has no room in the 3D campus."""
    return "go_to" in definition and definition["go_to"] not in ROOMS_3D


def clue_done(state, clue):
    if clue == "files_viewed":
        return state["flags"]["files_viewed"]
    if clue == "leonor":
        return state["flags"]["colleague_choice"] != "none"
    return clue in state["inventory"]


def missing_clues_note(state, language):
    """The note for trying the auditorium too early. Empty once every clue is done."""
    t = TEXT[language]
    missing = [t["clues"][clue] for clue, _room in CLUES if not clue_done(state, clue)]
    if not missing:
        return ""
    return f"{t['auditorium_note']} {t['missing']}: {'; '.join(missing)}."


def clock_text(state):
    """The time of the night, computed from the saved progress (it never ends the game)."""
    done = sum(clue_done(state, clue) for clue, _room in CLUES)
    flagged = sum(1 for n in range(1, 6) if state["flags"].get(f"flagged_{n}"))
    minutes = (22 * 60 + 15 + 40 * done + 5 * flagged) % (24 * 60)
    return f"{minutes // 60:02d}:{minutes % 60:02d}"


def chat_notes(story, state):
    """The chat messages the player has flagged, in order. Says nothing about which ones are fake."""
    messages = [t["text"] for t in story["scenes"]["group_chat"]["texts"] if t["when"] == {}][1:]
    title = story["scenes"]["group_chat"]["title"]
    return [{"title": f"{title} · {n}", "text": messages[n - 1]} for n in range(1, 6)
            if state["flags"].get(f"flagged_{n}")]


def route(story, start, goal):
    """The scenes to pass through, in order, from `start` to `goal` using the story's own go_to actions."""
    seen, queue = {start: []}, [start]
    while queue:
        here = queue.pop(0)
        for definition in story["scenes"][here]["actions"].values():
            nxt = definition.get("go_to")
            if nxt and nxt not in seen:
                seen[nxt] = seen[here] + [nxt]
                queue.append(nxt)
    return seen.get(goal)


def snapshot(player, language, message="", accepted=True):
    """Send the current scene, not the full mystery, to the browser."""
    state = game.load(player)
    if state is None:
        raise ValueError(UI_TEXTS[language]["no_game"])
    language = db.load_language(player) or language
    story = STORIES[language]
    scene = story["scenes"][state["scene"]]
    note = missing_clues_note(state, language)
    actions = []
    for action in logic.available_actions(story, state):
        definition = scene["actions"][action["id"]]
        if leads_outside_3d(definition):
            continue
        row = dict(
            action,
            kind="travel" if "go_to" in definition and definition["go_to"] != "group_chat" else "investigate",
            blocked_text=definition.get("blocked_text", "") if not action["allowed"] else "",
            decision="colleague_choice" in definition.get("sets", {}),
        )
        if definition.get("go_to") == FINAL_ROOM and note:
            row.update(allowed=False, blocked_text=note)
        actions.append(row)

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
    ] + chat_notes(story, state)
    ending = next(({"id": e["id"], "title": e["title"], "text": e["text"]}
                   for e in story["endings"] if e["id"] == state["ending"]), None)
    return {
        "player": player, "language": language, "scene": state["scene"],
        "title": scene["title"], "texts": logic.scene_text(story, state),
        "inventory": [{"id": item, "label": story["items"][item]} for item in state["inventory"]],
        "actions": actions, "notebook": notebook, "ending": ending,
        # The to-do list of the phone: what has to be collected, where, and what is already done.
        "clues": [{"id": clue, "label": TEXT[language]["clues"][clue], "room": story["scenes"][room]["title"],
                   "done": clue_done(state, clue)} for clue, room in CLUES],
        "accepted": accepted, "message": message,
        # The 3D room where the saved scene takes place (the group chat happens in the computer lab).
        "room": room_of_scene(state["scene"]),
        "people": people_in_room(state["scene"], state, language),
        "clock": clock_text(state),
        "leonor_present": choice != "accused",
        # True while the game is untouched: the 3D scene then starts the character outside.
        "fresh": state == story["start"],
    }


def enter_room(player, language, room):
    """The character walked through the door of `room`: travel there with the story's own actions.

    Every room connects only to the starting scene, so walking from one room to another is two
    moves (back to the hub, then the room). Each move is an ordinary game.play call, so a locked
    door refuses exactly as it does for the buttons, and the walk stops at the first refusal.
    """
    state = game.load(player)
    language = db.load_language(player) or language
    story = STORIES[language]
    steps = [] if room_of_scene(state["scene"]) == room else route(story, state["scene"], room) or []
    message, accepted = "", True
    for target in steps:
        actions = story["scenes"][state["scene"]]["actions"]
        action_id = next((a for a, definition in actions.items() if definition.get("go_to") == target), None)
        if action_id is None:
            message, accepted = story["messages"]["not_here"], False
            break
        note = missing_clues_note(state, language) if target == FINAL_ROOM and state["ending"] == "none" else ""
        if note:   # the auditorium stays closed until every clue is done: nothing is played or saved
            message, accepted = note, False
            break
        result = game.play(player, action_id, language)
        message, accepted = result["message"], result["accepted"]
        if not accepted:
            break
        state = game.load(player)
    return snapshot(player, language, message, accepted)


def command(payload):
    """Validate browser input before calling the existing saved-game functions."""
    if not isinstance(payload, dict):
        raise ValueError("Invalid request / Pedido inválido.")
    operation = payload.get("operation")
    allowed_fields = {
        "open": {"operation", "player", "language"},
        "play": {"operation", "player", "language", "action"},
        "restart": {"operation", "player", "language", "confirmed"},
        "enter": {"operation", "player", "language", "room"},
        "talk": {"operation", "player", "language", "npc", "node"},
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
    if operation == "talk":
        # Talking only reads the saved game: nothing is written, so the endings cannot be touched.
        language = db.load_language(player) or language
        return talk(game.load(player), language, payload["npc"], payload["node"])
    if operation == "enter":
        room = payload["room"]
        if not isinstance(room, str) or room not in set(ROOM_OF_PERSON.values()):
            raise ValueError("Invalid room / Sala inválida.")
        return enter_room(player, language, room)
    if not isinstance(payload["action"], str):
        raise ValueError("Invalid action / Ação inválida.")
    # Going to the auditorium by the button needs every clue too, exactly as walking in through its door.
    state = game.load(player)
    saved_language = db.load_language(player) or language
    definition = STORIES[saved_language]["scenes"][state["scene"]]["actions"].get(payload["action"], {})
    if leads_outside_3d(definition):
        return snapshot(player, language, STORIES[saved_language]["messages"]["not_here"], accepted=False)
    if definition.get("go_to") == FINAL_ROOM and state["ending"] == "none":
        note = missing_clues_note(state, saved_language)
        if note:
            return snapshot(player, language, note, accepted=False)
    result = game.play(player, payload["action"], language)
    return snapshot(player, language, result["message"], result["accepted"])
