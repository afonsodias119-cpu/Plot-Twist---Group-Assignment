"""Adapt the existing Python game for the 3D screen; never duplicate its rules."""

from datetime import date

import db
import game
import logic
from campus_people import ACTION_PERSON, ROOM_OF_PERSON, followers, is_rude, people_in_room, room_of_scene, talk, temper
# The friends' names of the start screen, cleaned on the server (specs/your-own-group.md, point 3).
from campus_people import clean_group
from campus_text import TEXT
# Evidence cards, confrontations and the hearing (specs/evidence-and-hearing.md). The answers stay on
# the server: campus_case.py is read only by campus_evidence.py and campus_memory.py.
from campus_evidence import (FINAL_ROOM, confront, hand, hearing, hearing_open, hearing_view, read_night,
                             refuse_during_hearing, shown_ending, without_broken_claims, write_night)
# The rude answers remembered tonight and the temper they give (specs/trust-has-consequences.md).
# The temper stays on the server: only the text and the note of a line change.
from campus_evidence import moods, remember_rude
# The night's clock (specs/night-schedule.md): the costs, the departures and the rounds. Server only,
# like the two files below: the clerk's sentence names the date of the code.
from campus_clock import (COSTS, LEAVES, NIGHT_MINUTES, ROUNDS, SHUTTER, WARNING, duarte_place, next_mark,
                          round_reached, time_text)
# The case of the day (specs/case-of-the-day.md): the date picks the case, the notes keep it. The
# case's data stays on the server: campus_evidence.case_of gives it, and the page sees only the date.
from campus_clock import case_day, case_of_day
from campus_evidence import CLASSIC
# Every reply is told on its way out with the friends' names (specs/your-own-group.md). The culprit is
# always Duarte now (specs/computer-lab-backup.md removed the cases of specs/culprit-of-the-night.md).
from campus_evidence import retell
# What the server remembers of a name's earlier nights (specs/earlier-nights.md). Server only too:
# its texts (the unknown number's whispers, the true ending) are in campus_case.py.
from campus_memory import TIME_UP, memory_view, night_number, record, round_warning, whispers
# The answers of the two puzzles: read only here, never sent to the page (specs/pen-and-code.md).
from campus_search import PC12_CODE, PEN_SPOT, PHOTO_PIECES, PHOTO_SOLUTION, PHOTO_TEXT, SEARCH_TEXT, SPOTS
# The things to examine in the rooms and their texts (specs/more-to-find.md). Server only too: the page
# gets a text only when the player examines the thing (the operation `examine`).
from campus_search import FIND_LATER, FIND_MINUTES, FIND_TEXT, FINDS
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
# The scenes the 3D campus can show. The five rooms have their own place in game3d.html (ROOMS).
ROOMS_3D = {"study_room", "print_shop", "library", "computer_lab", "auditorium"}
# The room of each thing to examine, read from FINDS (specs/more-to-find.md, point 2).
FIND_ROOM = {thing: room for room, things in FINDS.items() for thing in things}


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
    nothing moves after an ending: then nothing is written. A round reached while the player works at
    computer 12 (the files seen, the backup not saved yet: specs/computer-lab-backup.md) catches the
    player, unless Tomás has cracked and stands in the lab door: 3 minutes are charged and nothing else
    is saved. One command catches
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
    if mark is not None and at_computer_12(state):
        if "tomas" in night["cracked"]:
            message = TEXT[language]["schedule"]["door"]
        else:
            new = min(new + COSTS["caught"], NIGHT_MINUTES)
            caught, message = True, TEXT[language]["schedule"]["caught"]
            night = dict(night, caught=night["caught"] + [mark])
    if new >= NIGHT_MINUTES:   # the faculty closes with no ending (a catch never ends the story)
        night = record(player, night, TIME_UP)
    write_night(player, dict(night, minute=new))
    return {"charged": new - min(since, NIGHT_MINUTES), "caught": caught, "message": message}


