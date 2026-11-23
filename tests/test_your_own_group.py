"""Your own group in the story: three friends' names for the three teammates (specs/your-own-group.md).

Written before the code: one test for every line under "Checks" in the spec, in the same order.

How to read this file:
- `begin(names)` begins a game with these names, as the start screen sends them
  (specs/case-of-the-day.md). The day is never today's real date: `on_day(monkeypatch, variant)`
  replaces `campus_game.case_day` with a date that gives that case, as tests/test_culprit_of_the_night.py does.
- `twin(...)` plays the same commands twice with the same detective name, each time in its own
  database file: once with the story's names (`["", "", ""]`) and once with a group. The spec's rule
  is that the group's replies are the story's replies with the whole words Leonor, Rita and Tomás
  replaced in one pass (point 5), so `as_group` writes that rule out here, on its own, and the tests
  compare. Ids are lower case, so the rule can never reach them.
- `STORY_NAME` finds a story name left in a text; with the group "Ana, Bea, João" no reply may have one.
- A test whose comparison would also hold without the feature first checks that the group is really
  in use (a name typed shows up), so it cannot pass only because nothing was renamed.
- "saves nothing" means the database file has the same bytes before and after (`saved()`).
- The texts of the page are copied word for word from design-notes/texts-ideas.md, part D.
"""

import importlib
import json
import re
import sqlite3
import sys
from contextlib import closing
from datetime import date, timedelta
from pathlib import Path

import db
import game
import logic
from story import STORIES, UI_TEXTS

PROJECT = Path(__file__).resolve().parents[1]
FOLDER = PROJECT / "prototypes" / "campus-3d"
sys.path.insert(0, str(FOLDER))
campus = importlib.import_module("campus_game")
people = importlib.import_module("campus_people")
TEXT = importlib.import_module("campus_text").TEXT

PLAYER = "detective"
NO_NAMES = ["", "", ""]
STORY_GROUP = ["Leonor", "Rita", "Tomás"]
FRIENDS = ["Ana", "Bea", "João"]
# Changed by specs/computer-lab-backup.md ("Reviewed tests that change"): the chat, its messages and the cases of
# specs/culprit-of-the-night.md are gone; three story endings, and the culprit is always Duarte.
# Changed by specs/three-proofs.md ("Reviewed tests that change"): two story endings, chosen by the proofs, and no
# true ending, so no night starts with every ending seen and the list ENDINGS is gone.
STORY_NAME = re.compile(r"\b(Leonor|Rita|Tomás)\b")
# Part D of design-notes/texts-ideas.md, word for word.
GROUP_TEXTS = {
    "en": {"group_title": "Your group (optional)",
           "group_hint": "Type three friends' names and they take the teammates' places in the story. Leave a field empty to keep the story's name.",
           "group_slots": ["In Leonor's place (she)", "In Rita's place (she)", "In Tomás's place (he)"],
           "group_reset": "Some names could not be used, so the story keeps its own there.",
           "group_kept": "This game keeps the group it started with. A new game with another detective name can have another group."},
    "pt": {"group_title": "O teu grupo (opcional)",
           "group_hint": "Escreve os nomes de três amigos e eles ficam no lugar dos colegas da história. Deixa um campo vazio para ficar o nome da história.",
           "group_slots": ["No lugar da Leonor (ela)", "No lugar da Rita (ela)", "No lugar do Tomás (ele)"],
           "group_reset": "Alguns nomes não puderam ser usados, por isso a história ficou com os seus.",
           "group_kept": "Este jogo fica com o grupo com que começou. Um jogo novo com outro nome de detetive pode ter outro grupo."},
}


# ---------- helpers: the day and the requests ----------

def clock():
    """campus_clock.py, where the case of each day is decided."""
    return importlib.import_module("campus_clock")


def day_of(variant):
    """A date that gives this case (at most a month after 22 November 2026)."""
    for step in range(31):
        day = date(2026, 11, 22) + timedelta(days=step)
        if clock().case_of_day(day) == variant:
            return day
    raise AssertionError(f"no day gives the case {variant}")


def on_day(monkeypatch, variant):
    """From now on the server believes that today is a day of this case."""
    day = day_of(variant)
    monkeypatch.setattr(campus, "case_day", lambda: day)


def call(operation="open", language="en", player=PLAYER, **extra):
    """One request to the server, exactly as the page sends it."""
    return campus.command(dict(operation=operation, language=language, player=player, **extra))


def begin(names, language="en", player=PLAYER):
    """The operation `begin` with these three names."""
    return call("begin", language, player, names=names)


