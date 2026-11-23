"""Earlier nights: the game remembers, and one night can finally end (specs/earlier-nights.md).

Written before the code: one test for every line under "Checks" in the spec, in the same order and
under the same headings.

How to read this file:
- `finish(ending)` plays a night to that story ending through the hearing (the spec's own helper).
  specs/three-proofs.md removed the true ending of point 8 and its helpers: the story now has two
  endings, chosen by the proofs.
- "saves nothing" means the database file has the same bytes before and after (`saved()`).
- A test that expects a ValueError first sends one valid request of the same operation in the same
  game and checks its reply, and a valid `open` whose reply has `memory`. Without that, the test
  would pass today for the wrong reason (the old operations already refuse extra fields).
- The counting tests play their nights for real. The other tests write the rows of earlier nights
  with the new `db.add_run` (`remember()`), exactly as the server writes them when a night ends,
  so they do not have to play four nights first. A row `time_up` is a finished night that is not
  a story ending: it moves the night number and opens nothing.
- The new module campus_memory.py is imported inside `memory_rules()`, not at the top, so pytest
  can read this file while it does not exist yet. The new texts are read inside the tests.
- The expected texts are copied from design-notes/texts-3-nights.md below.
- Every game here charges at most 2.5 minutes (the copy, the decision and the files) unless it
  reports a minute on purpose, so the schedule of specs/night-schedule.md never meets it.
"""

import ast
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
page3d = importlib.import_module("page3d")
TEXT = importlib.import_module("campus_text").TEXT

PAGE = page3d.build_page(playable=True, inline=True)
PLAYER = "detective"
# The story's endings, in the order of its list (the order of `memory.seen`, point 3).
# Changed by specs/computer-lab-backup.md ("Reviewed tests that change"): "The fifth element" is gone.
# Changed by specs/three-proofs.md ("Reviewed tests that change"): Leonor can no longer be accused, so
# "The impostor" is gone too; the story has two endings and there is no true ending.
ENDINGS = ["full_case", "stolen_credits"]

# The six memory answers (point 5): person -> (the first night it is offered, the line it leads to,
# its label in each language), word for word as in design-notes/texts-3-nights.md (A1).
MEMORY = {
    "amelia": (2, "again", {"en": "Say the date before she does", "pt": "Dizer a data antes dela"}),
    "tomas": (2, "slides", {"en": "Tell him you know what the chat says about the slides",
                            "pt": "Dizer-lhe que já sabes o que o chat diz sobre os slides"}),
    "duarte": (2, "again", {"en": "Ask him how many nights this has been",
                            "pt": "Perguntar-lhe quantas noites já foram"}),
    "rita": (3, "five", {"en": "Tell her you remember her counting heads",
                         "pt": "Dizer-lhe que te lembras de ela contar as cabeças"}),
    "leonor": (3, "again", {"en": "Tell her you knew she would say exactly that",
                            "pt": "Dizer-lhe que sabias que ela ia dizer exatamente isso"}),
    "professor": (4, "again", {"en": "Ask if he has heard this case before", "pt": "Perguntar se já ouviu este caso"}),
}
# The clerk's new line `again` (A2).
CLERK_AGAIN = ('The clerk stops with her hand on the printer. "The seventeenth of October. Yes. How do you...?" '
               'She looks at the clock. "I have been closing in ten minutes for a very long time." '
               'She frowns at the counter. "Odd. I do not remember you leaving."')

# The unknown number (B1 and B2): the line of each night and the whisper of the three round warnings
# from night 3. Changed by specs/three-proofs.md: no true ending, so no dare.
WHISPERS = {
    "en": {"night-2": "You again?",
           "night-3": "You again. Same coat, same scarf.",
           "night-4": "I have stopped counting the nights. You have not.",
           "later": "Look at the photo on your case file. Then tell me which of us is the fifth.",
           "round": "Close the computer. He is walking."},
    "pt": {"night-2": "Outra vez tu?",
           "night-3": "Outra vez tu. O mesmo casaco, o mesmo cachecol.",
           "night-4": "Eu já deixei de contar as noites. Tu não.",
           "later": "Olha para a fotografia do teu caso. Depois diz-me qual de nós é o quinto.",
           "round": "Fecha o computador. Ele vem aí."},
}

