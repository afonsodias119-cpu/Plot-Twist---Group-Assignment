"""A different culprit some nights: Duarte alone, or a teammate who let him in
(specs/culprit-of-the-night.md).

Written before the code: one test for every line under "Checks" in the spec, in the same order.

How to read this file:
- `play_case(monkeypatch, variant)` begins a game on a date that gives that case, by replacing
  `campus_game.case_day` (specs/case-of-the-day.md): the tests never depend on today's real date.
- Every number the tests send is a shown number, as the page sends it: `FAKES[variant]` are the
  places of the three fake messages on the screen, `LATE[variant]` the place of the message with
  Tomás's name that arrived last night (the card that cracks him). Both are the spec's table.
- `investigate(...)` plays a new game up to the computer lab, as in tests/test_earlier_nights.py:
  the USB stick, the copy, the decision about Leonor, the old files (2.5 charged minutes) and the
  chat messages in `flagged`. `perfect(...)` adds both cracks and the three right answers.
- The texts a check names are copied word for word from design-notes/texts-ideas.md, part B. The
  spec names `CASES` and its keys (`order`, `accepts`, `right`, `texts`), so the checks on the texts
  themselves read that table; the other tests only use the commands.
- The cover photo, its date (Saturday 17 October) and the code `1710` are the same in every case
  (specs/calendar-code.md): the group remembers that day at computer 12, and no case changes it.
- "the classic sources" are the tables the spec lists in point 6: story.py, campus_people.PEOPLE,
  campus_case.CASE_TEXT, campus_clock.SHUTTER, campus_search.PHOTO_TEXT and campus_case.NIGHT_TEXT.
- "saves nothing" means the database file has the same bytes before and after (`saved()`).
"""

import importlib
import json
import re
import sys
from datetime import date, timedelta
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
NO_NAMES = ["", "", ""]
VARIANTS = ("outsider", "tomas", "rita")
FOUR = ["fifth_element", "full_case", "impostor", "stolen_credits"]
SOLUTION = [[piece, 0] for piece in search.PHOTO_SOLUTION]

# The spec's table (point 2), in shown numbers.
FAKES = {"outsider": (2, 4, 5), "tomas": (1, 3, 5), "rita": (1, 2, 4)}
LATE = {"outsider": 5, "tomas": 1, "rita": 4}   # the message with Tomás's name that arrived last night
# Codes that are wrong in every case: the old ones of specs/pen-and-code.md and of the first cases.
OLD_CODES = ("1411", "1011", "1311")
# The words of what the group remembers of the day of the photo: no case text may use them.
DAY_WORDS = ("October", "outubro", "Saturday", "sábado", "Finance", "Finanças", "sun", "sunny", "sol", "15", "17")