def do(action, player=PLAYER, language="en"):
    """Play one story action. It must be accepted."""
    result = call("play", language, player, action=action)
    assert result["accepted"], action
    return result


def talk(person, node, player=PLAYER, language="en"):
    return call("talk", language, player, npc=person, node=node)


def snapshot_now(player=PLAYER, language="en"):
    """The snapshot as it is now: a report of minute 0 never moves the clock and writes nothing."""
    return call("time", language, player, minute=0)


def restart(player=PLAYER, language="en"):
    return call("restart", language, player, confirmed=True)


def saved():
    return db.DB_PATH.read_bytes()


def notes(player=PLAYER):
    """The night's notes as they are saved ({} when there is no row)."""
    return db.load_night(player)["notes"]


def write_notes(player, **changes):
    """Rewrite this player's night notes by hand, the way a damaged file would have them."""
    night = db.load_night(player)
    written = dict(night["notes"], **changes)
    db.init_db()
    with closing(sqlite3.connect(db.DB_PATH)) as connection, connection:
        connection.execute("INSERT OR REPLACE INTO nights (player, minute, notes) VALUES (?, ?, ?)",
                           (player, night["minute"], json.dumps(written)))


def games_row(player=PLAYER):
    """The row of `games` exactly as it is saved."""
    with closing(sqlite3.connect(db.DB_PATH)) as connection:
        return connection.execute("SELECT * FROM games WHERE player = ?", (player,)).fetchone()


# ---------- helpers: the scripts ----------

def play(action):
    return {"operation": "play", "action": action}


def speak(person, node):
    return {"operation": "talk", "npc": person, "node": node}


def show(card, person, node):
    return {"operation": "confront", "npc": person, "node": node, "evidence": card}


def answer(value):
    return {"operation": "hearing", "answer": value}


def enter(room):
    return {"operation": "enter", "room": room}


def investigation(backup=True):
    """Every clue of the night, with a word with each teammate on the way, and (unless `backup` is
    False) the backup saved."""
    steps = [speak("rita", "start"), play("open_drawer"), play("go_print_shop"), play("request_copy"),
             play("go_study_room"), play("go_library"), speak("leonor", "start"), play("ask_for_help"),
             play("go_study_room"), play("go_computer_lab"), speak("tomas", "start"), play("view_files")]
    return steps + [play("save_backup"), FOOTAGE] if backup else steps


# Changed by specs/camera-proof.md ("Reviewed tests that change"): the picture of the recordings kept as
# the fourth proof, in every investigation that saves the backup.
FOOTAGE = {"operation": "footage", "camera": "computer_lab", "minute": 23 * 60 + 47}


def no_backup_night():
    """The backup was never saved: Duarte's third claim has no proof, so Stolen credit.
    Changed by specs/three-proofs.md ("Reviewed tests that change"): it replaces the night where Leonor was accused."""
    return investigation(backup=False) + [enter("auditorium"), answer("start"), answer("files"),
                                          answer("original_photo"), answer("concede"), answer("concede")]


def stolen_night():
    """Three doubts after asking Leonor for help: stolen_credits."""
    return investigation() + [enter("auditorium"), answer("start"), answer("concede"),
                              answer("concede"), answer("concede"), answer("concede")]


def perfect_night():
    """Both cracks and the three right answers (specs/earlier-nights.md, point 8)."""
    return investigation() + [show("files", "tomas", "slides"), enter("study_room"),
                              show("original_photo", "rita", "five"), enter("auditorium"), answer("start"),
                              answer("files"), answer("original_photo"), answer("backup"), answer("footage")]


def twin(monkeypatch, tmp_path, label, variant, language, steps, names=FRIENDS, runs=()):
    """The same night played twice, each in its own new database (named after `label`): with the story's
    names and with `names`. `runs` are endings seen on earlier nights, added first in both.
    Returns (story replies, group replies)."""
    on_day(monkeypatch, variant)
    replies = {}
    for way, group in (("story", NO_NAMES), ("group", names)):
        monkeypatch.setattr(db, "DB_PATH", tmp_path / f"{way} {label} {variant} {language}.db")
        for ending in runs:
            db.add_run(PLAYER, ending)
        replies[way] = [begin(group, language)] + [campus.command(dict(step, player=PLAYER, language=language))
                                                   for step in steps]
    return replies["story"], replies["group"]


# ---------- helpers: the rule of the spec, written out ----------

