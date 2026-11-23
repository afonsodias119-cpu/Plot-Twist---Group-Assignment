"""A campus that does not wait: the campus minute, two people who leave, and Duarte's rounds
(specs/night-schedule.md).

Written before the code: one test for every line under "Checks" in the spec, in the same order and
under the same headings.

How to read this file:
- `at(minute)` is the new `time` operation: the page reports its own campus minute.
- "saves nothing" means the database file has the same bytes before and after (`saved()`).
- A test that expects a ValueError first sends one valid request of the same operation in the same
  game and checks its reply. Without that, the test would pass today for the wrong reason
  ("Unknown operation").
- The new module campus_clock.py is imported inside `clock_rules()`, not at the top, so pytest can
  read this file while the module does not exist yet. The same for the new texts: they are read
  inside the tests, never when the file is loaded.
- The spec does not name the keys of TEXT["schedule"]. This file uses the keys of
  design-notes/texts-2-schedule.md (leonor_gone, warn_shop, warn_leonor, lost, round, caught, door).
- The balance tests play the routes of the spec's point 13 through campus_game.command, at a pace
  of some seconds a command (`paced`). Their helpers are the last ones at the top, under
  "helpers: the balance". They are the model of design-notes/balance.py and give its numbers.
"""

import ast
import importlib
import json
import re
import sqlite3
import sys
from contextlib import closing
from pathlib import Path

import pytest

import db
import game
import logic
from story import STORIES

PROJECT = Path(__file__).resolve().parents[1]
FOLDER = PROJECT / "prototypes" / "campus-3d"
sys.path.insert(0, str(FOLDER))
campus = importlib.import_module("campus_game")
people = importlib.import_module("campus_people")
search = importlib.import_module("campus_search")
page3d = importlib.import_module("page3d")
TEXT = importlib.import_module("campus_text").TEXT

PAGE = page3d.build_page(playable=True, inline=True)
PLAYER = "detective"
# The torn photo put together right: each piece in its place, upright (specs/torn-photo.md).
SOLUTION = [[piece, 0] for piece in search.PHOTO_SOLUTION]

# The professor's opening line at the hearing for a player who was caught at computer 12, word for
# word as in design-notes/texts-1-evidence.md (B5). The spec does not say in which table it lives.
CAUGHT_OPENING = {
    "en": "\"Before we begin: Mr Sequeira tells me you were reading the group's messages in secret tonight.\" The professor makes a mark beside your name.",
}


# ---------- helpers: requests ----------

def call(operation="open", language="en", player=PLAYER, **extra):
    """One request to the server, exactly as the page sends it."""
    return campus.command(dict(operation=operation, language=language, player=player, **extra))


def at(minute, player=PLAYER, language="en"):
    """The page reports its campus minute (the new `time` operation)."""
    return call("time", language, player, minute=minute)


def saved():
    """The bytes of the database file: equal before and after means nothing was written."""
    return db.DB_PATH.read_bytes()


def clock_rules():
    """The new module campus_clock.py. Imported here so this file can be collected before it exists."""
    return importlib.import_module("campus_clock")


def case():
    """The case file of feature 1 (campus_case.py): the claims and the verdict lines."""
    return importlib.import_module("campus_case")


def do(action, player=PLAYER, language="en"):
    """Play one story action (the `play` operation). It must be accepted."""
    result = call("play", language, player, action=action)
    assert result["accepted"], action
    return result


def play(*actions, language="en", player=PLAYER):
    """Open the game and play these story actions in order. Each one must be accepted."""
    result = call("open", language, player)
    for action in actions:
        result = do(action, player, language)
    return result


def walk(room, player=PLAYER, language="en"):
    """Walk through the door of a room (the `enter` operation). It must be accepted."""
    result = call("enter", language, player, room=room)
    assert result["accepted"], room
    return result


def unlock(player=PLAYER, language="en"):
    """Type the right code on computer 12: the story's view_files is played."""
    result = call("unlock", language, player, code=search.PC12_CODE)
    assert result["accepted"] and result["unlocked"]
    return result


def show(card, npc, node, player=PLAYER, language="en"):
    """Show one card to a person on one of their lines (the `confront` operation)."""
    return call("confront", language, player, npc=npc, node=node, evidence=card)


def investigate(player=PLAYER, language="en", leonor="ask_for_help", backup=True):
    """A new game played up to the computer lab, as in tests/test_evidence_and_hearing.py: the USB
    stick, the copy, the decision about Leonor, the old files (2.5 charged minutes: half a minute for
    the copy, one for the decision, one for the files) and, unless `backup` is False, the backup of
    the conversations (it costs nothing). The player stands beside Tomás; with `backup=False` the
    player is still working at computer 12, where Duarte's rounds catch (specs/computer-lab-backup.md)."""
    steps = ["open_drawer", "go_print_shop", "request_copy", "go_study_room",
             "go_library", leonor, "go_study_room", "go_computer_lab", "view_files"]
    if backup:
        steps.append("save_backup")
    return play(*steps, language=language, player=player)


def crack_tomas(player=PLAYER, language="en"):
    """In the computer lab: the file history on his claim line (0 minutes; specs/computer-lab-backup.md)."""
    reply = show("files", "tomas", "slides", player, language)
    assert reply["confront"]["cracked"] is True
    return reply


def to_the_hearing(player=PLAYER, language="en"):
    """A whole investigation (Leonor helps, the backup saved) and then into the auditorium: minute 2.5."""
    investigate(player, language)
    return walk("auditorium", player, language)


def answer(value, player=PLAYER, language="en"):
    """One request of the `hearing` operation: "start", "concede" or the id of a card."""
    return call("hearing", language, player, answer=value)


def hear(*answers, player=PLAYER, language="en"):
    """Start the hearing and give these answers, one for each claim. Returns the last reply."""
    result = answer("start", player, language)
    assert result["accepted"], "start"
    for value in answers:
        result = answer(value, player, language)
        assert result["heard"] is True, value
    return result


# ---------- helpers: reading a reply ----------

def schedule(language, key):
    """A text of TEXT[language]["schedule"] (the keys of design-notes/texts-2-schedule.md)."""
    return TEXT[language]["schedule"][key]


def shutter(language):
    """The clerk's schedule sentence, kept only in the server's campus_clock.py (spec, point 5)."""
    return clock_rules().SHUTTER[language]


def people_ids(result):
    """Who is in the room of the saved scene, by id."""
    return [person["id"] for person in result["people"]]


def message_ids(result):
    """The ids of the messages of the unknown number that are due now."""
    return [message["id"] for message in result["night"]["messages"]]


def clue_row(result, clue):
    """One row of the phone's Clues app."""
    return next(row for row in result["clues"] if row["id"] == clue)


def caught_note(player=PLAYER):
    """The note `caught` of the night, as saved (an empty list when there is none)."""
    return db.load_night(player)["notes"].get("caught", [])


def refuses_both_decisions(player, sentence):
    """Leonor's two decisions are refused with `sentence`, and nothing is saved."""
    before = saved()
    for action in ("ask_for_help", "accuse"):
        refused = call("play", player=player, action=action)
        assert not refused["accepted"] and refused["message"] == sentence, action
    assert saved() == before
    assert game.load(player)["flags"]["colleague_choice"] == "none"


def shows(where, text):
    """True when `text` is inside `where`, also in the way JSON writes it into the page: a quote
    becomes \\" and an accented letter becomes \\u00e1."""
    forms = {text, json.dumps(text)[1:-1], json.dumps(text, ensure_ascii=False)[1:-1]}
    return any(form in where for form in forms)


def code_only(text):
    """A source text without its comments, so a comment that explains a rule cannot fail a check."""
    return "\n".join(line.split("#")[0] for line in text.splitlines())


# ---------- helpers: the table `nights`, read and written by hand ----------

def night_row(player):
    """The row of `nights` of this player as (minute, notes), or None when there is no row."""
    with closing(sqlite3.connect(db.DB_PATH)) as connection:
        return connection.execute("SELECT minute, notes FROM nights WHERE player = ?", (player,)).fetchone()


