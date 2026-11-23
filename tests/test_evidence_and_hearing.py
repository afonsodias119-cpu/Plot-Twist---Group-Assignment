"""Evidence cards, confrontations and the hearing (specs/evidence-and-hearing.md).

Written before the code: one test for every line under "Checks" in the spec, in the same order.

How to read this file:
- "saves nothing" means the database file has the same bytes before and after (`saved()`).
- A test that expects a ValueError first sends one valid request of the same operation and checks
  its reply. Without that, the test would pass today for the wrong reason ("Unknown operation").
- The two new modules (campus_case, campus_evidence) are imported inside `case()`, not at the top,
  so pytest can read this file while they do not exist yet.
- The spec does not say how CASE_TEXT is organised inside each language, so no test reads a text
  of it by its key: `flat()` walks through the whole table instead. The few lines a check names
  are copied in LINES below.
- No game here shows more than 6 minutes of cards (three rebuffs, or six cards to Duarte). With
  the 3 minutes specs/night-schedule.md charges for the copy, the decision and the files, that is
  minute 9 at most, before anything of the schedule happens (minute 10).
- "Each card in its own game" is done by playing a new game under another player name. Nothing is
  copied or put back by hand: the only rows written by hand are the damaged and left-behind ones.
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

# The cards, in the order the hand shows them (spec, point 4).
# Changed by specs/computer-lab-backup.md ("Reviewed tests that change"): the five flagged messages are gone.
CARDS = ["original_photo", "files", "backup"]
# Changed by specs/computer-lab-backup.md ("Reviewed tests that change"): the proofs are the photo, the files and the backup;
# the facts won by cracking a person stay in the night's notes and are never cards.
FACT_CARDS = {"tomas_word", "rita_word"}

# The lines a check names, word for word as in the dialogue script (docs/guiao-conversas.md, section
# "Provas, confrontos e audiência"). Every other expected text is read from the game's own tables.
LINES = {
    "en": {
        # Spec, point 7: what Tomás says when he reads the history of the slides (specs/computer-lab-backup.md).
        "tomas_reveal": '"So the message says Duarte did them. The files say I did."',
        # The rebuffs: one line for each person, for any other card or any other line.
        "tomas_rebuff": 'Tomás glances at it and back at his screen. "And what does that have to do with what I just said?"',
        "rita_rebuff": 'Rita looks at it, then back at her laptop. "And? I do not see what that changes."',
        "leonor_rebuff": 'Leonor looks at what you are holding, then at you. "If you want to show me something, say what you want from me."',
        "clerk_rebuff": 'The clerk looks over her glasses. "I print things. I do not judge them. Is there anything you need printed?"',
        "professor_rebuff": 'The professor does not take it. "Not like this. Present your evidence properly, when you are ready."',
        "duarte": 'Duarte does not look at it. "Keep it for the professor. I will be sitting in the front row."',
        # The hearing: Duarte's first claim, and his line when the player says nothing.
        "claim_name": 'Duarte stands up without hurry. "Professor, open the report. My name is on the cover. It has been there since the first draft."',
        "nothing": 'The professor waits. Duarte smiles. "Nothing?"',
        # The professor, on any card that does not break the claim `name` (its general wrong line).
        "name_wrong": '"That does not tell me who wrote a report." He makes a small mark on the list.',
        # The professor, on the card `files` shown against the claim `photo`.
        "history": '"The history says a photo was swapped. It does not show me the one that was there before."',
        # The verdict lines (spec, point 11), by their key.
        "three": '"Three times tonight you gave me a reason to doubt you. I cannot cross out a name on a guess."',
        "three_help": 'The professor closes the list before Leonor reaches the door. "I have heard enough guesses for one night."',
        "two": '"You are right about him, I think. But you made me doubt you twice tonight, and I write down only what I am sure of."',
        "unused_no_originals": "The professor looks at Duarte's phone for a long moment. \"One message is answered. He has a phone full of them, and nobody from your group is here to confirm your backup.\"",
    },
    "pt": {
        "tomas_reveal": '"Então a mensagem diz que foi o Duarte. Os ficheiros dizem que fui eu."',
        "unused_no_originals": 'O professor fica muito tempo a olhar para o telemóvel do Duarte. "Uma mensagem está respondida. Ele tem um telemóvel cheio delas, e ninguém do teu grupo está aqui para confirmar o teu backup."',
    },
}


# ---------- helpers: requests ----------

def call(operation="open", language="en", player=PLAYER, **extra):
    """One request to the server, exactly as the page sends it."""
    return campus.command(dict(operation=operation, language=language, player=player, **extra))


def saved():
    """The bytes of the database file: equal before and after means nothing was written."""
    return db.DB_PATH.read_bytes()


def case():
    """The case file (campus_case.py). Imported here so this file can be collected before it exists."""
    return importlib.import_module("campus_case")


def play(*actions, language="en", player=PLAYER):
    """Open the game and play these story actions in order. Each one must be accepted."""
    result = call("open", language, player)
    for action in actions:
        result = call("play", language, player, action=action)
        assert result["accepted"], action
    return result


def walk(room, player=PLAYER, language="en"):
    """Walk through the door of a room (the `enter` operation)."""
    result = call("enter", language, player, room=room)
    assert result["accepted"], room
    return result


# ---------- helpers: the steps that give the cards ----------

def investigate(player=PLAYER, language="en", leonor="ask_for_help"):
    """A new game played up to the computer lab: the USB stick, the original photo, the decision
    about Leonor ("ask_for_help" or "accuse"), the old files and the backup of the conversations.

    The player then holds `original_photo`, `files` and `backup`,
    and stands beside Tomás. Changed by specs/computer-lab-backup.md: no chat messages are flagged.
    """
    steps = ["open_drawer", "go_print_shop", "request_copy", "go_study_room",
             "go_library", leonor, "go_study_room", "go_computer_lab", "view_files", "save_backup"]
    if leonor is None:   # no decision: Leonor is never asked (to_the_hearing then lets her leave)
        steps = ["open_drawer", "go_print_shop", "request_copy", "go_study_room", "go_computer_lab", "view_files", "save_backup"]
    return play(*steps, language=language, player=player)


def show(card, npc, node, player=PLAYER, language="en"):
    """Show one card to a person on one of their lines (the `confront` operation)."""
    return call("confront", language, player, npc=npc, node=node, evidence=card)


def crack_tomas(player=PLAYER, language="en"):
    """In the computer lab: the file history on his claim line cracks him (specs/computer-lab-backup.md)."""
    reply = show("files", "tomas", "slides", player, language)
    assert reply["confront"]["cracked"] is True
    return reply


def crack_rita(player=PLAYER, language="en"):
    """With the original photo: walk to the study room and break her claim line."""
    walk("study_room", player, language)
    reply = show("original_photo", "rita", "five", player, language)
    assert reply["confront"]["cracked"] is True
    return reply


def everything(player=PLAYER, language="en"):
    """A night that holds every card and ends standing in the auditorium. No card is charged."""
    investigate(player, language)
    crack_tomas(player, language)
    crack_rita(player, language)
    return walk("auditorium", player, language)


def ids(result):
    """The ids of the cards in a snapshot, in the order they are listed."""
    return [card["id"] for card in result["evidence"]]


def label_of(result, card):
    return next(c["label"] for c in result["evidence"] if c["id"] == card)


def answers_of(reply):
    """The line ids a `talk` reply offers."""
    return [option["next"] for option in reply["options"]]


# ---------- helpers: the hearing ----------

def to_the_hearing(player=PLAYER, language="en", leonor="ask_for_help", tomas=False):
    """A whole investigation and then into the auditorium. `tomas=True` cracks Tomás on the way.

    `leonor=None`: she is never asked, and the night is moved to 22:30, when she leaves undecided; her
    clue is lost, the auditorium opens and the story's ending is "stolen_credits" (specs/computer-lab-backup.md:
    accusing her now gives "impostor")."""
    investigate(player, language, leonor)
    if tomas:
        crack_tomas(player, language)
    if leonor is None:
        assert call("time", language, player, minute=15)["accepted"]
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


def reply_to_the_last_answer(hearing):
    """The line said right after the player's last answer (the professor's, or Duarte's after "Say nothing")."""
    said = hearing["said"]
    last = max(index for index, entry in enumerate(said) if entry["who"] == "you")
    return said[last + 1]


