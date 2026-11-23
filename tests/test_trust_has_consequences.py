"""Trust has consequences: people you were rude to answer less, warn the others, or lie
(specs/trust-has-consequences.md).

Written before the code: one test for every line under "Checks" in the spec, in the same order.

How to read this file:
- `rude(person, node)` is the new operation: the page sends it instead of `talk` when the player
  chooses an answer that has a `cost`. `make(person, mood)` sends one rude answer (wary) or two
  (hostile) to that person, as the page would: Leonor "Say she is lying" then "Insist", Tomás
  "Demand to know..." then "Push harder", Duarte "Tell him you know the truth" then "Press him".
- "saves nothing" means the database file has the same bytes before and after (`saved()`).
- A test that expects a ValueError first sends one valid request of the same operation in the same
  game, so it cannot pass only because the operation does not exist yet.
- `investigate()` plays a new game up to the computer lab, as in tests/test_earlier_nights.py: the
  USB stick, the copy, Leonor helps, the old files (2.5 charged minutes), so every line of every
  person can be reached and the schedule never meets the test. The auditorium is open then.
- The new texts are copied word for word from design-notes/texts-ideas.md, part A. The spec names
  the tables of campus_people.py (`COLD`, `WITHHELD`, `LIES`, `WARNED`, `WARNS`), so the last
  tests read them by name. The other tests only use the commands, as the page does.
"""

import importlib
import json
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
evidence = importlib.import_module("campus_evidence")
TEXT = importlib.import_module("campus_text").TEXT
PC12_CODE = importlib.import_module("campus_search").PC12_CODE

PLAYER = "detective"
# The answers with a cost, in the order the page offers them (the first one, then the one after it).
TARGETS = {"leonor": ["harsh", "closed"], "tomas": ["hard", "closed"], "duarte": ["know", "closed"]}
# Who warns whom (point 6).
WARNS = {"tomas": "leonor", "leonor": "rita", "duarte": "professor"}
# The claim lines (specs/evidence-and-hearing.md, point 7).
CLAIMS = {"tomas": "slides", "rita": "five", "leonor": "sure"}

# A1: the curt lines (wary or hostile). The line keeps the story's note.
COLD = {
    "en": {
        "tomas": {"start": 'Tomás does not look up from computer 11. "What now?"',
                  "kind": '"Finishing the slides." He keeps typing. "Someone was at computer 12 last night. That is all I know."',
                  "password": '"The day and month of the cover photo. Four digits." He does not look up.',
                  "who": '"Someone in a hood, at computer 12." He keeps typing.'},
        "leonor": {"start": 'Leonor does not close her book this time. "Yes?"',
                   "messages": '"From a number I did not know. Last night."'},
        "duarte": {"start": 'Duarte does not bother to smile. "Still here?"',
                   "part": '"The slides. Ask anyone." He looks past you.'},
    },
    "pt": {
        "tomas": {"start": 'O Tomás nem levanta os olhos do computador 11. "O que foi agora?"',
                  "kind": '"A acabar os slides." Continua a escrever. "Esteve alguém no computador 12 ontem à noite. É tudo o que sei."',
                  "password": '"O dia e o mês da fotografia da capa. Quatro algarismos." Nem levanta os olhos.',
                  "who": '"Alguém de capuz, no computador 12." Continua a escrever.'},
        "leonor": {"start": 'Desta vez a Leonor não fecha o livro. "Sim?"',
                   "messages": '"De um número que eu não conhecia. Ontem à noite."'},
        "duarte": {"start": 'O Duarte nem se dá ao trabalho de sorrir. "Ainda por aqui?"',
                   "part": '"Os slides. Pergunta a qualquer um." Olha para além de ti.'},
    },
}
# A2: the hints that are not given (wary or hostile). The line has no note.
WITHHELD = {
    "en": {
        "tomas": {"help": 'Tomás looks at the photo a second too long. "Check what you like. I am busy."'},
        "leonor": {"mine": '"Work it out yourself."'},
        "duarte": {"slide": '"Why would I tell you?" Duarte glances at the door.'},
    },
    "pt": {
        "tomas": {"help": 'O Tomás fica a olhar para a fotografia um segundo a mais. "Vê o que quiseres. Estou ocupado."'},
        "leonor": {"mine": '"Descobre tu."'},
        "duarte": {"slide": '"Porque é que te havia de dizer?" O Duarte olha para a porta.'},
    },
}
# A3: the lies (hostile only).
# Changed by specs/two-answers.md ("Reviewed tests that change"): Tomás's lie was on his line about message 5, which is gone.
LIES = {
    "en": {
        "leonor": {"messages": {"text": '"Nothing strange about them. They came on the dates they say, weeks ago." She turns the phone face down.',
                                "note": "Leonor says the messages arrived on their dates, weeks ago."}},
    },
    "pt": {
        "leonor": {"messages": {"text": '"Não têm nada de estranho. Chegaram nas datas que lá dizem, há semanas." Vira o telemóvel ao contrário.',
                                "note": "A Leonor diz que as mensagens chegaram nas datas delas, há semanas."}},
    },
}
# A4: the first line of the person who was warned.
WARNED = {
    "en": {"leonor": 'Leonor closes her book before you reach the table. "Tomás texted me. He says you are going round calling people liars."',
           "rita": 'Rita looks up and does not smile. "Leonor says you shouted at her in the library. Is that true?"',
           "professor": 'The professor looks up from the list and does not smile. "Duarte tells me you threatened him. I hope you bring evidence tomorrow, not that."'},
    "pt": {"leonor": 'A Leonor fecha o livro antes de chegares à mesa. "O Tomás mandou-me mensagem. Diz que andas por aí a chamar mentirosos às pessoas."',
           "rita": 'A Rita levanta os olhos e não sorri. "A Leonor diz que lhe gritaste na biblioteca. É verdade?"',
           "professor": 'O professor levanta os olhos da lista e não sorri. "O Duarte diz-me que o ameaçou. Espero que amanhã me traga provas, e não isso."'},
}
# A5: the "conversations" row of `howto_items`.
HOWTO = {"en": "The people and the dialogues with choices and trust. Talking saves nothing; a rude answer is remembered for the rest of the night.",
         "pt": "As pessoas e os diálogos com escolhas e confiança. Falar não grava nada; uma resposta rude fica lembrada até ao fim da noite."}


