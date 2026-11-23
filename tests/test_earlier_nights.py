"""Earlier nights: the game remembers, and one night can finally end (specs/earlier-nights.md).

Written before the code: one test for every line under "Checks" in the spec, in the same order and
under the same headings.

How to read this file:
- `finish(ending)` plays a night to that story ending through the hearing with no doubt (the
  spec's own helper). `true_night()` is the perfect night of point 8: `full_case`, Tomás and Rita
  cracked, no doubt; each of its arguments takes one of those things away.
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
- The spec does not say how the new texts are laid out inside campus_case.py, so no test reads
  them by a key: the expected texts are copied from design-notes/texts-3-nights.md below, and
  `case_strings()` walks through the whole module.
- Every game here charges at most 2.5 minutes (the copy, the decision and the files) unless it
  reports a minute on purpose, so the schedule of specs/night-schedule.md never meets it.
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
page3d = importlib.import_module("page3d")
TEXT = importlib.import_module("campus_text").TEXT

PAGE = page3d.build_page(playable=True, inline=True)
PLAYER = "detective"
# The story's endings, in the order of its list (the order of `memory.seen`, point 3).
# Changed by specs/computer-lab-backup.md ("Reviewed tests that change"): "The fifth element" is gone,
# so there are three story endings and the true ending needs those three.
ENDINGS = ["full_case", "impostor", "stolen_credits"]
# The three right answers of the hearing when Leonor helps (specs/evidence-and-hearing.md, point 10).
PERFECT = ("files", "original_photo", "backup")   # specs/computer-lab-backup.md

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

# The unknown number (B1 and B2): the line of each night, the dare that replaces it once the four
# story endings were seen, and the whisper of the three round warnings from night 3.
WHISPERS = {
    "en": {"night-2": "You again?",
           "night-3": "You again. Same coat, same scarf.",
           "night-4": "I have stopped counting the nights. You have not.",
           "later": "Look at the photo on your case file. Then tell me which of us is the fifth.",
           "dare": "Three endings, and still here. You will never get all three of them to stand with you. "
                   "Not in thirty minutes.",
           "round": "Close the computer. He is walking."},
    "pt": {"night-2": "Outra vez tu?",
           "night-3": "Outra vez tu. O mesmo casaco, o mesmo cachecol.",
           "night-4": "Eu já deixei de contar as noites. Tu não.",
           "later": "Olha para a fotografia do teu caso. Depois diz-me qual de nós é o quinto.",
           "dare": "Três finais, e continuas aqui. Nunca vais conseguir que os três fiquem do teu lado. "
                   "Não em trinta minutos.",
           "round": "Fecha o computador. Ele vem aí."},
}

# The true ending (B3), as the snapshot carries it once it is earned.
# Changed by specs/night-and-clues.md ("Reviewed tests that change"): the night ends at 23:00, so the
# true ending's title and its wall clock say 23:01. Was: 22:46.
VOICES = ["rita", "duarte", "duarte", "professor"]
TRUE_ENDING = {
    "en": {"title": "23:01", "stamp": "THE NIGHT IS OVER", "emoji": "🌅", "voices": VOICES, "text": (
        'You do not wait for Duarte to finish his sentences; you have heard them before. Three claims, three '
        'answers, each one on the table before he stops speaking, and the professor never once looks away from '
        'you. Then the door opens and nobody is alone any more. Leonor comes in with her phone, Tomás with his '
        'slides, Rita counting under her breath. "Four. I counted." Duarte looks at the four of you standing '
        'together, and for the first time his smile has nowhere to go. "You again." It is not a question. '
        '"I only ever needed one of you to doubt the other three." He pushes back his hood. There is no stranger '
        'under it: only a hat, a scarf and a long coat, and they are yours. The professor crosses out the fifth '
        'name. When you look back at the front row the seat is empty; on it lies a phone with every message you '
        'ever received from the unknown number, written and never sent. Your own phone buzzes one last time. The '
        'sender is no longer unknown: the name on the screen is your own. The clock on the wall reads 23:01. '
        'Nobody has switched off the lights. "Tomorrow, the four of you present." In the photo on the cover '
        'there are four people, and you know every one of them.')},
    "pt": {"title": "23:01", "stamp": "A NOITE ACABOU", "emoji": "🌅", "voices": VOICES, "text": (
        'Não esperas que o Duarte acabe as frases; já as ouviste antes. Três afirmações, três respostas, cada uma '
        'em cima da mesa antes de ele se calar, e o professor não tira os olhos de ti uma única vez. Depois a '
        'porta abre-se e já ninguém está sozinho. A Leonor entra com o telemóvel, o Tomás com os slides, a Rita '
        'a contar baixinho. «Quatro. Eu contei.» O Duarte olha para os quatro, juntos, e pela primeira vez o '
        'sorriso dele não tem para onde ir. «Outra vez tu.» Não é uma pergunta. «Só precisava que um de vocês '
        'duvidasse dos outros três.» Puxa o capuz para trás. Por baixo não há nenhum desconhecido: só um chapéu, '
        'um cachecol e um casaco comprido, e são os teus. O professor risca o quinto nome. Quando voltas a olhar '
        'para a primeira fila, a cadeira está vazia; em cima dela ficou um telemóvel com todas as mensagens que '
        'recebeste do número desconhecido, escritas e nunca enviadas. O teu telemóvel vibra uma última vez. O '
        'remetente já não é desconhecido: o nome no ecrã é o teu. O relógio da parede marca 23:01. Ninguém apagou '
        'as luzes. «Amanhã apresentam os quatro.» Na fotografia da capa estão quatro pessoas, e tu conheces todas.')},
}

# The interface texts of campus_text.py (C1 and C2).
NIGHT_TEXTS = {
    "en": {"night_lines": ["Night {n}. The fifth figure in the photo is darker than it was yesterday.",
                           "Night {n}. The fifth figure's long coat has a colour now. Yours.",
                           "Night {n}. A long coat, and a scarf like yours.",
                           "Night {n}. A coat, a scarf and a hat. You own all three.",
                           "Night {n}. Somebody has written your initial where the question mark was."],
           "night_done": "No more nights. The photo shows four people.",
           "memory_answer": "You have heard this before"},
    "pt": {"night_lines": ["Noite {n}. A quinta figura da fotografia está mais escura do que ontem.",
                           "Noite {n}. O casaco comprido da quinta figura agora tem cor. A do teu.",
                           "Noite {n}. Um casaco comprido, e um cachecol como o teu.",
                           "Noite {n}. Um casaco, um cachecol e um chapéu. Tu tens os três.",
                           "Noite {n}. Alguém escreveu a tua inicial onde estava o ponto de interrogação."],
           "night_done": "Acabaram-se as noites. A fotografia mostra quatro pessoas.",
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


def case():
    """The case file (campus_case.py), where the spec puts every secret text of this feature."""
    return importlib.import_module("campus_case")


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
    """Play a night to this story ending through the hearing with no doubt (the spec's `finish`).

    Leonor's choice chooses the story's ending (specs/computer-lab-backup.md): she helps for
    `full_case`, she is accused for `impostor`, and for `stolen_credits` she is never asked and leaves
    at 22:30. The backup answers the claim about the messages in every case.
    """
    leonor = {"full_case": "ask_for_help", "impostor": "accuse", "stolen_credits": None}[ending]
    investigate(player, language, leonor)
    third = "backup"
    if leonor is None:
        at(15, player, language)   # Leonor leaves undecided: her clue is lost and the auditorium opens
    walk("auditorium", player, language)
    result = hear("files", "original_photo", third, player=player, language=language)
    assert result["ending"]["id"] == ending and result["hearing"]["doubts"] == 0, ending
    return result


def true_night(player=PLAYER, language="en", leonor="ask_for_help", tomas=True, rita=True, caught=False,
               answers=PERFECT):
    """The perfect night of point 8, or that night with one thing changed: the story's `full_case`
    (Leonor helps), Tomás and Rita cracked, three right answers.
    `caught` keeps the player at computer 12, before the backup, when Duarte passes at minute 12
    (one doubt; specs/computer-lab-backup.md). Returns the reply to the last answer of the hearing."""
    investigate(player, language, leonor, backup=not caught)
    if caught:
        assert at(12, player, language)["night"]["caught"] is True
        do("save_backup", player, language)
    if tomas:
        crack_tomas(player, language)
    if rita:
        crack_rita(player, language)
    walk("auditorium", player, language)
    return hear(*answers, player=player, language=language)


def presented_directly(player=PLAYER, language="en"):
    """The perfect night, but `present_evidence` is played directly (a hand-made request): no hearing."""
    investigate(player, language)
    crack_tomas(player, language)
    crack_rita(player, language)
    walk("auditorium", player, language)
    return do("present_evidence", player, language)


# ---------- helpers: the table `runs` and the night's notes ----------

def remember(player, *endings, language="en"):
    """Rows of nights this name has already finished, written with the new db.add_run as the server
    writes them when a night ends. Then tonight's game is opened; its reply is returned."""
    for ending in endings:
        db.add_run(player, ending)
    return call(language=language, player=player)


def earned(player, language="en"):
    """The story endings seen on earlier nights, then the perfect night: the true ending."""
    remember(player, *ENDINGS, language=language)
    result = true_night(player, language)
    assert result["ending"]["id"] == "night_over"
    return result


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


def whisper(language, night, seen_all=False):
    """The message of the unknown number expected as night `night` starts (B1)."""
    if seen_all:
        return {"id": f"night-{night}", "text": WHISPERS[language]["dare"]}
    key = f"night-{night}" if night <= 4 else "later"
    return {"id": f"night-{night}", "text": WHISPERS[language][key]}


def round_text(result, mark):
    """The text of the round warning `round-<mark>` in this reply (None when it is not there)."""
    return next((message["text"] for message in result["night"]["messages"] if message["id"] == f"round-{mark}"),
                None)


def shows(where, text):
    """True when `text` is inside `where`, also in the way JSON writes it: a quote becomes \\" and,
    in the page, an accented letter becomes \\u00e1."""
    forms = {text, json.dumps(text)[1:-1], json.dumps(text, ensure_ascii=False)[1:-1]}
    return any(form in where for form in forms)


def as_text(result):
    """A reply as one text, to search it for sentences that should not be there."""
    return json.dumps(result, ensure_ascii=False)


def flat(table):
    """Every text inside a table, whatever its layout (dictionaries and lists inside each other)."""
    if isinstance(table, str):
        return [table]
    if isinstance(table, dict):
        table = list(table.values())
    if not isinstance(table, (list, tuple)):
        return []   # a number or None is not a text
    return [text for value in table for text in flat(value)]


def case_strings():
    """Every text of campus_case.py, in all its tables."""
    module = case()
    return flat([value for name, value in vars(module).items() if not name.startswith("_")])


def sentences(text):
    """The sentences of a text with more than three words (shorter ones could be anywhere)."""
    return [part for part in re.split(r'(?<=[.!?"»])\s+', text) if len(part.split()) > 3]


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
    db.add_run("ana", "impostor")
    assert db.load_runs("ana") == ["stolen_credits", "impostor"] == runs("ana")
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
        assert result["memory"] == {"night": 1, "seen": [], "open": False, "over": False}, language
        assert result["whispers"] == [], language
        # Every snapshot has it, not only `open`.
        assert do("go_print_shop", player, language)["memory"]["night"] == 1, language


def test_a_finished_night_is_recorded_once():
    ended = finish("impostor")
    assert runs() == ["impostor"]
    assert ended["memory"]["seen"] == ["impostor"]
    before = saved()
    assert call()["ending"]["id"] == "impostor"                     # a reload
    assert answer("concede")["heard"] is False                      # a fourth answer of the hearing
    assert at(20)["ending"]["id"] == "impostor"                     # a report of the page
    assert runs() == ["impostor"]
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
    assert next_night()["memory"] == {"night": 2, "seen": [], "open": False, "over": False}


def test_a_plain_restart_is_not_a_night():
    call()
    for _ in range(5):
        do("go_print_shop")   # a night that has started, and did not finish
        restarted = next_night()
    assert restarted["memory"]["night"] == 1 and call()["memory"]["night"] == 1
    assert runs() == []


def test_the_night_number_grows_only_after_the_restart():
    ended = finish("impostor")
    assert ended["memory"]["night"] == 1   # while the ending is on the screen
    assert call()["memory"]["night"] == 1  # and after a reload of it
    assert next_night()["memory"]["night"] == 2
    assert call()["memory"]["night"] == 2


def test_the_shown_ending_is_the_one_remembered():
    investigate()   # the story's full_case
    walk("auditorium")
    ended = hear("concede", "concede", "concede")
    assert ended["ending"]["id"] == "stolen_credits"   # three doubts cap it
    assert game.load(PLAYER)["ending"] == "full_case"
    assert runs() == ["stolen_credits"]
    assert ended["memory"]["seen"] == ["stolen_credits"]


def test_memory_belongs_to_the_name():
    finish("impostor", "ana")
    assert next_night("ana")["memory"]["night"] == 2
    other = call(player="rui")
    assert other["memory"] == {"night": 1, "seen": [], "open": False, "over": False}
    assert other["whispers"] == []
    assert runs("rui") == []


def test_a_damaged_run_note_cannot_count_a_night_twice_or_raise():
    for number, damaged in enumerate(("yes", 7, None)):   # None: the note is missing
        player = f"damaged {number}"
        finish("impostor", player)
        if damaged is None:
            change_notes(player, drop=("run",))
        else:
            change_notes(player, run=damaged)
        reloaded = call(player=player)                         # raises nothing
        assert reloaded["ending"]["id"] == "impostor", damaged
        assert answer("concede", player)["heard"] is False, damaged
        at(20, player)
        assert runs(player) == ["impostor"], damaged           # no second row
        assert reloaded["memory"]["night"] in (1, 2), damaged  # at most one too high
        assert next_night(player)["memory"]["night"] == 2, damaged


# ---------- The unknown number ----------

def test_night_2_opens_with_you_again_in_both_languages():
    for language in ("en", "pt"):
        player = f"again {language}"
        finish("impostor", player, language)
        second = next_night(player, language)
        assert second["whispers"] == [{"id": "night-2", "text": WHISPERS[language]["night-2"]}], language


def test_each_night_has_its_line_and_four_endings_change_it():
    for language in ("en", "pt"):
        for night in (3, 4, 5, 9):
            # Earlier nights that ended at 22:45: they count, and they open nothing.
            result = remember(f"night {night} {language}", *["time_up"] * (night - 1), language=language)
            assert result["memory"]["night"] == night and result["memory"]["open"] is False
            assert result["whispers"] == [whisper(language, night)], (language, night)
        for night in (4, 9):
            # The story endings, then the rest: the dare replaces the line of the night.
            # (specs/computer-lab-backup.md: three endings, so the earliest such night is night 4.)
            earlier = ENDINGS + ["time_up"] * (night - 1 - len(ENDINGS))
            result = remember(f"open {night} {language}", *earlier, language=language)
            assert result["memory"]["night"] == night and result["memory"]["open"] is True
            assert result["whispers"] == [whisper(language, night, seen_all=True)], (language, night)


def test_from_night_3_the_round_warning_changes():
    for language in ("en", "pt"):
        for night in (1, 2, 3, 6):
            player = f"rounds {night} {language}"
            remember(player, *["time_up"] * (night - 1), language=language)
            for mark in (12, 19, 26):
                text = round_text(at(mark - 1, player, language), mark)   # the same ids as before
                expected = TEXT[language]["schedule"]["round"] if night < 3 else WHISPERS[language]["round"]
                assert text == expected, (language, night, mark)


def test_no_whisper_after_an_ending_and_none_after_the_true_ending():
    finish("impostor")
    assert next_night()["whispers"] != []          # night 2 opens with its line
    ended = finish("full_case")
    assert ended["whispers"] == [] and call()["whispers"] == []

    over = earned("over")
    assert over["whispers"] == [] and call(player="over")["whispers"] == []
    later = next_night("over")
    assert later["memory"]["over"] is True and later["memory"]["night"] == len(ENDINGS) + 2   # specs/computer-lab-backup.md
    assert later["whispers"] == []                 # the number is quiet


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


# ---------- The true ending ----------

def test_the_true_ending_needs_the_four_endings_seen_before_tonight():
    # Changed by specs/computer-lab-backup.md: three story endings now, so two seen before tonight.
    remember(PLAYER, "impostor", "stolen_credits")
    tonight = true_night()   # the perfect night, with two endings seen before it
    assert tonight["ending"]["id"] == "full_case"
    assert runs()[-1] == "full_case"
    assert tonight["memory"]["seen"] == ENDINGS and tonight["memory"]["open"] is True   # this night completes the four
    assert tonight["memory"]["over"] is False
    next_night()
    assert true_night()["ending"]["id"] == "night_over"   # the next perfect night is the true ending


def test_the_true_ending_needs_no_doubt_and_both_words():
    almost = {"one wrong answer": dict(answers=("files", "files", "backup")),
              "one catch": dict(caught=True),
              "no tomas": dict(tomas=False),
              "no rita": dict(rita=False),
              # specs/computer-lab-backup.md: the story's impostor now comes from accusing Leonor
              "leonor accused": dict(leonor="accuse")}
    for player, change in almost.items():
        remember(player, *ENDINGS)
        ended = true_night(player, **change)
        assert ended["ending"]["id"] != "night_over", player
        assert runs(player)[-1] != "night_over" and ended["memory"]["over"] is False, player


def test_the_true_ending_is_shown_saved_and_recorded():
    for language in ("en", "pt"):
        player = f"true {language}"
        ending = earned(player, language)["ending"]
        expected = TRUE_ENDING[language]
        assert ending["id"] == "night_over"
        for key in ("title", "text", "stamp", "emoji", "voices"):
            assert ending[key] == expected[key], (language, key)
        assert ending["verdict"] == ""
        state = game.load(player)
        assert state["ending"] == "full_case" and logic.is_valid_state(STORIES[language], state)
        reloaded = call(language=language, player=player)
        assert reloaded["ending"] == ending
        assert runs(player)[-1] == "night_over"
        assert reloaded["memory"]["over"] is True


def test_presenting_directly_never_gives_the_true_ending():
    remember(PLAYER, *ENDINGS)
    ended = presented_directly()
    assert ended["ending"]["id"] == "full_case"
    assert runs()[-1] == "full_case" and ended["memory"]["over"] is False
    assert call()["ending"]["id"] == "full_case"


def test_the_four_story_endings_stay_reachable_after_the_gate_opens():
    assert remember(PLAYER, *ENDINGS)["memory"]["open"] is True
    for ending in ENDINGS:
        ended = finish(ending)   # it checks the shown ending
        assert ended["memory"]["open"] is True and ended["memory"]["over"] is False, ending
        next_night()
    assert runs() == ENDINGS + ENDINGS


def test_a_damaged_verdict_cannot_give_the_true_ending():
    # An earned true ending is shown again after `open`.
    earned("earned")
    assert call(player="earned")["ending"]["id"] == "night_over"

    # `night_over` written by hand on a night that ended in stolen_credits.
    remember("capped", *ENDINGS)
    finish("stolen_credits", "capped")
    change_notes("capped", verdict="night_over")
    assert call(player="capped")["ending"]["id"] == "stolen_credits"

    # And on a full_case with no hearing (present_evidence played directly).
    remember("direct", *ENDINGS)
    presented_directly("direct")
    change_notes("direct", verdict="night_over")
    assert call(player="direct")["ending"]["id"] == "full_case"
    assert runs("capped")[-1] == "stolen_credits" and runs("direct")[-1] == "full_case"


def test_the_true_ending_says_who_speaks_each_line_in_both_languages():
    play_js = (FOLDER / "play.js").read_text(encoding="utf-8")
    table = re.search(r"const VOICES = \{(.*?)\};", play_js, re.S).group(1)
    speakers = set(re.findall(r"(\w+): \[", table)) - {"narrator"}   # the people play.js has a voice for
    assert {"rita", "duarte", "professor"} <= speakers
    for language in ("en", "pt"):
        ending = earned(f"voices {language}", language)["ending"]
        spoken = [quote for quote in quotes(ending["text"]) if is_spoken(quote)]
        assert len(spoken) == 4 == len(ending["voices"]), (language, spoken)
        assert all(who in speakers for who in ending["voices"]), language
        assert ending["voices"] == VOICES, language


def test_the_secret_texts_are_never_in_the_page_nor_in_an_early_snapshot():
    secrets = ["night_over", "23:01"]   # was "22:46" (specs/night-and-clues.md)
    for language in ("en", "pt"):
        secrets += [TRUE_ENDING[language]["stamp"]] + list(WHISPERS[language].values())
        secrets += sentences(TRUE_ENDING[language]["text"])
    # The server has them: every text is in campus_case.py (the id may be a key there, so it is read in the source).
    strings = case_strings()
    assert [text for text in secrets[2:] if not any(text in string for string in strings)] == []
    assert "night_over" in (FOLDER / "campus_case.py").read_text(encoding="utf-8")

    assert [secret for secret in secrets if shows(PAGE, secret)] == []
    # Night-1 snapshots: a new game, and a perfect first night (the gate is closed).
    new_game = call(player="newcomer")
    assert "memory" in new_game
    ended = true_night("first night")
    assert ended["ending"]["id"] == "full_case"
    for snapshot in (new_game, ended):
        assert [secret for secret in secrets if shows(as_text(snapshot), secret)] == []
    for language in ("en", "pt"):
        assert [ending["id"] for ending in page3d.language_data(language)["endings"]] == ENDINGS, language


def test_the_story_still_has_its_four_endings_in_the_same_order():
    # A guard: green before and after the feature.
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
        for key in ("night_lines", "night_done", "memory_answer"):
            assert TEXT[language][key] == NIGHT_TEXTS[language][key], (language, key)
        assert len(TEXT[language]["notices"]) == 4, language
        assert len(page3d.EXTRA[language]["group"]) == 4, language   # the four names of the case file


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
                dict(operation="restart", confirmed=True, seen=["impostor"])):
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