def at_computer_12(state):
    """True while the player works at computer 12: in the lab, the files seen, the backup not saved yet."""
    flags = state["flags"]
    return state["scene"] == "computer_lab" and flags["files_viewed"] and not flags["backup_saved"]


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
    minutes = (22 * 60 + 15 + 40 * done) % (24 * 60)
    return f"{minutes // 60:02d}:{minutes % 60:02d}"


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


def action_rows(story, state, language, night):
    """The actions offered in the saved scene, ready for the screen. `person` says who offers it, if anyone.
    The campus minute of `night` matters: a lost clue no longer locks the auditorium."""
    scene, minute = story["scenes"][state["scene"]], night["minute"]
    note = missing_clues_note(state, language, minute)
    actions = []
    for action in logic.available_actions(story, state):
        definition = scene["actions"][action["id"]]
        if leads_outside_3d(definition):
            continue
        row = dict(
            action,
            kind="travel" if "go_to" in definition else "investigate",
            blocked_text=definition.get("blocked_text", "") if not action["allowed"] else "",
            decision="colleague_choice" in definition.get("sets", {}),
            person=ACTION_PERSON.get(action["id"]),
        )
        if definition.get("go_to") == FINAL_ROOM and note:
            row.update(allowed=False, blocked_text=note)
        actions.append(row)
    return actions


def find_rows(state, language):
    """The things of the 3D room of the saved scene, as {"id", "name"}; none after an ending
    (specs/more-to-find.md, point 6)."""
    if state["ending"] != "none":
        return []
    things = FINDS.get(room_of_scene(state["scene"]), ())
    return [{"id": thing, "name": FIND_TEXT[language][thing]["name"]} for thing in things]


# ---------- the case of the day (specs/case-of-the-day.md) ----------

def todays_case():
    """The note `case` of a game that starts now: today's case and today's date (point 2)."""
    today = case_day()
    return {"variant": case_of_day(today), "date": today.isoformat()}


def check_names(names):
    """`names` of `begin` must be a list of exactly three texts, each of them may be empty (point 2).
    A wrong shape is refused; a bad name inside is not: clean_group gives that field the story's
    name (specs/your-own-group.md, point 3)."""
    if not isinstance(names, list) or len(names) != 3 or not all(isinstance(name, str) for name in names):
        raise ValueError("Invalid names / Nomes inválidos.")


def mark_case(player, continued, names):
    """After `begin` opened the game: a new game gets today's case and the group cleaned from
    `names` (specs/your-own-group.md, point 2); a continued game with no case (a save from before
    this feature, or a game started with `open`) is marked as the classic case, with no date; a
    continued game that has a case keeps it and nothing is written (point 2). A continued game
    keeps its own group: the names sent now are not used."""
    night = read_night(player, game.load(player))
    if not continued:
        write_night(player, dict(night, case=todays_case(), names=clean_group(names)))
    elif night["case"] is None:
        write_night(player, dict(night, case={"variant": CLASSIC, "date": ""}))


def day_label(day_text, language):
    """"Case of 22 November" for "2026-11-22", "" for no date (point 5)."""
    if not day_text:
        return ""
    day, t = date.fromisoformat(day_text), TEXT[language]
    return t["case_of_day"].format(d=day.day, month=t["months"][day.month - 1])