# The interface texts of campus_text.py (C1 and C2). Changed by specs/three-proofs.md: no "night_done".
NIGHT_TEXTS = {
    "en": {"night_lines": ["Night {n}. The fifth figure in the photo is darker than it was yesterday.",
                           "Night {n}. The fifth figure's long coat has a colour now. Yours.",
                           "Night {n}. A long coat, and a scarf like yours.",
                           "Night {n}. A coat, a scarf and a hat. You own all three.",
                           "Night {n}. Somebody has written your initial where the question mark was."],
           "memory_answer": "You have heard this before"},
    "pt": {"night_lines": ["Noite {n}. A quinta figura da fotografia está mais escura do que ontem.",
                           "Noite {n}. O casaco comprido da quinta figura agora tem cor. A do teu.",
                           "Noite {n}. Um casaco comprido, e um cachecol como o teu.",
                           "Noite {n}. Um casaco, um cachecol e um chapéu. Tu tens os três.",
                           "Noite {n}. Alguém escreveu a tua inicial onde estava o ponto de interrogação."],
           "memory_answer": "Já ouviste isto antes"},
}


# ---------- helpers: requests ----------

def call(operation="open", language="en", player=PLAYER, **extra):
    """One request to the server, exactly as the page sends it."""
    return campus.command(dict(operation=operation, language=language, player=player, **extra))


def saved():
    """The bytes of the database file: equal before and after means nothing was written."""
    return db.DB_PATH.read_bytes()


def memory_rules():
    """The new module campus_memory.py. Imported here so this file can be collected before it exists."""
    return importlib.import_module("campus_memory")


def at(minute, player=PLAYER, language="en"):
    """The page reports its campus minute (the `time` operation of specs/night-schedule.md)."""
    return call("time", language, player, minute=minute)


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
    if game.load(player)["scene"] != room:
        walk(room, player, language)


def talk(person, node, player=PLAYER, language="en"):
    """One line of a conversation (the `talk` operation)."""
    return call("talk", language, player, npc=person, node=node)


def next_night(player=PLAYER, language="en"):
    """The confirmed "New game": the next night of this name starts."""
    return call("restart", language, player, confirmed=True)


# ---------- helpers: the steps of a night ----------

def investigate(player=PLAYER, language="en", leonor="ask_for_help", backup=True):
    """A new game played up to the computer lab, as in tests/test_evidence_and_hearing.py: the USB
    stick, the copy, the decision about Leonor (None: she is never asked), the old files (2.5 charged
    minutes) and, unless `backup` is False, the backup of the conversations. The player stands beside Tomás.
    Changed by specs/computer-lab-backup.md: the chat and its flags are gone."""
    steps = ["open_drawer", "go_print_shop", "request_copy", "go_study_room",
             "go_library", leonor, "go_study_room", "go_computer_lab", "view_files"]
    if leonor is None:
        steps = ["open_drawer", "go_print_shop", "request_copy", "go_study_room", "go_computer_lab", "view_files"]
    if backup:
        steps.append("save_backup")
    call(language=language, player=player)
    for action in steps:
        do(action, player, language)


def show(card, npc, node, player=PLAYER, language="en"):
    """Show one card to a person on one of their lines (the `confront` operation)."""
    return call("confront", language, player, npc=npc, node=node, evidence=card)


def crack_tomas(player=PLAYER, language="en"):
    """In the computer lab: the file history on his claim line cracks him (specs/computer-lab-backup.md)."""
    assert show("files", "tomas", "slides", player, language)["confront"]["cracked"] is True


def crack_rita(player=PLAYER, language="en"):
    """With the original photo: walk to the study room and break her claim line."""
    walk("study_room", player, language)
    assert show("original_photo", "rita", "five", player, language)["confront"]["cracked"] is True


def answer(value, player=PLAYER, language="en"):
    """One request of the `hearing` operation: "start", "concede" or the id of a card."""
    return call("hearing", language, player, answer=value)


