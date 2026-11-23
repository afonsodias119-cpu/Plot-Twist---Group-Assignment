"""More to find in the rooms: student life on the walls, and two red herrings (specs/more-to-find.md).

Written before the code: one test for every line under "Checks" in the spec, in the same order.

How to read this file:
- `peek(thing)` is the new `examine` operation: the player looks at one thing of a room.
- "saves nothing" means the database file has the same bytes before and after (`saved()`).
- A test that expects a ValueError first sends one valid `examine` in the same game and checks its
  reply. Without that, the test would pass today for the wrong reason ("Unknown operation").
- The new tables of campus_search.py (FINDS, FIND_MINUTES, FIND_LATER, FIND_TEXT) are read inside the
  tests, never when the file is loaded, so pytest can read this file before they exist.
- The expected texts are copied word for word from design-notes/texts-ideas.md, part E.
- `campus_case.CASES` comes with specs/case-of-the-day.md and specs/culprit-of-the-night.md. A game
  cannot be put into a given case from here, and `unlock` compares the code with the case's own
  `code`; so "2311 is wrong in every case" is checked as: no case (and not PC12_CODE) has the code
  2311, and 2311 is refused at computer 12 in a game played now. Before CASES exists only
  PC12_CODE is a code.
"""

import importlib
import json
import math
import re
import sys
from pathlib import Path

import pytest

import db

FOLDER = Path(__file__).resolve().parents[1] / "prototypes" / "campus-3d"
sys.path.insert(0, str(FOLDER))
campus = importlib.import_module("campus_game")
search = importlib.import_module("campus_search")
page3d = importlib.import_module("page3d")
TEXT = importlib.import_module("campus_text").TEXT

PAGE = page3d.build_page(playable=True, inline=True)
TABLE_JS = (FOLDER / "table.js").read_text(encoding="utf-8")
PLAY_JS = (FOLDER / "play.js").read_text(encoding="utf-8")
GAME_HTML = (FOLDER / "game3d.html").read_text(encoding="utf-8")
PLAYER = "detective"

# The room of each thing (point 2), and which ones are only flavour (point 4).
ROOM = {"price_list": "print_shop", "order_book": "print_shop", "noticeboard": "library",
        "returns_trolley": "library", "lab_whiteboard": "computer_lab", "computer7": "computer_lab"}
# Changed by specs/professor-before-podium.md ("Reviewed tests that change"): the podium is gone, the
# auditorium has nothing to look at. Was: "podium": "auditorium" in ROOM and "podium" in FLAVOUR.
FLAVOUR = ("price_list", "noticeboard", "returns_trolley", "lab_whiteboard")
HERRINGS = ("order_book", "computer7")

# E1: the three new objects of the table, (label, "nothing" text).
TABLE_KINDS = {
    "en": {"student_card": ("Student card", "Someone's student card. The photo is from first year, and nobody would recognise the face now."),
           "timetable": ("Exam timetable", "The exam timetable. Corporate Finance is circled three times in red, with a small skull next to it."),
           "receipt": ("Pizza receipt", "Last night's pizza receipt: four margheritas, the bill split four ways.")},
    "pt": {"student_card": ("Cartão de estudante", "O cartão de estudante de alguém. A fotografia é do primeiro ano, e hoje ninguém reconheceria aquela cara."),
           "timetable": ("Calendário de exames", "O calendário de exames. Finanças Empresariais está rodeado três vezes a vermelho, com uma caveira pequenina ao lado."),
           "receipt": ("Talão da pizza", "O talão da pizza de ontem à noite: quatro pizzas margherita, a conta dividida por quatro.")},
}