def day_view(night, language):
    """The snapshot's `day` (point 5): the date and its label. A classic game sends none (also an old
    save marked classic, with no date: it finishes as the classic case). It never says the case's id
    or its data."""
    case = night["case"]
    if case is None or not case["date"]:
        return {"date": "", "label": ""}
    return {"date": case["date"], "label": day_label(case["date"], language)}


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
    actions = action_rows(story, state, language, night)
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
    if state["flags"]["backup_saved"]:
        sources.append(("computer_lab", "save_backup"))
    notebook = [
        {"title": story["scenes"][room]["title"],
         "text": story["scenes"][room]["actions"][action]["result_text"]}
        for room, action in sources
    ]
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
        # The 3D room where the saved scene takes place.
        "room": room_of_scene(state["scene"]),
        "people": people_in_room(state["scene"], state, language, gone),
        # The things to examine in that room: only their ids and names, never their texts (specs/more-to-find.md, point 6).
        "finds": find_rows(state, language),
        # Who walks with the player, and whether they already wait at computer 12 (specs/calendar-code.md).
        "followers": {"ids": followers(state),
                      "at_lab": state["flags"]["files_viewed"] or room_of_scene(state["scene"]) == "computer_lab"},
        "clock": clock_text(state),   # the old time from progress, kept for the reviewed tests; not shown
        # The campus minute and the schedule (specs/night-schedule.md, point 10).
        "night": night_view(state, night, language, charged, memory["night"]),
        # The night number, the story endings seen and the two gates; and the unknown number's
        # messages as this night starts (specs/earlier-nights.md, points 3 and 4).
        # No whisper once the faculty has closed: 22:45 ends the night as an ending does.
        "memory": memory, "whispers": [] if night_closed(state, night) else whispers(state, memory, language),
        "leonor_present": choice != "accused" and "leonor" not in gone,
        # True while the game is untouched: the 3D scene then starts the character outside.
        "fresh": state == story["start"],
        # The day of the case: its date and "Case of 22 November" (specs/case-of-the-day.md, point 5).
        "day": day_view(night, language),
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
    # The photo and the code are the same every night (specs/calendar-code.md).
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


def find_thing(player, language, thing):
    """The player examines one thing of a room (specs/more-to-find.md, point 5).

    The thing must be in the 3D room of the saved scene and the game must not have ended; otherwise
    the reply says so and nothing is saved. The flavour things and computer 7 cost nothing and write
    nothing. The order book costs its minutes from FIND_MINUTES, charged like every other cost, until
    the original photo is held. The reply is the snapshot plus the thing: {"id", "name", "text",
    "minutes"}, or None when it was refused.
    """
    if not isinstance(thing, str) or thing not in FIND_ROOM:
        raise ValueError("Unknown thing / Coisa desconhecida.")
    if locked(player):   # nothing else during the hearing (specs/evidence-and-hearing.md, point 12)
        return locked_reply(player, language, examine=None)
    state = game.load(player)
    language = db.load_language(player) or language
    if state["ending"] != "none" or room_of_scene(state["scene"]) != FIND_ROOM[thing]:
        return dict(snapshot(player, language, TEXT[language]["examine_where"], accepted=False), examine=None)
    texts = FIND_TEXT[language][thing]
    # A red herring reads differently once its condition is true, and then it costs nothing (point 3).
    later = thing in FIND_LATER and logic._condition_met(FIND_LATER[thing], state)
    minutes = 0 if later else FIND_MINUTES.get(thing, 0)
    clock = charge(player, language, minutes) if minutes else CLOCK_STILL
    seen = {"id": thing, "name": texts["name"], "text": texts["later"] if later else texts["text"], "minutes": minutes}
    return dict(clocked_snapshot(player, language, "", True, clock), examine=seen)


def report_time(player, language, minute):
    """The page reports its own whole campus minute (specs/night-schedule.md, point 3).

    The server keeps the larger of the saved minute and the reported one, so the minute never goes
    down; a report that is not larger, or any report after an ending, writes nothing. The reply is the
    snapshot: a round reached at computer 12 before the backup makes it a catch, which is not accepted.
    """
    if type(minute) is not int or not 0 <= minute <= NIGHT_MINUTES:   # `type(...) is int`: True is not a minute
        raise ValueError("Invalid minute / Minuto inválido.")
    language = db.load_language(player) or language
    clock = move_clock(player, language, minute, since=minute)
    return clocked_snapshot(player, language, "", True, clock)