def story_ending(language, ending_id):
    return next(ending for ending in STORIES[language]["endings"] if ending["id"] == ending_id)


def check_ending(result, player, language, saved_id, shown_id, verdict):
    """The ending on the screen is the story's `shown_id`, with its own title and text and this
    verdict line beside it; the row in `games` keeps the story's own ending, `saved_id`."""
    ending = result["ending"]
    expected = story_ending(language, shown_id)
    assert ending["id"] == shown_id
    assert ending["title"] == expected["title"] and ending["text"] == expected["text"]   # the verdict is never joined to the text
    assert ending["verdict"] == verdict
    assert game.load(player)["ending"] == saved_id


# ---------- helpers: the texts of the case file ----------

def flat(table, place=""):
    """Every text of a table as {place: text}, whatever its layout (dictionaries and lists inside
    each other). The place is the path of keys, for example "/rebuff/tomas"."""
    if isinstance(table, str):
        return {place: table}
    if not isinstance(table, (dict, list, tuple)):
        return {}   # a number or None (a trust, a missing note) is not a text
    found = {}
    for key, value in (table.items() if isinstance(table, dict) else enumerate(table)):
        found.update(flat(value, f"{place}/{key}"))
    return found


def case_texts(language):
    """The sentences of the case file in one language: labels, reveals, rebuffs, claims, the
    professor's lines and the verdict lines. A text of three words or fewer is a name, not a secret."""
    texts = [text for text in flat(case().CASE_TEXT[language]).values() if len(text.split()) > 3]
    assert len(texts) >= 20, "the case file is almost empty"
    return texts


def shows(where, text):
    """True when `text` is inside `where` (a page or a reply turned into text), also in the way JSON
    writes it: a quote becomes \\" and, in the page, an accented letter becomes \\u00e1."""
    forms = {text, json.dumps(text)[1:-1], json.dumps(text, ensure_ascii=False)[1:-1]}
    return any(form in where for form in forms)


def as_text(result):
    """A reply as one text, to search it for sentences that should not be there."""
    return json.dumps(result, ensure_ascii=False)


QUOTE = re.compile(r'"([^"]+)"|«([^»]+)»|“([^”]+)”')   # the three kinds of quotation marks play.js knows


def quotes(text):
    """What is between quotation marks in a text."""
    return [(match.group(1) or match.group(2) or match.group(3)).strip() for match in QUOTE.finditer(text)]


def is_spoken(quote):
    """The rule of partsOf in play.js: a quote is spoken when it has more than three words or . ! ? …"""
    return len(quote.split()) > 3 or any(mark in quote for mark in ".!?…")


def code_only(text):
    """A source text without its comments, so a comment that explains a rule cannot fail a check."""
    return "\n".join(line.split("#")[0] for line in text.splitlines())


# ---------- helpers: the table `nights`, read and written by hand ----------

def table_names():
    with closing(sqlite3.connect(db.DB_PATH)) as connection:
        return {row[0] for row in connection.execute("SELECT name FROM sqlite_master WHERE type = 'table'")}


def cracked(player=PLAYER):
    """Who was cracked tonight, from the night's notes (the facts are not cards any more)."""
    return db.load_night(player)["notes"].get("cracked", [])


def night_row(player):
    """The row of `nights` of this player as (minute, notes), or None when there is no row."""
    with closing(sqlite3.connect(db.DB_PATH)) as connection:
        return connection.execute("SELECT minute, notes FROM nights WHERE player = ?", (player,)).fetchone()


def write_night_by_hand(player, notes):
    """Put a row in `nights` with any text as its notes, the way a damaged file would have it."""
    with closing(sqlite3.connect(db.DB_PATH)) as connection, connection:
        connection.execute("INSERT OR REPLACE INTO nights (player, minute, notes) VALUES (?, 0, ?)", (player, notes))


# ---------- The table and the notes ----------

def test_the_database_has_a_nights_table_beside_games():
    db.init_db()
    db.init_db()   # a second call changes nothing and does not fail
    assert {"games", "nights"} <= table_names()
    with closing(sqlite3.connect(db.DB_PATH)) as connection:
        # Each row of table_info is (position, name, type, not null, default, primary key).
        columns = [(row[1], row[2], row[3], row[5]) for row in connection.execute("PRAGMA table_info(nights)")]
    assert columns == [("player", "TEXT", 0, 1), ("minute", "INTEGER", 1, 0), ("notes", "TEXT", 1, 0)]

    # A file from before this feature: it has a saved game and no `nights` table.
    call()
    with closing(sqlite3.connect(db.DB_PATH)) as connection, connection:
        connection.execute("DROP TABLE IF EXISTS nights")
    assert "nights" not in table_names()
    db.init_db()
    assert {"games", "nights"} <= table_names()
    assert game.load(PLAYER) == STORIES["en"]["start"]   # the saved game is still there


def test_reading_a_night_that_was_never_saved_gives_an_empty_one_and_saves_nothing():
    call()
    before = saved()
    assert db.load_night("nobody") == {"minute": 0, "notes": {}}
    assert db.load_night(PLAYER) == {"minute": 0, "notes": {}}   # a game that has no notes yet
    assert saved() == before

    # The other two names the spec fixes (point 1); specs/night-schedule.md builds on them.
    notes = {"cracked": ["tomas"], "hearing": ["files", "concede"], "verdict": ""}   # the example row of the spec
    db.save_night("ana", 0, notes)
    assert night_row("ana")[0] == 0 and json.loads(night_row("ana")[1]) == notes
    assert db.load_night("ana") == {"minute": 0, "notes": notes}
    db.save_night("ana", 0, {})   # a second save replaces the row
    assert db.load_night("ana") == {"minute": 0, "notes": {}}
    write_night_by_hand("ana", "not json")
    before = saved()
    assert db.load_night("ana") == {"minute": 0, "notes": {}}   # a row that cannot be read
    assert saved() == before   # and reading it repairs nothing
    db.delete_night("ana")
    assert night_row("ana") is None
    db.delete_night("ana")   # deleting what is not there raises nothing
    assert db.load_night(PLAYER) == {"minute": 0, "notes": {}} and game.load(PLAYER) is not None   # nobody else is touched