# ---------- helpers: requests ----------

def call(operation="open", language="en", player=PLAYER, **extra):
    """One request to the server, exactly as the page sends it."""
    return campus.command(dict(operation=operation, language=language, player=player, **extra))


def saved():
    """The bytes of the database file: equal before and after means nothing was written."""
    return db.DB_PATH.read_bytes()


def do(action, player=PLAYER, language="en"):
    """Play one story action (the `play` operation). It must be accepted."""
    result = call("play", language, player, action=action)
    assert result["accepted"], action
    return result


def walk(room, player=PLAYER, language="en"):
    """Walk through the door of a room (the `enter` operation). It must be accepted."""
    result = call("enter", language, player, room=room)
    assert result["accepted"], room
    return result


def walk_to(person, player=PLAYER, language="en"):
    """Walk to the room of `person`, unless the player already stands there."""
    room = people.ROOM_OF_PERSON[person]
    if people.room_of_scene(game.load(player)["scene"]) != room:
        walk(room, player, language)


def talk(person, node, player=PLAYER, language="en"):
    """One line of a conversation (the `talk` operation)."""
    return call("talk", language, player, npc=person, node=node)


def rude(person, node, player=PLAYER, language="en"):
    """One line reached by an answer with a cost (the new `rude` operation)."""
    return call("rude", language, player, npc=person, node=node)


def make(person, mood, player=PLAYER, language="en"):
    """Walk to `person` and give them one rude answer ("wary") or two ("hostile")."""
    walk_to(person, player, language)
    for node in TARGETS[person][:{"wary": 1, "hostile": 2}[mood]]:
        assert rude(person, node, player, language)["node"] == node
    return game.load(player)


def at(minute, player=PLAYER, language="en"):
    """The page reports its campus minute (the `time` operation of specs/night-schedule.md)."""
    return call("time", language, player, minute=minute)


def show(card, npc, node, player=PLAYER, language="en"):
    """Show one card to a person on one of their lines (the `confront` operation)."""
    return call("confront", language, player, npc=npc, node=node, evidence=card)


def investigate(player=PLAYER, language="en"):
    """A new game played up to the computer lab: the USB stick, the copy, Leonor helps, the old
    files and the backup of the conversations (specs/computer-lab-backup.md: no chat any more).
    The player stands beside Tomás."""
    steps = ["open_drawer", "go_print_shop", "request_copy", "go_study_room",
             "go_library", "ask_for_help", "go_study_room", "go_computer_lab", "view_files", "save_backup"]
    call(language=language, player=player)
    for action in steps:
        do(action, player, language)


