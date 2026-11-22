"""Adapt the existing Python game for the 3D screen; never duplicate its rules."""

import db
import game
import logic
from campus_people import ACTION_PERSON, ROOM_OF_PERSON, people_in_room, room_of_scene, talk
from campus_text import TEXT
# Evidence cards, confrontations and the hearing (specs/evidence-and-hearing.md). The answers stay on
# the server: campus_case.py is read only by campus_evidence.py.
from campus_evidence import (FINAL_ROOM, confront, hand, hearing, hearing_open, hearing_view, read_night,
                             refuse_during_hearing, shown_ending, without_broken_claims)
# The answers of the two puzzles: read only here, never sent to the page (specs/pen-and-code.md).
from campus_search import PC12_CODE, PEN_SPOT, PHOTO_PIECES, PHOTO_SOLUTION, PHOTO_TEXT, SEARCH_TEXT, SPOTS
from story import LANGUAGES, STORIES, UI_TEXTS

# The clues the player has to collect, and the room where each one is found. In this 3D version the
# auditorium opens only when all of them are done. (The Streamlit game keeps the story's own, looser
# rule: the old files must have been viewed.)
CLUES = [("usb_stick", "study_room"), ("original_photo", "print_shop"),
         ("files_viewed", "computer_lab"), ("leonor", "library")]
# FINAL_ROOM (the auditorium) is imported from campus_evidence.py above: the hearing uses it too.
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
    """The note for trying the auditorium too early. Empty once every clue is done.

    It does not say which clues are missing (specs/harder-campus.md): the player has to work it out.
    """
    if all(clue_done(state, clue) for clue, _room in CLUES):
        return ""
    return TEXT[language]["auditorium_note"]


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


def chat_view(story, state):
    """What the chat screen of computer 12 shows: the five messages and which ones are flagged.
    It never says which messages are fake."""
    if state["scene"] != "group_chat":
        return None
    texts = story["scenes"]["group_chat"]["texts"]
    messages = [t["text"] for t in texts if t["when"] == {}]
    return {"intro": messages[0], "messages": [
        {"n": n, "text": messages[n], "flagged": bool(state["flags"].get(f"flagged_{n}")), "action": f"flag_{n}"}
        for n in range(1, 6)]}


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


def action_rows(story, state, language):
    """The actions offered in the saved scene, ready for the screen. `person` says who offers it, if anyone."""
    scene = story["scenes"][state["scene"]]
    note = missing_clues_note(state, language)
    actions = []
    for action in logic.available_actions(story, state):
        definition = scene["actions"][action["id"]]
        if leads_outside_3d(definition):
            continue
        row = dict(
            action,
            kind="travel" if "go_to" in definition and definition["go_to"] != "group_chat"
                 else "chat" if action["id"].startswith("flag_") else "investigate",
            blocked_text=definition.get("blocked_text", "") if not action["allowed"] else "",
            decision="colleague_choice" in definition.get("sets", {}),
            person=ACTION_PERSON.get(action["id"]),
        )
        if definition.get("go_to") == FINAL_ROOM and note:
            row.update(allowed=False, blocked_text=note)
        actions.append(row)
    return actions