def rude_answer(player, state, night, language, person, node):
    """The player chose an answer with a cost (specs/trust-has-consequences.md, point 2).

    `node` must be where such an answer leads in that person's tree. Then the same checks as `talk`
    are made first (the person is here, the line can be reached now), so a refused request writes
    nothing. When accepted, one more rude answer to that person is saved in the night's notes. It
    charges nothing: the page still takes the 5 minutes itself. Returns the night as saved now.
    """
    if not is_rude(language, person, node):
        raise ValueError("Unknown answer / Resposta desconhecida.")
    line = talk(state, language, person, node, gone_people(state, night["minute"]), night_number(player, night))
    without_broken_claims(line, night)
    return remember_rude(player, night, person)


def closed_reply(player, language, operation):
    """At 22:45 the faculty is closed (point 9): `talk`, `rude` and `confront` raise, every other
    operation is refused with "The faculty is closed". Nothing is played or written."""
    closed_text = TEXT[language]["time_up_title"]
    if operation in ("talk", "rude", "confront"):
        raise ValueError(closed_text)
    extra = {"search": {"found": False}, "unlock": {"unlocked": False}, "assemble": {"assembled": False},
             "hearing": {"heard": False}, "examine": {"examine": None}}
    return dict(snapshot(player, language, closed_text, accepted=False), **extra.get(operation, {}))


