"""Adapt the existing Python game for the 3D screen; never duplicate its rules."""

import db
import game
import logic
from campus_people import ACTION_PERSON, ROOM_OF_PERSON, people_in_room, room_of_scene, talk
from campus_text import TEXT
# Evidence cards, confrontations and the hearing (specs/evidence-and-hearing.md). The answers stay on
# the server: campus_case.py is read only by campus_evidence.py and campus_memory.py.
from campus_evidence import (FINAL_ROOM, confront, hand, hearing, hearing_open, hearing_view, read_night,
                             refuse_during_hearing, shown_ending, without_broken_claims, write_night)
# The night's clock (specs/night-schedule.md): the costs, the departures and the rounds. Server only,
# like the two files below: the clerk's sentence names the date of the code.
from campus_clock import (COSTS, LEAVES, NIGHT_MINUTES, ROUNDS, SHUTTER, WARNING, duarte_place, next_mark,
                          round_reached, time_text)
# What the server remembers of a name's earlier nights (specs/earlier-nights.md). Server only too:
# its texts (the unknown number's whispers, the true ending) are in campus_case.py.
from campus_memory import TIME_UP, memory_view, night_number, record, round_warning, whispers
# The answers of the two puzzles: read only here, never sent to the page (specs/pen-and-code.md).
from campus_search import PC12_CODE, PEN_SPOT, PHOTO_PIECES, PHOTO_SOLUTION, PHOTO_TEXT, SEARCH_TEXT, SPOTS
from story import LANGUAGES, STORIES, UI_TEXTS

# The clues the player has to collect, and the room where each one is found. In this 3D version the
# auditorium opens only when each of them is done or lost. (The Streamlit game keeps the story's own,
# looser rule: the old files must have been viewed.)
CLUES = [("usb_stick", "study_room"), ("original_photo", "print_shop"),
         ("files_viewed", "computer_lab"), ("leonor", "library")]
# The clues that only a person who leaves can give (specs/night-schedule.md, point 6).
CLUE_PERSON = {"original_photo": "amelia", "leonor": "leonor"}
# What a command that did not move the clock returns (see move_clock).
CLOCK_STILL = {"charged": 0, "caught": False, "message": ""}
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


def clue_lost(state, clue, minute):
    """True when a clue that is not done can no longer be got tonight (specs/night-schedule.md, point 6).

    The photo is lost when the clerk has gone home. Leonor is lost when she has left, or as soon as
    the photo is lost: her decision needs it.
    """
    if clue not in CLUE_PERSON or clue_done(state, clue):
        return False
    if clue == "leonor" and clue_lost(state, "original_photo", minute):
        return True
    return minute >= LEAVES[CLUE_PERSON[clue]]


def missing_clues_note(state, language, minute=0):
    """The note for trying the auditorium too early. Empty once every clue is done or lost.

    A lost clue does not lock the auditorium, so every night can end (specs/night-schedule.md,
    point 6). It does not say which clues are missing (specs/harder-campus.md): the player has to
    work it out.
    """
    if all(clue_done(state, clue) or clue_lost(state, clue, minute) for clue, _room in CLUES):
        return ""
    return TEXT[language]["auditorium_note"]


def clue_rows(story, state, language, minute):
    """The to-do list of the phone: what has to be collected, where, until when, and what is done or lost."""
    return [{"id": clue, "label": TEXT[language]["clues"][clue], "room": story["scenes"][room]["title"],
             "done": clue_done(state, clue),
             "until": time_text(LEAVES[CLUE_PERSON[clue]]) if clue in CLUE_PERSON else "",
             "lost": clue_lost(state, clue, minute)} for clue, room in CLUES]


# ---------- the night's schedule (specs/night-schedule.md) ----------

def gone_people(state, minute):
    """The people who have left by the schedule (point 5): the clerk from minute 10, and Leonor from
    minute 15 only while she is undecided (once she helps she stays; once accused the story already
    emptied her table)."""
    gone = []
    if minute >= LEAVES["amelia"]:
        gone.append("amelia")
    if minute >= LEAVES["leonor"] and state["flags"]["colleague_choice"] == "none":
        gone.append("leonor")
    return gone