def hear(*answers, player=PLAYER, language="en"):
    """Start the hearing and give these answers, one for each claim. Returns the last reply."""
    assert answer("start", player, language)["accepted"], "start"
    for value in answers:
        result = answer(value, player, language)
        assert result["heard"] is True, value
    return result


def finish(ending, player=PLAYER, language="en"):
    """Play a night to this story ending through the hearing (the spec's `finish`).

    Changed by specs/three-proofs.md: the proofs choose the ending. Leonor always helps. For
    `full_case` the backup is saved and the three answers are right (no doubt); for `stolen_credits`
    the backup is never saved, so the claim about the messages is conceded.
    """
    # Changed by specs/camera-proof.md ("Reviewed tests that change"): for `full_case` the recording is
    # kept too and answers the fourth claim; for `stolen_credits` both are conceded (two doubts).
    full = ending == "full_case"
    investigate(player, language, backup=full)
    if full:
        assert call("footage", language, player, camera="computer_lab", minute=23 * 60 + 47)["footage"] is True
    walk("auditorium", player, language)
    last = ["backup", "footage"] if full else ["concede", "concede"]
    result = hear("files", "original_photo", *last, player=player, language=language)
    assert result["ending"]["id"] == ending, ending
    assert result["hearing"]["doubts"] == (0 if full else 2), ending
    return result


# ---------- helpers: the table `runs` and the night's notes ----------

def remember(player, *endings, language="en"):
    """Rows of nights this name has already finished, written with the new db.add_run as the server
    writes them when a night ends. Then tonight's game is opened; its reply is returned."""
    for ending in endings:
        db.add_run(player, ending)
    return call(language=language, player=player)


def runs(player=PLAYER):
    """The endings of this player's rows in the table `runs`, oldest first, read straight from the file."""
    with closing(sqlite3.connect(db.DB_PATH)) as connection:
        rows = connection.execute("SELECT ending FROM runs WHERE player = ? ORDER BY id", (player,)).fetchall()
    return [row[0] for row in rows]


def table_names():
    with closing(sqlite3.connect(db.DB_PATH)) as connection:
        return {row[0] for row in connection.execute("SELECT name FROM sqlite_master WHERE type = 'table'")}


def change_notes(player, drop=(), **changes):
    """Rewrite this player's night notes by hand, the way a damaged file would have them: the saved
    notes, with the notes in `drop` taken out and the ones in `changes` replaced. The minute stays."""
    night = db.load_night(player)
    notes = {key: value for key, value in night["notes"].items() if key not in drop}
    notes.update(changes)
    with closing(sqlite3.connect(db.DB_PATH)) as connection, connection:
        connection.execute("INSERT OR REPLACE INTO nights (player, minute, notes) VALUES (?, ?, ?)",
                           (player, night["minute"], json.dumps(notes)))


# ---------- helpers: reading a reply and the source ----------

def marked(reply):
    """The answers of a `talk` reply that are marked as memory answers, as (label, next)."""
    return [(option["label"], option["next"]) for option in reply["options"] if option.get("memory")]


def leads_to(reply):
    """The line ids a `talk` reply offers."""
    return [option["next"] for option in reply["options"]]


def whisper(language, night):
    """The message of the unknown number expected as night `night` starts (B1)."""
    key = f"night-{night}" if night <= 4 else "later"
    return {"id": f"night-{night}", "text": WHISPERS[language][key]}


def round_text(result, mark):
    """The text of the round warning `round-<mark>` in this reply (None when it is not there)."""
    return next((message["text"] for message in result["night"]["messages"] if message["id"] == f"round-{mark}"),
                None)


def code_only(text):
    """A source text without its comments, so a comment that explains a rule cannot fail a check."""
    return "\n".join(line.split("#")[0] for line in text.splitlines())


# ---------- Counting nights ----------