def test_a_damaged_notes_row_counts_as_empty_and_cannot_help():
    damaged = ["not json", "[]", '{"cracked": ["duarte", 7], "hearing": "x", "verdict": "full_case"}']
    for number, notes in enumerate(damaged):
        player = f"damaged {number}"
        to_the_hearing(player, leonor="accuse")   # Leonor is accused: the story's ending is "impostor" (specs/computer-lab-backup.md)
        write_night_by_hand(player, notes)
        before = saved()
        result = call(player=player)   # raises nothing
        assert not FACT_CARDS & set(ids(result)), notes
        assert result["hearing"] is None, notes
        # `talk` reads the notes too (to hide the broken claims): it raises nothing either.
        assert call("talk", player=player, npc="professor", node="start")["name"] == "Professor", notes
        assert saved() == before, notes   # cleaning happens in memory: the damaged row is not repaired

        # An ended game with the same damaged row: the "verdict" written by hand cannot improve the ending.
        assert call("play", player=player, action="present_evidence")["accepted"]
        write_night_by_hand(player, notes)
        ended = call(player=player)
        check_ending(ended, player, "en", saved_id="impostor", shown_id="impostor", verdict="")
        assert ended["hearing"] is None, notes

        # The same verdict beside a hearing that is valid: three right answers on a night whose story
        # ending is "impostor" could never have produced "full_case", so it is dropped all the same.
        write_night_by_hand(player, '{"hearing": ["files", "original_photo", "backup"], "verdict": "full_case"}')
        check_ending(call(player=player), player, "en", saved_id="impostor", shown_id="impostor", verdict="")

    # What is understood is kept and the rest is dropped (spec, point 2): Tomás has a confrontation,
    # Duarte and the number 7 have none.
    to_the_hearing("half")
    write_night_by_hand("half", '{"cracked": ["tomas", "duarte", 7]}')
    rules = importlib.import_module("campus_evidence")   # the notes as the server reads them, cleaned
    assert not FACT_CARDS & set(ids(call(player="half")))   # specs/computer-lab-backup.md: facts are not cards
    assert rules.read_night("half", game.load("half"))["cracked"] == ["tomas"]
    # `hearing` is a list of at most three answers, each "concede" or the id of a card.
    for notes in ('{"hearing": ["knife"]}', '{"hearing": [7]}', '{"hearing": ["files", "concede", "files", "concede"]}'):
        write_night_by_hand("half", notes)
        assert call(player="half")["hearing"] is None, notes
    write_night_by_hand("half", '{"hearing": []}')
    assert call(player="half")["hearing"]["step"] == 1   # in the auditorium an empty list is a hearing that has started

    # The same row counts only in the auditorium: it cannot lock a player who is still in the study room.
    call(player="early")
    write_night_by_hand("early", '{"hearing": []}')
    assert call(player="early")["hearing"] is None
    assert call("play", player="early", action="go_print_shop")["accepted"]


def test_a_restart_and_a_new_game_wipe_the_night():
    investigate()
    crack_tomas()
    assert night_row(PLAYER) is not None

    # An unconfirmed restart changes nothing. (No valid restart can come first here: it would wipe
    # the very notes this part looks at. The test already fails without `confront`, two lines above.)
    before = saved()
    with pytest.raises(ValueError):
        call("restart", confirmed=False)
    assert saved() == before
    assert cracked() == ["tomas"]   # Changed by specs/computer-lab-backup.md ("Reviewed tests that change"): a fact, not a card

    # A confirmed restart: no row is left, and playing the same steps again does not bring the fact back.
    restarted = call("restart", confirmed=True)
    assert restarted["evidence"] == []
    assert night_row(PLAYER) is None
    investigate()
    assert cracked() == []

    # A row left behind for a name that has no saved game: `open` starts a new game and deletes it.
    write_night_by_hand("ghost", '{"cracked": ["tomas"]}')
    assert call(player="ghost")["evidence"] == []
    assert night_row("ghost") is None


# ---------- The cards ----------

def expect_hand(result, held):
    """The hand has exactly the cards of `held`, in the order of the spec (point 4)."""
    assert ids(result) == [card for card in CARDS if card in held], held


def test_the_hand_lists_only_what_the_player_holds():
    assert call()["evidence"] == []
    expect_hand(call("play", action="open_drawer"), [])   # the USB stick is not a card
    call("play", action="go_print_shop")
    held = ["original_photo"]
    expect_hand(call("play", action="request_copy"), held)
    call("play", action="go_study_room")
    call("play", action="go_library")
    # Changed by specs/computer-lab-backup.md ("Reviewed tests that change"): Leonor's screenshots are not a card any more,
    # the backup is, and cracking Tomás or Rita gives a fact in the notes, not a card.
    expect_hand(call("play", action="ask_for_help"), held)
    call("play", action="go_study_room")
    expect_hand(call("play", action="go_computer_lab"), held)   # walking gives nothing
    held += ["files"]
    expect_hand(call("play", action="view_files"), held)
    held += ["backup"]
    expect_hand(call("play", action="save_backup"), held)
    expect_hand(crack_tomas(), held)
    expect_hand(crack_rita(), held)
    assert cracked() == ["tomas", "rita"]
    assert ids(call()) == CARDS   # all of them, and every card has a label
    assert all(card["label"].strip() for card in call()["evidence"])
    assert all(set(card) == {"id", "label"} for card in call()["evidence"])

    # Accusing Leonor changes nothing in the hand.
    assert ids(investigate(player="accuser", leonor="accuse")) == CARDS


def test_card_labels_follow_the_saved_language():
    investigate(language="pt")
    reveal = crack_tomas(language="en")["confront"]   # the request says English; the game was saved in Portuguese
    assert LINES["pt"]["tomas_reveal"] in reveal["text"] and reveal["text"] in case_texts("pt")
    result = call("open", "en")
    assert ids(result) == ["original_photo", "files", "backup"]   # specs/computer-lab-backup.md
    portuguese, english = case_texts("pt"), case_texts("en")
    for card in result["evidence"]:
        assert card["label"] in portuguese and card["label"] not in english, card["id"]


def test_no_card_shows_a_clue_before_it_is_found():
    secrets = case_texts("en") + case_texts("pt")
    for language in ("en", "pt"):
        result = call(language=language, player=f"new {language}")
        assert result["evidence"] == []
        text = as_text(result)
        assert "23h47" not in text and "11:47" not in text   # the same clue, as each story writes it
        assert [secret for secret in secrets if shows(text, secret)] == []


# ---------- Confronting ----------

def test_the_right_card_on_the_claim_line_cracks_tomas_and_it_is_saved():
    investigate()
    state = game.load(PLAYER)
    reply = show("files", "tomas", "slides")  # specs/computer-lab-backup.md: the file history breaks Tomás's claim now
    assert game.load(PLAYER) == state   # only the notes are written: the saved game is as it was
    assert db.load_night(PLAYER)["notes"]["cracked"] == ["tomas"]
    confront = reply["confront"]
    assert confront["npc"] == "tomas" and confront["name"] == "Tomás"
    assert confront["cracked"] is True and confront["trust"] == 3 and confront["minutes"] == 0
    assert LINES["en"]["tomas_reveal"] in confront["text"] and confront["text"] in case_texts("en")
    assert confront["note"].strip()
    assert "tomas_word" not in ids(reply)   # specs/computer-lab-backup.md: a fact in the notes, not a card
    assert cracked() == ["tomas"]   # saved: still there when the game is opened again