# E2: FIND_TEXT as the spec's texts give it.
FIND_TEXTS = {
    "en": {
        "price_list": {"name": "Price list", "text": "A laminated price list. Black and white, 5 cents. Colour, 25 cents. Thesis binding: ask nicely. Thesis binding after midnight: ask even more nicely."},
        "order_book": {"name": "Order book",
                       "text": "You leaf back through a year of orders until you find your group's: cover photo, 5 prints. Five.",
                       "later": "Your group's order again: cover photo, 5 prints. In the margin, in the clerk's handwriting: one for each of you and one for the professor's file. Five prints, not five people."},
        "noticeboard": {"name": "Noticeboard", "text": "The library noticeboard. Silence, please. Lost: a grey umbrella. Lost: the will to live, last seen in week 7 of Corporate Finance."},
        "returns_trolley": {"name": "Returns trolley", "text": "A trolley of returned books. On top, 'Excel for People Who Hate Excel', with a sticky note inside the cover: it did not help."},
        "lab_whiteboard": {"name": "Whiteboard", "text": "A perfect supply and demand graph, drawn with care. Underneath, in smaller letters: help."},
        "computer7": {"name": "Computer 7",
                      "text": "Computer 7 is locked too. A sticky note on its screen: pw 2311, presentation day!!",
                      "later": "The sticky note on computer 7 again: 2311, the day of the presentation. Someone's own computer, someone's own password. It has nothing to do with computer 12."},    },
    "pt": {
        "price_list": {"name": "Tabela de preços", "text": "Uma tabela de preços plastificada. Preto e branco, 5 cêntimos. Cores, 25 cêntimos. Encadernação de tese: pedir com jeitinho. Encadernação de tese depois da meia-noite: pedir com ainda mais jeitinho."},
        "order_book": {"name": "Livro de pedidos",
                       "text": "Folheias um ano inteiro de pedidos até encontrares o do vosso grupo: fotografia da capa, 5 impressões. Cinco.",
                       "later": "Outra vez o pedido do vosso grupo: fotografia da capa, 5 impressões. Na margem, com a letra da funcionária: uma para cada um e uma para o processo do professor. Cinco impressões, não cinco pessoas."},
        "noticeboard": {"name": "Quadro de avisos", "text": "O quadro de avisos da biblioteca. Silêncio, por favor. Perdido: um guarda-chuva cinzento. Perdida: a vontade de viver, vista pela última vez na semana 7 de Finanças Empresariais."},
        "returns_trolley": {"name": "Carrinho das devoluções", "text": "Um carrinho de livros devolvidos. Em cima, 'Excel para Quem Odeia Excel', com um post-it dentro da capa: não ajudou."},
        "lab_whiteboard": {"name": "Quadro branco", "text": "Um gráfico de oferta e procura perfeito, desenhado com cuidado. Por baixo, em letra mais pequena: socorro."},
        "computer7": {"name": "Computador 7",
                      "text": "O computador 7 também está bloqueado. Um post-it no ecrã: pw 2311, dia da apresentação!!",
                      "later": "Outra vez o post-it do computador 7: 2311, o dia da apresentação. O computador de alguém, a password de alguém. Não tem nada a ver com o computador 12."},    },
}

# E3: the interface texts of campus_text.py.
INTERFACE = {"en": {"look_title": "Look at", "examine_where": "That is not here.", "press_look": "Press the K key to look: {name}"},
             "pt": {"look_title": "Ver", "examine_where": "Isso não está aqui.", "press_look": "Clica na tecla K para ver: {name}"}}


# ---------- helpers: requests ----------

def call(operation="open", language="en", player=PLAYER, **extra):
    """One request to the server, exactly as the page sends it."""
    return campus.command(dict(operation=operation, language=language, player=player, **extra))


def peek(thing, player=PLAYER, language="en"):
    """Look at one thing of a room (the new `examine` operation)."""
    return call("examine", language, player, thing=thing)


def saved():
    """The bytes of the database file: equal before and after means nothing was written."""
    return db.DB_PATH.read_bytes()


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


def investigate(player=PLAYER, language="en"):
    """A new game played up to the computer lab with every clue, as in tests/test_night_schedule.py."""
    return play("open_drawer", "go_print_shop", "request_copy", "go_study_room", "go_library", "ask_for_help",
                "go_study_room", "go_computer_lab", "view_files", "save_backup",   # specs/computer-lab-backup.md
                language=language, player=player)


def to_the_auditorium(player=PLAYER, language="en"):
    """Every clue, then into the auditorium (the hearing has not started)."""
    investigate(player, language)
    return walk("auditorium", player, language)


def ended(player=PLAYER, language="en"):
    """A game that has ended: every clue, then the evidence presented directly (impostor)."""
    to_the_auditorium(player, language)
    result = do("present_evidence", player, language)
    assert result["ending"]
    return result


def refused(result, message):
    """A refused `examine`: the reason, not accepted, and no thing."""
    assert result["accepted"] is False
    assert result["message"] == message
    assert result["examine"] is None


def seen(result, thing, language, text_key="text", minutes=0):
    """An accepted `examine` of `thing`: its id, name, text and minutes."""
    assert result["accepted"] is True
    assert result["examine"] == {"id": thing, "name": FIND_TEXTS[language][thing]["name"],
                              "text": FIND_TEXTS[language][thing][text_key], "minutes": minutes}


def drawn():
    """The objects of the ITEMS list of table.js, in order, as (kind, x, y)."""
    items = TABLE_JS[TABLE_JS.index("const ITEMS = ["):TABLE_JS.index("];", TABLE_JS.index("const ITEMS = ["))]
    return [(kind, float(x), float(y)) for kind, x, y in re.findall(r'\["([a-z_]+)", (-?[\d.]+), (-?[\d.]+),', items)]