def gone_sentence(person, language):
    """The schedule sentence of a person who has left. The clerk's is kept in the server-only
    campus_clock.py, because the slip on the shutter names the date of the code."""
    if person == "amelia":
        return SHUTTER[language]
    return TEXT[language]["schedule"]["leonor_gone"]


def room_notice(state, minute, language):
    """`night.notice`: the schedule sentence of the saved room while its person has left and the game
    has not ended, otherwise "" (point 5)."""
    if state["ending"] != "none":
        return ""
    for person in gone_people(state, minute):
        if ROOM_OF_PERSON[person] == room_of_scene(state["scene"]):
            return gone_sentence(person, language)
    return ""


def schedule_refusal(state, minute, action, language):
    """The schedule sentence when `action` is the story action of a person who has left and the player
    stands in that person's room (point 5), otherwise "". It is checked before the story's own rules."""
    person = ACTION_PERSON.get(action)
    if (state["ending"] != "none" or person not in gone_people(state, minute)
            or ROOM_OF_PERSON[person] != room_of_scene(state["scene"])):
        return ""
    return gone_sentence(person, language)


def room_texts(story, state, notice):
    """The paragraphs of the saved scene. While its person has left, the schedule sentence is the first
    paragraph, in place of the story's opening one, which would say the opposite (point 5)."""
    texts = logic.scene_text(story, state)
    if not notice:
        return texts
    opening = story["scenes"][state["scene"]]["texts"][0]["text"]
    return [notice] + [text for text in texts if text != opening]


def night_closed(state, night):
    """True at 22:45 when the story has not ended: the faculty is closed (point 9)."""
    return night["minute"] >= NIGHT_MINUTES and state["ending"] == "none"


def due_messages(state, night, language, number=1):
    """The messages of the unknown number that are due now, as {"id", "text"} (point 7).

    Every rule takes the whole minute: at 9.5 the warning `shop` is still due. `number` is which
    night of this name tonight is: from night 3 the round warnings are a whisper, with the same ids
    (specs/earlier-nights.md, point 4).
    """
    minute, whole = night["minute"], int(night["minute"])
    text = TEXT[language]["schedule"]
    due = []
    if LEAVES["amelia"] - WARNING <= whole < LEAVES["amelia"] and "original_photo" not in state["inventory"]:
        due.append({"id": "shop", "text": text["warn_shop"]})
    if (LEAVES["leonor"] - WARNING <= whole < LEAVES["leonor"] and state["flags"]["colleague_choice"] == "none"
            and not clue_lost(state, "leonor", minute)):
        due.append({"id": "leonor", "text": text["warn_leonor"]})
    if any(clue_lost(state, clue, minute) for clue, _room in CLUES):
        due.append({"id": "lost", "text": text["lost"]})
    if "tomas" not in night["cracked"]:   # once Tomás watches the door, no round is a danger
        due += [{"id": f"round-{mark}", "text": round_warning(language, number)} for mark in ROUNDS if whole == mark - 1]
    return due


def night_view(state, night, language, charged, number=1):
    """The `night` object of the snapshot (point 10). `charged` is what this command cost; `number`
    is which night of this name tonight is (for the round warnings)."""
    minute = night["minute"]
    return {"minute": minute, "time": time_text(minute), "charged": charged,
            "report_at": next_mark(minute), "gone": gone_people(state, minute),
            "notice": room_notice(state, minute, language), "duarte": duarte_place(minute),
            "caught": bool(night["caught"]), "closed": night_closed(state, night),
            "messages": due_messages(state, night, language, number)}