def test_rita_cracks_with_the_file_history_or_with_the_original_photo():
    # With the file history.
    investigate(player="with files")
    walk("study_room", player="with files")
    # Not any card: the backup says nothing about a photo (one rebuff: 2 minutes in this game).
    wrong = show("backup", "rita", "five", player="with files")
    assert wrong["confront"]["cracked"] is False and wrong["confront"]["minutes"] == 2
    assert wrong["confront"]["name"] == "Rita" and wrong["confront"]["text"] == LINES["en"]["rita_rebuff"]
    assert wrong["confront"]["trust"] is None and wrong["confront"]["note"] == ""
    assert cracked("with files") == []

    reply = show("files", "rita", "five", player="with files")
    assert reply["confront"]["cracked"] is True and reply["confront"]["minutes"] == 0
    assert reply["confront"]["trust"] is None   # Rita has no hearts
    assert reply["confront"]["text"] in case_texts("en") and reply["confront"]["note"].strip()
    assert cracked("with files") == ["rita"]   # specs/computer-lab-backup.md: a fact, not a card

    # With the original photo alone: the files were never viewed in this game.
    play("open_drawer", "go_print_shop", "request_copy", "go_study_room", player="with photo")
    reply = show("original_photo", "rita", "five", player="with photo")
    assert reply["confront"]["cracked"] is True and reply["confront"]["minutes"] == 0
    assert ids(reply) == ["original_photo"] and cracked("with photo") == ["rita"]


# Changed by specs/computer-lab-backup.md ("Reviewed tests that change"): Leonor is no longer convinced
# with a card, and Tomás's word is a fact in the notes, not a card that can be shown.
def test_leonor_is_not_cracked_by_any_card():
    investigate()
    crack_tomas()
    walk("library")
    reply = show("files", "leonor", "sure")
    assert reply["confront"]["cracked"] is False and reply["confront"]["minutes"] == 2
    assert reply["confront"]["text"] == LINES["en"]["leonor_rebuff"]
    before = saved()
    with pytest.raises(ValueError):
        show("tomas_word", "leonor", "sure")
    assert saved() == before
    assert "sure" in answers_of(call("talk", npc="leonor", node="start"))   # her claim is still there


# Changed by specs/two-answers.md ("Reviewed tests that change"): Tomás's slides are asked after the password.
def test_a_broken_claim_is_not_offered_again():
    investigate()
    assert "slides" in answers_of(call("talk", npc="tomas", node="password"))
    assert call("talk", npc="tomas", node="slides")["node"] == "slides"   # a valid `talk` first
    crack_tomas()                                                         # and a valid `confront`
    before = saved()
    offered = answers_of(call("talk", npc="tomas", node="password"))   # reading the notes writes nothing
    assert offered == ["hard"]   # only the answer to the broken claim is gone
    with pytest.raises(ValueError):
        call("talk", npc="tomas", node="slides")
    with pytest.raises(ValueError):
        show("files", "tomas", "slides")
    assert saved() == before


def test_any_other_card_gets_the_rebuff_and_costs_two_minutes():
    investigate()
    reply = show("original_photo", "tomas", "slides")  # specs/computer-lab-backup.md: the file history breaks Tomás's claim now
    confront = reply["confront"]
    assert confront["cracked"] is False and confront["text"] == LINES["en"]["tomas_rebuff"]
    assert confront["trust"] is None and confront["note"] == "" and confront["minutes"] == 2
    assert not FACT_CARDS & set(ids(reply))
    assert not FACT_CARDS & set(ids(call()))


def test_the_right_card_on_another_line_does_not_crack():
    investigate()
    for node in ("start", "kind", "who"):   # three rebuffs: 6 minutes (specs/two-answers.md: no msg5 line)
        confront = show("files", "tomas", node)["confront"]
        assert confront["cracked"] is False and confront["minutes"] == 2, node
        assert confront["text"] == LINES["en"]["tomas_rebuff"], node
    assert "tomas_word" not in ids(call())


def test_duarte_answers_any_card_with_one_line_for_one_minute():
    for number, card in enumerate(CARDS):
        player = f"duarte {number}"   # each card in its own game, on two of his lines: 2 minutes
        everything(player)
        for node in ("start", "part"):
            reply = show(card, "duarte", node, player)
            confront = reply["confront"]
            assert confront["npc"] == "duarte" and confront["name"] == "Duarte", (card, node)
            assert confront["cracked"] is False and confront["text"] == LINES["en"]["duarte"], (card, node)
            # His line is not a reveal: the hearts stay as they were and nothing goes in the diary.
            assert confront["trust"] is None and confront["note"] == "" and confront["minutes"] == 1, (card, node)
            assert ids(reply) == CARDS


def test_the_clerk_and_the_professor_only_rebuff():
    play("open_drawer", "go_print_shop", "request_copy", player="at the shop")
    clerk = show("original_photo", "amelia", "start", player="at the shop")["confront"]
    to_the_hearing(player="at the end")
    professor = show("files", "professor", "start", player="at the end")["confront"]
    for confront in (clerk, professor):
        assert confront["cracked"] is False and confront["minutes"] == 2
        assert confront["trust"] is None and confront["note"] == ""
    assert clerk["name"] == "Clerk" and clerk["text"] == LINES["en"]["clerk_rebuff"]
    assert professor["name"] == "Professor" and professor["text"] == LINES["en"]["professor_rebuff"]
    assert not FACT_CARDS & set(ids(call(player="at the shop")) + ids(call(player="at the end")))


def test_a_card_the_player_does_not_hold_is_rejected_and_saves_nothing():
    investigate()   # Tomás is not cracked
    assert show("original_photo", "tomas", "slides")["confront"]["cracked"] is False   # a valid request first
    before = saved()
    for card in ("rita_word", "tomas_word"):   # specs/computer-lab-backup.md: no flagged messages any more
        with pytest.raises(ValueError):
            show(card, "tomas", "slides")
    assert saved() == before


def test_unknown_person_card_and_line_are_rejected_and_save_nothing():
    # In the lab with the photo, before the files are viewed: Tomás's line `slides` cannot be reached yet.
    play("open_drawer", "go_print_shop", "request_copy", "go_study_room", "go_computer_lab")
    assert show("original_photo", "tomas", "start")["confront"]["cracked"] is False   # a valid request first
    before = saved()
    bad_requests = [
        dict(npc="nobody", node="start", evidence="original_photo"),
        dict(npc="computer12", node="start", evidence="original_photo"),
        dict(npc=7, node="start", evidence="original_photo"),
        dict(npc="tomas", node="start", evidence="knife"),
        dict(npc="tomas", node="start", evidence=["msg_5"]),
        dict(npc="tomas", node="nope", evidence="original_photo"),
        dict(npc="tomas", node="slides", evidence="original_photo"),
        dict(npc="tomas", node=7, evidence="original_photo"),            # a line is a text:
        dict(npc="tomas", node=["start"], evidence="original_photo"),    # a list must not raise a TypeError
    ]
    for bad in bad_requests:
        with pytest.raises(ValueError):
            call("confront", **bad)
    assert saved() == before