# The chat as shown, place 1 to 5 (B1.1 to B1.4, B2.1 and B2.3; the classic one is story.py's).
CHAT = {
    "en": {
        "room_leonor": 'Leonor, 3 weeks ago, 9:05 pm: "Can someone book the study room for Thursday?"',
        "room_rita": 'Rita, 3 weeks ago, 9:05 pm: "Can someone book the study room for Thursday?"',
        "room_tomas": 'Tomás, 3 weeks ago, 9:05 pm: "Can someone book the study room for Thursday?"',
        "booked_unknown": 'Unknown number, 3 weeks ago, 9:07 pm: "Booked it. I wrote the conclusion too, like always."',
        "booked_duarte": 'Duarte, 3 weeks ago, 9:07 pm: "Booked it. I wrote the conclusion too, like always."',
        "photo_rita": 'Rita, 2 weeks ago, 6:40 pm: "Photo for the cover is ready. Four of us, finally!"',
        "photo_leonor": 'Leonor, 2 weeks ago, 6:40 pm: "Photo for the cover is ready. Four of us, finally!"',
        "five_duarte": "Duarte, 3 weeks ago, 10:10 pm: \"Can't wait for the five of us to present.\"",
        "five_unknown": "Unknown number, 3 weeks ago, 10:10 pm: \"Can't wait for the five of us to present.\"",
        "late": 'Tomás, 3 weeks ago, 10:12 pm (arrived yesterday, 11:49 pm): "Duarte did the slides, obviously."',
    },
    "pt": {
        "room_leonor": 'Leonor, há 3 semanas, 21h05: "Alguém pode reservar a sala de estudo para quinta-feira?"',
        "room_rita": 'Rita, há 3 semanas, 21h05: "Alguém pode reservar a sala de estudo para quinta-feira?"',
        "room_tomas": 'Tomás, há 3 semanas, 21h05: "Alguém pode reservar a sala de estudo para quinta-feira?"',
        "booked_unknown": 'Número desconhecido, há 3 semanas, 21h07: "Já reservei. Também escrevi a conclusão, como sempre."',
        "booked_duarte": 'Duarte, há 3 semanas, 21h07: "Já reservei. Também escrevi a conclusão, como sempre."',
        "photo_rita": 'Rita, há 2 semanas, 18h40: "A fotografia para a capa está pronta. Os quatro, finalmente!"',
        "photo_leonor": 'Leonor, há 2 semanas, 18h40: "A fotografia para a capa está pronta. Os quatro, finalmente!"',
        "five_duarte": 'Duarte, há 3 semanas, 22h10: "Mal posso esperar para apresentarmos os cinco."',
        "five_unknown": 'Número desconhecido, há 3 semanas, 22h10: "Mal posso esperar para apresentarmos os cinco."',
        "late": 'Tomás, há 3 semanas, 22h12 (chegou ontem às 23h49): "Os slides foram do Duarte, claro."',
    },
}
SHOWN = {"outsider": ["room_leonor", "booked_unknown", "photo_rita", "five_duarte", "late"],
         "tomas": ["late", "room_rita", "booked_duarte", "photo_leonor", "five_unknown"],
         "rita": ["booked_unknown", "five_duarte", "photo_leonor", "late", "room_tomas"]}

# The ending `full_case` of each teammate case (B1.25, B2.25).
FULL_CASE = {
    "tomas": {
        "en": "You show the history on the USB stick and the three messages you flagged: one from Duarte himself, weeks before anyone had heard of him; one from a number nobody knew, counting five of you; and one under Tomás's name that arrived last night, two minutes after his own account changed the shared folder. Leonor walks in with the original messages, and they match. Before the professor can ask, Tomás stands up and tells the room what he did: the name, the photo and the message, all for slides he never made. The professor crosses the fifth name off the list. Tomorrow, the four of you present, and Tomás presents the slides he finishes tonight.",
        "pt": "Mostras o histórico da pen e as três mensagens que marcaste: uma do próprio Duarte, semanas antes de alguém ter ouvido falar dele; uma de um número que ninguém conhecia, a contar cinco; e uma com o nome do Tomás que chegou ontem à noite, dois minutos depois de a conta dele ter alterado a pasta partilhada. A Leonor entra com as mensagens originais, e batem certo. Antes de o professor perguntar, o Tomás levanta-se e conta o que fez: o nome, a fotografia e a mensagem, tudo por uns slides que nunca fez. O professor risca o quinto nome da lista. Amanhã apresentam os quatro, e o Tomás apresenta os slides que acaba esta noite.",
    },
    "rita": {
        "en": "You show the history on the USB stick and the three messages you flagged: one from a number nobody knew; one from Duarte, counting five of you when there were four; and one under Tomás's name that arrived last night, two minutes after Rita's account changed the shared folder. Leonor walks in with the original messages, and they match. Rita does not wait to be asked: she tells the professor that she added the name and swapped the photo, because Duarte needed a group. The professor crosses the fifth name off the list. Tomorrow, the four of you present, and Rita has a lot to explain on the way there.",
        "pt": "Mostras o histórico da pen e as três mensagens que marcaste: uma de um número que ninguém conhecia; uma do Duarte, a contar cinco quando eram quatro; e uma com o nome do Tomás que chegou ontem à noite, dois minutos depois de a conta da Rita ter alterado a pasta partilhada. A Leonor entra com as mensagens originais, e batem certo. A Rita não espera que lhe perguntem: conta ao professor que acrescentou o nome e trocou a fotografia, porque o Duarte precisava de um grupo. O professor risca o quinto nome da lista. Amanhã apresentam os quatro, e a Rita tem muito que explicar pelo caminho.",
    },
}
# The professor's line for a confession on the claim "name" (B1.24, B2.24).
NAME_RIGHT = {
    "tomas": {"en": "\"The person who put the name there has told me so himself. So much for 'since the first draft'.\"",
              "pt": "\"Quem pôs lá o nome já mo disse ele próprio. Lá se vai o 'desde o primeiro rascunho'.\""},
    "rita": {"en": "\"The person who put the name there has told me so herself. Go on.\"",
             "pt": "\"Quem pôs lá o nome já mo disse ela própria. Continue.\""},
}
# The sentence of the true ending (B1.28, B2.28; the classic one is campus_case.NIGHT_TEXT's).
TRUE_SENTENCE = {
    "outsider": {"en": "Leonor comes in with her phone, Tomás with his slides, Rita counting under her breath.",
                 "pt": "A Leonor entra com o telemóvel, o Tomás com os slides, a Rita a contar baixinho."},
    "tomas": {"en": "Tomás comes in first, with the slides he finally finished tonight, and does not look at you; then Leonor with her phone, and Rita counting under her breath.",
              "pt": "O Tomás entra primeiro, com os slides que finalmente acabou esta noite, sem olhar para ti; depois a Leonor com o telemóvel, e a Rita a contar baixinho."},
    "rita": {"en": "Leonor comes in with her phone, Tomás with his slides, and Rita last of all, slowly, counting under her breath.",
             "pt": "A Leonor entra com o telemóvel, o Tomás com os slides e, por último, devagar, a Rita, a contar baixinho."},
}
# Who changed the shared folder (B1.5, B2.5), and the two signs against the liar (B1.9, B1.10, B2.9, B2.12).
ACCOUNT = {"tomas": {"en": "from which account: Tomás's.", "pt": "a pasta diz de que conta: a do Tomás."},
           "rita": {"en": "from which account: Rita's.", "pt": "a pasta diz de que conta: a da Rita."}}