def as_group(value, group):
    """`value` with the whole words Leonor, Rita and Tomás replaced by `group`, in one pass, in every
    string inside it. Dict keys are never changed (point 5)."""
    names = dict(zip(STORY_GROUP, group))
    if isinstance(value, str):
        return STORY_NAME.sub(lambda match: names[match.group(1)], value)
    if isinstance(value, dict):
        return {key: as_group(inner, group) for key, inner in value.items()}
    if isinstance(value, list):
        return [as_group(inner, group) for inner in value]
    return value


def without(reply, *keys):
    return {key: value for key, value in reply.items() if key not in keys}


def text_of(reply):
    """Every text of a reply, in one string (the group itself is left out)."""
    return json.dumps(without(reply, "group"), ensure_ascii=False)


def person(reply, who):
    """The entry of `people` for this id."""
    return next(entry for entry in reply["people"] if entry["id"] == who)


def ids(reply):
    """The ids of a reply: what the page sends back or compares, never shown as a name."""
    found = {key: reply.get(key) for key in ("player", "scene", "room", "npc", "node")}
    found["evidence"] = [card["id"] for card in reply.get("evidence", [])]
    found["people"] = [entry["id"] for entry in reply.get("people", [])]
    found["actions"] = [row["id"] for row in reply.get("actions", [])]
    found["clues"] = [row["id"] for row in reply.get("clues", [])]
    found["gone"] = (reply.get("night") or {}).get("gone")
    found["said"] = [entry["who"] for entry in (reply.get("hearing") or {}).get("said", [])]
    found["ending"] = (reply.get("ending") or {}).get("id")
    found["voices"] = (reply.get("ending") or {}).get("voices")
    found["options"] = [option["next"] for option in reply.get("options", [])]
    return found


# ---------- Checks ----------

def test_no_names_keeps_the_story(monkeypatch, tmp_path):
    for language in ("en", "pt"):
        on_day(monkeypatch, "outsider")
        replies = {}
        for way in ("open", "begin"):
            monkeypatch.setattr(db, "DB_PATH", tmp_path / f"{way} {language}.db")   # the same name, in its own file
            first = call("open", language) if way == "open" else begin(NO_NAMES, language)
            replies[way] = [first] + [campus.command(dict(step, player=PLAYER, language=language))
                                      for step in no_backup_night()]
        assert replies["begin"][-1]["ending"]["id"] == "stolen_credits", language   # specs/three-proofs.md
        for number, (classic, daily) in enumerate(zip(replies["open"], replies["begin"])):
            assert without(classic, "day") == without(daily, "day"), (language, number)
            if "scene" in classic:   # every snapshot, not the replies of `talk`
                assert classic["group"] == daily["group"] == STORY_GROUP, (language, number)
        assert "names" not in notes() or notes()["names"] == STORY_GROUP


def test_the_names_reach_dialogue_chat_cards_hearing_and_endings(monkeypatch, tmp_path):
    for language in ("en", "pt"):
        # Changed by specs/three-proofs.md ("Reviewed tests that change"): the impostor night became the night
        # without the backup, and the true night is gone with the true ending.
        nights = {"no backup": twin(monkeypatch, tmp_path, "no backup", "outsider", language, no_backup_night()),
                  "stolen": twin(monkeypatch, tmp_path, "stolen", "outsider", language, stolen_night()),
                  "perfect": twin(monkeypatch, tmp_path, "perfect", "outsider", language, perfect_night())}
        endings = {"no backup": "stolen_credits", "stolen": "stolen_credits", "perfect": "full_case"}
        for night, (story, group) in nights.items():
            assert story[-1]["ending"]["id"] == group[-1]["ending"]["id"] == endings[night], (language, night)
            for number, (told, renamed) in enumerate(zip(story, group)):
                # Every text of every reply is the story's, with the friends' names in one pass (point 5).
                assert without(renamed, "group") == as_group(without(told, "group"), FRIENDS), (language, night, number)
                assert not STORY_NAME.search(text_of(renamed)), (language, night, number)
                if "scene" in renamed:
                    assert renamed["group"] == FRIENDS and told["group"] == STORY_GROUP, (language, night, number)
        story, group = nights["no backup"]
        # Rita's greeting, and Leonor's name in `people` (the library).
        greeting = group[1]
        assert greeting["npc"] == "rita" and greeting["name"] == "Bea" and "Bea" in greeting["text"], language
        library = next(reply for reply in group if reply.get("scene") == "library")
        assert person(library, "leonor")["name"] == "Ana", language
        # The clue list. Changed by specs/three-proofs.md ("Reviewed tests that change"): Leonor is no longer a row of it.
        back = next(reply for reply in group if reply.get("clues"))
        assert "leonor" not in [row["id"] for row in back["clues"]], language
        # Duarte's third claim says João (specs/camera-proof.md: a fourth claim follows it, so it is the reply before).
        third = group[-3]["hearing"]["said"][-1]
        assert third["who"] == "duarte" and "João" in third["text"] and "Tomás" not in third["text"], language
        # The endings and a verdict line. Changed by specs/three-proofs.md ("Reviewed tests that change"): the two endings and the
        # verdict `missing` name nobody of the group, so they only must not show a story name.
        for night in nights.values():
            ending = night[1][-1]["ending"]
            assert not STORY_NAME.search(ending["text"] + ending["verdict"]), language