def test_confront_needs_the_person_in_the_saved_room_no_ending_and_exact_fields():
    investigate()
    assert show("files", "tomas", "start")["confront"]["cracked"] is False   # a valid request first
    before = saved()
    with pytest.raises(ValueError):   # a missing field
        call("confront", npc="tomas", node="start")
    with pytest.raises(ValueError):   # an extra field
        call("confront", npc="tomas", node="start", evidence="files", extra=1)
    assert saved() == before

    walk("study_room")
    before = saved()
    with pytest.raises(ValueError):   # Tomás is in the computer lab
        show("files", "tomas", "start")
    assert saved() == before

    walk("auditorium")
    assert call("play", action="present_evidence")["ending"] is not None
    before = saved()
    for person in ("professor", "duarte"):   # nobody can be shown a card after the ending
        with pytest.raises(ValueError):
            show("files", person, "start")
    assert saved() == before


def test_the_reply_never_says_which_card_is_right():
    investigate()
    reply = show("original_photo", "tomas", "slides")   # a rebuff: the right card would have been files
    confront = reply["confront"]
    assert set(confront) == {"npc", "name", "cracked", "text", "trust", "note", "minutes"}
    assert not any(value in CARDS for value in confront.values() if isinstance(value, str))
    assert ids(reply) == ["original_photo", "files", "backup"]   # only what is held

    # Of the whole case file, the reply may contain the rebuff it gives and the labels of the cards
    # held, and nothing else: no reveal, in either language.
    text = as_text(reply)
    allowed = [confront["text"]] + [card["label"] for card in reply["evidence"]]
    leaked = [secret for secret in case_texts("en") + case_texts("pt") if shows(text, secret) and secret not in allowed]
    assert leaked == []
    assert LINES["en"]["tomas_reveal"] not in text and LINES["pt"]["tomas_reveal"] not in text


# ---------- The dialogue ----------

# person: (the existing line that gains an answer, the new line that answer leads to)
# specs/two-answers.md: Tomás's slides are asked after the password.
NEW_LINES = {"tomas": ("password", "slides"), "rita": ("photo", "five"), "leonor": ("start", "mine")}


def line_shape(nodes, node):
    """What must be equal in both languages: where the answers lead, their conditions, trust, and having a note."""
    line = nodes[node]
    return ([(o["next"], o.get("if")) for o in line["options"]], line.get("trust"), bool(line.get("note")))


def test_the_new_lines_have_the_same_shape_in_both_languages():
    for person, (old, new) in NEW_LINES.items():
        en, pt = people.PEOPLE["en"][person]["nodes"], people.PEOPLE["pt"][person]["nodes"]
        assert new in en and new in pt, new
        assert line_shape(en, new) == line_shape(pt, new) and line_shape(en, old) == line_shape(pt, old), new
        for nodes in (en, pt):
            leading = [option for option in nodes[old]["options"] if option["next"] == new]
            assert len(leading) == 1, new
            assert not any("cost" in option for option in leading + nodes[new]["options"]), new
    for person, confrontation in case().CONFRONT.items():
        for language in ("en", "pt"):
            assert confrontation["node"] in people.PEOPLE[language][person]["nodes"], person

    # The wording the spec itself gives (points 7 and 8): the new answers and what the claim lines say.
    tomas, rita = people.PEOPLE["en"]["tomas"]["nodes"], people.PEOPLE["en"]["rita"]["nodes"]
    assert [o["label"] for o in tomas["password"]["options"] if o["next"] == "slides"] == ["Ask who made the slides"]
    assert [o["label"] for o in rita["photo"]["options"] if o["next"] == "five"] == ["Ask why the photo in the folder shows five"]
    assert "the chat says Duarte did them, under my name. So maybe he did, and I only tidied up." in tomas["slides"]["text"]
    assert "A photo cannot change. My memory can." in rita["five"]["text"]
    assert len(tomas["kind"]["options"]) == 2 and len(rita["photo"]["options"]) == 2   # specs/two-answers.md

    # The names the spec fixes in the two new modules (point 3); the later specs build on them.
    assert case().FACTS == {"tomas": "tomas_word", "rita": "rita_word"}
    assert case().CONFRONT == {"tomas": {"node": "slides", "breaks": ["files"]},   # specs/computer-lab-backup.md
                               "rita": {"node": "five", "breaks": ["files", "original_photo"]},
                               }   # specs/computer-lab-backup.md: Leonor is no longer convinced with a card
    assert set(case().EVIDENCE) == set(CARDS) - FACT_CARDS   # a fact is held through the notes, not through the save
    assert case().EVIDENCE["files"] == {"flags": {"files_viewed": True}}
    rules = importlib.import_module("campus_evidence")
    for name in ("read_night", "held", "confront", "hearing", "hearing_view", "shown_ending"):
        assert callable(getattr(rules, name)), name
    # campus_case.py is data only, like campus_search.py: no line of it starts a function.
    case_file = (FOLDER / "campus_case.py").read_text(encoding="utf-8")
    assert not re.search(r"^\s*def ", case_file, flags=re.MULTILINE)


# Changed by specs/two-answers.md ("Reviewed tests that change"): the question about message 5 is gone;
# his claim line still never says he did not write it before the proof.
def test_tomas_never_says_he_did_not_write_it_before_he_is_shown_the_proof():
    for language in ("en", "pt"):
        nodes = people.PEOPLE[language]["tomas"]["nodes"]
        assert "msg5" not in nodes
        line = nodes["slides"]
        leading = [option for option in nodes["password"]["options"] if option["next"] == "slides"]
        assert len(leading) == 1 and leading[0]["if"] == {"flags": {"files_viewed": True}}
        words = (line["text"] + " " + line["note"]).lower()
        assert "never wrote" not in words and "nunca escrev" not in words, language


# Changed by specs/two-answers.md ("Reviewed tests that change"): the slides are asked after the password.
def test_the_slides_answer_waits_for_the_files_like_msg5():
    for language in ("en", "pt"):
        early, late = f"early {language}", f"late {language}"
        play("go_computer_lab", language=language, player=early)
        assert "slides" not in answers_of(call("talk", language, early, npc="tomas", node="password"))
        with pytest.raises(ValueError):   # and the line cannot be asked for directly
            call("talk", language, early, npc="tomas", node="slides")

        play("open_drawer", "go_computer_lab", "view_files", language=language, player=late)
        assert "slides" in answers_of(call("talk", language, late, npc="tomas", node="password"))
        reply = call("talk", language, late, npc="tomas", node="slides")
        assert reply["text"] == people.PEOPLE[language]["tomas"]["nodes"]["slides"]["text"]


def test_leonor_says_which_message_is_hers_only_after_helping():
    play("open_drawer", "go_print_shop", "request_copy", "go_study_room", "go_library")
    assert "mine" not in answers_of(call("talk", npc="leonor", node="start"))   # she has not decided yet
    with pytest.raises(ValueError):
        call("talk", npc="leonor", node="mine")
    assert call("play", action="ask_for_help")["accepted"]
    assert "mine" in answers_of(call("talk", npc="leonor", node="start"))
    reply = call("talk", npc="leonor", node="mine")
    assert reply["node"] == "mine" and reply["text"] == people.PEOPLE["en"]["leonor"]["nodes"]["mine"]["text"]