SIGNS = {
    "tomas": {"rita": {"en": "Tomás went outside for some air before half past eleven, with his hood up, and he never came back.",
                       "pt": "O Tomás foi lá para fora apanhar ar antes das onze e meia, de capuz posto, e nunca mais voltou."},
              "tomas": {"en": "I never went near computer 12.", "pt": "Nunca me aproximei do 12."}},
    "rita": {"tomas": {"en": "Long hair under it, and a pink sleeve on the mouse. I thought it was Rita, but she told us she was going home early.",
                       "pt": "Cabelo comprido por baixo e uma manga cor-de-rosa no rato. Pensei que era a Rita, mas ela tinha dito que ia cedo para casa."},
             "rita": {"en": "I went home early last night.", "pt": "Ontem fui cedo para casa."}},
}


# ---------- helpers: the case ----------

def case_file():
    """campus_case.py, where the spec puts CASES. Imported here so this file can be collected first."""
    return importlib.import_module("campus_case")


def clock():
    return importlib.import_module("campus_clock")


def day_of(variant):
    """A date that gives this case (at most a month after 22 November 2026)."""
    for step in range(31):
        day = date(2026, 11, 22) + timedelta(days=step)
        if clock().case_of_day(day) == variant:
            return day
    raise AssertionError(f"no day gives the case {variant}")


def play_case(monkeypatch, variant, player=PLAYER, language="en"):
    """Begin a game on a date that gives `variant` (the spec's `play_case`)."""
    day = day_of(variant)
    monkeypatch.setattr(campus, "case_day", lambda: day)
    return call("begin", language, player, names=NO_NAMES)


def shown_chat(variant, language):
    """The five texts of the chat as the case shows them."""
    return [CHAT[language][key] for key in SHOWN[variant]]


# ---------- helpers: requests ----------

