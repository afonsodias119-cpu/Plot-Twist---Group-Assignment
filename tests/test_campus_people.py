"""People, dialogues, clock, diary and chat of the 3D campus (specs/campus-people-and-atmosphere.md)."""

import importlib
import sys
from pathlib import Path

import pytest

import db
import game
from story import STORIES

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "prototypes" / "campus-3d"))
campus = importlib.import_module("campus_game")
people = importlib.import_module("campus_people")

PLAYER = "talker"


def call(operation="open", language="en", player=PLAYER, **extra):
    return campus.command(dict(operation=operation, language=language, player=player, **extra))


def play(*actions, language="en", player=PLAYER):
    result = call("open", language, player)
    for action in actions:
        result = call("play", language, player, action=action)
        assert result["accepted"], action
    return result


# ---------- the data ----------

def node_shape(nodes, node):
    line = nodes[node]
    return ([(o["next"], o.get("if")) for o in line["options"]], line.get("trust"), bool(line.get("note")))


def test_both_languages_have_the_same_dialogue_structure():
    assert people.PEOPLE["en"].keys() == people.PEOPLE["pt"].keys() == people.ROOM_OF_PERSON.keys()
    for person in people.ROOM_OF_PERSON:
        en, pt = people.PEOPLE["en"][person]["nodes"], people.PEOPLE["pt"][person]["nodes"]
        assert en.keys() == pt.keys()
        for node in en:
            assert node_shape(en, node) == node_shape(pt, node), (person, node)


def test_every_conversation_can_start_end_and_has_no_dead_links():
    for language in ("en", "pt"):
        for person, data in people.PEOPLE[language].items():
            nodes = data["nodes"]
            assert "start" in nodes
            for line in nodes.values():
                assert line["options"], (person, "every line offers an answer")
                for option in line["options"]:
                    assert option["next"] is None or option["next"] in nodes
            assert any(o["next"] is None for line in nodes.values() for o in line["options"])


# ---------- talking ----------

def test_each_room_shows_its_people_and_only_theirs():
    assert [p["id"] for p in play(player="a")["people"]] == ["rita"]
    assert [p["id"] for p in play("go_print_shop", player="b")["people"]] == ["amelia"]
    assert [p["id"] for p in play("go_print_shop", "go_study_room", "go_library", player="c")["people"]] == ["leonor"]
    assert [p["id"] for p in play("go_computer_lab", player="d")["people"]] == ["tomas"]


def test_talking_offers_answers_and_writes_nothing():
    play()
    before = db.DB_PATH.read_bytes()
    reply = call("talk", npc="rita", node="start")
    assert reply["name"] == "Rita" and reply["text"] and len(reply["options"]) >= 2
    assert db.DB_PATH.read_bytes() == before


def test_you_can_only_talk_to_people_in_the_saved_room():
    play()
    for person in ("tomas", "leonor", "amelia", "professor", "duarte"):
        with pytest.raises(ValueError):
            call("talk", npc=person, node="start")


def test_unknown_person_node_and_extra_fields_are_rejected():
    play()
    before = db.DB_PATH.read_bytes()
    for bad in (dict(npc="nobody", node="start"), dict(npc="rita", node="nope"), dict(npc=7, node="start"),
                dict(npc="rita", node=["start"]), dict(npc="rita", node="start", extra="x")):
        with pytest.raises(ValueError):
            call("talk", **bad)
    assert db.DB_PATH.read_bytes() == before


def test_talking_needs_a_game_and_is_closed_after_an_ending():
    with pytest.raises(ValueError):
        call("talk", npc="rita", node="start")           # no saved game yet
    play("open_drawer", "go_print_shop", "request_copy", "go_study_room", "go_library", "ask_for_help", "go_study_room",
         "go_computer_lab", "view_files", "go_study_room", "go_auditorium", "present_evidence")
    with pytest.raises(ValueError):
        call("talk", npc="duarte", node="start")