def test_nobody_lists_the_fake_messages():
    texts = []
    for language in ("en", "pt"):
        texts += flat(case().CASE_TEXT[language]).values()
        for person, (_old, new) in NEW_LINES.items():
            line = people.PEOPLE[language][person]["nodes"][new]
            texts += [line["text"], line.get("note", "")]
    for text in texts:
        assert not any(phrase in text.lower() for phrase in ("message 2", "message 4", "mensagem 2", "mensagem 4")), text


def test_every_quote_of_the_case_file_is_a_spoken_line_in_both_languages():
    table = case().CASE_TEXT
    assert table["en"].keys() == table["pt"].keys()
    en, pt = flat(table["en"]), flat(table["pt"])
    assert en.keys() == pt.keys()
    assert any(quotes(text) for text in en.values())   # the reveals, rebuffs and claims are in the table
    for place in en:
        for text in (en[place], pt[place]):
            # A short quote without a full stop would stay in the narration and never be read aloud.
            assert all(is_spoken(quote) for quote in quotes(text)), (place, text)
        assert len(quotes(en[place])) == len(quotes(pt[place])), place


# ---------- The hearing ----------

def test_the_hearing_starts_only_in_the_auditorium_and_only_once():
    investigate()
    walk("study_room")
    before = saved()
    refused = answer("start")
    assert not refused["accepted"] and refused["heard"] is False
    assert refused["message"] == STORIES["en"]["messages"]["not_here"] and refused["hearing"] is None
    assert saved() == before

    walk("auditorium")
    started = answer("start")
    assert started["accepted"]
    assert started["heard"] is True   # the start is saved in the notes too: a reload shows the hearing
    assert db.load_night(PLAYER)["notes"]["hearing"] == []
    hearing = started["hearing"]
    assert set(hearing) == {"step", "doubts", "said"}
    assert hearing["step"] == 1 and hearing["doubts"] == 0 and len(hearing["said"]) == 1
    assert hearing["said"][0] == {"who": "duarte", "name": "Duarte", "text": LINES["en"]["claim_name"]}

    before = saved()
    again = answer("start")
    assert not again["accepted"] and again["heard"] is False
    assert again["message"] == TEXT["en"]["hearing_locked"]
    assert again["hearing"] == hearing
    assert saved() == before


def test_an_answer_before_the_hearing_starts_is_refused_and_saves_nothing():
    to_the_hearing()
    before = saved()
    for value in ("files", "concede"):
        refused = answer(value)
        assert not refused["accepted"] and refused["heard"] is False, value
        assert refused["message"] == STORIES["en"]["messages"]["not_here"], value
        assert refused["hearing"] is None and refused["ending"] is None, value
    assert saved() == before


def test_each_claim_accepts_only_its_own_cards():
    claims = case().HEARING
    assert [(claim["id"], claim["accepts"]) for claim in claims] == [
        ("name", ["files"]), ("photo", ["original_photo"]), ("messages", ["backup"])]   # specs/computer-lab-backup.md
    # The wrong cards that have a line of their own (spec, points 3 and 10). Every other wrong card
    # gets the general wrong line of its claim.
    own_lines = {"name": {}, "photo": {"files": LINES["en"]["history"]},
                 "messages": {}}   # specs/computer-lab-backup.md: the flagged messages and their line are gone
    for claim in claims:
        assert set(claim["wrong"]) == set(own_lines[claim["id"]]), claim["id"]

    # One answer per claim and no retry, so trying every card on every claim takes more than one
    # game. One night for each card, each holding every card: night 0 answers the three claims with
    # cards 0, 1 and 2 of CARDS, night 1 with cards 1, 2 and 3, and so on, going round the list. After
    # those nights every card has been shown against every claim.
    lines = {claim["id"]: {} for claim in claims}   # claim: {card: what the professor answers to it}
    for night in range(len(CARDS)):
        player = f"hearing {night}"
        everything(player)
        doubts = hear(player=player)["hearing"]["doubts"]
        assert doubts == 0
        for number, claim in enumerate(claims):
            card = CARDS[(night + number) % len(CARDS)]
            result = answer(card, player)
            assert result["heard"] is True, (claim["id"], card)
            doubts += 0 if card in claim["accepts"] else 1   # a card that does not break the claim is a doubt
            assert result["hearing"]["doubts"] == doubts, (claim["id"], card)
            line = reply_to_the_last_answer(result["hearing"])
            assert line["who"] == "professor" and line["name"] == "Professor", (claim["id"], card)
            lines[claim["id"]][card] = line["text"]

    for claim in claims:
        said, own = lines[claim["id"]], own_lines[claim["id"]]
        assert set(said) == set(CARDS), claim["id"]   # every card was tried on this claim
        assert all(said[card] == text for card, text in own.items()), claim["id"]
        general = {said[card] for card in CARDS if card not in claim["accepts"] and card not in own}
        assert len(general) == 1, claim["id"]   # one general wrong line for each claim
        right = [said[card] for card in claim["accepts"]]
        assert len(set(right)) == len(right), claim["id"]   # each card that breaks the claim has its own line
        assert not general & set(right) and not general & set(own.values()), claim["id"]


def test_saying_nothing_is_always_a_doubt():
    to_the_hearing()
    assert answer("start")["hearing"]["doubts"] == 0
    for doubts in (1, 2, 3):
        result = answer("concede")
        assert result["heard"] is True and result["hearing"]["doubts"] == doubts
        # Each answer adds three entries to the log: the player's, the reply and the next claim
        # (the third answer adds no claim). These are the first two of this answer.
        first = 3 * (doubts - 1) + 1
        mine, his = result["hearing"]["said"][first:first + 2]
        assert mine == {"who": "you", "name": "", "text": TEXT["en"]["hearing_concede"]}
        assert his == {"who": "duarte", "name": "Duarte", "text": LINES["en"]["nothing"]}
    assert result["hearing"]["said"][-1] == his   # after the third answer the log ends with the reply
    assert result["hearing"]["step"] == 3 and len(result["hearing"]["said"]) == 9


def test_one_answer_per_claim_and_no_retry():
    to_the_hearing()
    first_claim = answer("start")["hearing"]["said"][0]
    wrong = answer("original_photo")   # it does not say who wrote a report
    hearing = wrong["hearing"]
    assert wrong["heard"] is True and hearing["step"] == 2 and hearing["doubts"] == 1
    said = hearing["said"]
    assert [entry["who"] for entry in said] == ["duarte", "you", "professor", "duarte"]
    assert said[0] == first_claim and said[-1]["text"] != first_claim["text"]   # it ends with the next claim
    assert said[1]["name"] == "" and said[1]["text"].startswith("📁")
    assert said[1]["text"].endswith(label_of(wrong, "original_photo"))
    assert all(set(entry) == {"who", "name", "text"} for entry in said)
    assert said[2]["name"] == "Professor" and said[2]["text"] == LINES["en"]["name_wrong"]
    assert "the one on the right, in the long coat" in said[-1]["text"]   # claim 2 (spec, point 10)

    # No retry: the card that breaks claim 1 is now an answer to claim 2, and a wrong one.
    second = answer("files")["hearing"]
    assert second["step"] == 3 and second["doubts"] == 2
    assert second["said"][-1]["who"] == "duarte" and "Is Tomás a liar too?" in second["said"][-1]["text"]   # claim 3