def call(operation="open", language="en", player=PLAYER, **extra):
    """One request to the server, exactly as the page sends it."""
    return campus.command(dict(operation=operation, language=language, player=player, **extra))


def saved():
    return db.DB_PATH.read_bytes()


def do(action, player=PLAYER, language="en"):
    result = call("play", language, player, action=action)
    assert result["accepted"], action
    return result


def walk(room, player=PLAYER, language="en"):
    result = call("enter", language, player, room=room)
    assert result["accepted"], room
    return result


def talk(person, node, player=PLAYER, language="en"):
    return call("talk", language, player, npc=person, node=node)


def show(card, npc, node, player=PLAYER, language="en"):
    return call("confront", language, player, npc=npc, node=node, evidence=card)


def answer(value, player=PLAYER, language="en"):
    return call("hearing", language, player, answer=value)


def hear(*answers, player=PLAYER, language="en"):
    """Start the hearing and give these answers, one for each claim. Returns the last reply."""
    assert answer("start", player, language)["accepted"], "start"
    result = None
    for value in answers:
        result = answer(value, player, language)
        assert result["heard"] is True, value
    return result


def investigate(player=PLAYER, language="en", leonor="ask_for_help", flagged=()):
    """A game already begun, played up to the computer lab (see the module's docstring)."""
    steps = ["open_drawer", "go_print_shop", "request_copy", "go_study_room",
             "go_library", leonor, "go_study_room", "go_computer_lab", "view_files"]
    if flagged:
        steps += ["open_chat"] + [f"flag_{n}" for n in flagged] + ["go_computer_lab"]
    for action in steps:
        do(action, player, language)


def crack_tomas(variant, player=PLAYER, language="en"):
    """In the computer lab: the flagged message with his name, shown on his claim line."""
    result = show(f"msg_{LATE[variant]}", "tomas", "slides", player, language)
    assert result["confront"]["cracked"] is True
    return result


def crack_rita(player=PLAYER, language="en"):
    walk("study_room", player, language)
    result = show("original_photo", "rita", "five", player, language)
    assert result["confront"]["cracked"] is True
    return result


def perfect(variant, player=PLAYER, language="en"):
    """The perfect night of specs/earlier-nights.md, point 8, in this case's shown numbers."""
    investigate(player, language, flagged=FAKES[variant])
    crack_tomas(variant, player, language)
    crack_rita(player, language)
    walk("auditorium", player, language)
    return hear("files", "original_photo", "leonor_messages", player=player, language=language)


# ---------- helpers: the texts ----------

def leaves(table, path=()):
    """Every text inside a table, with the place where it is: [(path, text)]."""
    if isinstance(table, str):
        return [(path, table)]
    if isinstance(table, dict):
        return [found for key, value in table.items() for found in leaves(value, path + (key,))]
    if isinstance(table, (list, tuple)):
        return [found for number, value in enumerate(table) for found in leaves(value, path + (number,))]
    return []


def classic_sources(language):
    """The classic texts of one language, by source (point 6)."""
    case = case_file()
    return {"story": STORIES[language], "people": people.PEOPLE[language], "case_text": case.CASE_TEXT[language],
            "shutter": clock().SHUTTER[language], "photo_text": search.PHOTO_TEXT[language],
            "night_text": case.NIGHT_TEXT[language]}


def classic_leaves(language):
    return [((source,) + path, text) for source, table in classic_sources(language).items()
            for path, text in leaves(table)]


def sentences(text):
    """The sentences of a text with more than three words (shorter ones could be anywhere)."""
    return [part for part in re.split(r'(?<=[.!?"»])\s+', text) if len(part.split()) > 3]


def place_of(key, language):
    """Where a key is among the classic texts: [(path, text)] of every classic text that has it."""
    return [(path, text) for path, text in classic_leaves(language) if key in text]


QUOTE = re.compile(r'"([^"]+)"|«([^»]+)»|“([^”]+)”')   # the three kinds of quotation marks play.js knows


def spoken(text):
    """The spoken quotes of a text, by the rule of partsOf in play.js."""
    found = [(m.group(1) or m.group(2) or m.group(3)).strip() for m in QUOTE.finditer(text)]
    return [quote for quote in found if len(quote.split()) > 3 or any(mark in quote for mark in ".!?…")]