# ---------- helpers: reading ----------

def story_line(person, node, language="en"):
    """The story's own line (campus_people.PEOPLE), which a calm person says."""
    return people.PEOPLE[language][person]["nodes"][node]


def notes(player=PLAYER):
    """The night's notes as saved, read straight from db.py."""
    return db.load_night(player)["notes"]


def change_notes(player, **changes):
    """Rewrite this player's night notes by hand, the way a damaged file would have them."""
    night = db.load_night(player)
    written = dict(night["notes"], **changes)
    with closing(sqlite3.connect(db.DB_PATH)) as connection, connection:
        connection.execute("INSERT OR REPLACE INTO nights (player, minute, notes) VALUES (?, ?, ?)",
                           (player, night["minute"], json.dumps(written)))


def keys_of(value):
    """Every key of every dictionary inside a reply, at any depth."""
    if isinstance(value, dict):
        return set(value) | {key for inner in value.values() for key in keys_of(inner)}
    if isinstance(value, list):
        return {key for inner in value for key in keys_of(inner)}
    return set()


def texts_of(table):
    """Every text inside a table, whatever its layout."""
    if isinstance(table, str):
        return [table]
    if isinstance(table, dict):
        return [text for value in table.values() for text in texts_of(value)]
    return []


def shape(table):
    """The keys of a table at every depth, without its texts, to compare the two languages."""
    if isinstance(table, dict):
        return {key: shape(value) for key, value in table.items()}
    return None


# ---------- Checks ----------

def test_talk_still_saves_nothing_after_rudeness():
    call()
    walk("library")
    before = saved()
    assert talk("leonor", "harsh")["text"] == story_line("leonor", "harsh")["text"]
    assert talk("leonor", "closed")["text"] == story_line("leonor", "closed")["text"]
    assert saved() == before
    # A later line is the story's own: a `talk` is never remembered as rude.
    for node in ("start", "messages", "sure"):
        reply = talk("leonor", node)
        assert (reply["text"], reply["note"]) == (story_line("leonor", node)["text"],
                                                   story_line("leonor", node).get("note", "")), node
    assert "rude" not in notes()
    assert saved() == before


def test_rude_is_a_talk_that_is_remembered():
    call()
    walk("library")
    plain = talk("leonor", "harsh")
    remembered = rude("leonor", "harsh")
    assert set(remembered) == set(plain)
    assert remembered["text"] == plain["text"] and remembered == plain
    assert notes()["rude"] == {"leonor": 1}
    assert rude("leonor", "closed")["text"] == talk("leonor", "closed")["text"]
    assert notes()["rude"] == {"leonor": 2}
    rude("leonor", "harsh")
    assert notes()["rude"] == {"leonor": 2}   # never above 2
    # It charges nothing: the page takes the 5 minutes, as before.
    assert call()["night"]["minute"] == 0


def test_rude_only_for_the_targets_of_a_costly_answer():
    call()
    walk("library")
    assert rude("leonor", "harsh")["node"] == "harsh"   # a valid one first
    before = saved()
    for bad in (dict(npc="leonor", node="soft"),                        # an answer without a cost
                dict(npc="leonor", node="start"),
                dict(npc="leonor", node="hard"),                        # Tomás's line, not hers
                dict(npc="leonor", node="harsh", evidence="files"),     # an extra field
                dict(npc="tomas", node="hard"),                         # a person who is not here
                dict(npc=["leonor"], node="harsh"),
                dict(npc="leonor", node=["harsh"])):
        with pytest.raises(ValueError):
            call("rude", **bad)
    with pytest.raises(ValueError):
        call("rude", npc="leonor")                                      # a missing field
    assert saved() == before
    # Rita and the clerk have no answer with a cost.
    walk("study_room")
    before = saved()
    for node in ("start", "photo", "harsh", "closed"):
        with pytest.raises(ValueError):
            rude("rita", node)
    walk("print_shop")
    before = saved()
    for node in ("start", "order", "closed"):
        with pytest.raises(ValueError):
            rude("amelia", node)
    assert saved() == before

    # The same refusals as `talk`: during the hearing and at 22:45.
    investigate(player="heard")
    walk("auditorium", player="heard")
    assert call("hearing", player="heard", answer="start")["accepted"]
    before = saved()
    for operation in ("talk", "rude"):
        with pytest.raises(ValueError) as refused:
            call(operation, player="heard", npc="duarte", node="know")
        assert refused.value.args[0] == TEXT["en"]["hearing_locked"], operation
    assert saved() == before
    investigate(player="late")
    walk("auditorium", player="late")
    assert at(30, player="late")["night"]["closed"] is True
    before = saved()
    for operation in ("talk", "rude"):
        with pytest.raises(ValueError) as refused:
            call(operation, player="late", npc="duarte", node="know")
        assert refused.value.args[0] == TEXT["en"]["time_up_title"], operation
    assert saved() == before