def snapshot(player, language, message="", accepted=True):
    """Send the current scene, not the full mystery, to the browser."""
    state = game.load(player)
    if state is None:
        raise ValueError(UI_TEXTS[language]["no_game"])
    language = db.load_language(player) or language
    story = STORIES[language]
    scene = story["scenes"][state["scene"]]
    actions = action_rows(story, state, language)

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
    # The night's notes (who was cracked, the hearing), cleaned in memory: reading writes nothing.
    night = read_night(player, state)
    return {
        "player": player, "language": language, "scene": state["scene"],
        "title": scene["title"], "texts": logic.scene_text(story, state),
        "inventory": [{"id": item, "label": story["items"][item]} for item in state["inventory"]],
        "actions": actions, "notebook": notebook,
        # The ending on the screen: after a hearing, the verdict can cap the story's ending (point 11).
        "ending": shown_ending(state, night, language),
        # The cards held now, and the hearing (None when none was started tonight).
        "evidence": hand(state, night, language),
        "hearing": hearing_view(state, night, language),
        # The to-do list of the phone: what has to be collected, where, and what is already done.
        "clues": [{"id": clue, "label": TEXT[language]["clues"][clue], "room": story["scenes"][room]["title"],
                   "done": clue_done(state, clue)} for clue, room in CLUES],
        "accepted": accepted, "message": message,
        # The 3D room where the saved scene takes place (the group chat happens in the computer lab).
        "room": room_of_scene(state["scene"]),
        "people": people_in_room(state["scene"], state, language),
        "clock": clock_text(state),
        "chat": chat_view(story, state),
        "flagged": sum(1 for n in range(1, 6) if state["flags"].get(f"flagged_{n}")),   # for the unknown number's messages and the share card
        "leonor_present": choice != "accused",
        # True while the game is untouched: the 3D scene then starts the character outside.
        "fresh": state == story["start"],
    }


def locked(player):
    """True from the start of the hearing until the ending (specs/evidence-and-hearing.md, point 12)."""
    state = game.load(player)
    return hearing_open(state, read_night(player, state))


def locked_reply(player, language, **extra):
    """The refusal for play, enter, search and unlock during the hearing. Nothing is played or saved."""
    language = db.load_language(player) or language
    return dict(snapshot(player, language, TEXT[language]["hearing_locked"], accepted=False), **extra)


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


def search_room(player, language, spot):
    """The player clicked a spot of the study room (specs/pen-and-code.md).

    A wrong spot only says what is there and saves nothing. The right spot plays the story's own
    open_drawer action, so the USB stick is saved exactly as before. `found` tells the page which.
    """
    if not isinstance(spot, str) or spot not in SPOTS:
        raise ValueError("Unknown place / Sítio desconhecido.")
    if locked(player):
        return locked_reply(player, language, found=False)
    state = game.load(player)
    language = db.load_language(player) or language
    t = TEXT[language]
    if state["ending"] != "none" or state["scene"] != "study_room":
        return dict(snapshot(player, language, t["search_where"], accepted=False), found=False)
    if "usb_stick" in state["inventory"]:
        return dict(snapshot(player, language, t["search_done"], accepted=False), found=False)
    if spot != PEN_SPOT:
        return dict(snapshot(player, language, SEARCH_TEXT[language]["nothing"][spot], accepted=False), found=False)
    result = game.play(player, "open_drawer", language)
    message = SEARCH_TEXT[language]["found"] if result["accepted"] else result["message"]
    return dict(snapshot(player, language, message, result["accepted"]), found=result["accepted"])


def unlock_computer(player, language, code):
    """The player typed a code on computer 12 (specs/pen-and-code.md).

    A wrong code saves nothing. The right code plays the story's own view_files action, which still
    needs the USB stick. `unlocked` tells the page whether the code was right.
    """
    if not isinstance(code, str):
        raise ValueError("Invalid code / Código inválido.")
    if locked(player):
        return locked_reply(player, language, unlocked=False)
    language = db.load_language(player) or language
    if code != PC12_CODE:
        return dict(snapshot(player, language, TEXT[language]["code_wrong"], accepted=False), unlocked=False)
    result = game.play(player, "view_files", language)
    return dict(snapshot(player, language, result["message"], result["accepted"]), unlocked=True)