def test_the_database_has_a_runs_table_and_old_files_get_it():
    db.init_db()
    db.init_db()   # a second call changes nothing and does not fail
    assert {"games", "nights", "runs"} <= table_names()
    with closing(sqlite3.connect(db.DB_PATH)) as connection:
        # Each row of table_info is (position, name, type, not null, default, primary key).
        columns = [(row[1], row[2], row[3], row[5]) for row in connection.execute("PRAGMA table_info(runs)")]
        create = connection.execute("SELECT sql FROM sqlite_master WHERE name = 'runs'").fetchone()[0]
    assert columns == [("id", "INTEGER", 0, 1), ("player", "TEXT", 1, 0), ("ending", "TEXT", 1, 0)]
    assert "AUTOINCREMENT" in create.upper()

    # The two new functions: one row per call, and load_runs gives that name's endings, oldest first.
    db.add_run("ana", "stolen_credits")
    db.add_run("rui", "full_case")
    db.add_run("ana", "full_case")   # specs/three-proofs.md: "impostor" is no longer an ending
    assert db.load_runs("ana") == ["stolen_credits", "full_case"] == runs("ana")
    before = saved()
    assert db.load_runs("nobody") == []
    assert saved() == before   # reading never writes

    # A file from before this feature: it has a saved game and neither `nights` nor `runs`.
    call()
    with closing(sqlite3.connect(db.DB_PATH)) as connection, connection:
        connection.execute("DROP TABLE IF EXISTS nights")
        connection.execute("DROP TABLE IF EXISTS runs")
    assert not {"nights", "runs"} & table_names()
    db.init_db()
    assert {"games", "nights", "runs"} <= table_names()
    assert game.load(PLAYER) == STORIES["en"]["start"]   # the saved game is still there


def test_the_first_night_is_night_1_with_nothing_seen():
    for language in ("en", "pt"):
        player = f"first {language}"
        result = call(language=language, player=player)
        # Changed by specs/three-proofs.md ("Reviewed tests that change"): no "open" and no "over".
        assert result["memory"] == {"night": 1, "seen": []}, language
        assert result["whispers"] == [], language
        # Every snapshot has it, not only `open`.
        assert do("go_print_shop", player, language)["memory"]["night"] == 1, language


def test_a_finished_night_is_recorded_once():
    # Changed by specs/three-proofs.md ("Reviewed tests that change"): the night ends in stolen_credits, not impostor.
    ended = finish("stolen_credits")
    assert runs() == ["stolen_credits"]
    assert ended["memory"]["seen"] == ["stolen_credits"]
    before = saved()
    assert call()["ending"]["id"] == "stolen_credits"                     # a reload
    assert answer("concede")["heard"] is False                      # a fourth answer of the hearing
    assert at(20)["ending"]["id"] == "stolen_credits"                     # a report of the page
    assert runs() == ["stolen_credits"]
    assert saved() == before


def test_presenting_directly_records_the_night_too():
    investigate()
    walk("auditorium")
    ended = do("present_evidence")   # a hand-made request: no hearing was started
    assert ended["ending"]["id"] == "full_case"
    assert runs() == ["full_case"]
    assert ended["memory"]["seen"] == ["full_case"]
    call()
    at(20)
    assert runs() == ["full_case"]


def test_the_faculty_closing_is_recorded_once_as_time_up():
    call()
    closed = at(30)
    assert closed["night"]["closed"] is True
    assert runs() == ["time_up"]
    assert at(30)["night"]["closed"] is True   # the same report again
    assert call()["night"]["closed"] is True   # and a reload
    assert runs() == ["time_up"]
    assert closed["memory"]["seen"] == []      # a closed faculty is not a story ending
    # Changed by specs/three-proofs.md ("Reviewed tests that change"): no "open" and no "over".
    assert next_night()["memory"] == {"night": 2, "seen": []}


def test_a_plain_restart_is_not_a_night():
    call()
    for _ in range(5):
        do("go_print_shop")   # a night that has started, and did not finish
        restarted = next_night()
    assert restarted["memory"]["night"] == 1 and call()["memory"]["night"] == 1
    assert runs() == []


def test_the_night_number_grows_only_after_the_restart():
    ended = finish("stolen_credits")
    assert ended["memory"]["night"] == 1   # while the ending is on the screen
    assert call()["memory"]["night"] == 1  # and after a reload of it
    assert next_night()["memory"]["night"] == 2
    assert call()["memory"]["night"] == 2