def test_wary_gives_curt_lines_with_the_same_note():
    for language in ("en", "pt"):
        calm, wary = f"calm {language}", f"wary {language}"
        investigate(calm, language)
        investigate(wary, language)
        walk_to("tomas", calm, language)
        story = talk("tomas", "password", calm, language)
        make("tomas", "wary", wary, language)
        curt = talk("tomas", "password", wary, language)
        assert curt["text"] == COLD[language]["tomas"]["password"], language
        assert curt["note"] == story_line("tomas", "password", language)["note"] == story["note"], language
        assert curt["options"] == story["options"] and curt["actions"] == story["actions"], language
        # Every curt line keeps its note and its answers.
        for person in ("tomas", "leonor", "duarte"):
            if person != "tomas":
                make(person, "wary", wary, language)
            walk_to(person, calm, language)
            for node, text in COLD[language][person].items():
                plain, short = talk(person, node, calm, language), talk(person, node, wary, language)
                assert short["text"] == text, (language, person, node)
                assert short["note"] == plain["note"] == story_line(person, node, language).get("note", ""), (person, node)
                assert short["options"] == plain["options"] and short["actions"] == plain["actions"], (person, node)


def test_wary_withholds_hints():
    for language in ("en", "pt"):
        calm, wary = f"calm {language}", f"wary {language}"
        investigate(calm, language)
        investigate(wary, language)
        for person in ("tomas", "leonor", "duarte"):
            make(person, "wary", wary, language)
            walk_to(person, calm, language)
            for node, text in WITHHELD[language][person].items():
                plain, short = talk(person, node, calm, language), talk(person, node, wary, language)
                assert plain["note"] == story_line(person, node, language)["note"] != "", (person, node)
                assert short["text"] == text, (language, person, node)
                assert short["note"] == "", (language, person, node)
                assert short["options"] == plain["options"], (person, node)


# Changed by specs/two-answers.md ("Reviewed tests that change"): a hostile Tomás no longer lies (his
# message 5 line is gone); his claim line stays the story's own, and the backup still says the message was new.
def test_hostile_tomas_tells_no_lie_and_the_backup_says_otherwise():
    for language in ("en", "pt"):
        player = f"lied to {language}"
        investigate(player, language)
        rude("tomas", "hard", player, language)
        rude("tomas", "closed", player, language)
        assert "tomas" not in people.LIES[language]
        slides = talk("tomas", "slides", player, language)
        assert slides["text"] == story_line("tomas", "slides", language)["text"], language
        backup = STORIES[language]["scenes"]["computer_lab"]["actions"]["save_backup"]["result_text"]
        assert backup in [entry["text"] for entry in call(language=language, player=player)["notebook"]], language
        # And Rita says an old message does not arrive as new.
        walk("study_room", player, language)
        rita = talk("rita", "chat", player, language)
        assert (rita["text"], rita["note"]) == (story_line("rita", "chat", language)["text"],
                                                story_line("rita", "chat", language)["note"]), language

def test_hostile_leonor_lies_about_the_messages():
    for language in ("en", "pt"):
        player = f"lied to {language}"
        investigate(player, language)
        make("leonor", "hostile", player, language)
        for before in ("sure", "soft"):   # both answers that lead to her messages
            assert talk("leonor", before, player, language)["node"] == before
        lie = talk("leonor", "messages", player, language)
        assert lie["text"] == LIES[language]["leonor"]["messages"]["text"], language
        assert lie["note"] == LIES[language]["leonor"]["messages"]["note"], language
        assert lie["options"] == [people.offered(o) for o in story_line("leonor", "messages", language)["options"]]