def is_whole_or_half(minutes):
    """True for a number of minutes like 12 or 12.5 (not a bool): twice it is a whole number."""
    return type(minutes) in (int, float) and minutes * 2 == int(minutes * 2)


def write_night_by_hand(player, notes, minute=0):
    """Put a row in `nights` with any minute and any notes, the way a damaged file would have it."""
    with closing(sqlite3.connect(db.DB_PATH)) as connection, connection:
        connection.execute("INSERT OR REPLACE INTO nights (player, minute, notes) VALUES (?, ?, ?)",
                           (player, minute, notes))


# ---------- helpers: the messages of the unknown number ----------

# The id of each warning of point 7, and its key in TEXT["schedule"].
WARNINGS = {"shop": "warn_shop", "leonor": "warn_leonor", "lost": "lost"}


def warnings_due(result, language):
    """The warnings of point 7 that are due in this reply (the round warnings are left out), after
    checking that each one has its own text in this language."""
    found = {}
    for message in result["night"]["messages"]:
        assert set(message) == {"id", "text"}
        if message["id"] in WARNINGS:
            found[message["id"]] = message["text"]
    for warning, text in found.items():
        assert text == schedule(language, WARNINGS[warning]), (warning, language)
    return set(found)


# ---------- helpers: the balance (spec, point 13) ----------
#
# A route is a list of commands written in the spec's own notation, separated by "; ":
#   "search x"          an object of the table clicked (the first one of a visit also opens the close-up)
#   "> room"            a door
#   "rita: start, pen"  one `talk` for each line, in one conversation
#   "do x"              the story action x
#   "code"              the right code
#   "photo"             the torn photo: the answer that asks for the copy, the pieces, one `assemble`
#   "backup"            computer12 (its card is open after the code): do save_backup. Changed by
#                       specs/computer-lab-backup.md ("Reviewed tests that change"): it replaces "chat 5 2 4"
#   "show x"            card x shown on the line just heard (`confront`)
#   "hearing a, b, c"   start and three answers ("-" is "Say nothing")
#   "wait until 22:25"  the player does nothing until that time
#
# `paced(seconds, route)` plays one route through campus.command. Each command takes `seconds` of real
# time; a click with nothing to read takes QUICK_SECONDS (opening the close-up of the table), and the hands on the pieces of the photo take photo_hands() seconds. The page's campus
# minute is that real time plus every minute charged so far: by the server (night.charged) and by the
# page (1 for each wrong place). Right before a request is sent, the page reports its whole minute
# with `time` when it is ahead of the server; a player who waits reports when the wait ends (a wait
# always ends on a mark). Two commands send no request: opening the table and the answer that asks
# for the copy (it shows the clerk's line about the shredded print and opens the pieces). This is the
# model of design-notes/balance.py, with the server's own rules instead of a copy of them.

QUICK_SECONDS = 5

LAB = "> computer_lab; computer12: start; code; backup"
END = "> auditorium; professor: start"


def clues(choice):
    """CLUES(x) of the spec: the USB stick, the copy (the clerk's order line first, then the torn
    photo) and Leonor's decision `choice`."""
    return f"search usb_stick; > print_shop; amelia: start, order; photo; > library; leonor: start; do {choice}"


ROUTES = {
    # Changed by specs/computer-lab-backup.md ("Reviewed tests that change"): no chat, no flags and no
    # "fifth_element"; Leonor's choice decides the story's ending, and LAB saves the backup.
    1: "; ".join([clues("accuse"), LAB, END, "hearing files, original_photo, -"]),
    2: "; ".join([clues("ask_for_help"), LAB, END, "hearing files, original_photo, backup"]),
    # Route 3 is route 2, the careful night that route 6 is compared with.
    3: "; ".join([clues("ask_for_help"), LAB, END, "hearing files, original_photo, backup"]),
    # Only the lab: the photo is lost at 22:25 and Leonor at 22:30, so the auditorium opens.
    5: "; ".join(["search usb_stick", LAB, "wait until 22:30", END, "hearing files, -, -"]),
    # Route 6 is route 3 played by a player who waits at computer 12, the files open, until Duarte comes.
    6: "; ".join([clues("ask_for_help"), LAB, END, "hearing files, original_photo, backup"]),
    # With the photo, Leonor's card offers only the two decisions (specs/actions-when-they-make-sense.md).
    7: "; ".join(["rita: start, pen; search can; search usb_stick; > print_shop; amelia: start, order; "
                  "photo; > library; leonor: start; do ask_for_help; > computer_lab; "
                  "tomas: start, kind, who, password; computer12: start; code; backup",
                  END, "hearing files, original_photo, backup"]),
    9: "; ".join(["search usb_stick; > print_shop; amelia: start, order; photo; > study_room; "
                  "rita: start, photo, five; show original_photo; > library; leonor: start; do ask_for_help",
                  LAB, "tomas: start, kind, who, password, slides; show files",   # specs/two-answers.md: the order
                  END, "hearing files, original_photo, backup"]),
    11: "; ".join(["search usb_stick; > print_shop; amelia: start, order; photo",
                   LAB, "tomas: start, kind, who, password, slides; show files; "
                   "> library; leonor: start; do ask_for_help; leonor: soft, messages, mine, sure; "
                   "> study_room; rita: start, photo, duarte, warned, chat, five; show files; "
                   "> auditorium; duarte: start, part, slide; show files; professor: start, list, evidence, proof",
                   "hearing files, original_photo, backup"]),
}

# How each route treats a round while Tomás has not cracked (the rule under the routes in the spec):
# "warning": waits before the code when the warning has come (the round is at most a minute away);
# "knows":   the same, and also waits when the round would come before the code and the backup are done;
# "linger":  waits at computer 12, the files open, until Duarte comes (route 6).
ROUND_HABITS = {1: "knows", 2: "knows", 3: "knows", 5: "knows", 6: "linger", 7: "warning",
                9: "knows", 11: "knows"}

# The commands of "everything" that are not polite lines and cannot be skipped (spec, point 13).
# One of them takes QUICK_SECONDS: opening the table.
OTHER_COMMANDS = {"open the table": 1, "search": 1, "doors (print shop, library, lab, back to Rita, auditorium)": 5,
                  "copy (the answer and the full frame)": 2, "decision": 1, "code": 1, "backup": 1,
                  "cards (Tomás, Rita, Duarte)": 3, "hearing (start and three answers)": 4}