def test_the_shown_ending_is_the_one_remembered():
    investigate()   # the story's full_case
    walk("auditorium")
    ended = hear("concede", "concede", "concede", "concede")   # specs/camera-proof.md: four claims
    assert ended["ending"]["id"] == "stolen_credits"   # three doubts cap it
    assert game.load(PLAYER)["ending"] == "full_case"
    assert runs() == ["stolen_credits"]
    assert ended["memory"]["seen"] == ["stolen_credits"]


def test_memory_belongs_to_the_name():
    finish("stolen_credits", "ana")
    assert next_night("ana")["memory"]["night"] == 2
    other = call(player="rui")
    # Changed by specs/three-proofs.md ("Reviewed tests that change"): no "open" and no "over".
    assert other["memory"] == {"night": 1, "seen": []}
    assert other["whispers"] == []
    assert runs("rui") == []


def test_a_damaged_run_note_cannot_count_a_night_twice_or_raise():
    for number, damaged in enumerate(("yes", 7, None)):   # None: the note is missing
        player = f"damaged {number}"
        finish("stolen_credits", player)
        if damaged is None:
            change_notes(player, drop=("run",))
        else:
            change_notes(player, run=damaged)
        reloaded = call(player=player)                         # raises nothing
        assert reloaded["ending"]["id"] == "stolen_credits", damaged
        assert answer("concede", player)["heard"] is False, damaged
        at(20, player)
        assert runs(player) == ["stolen_credits"], damaged           # no second row
        assert reloaded["memory"]["night"] in (1, 2), damaged  # at most one too high
        assert next_night(player)["memory"]["night"] == 2, damaged


# ---------- The unknown number ----------

def test_night_2_opens_with_you_again_in_both_languages():
    for language in ("en", "pt"):
        player = f"again {language}"
        finish("stolen_credits", player, language)
        second = next_night(player, language)
        assert second["whispers"] == [{"id": "night-2", "text": WHISPERS[language]["night-2"]}], language


def test_each_night_has_its_line():
    # Changed by specs/three-proofs.md ("Reviewed tests that change"): no dare, so the story endings
    # seen before no longer change the line of the night.
    for language in ("en", "pt"):
        for night in (3, 4, 5, 9):
            # Earlier nights that ended at 22:45 count; so do earlier story endings.
            result = remember(f"night {night} {language}", *["time_up"] * (night - 1), language=language)
            assert result["memory"]["night"] == night
            assert result["whispers"] == [whisper(language, night)], (language, night)
            earlier = ENDINGS + ["time_up"] * (night - 1 - len(ENDINGS))
            result = remember(f"seen {night} {language}", *earlier, language=language)
            assert result["memory"]["night"] == night
            assert result["whispers"] == [whisper(language, night)], (language, night)


def test_from_night_3_the_round_warning_changes():
    for language in ("en", "pt"):
        for night in (1, 2, 3, 6):
            player = f"rounds {night} {language}"
            remember(player, *["time_up"] * (night - 1), language=language)
            for mark in (12, 19, 26):
                text = round_text(at(mark - 1, player, language), mark)   # the same ids as before
                expected = TEXT[language]["schedule"]["round"] if night < 3 else WHISPERS[language]["round"]
                assert text == expected, (language, night, mark)


def test_no_whisper_after_an_ending():
    # Changed by specs/three-proofs.md ("Reviewed tests that change"): there is no true ending to stay quiet after.
    finish("stolen_credits")
    assert next_night()["whispers"] != []          # night 2 opens with its line
    ended = finish("full_case")
    assert ended["whispers"] == [] and call()["whispers"] == []


# ---------- Answers heard before ----------