def shows(where, text):
    """True when `text` is inside `where`, also in the way JSON writes it."""
    forms = {text, json.dumps(text)[1:-1], json.dumps(text, ensure_ascii=False)[1:-1]}
    return any(form in where for form in forms)


def all_find_texts():
    """Every `text` and `later` of FIND_TEXT, in both languages."""
    return [entry[key] for language in ("en", "pt") for entry in search.FIND_TEXT[language].values()
            for key in ("text", "later") if key in entry]


# ---------- Checks ----------

def test_the_new_table_kinds_are_in_every_list():
    kinds = [kind for kind, _x, _y in drawn()]
    stick = next((x, y) for kind, x, y in drawn() if kind == "usb_stick")
    for kind in ("student_card", "timetable", "receipt"):
        assert kind in search.SPOTS, kind
        for language in ("en", "pt"):
            label, text = TABLE_KINDS[language][kind]
            assert TEXT[language]["spots"][kind] == label, (language, kind)
            assert search.SEARCH_TEXT[language]["nothing"][kind] == text, (language, kind)
        assert kinds.count(kind) == 1, kind
        assert f"    {kind}: () =>" in TABLE_JS, kind   # its own drawing
        x, y = next((x, y) for k, x, y in drawn() if k == kind)
        assert math.dist((x, y), stick) > 150, kind   # away from the stick
    assert search.PEN_SPOT == "usb_stick"


def test_looking_at_flavour_costs_nothing_and_saves_nothing():
    for language in ("en", "pt"):
        player = f"flavour-{language}"
        to_the_auditorium(player, language)
        for thing in FLAVOUR:
            walk(ROOM[thing], player, language)   # walking costs nothing and goes through the study room
            before = saved()
            result = peek(thing, player, language)
            seen(result, thing, language)
            assert result["night"]["charged"] == 0
            assert saved() == before, thing


def test_the_order_book_costs_two_minutes_and_reads_differently_with_the_photo():
    call()
    walk("print_shop")
    result = peek("order_book")
    seen(result, "order_book", "en", minutes=2)
    assert result["night"]["charged"] == 2 and result["night"]["minute"] == 2
    # With the original photo the same look reads the margin note, and costs nothing.
    play("open_drawer", "go_print_shop", "request_copy", player="holder")
    before = saved()
    result = peek("order_book", "holder")
    seen(result, "order_book", "en", "later", 0)
    assert result["night"]["charged"] == 0
    assert saved() == before
    play("open_drawer", "go_print_shop", "request_copy", language="pt", player="titular")
    seen(peek("order_book", "titular", "pt"), "order_book", "pt", "later", 0)


def test_computer_7s_code_is_never_a_code():
    # Every case has the one code of computer 12, the date of the cover photo (specs/calendar-code.md).
    case_module = importlib.import_module("campus_case")
    assert all("code" not in case for case in case_module.CASES.values())
    assert search.PC12_CODE == "1710" and search.PC12_CODE != "2311"
    play("open_drawer", "go_computer_lab")
    seen(peek("computer7"), "computer7", "en")   # before the files: the sticky note, and free
    before = saved()
    result = call("unlock", code="2311")
    assert result["unlocked"] is False and result["accepted"] is False
    assert result["message"] == TEXT["en"]["code_wrong"]
    assert saved() == before
    do("view_files")
    seen(peek("computer7"), "computer7", "en", "later")


def test_look_needs_the_room_and_no_ending():
    call()
    for thing in ROOM:   # from the study room, none of them is here
        before = saved()
        refused(peek(thing), TEXT["en"]["examine_where"])
        assert saved() == before, thing
    walk("library")
    refused(peek("price_list"), TEXT["en"]["examine_where"])
    ended("over")
    for thing in ("noticeboard", "price_list"):   # was "podium" (specs/professor-before-podium.md)
        before = saved()
        result = peek(thing, "over")
        refused(result, TEXT["en"]["examine_where"])
        assert result["finds"] == []
        assert saved() == before, thing


def test_look_is_locked_during_the_hearing_and_closed_at_2245():
    to_the_auditorium()
    assert call("hearing", answer="start")["accepted"]
    before = saved()
    refused(peek("price_list"), TEXT["en"]["hearing_locked"])   # was "podium" (specs/professor-before-podium.md)
    assert saved() == before
    call(player="late")
    walk("print_shop", "late")
    call("time", player="late", minute=30)
    before = saved()
    refused(peek("price_list", "late"), TEXT["en"]["time_up_title"])
    refused(peek("order_book", "late"), TEXT["en"]["time_up_title"])
    assert saved() == before