def test_names_never_chain(monkeypatch):
    on_day(monkeypatch, "outsider")
    # "Rita" in Leonor's place is another slot's name: the whole group goes back to the story's.
    refused = begin(["Rita", "Ana", "João"], player="refused")
    assert refused["group"] == STORY_GROUP
    assert "Rita" in talk("rita", "start", "refused")["name"]
    assert notes("refused").get("names", STORY_GROUP) == STORY_GROUP
    # Leonor → Bea and Rita → Ana: never Leonor → Bea → ... or Leonor → Rita → Ana.
    swapped = begin(["Bea", "Ana", "João"], player="swapped")
    assert swapped["group"] == ["Bea", "Ana", "João"]
    greeting = talk("rita", "start", "swapped")
    assert greeting["name"] == "Ana" and "Ana" in greeting["text"] and "Bea" not in greeting["text"]
    for action in ("open_drawer", "go_print_shop", "request_copy", "go_study_room", "go_library"):
        library = do(action, "swapped")
    assert person(library, "leonor")["name"] == "Bea"
    # Leonor's own line (specs/computer-lab-backup.md: the chat that showed both names is gone).
    leonor = talk("leonor", "start", "swapped")
    assert leonor["name"] == "Bea" and "Ana" not in leonor["text"]


def test_bad_names_fall_back_one_by_one():
    clean_group = people.clean_group
    assert people.DEFAULT_GROUP == STORY_GROUP
    assert clean_group(["<b>", "Bea", "João"]) == ["Leonor", "Bea", "João"]
    assert clean_group(["Ana", "x" * 15, "João"]) == ["Ana", "Rita", "João"]
    assert clean_group(["Ana", "Bea", "123"]) == ["Ana", "Bea", "Tomás"]
    assert clean_group(["  ", "Bea", "João"]) == ["Leonor", "Bea", "João"]
    assert clean_group(["ana  maria", "Bea", "João"]) == ["Ana maria", "Bea", "João"]
    # Through `begin`, the same: a bad field keeps the story's name, the others stay.
    reply = begin(["<b>x</b>", "bea", "  joão  "])
    assert reply["group"] == ["Leonor", "Bea", "João"]


def test_a_clash_or_duarte_brings_back_the_whole_story_group():
    clean_group = people.clean_group
    assert clean_group(["Ana", "Bea", "João"]) == FRIENDS   # a good group is kept
    assert clean_group(["Ana", "ana", "João"]) == STORY_GROUP
    assert clean_group(["Ana", "Bea", "ANA"]) == STORY_GROUP
    assert clean_group(["Ana", "Bea", "duarte"]) == STORY_GROUP
    assert clean_group(["Duarte", "", ""]) == STORY_GROUP
    assert begin(["Ana", "Bea", "duarte"])["group"] == STORY_GROUP


def test_ids_are_never_renamed(monkeypatch, tmp_path):
    # Early: the clerk and Leonor (undecided) have gone at minute 16, so `night.gone` has both ids.
    early = [speak("rita", "start"), play("open_drawer"), {"operation": "time", "minute": 16}]
    nights = {"early": early, "no backup": no_backup_night()}   # specs/three-proofs.md
    for label, steps in nights.items():
        story, group = twin(monkeypatch, tmp_path, label, "outsider", "en", steps)
        assert any("Bea" in text_of(reply) for reply in group), label   # the group is in use
        for number, (told, renamed) in enumerate(zip(story, group)):
            assert ids(renamed) == ids(told), (label, number)
        assert group[0]["player"] == PLAYER, label
        if label == "early":
            assert group[-1]["night"]["gone"] == ["amelia", "leonor"]   # ids, never "Ana"