def test_memory_answers_appear_only_from_their_night():
    for language in ("en", "pt"):
        for night in (1, 2, 3, 4):
            player = f"memory {night} {language}"
            assert remember(player, *["time_up"] * (night - 1), language=language)["memory"]["night"] == night
            investigate(player, language)   # every clue: the auditorium opens, and everybody can be met
            for person, (first, target, labels) in MEMORY.items():
                walk_to(person, player, language)
                start = talk(person, "start", player, language)
                if night >= first:
                    assert marked(start) == [(labels[language], target)], (language, night, person)
                else:   # absent: no ↺ answer, and no answer of `start` leads to its line
                    assert marked(start) == [] and target not in leads_to(start), (language, night, person)
                # Ordinary answers are not marked.
                assert all(not option.get("memory") for option in start["options"]
                           if option["label"] != labels[language]), (language, night, person)


def test_a_memory_line_cannot_be_asked_for_before_its_night():
    # Night 1: the clerk's new line and Tomás's claim line (files not viewed) cannot be asked for.
    assert call()["memory"]["night"] == 1
    walk("print_shop")
    assert talk("amelia", "start")["name"] == "Clerk"   # a valid talk first
    before = saved()
    with pytest.raises(ValueError):
        talk("amelia", "again")
    assert saved() == before
    walk("computer_lab")
    assert talk("tomas", "start")["name"] == "Tomás"
    before = saved()
    with pytest.raises(ValueError):
        talk("tomas", "slides")
    assert saved() == before

    # Night 2: both lines answer.
    remember("returning", "time_up")
    walk("print_shop", "returning")
    again = talk("amelia", "again", "returning")
    assert again["node"] == "again" and again["text"] == CLERK_AGAIN
    walk("computer_lab", "returning")
    assert talk("tomas", "slides", "returning")["node"] == "slides"

    # Once Tomás has cracked, his `start` no longer offers the shortcut, and `slides` raises again.
    remember("cracked", "time_up")
    investigate("cracked")
    shortcut = (MEMORY["tomas"][2]["en"], "slides")
    assert marked(talk("tomas", "start", "cracked")) == [shortcut]   # offered before he cracks
    crack_tomas("cracked")
    start = talk("tomas", "start", "cracked")
    assert marked(start) == [] and "slides" not in leads_to(start)
    with pytest.raises(ValueError):
        talk("tomas", "slides", "cracked")


def test_both_languages_have_the_same_nights_and_no_new_cost():
    def nights_of(language):
        """(person, line, the line it leads to) -> night, for every answer that has a `night`."""
        return {(person, node, option["next"]): option["night"]
                for person, data in people.PEOPLE[language].items()
                for node, line in data["nodes"].items() for option in line["options"] if "night" in option}

    def costly(language):
        return {(person, node, option["next"])
                for person, data in people.PEOPLE[language].items()
                for node, line in data["nodes"].items() for option in line["options"] if "cost" in option}

    expected = {(person, "start", target): first for person, (first, target, _labels) in MEMORY.items()}
    assert nights_of("en") == nights_of("pt") == expected
    assert all(type(night) is int for night in nights_of("en").values())   # True is not a night
    rude = {("leonor", "start", "harsh"), ("leonor", "harsh", "closed"), ("tomas", "start", "hard"),
            ("tomas", "hard", "closed"), ("duarte", "start", "know"), ("duarte", "know", "closed")}
    assert costly("en") == costly("pt") == rude   # still the six rude answers (tests/test_harder_campus.py)


def test_talking_on_a_later_night_still_saves_nothing():
    assert remember(PLAYER, "time_up", "time_up", "time_up")["memory"]["night"] == 4   # all six are offered
    investigate()
    for person, (_first, target, _labels) in MEMORY.items():
        walk_to(person)
        before = saved()
        assert marked(talk(person, "start")), person
        assert talk(person, target)["node"] == target, person
        assert saved() == before, person


# ---------- The endings ----------
# Changed by specs/three-proofs.md ("Reviewed tests that change"): the true ending is gone, and so are
# its eight tests (the gate, the doubts, showing it, presenting directly, the damaged verdict, the
# voices and the secret texts). What is left checks that it really is gone.