def test_a_reload_in_the_middle_keeps_the_step_the_doubts_and_the_log():
    to_the_hearing()
    hearing = hear("concede")["hearing"]
    assert hearing["step"] == 2 and hearing["doubts"] == 1
    reloaded = call()
    assert reloaded["hearing"] == hearing and reloaded["ending"] is None


def test_nothing_else_can_be_done_during_the_hearing():
    to_the_hearing()
    # A valid `talk` and a valid `confront` first (one rebuff: 2 minutes), then the hearing starts.
    assert call("talk", npc="professor", node="start")["name"] == "Professor"
    assert show("files", "professor", "start")["confront"]["cracked"] is False
    assert answer("start")["hearing"]["step"] == 1
    locked = TEXT["en"]["hearing_locked"]
    before = saved()
    refused = [call("play", action="go_study_room"), call("play", action="present_evidence"),
               call("enter", room="study_room"), call("search", spot=search.PEN_SPOT),
               call("unlock", code=search.PC12_CODE)]
    for result in refused:
        assert not result["accepted"] and result["message"] == locked
        assert result["scene"] == "auditorium" and result["ending"] is None
    with pytest.raises(ValueError) as error:
        call("talk", npc="professor", node="start")
    assert locked in str(error.value)
    with pytest.raises(ValueError) as error:
        show("files", "professor", "start")
    assert locked in str(error.value)
    assert saved() == before

    restarted = call("restart", confirmed=True)   # the way out: a new night
    assert restarted["scene"] == "study_room" and restarted["hearing"] is None and restarted["evidence"] == []


def test_three_answers_end_the_game_with_the_story_ending_of_leonors_choice():
    # Changed by specs/computer-lab-backup.md ("Reviewed tests that change"): Leonor's choice decides the story's ending.
    cases = [
        # (the story's ending, Leonor, Tomás cracked, the three answers, doubts, verdict line)
        ("full_case", "ask_for_help", False, ["files", "original_photo", "backup"], 0, ""),
        ("full_case", "ask_for_help", False, ["concede", "original_photo", "backup"], 1, ""),
        ("impostor", "accuse", False, ["files", "original_photo", "concede"], 1, ""),
        # Stolen credit with the `messages` claim not broken: the one doubt is there, and no line.
        ("stolen_credits", None, False, ["files", "original_photo", "concede"], 1, ""),
        # Stolen credit although Tomás's word broke the `messages` claim: the professor says why.
        ("stolen_credits", None, True, ["files", "original_photo", "backup"], 0, ""),
    ]
    for language in ("en", "pt"):
        for number, (ending, leonor, tomas, answers, doubts, line) in enumerate(cases):
            player = f"{language} case {number}"
            to_the_hearing(player, language, leonor, tomas)
            result = hear(*answers, player=player, language=language)
            assert result["hearing"]["doubts"] == doubts, player
            verdict = LINES[language][line] if line else ""
            check_ending(result, player, language, saved_id=ending, shown_id=ending, verdict=verdict)


def test_two_doubts_show_stolen_credit_instead_of_case_closed():
    # Changed by specs/computer-lab-backup.md ("Reviewed tests that change"): "The impostor" now means Leonor was accused,
    # so two doubts on a "Case closed" night show "Stolen credit" (the professor's line is the same).
    to_the_hearing()
    result = hear("concede", "concede", "backup")
    assert result["hearing"]["doubts"] == 2
    check_ending(result, PLAYER, "en", saved_id="full_case", shown_id="stolen_credits", verdict=LINES["en"]["two"])


def test_two_doubts_leave_the_other_endings_alone():
    cases = [
        # (the story's ending, Leonor, the three answers)
        ("impostor", "accuse", ["files", "concede", "concede"]),
        ("stolen_credits", None, ["files", "concede", "concede"]),
    ]
    for ending, leonor, answers in cases:
        to_the_hearing(ending, "en", leonor)   # the player is named after the ending
        result = hear(*answers, player=ending)
        assert result["hearing"]["doubts"] == 2, ending
        check_ending(result, ending, "en", saved_id=ending, shown_id=ending, verdict="")


def test_three_doubts_show_stolen_credit_whatever_leonor_chose():
    cases = [
        # (the story's ending, Leonor, the verdict line)
        ("full_case", "ask_for_help", "three_help"),
        ("impostor", "accuse", "three"),
        # The story's ending is already "Stolen credit": the three doubts still get their line.
        ("stolen_credits", None, "three"),
    ]
    for ending, leonor, line in cases:
        to_the_hearing(ending, "en", leonor)
        result = hear("concede", "concede", "concede", player=ending)
        assert result["hearing"]["doubts"] == 3, ending
        check_ending(result, ending, "en", saved_id=ending, shown_id="stolen_credits", verdict=LINES["en"][line])


def test_a_perfect_hearing_cannot_lift_stolen_credit():
    # Changed by specs/computer-lab-backup.md ("Reviewed tests that change"): the backup answers the messages claim, and
    # with nobody from the group there (Leonor never asked) the story's "Stolen credit" stays, with no line.
    to_the_hearing(leonor=None, tomas=True)
    result = hear("files", "original_photo", "backup")
    assert result["hearing"]["doubts"] == 0
    assert result["hearing"]["said"][-1]["who"] == "professor"
    check_ending(result, PLAYER, "en", saved_id="stolen_credits", shown_id="stolen_credits", verdict="")


def test_the_verdict_is_saved_and_a_reload_shows_it():
    to_the_hearing()
    ended = hear("concede", "concede", "backup")   # two doubts on a full case: a capped ending
    assert ended["ending"]["verdict"] == LINES["en"]["two"]
    notes = db.load_night(PLAYER)["notes"]
    # Changed by specs/computer-lab-backup.md: the capped ending is "Stolen credit" now.
    assert notes["hearing"] == ["concede", "concede", "backup"] and notes["verdict"] == "stolen_credits"

    reloaded = call()
    assert reloaded["ending"] == ended["ending"]
    assert reloaded["hearing"] == ended["hearing"]
    assert reloaded["hearing"]["step"] == 3 and reloaded["hearing"]["doubts"] == 2
    last = reloaded["hearing"]["said"][-1]
    assert last["who"] == "professor" and last == reply_to_the_last_answer(reloaded["hearing"])


def test_the_hearing_cannot_be_answered_a_fourth_time():
    to_the_hearing()
    ended = hear("files", "original_photo", "backup")
    assert ended["ending"]["id"] == "full_case"   # specs/computer-lab-backup.md: Leonor helps, so "Case closed"
    before = saved()
    for value in ("files", "concede"):
        refused = answer(value)
        assert not refused["accepted"] and refused["heard"] is False, value
        assert refused["message"] == STORIES["en"]["messages"]["game_over"], value
        assert refused["ending"] == ended["ending"] and refused["hearing"] == ended["hearing"], value

    # Nor opened again: after the verdict the game is over, and the saved answers stay as they are.
    again = answer("start")
    assert not again["accepted"] and again["heard"] is False
    assert again["message"] == STORIES["en"]["messages"]["game_over"]
    assert again["ending"] == ended["ending"] and again["hearing"] == ended["hearing"]
    assert saved() == before