def photo_hands():
    """Seconds of hand work on the torn photo: 3 to drag each piece into the frame and 1 for each
    quarter turn, from where photo.js lays the pieces on the counter (its START list)."""
    source = (FOLDER / "photo.js").read_text(encoding="utf-8")
    start = re.search(r"const START = \[(.*?)\];", source, re.S).group(1)
    turns = [int(rotation) for rotation in re.findall(r'\["\w", \d+, \d+, (\d+)\]', start)]
    assert len(turns) == len(search.PHOTO_PIECES), turns
    return 3 * len(turns) + sum((360 - rotation) % 360 // 90 for rotation in turns)


def page_minute(run):
    """The campus minute on the page: the real time used plus every minute charged so far."""
    return run["seconds"] / 60 + run["charged"]


def take(run, reply):
    """Keep a snapshot the server sent, and take off the minutes it charged (point 4)."""
    run["last"] = reply
    run["charged"] += reply["night"]["charged"]


def report(run):
    """Send `time` with the page's whole minute when it is ahead of the server. False when the
    reply is a catch: the command that was waiting is then not sent (point 4)."""
    minute = int(page_minute(run))   # rounded down: the server keeps the copy's half, the page reports whole minutes
    if minute <= run["last"]["night"]["minute"]:
        return True
    reply = at(minute, run["player"])
    take(run, reply)
    return reply["accepted"]


def time_left_check(run):
    """At 22:45 with no ending the page shows its time-up card: the route has failed."""
    if page_minute(run) >= clock_rules().NIGHT_MINUTES:
        raise ValueError("the faculty closed")


def send(run, operation, seconds=None, **fields):
    """One command: its seconds pass, the page reports its minute, then the command is sent.
    Returns the reply, or None when the report brought a catch and the command was not sent."""
    run["commands"] += 1
    run["seconds"] += run["pace"] if seconds is None else seconds
    time_left_check(run)
    if not report(run):
        return None
    reply = call(operation, player=run["player"], **fields)
    if "night" in reply:   # a `talk` reply is not a snapshot
        take(run, reply)
    return reply


def think(run, seconds):
    """A command that sends no request (opening the table, asking for the copy): only its seconds pass."""
    run["commands"] += 1
    run["seconds"] += seconds
    time_left_check(run)


def deciding(run):
    """Leonor's decision can be taken (the photo is held, nothing decided): her card offers only the
    two decisions, no other answer (specs/actions-when-they-make-sense.md)."""
    state = game.load(run["player"])
    return "original_photo" in state["inventory"] and state["flags"]["colleague_choice"] == "none"


def sent(reply, step):
    """A command of the route must be sent (no catch) and accepted, or the route fails."""
    if reply is None or not reply["accepted"]:
        raise ValueError(f"refused: {step}")
    return reply


def wait_until(run, minute):
    """The player does nothing until `minute`; the page reports it when it gets there."""
    if page_minute(run) < minute:
        run["seconds"] = (minute - run["charged"]) * 60
        time_left_check(run)
        report(run)


def next_round(run):
    """The first round after the page's minute, or None after the last one."""
    return next((mark for mark in clock_rules().ROUNDS if mark > page_minute(run)), None)


def tomas_cracked(run):
    """Tomás stands in the lab door once he has cracked: a round can no longer catch the player."""
    return "tomas" in db.load_night(run["player"])["notes"].get("cracked", [])   # a fact, not a card (specs/computer-lab-backup.md)


def warned_round(run):
    """The round whose warning has come (it is at most one minute away), or None. A player who
    lingers does not heed it."""
    mark = next_round(run)
    if run["habit"] == "linger" or tomas_cracked(run) or mark is None or page_minute(run) < mark - 1:
        return None
    return mark


def before_the_code(run):
    """A careful player does not open the files with a round about to come: between the code and the
    backup the player is at computer 12, where Duarte catches (specs/computer-lab-backup.md)."""
    mark = next_round(run)
    if run["habit"] == "linger" or tomas_cracked(run) or mark is None:
        return
    warned = page_minute(run) >= mark - 1
    # the code and the backup, and the minute the code itself costs
    too_close = page_minute(run) + 2 * run["pace"] / 60 + clock_rules().COSTS["view_files"] >= mark
    if warned or (run["habit"] == "knows" and too_close):
        wait_until(run, mark)


def backup(run):
    """The step "backup": save_backup at computer 12. A lingering player first waits for Duarte with
    the files open; a catch only costs time, so the backup is then simply asked for again."""
    mark = next_round(run)
    if run["habit"] == "linger" and not tomas_cracked(run) and not run["last"]["night"]["caught"] and mark:
        wait_until(run, mark)   # Duarte finds the player at computer 12
    while True:
        reply = send(run, "play", action="save_backup")
        if reply is not None:
            sent(reply, "backup")
            return


def hearing(run, answers):
    """The step "hearing a, b, c": start, then one answer for each claim."""
    sent(send(run, "hearing", answer="start"), "hearing start")
    for value in answers:
        reply = sent(send(run, "hearing", answer="concede" if value == "-" else value), f"hearing {value}")
    run["ending"] = reply["ending"]["id"]
    run["doubts"] = reply["hearing"]["doubts"]


def play_step(run, step):
    """Play one step of a route, in the notation explained above."""
    if step.startswith("> "):
        sent(send(run, "enter", room=step[2:]), step)
        run["table"] = False   # the close-up of the table stays in the study room
    elif step.startswith("search "):
        if not run["table"]:   # the first object of a visit: the close-up opens first
            think(run, QUICK_SECONDS)
            run["table"] = True
        reply = send(run, "search", spot=step[len("search "):])   # a wrong object is not accepted, but it was sent
        if reply is None:
            raise ValueError(f"caught before {step}")
        if not reply["found"]:
            run["charged"] += clock_rules().PAGE_COSTS["wrong_spot"]   # taken by the page, as today
        else:
            run["table"] = False   # the close-up closes with the USB stick
    elif step.startswith("do "):
        action = step[len("do "):]
        person = people.ACTION_PERSON.get(action)
        if person == "leonor" and (run["line"] is None or run["line"][0] != person):
            raise ValueError(f"{step}: it is an answer of Leonor's card, and it is not open")
        sent(send(run, "play", action=action), step)
    elif step == "photo":
        # The copy is offered only after the clerk's order line (specs/actions-when-they-make-sense.md).
        if run["line"] != ("amelia", "order"):
            raise ValueError("photo: the copy is offered only after the clerk's order line")
        think(run, run["pace"])   # the answer: the clerk's line about the shredded print
        run["seconds"] += photo_hands()   # the hands on the pieces
        time_left_check(run)
        reply = sent(send(run, "assemble", pieces=SOLUTION), step)   # refused if she has gone home meanwhile
        assert reply["assembled"] is True
        run["line"] = None   # after the photo the clerk's card offers nothing more
    elif step == "code":
        before_the_code(run)
        reply = send(run, "unlock", code=search.PC12_CODE)
        # The code's own minute may reach a round: Duarte then catches the player with the files just
        # opened (not accepted), but the files are seen all the same.
        if reply is None or not reply["unlocked"]:
            raise ValueError(f"refused: {step}")
    elif step == "backup":
        backup(run)
    elif step.startswith("show "):
        person, node = run["line"]
        sent(send(run, "confront", npc=person, node=node, evidence=step[len("show "):]), step)
    elif step.startswith("hearing "):
        hearing(run, [value.strip() for value in step[len("hearing "):].split(",")])
    elif step.startswith("wait until "):
        hours, minutes = step[len("wait until "):].split(":")
        wait_until(run, int(hours) * 60 + int(minutes) - (22 * 60 + 15))
    else:   # "person: line, line, ...": one `talk` for each line, in one conversation
        person, lines = step.split(": ")
        for node in lines.split(", "):
            if person == "leonor" and node != "start" and deciding(run):
                raise ValueError(f"leonor: {node} is not offered while her decision can be taken")
            if send(run, "talk", npc=person, node=node) is None:
                raise ValueError(f"caught before {step}")
            run["line"] = (person, node)


def paced(seconds, route):
    """Play route number `route` with one command every `seconds`. Returns what happened:
    "ending" (None when the night did not end), "minute" (the page's campus minute at the end),
    "commands", "charged", "doubts", "caught" and "failed" (why the route stopped, or "")."""
    player = f"route {route} at {seconds}"
    run = {"player": player, "pace": seconds, "habit": ROUND_HABITS[route], "seconds": 0, "charged": 0,
           "commands": 0, "line": None, "table": False, "ending": None, "doubts": None, "failed": ""}
    run["last"] = call(player=player)   # a new night at 22:15, in the study room
    try:
        for step in ROUTES[route].split("; "):
            play_step(run, step)
    except ValueError as problem:   # a refused command, a person who has left, or 22:45
        run["failed"] = str(problem)
    return {"ending": run["ending"], "minute": page_minute(run), "commands": run["commands"],
            "charged": run["charged"], "doubts": run["doubts"], "caught": run["last"]["night"]["caught"],
            "failed": run["failed"]}


def polite_lines(person):
    """Every line of `person` that can be reached without a rude answer (an answer with a `cost`)."""
    nodes = people.PEOPLE["en"][person]["nodes"]
    seen, to_visit = set(), ["start"]
    while to_visit:
        node = to_visit.pop()
        if node not in seen:
            seen.add(node)
            to_visit += [option["next"] for option in nodes[node]["options"]
                         if option["next"] is not None and "cost" not in option]
    return seen


# ---------- The minute and its costs ----------

def test_a_new_night_starts_at_2215():
    result = call()
    assert result["night"] == {"minute": 0, "time": "22:15", "charged": 0, "report_at": 5, "gone": [],
                               "notice": "", "duarte": "auditorium", "caught": False, "closed": False,
                               "messages": []}
    assert result["clock"] == "22:15"   # the old field, computed from progress, is unchanged


def test_the_copy_costs_half_a_minute_and_the_decision_and_the_files_one_minute_each():
    # The copy, Leonor's help and the right code.
    call()
    call("search", spot=search.PEN_SPOT)
    do("go_print_shop")
    copy = do("request_copy")
    assert copy["night"]["charged"] == 0.5 and copy["night"]["minute"] == 0.5
    do("go_study_room")
    do("go_library")
    decision = do("ask_for_help")
    assert decision["night"]["charged"] == 1 and decision["night"]["minute"] == 1.5
    do("go_study_room")
    do("go_computer_lab")
    code = unlock()
    assert code["night"]["charged"] == 1 and code["night"]["minute"] == 0.5 + 1 + 1

    # The other decision, and view_files played directly (a hand-made request): the same minute.
    play("open_drawer", "go_print_shop", player="accuser")
    assert do("request_copy", "accuser")["night"]["charged"] == 0.5
    do("go_study_room", "accuser")
    do("go_library", "accuser")
    accuse = do("accuse", "accuser")
    assert accuse["night"]["charged"] == 1 and accuse["night"]["minute"] == 1.5
    do("go_study_room", "accuser")
    do("go_computer_lab", "accuser")
    files = do("view_files", "accuser")
    assert files["night"]["charged"] == 1 and files["night"]["minute"] == 0.5 + 1 + 1


def test_half_a_minute_is_kept_and_the_time_shows_the_whole_minutes():
    call()
    walk("print_shop")
    at(9)
    copy = do("request_copy")
    assert copy["night"]["charged"] == 0.5 and copy["night"]["minute"] == 9.5
    assert copy["night"]["time"] == "22:24"          # the shown time uses the whole minutes
    assert copy["night"]["report_at"] == 10
    assert "amelia" in people_ids(copy) and copy["night"]["gone"] == []   # 9.5 is still before 22:25
    # The INTEGER column keeps the whole minutes (db.py is not changed); the half is the note `half`.
    minute, notes = night_row(PLAYER)
    assert minute == 9 and json.loads(notes)["half"] is True
    assert call()["night"]["minute"] == 9.5          # a reload keeps the half

    before = saved()
    assert at(9)["night"]["minute"] == 9.5           # a smaller whole report changes nothing
    assert saved() == before
    ten = at(10)
    assert ten["night"]["minute"] == 10 and ten["night"]["gone"] == ["amelia"]
    assert night_row(PLAYER)[0] == 10 and json.loads(night_row(PLAYER)[1]).get("half", False) is False


def test_walking_talking_the_backup_and_the_hearing_cost_nothing():
    def costs_nothing(result, minute):
        assert result["night"]["charged"] == 0 and result["night"]["minute"] == minute

    call()
    costs_nothing(call("search", spot=search.PEN_SPOT), 0)   # the right place
    costs_nothing(walk("print_shop"), 0)                      # a door
    talked = call("talk", npc="amelia", node="start")
    assert "night" not in talked                              # a `talk` reply is not a snapshot
    costs_nothing(call(), 0)                                  # and talking moved nothing
    assert do("request_copy")["night"]["minute"] == 0.5
    costs_nothing(do("go_study_room"), 0.5)                   # a button
    costs_nothing(do("go_library"), 0.5)
    assert do("ask_for_help")["night"]["minute"] == 1.5
    costs_nothing(walk("computer_lab"), 1.5)                  # a door: two moves of the story
    assert unlock()["night"]["minute"] == 2.5
    costs_nothing(do("save_backup"), 2.5)                     # the backup (specs/computer-lab-backup.md: it replaces the chat)
    costs_nothing(walk("auditorium"), 2.5)
    for value in ("start", "files", "original_photo", "backup"):   # the four hearing commands
        costs_nothing(answer(value), 2.5)
    assert game.load(PLAYER)["ending"] != "none"


def test_refused_actions_cost_nothing_and_save_nothing():
    call()
    before = saved()
    refused = [call("search", spot="can"),             # a wrong object of the table (the page takes its minute, not the server)
               call("enter", room="auditorium")]       # a refused door: no clue is done yet
    assert saved() == before
    do("go_computer_lab")
    before = saved()
    refused += [call("play", action="view_files"),     # a blocked action: the USB stick is missing
                call("unlock", code="0000")]           # a wrong code
    assert saved() == before
    for result in refused:
        assert not result["accepted"]
        assert result["night"]["charged"] == 0 and result["night"]["minute"] == 0
    assert call()["night"]["minute"] == 0


def test_cards_cost_what_the_table_says():
    costs = clock_rules().COSTS
    investigate()   # minute 2.5
    right = crack_tomas()
    assert right["night"]["charged"] == right["confront"]["minutes"] == costs["card_right"] == 0
    rebuff = show("files", "tomas", "start")
    assert rebuff["confront"]["cracked"] is False
    assert rebuff["night"]["charged"] == rebuff["confront"]["minutes"] == costs["card_wrong"] == 2
    walk("auditorium")
    duarte = show("files", "duarte", "start")
    assert duarte["night"]["charged"] == duarte["confront"]["minutes"] == costs["card_duarte"] == 1
    assert duarte["night"]["minute"] == 2.5 + 0 + 2 + 1


def test_the_cost_table_is_whole_or_half_minutes_and_matches_the_rude_answers():
    rules = clock_rules()
    # The names the spec fixes (point 2); the numbers can be retuned, the balance tests below guard them.
    assert set(rules.COSTS) == {"request_copy", "ask_for_help", "accuse", "view_files",
                                "card_right", "card_wrong", "card_duarte", "caught"}
    assert set(rules.PAGE_COSTS) == {"rude_answer", "wrong_spot", "wrong_code"}
    for name, minutes in rules.COSTS.items():   # the server's costs may be a half (the copy is 0.5)
        assert is_whole_or_half(minutes) and 0 <= minutes <= 5, name   # True is not a minute
    for name, minutes in rules.PAGE_COSTS.items():   # the page takes whole minutes, as today
        assert type(minutes) is int and 0 <= minutes <= 5, name   # `type(...) is int`: True is not a minute
    for language in ("en", "pt"):
        costs = [option["cost"] for person in people.PEOPLE[language].values()
                 for line in person["nodes"].values() for option in line["options"] if "cost" in option]
        assert costs, language
        assert all(cost == rules.PAGE_COSTS["rude_answer"] for cost in costs), language


# ---------- The `time` operation ----------

def test_time_keeps_the_larger_minute_and_never_goes_down():
    call()
    seven = at(7)
    assert seven["accepted"] and seven["night"]["minute"] == 7 and seven["night"]["time"] == "22:22"
    before = saved()
    for minute in (3, 7):   # smaller, then the same: nothing changes and nothing is written
        assert at(minute)["night"]["minute"] == 7, minute
    assert saved() == before
    assert night_row(PLAYER)[0] == 7


def test_a_charge_is_added_to_the_reported_minute():
    call()
    do("go_print_shop")
    assert at(4)["night"]["minute"] == 4
    copy = do("request_copy")
    assert copy["night"]["minute"] == 4.5 and copy["night"]["charged"] == 0.5


def test_time_rejects_bad_minutes_and_extra_fields_and_saves_nothing():
    call()
    assert at(1)["night"]["minute"] == 1   # a valid request first
    before = saved()
    for bad in ("5", 5.0, 5.5, True, None, [5], -1, 31):   # 5.5 too: the page reports whole minutes
        with pytest.raises(ValueError):
            at(bad)
    with pytest.raises(ValueError):   # no minute
        call("time")
    with pytest.raises(ValueError):   # an extra field
        call("time", minute=5, extra=1)
    assert saved() == before
    assert call()["night"]["minute"] == 1


def test_time_needs_a_game_and_changes_nothing_after_an_ending():
    call()
    assert at(1)["night"]["minute"] == 1   # a valid request first
    before = saved()
    with pytest.raises(ValueError):   # a name that has no saved game
        at(3, player="nobody")
    assert saved() == before and game.load("nobody") is None

    to_the_hearing("ended")
    ended = do("present_evidence", "ended")
    assert ended["ending"] is not None
    minute = ended["night"]["minute"]
    before = saved()
    late = at(20, player="ended")
    assert late["night"]["minute"] == minute and late["ending"] == ended["ending"]
    assert saved() == before


def test_a_damaged_minute_in_the_table_is_brought_back_between_0_and_30():
    # (the column, the notes, the minute of the snapshot). The column holds whole minutes, so a 12.5
    # written there cannot be read (db.load_night counts it as 0); the half is the note `half`.
    rows = [(99, {}, 30), (-5, {}, 0), ("x", {}, 0), (12.5, {}, 0),
            (12, {"half": True}, 12.5), (12, {"half": "yes"}, 12), (30, {"half": True}, 30)]
    for number, (column, notes, expected) in enumerate(rows):
        player = f"damaged {number}"
        call(player=player)
        write_night_by_hand(player, json.dumps(notes), minute=column)
        minute = call(player=player)["night"]["minute"]   # raises nothing
        assert is_whole_or_half(minute) and minute == expected, (column, notes, minute)


def test_report_at_is_the_next_mark():
    assert call()["night"]["report_at"] == 5
    for minute, mark in ((5, 10), (12, 13), (26, 27), (27, 30), (30, 30)):   # in the study room: no catch
        assert at(minute)["night"]["report_at"] == mark, minute

    # Every minute of the night, against the table: the first mark after the minute, 30 at the end.
    marks = clock_rules().MARKS
    call(player="every minute")
    for minute in range(1, 31):
        expected = next((mark for mark in marks if mark > minute), 30)
        assert at(minute, "every minute")["night"]["report_at"] == expected, minute


def test_a_restart_brings_the_night_back_to_2215():
    call()
    at(20)
    restarted = call("restart", confirmed=True)
    assert restarted["night"]["minute"] == 0 and restarted["night"]["time"] == "22:15"
    assert restarted["night"]["gone"] == [] and restarted["night"]["closed"] is False
    assert restarted["fresh"] is True   # with minute 0, the page gives itself 30 new minutes (point 4)
    assert night_row(PLAYER) is None    # a confirmed restart deletes the row
    assert call()["night"]["minute"] == 0


# ---------- The two departures and the lost clues ----------

def test_the_clerk_is_gone_at_2225():
    # At minute 9 she is still there, and she gives the copy.
    call(player="early")
    walk("print_shop", "early")
    nine = at(9, "early")
    assert "amelia" in people_ids(nine) and nine["night"]["gone"] == []
    copy = call("play", player="early", action="request_copy")
    assert copy["accepted"]
    assert copy["message"] == STORIES["en"]["scenes"]["print_shop"]["actions"]["request_copy"]["result_text"]

    # At minute 10 she has gone home, also for a player who already holds the photo.
    call()
    walk("print_shop")
    assert call("talk", npc="amelia", node="start")["name"] == "Clerk"                    # a valid talk first
    do("request_copy")                                                                     # minute 0.5
    assert show("original_photo", "amelia", "start")["confront"]["cracked"] is False      # a valid confront (2 minutes)
    ten = at(10)
    assert people_ids(ten) == [] and ten["night"]["gone"] == ["amelia"]
    before = saved()
    with pytest.raises(ValueError):
        call("talk", npc="amelia", node="start")
    with pytest.raises(ValueError):
        show("original_photo", "amelia", "start")
    refused = call("play", action="request_copy")   # the story would say "You have already done that."
    assert not refused["accepted"] and refused["message"] == shutter("en")
    rebuilt = call("assemble", pieces=SOLUTION)     # the torn photo plays request_copy (specs/torn-photo.md)
    assert not rebuilt["accepted"] and rebuilt["message"] == shutter("en")
    assert saved() == before

    # Without the photo: the copy is refused with the same sentence and nothing is saved, also when
    # the torn photo is rebuilt right.
    call(player="late")
    walk("print_shop", "late")
    at(10, "late")
    before = saved()
    refused = call("play", player="late", action="request_copy")
    assert not refused["accepted"] and refused["message"] == shutter("en")
    rebuilt = call("assemble", player="late", pieces=SOLUTION)
    assert not rebuilt["accepted"] and rebuilt["message"] == shutter("en") and rebuilt["assembled"] is False
    assert saved() == before
    assert "original_photo" not in game.load("late")["inventory"]

    # The room can still be entered: the clerk is not in it.
    walk("study_room", "late")
    again = walk("print_shop", "late")
    assert again["scene"] == "print_shop" and people_ids(again) == []


def test_the_schedule_sentence_is_only_for_the_room_of_the_person_who_left():
    messages = STORIES["en"]["messages"]
    call()
    at(10)
    before = saved()
    elsewhere = call("play", action="request_copy")   # from the study room
    assert not elsewhere["accepted"] and elsewhere["message"] == messages["not_here"]
    assert elsewhere["message"] != shutter("en")
    assert saved() == before

    # After an ending (the photo and Leonor are lost, so the auditorium opens with the stick and the files).
    call("search", spot=search.PEN_SPOT)
    walk("computer_lab")
    unlock()
    do("save_backup")  # specs/computer-lab-backup.md: the auditorium needs the backup too
    walk("auditorium")
    assert do("present_evidence")["ending"] is not None
    before = saved()
    over = call("play", action="request_copy")
    assert not over["accepted"] and over["message"] == messages["game_over"]
    assert over["message"] != shutter("en")
    assert saved() == before


def test_leonor_leaves_at_2230_unless_she_is_helping():
    empty_chair = schedule("en", "leonor_gone")

    # Undecided, with the photo: gone at minute 15, and both decisions are refused with her sentence.
    play("go_print_shop", "request_copy", "go_study_room", "go_library", player="with photo")
    gone = at(15, "with photo")
    assert people_ids(gone) == [] and "leonor" in gone["night"]["gone"]
    assert gone["night"]["notice"] == empty_chair
    refuses_both_decisions("with photo", empty_chair)

    # Undecided, without the photo (the story would answer with its own blocked text).
    play("go_library", player="without photo")
    gone = at(15, "without photo")
    assert people_ids(gone) == [] and "leonor" in gone["night"]["gone"]
    assert gone["night"]["notice"] == empty_chair
    refuses_both_decisions("without photo", empty_chair)

    # Helping: she stays, saving her screenshots.
    play("go_print_shop", "request_copy", "go_study_room", "go_library", "ask_for_help", player="helping")
    late = at(29, "helping")
    assert "leonor" in people_ids(late) and "leonor" not in late["night"]["gone"]
    assert late["night"]["notice"] == ""

    # Accused: the story already emptied her table, and minute 15 changes nothing.
    play("go_print_shop", "request_copy", "go_study_room", "go_library", "accuse", player="accused")
    fourteen = at(14, "accused")
    asked_at_14 = call("play", player="accused", action="ask_for_help")
    fifteen = at(15, "accused")
    asked_at_15 = call("play", player="accused", action="ask_for_help")
    assert fifteen["texts"] == fourteen["texts"]
    assert asked_at_15["message"] == asked_at_14["message"]
    assert "leonor" not in fifteen["night"]["gone"] and fifteen["night"]["notice"] == ""


def test_the_room_text_starts_with_the_schedule_sentence():
    for language in ("en", "pt"):
        story = STORIES[language]
        rooms = [("print_shop", 10, shutter(language)), ("library", 15, schedule(language, "leonor_gone"))]
        for room, minute, sentence in rooms:
            player = f"{room} {language}"
            call(language=language, player=player)
            walk(room, player, language)
            opening = story["scenes"][room]["texts"][0]["text"]   # the story's opening paragraph of the room
            before = at(minute - 1, player, language)
            assert before["texts"] == logic.scene_text(story, game.load(player)), (room, language)
            assert before["texts"][0] == opening, (room, language)
            after = at(minute, player, language)
            assert after["texts"][0] == sentence, (room, language)
            assert opening not in after["texts"], (room, language)


def test_the_date_of_the_code_can_still_be_read_after_2225():
    for language in ("en", "pt"):
        player = f"date {language}"
        call(language=language, player=player)
        study = at(10, player, language)
        assert study["night"]["notice"] == "", language
        shop = walk("print_shop", player, language)
        first = shop["texts"][0]
        assert "17" in first, language   # the day of the code (17 October), on the slip
        assert shop["night"]["notice"] == first, language
    for language in ("en", "pt"):
        assert not shows(PAGE, shutter(language)), language


def test_the_closing_times_are_on_the_clue_rows_from_the_start():
    for language in ("en", "pt"):
        rows = call(language=language, player=f"new {language}")["clues"]
        assert {row["id"]: row["until"] for row in rows} == {
            "usb_stick": "", "original_photo": "22:25", "files_viewed": "", "leonor": "22:30"}, language
        assert not any(row["lost"] for row in rows), language
        assert all(set(row) == {"id", "label", "room", "done", "until", "lost"} for row in rows), language


def test_a_lost_photo_loses_leonor_too_and_no_longer_locks_the_auditorium():
    for way in ("door", "button"):
        player = f"lost by {way}"
        call(player=player)
        call("search", player=player, spot=search.PEN_SPOT)
        walk("computer_lab", player)
        unlock(player)
        do("save_backup", player)  # specs/computer-lab-backup.md: the auditorium needs the backup too
        at(9, player)
        assert not call("enter", player=player, room="auditorium")["accepted"], way   # still locked at 22:24
        ten = at(10, player)   # the walk stopped in the study room
        for clue in ("original_photo", "leonor"):
            assert clue_row(ten, clue)["lost"] is True and clue_row(ten, clue)["done"] is False, (way, clue)
        for clue in ("usb_stick", "files_viewed"):
            assert clue_row(ten, clue)["done"] is True and clue_row(ten, clue)["lost"] is False, (way, clue)
        if way == "door":
            entered = call("enter", player=player, room="auditorium")
        else:
            entered = call("play", player=player, action="go_auditorium")
        assert entered["accepted"] and entered["scene"] == "auditorium", way


def test_leonor_alone_is_lost_at_2230_when_the_photo_is_held():
    call()
    call("search", spot=search.PEN_SPOT)
    walk("print_shop")
    do("request_copy")
    walk("computer_lab")
    unlock()   # minute 1.5
    do("save_backup")   # specs/computer-lab-backup.md: away from computer 12 before the round at 22:27
    fourteen = at(14)
    assert clue_row(fourteen, "leonor")["lost"] is False and clue_row(fourteen, "leonor")["done"] is False
    assert not call("enter", room="auditorium")["accepted"]
    fifteen = at(15)
    assert clue_row(fifteen, "leonor")["lost"] is True and clue_row(fifteen, "leonor")["done"] is False
    assert clue_row(fifteen, "original_photo")["done"] is True and clue_row(fifteen, "original_photo")["lost"] is False
    assert call("enter", room="auditorium")["accepted"]


def test_the_story_rule_still_needs_the_old_files():
    call()
    call("search", spot=search.PEN_SPOT)
    ten = at(10)
    assert clue_row(ten, "original_photo")["lost"] and clue_row(ten, "leonor")["lost"]
    before = saved()
    door = call("enter", room="auditorium")
    button = call("play", action="go_auditorium")
    assert not door["accepted"] and not button["accepted"]
    assert door["scene"] == button["scene"] == "study_room"
    assert saved() == before


def test_a_night_that_lost_the_print_shop_ends_in_stolen_credit():
    call()
    call("search", spot=search.PEN_SPOT)
    walk("computer_lab")
    unlock()
    do("save_backup")  # specs/computer-lab-backup.md: the auditorium needs the backup too
    at(10)
    walk("auditorium")
    # The photo claim and the messages claim cannot be answered: the player says nothing to both.
    result = hear("files", "concede", "concede")
    assert result["hearing"]["doubts"] == 2
    assert result["ending"]["id"] == "stolen_credits" and game.load(PLAYER)["ending"] == "stolen_credits"


def test_the_reviewed_paths_never_meet_the_schedule():
    ended = play("open_drawer", "go_print_shop", "request_copy", "go_study_room", "go_library", "ask_for_help",
                 "go_study_room", "go_computer_lab", "view_files", "save_backup",
                 "go_study_room", "go_auditorium", "present_evidence")   # specs/computer-lab-backup.md
    assert ended["ending"]["id"] == "full_case"
    assert ended["night"]["minute"] == 2.5   # no report: only the copy (0.5), the decision and the files
    assert ended["night"]["gone"] == [] and ended["night"]["caught"] is False

    # The door note for a new game, with the two reviewed arguments and with the new optional one.
    new = game.load(call(player="newcomer")["player"])
    note = TEXT["en"]["auditorium_note"]
    assert campus.missing_clues_note(new, "en") == note
    assert campus.missing_clues_note(new, "en", minute=0) == note
    # people_in_room keeps its three reviewed arguments; the fourth, `gone`, is optional (point 5).
    assert [person["id"] for person in people.people_in_room("print_shop", new, "en")] == ["amelia"]
    assert people.people_in_room("print_shop", new, "en", gone=("amelia",)) == []


# ---------- The unknown number ----------

def test_the_warnings_come_at_minute_5_and_10_and_when_a_clue_is_lost():
    for language in ("en", "pt"):
        # Without the photo: `shop` from 5 to 9; at 10 the photo is lost, so Leonor is lost too: only `lost`.
        player = f"no photo {language}"
        call(language=language, player=player)
        for minute in range(4, 17):
            expected = {"shop"} if 5 <= minute <= 9 else {"lost"} if minute >= 10 else set()
            assert warnings_due(at(minute, player, language), language) == expected, (language, minute)

        # With the photo, Leonor undecided: no `shop`; `leonor` from 10 to 14; at 15 she is lost.
        player = f"photo {language}"
        play("go_print_shop", "request_copy", language=language, player=player)   # minute 0.5
        for minute in range(4, 17):
            expected = {"leonor"} if 10 <= minute <= 14 else {"lost"} if minute >= 15 else set()
            assert warnings_due(at(minute, player, language), language) == expected, (language, minute)

        # With the photo and Leonor helping: no warning and nothing lost.
        player = f"helping {language}"
        play("go_print_shop", "request_copy", "go_study_room", "go_library", "ask_for_help",
             language=language, player=player)
        for minute in (5, 10, 15):
            assert warnings_due(at(minute, player, language), language) == set(), (language, minute)


def test_the_warning_comes_one_minute_before_each_round_and_is_impersonal():
    call()
    for mark in (12, 19, 26):
        warning = f"round-{mark}"
        assert warning not in message_ids(at(mark - 2)), mark
        before = at(mark - 1)
        assert warning in message_ids(before), mark
        text = next(message["text"] for message in before["night"]["messages"] if message["id"] == warning)
        assert text == schedule("en", "round"), mark
        assert warning not in message_ids(at(mark)), mark   # not in the round's own minute
    assert "I " not in schedule("en", "round")   # it must not say who the unknown number is

    # Once Tomás has cracked, no round warning comes.
    investigate("cracked")
    crack_tomas("cracked")
    for mark in (12, 19, 26):
        assert not any(found.startswith("round-") for found in message_ids(at(mark - 1, "cracked"))), mark


# ---------- Duarte's rounds ----------

# Changed by specs/computer-lab-backup.md ("Reviewed tests that change"): Duarte now catches the player
# at computer 12, with the files open and the backup not saved yet (there is no chat any more).
def test_duarte_catches_the_player_at_computer_12():
    for language in ("en", "pt"):
        player = f"caught {language}"
        investigate(player, language, backup=False)   # minute 2.5, the files open at computer 12
        caught = at(12, player, language)
        assert not caught["accepted"] and caught["scene"] == "computer_lab", language
        flags = game.load(player)["flags"]
        assert flags["files_viewed"] is True and flags["backup_saved"] is False, language   # nothing else changes
        assert caught["night"]["minute"] == 15 and caught["night"]["charged"] == 3, language
        assert caught["night"]["caught"] is True and caught_note(player) == [12], language
        assert caught["message"] == schedule(language, "caught"), language
        assert "Duarte" in caught["message"], language


def test_a_charge_that_reaches_a_round_catches_too():
    investigate(backup=False)   # at computer 12 (specs/computer-lab-backup.md)
    at(10)
    rebuff = show("files", "tomas", "start")   # 2 minutes: 10 + 2 reaches the round at 12
    assert rebuff["confront"]["cracked"] is False and rebuff["confront"]["minutes"] == 2
    assert not rebuff["accepted"] and rebuff["scene"] == "computer_lab"
    assert rebuff["message"] == schedule("en", "caught")
    assert rebuff["night"]["minute"] == 15 and rebuff["night"]["charged"] == 2 + 3
    assert rebuff["night"]["caught"] is True and caught_note() == [12]


def test_one_report_that_passes_two_rounds_catches_once():
    investigate(backup=False)   # at computer 12 (specs/computer-lab-backup.md)
    assert at(11)["night"]["caught"] is False
    caught = at(20)   # passes 12 and 19: only the first round reached catches
    assert caught["night"]["minute"] == 23 and caught["night"]["charged"] == 3
    assert caught_note() == [12]


def test_a_round_is_reached_from_a_half_minute():
    def chat_at_eleven_and_a_half(player):
        """The copy at minute 9 (9.5), Leonor's help (10.5), the files (11.5), and the player stays at
        computer 12 without saving the backup (specs/computer-lab-backup.md: no chat any more)."""
        call(player=player)
        call("search", player=player, spot=search.PEN_SPOT)
        walk("print_shop", player)
        at(9, player)
        do("request_copy", player)
        walk("library", player)
        do("ask_for_help", player)
        walk("computer_lab", player)
        files = unlock(player)
        assert files["night"]["minute"] == 11.5 and files["night"]["caught"] is False

    # A report: 11.5 is below the round and 12 is at it.
    chat_at_eleven_and_a_half("report")
    caught = at(12, "report")
    assert caught["night"]["caught"] is True and caught["night"]["minute"] == 12 + 3
    assert caught_note("report") == [12]

    # A charge: 11.5 + 2 for a rebuff reaches the round, and the 3 minutes come on top.
    chat_at_eleven_and_a_half("rebuff")
    rebuff = show("files", "tomas", "start", "rebuff")
    assert not rebuff["accepted"] and rebuff["message"] == schedule("en", "caught")
    assert rebuff["night"]["minute"] == 11.5 + 2 + 3 and rebuff["night"]["charged"] == 2 + 3
    assert caught_note("rebuff") == [12]


def test_outside_the_chat_a_round_changes_nothing():
    investigate()   # in the computer lab, beside Tomás
    for room, mark in (("computer_lab", 12), ("study_room", 19)):
        if room == "study_room":
            walk("study_room")
        result = at(mark)
        assert result["scene"] == room, room
        assert result["night"]["minute"] == mark and result["night"]["charged"] == 0, room
        assert result["night"]["caught"] is False and caught_note() == [], room


def test_tomas_at_the_door_prevents_the_catch():
    investigate(backup=False)   # specs/computer-lab-backup.md: at computer 12, the backup not saved
    crack_tomas()
    door = at(12)
    assert door["accepted"] and door["scene"] == "computer_lab"   # the player stays at computer 12
    assert door["night"]["minute"] == 12 and door["night"]["charged"] == 0
    assert door["night"]["caught"] is False and caught_note() == []
    assert door["message"] == schedule("en", "door")


def test_being_caught_twice_costs_six_minutes_and_one_doubt():
    investigate(backup=False)   # minute 2.5   # specs/computer-lab-backup.md: at computer 12, the backup not saved
    first = at(12)
    assert first["night"]["minute"] == 12 + 3 and first["night"]["charged"] == 3
    second = at(19)   # still at computer 12: a catch moves nobody
    assert second["night"]["minute"] == 19 + 3 and second["night"]["charged"] == 3
    assert caught_note() == [12, 19]
    do("save_backup")
    walk("auditorium")
    hearing = answer("start")["hearing"]
    assert hearing["doubts"] == 1   # however many times it happened
    assert hearing["said"][0] == {"who": "professor", "name": "Professor", "text": CAUGHT_OPENING["en"]}
    assert hearing["said"][1] == {"who": "duarte", "name": "Duarte", "text": case().CASE_TEXT["en"]["claims"]["name"]}


def test_a_caught_player_who_fails_every_claim_still_has_three_doubts():
    investigate(backup=False)   # Leonor helps   # specs/computer-lab-backup.md: at computer 12, the backup not saved
    assert at(12)["night"]["caught"] is True
    do("save_backup")
    walk("auditorium")
    assert answer("start")["hearing"]["doubts"] == 1
    assert answer("concede")["hearing"]["doubts"] == 2
    assert answer("concede")["hearing"]["doubts"] == 3
    last = answer("concede")
    assert last["hearing"]["doubts"] == 3   # never counted above three
    assert last["ending"]["id"] == "stolen_credits"
    assert last["ending"]["verdict"] == case().CASE_TEXT["en"]["verdicts"]["three_help"]   # `three` when Leonor does not help


def test_a_catch_at_the_first_round_loses_an_undecided_leonor():
    play("open_drawer", "go_print_shop", "request_copy", "go_study_room", "go_computer_lab",
         "view_files")   # the photo is held, Leonor is undecided, minute 1.5, at computer 12 (specs/computer-lab-backup.md)
    caught = at(12)
    assert caught["night"]["caught"] is True and caught["night"]["minute"] == 15   # the 3 minutes end at 22:30
    assert clue_row(caught, "leonor")["lost"] is True and clue_row(caught, "leonor")["done"] is False
    walk("library")
    refuses_both_decisions(PLAYER, schedule("en", "leonor_gone"))


def test_a_damaged_caught_note_counts_as_not_caught():
    for number, damaged in enumerate(("yes", [5], 7)):
        player = f"damaged {number}"
        to_the_hearing(player)
        write_night_by_hand(player, json.dumps({"caught": damaged}), minute=db.load_night(player)["minute"])
        assert call(player=player)["night"]["caught"] is False, damaged
        hearing = answer("start", player)["hearing"]
        assert hearing["doubts"] == 0, damaged
        assert hearing["said"][0]["who"] == "duarte", damaged   # no opening line from the professor


def test_duarte_is_at_the_lab_door_only_around_a_round():
    call()   # in the study room the whole time: no catch
    places = [(10, "auditorium"), (11, "lab_door"), (12, "lab_door"), (13, "auditorium"),
              (17, "auditorium"), (18, "lab_door"), (19, "lab_door"), (20, "auditorium"),
              (24, "auditorium"), (25, "lab_door"), (26, "lab_door"), (27, "auditorium")]
    for minute, place in places:
        assert at(minute)["night"]["duarte"] == place, minute


# ---------- 22:45 ----------

def test_the_faculty_closes_at_2245():
    call()
    do("go_print_shop")
    do("request_copy")                                                                  # minute 0.5
    assert show("original_photo", "amelia", "start")["confront"]["cracked"] is False   # a valid confront (2 minutes)
    do("go_study_room")
    assert call("talk", npc="rita", node="start")["name"] == "Rita"                    # a valid talk
    closed = at(30)
    assert closed["night"]["closed"] is True and closed["night"]["minute"] == 30

    closed_text = TEXT["en"]["time_up_title"]
    before = saved()
    refused = [call("play", action="go_print_shop"), call("enter", room="print_shop"),
               call("search", spot=search.PEN_SPOT), call("unlock", code=search.PC12_CODE), answer("start")]
    for result in refused:
        assert not result["accepted"] and result["message"] == closed_text
    with pytest.raises(ValueError):
        call("talk", npc="rita", node="start")
    with pytest.raises(ValueError):
        show("original_photo", "rita", "start")
    assert saved() == before
    assert game.load(PLAYER)["scene"] == "study_room" and "usb_stick" not in game.load(PLAYER)["inventory"]

    # What still works: opening the game, reporting the time, and a restart.
    assert call()["night"]["closed"] is True
    assert at(30)["night"]["minute"] == 30
    assert saved() == before
    restarted = call("restart", confirmed=True)
    assert restarted["night"]["closed"] is False and restarted["night"]["minute"] == 0


# ---------- The balance, over the real tables ----------

def test_every_story_ending_has_a_route_at_15_30_45_and_60_seconds():
    for seconds in (15, 30, 45, 60):
        # Changed by specs/computer-lab-backup.md: three story endings, chosen by Leonor's decision.
        shown = {paced(seconds, route)["ending"] for route in (1, 2, 5)}
        assert {"stolen_credits", "impostor", "full_case"} <= shown, seconds


def test_a_careful_first_night_fits_at_45_seconds_with_two_minutes_left():
    for seconds in (43, 45, 47):
        night = paced(seconds, 7)
        assert night["ending"] == "full_case", (seconds, night)
        assert clock_rules().NIGHT_MINUTES - night["minute"] >= 2, (seconds, night)


def test_the_best_night_fits_at_45_seconds():
    # It fits at 45 seconds again because the copy costs half a minute (spec, point 13): 29.0 in the model.
    night = paced(45, 9)
    assert night["ending"] == "full_case" and night["doubts"] == 0, night
    assert clock_rules().NIGHT_MINUTES - night["minute"] >= 1, night


def test_being_caught_costs_three_minutes_and_one_doubt_and_the_night_still_ends():
    caught_cost = clock_rules().COSTS["caught"]
    for seconds in (15, 30):
        careful, caught = paced(seconds, 3), paced(seconds, 6)
        assert careful["ending"] == "full_case" and careful["doubts"] == 0 and not careful["caught"], seconds
        assert caught["ending"] is not None and caught["caught"] is True, (seconds, caught)
        assert caught["doubts"] == careful["doubts"] + 1, (seconds, caught)
        assert caught["charged"] == careful["charged"] + caught_cost == careful["charged"] + 3, (seconds, caught)


def test_doing_everything_does_not_fit_at_30_seconds():
    rules = clock_rules()
    lines = sum(len(polite_lines(person)) for person in people.PEOPLE["en"])
    commands = lines + sum(OTHER_COMMANDS.values())
    # Changed by specs/computer-lab-backup.md ("Reviewed tests that change"): opening the chat, the five
    # flags and closing it (7 commands) became one backup, and Leonor is no longer shown a card: 19
    # commands instead of 26.
    assert sum(OTHER_COMMANDS.values()) == 19
    # Every command at half a minute, except opening the table (QUICK_SECONDS) and the hands on the
    # pieces of the photo.
    real_minutes = ((commands - 1) * 30 + QUICK_SECONDS + photo_hands()) / 60
    # The smallest charges of such a night: the copy, the decision, the files, two right cards, Duarte's card.
    costs = rules.COSTS
    charges = (costs["request_copy"] + costs["ask_for_help"] + costs["view_files"] + 2 * costs["card_right"]
               + costs["card_duarte"])
    assert real_minutes + charges > rules.NIGHT_MINUTES, (lines, commands, real_minutes, charges)
    # Route 11 (not every polite line) lost the same commands, Tomás's conversation is shorter and Rita is
    # no longer asked about the USB stick once it is found (specs/two-answers.md, specs/evidence-after-monitors.md):
    # it now fits up to 35 seconds a command and no longer at 36.
    assert paced(35, 11)["ending"] == "full_case"
    assert paced(36, 11)["ending"] is None


# ---------- The texts, the page and the files ----------

def test_the_schedule_texts_exist_in_both_languages():
    assert TEXT["en"]["schedule"].keys() == TEXT["pt"]["schedule"].keys()
    for language in ("en", "pt"):
        for key in ("leonor_gone", "warn_shop", "warn_leonor", "lost", "round", "caught", "door"):
            assert schedule(language, key).strip(), (language, key)
        for key in ("todo_until", "todo_lost", "todo_hint_lost", "time_charged"):
            assert TEXT[language][key].strip(), (language, key)
        assert "{time}" in TEXT[language]["todo_until"], language
        assert "{n}" in TEXT[language]["time_charged"], language
        assert len(TEXT[language]["notices"]) == 4, language
    # `map_locked` is reworded: the auditorium now also opens when a clue is lost.
    assert TEXT["en"]["map_locked"] != "Closed until you have every clue"
    assert TEXT["pt"]["map_locked"] != "Fechado até teres todas as pistas"
    shutter_texts = clock_rules().SHUTTER
    assert set(shutter_texts) == {"en", "pt"}
    text_source = (FOLDER / "campus_text.py").read_text(encoding="utf-8")
    for language in ("en", "pt"):
        assert shutter_texts[language].strip(), language
        assert shutter_texts[language] not in text_source, language   # the date stays out of the page's texts


def test_the_page_follows_the_server_clock():
    new = ["function reportTime(", "function applyNight(", "night.charged", "report_at", "night.minute === 0",
           "night.notice"]
    kept = ["const COUNTDOWN_MINUTES = 30", "const running = !current.ending && !document.hidden && !shell.hidden",
            "if (option.cost) penalize(option.cost)"]
    for needle in new + kept:
        assert needle in PAGE, needle
    # PAGE holds every key of campus_text.py, used or not (page3d.py:79), so these are looked for in play.js.
    play_js = (FOLDER / "play.js").read_text(encoding="utf-8")
    for key in ("todo_until", "todo_lost"):
        assert key in play_js, key
    assert '"time"' in play_js or "'time'" in play_js   # the page sends the new operation


def test_old_operations_still_refuse_extra_fields():
    assert "night" in call()   # a valid `open` first: it returns the night
    before = saved()
    for bad in (dict(operation="play", action="go_print_shop", minute=5),
                dict(operation="talk", npc="rita", node="start", minute=5),
                dict(operation="enter", room="library", minute=5),
                dict(operation="open", minute=5)):
        with pytest.raises(ValueError):
            call(**bad)
    assert saved() == before


def test_app_3d_reloads_campus_clock_before_the_modules_that_use_it():
    source = (PROJECT / "app_3d.py").read_text(encoding="utf-8")   # read, not run: running it starts Streamlit
    after_name = source.split("CODE_MODULES = ", 1)[1]
    modules = ast.literal_eval(after_name[:after_name.index("]") + 1])   # the list, as Python would read it
    assert modules.index("campus_case") < modules.index("campus_clock") < modules.index("campus_evidence")
    # Comments are left out of both checks: a comment may well say why the module is not there.
    page_files = code_only(source.split("PAGE_FILES = ", 1)[1].split("def page_version", 1)[0])
    assert "campus_clock" not in page_files
    page3d_source = (FOLDER / "page3d.py").read_text(encoding="utf-8")
    imports = [line for line in code_only(page3d_source).splitlines()
               if line.strip().startswith(("import ", "from ")) or "import_module" in line]
    assert len(imports) >= 4   # the import lines were found
    assert not any("campus_clock" in line for line in imports)