def run_command(payload):
    """Validate browser input before calling the existing saved-game functions."""
    if not isinstance(payload, dict):
        raise ValueError("Invalid request / Pedido inválido.")
    operation = payload.get("operation")
    allowed_fields = {
        "open": {"operation", "player", "language"},
        # `open` plus the case of the day and the group's three names (specs/case-of-the-day.md, point 2)
        "begin": {"operation", "player", "language", "names"},
        "play": {"operation", "player", "language", "action"},
        "restart": {"operation", "player", "language", "confirmed"},
        "enter": {"operation", "player", "language", "room"},
        "talk": {"operation", "player", "language", "npc", "node"},
        # a `talk` that is remembered: the page sends it for an answer with a cost (specs/trust-has-consequences.md, point 2)
        "rude": {"operation", "player", "language", "npc", "node"},
        "search": {"operation", "player", "language", "spot"},
        "unlock": {"operation", "player", "language", "code"},
        "assemble": {"operation", "player", "language", "pieces"},
        # specs/evidence-and-hearing.md, points 6 and 10
        "confront": {"operation", "player", "language", "npc", "node", "evidence"},
        "hearing": {"operation", "player", "language", "answer"},
        # the page reports its campus minute (specs/night-schedule.md, point 3)
        "time": {"operation", "player", "language", "minute"},
        # examining a thing of a room (specs/more-to-find.md, point 5)
        "examine": {"operation", "player", "language", "thing"},
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

    if operation == "begin":
        check_names(payload["names"])   # before anything is opened, so a bad request writes nothing
    if operation in ("open", "begin"):
        result = game.open_game(player, language)
        if not result["continued"]:
            # A new game is a new night: notes left behind by an older game must not help it.
            db.delete_night(player)
        if operation == "begin":
            mark_case(player, result["continued"], payload["names"])
        language = result["language"]
        message = UI_TEXTS[language]["continued" if result["continued"] else "started"]
        return snapshot(player, language, message)
    if game.load(player) is None:
        raise ValueError(UI_TEXTS[language]["no_game"])
    if operation == "restart":
        if payload["confirmed"] is not True:
            raise ValueError(UI_TEXTS[language]["confirm_question"])
        # The kind of game is kept (specs/case-of-the-day.md, point 3): a game of the day starts
        # today's case, a classic game stays classic and writes no notes, exactly as before.
        old_night = read_night(player, game.load(player))
        daily = old_night["case"] is not None
        game.restart(player)
        db.delete_night(player)   # a new night at 22:15: nobody is cracked, gone or caught, no hearing
        if daily:   # the same group plays the new night (specs/your-own-group.md, point 2)
            write_night(player, dict(read_night(player, game.load(player)), case=todays_case(),
                                     names=old_night["names"]))
        return snapshot(player, language)
    if operation == "time":
        return report_time(player, language, payload["minute"])
    language = db.load_language(player) or language
    state = game.load(player)
    night = read_night(player, state)
    if night_closed(state, night):
        return closed_reply(player, language, operation)
    if operation in ("talk", "rude"):
        # Talking only reads the saved game and the notes: nothing is written, so the endings cannot be touched.
        # A `rude` writes one thing only, its note in the night's notes (rude_answer).
        refuse_during_hearing(state, night, language)
        if operation == "rude":
            night = rude_answer(player, state, night, language, payload["npc"], payload["node"])
        # The night number decides which memory answers are offered (specs/earlier-nights.md, point 5).
        reply = talk(state, language, payload["npc"], payload["node"], gone_people(state, night["minute"]),
                     night_number(player, night))
        # A claim already broken tonight is not offered again (specs/evidence-and-hearing.md, point 7).
        reply = without_broken_claims(reply, night)
        # A person who got rude answers tonight answers shorter, warns the next person or lies
        # (specs/trust-has-consequences.md). Only the text and the note change.
        reply = temper(reply, moods(night), language)
        # The things the player can do by talking to this person (ask for the copy, take the decision, ...).
        reply["actions"] = [a for a in action_rows(STORIES[language], state, language, night)
                            if a["person"] == reply["npc"]]
        return reply
    if operation == "confront":
        # Showing a card: cracking a person writes in the night's notes, and the card's minutes are
        # added to the campus minute (specs/night-schedule.md, point 2). They can reach a round.
        card = payload["evidence"]
        result = confront(player, state, night, language, payload["npc"], payload["node"], card,
                          gone_people(state, night["minute"]), night_number(player, night))
        clock = charge(player, language, result["minutes"])
        return dict(clocked_snapshot(player, language, "", True, clock), confront=result)
    if operation == "hearing":
        answer = payload["answer"]
        accepted, message, heard = hearing(player, state, night, language, answer)
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
    if operation == "examine":
        return find_thing(player, language, payload["thing"])
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


def command(payload):
    """Validate browser input, run the operation, then tell the reply in tonight's case.

    retell runs once, on every reply, after the operation has run, so it reads the night's notes as
    they are now (specs/case-of-the-day.md). A request that raises is never told.
    A snapshot (a reply with a `scene`) then gets `group`, the three names in the order of the
    places, after retell so the names are never renamed (specs/your-own-group.md, points 4 and 5).
    """
    reply = run_command(payload)
    player = game.clean_name(payload["player"])   # valid: run_command has checked it
    state = game.load(player)
    if state is None:
        return reply
    language = db.load_language(player)
    language = language if language in LANGUAGES else payload["language"]
    night = read_night(player, state)
    told = retell(reply, night, language)
    if "scene" in told:
        told["group"] = list(night["names"])
    return told


# What the bridge sends when the page opens, so Streamlit's first round trip happens while the
# player reads the case, not on the first click (specs/warm-start.md).
WARMUP = {"warmup": True}


def keyed_command(payload):
    """command() for the published app: a name answers only to the browser that started it.

    The page's bridge adds `key` to every request (specs/name-belongs-to-browser.md, points 3 and 5).
    The key is taken out first, so command() and its allowed fields stay exactly as before.
    Returns (reply, key): the key goes back to the bridge, which keeps it for that name.
    The bridge's warm-up when the page opens is answered at once, with nothing read or saved
    (specs/warm-start.md, point 1).
    """
    # `is True`, not `==`: in Python 1 == True, and {"warmup": 1} must be refused like any bad request.
    if isinstance(payload, dict) and set(payload) == set(WARMUP) and payload["warmup"] is True:
        return {"warm": True}, ""
    if not isinstance(payload, dict):
        return command(payload), ""   # command() refuses it with the usual message
    request = {field: value for field, value in payload.items() if field != "key"}
    key = game.claim_name(request.get("player"), payload.get("key"))
    if key is None:
        language = request.get("language") if request.get("language") in LANGUAGES else "en"
        raise ValueError(TEXT[language]["name_taken"])
    return command(request), key