def test_a_card_not_held_or_unknown_is_rejected_at_the_hearing_and_saves_nothing():
    to_the_hearing()   # nothing flagged, nobody cracked
    assert answer("start")["hearing"]["step"] == 1   # a valid request first
    before = saved()
    for bad in ("msg_5", "tomas_word", "knife", 7, ["files"]):
        with pytest.raises(ValueError):
            answer(bad)
    with pytest.raises(ValueError):   # an extra field
        call("hearing", answer="files", extra=1)
    with pytest.raises(ValueError):   # a missing field
        call("hearing")
    assert saved() == before
    assert call()["hearing"]["step"] == 1   # the claim is still waiting for its one answer

    # Leonor's screenshots are not held by a player who accused her: she deleted the messages.
    to_the_hearing("accuser", leonor="accuse")
    assert answer("start", "accuser")["hearing"]["step"] == 1   # a valid request first
    before = saved()
    with pytest.raises(ValueError):
        answer("leonor_messages", "accuser")
    assert saved() == before


def test_presenting_directly_still_gives_the_story_ending():
    to_the_hearing()
    result = call("play", action="present_evidence")   # a hand-made request: no hearing was started
    assert result["accepted"]
    check_ending(result, PLAYER, "en", saved_id="full_case", shown_id="full_case", verdict="")
    assert result["hearing"] is None
    assert call()["hearing"] is None and call()["ending"] == result["ending"]

    # No hearing can start once the story has ended: this path never gets a cap (spec, Limits).
    before = saved()
    late = answer("start")
    assert not late["accepted"] and late["heard"] is False and late["hearing"] is None
    assert late["message"] == STORIES["en"]["messages"]["game_over"] and late["ending"] == result["ending"]
    assert saved() == before


# ---------- The old operations, the page and the files ----------

def test_talking_still_writes_nothing_and_old_operations_still_refuse_extra_fields():
    investigate()
    before = saved()
    reply = call("talk", npc="tomas", node="slides")
    assert reply["node"] == "slides" and reply["text"] == people.PEOPLE["en"]["tomas"]["nodes"]["slides"]["text"]
    assert "confront" not in reply
    assert saved() == before
    for bad in (dict(operation="talk", npc="tomas", node="slides", evidence="files"),
                dict(operation="play", action="go_study_room", answer="start"),
                dict(operation="open", npc="tomas")):
        with pytest.raises(ValueError):
            call(**bad)
    assert saved() == before


def test_the_page_and_early_snapshots_never_contain_the_case_file():
    secrets = case_texts("en") + case_texts("pt")
    assert [secret for secret in secrets if shows(PAGE, secret)] == []
    new_game = as_text(call(player="newcomer"))
    assert [secret for secret in secrets if shows(new_game, secret)] == []

    # A hearing after one answer: of the whole case file, only the lines already said (and the
    # labels of the cards in the hand) may be in the reply.
    to_the_hearing()
    result = hear("original_photo")
    allowed = [entry["text"] for entry in result["hearing"]["said"]] + [card["label"] for card in result["evidence"]]
    text = as_text(result)
    assert [secret for secret in secrets if shows(text, secret) and secret not in allowed] == []


def test_the_page_has_the_tray_and_the_hearing_inside_the_conversation_card():
    # Changed by specs/two-answers.md ("Reviewed tests that change"): no "Show evidence" tray; the right
    # answer of a claim line shows its card (`option.crack`).
    new = ["function confrontWith(", "function showHearing(", 'action.id === "present_evidence"', "option.crack",
           "ending.verdict", "hearing.said", "topics.delete(", 'line.npc === "rita" && line.node === "photo"']
    kept = ['action.id === "open_drawer"', "if (option.cost) penalize(option.cost)",
            "line.options.filter(option => option.next !== null && !asked.has(option.next))",
            "  function showLine(line) {", "// The player chose to do something", "topics.clear()", 'node: "result"']
    for needle in new + kept:
        assert needle in PAGE, needle
    assert 'id="hearing-card"' not in PAGE   # the hearing has no card of its own
    # PAGE holds every key of campus_text.py, used or not, so the use of these two is looked for in play.js itself.
    play_js = (FOLDER / "play.js").read_text(encoding="utf-8")
    assert "evidence_show" not in play_js and "talk-evidence" not in play_js and "hearing_concede" in play_js
    # The same for the other texts the page shows (points 5, 6 and 9), and for the two new operations it sends.
    for key in ("hearing_hint", "time_penalty_card", "time_penalty_duarte"):   # evidence_back went with the tray
        assert key in play_js, key
    for operation in ("confront", "hearing"):
        assert f'"{operation}"' in play_js or f"'{operation}'" in play_js, operation

    # The lines tests/continuous-conversations.cjs runs alone, with a fake page (spec, point 13).
    # Node is not installed on every computer of the team, so the rules that keep that test
    # passing are also read here, in the source.
    start = play_js.index("  function showLine(line) {")
    block = play_js[start:play_js.index("  // The player chose to do something", start)]
    assert "option.crack" in block   # the right answer of a claim line is handled inside showLine
    assert "classList.add" not in block and ".remove()" not in block   # the fake page has neither
    assert not re.search(r"\bt\.\w+\[", block)   # ui() is {} there: t.night_lines[0] would break


def test_the_new_texts_exist_in_both_languages():
    keys = ["evidence_show", "evidence_title", "evidence_empty", "evidence_back", "time_penalty_card",
            "time_penalty_duarte", "hearing_hint", "hearing_concede", "hearing_step", "hearing_trust", "hearing_locked"]
    for language in ("en", "pt"):
        for key in keys:
            assert TEXT[language][key].strip(), (language, key)
        for key in ("time_penalty_card", "time_penalty_duarte", "hearing_step"):
            assert "{n}" in TEXT[language][key], (language, key)
    assert TEXT["en"]["hearing_locked"] == "You cannot walk out in the middle of your own case."   # spec, point 12


def test_app_3d_reloads_the_new_modules_in_order():
    source = (PROJECT / "app_3d.py").read_text(encoding="utf-8")   # read, not run: running it starts Streamlit
    after_name = source.split("CODE_MODULES = ", 1)[1]
    modules = ast.literal_eval(after_name[:after_name.index("]") + 1])   # the list, as Python would read it
    assert "campus_case" in modules and "campus_evidence" in modules
    # A module comes after the ones it imports from.
    assert (modules.index("campus_search") < modules.index("campus_case")
            < modules.index("campus_evidence") < modules.index("campus_game"))
    # Comments are left out of both checks: a comment may well say why the two modules are not there.
    page_files = code_only(source.split("PAGE_FILES = ", 1)[1].split("def page_version", 1)[0])
    assert "campus_case" not in page_files and "campus_evidence" not in page_files
    page3d_source = (FOLDER / "page3d.py").read_text(encoding="utf-8")
    imports = [line for line in code_only(page3d_source).splitlines()
               if line.strip().startswith(("import ", "from ")) or "import_module" in line]
    assert len(imports) >= 4   # the import lines were found
    assert not any("campus_case" in line or "campus_evidence" in line for line in imports)