def test_an_answer_is_offered_only_when_the_player_has_earned_it():
    play("go_computer_lab")
    start = call("talk", npc="tomas", node="start")
    assert "photo" not in [o["next"] for o in start["options"]]           # no original photo yet
    with pytest.raises(ValueError):                                       # and the line cannot be asked for directly
        call("talk", npc="tomas", node="photo")
    kind = call("talk", npc="tomas", node="kind")
    assert "msg5" not in [o["next"] for o in kind["options"]]             # the old files are not viewed yet
    with pytest.raises(ValueError):
        call("talk", npc="tomas", node="msg5")


def test_the_right_items_unlock_more_answers():
    play("open_drawer", "go_print_shop", "request_copy", "go_study_room", "go_computer_lab", "view_files")
    assert "photo" in [o["next"] for o in call("talk", npc="tomas", node="start")["options"]]
    assert "msg5" in [o["next"] for o in call("talk", npc="tomas", node="kind")["options"]]
    assert call("talk", npc="tomas", node="msg5")["note"]


def test_pressing_a_person_too_hard_ends_the_conversation():
    play("go_computer_lab")
    assert call("talk", npc="tomas", node="start")["trust"] == 2
    assert call("talk", npc="tomas", node="hard")["trust"] == 1
    closed = call("talk", npc="tomas", node="closed")
    assert closed["trust"] == 0 and [o["next"] for o in closed["options"]] == [None]


def test_a_kind_answer_keeps_the_trust_up():
    play("go_computer_lab")
    assert call("talk", npc="tomas", node="kind")["trust"] == 3


def test_dialogue_never_names_which_chat_messages_are_fake():
    for language in ("en", "pt"):
        for data in people.PEOPLE[language].values():
            for line in data["nodes"].values():
                text = (line["text"] + " " + line.get("note", "")).lower()
                assert not any(phrase in text for phrase in ("message 2", "message 4", "mensagem 2", "mensagem 4"))


def test_leonor_leaves_after_being_accused():
    play("open_drawer", "go_print_shop", "request_copy", "go_study_room", "go_library", "accuse")
    assert call("open")["people"] == []


def test_people_texts_follow_the_saved_language():
    play(language="pt")
    reply = call("talk", "en", npc="rita", node="start")   # the saved language wins, like everywhere else
    assert reply["text"] == people.PEOPLE["pt"]["rita"]["nodes"]["start"]["text"]


# ---------- the clock, the chat and moving between rooms ----------

def test_the_clock_follows_progress():
    assert play(player="a")["clock"] == "22:15"
    assert play("open_drawer", player="b")["clock"] == "22:55"
    assert play("open_drawer", "go_computer_lab", "view_files", player="c")["clock"] == "23:35"


def test_the_clock_wraps_past_midnight():
    result = play("open_drawer", "go_print_shop", "request_copy", "go_study_room", "go_library", "ask_for_help",
                  "go_study_room", "go_computer_lab", "view_files")
    assert result["clock"] == "00:55"


def test_chat_flags_reach_the_diary_without_saying_which_are_fake():
    result = play("open_drawer", "go_computer_lab", "view_files", "open_chat", "flag_1", "flag_2")
    chat_title = STORIES["en"]["scenes"]["group_chat"]["title"]
    chat_notes = [n for n in result["notebook"] if n["title"].startswith(chat_title)]
    assert [n["title"][-1] for n in chat_notes] == ["1", "2"]
    assert "fake" not in " ".join(n["text"] for n in chat_notes).lower()
    assert result["room"] == "computer_lab" and result["clock"] == "23:45"


def test_walking_from_the_chat_to_another_room_follows_the_story_paths():
    play("open_drawer", "go_computer_lab", "view_files", "open_chat")
    result = call("enter", room="study_room")
    assert result["accepted"] and result["scene"] == "study_room"