def shows(where, text):
    """True when `text` is inside `where`, also in the way JSON writes it."""
    forms = {text, json.dumps(text)[1:-1], json.dumps(text, ensure_ascii=False)[1:-1]}
    return any(form in where for form in forms)


def without(reply, *keys):
    return {key: value for key, value in reply.items() if key not in keys}


# ---------- Checks ----------

def test_the_classic_case_changes_nothing(monkeypatch, tmp_path):
    commands = [
        dict(operation="talk", npc="rita", node="pen"),
        dict(operation="play", action="open_drawer"),
        dict(operation="play", action="go_print_shop"),
        dict(operation="talk", npc="amelia", node="order"),
        dict(operation="assemble", pieces=SOLUTION),
        dict(operation="play", action="go_study_room"),
        dict(operation="play", action="go_library"),
        dict(operation="talk", npc="leonor", node="start"),
        dict(operation="play", action="ask_for_help"),
        dict(operation="enter", room="computer_lab"),
        dict(operation="talk", npc="tomas", node="kind"),
        dict(operation="talk", npc="tomas", node="who"),
        dict(operation="unlock", code="1411"),
        dict(operation="unlock", code=search.PC12_CODE),
        dict(operation="play", action="open_chat"),
        dict(operation="play", action="flag_2"),
        dict(operation="play", action="flag_4"),
        dict(operation="play", action="flag_5"),
        dict(operation="play", action="go_computer_lab"),
        dict(operation="confront", npc="tomas", node="slides", evidence="msg_5"),
        dict(operation="enter", room="study_room"),
        dict(operation="confront", npc="rita", node="five", evidence="original_photo"),
        dict(operation="enter", room="auditorium"),
        dict(operation="hearing", answer="start"),
        dict(operation="hearing", answer="files"),
        dict(operation="hearing", answer="original_photo"),
        dict(operation="hearing", answer="leonor_messages"),
    ]
    replies = {}
    for way in ("open", "begin"):
        monkeypatch.setattr(db, "DB_PATH", tmp_path / f"{way}.db")   # the same name, in its own file
        if way == "open":
            first = call("open")
        else:
            first = play_case(monkeypatch, "outsider")
        replies[way] = [first] + [campus.command(dict(command, player=PLAYER, language="en")) for command in commands]
    assert replies["begin"][-1]["ending"]["id"] == "full_case"
    for number, (classic, daily) in enumerate(zip(replies["open"], replies["begin"])):
        assert without(classic, "day") == without(daily, "day"), number


def test_each_case_shows_the_chat_in_its_own_order(monkeypatch):
    for variant in VARIANTS:
        for language in ("en", "pt"):
            player = f"{variant} {language}"
            play_case(monkeypatch, variant, player, language)
            investigate(player, language)
            chat = do("open_chat", player, language)["chat"]
            assert [message["text"] for message in chat["messages"]] == shown_chat(variant, language), (variant, language)
            assert chat["intro"] == STORIES[language]["scenes"]["group_chat"]["texts"][0]["text"]
            for n in FAKES[variant]:
                do(f"flag_{n}", player, language)
            do("go_computer_lab", player, language)
            walk("auditorium", player, language)
            ending = hear("files", "original_photo", "leonor_messages", player=player, language=language)["ending"]
            assert ending["id"] == "full_case", (variant, language)
            if variant in FULL_CASE:
                assert ending["text"] == FULL_CASE[variant][language], (variant, language)
            else:
                assert ending["text"] == STORIES[language]["endings"][1]["text"], language