def test_the_warning_reaches_the_next_person_only():
    for language in ("en", "pt"):
        calm = f"calm {language}"
        investigate(calm, language)
        for warner, listener in WARNS.items():
            player = f"{warner} {language}"
            investigate(player, language)
            make(warner, "wary", player, language)
            walk_to(listener, player, language)
            # Wary is not enough: only a hostile person warns.
            assert talk(listener, "start", player, language)["text"] == story_line(listener, "start", language)["text"]
            make(warner, "hostile", player, language)
            for person in ("rita", "leonor", "professor"):
                if person == warner:   # her own first line is curt (point 4), not a warning
                    continue
                walk_to(person, player, language)
                walk_to(person, calm, language)
                plain, greeted = talk(person, "start", calm, language), talk(person, "start", player, language)
                if person == listener:
                    assert greeted["text"] == WARNED[language][listener], (language, warner)
                else:
                    assert greeted["text"] == plain["text"], (language, warner, person)
                # Only the first line changes: the answers and the actions are as before.
                assert greeted["options"] == plain["options"] and greeted["actions"] == plain["actions"]
                assert greeted["note"] == plain["note"] and greeted["trust"] == plain["trust"]


def test_cracking_forgives():
    investigate()
    make("tomas", "hostile")
    assert talk("tomas", "start")["text"] == COLD["en"]["tomas"]["start"]
    # A card on another line is not a confrontation: the usual rebuff (specs/two-answers.md: no msg5 line).
    assert show("files", "tomas", "who")["confront"]["cracked"] is False
    walk("library")
    assert talk("leonor", "start")["text"] == WARNED["en"]["leonor"]
    walk("computer_lab")
    assert show("files", "tomas", "slides")["confront"]["cracked"] is True   # specs/computer-lab-backup.md
    for node in ("start", "kind", "password", "who"):
        reply = talk("tomas", node)
        assert (reply["text"], reply["note"]) == (story_line("tomas", node)["text"],
                                                   story_line("tomas", node).get("note", "")), node
    # Calm for the rest of the night, whatever is said afterwards.
    rude("tomas", "hard")
    assert talk("tomas", "start")["text"] == story_line("tomas", "start")["text"]
    walk("library")
    assert talk("leonor", "start")["text"] == story_line("leonor", "start")["text"]

    # Changed by specs/computer-lab-backup.md ("Reviewed tests that change"): Leonor is no longer cracked with a card,
    # so only Tomás's half of this test remains.

def test_claims_actions_and_the_code_rule_never_change_with_temper():
    investigate("calm")
    investigate("hostile")
    for person in ("tomas", "leonor", "duarte"):
        make(person, "hostile", "hostile")
    for person in ("tomas", "leonor", "duarte", "rita", "professor"):
        walk_to(person, "calm")
        walk_to(person, "hostile")
        for node in people.PEOPLE["en"][person]["nodes"]:
            try:
                plain = talk(person, node, "calm")
            except ValueError:
                with pytest.raises(ValueError):   # a line that cannot be asked for now stays so
                    talk(person, node, "hostile")
                continue
            told = talk(person, node, "hostile")
            assert told["options"] == plain["options"], (person, node)
            assert told["actions"] == plain["actions"], (person, node)
            assert told["trust"] == plain["trust"], (person, node)
            if CLAIMS.get(person) == node:   # a claim line is the story's own
                assert told == plain, (person, node)

    # Leonor's decision is still offered, and taken, by a hostile player.
    # Changed by specs/three-proofs.md ("Reviewed tests that change"): she has one decision (no "accuse").
    for player in ("deciding calm", "deciding hostile"):
        call(player=player)
        for action in ("open_drawer", "go_print_shop", "request_copy", "go_study_room", "go_library"):
            do(action, player)
    make("leonor", "hostile", "deciding hostile")
    plain, told = talk("leonor", "start", "deciding calm"), talk("leonor", "start", "deciding hostile")
    assert told["actions"] == plain["actions"]
    assert {action["id"] for action in told["actions"] if action["allowed"]} >= {"ask_for_help"}
    do("ask_for_help", "deciding hostile")

    # The schedule: an undecided Leonor still leaves at 22:30.
    call(player="leaving")
    make("leonor", "hostile", "leaving")
    assert "leonor" in at(15, player="leaving")["night"]["gone"]

    # The code rule: Tomás's `password` is only curt, and the code still unlocks computer 12.
    call(player="coder")
    do("open_drawer", "coder")
    make("tomas", "hostile", "coder")
    password = talk("tomas", "password", "coder")
    assert password["text"] == COLD["en"]["tomas"]["password"]
    assert password["note"] == story_line("tomas", "password")["note"]
    unlocked = call("unlock", player="coder", code=PC12_CODE)
    assert unlocked["unlocked"] is True and unlocked["accepted"] is True
    assert game.load("coder")["flags"]["files_viewed"] is True