def test_entering_the_lab_from_the_chat_changes_nothing():
    play("open_drawer", "go_computer_lab", "view_files", "open_chat")
    assert call("enter", room="computer_lab")["scene"] == "group_chat"


def test_walking_to_the_auditorium_from_the_chat_is_still_gated_by_the_clues():
    play("open_drawer", "go_computer_lab", "view_files", "open_chat")
    result = call("enter", room="auditorium")
    # The walk stops at the first refusal, as for every other room: it got as far as the study room.
    assert not result["accepted"] and result["scene"] == "study_room"
    assert result["message"] == campus.missing_clues_note(game.load(PLAYER), "en")   # it explains what is missing
    assert game.load(PLAYER)["scene"] == "study_room" and game.load(PLAYER)["ending"] == "none"


def test_enter_only_accepts_the_five_rooms():
    play()
    with pytest.raises(ValueError):
        call("enter", room="group_chat")


# ---------- things done by talking (specs/campus-people-and-atmosphere.md, "Interface update") ----------

def offered(person, player):
    """The story actions this person offers inside the conversation, by id."""
    return {a["id"]: a for a in call("talk", player=player, npc=person, node="start")["actions"]}


def test_every_person_action_exists_in_the_story_and_belongs_to_the_room_of_that_person():
    for action, person in people.ACTION_PERSON.items():
        scenes = [s for s, data in STORIES["en"]["scenes"].items() if action in data["actions"]]
        assert scenes, action
        assert any(people.room_of_scene(scene) == people.ROOM_OF_PERSON[person] for scene in scenes), action


def test_each_person_offers_the_actions_of_their_room_inside_the_conversation():
    play(player="a")
    assert list(offered("rita", "a")) == ["open_drawer"] and offered("rita", "a")["open_drawer"]["allowed"]
    call("play", player="a", action="go_print_shop")
    assert list(offered("amelia", "a")) == ["request_copy"]
    # the library: with the photo the decision can be taken, and it is marked as a decision
    call("play", player="a", action="request_copy")
    call("play", player="a", action="go_study_room")
    call("play", player="a", action="go_library")
    leonor = offered("leonor", "a")
    assert set(leonor) == {"ask_for_help", "accuse"} and all(x["allowed"] and x["decision"] for x in leonor.values())


def test_blocked_actions_are_still_offered_with_their_reason_and_change_nothing():
    play("go_library", player="b")
    leonor = offered("leonor", "b")
    assert not leonor["ask_for_help"]["allowed"] and leonor["ask_for_help"]["blocked_text"]
    before = db.DB_PATH.read_bytes()
    result = call("play", player="b", action="ask_for_help")
    assert not result["accepted"] and result["message"] == leonor["ask_for_help"]["blocked_text"]
    assert db.DB_PATH.read_bytes() == before


def test_computer_lab_actions_unlock_in_order_and_the_chat_comes_after_the_files():
    play("go_computer_lab", player="c")
    lab = offered("tomas", "c")
    assert set(lab) == {"view_files"} and not lab["view_files"]["allowed"]
    play("open_drawer", "go_computer_lab", "view_files", player="d")
    assert "open_chat" in offered("tomas", "d")


def test_the_professor_offers_the_final_presentation():
    play("open_drawer", "go_print_shop", "request_copy", "go_study_room", "go_library", "ask_for_help",
         "go_study_room", "go_computer_lab", "view_files", "go_study_room", "go_auditorium", player="e")
    assert list(offered("professor", "e")) == ["present_evidence"]


def test_the_snapshot_says_who_offers_each_action_and_the_chat_flags_have_nobody():
    state = play("open_drawer", "go_computer_lab", "view_files", "open_chat", player="f")
    by_id = {a["id"]: a for a in state["actions"]}
    assert by_id["flag_1"]["person"] is None and by_id["go_computer_lab"]["person"] is None
    assert {a["id"]: a["person"] for a in play(player="g")["actions"]}["open_drawer"] == "rita"