def test_the_page_sees_only_shown_numbers(monkeypatch):
    classic = "classic"
    call("open", player=classic)
    investigate(classic)
    classic_refusal = call("play", player=classic, action="flag_1")
    assert classic_refusal["accepted"] is False
    for variant in ("tomas", "rita"):
        player = variant
        play_case(monkeypatch, variant, player)
        investigate(player)
        # A flag outside the chat is refused as before.
        refused = call("play", player=player, action="flag_1")
        assert refused["accepted"] is False and refused["message"] == classic_refusal["message"]
        opened = do("open_chat", player)
        texts = shown_chat(variant, "en")
        assert [(m["n"], m["action"]) for m in opened["chat"]["messages"]] == [(n, f"flag_{n}") for n in range(1, 6)]
        rows = [row for row in opened["actions"] if row["kind"] == "chat"]
        assert [(row["id"], row["label"]) for row in rows] == [(f"flag_{n}", f"Flag message {n}") for n in range(1, 6)]
        for n in FAKES[variant]:
            reply = do(f"flag_{n}", player)
            assert reply["message"] == f"You flag message {n} for the professor.", (variant, n)
            assert [m["flagged"] for m in reply["chat"]["messages"]][n - 1] is True
        left = [row["id"] for row in reply["actions"] if row["kind"] == "chat"]
        assert left == [f"flag_{n}" for n in range(1, 6) if n not in FAKES[variant]]
        back = do("go_computer_lab", player)
        cards = [card for card in back["evidence"] if card["id"].startswith("msg_")]
        assert [card["id"] for card in cards] == [f"msg_{n}" for n in FAKES[variant]]
        assert [card["label"] for card in cards] == ["🚩 " + texts[n - 1] for n in FAKES[variant]]
        title = STORIES["en"]["scenes"]["group_chat"]["title"]
        notes = [entry for entry in back["notebook"] if entry["title"].startswith(title)]
        assert notes == [{"title": f"{title} · {n}", "text": texts[n - 1]} for n in FAKES[variant]]
        # The card of another fake message does not crack him; the one with his name, as shown, does.
        other = next(n for n in FAKES[variant] if n != LATE[variant])
        assert show(f"msg_{other}", "tomas", "slides", player)["confront"]["cracked"] is False
        crack_tomas(variant, player)


def test_every_case_has_the_one_code_of_the_photo(monkeypatch):
    for variant in VARIANTS:
        player = f"code {variant}"
        play_case(monkeypatch, variant, player)
        do("open_drawer", player)
        walk("computer_lab", player)
        before = saved()
        for wrong_code in OLD_CODES + ("2311",):   # the old codes, and the sticky note of computer 7
            wrong = call("unlock", player=player, code=wrong_code)
            assert wrong["unlocked"] is False and wrong["accepted"] is False, (variant, wrong_code)
        assert saved() == before
        right = call("unlock", player=player, code=search.PC12_CODE)
        assert right["unlocked"] is True and right["accepted"] is True, variant
        assert game.load(player)["flags"]["files_viewed"] is True
    assert search.PC12_CODE == "1710"


def test_every_case_has_the_same_photo_and_date(monkeypatch):
    for variant in VARIANTS:
        for language in ("en", "pt"):
            player = f"photo {variant} {language}"
            begun = play_case(monkeypatch, variant, player, language)
            classic = people.PEOPLE[language]["amelia"]["nodes"]["order"]
            do("go_print_shop", player, language)
            order = talk("amelia", "order", player, language)
            assert (order["text"], order["note"]) == (classic["text"], classic["note"]), (variant, language)
            taped = call("assemble", language, player, pieces=SOLUTION)
            assert taped["assembled"] is True and taped["message"] == search.PHOTO_TEXT[language], (variant, language)
            assert taped["day"] == begun["day"]   # no stamp of its own in the snapshot
            # The slip on the shutter, once the clerk has gone (another game of the same case).
            late = f"late {variant} {language}"
            play_case(monkeypatch, variant, late, language)
            do("go_print_shop", late, language)
            closed = call("time", language, late, minute=10)
            assert closed["night"]["notice"] == clock().SHUTTER[language], (variant, language)
    photo_js = (FOLDER / "photo.js").read_text(encoding="utf-8")
    play_js = (FOLDER / "play.js").read_text(encoding="utf-8")
    assert "17.10.2026" in photo_js and "opts.stamp" not in photo_js
    assert "photo_date" not in play_js