def test_there_is_no_true_ending_any_more():
    remember(PLAYER, *ENDINGS)
    for ending in ENDINGS:   # every night after the story endings were seen still ends in a story ending
        assert finish(ending)["ending"]["id"] == ending
        next_night()
    assert runs() == ENDINGS + ENDINGS
    for name in ("campus_case.py", "campus_memory.py", "campus_evidence.py", "play.js"):
        source = (FOLDER / name).read_text(encoding="utf-8")
        assert "night_over" not in source and "TRUE_ENDING" not in source, name


def test_the_story_still_has_its_endings_in_the_same_order():
    # A guard: green before and after the feature. Changed by specs/three-proofs.md: two endings.
    for language in ("en", "pt"):
        assert [ending["id"] for ending in STORIES[language]["endings"]] == ENDINGS, language
        assert set(TEXT[language]["stamps"]) == set(ENDINGS), language
        assert set(TEXT[language]["ending_voices"]) <= set(ENDINGS), language
        assert [ending["id"] for ending in page3d.language_data(language)["endings"]] == ENDINGS, language


# ---------- The texts, the page and the files ----------

def test_the_night_texts_exist_in_both_languages():
    for language in ("en", "pt"):
        lines = TEXT[language]["night_lines"]
        assert len(lines) == 5 and all("{n}" in line for line in lines), language
        for key in ("night_lines", "memory_answer"):   # specs/three-proofs.md: no night_done
            assert TEXT[language][key] == NIGHT_TEXTS[language][key], (language, key)
        assert len(TEXT[language]["notices"]) == 3, language   # specs/three-proofs.md: no accusing
        # Changed by specs/combined-start-briefing.md ("Reviewed tests that change"): no group on the case file. Was: its four names.
        assert "group" not in page3d.EXTRA[language], language


def test_the_page_draws_the_fifth_figure_and_keeps_you_again_through_a_new_game():
    new = ["fifth-figure", "plot-twist-night", "function nightStage(", "ending-extra", "restarting", "option.memory"]
    kept = ["line.options.filter(option => option.next !== null && !asked.has(option.next))",
            "  function showLine(line) {", "// The player chose to do something"]
    for needle in new + kept:
        assert needle in PAGE, needle
    # PAGE holds every key of campus_text.py, used or not (page3d.py:79), so the key is looked for in play.js.
    play_js = (FOLDER / "play.js").read_text(encoding="utf-8")
    assert "memory_answer" in play_js


def test_old_operations_still_refuse_extra_fields():
    assert "memory" in call()                                   # a valid `open` has `memory`
    assert talk("rita", "start")["name"] == "Rita"              # a valid `talk`
    assert "memory" in next_night()                             # a valid `restart`
    before = saved()
    for bad in (dict(operation="open", night=2),
                dict(operation="talk", npc="rita", node="start", night=2),
                dict(operation="restart", confirmed=True, seen=["stolen_credits"])):
        with pytest.raises(ValueError):
            call(**bad)
    assert saved() == before


def test_app_3d_reloads_every_module_in_the_final_order():
    source = (PROJECT / "app_3d.py").read_text(encoding="utf-8")   # read, not run: running it starts Streamlit
    after_name = source.split("CODE_MODULES = ", 1)[1]
    modules = ast.literal_eval(after_name[:after_name.index("]") + 1])   # the list, as Python would read it
    assert modules == ["story", "logic", "db", "game", "campus_text", "campus_people", "campus_search", "campus_case",
                       "campus_clock", "campus_memory", "campus_evidence", "campus_game", "page3d"]
    # Comments are left out of both checks: a comment may well say why the module is not there.
    page_files = code_only(source.split("PAGE_FILES = ", 1)[1].split("def page_version", 1)[0])
    assert "campus_memory" not in page_files
    page3d_source = (FOLDER / "page3d.py").read_text(encoding="utf-8")
    imports = [line for line in code_only(page3d_source).splitlines()
               if line.strip().startswith(("import ", "from ")) or "import_module" in line]
    assert len(imports) >= 4   # the import lines were found
    assert not any("campus_memory" in line for line in imports)
    rules = memory_rules()   # the four names of point 3
    for name in ("night_number", "seen", "record", "memory_view"):
        assert callable(getattr(rules, name)), name