def test_look_rejects_unknown_things_and_extra_fields():
    call()
    walk("print_shop")
    seen(peek("price_list"), "price_list", "en")   # a valid examine first: the operation exists
    for thing in ("knife", 7, ["price_list"], "podium", None, "PRICE_LIST"):   # "podium" is now unknown too
        before = saved()
        with pytest.raises(ValueError):
            peek(thing)
        assert saved() == before, thing
    before = saved()
    with pytest.raises(ValueError):
        call("examine", thing="price_list", extra=1)
    with pytest.raises(ValueError):
        call("examine")   # no thing
    assert saved() == before


def test_finds_lists_only_the_saved_rooms_things_and_no_text():
    names = FIND_TEXTS["en"]
    expected = lambda room: [{"id": thing, "name": names[thing]["name"]} for thing in ROOM if ROOM[thing] == room]
    start = call()
    assert start["finds"] == []   # the study room has its table, not things to look at
    for room in ("print_shop", "library", "computer_lab"):
        assert walk(room)["finds"] == expected(room), room
    # Changed by specs/computer-lab-backup.md ("Reviewed tests that change"): there is no group chat; the
    # lab keeps its things after the files and the backup.
    lab = play("open_drawer", "go_computer_lab", "view_files", "save_backup", player="chat")
    assert lab["scene"] == "computer_lab"
    assert lab["finds"] == expected("computer_lab")
    assert to_the_auditorium("hall")["finds"] == expected("auditorium")
    for result in (start, lab):
        everything = json.dumps(result, ensure_ascii=False)
        for text in all_find_texts():
            assert text not in everything
        assert all(set(find) == {"id", "name"} for find in result["finds"])
    assert ended("over")["finds"] == []


def test_the_red_herrings_name_no_code_date_or_person():
    for language in ("en", "pt"):
        for thing in HERRINGS:
            entry = search.FIND_TEXT[language][thing]
            for key in ("text", "later"):
                # the code and the day of the photo (17 October, specs/calendar-code.md), the old ones, and no person
                for word in (search.PC12_CODE, "17", "October", "outubro", "1411", "14", "Duarte", "Leonor", "Rita", "Tomás"):
                    assert word not in entry[key], (language, thing, key, word)


def test_find_texts_have_the_same_keys_in_both_languages_and_are_not_in_the_page():
    things = {thing for group in search.FINDS.values() for thing in group}
    assert {thing: room for room, group in search.FINDS.items() for thing in group} == ROOM
    assert search.FIND_MINUTES == {"order_book": 2}
    assert search.FIND_LATER == {"order_book": {"has": ["original_photo"]}, "computer7": {"flags": {"files_viewed": True}}}
    for language in ("en", "pt"):
        assert set(search.FIND_TEXT[language]) == things
        for thing, entry in search.FIND_TEXT[language].items():
            assert set(entry) == ({"name", "text", "later"} if thing in search.FIND_LATER else {"name", "text"}), thing
    assert search.FIND_TEXT == FIND_TEXTS
    for text in all_find_texts():
        assert not shows(PAGE, text), text
    # The minutes of the herring live in their own table: the cost table keeps its keys.
    clock = importlib.import_module("campus_clock")
    assert "order_book" not in clock.COSTS and "examine" not in clock.COSTS


def test_the_page_can_look():
    assert 'send("examine"' in PLAY_JS and "look_title" in PLAY_JS and "press_look" in PLAY_JS
    for language in ("en", "pt"):
        for key, text in INTERFACE[language].items():
            assert TEXT[language][key] == text, (language, key)
    # A spot in the 3D for each thing, at least 1.2 m from every person (and from Duarte at the lab door).
    spots = {thing: (float(x), float(z)) for thing, x, z in
             re.findall(r'\{ id: "([a-z_0-9]+)", x: (-?[\d.]+), z: (-?[\d.]+) \}', GAME_HTML)}
    for thing in ROOM:
        assert thing in spots, thing
    people = [(float(x), float(z)) for x, z in re.findall(r"placeNpc\(\{[^}]*\}, (-?[\d.]+), (-?[\d.]+),", GAME_HTML)]
    door = re.search(r"lab_door: \{ x: (-?[\d.]+), z: (-?[\d.]+)", GAME_HTML)
    people.append((float(door.group(1)), float(door.group(2))))
    assert len(people) >= 7   # the seven of the story (and the security desk's guard, specs/security-desk.md)
    for thing in ROOM:
        for person in people:
            assert math.dist(spots[thing], person) >= 1.2, (thing, person)