def move_clock(player, language, minute, since):
    """Move the campus minute forward to `minute` and play the round it reaches (point 8).

    Used for a charge (`since` is the old minute) and for a report of the page (`since` is the
    reported minute, so the report itself is not counted as charged). The minute never goes down and
    nothing moves after an ending: then nothing is written. A round reached while the saved scene is
    the group chat catches the player, unless Tomás has cracked and stands in the lab door: the story's
    own go_computer_lab closes the chat (the flags stay) and 3 minutes are charged. One command catches
    at most once. A move that reaches 22:45 with no ending ends the night, so tonight's row is written
    then, as TIME_UP (specs/earlier-nights.md, point 2). Returns {"charged", "caught", "message"}.
    """
    state = game.load(player)
    night = read_night(player, state)
    old, new = night["minute"], min(minute, NIGHT_MINUTES)
    if state["ending"] != "none" or new <= old:
        return CLOCK_STILL
    caught, message = False, ""
    mark = round_reached(old, new)
    if mark is not None and state["scene"] == "group_chat":
        if "tomas" in night["cracked"]:
            message = TEXT[language]["schedule"]["door"]
        else:
            game.play(player, "go_computer_lab", language)
            new = min(new + COSTS["caught"], NIGHT_MINUTES)
            caught, message = True, TEXT[language]["schedule"]["caught"]
            night = dict(night, caught=night["caught"] + [mark])
    if new >= NIGHT_MINUTES:   # the faculty closes with no ending (a catch never ends the story)
        night = record(player, night, TIME_UP)
    write_night(player, dict(night, minute=new))
    return {"charged": new - min(since, NIGHT_MINUTES), "caught": caught, "message": message}


def charge(player, language, minutes):
    """Add the campus minutes a command costs (point 2). A cost of 0 changes and writes nothing."""
    minute = read_night(player, game.load(player))["minute"]
    return move_clock(player, language, minute + minutes, since=minute)


def play_and_charge(player, action, language):
    """game.play, then the action's minutes from the cost table when it was accepted (point 2).

    Every story action of the 3D game is played through here, so a right code and a direct
    view_files cost the same, and a refused action costs nothing. An action that ends the story (a
    direct present_evidence, with no hearing) ends the night: its row is written now, with the
    story's own ending, which is the one shown (specs/earlier-nights.md, point 2). Returns (result, clock).
    """
    result = game.play(player, action, language)
    if not result["accepted"]:
        return result, CLOCK_STILL
    state = game.load(player)
    if state["ending"] != "none":
        write_night(player, record(player, read_night(player, state), state["ending"]))
    return result, charge(player, language, COSTS.get(action, 0))


def clocked_snapshot(player, language, message, accepted, clock):
    """The snapshot after a command that may have moved the clock. A catch is not accepted and its
    message is Duarte's line; Tomás in the doorway gives his own line (point 8)."""
    if clock["message"]:
        message = clock["message"]
    return snapshot(player, language, message, accepted and not clock["caught"], clock["charged"])


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


def action_rows(story, state, language, minute=0):
    """The actions offered in the saved scene, ready for the screen. `person` says who offers it, if anyone.
    `minute` is the campus minute: a lost clue no longer locks the auditorium."""
    scene = story["scenes"][state["scene"]]
    note = missing_clues_note(state, language, minute)
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