def test_the_groups_memories_are_true_in_every_case():
    # At computer 12 Tomás, Rita and Leonor remember the day of the photo (specs/calendar-code.md). Those
    # lines are the page's own (campus_text.TEXT), never a key of a case; and no case text, swapped or new,
    # speaks of that day, so a culprit's lie never touches what the group remembers.
    cases = case_file().CASES
    for language in ("en", "pt"):
        memories = list(TEXT[language]["group_clues"].values())
        rule = people.PEOPLE[language]["tomas"]["nodes"]["password"]
        for variant in VARIANTS:
            table = cases[variant]["texts"][language]
            new_lines = [line for lines in cases[variant]["right"][language].values() for line in lines.values()]
            for key in table:
                assert not any(key in memory or memory in key for memory in memories), (variant, key)
                assert key not in (rule["text"], rule["note"]), (variant, key)
            for text in list(table) + list(table.values()) + new_lines:
                for word in DAY_WORDS:
                    assert not re.search(rf"(?<!\w){word}(?!\w)", text), (variant, language, word, text)


def test_the_confession_breaks_the_name_claim(monkeypatch):
    for variant in VARIANTS:
        for language in ("en", "pt"):
            player = f"name {variant} {language}"
            play_case(monkeypatch, variant, player, language)
            investigate(player, language, flagged=FAKES[variant])
            crack_tomas(variant, player, language)
            word = "tomas_word"
            if variant == "rita":
                crack_rita(player, language)
                word = "rita_word"
            walk("auditorium", player, language)
            assert answer("start", player, language)["accepted"]
            heard = answer(word, player, language)["hearing"]
            reply = heard["said"][-2]
            assert reply["who"] == "professor", (variant, language)
            if variant == "outsider":
                assert heard["doubts"] == 1, language
                assert reply["text"] == case_file().CASE_TEXT[language]["wrong"]["name"], language
            else:
                assert heard["doubts"] == 0, (variant, language)
                assert reply["text"] == NAME_RIGHT[variant][language], (variant, language)


def test_the_true_ending_can_be_earned_in_every_case(monkeypatch):
    for variant in VARIANTS:
        for language in ("en", "pt"):
            player = f"true {variant} {language}"
            for ending in FOUR:
                db.add_run(player, ending)
            play_case(monkeypatch, variant, player, language)
            ending = perfect(variant, player, language)["ending"]
            assert ending["id"] == "night_over", (variant, language)
            assert TRUE_SENTENCE[variant][language] in ending["text"], (variant, language)
            if variant != "outsider":
                assert TRUE_SENTENCE["outsider"][language] not in ending["text"], (variant, language)
            assert len(spoken(ending["text"])) == len(ending["voices"]) == 4, (variant, language)


def test_every_key_is_a_classic_text():
    cases = case_file().CASES
    for variant in VARIANTS:
        for language in ("en", "pt"):
            table = cases[variant]["texts"][language]
            if variant == "outsider":
                assert table == {}, language
                continue
            assert len(table) >= 20, (variant, language)
            true_text = case_file().NIGHT_TEXT[language]["ending"]["text"]
            for key, value in table.items():
                assert len(key.split()) > 3, key
                places = place_of(key, language)
                assert len(places) == 1, (variant, key, [path for path, _text in places])
                path, text = places[0]
                assert text == key or (text == true_text and key in sentences(true_text)), (variant, key)
                assert value != key and value.strip(), key
                others = [other for other in table if other != key]
                assert not any(key in other for other in others), (variant, key)   # no key is part of another
                assert not any(other in value for other in others), (variant, key)   # no value has another key


def test_case_texts_keep_their_spoken_quotes():
    cases = case_file().CASES
    for variant in ("tomas", "rita"):
        found = {}
        for language in ("en", "pt"):
            found[language] = {}
            for key, value in cases[variant]["texts"][language].items():
                path = place_of(key, language)[0][0]
                found[language][path] = len(spoken(value))
                if path[:2] in (("story", "endings"), ("night_text", "ending"), ("case_text", "right")):
                    assert len(spoken(value)) == len(spoken(key)), (variant, language, path)
            for lines in cases[variant]["right"][language].values():   # the professor's new lines
                assert all(len(spoken(line)) == 1 for line in lines.values()), (variant, language)
        assert set(found["en"]) == set(found["pt"]), variant   # the same places in both languages
        assert found["en"] == found["pt"], variant             # and the same number of spoken quotes
        assert set(cases[variant]["right"]["en"]) == set(cases[variant]["right"]["pt"]) == set(cases[variant]["accepts"])