def assemble_photo(player, language, pieces):
    """The player filled the frame with the pieces of the torn photo (specs/torn-photo.md).

    `pieces` has one [piece id, rotation] for each place of the frame, in reading order. A wrong photo
    saves nothing. The right one plays the story's own request_copy action, so the photo is saved
    exactly as before. `assembled` tells the page which.
    """
    if (not isinstance(pieces, list) or len(pieces) != len(PHOTO_PIECES)
            or not all(isinstance(p, list) and len(p) == 2 and isinstance(p[0], str)
                       and type(p[1]) is int and p[1] in (0, 90, 180, 270) for p in pieces)
            or sorted(p[0] for p in pieces) != sorted(PHOTO_PIECES)):
        raise ValueError("Invalid photo / Fotografia inválida.")
    if locked(player):   # nothing else during the hearing (specs/evidence-and-hearing.md, point 12)
        return locked_reply(player, language, assembled=False)
    state = game.load(player)
    language = db.load_language(player) or language
    t = TEXT[language]
    if state["ending"] != "none" or state["scene"] != "print_shop" or "original_photo" in state["inventory"]:
        return dict(snapshot(player, language, t["photo_wrong"], accepted=False), assembled=False)
    if [p[0] for p in pieces] != list(PHOTO_SOLUTION) or any(p[1] != 0 for p in pieces):
        return dict(snapshot(player, language, t["photo_wrong"], accepted=False), assembled=False)
    result = game.play(player, "request_copy", language)
    message = PHOTO_TEXT[language] if result["accepted"] else result["message"]
    return dict(snapshot(player, language, message, result["accepted"]), assembled=result["accepted"])


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
        "search": {"operation", "player", "language", "spot"},
        "unlock": {"operation", "player", "language", "code"},
        "assemble": {"operation", "player", "language", "pieces"},
        # specs/evidence-and-hearing.md, points 6 and 10
        "confront": {"operation", "player", "language", "npc", "node", "evidence"},
        "hearing": {"operation", "player", "language", "answer"},
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
        if not result["continued"]:
            # A new game is a new night: notes left behind by an older game must not help it.
            db.delete_night(player)
        language = result["language"]
        message = UI_TEXTS[language]["continued" if result["continued"] else "started"]
        return snapshot(player, language, message)
    if game.load(player) is None:
        raise ValueError(UI_TEXTS[language]["no_game"])
    if operation == "restart":
        if payload["confirmed"] is not True:
            raise ValueError(UI_TEXTS[language]["confirm_question"])
        game.restart(player)
        db.delete_night(player)   # a new night: nobody is cracked and no hearing has started
        return snapshot(player, language)
    if operation == "talk":
        # Talking only reads the saved game and the notes: nothing is written, so the endings cannot be touched.
        language = db.load_language(player) or language
        state = game.load(player)
        night = read_night(player, state)
        refuse_during_hearing(state, night, language)
        reply = talk(state, language, payload["npc"], payload["node"])
        # A claim already broken tonight is not offered again (specs/evidence-and-hearing.md, point 7).
        reply = without_broken_claims(reply, night)
        # The things the player can do by talking to this person (ask for the copy, take the decision, ...).
        reply["actions"] = [a for a in action_rows(STORIES[language], state, language) if a["person"] == reply["npc"]]
        return reply
    if operation == "confront":
        # Showing a card: only cracking a person writes, and only in the night's notes.
        language = db.load_language(player) or language
        state = game.load(player)
        result = confront(player, state, read_night(player, state), language,
                          payload["npc"], payload["node"], payload["evidence"])
        return dict(snapshot(player, language), confront=result)
    if operation == "hearing":
        language = db.load_language(player) or language
        state = game.load(player)
        accepted, message, heard = hearing(player, state, read_night(player, state), language, payload["answer"])
        return dict(snapshot(player, language, message, accepted), heard=heard)
    if operation == "enter":
        room = payload["room"]
        if not isinstance(room, str) or room not in set(ROOM_OF_PERSON.values()):
            raise ValueError("Invalid room / Sala inválida.")
        if locked(player):
            return locked_reply(player, language)
        return enter_room(player, language, room)
    if operation == "search":
        return search_room(player, language, payload["spot"])
    if operation == "unlock":
        return unlock_computer(player, language, payload["code"])
    if operation == "assemble":
        return assemble_photo(player, language, payload["pieces"])
    if not isinstance(payload["action"], str):
        raise ValueError("Invalid action / Ação inválida.")
    if locked(player):
        return locked_reply(player, language)
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