def test_the_save_never_holds_the_names(monkeypatch, tmp_path):
    on_day(monkeypatch, "outsider")
    rows = {}
    for way, names in (("story", NO_NAMES), ("group", FRIENDS)):
        monkeypatch.setattr(db, "DB_PATH", tmp_path / f"{way}.db")
        begin(names)
        for action in ("open_drawer", "go_print_shop", "request_copy"):
            do(action)
        rows[way] = games_row()
        assert logic.is_valid_state(STORIES["en"], game.load(PLAYER)), way
    assert notes()["names"] == FRIENDS   # they live in the night's notes
    assert rows["group"] == rows["story"]
    assert not any("Ana" in str(column) or "João" in str(column) for column in rows["group"])


def test_a_damaged_names_note_gives_the_story_names(monkeypatch):
    on_day(monkeypatch, "outsider")
    for number, damaged in enumerate(("Ana", [1, 2, 3], ["Ana", "Bea"], ["Duarte", "Bea", "João"])):
        player = f"damaged {number}"
        begin(FRIENDS, player=player)
        assert talk("rita", "start", player)["name"] == "Bea"   # the group is in use before the damage
        write_notes(player, names=damaged)
        reply = snapshot_now(player)
        assert reply["group"] == STORY_GROUP, damaged
        greeting = talk("rita", "start", player)
        assert greeting["name"] == "Rita" and "Rita" in greeting["text"], damaged


def test_a_restart_keeps_the_group_and_a_continued_game_ignores_new_names(monkeypatch):
    on_day(monkeypatch, "outsider")
    begin(FRIENDS)
    do("open_drawer")
    restarted = restart()
    assert restarted["group"] == FRIENDS and notes()["names"] == FRIENDS
    assert game.load(PLAYER) == STORIES["en"]["start"]
    assert talk("rita", "start")["name"] == "Bea"
    # A continued game keeps its own group: the names sent now are ignored and nothing is written.
    do("open_drawer")
    before = saved()
    continued = begin(["Zé", "Rui", "Ivo"])
    assert continued["message"] == UI_TEXTS["en"]["continued"]
    assert continued["group"] == FRIENDS
    assert saved() == before
    # A game begun without a group does not get one by continuing either.
    begin(NO_NAMES, player="plain")
    do("open_drawer", "plain")
    assert begin(FRIENDS, player="plain")["group"] == STORY_GROUP
    assert talk("rita", "start", "plain")["name"] == "Rita"


def test_the_start_screen_has_three_fields_and_the_page_renames_the_tags():
    play_js = (FOLDER / "play.js").read_text(encoding="utf-8")
    game_html = (FOLDER / "game3d.html").read_text(encoding="utf-8")
    for needle in ("plot-twist-group", "group_slots", "names:"):
        assert needle in play_js, needle
    assert "state.group" in game_html
    for language in ("en", "pt"):
        t = TEXT[language]
        for key, text in GROUP_TEXTS[language].items():
            assert t[key] == text, (language, key)
        slots = t["group_slots"]
        assert len(slots) == 3, language
        assert [name in slot for name, slot in zip(STORY_GROUP, slots)] == [True, True, True], language


def test_the_names_box_is_in_the_detective_step_under_the_creator():
    # After the merge with specs/creator-after-name.md the creator has its own step ("Your detective"):
    # the group box goes there, under it, and no longer in the name box of the case file.
    play_js = (FOLDER / "play.js").read_text(encoding="utf-8")
    creator = play_js.index('stepLook.querySelector(".look-body").append(creator)')
    group = play_js.index('stepLook.querySelector(".look-body").append(groupBox)')
    assert creator < group
    assert "nameBox.append(groupBox)" not in play_js


def test_the_groups_memories_at_computer_12_say_the_friends_names():
    # The memories and the speakers' names at computer 12 (specs/calendar-code.md) are the page's own
    # texts: play.js renames them with the same one-pass rule as the server (`inGroup`).
    play_js = (FOLDER / "play.js").read_text(encoding="utf-8")
    assert r"(?<!\p{L})(Leonor|Rita|Tomás)(?!\p{L})" in play_js
    for needle in ("inGroup(t.group_clues[who])", "inGroup(HELPER_NAMES[who])", "current.group"):
        assert needle in play_js, needle
    for language in ("en", "pt"):
        clues = TEXT[language]["group_clues"]
        renamed = as_group(clues, FRIENDS)
        assert "Bea" in renamed["tomas"], language            # Tomás remembers Rita, who is Bea tonight
        assert not any(STORY_NAME.search(text) for text in renamed.values()), language
        assert as_group(clues, STORY_GROUP) == clues, language