def snapshot(player, language, message="", accepted=True, charged=0):
    """Send the current scene, not the full mystery, to the browser.

    `charged` is what this command cost in campus minutes (specs/night-schedule.md, point 10).
    """
    state = game.load(player)
    if state is None:
        raise ValueError(UI_TEXTS[language]["no_game"])
    language = db.load_language(player) or language
    story = STORIES[language]
    scene = story["scenes"][state["scene"]]
    # The night's notes (who was cracked, the hearing, the minute), cleaned in memory: reading writes nothing.
    night = read_night(player, state)
    minute = night["minute"]
    gone = gone_people(state, minute)
    actions = action_rows(story, state, language, minute)
    # What the server remembers of this name's earlier nights (specs/earlier-nights.md, point 3).
    memory = memory_view(player, night)

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
    return {
        "player": player, "language": language, "scene": state["scene"],
        # While the person of the room has left, its first paragraph is the schedule sentence (point 5).
        "title": scene["title"], "texts": room_texts(story, state, room_notice(state, minute, language)),
        "inventory": [{"id": item, "label": story["items"][item]} for item in state["inventory"]],
        "actions": actions, "notebook": notebook,
        # The ending on the screen: after a hearing, the verdict can cap the story's ending (point 11).
        "ending": shown_ending(state, night, language),
        # The cards held now, and the hearing (None when none was started tonight).
        "evidence": hand(state, night, language),
        "hearing": hearing_view(state, night, language),
        # The to-do list of the phone: what has to be collected, where, until when, what is done or lost.
        "clues": clue_rows(story, state, language, minute),
        "accepted": accepted, "message": message,
        # The 3D room where the saved scene takes place (the group chat happens in the computer lab).
        "room": room_of_scene(state["scene"]),
        "people": people_in_room(state["scene"], state, language, gone),
        "clock": clock_text(state),   # the old time from progress, kept for the reviewed tests; not shown
        # The campus minute and the schedule (specs/night-schedule.md, point 10).
        "night": night_view(state, night, language, charged, memory["night"]),
        # The night number, the story endings seen and the two gates; and the unknown number's
        # messages as this night starts (specs/earlier-nights.md, points 3 and 4).
        # No whisper once the faculty has closed: 22:45 ends the night as an ending does.
        "memory": memory, "whispers": [] if night_closed(state, night) else whispers(state, memory, language),
        "chat": chat_view(story, state),
        "flagged": sum(1 for n in range(1, 6) if state["flags"].get(f"flagged_{n}")),   # for the unknown number's messages and the share card
        "leonor_present": choice != "accused" and "leonor" not in gone,
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
    minute = read_night(player, state)["minute"]   # walking costs nothing, so it stays the same on the way
    message, accepted, clock = "", True, CLOCK_STILL
    for target in steps:
        actions = story["scenes"][state["scene"]]["actions"]
        action_id = next((a for a, definition in actions.items() if definition.get("go_to") == target), None)
        if action_id is None:
            message, accepted = story["messages"]["not_here"], False
            break
        note = missing_clues_note(state, language, minute) if target == FINAL_ROOM and state["ending"] == "none" else ""
        if note:   # the auditorium stays closed until every clue is done or lost: nothing is played or saved
            message, accepted = note, False
            break
        result, clock = play_and_charge(player, action_id, language)
        message, accepted = result["message"], result["accepted"]
        if not accepted:
            break
        state = game.load(player)
    return clocked_snapshot(player, language, message, accepted, clock)


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
    result, clock = play_and_charge(player, "open_drawer", language)
    message = SEARCH_TEXT[language]["found"] if result["accepted"] else result["message"]
    return dict(clocked_snapshot(player, language, message, result["accepted"], clock), found=result["accepted"])


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
    result, clock = play_and_charge(player, "view_files", language)   # 1 minute, the same as a direct view_files
    return dict(clocked_snapshot(player, language, result["message"], result["accepted"], clock), unlocked=True)


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
    # The clerk who went home cannot tape the pieces together: the schedule comes first
    # (specs/night-schedule.md, point 5), also when the photo is already held.
    gone_text = schedule_refusal(state, read_night(player, state)["minute"], "request_copy", language)
    if gone_text:
        return dict(snapshot(player, language, gone_text, accepted=False), assembled=False)
    if state["ending"] != "none" or state["scene"] != "print_shop" or "original_photo" in state["inventory"]:
        return dict(snapshot(player, language, t["photo_wrong"], accepted=False), assembled=False)
    if [p[0] for p in pieces] != list(PHOTO_SOLUTION) or any(p[1] != 0 for p in pieces):
        return dict(snapshot(player, language, t["photo_wrong"], accepted=False), assembled=False)
    result, clock = play_and_charge(player, "request_copy", language)   # half a minute, as the copy by its button
    message = PHOTO_TEXT[language] if result["accepted"] else result["message"]
    return dict(clocked_snapshot(player, language, message, result["accepted"], clock), assembled=result["accepted"])


def report_time(player, language, minute):
    """The page reports its own whole campus minute (specs/night-schedule.md, point 3).

    The server keeps the larger of the saved minute and the reported one, so the minute never goes
    down; a report that is not larger, or any report after an ending, writes nothing. The reply is the
    snapshot: a round reached in the group chat makes it a catch, which is not accepted.
    """
    if type(minute) is not int or not 0 <= minute <= NIGHT_MINUTES:   # `type(...) is int`: True is not a minute
        raise ValueError("Invalid minute / Minuto inválido.")
    language = db.load_language(player) or language
    clock = move_clock(player, language, minute, since=minute)
    return clocked_snapshot(player, language, "", True, clock)


def closed_reply(player, language, operation):
    """At 22:45 the faculty is closed (point 9): `talk` and `confront` raise, every other operation is
    refused with "The faculty is closed". Nothing is played or written."""
    closed_text = TEXT[language]["time_up_title"]
    if operation in ("talk", "confront"):
        raise ValueError(closed_text)
    extra = {"search": {"found": False}, "unlock": {"unlocked": False}, "assemble": {"assembled": False},
             "hearing": {"heard": False}}
    return dict(snapshot(player, language, closed_text, accepted=False), **extra.get(operation, {}))


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
        # the page reports its campus minute (specs/night-schedule.md, point 3)
        "time": {"operation", "player", "language", "minute"},
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
        db.delete_night(player)   # a new night at 22:15: nobody is cracked, gone or caught, no hearing
        return snapshot(player, language)
    if operation == "time":
        return report_time(player, language, payload["minute"])
    language = db.load_language(player) or language
    state = game.load(player)
    night = read_night(player, state)
    if night_closed(state, night):
        return closed_reply(player, language, operation)
    if operation == "talk":
        # Talking only reads the saved game and the notes: nothing is written, so the endings cannot be touched.
        refuse_during_hearing(state, night, language)
        # The night number decides which memory answers are offered (specs/earlier-nights.md, point 5).
        reply = talk(state, language, payload["npc"], payload["node"], gone_people(state, night["minute"]),
                     night_number(player, night))
        # A claim already broken tonight is not offered again (specs/evidence-and-hearing.md, point 7).
        reply = without_broken_claims(reply, night)
        # The things the player can do by talking to this person (ask for the copy, take the decision, ...).
        reply["actions"] = [a for a in action_rows(STORIES[language], state, language, night["minute"])
                            if a["person"] == reply["npc"]]
        return reply
    if operation == "confront":
        # Showing a card: cracking a person writes in the night's notes, and the card's minutes are
        # added to the campus minute (specs/night-schedule.md, point 2). They can reach a round.
        result = confront(player, state, night, language, payload["npc"], payload["node"], payload["evidence"],
                          gone_people(state, night["minute"]), night_number(player, night))
        clock = charge(player, language, result["minutes"])
        return dict(clocked_snapshot(player, language, "", True, clock), confront=result)
    if operation == "hearing":
        accepted, message, heard = hearing(player, state, night, language, payload["answer"])
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
    action = payload["action"]
    definition = STORIES[language]["scenes"][state["scene"]]["actions"].get(action, {})
    if leads_outside_3d(definition):
        return snapshot(player, language, STORIES[language]["messages"]["not_here"], accepted=False)
    # The schedule is checked before the story's own rules (specs/night-schedule.md, point 5).
    gone_text = schedule_refusal(state, night["minute"], action, language)
    if gone_text:
        return snapshot(player, language, gone_text, accepted=False)
    # Going to the auditorium by the button needs every clue done or lost too, exactly as walking in through its door.
    if definition.get("go_to") == FINAL_ROOM and state["ending"] == "none":
        note = missing_clues_note(state, language, night["minute"])
        if note:
            return snapshot(player, language, note, accepted=False)
    result, clock = play_and_charge(player, action, language)
    return clocked_snapshot(player, language, result["message"], result["accepted"], clock)