def test_a_damaged_rude_note_counts_as_calm():
    call()
    walk("computer_lab")
    # A good note in the same place does count (so this test cannot pass for the wrong reason).
    change_notes(PLAYER, rude={"tomas": 1})
    assert talk("tomas", "start")["text"] == COLD["en"]["tomas"]["start"]
    assert evidence.read_night(PLAYER, game.load(PLAYER))["rude"] == {"tomas": 1}
    for damaged in ("yes", {"rita": 2}, {"tomas": 7}, {"tomas": True}, {"tomas": 1.0}, [["tomas", 2]], None):
        change_notes(PLAYER, rude=damaged)
        before = saved()
        assert talk("tomas", "start")["text"] == story_line("tomas", "start")["text"], damaged
        assert talk("tomas", "kind")["text"] == story_line("tomas", "kind")["text"], damaged
        assert evidence.read_night(PLAYER, game.load(PLAYER))["rude"] == {}, damaged
        assert saved() == before
    # A damaged note is counted from nothing by the next rude answer.
    change_notes(PLAYER, rude={"tomas": 7})
    rude("tomas", "hard")
    assert notes()["rude"] == {"tomas": 1}


def test_no_reply_ever_carries_the_temper():
    investigate()
    replies = []
    for person in ("tomas", "leonor", "duarte"):
        make(person, "hostile")
        replies += [talk(person, node) for node in ("start", TARGETS[person][0])]
        replies.append(rude(person, TARGETS[person][1]))
        replies.append(call())   # the snapshot
    walk("study_room")
    replies += [talk("rita", "start"), call()]
    walk("computer_lab")
    replies.append(show("files", "tomas", "who"))   # specs/two-answers.md: no msg5 line
    for reply in replies:
        assert not keys_of(reply) & {"rude", "mood", "moods", "temper"}, reply.get("node")
        text = json.dumps(reply, ensure_ascii=False)
        assert '"wary"' not in text and '"hostile"' not in text   # ("calm" is a line of Tomás)


def test_the_trust_texts_have_the_same_keys_in_both_languages_and_name_no_culprit_date_or_code():
    assert people.WARNS == WARNS
    tables = {"COLD": people.COLD, "WITHHELD": people.WITHHELD, "LIES": people.LIES, "WARNED": people.WARNED}
    expected = {"COLD": COLD, "WITHHELD": WITHHELD, "LIES": LIES, "WARNED": WARNED}
    for name, table in tables.items():
        assert set(table) == {"en", "pt"}, name
        assert shape(table["en"]) == shape(table["pt"]), name
        assert table == expected[name], name   # word for word as in design-notes/texts-ideas.md
    # Every line they change is a line of the story's trees.
    for language in ("en", "pt"):
        for table in (people.COLD, people.WITHHELD, people.LIES):
            for person, lines in table[language].items():
                assert set(lines) <= set(people.PEOPLE[language][person]["nodes"]), person
        assert set(people.WARNED[language]) == set(WARNS.values())
    # The claim lines and the lines of a costly answer are never changed.
    for table in (people.COLD, people.WITHHELD, people.LIES):
        for person, lines in table["en"].items():
            assert CLAIMS.get(person) not in lines and not set(TARGETS[person]) & set(lines), person
    texts = [text for table in tables.values() for text in texts_of(table)]
    assert len(texts) == 2 * (7 + 4 + 2 * 1 + 3)   # specs/two-answers.md: only Leonor lies now
    for text in texts:
        for forbidden in ("14", "10 November", "10 de novembro", "1411", "account", "confess", "Tomas "):
            assert forbidden not in text, (forbidden, text)


def test_the_page_sends_rude_for_costly_answers():
    play_js = (FOLDER / "play.js").read_text(encoding="utf-8")
    for needle in ('rude ? "rude" : "talk"', "if (option.cost) penalize(option.cost)", 'operation: "talk"',
                   "Boolean(option.cost)"):
        assert needle in play_js, needle
    # The pinned penalize line is untouched, and the rude flag is passed on the line after it.
    lines = play_js.splitlines()
    pinned = next(n for n, line in enumerate(lines) if "if (option.cost) penalize(option.cost)" in line)
    assert "Boolean(option.cost)" in lines[pinned + 1]
    # The "How it was made" window says a rude answer is remembered.
    for language in ("en", "pt"):
        row = next(item for item in TEXT[language]["howto_items"] if item[1] == "prototypes/campus-3d/campus_people.py")
        assert row[2] == HOWTO[language], language