def test_no_case_text_is_in_the_page_or_a_new_snapshot(monkeypatch):
    cases = case_file().CASES
    secret_places = (("case_text", "reveals"), ("story", "endings"), ("night_text", "ending"),
                     ("story", "scenes", "computer_lab"), ("case_text", "labels", "files"))
    for variant in ("tomas", "rita"):
        for language in ("en", "pt"):
            new_lines = [line for lines in cases[variant]["right"][language].values() for line in lines.values()]
            texts = cases[variant]["texts"][language]
            own = [(sentence, key) for key, value in texts.items() for sentence in sentences(value)
                   if sentence not in key]
            assert own, (variant, language)
            # The page has no text of any case.
            assert [sentence for sentence, _key in own if shows(PAGE, sentence)] == [], (variant, language)
            assert [line for line in new_lines if shows(PAGE, line)] == [], (variant, language)
            # A new game of this case has none of its reveals, endings or file history yet.
            fresh = json.dumps(play_case(monkeypatch, variant, f"fresh {variant} {language}", language), ensure_ascii=False)
            secret = [sentence for sentence, key in own
                      if any(place_of(key, language)[0][0][:len(where)] == where for where in secret_places)]
            assert secret, (variant, language)
            assert [sentence for sentence in secret if shows(fresh, sentence)] == [], (variant, language)
            assert variant not in json.dumps(play_case(monkeypatch, variant, f"fresh {variant} {language}", language)["day"])


def test_each_case_names_the_account_and_the_liar_can_be_checked(monkeypatch):
    for variant in ("tomas", "rita"):
        for language in ("en", "pt"):
            player = f"account {variant} {language}"
            play_case(monkeypatch, variant, player, language)
            rita_line = talk("rita", "pen", player, language)   # the study room, before anything else
            do("open_drawer", player, language)
            walk("computer_lab", player, language)
            files = call("unlock", language, player, code=search.PC12_CODE)
            assert files["unlocked"] is True
            assert ACCOUNT[variant][language] in files["message"], (variant, language)
            card = next(card for card in files["evidence"] if card["id"] == "files")
            name = "Tomás" if variant == "tomas" else "Rita"
            assert name in card["label"], (variant, language)
            assert any(name in text for text in files["texts"]), (variant, language)   # the lab's paragraph
            talk("tomas", "kind", player, language)
            tomas_line = talk("tomas", "who", player, language)
            lines = {"rita": rita_line["text"], "tomas": tomas_line["text"]}
            for who, sign in SIGNS[variant].items():
                assert sign[language] in lines[who], (variant, language, who)


def test_campus_case_is_still_data_only():
    case = case_file()
    source = (FOLDER / "campus_case.py").read_text(encoding="utf-8")
    assert not re.search(r"^\s*def ", source, flags=re.MULTILINE)
    classic = case.CASES["outsider"]
    assert classic["order"] == [1, 2, 3, 4, 5]
    assert search.PC12_CODE == "1710"   # one code for every case (specs/calendar-code.md)
    assert classic["accepts"] == {} and classic["texts"] == {"en": {}, "pt": {}}
    assert set(case.CASES) == set(VARIANTS) and set(clock().CASE_ORDER) == set(VARIANTS)
    for variant in VARIANTS:
        assert sorted(case.CASES[variant]["order"]) == [1, 2, 3, 4, 5], variant
        assert set(case.CASES[variant]) == {"order", "accepts", "right", "texts"}, variant
    # The order of the days (specs/case-of-the-day.md, point 1).
    assert [clock().case_of_day(date(2026, 11, day)) for day in (22, 23, 24)] == ["tomas", "rita", "outsider"]
