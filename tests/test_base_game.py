"""Acceptance checks for the base game (specs/base-game.md, section 7).

This file holds the Rules checks. The Saving checks are added to this file by the
saving part, and the Screens checks live in tests/test_smoke.py.

Each test name is one checklist line of the spec. Expected texts are read from the
story, never typed here. In these tests STORY means STORIES["en"].
"""

import copy
import json
from pathlib import Path

import logic
from story import STORIES, UI_TEXTS

STORY = STORIES["en"]

P_SHORT = ["open_drawer", "go_computer_lab", "view_files", "go_study_room", "go_auditorium", "present_evidence"]
P_HELP = [
    "open_drawer", "go_print_shop", "request_copy", "go_study_room", "go_library", "ask_for_help",
    "go_study_room", "go_computer_lab", "view_files", "go_study_room", "go_auditorium", "present_evidence",
]
P_ACCUSE = ["accuse" if action == "ask_for_help" else action for action in P_HELP]


# ---------- helpers ----------

def play_path(path, story=STORY, state=None):
    """Play every action of `path` from `state` (a new game if None); each must be accepted."""
    if state is None:
        state = logic.new_game(story)
    for action_id in path:
        result = logic.apply_action(story, state, action_id)
        assert result["accepted"], f"{action_id} was rejected: {result['reason']}"
        state = result["state"]
    return state


def assert_rejected(state, action_id, reason, story=STORY):
    """The action is rejected with `reason`, and the state is unchanged."""
    before = copy.deepcopy(state)
    result = logic.apply_action(story, state, action_id)
    assert result["accepted"] is False
    assert result["reason"] == reason
    assert result["state"] == before
    assert state == before
    return result


def offered_ids(state, story=STORY):
    return [action["id"] for action in logic.available_actions(story, state)]


def all_action_ids(story):
    return {action_id for scene in story["scenes"].values() for action_id in scene["actions"]}


def scene_actions(scene_id, story=STORY):
    return story["scenes"][scene_id]["actions"]


# ---------- Rules ----------

def test_new_game_is_the_opening_state():
    """A new game equals the story's start, and two new games share no list or dictionary."""
    first = logic.new_game(STORY)
    second = logic.new_game(STORY)
    assert first == STORY["start"]
    assert first["inventory"] is not second["inventory"]
    assert first["flags"] is not second["flags"]
    assert first["inventory"] is not STORY["start"]["inventory"]
    assert first["flags"] is not STORY["start"]["flags"]


def test_study_room_offers_its_five_actions():
    """The study room offers its five actions in story order; only the auditorium is not allowed."""
    actions = logic.available_actions(STORY, logic.new_game(STORY))
    assert [a["id"] for a in actions] == ["open_drawer", "go_print_shop", "go_library", "go_computer_lab", "go_auditorium"]
    assert [a["id"] for a in actions if not a["allowed"]] == ["go_auditorium"]
    for action in actions:
        assert action["label"] == scene_actions("study_room")[action["id"]]["label"]


def test_auditorium_is_blocked_until_files_are_viewed():
    """go_auditorium is blocked in a new game and still blocked holding only the USB stick."""
    expected = scene_actions("study_room")["go_auditorium"]["blocked_text"]
    result = assert_rejected(logic.new_game(STORY), "go_auditorium", "blocked")
    assert result["message"] == expected
    result = assert_rejected(play_path(["open_drawer"]), "go_auditorium", "blocked")
    assert result["message"] == expected


def test_item_actions_are_blocked_without_their_item():
    """view_files needs the USB stick; ask_for_help and accuse need the original photo."""
    with_photo_only = play_path(["go_print_shop", "request_copy", "go_study_room", "go_computer_lab"])
    assert with_photo_only["inventory"] == ["original_photo"]
    result = assert_rejected(with_photo_only, "view_files", "blocked")
    assert result["message"] == scene_actions("computer_lab")["view_files"]["blocked_text"]

    with_stick_and_files = play_path(P_SHORT[:4] + ["go_library"])
    assert with_stick_and_files["inventory"] == ["usb_stick"]
    assert with_stick_and_files["flags"]["files_viewed"] is True
    for action_id in ["ask_for_help", "accuse"]:
        result = assert_rejected(with_stick_and_files, action_id, "blocked")
        assert result["message"] == scene_actions("library")[action_id]["blocked_text"]


def test_usb_stick_opens_the_files_then_the_auditorium_and_is_kept():
    """Brief A2: the key is usb_stick, its lock files_viewed, its route the auditorium."""
    state = play_path(P_SHORT[:5])
    assert state["scene"] == "auditorium"
    assert state["flags"]["files_viewed"] is True
    assert state["inventory"] == ["usb_stick"]


def test_original_photo_allows_the_decision_and_is_kept():
    """After asking for help, the decision is remembered and the photo is still held."""
    state = play_path(P_HELP[:6])
    assert state["flags"]["colleague_choice"] == "help"
    assert "original_photo" in state["inventory"]


def test_collected_item_is_not_collected_again():
    """After leaving and coming back, a collected item is not offered and cannot be taken twice."""
    state = play_path(["open_drawer", "go_print_shop", "go_study_room"])
    assert "open_drawer" not in offered_ids(state)
    result = assert_rejected(state, "open_drawer", "not_offered")
    assert result["message"] == STORY["messages"]["not_offered"]
    assert state["inventory"] == ["usb_stick"]

    state = play_path(["go_print_shop", "request_copy", "go_study_room", "go_print_shop"])
    assert "request_copy" not in offered_ids(state)
    assert_rejected(state, "request_copy", "not_offered")
    assert state["inventory"] == ["original_photo"]


def test_actions_already_done_are_not_offered():
    """Viewing the files twice, or accusing after asking for help, is rejected as not_offered."""
    after_view = play_path(P_SHORT[:3])
    assert "view_files" not in offered_ids(after_view)
    assert_rejected(after_view, "view_files", "not_offered")

    after_help = play_path(P_HELP[:6])
    assert "accuse" not in offered_ids(after_help)
    assert_rejected(after_help, "accuse", "not_offered")


def test_action_of_another_scene_is_rejected():
    """request_copy is rejected in the study room and accepted in the print shop."""
    result = assert_rejected(logic.new_game(STORY), "request_copy", "not_here")
    assert result["message"] == STORY["messages"]["not_here"]
    in_print_shop = play_path(["go_print_shop"])
    assert logic.apply_action(STORY, in_print_shop, "request_copy")["accepted"] is True


def test_unknown_action_ids_are_rejected():
    """Unknown ids, an empty text, None and a number are all rejected as not_here."""
    for action_id in ["fly", "", None, 7]:
        result = assert_rejected(logic.new_game(STORY), action_id, "not_here")
        assert result["message"] == STORY["messages"]["not_here"]


def test_three_paths_reach_their_endings():
    """Asking for help ends in impostor; skipping Leonor or accusing her ends in stolen_credits."""
    assert play_path(P_HELP)["ending"] == "impostor"
    assert play_path(P_SHORT)["ending"] == "stolen_credits"
    assert play_path(P_ACCUSE)["ending"] == "stolen_credits"


def test_every_action_is_rejected_after_an_ending():
    """After either ending, every action of the story is rejected and none is offered."""
    for path in [P_HELP, P_SHORT]:
        finished = play_path(path)
        assert logic.available_actions(STORY, finished) == []
        for action_id in all_action_ids(STORY):
            result = assert_rejected(finished, action_id, "game_over")
            assert result["message"] == STORY["messages"]["game_over"]


def test_every_ending_is_reachable_from_a_new_game():
    """Trying every offered action from every reachable state finds exactly the two endings."""
    start = logic.new_game(STORY)
    seen = {json.dumps(start, sort_keys=True)}
    to_visit = [start]
    endings_found = set()
    while to_visit:
        state = to_visit.pop()
        if state["ending"] != "none":
            endings_found.add(state["ending"])
            continue
        for action in logic.available_actions(STORY, state):
            result = logic.apply_action(STORY, state, action["id"])
            if result["accepted"]:
                key = json.dumps(result["state"], sort_keys=True)
                if key not in seen:
                    seen.add(key)
                    to_visit.append(result["state"])
    assert endings_found == {"impostor", "stolen_credits"}


def test_playing_never_changes_the_story():
    """Playing both paths leaves the story exactly as it was."""
    before = copy.deepcopy(STORY)
    play_path(P_HELP)
    play_path(P_SHORT)
    assert STORY == before


def test_apply_action_never_changes_the_state_it_was_given():
    """At every step, accepted or rejected, the state passed in is not changed."""
    state = logic.new_game(STORY)
    for action_id in P_HELP:
        before = copy.deepcopy(state)
        result = logic.apply_action(STORY, state, action_id)
        assert state == before
        state = result["state"]

    new = logic.new_game(STORY)
    before = copy.deepcopy(new)
    logic.apply_action(STORY, new, "go_auditorium")
    assert new == before


def test_scene_text_follows_remembered_changes():
    """Scene texts change with what the game remembers (brief R3)."""
    library = STORY["scenes"]["library"]["texts"]
    before_decision = logic.scene_text(STORY, play_path(["go_library"]))
    after_help = logic.scene_text(STORY, play_path(P_HELP[:6]))
    after_accuse = logic.scene_text(STORY, play_path(P_ACCUSE[:6]))
    assert before_decision == [library[0]["text"]]
    assert after_help == [library[1]["text"]]
    assert after_accuse == [library[2]["text"]]
    assert len({before_decision[0], after_help[0], after_accuse[0]}) == 3

    lab = STORY["scenes"]["computer_lab"]["texts"]
    assert logic.scene_text(STORY, play_path(["go_computer_lab"])) == [lab[0]["text"]]
    assert logic.scene_text(STORY, play_path(P_SHORT[:3])) == [lab[0]["text"], lab[1]["text"]]

    study = STORY["scenes"]["study_room"]["texts"]
    assert logic.scene_text(STORY, logic.new_game(STORY)) == [study[0]["text"]]
    assert logic.scene_text(STORY, play_path(["open_drawer"])) == [study[0]["text"], study[1]["text"]]

    shop = STORY["scenes"]["print_shop"]["texts"]
    assert logic.scene_text(STORY, play_path(["go_print_shop"])) == [shop[0]["text"]]
    assert logic.scene_text(STORY, play_path(["go_print_shop", "request_copy"])) == [shop[0]["text"], shop[1]["text"]]


STRUCTURE_KEYS = ["go_to", "gives", "sets", "ends_game", "offered_if", "requires"]


def structure(story):
    """Everything in a story except the texts: ids, conditions and effects."""
    return {
        "start": story["start"],
        "items": sorted(story["items"]),
        "messages": sorted(story["messages"]),
        "scenes": {
            scene_id: {
                "texts": [entry["when"] for entry in scene["texts"]],
                "actions": [
                    (action_id, {key: action.get(key) for key in STRUCTURE_KEYS})
                    for action_id, action in scene["actions"].items()
                ],
            }
            for scene_id, scene in story["scenes"].items()
        },
        "endings": [(ending["id"], ending["when"]) for ending in story["endings"]],
    }


def all_texts(story):
    """Every text the player can read in a story."""
    texts = list(story["items"].values()) + list(story["messages"].values())
    for scene in story["scenes"].values():
        texts.append(scene["title"])
        texts += [entry["text"] for entry in scene["texts"]]
        for action in scene["actions"].values():
            texts.append(action["label"])
            texts += [action[key] for key in ["blocked_text", "result_text"] if key in action]
    for ending in story["endings"]:
        texts += [ending["title"], ending["text"]]
    return texts


def test_both_languages_have_the_same_structure():
    """English and Portuguese differ only in their texts; every text is filled in."""
    assert set(STORIES) == {"en", "pt"}
    assert structure(STORIES["en"]) == structure(STORIES["pt"])
    for story in STORIES.values():
        for text in all_texts(story):
            assert isinstance(text, str) and text.strip() != ""
    assert set(UI_TEXTS) == {"en", "pt"}
    assert set(UI_TEXTS["en"]) == set(UI_TEXTS["pt"])
    for ui in UI_TEXTS.values():
        for text in ui.values():
            assert isinstance(text, str) and text.strip() != ""


def test_paths_work_in_every_language():
    """The three paths reach the same endings in every language."""
    for story in STORIES.values():
        assert play_path(P_HELP, story)["ending"] == "impostor"
        assert play_path(P_SHORT, story)["ending"] == "stolen_credits"
        assert play_path(P_ACCUSE, story)["ending"] == "stolen_credits"


def conditions_of(story):
    """Every condition in a story: text conditions, action conditions and ending conditions."""
    found = []
    for scene in story["scenes"].values():
        found += [entry["when"] for entry in scene["texts"]]
        for action in scene["actions"].values():
            found += [action[key] for key in ["offered_if", "requires"] if key in action]
    found += [ending["when"] for ending in story["endings"]]
    return found


def test_story_meets_the_content_baseline():
    """Each story has the brief's minimum content and no broken references."""
    for story in STORIES.values():
        assert len(story["scenes"]) >= 5
        assert len(story["items"]) >= 2
        assert len(story["endings"]) >= 2
        flag_names = set(story["start"]["flags"])
        for condition in conditions_of(story):
            for item in condition.get("has", []) + condition.get("lacks", []):
                assert item in story["items"]
            for flag in condition.get("flags", {}):
                assert flag in flag_names
        for scene in story["scenes"].values():
            for action in scene["actions"].values():
                if "go_to" in action:
                    assert action["go_to"] in story["scenes"]
                if "gives" in action:
                    assert action["gives"] in story["items"]
                for flag in action.get("sets", {}):
                    assert flag in flag_names
                if "gives" in action or "sets" in action:
                    assert action.get("result_text", "").strip() != ""
                if "requires" in action:
                    assert action.get("blocked_text", "").strip() != ""
        assert story["endings"][-1]["when"] == {}


def test_is_valid_state_rejects_broken_saves():
    """A save that does not fit the story is rejected, without raising an error."""
    assert logic.is_valid_state(STORY, logic.new_game(STORY)) is True
    assert logic.is_valid_state(STORY, play_path(P_HELP)) is True

    def changed(**changes):
        state = logic.new_game(STORY)
        state.update(changes)
        return state

    def changed_flags(**changes):
        state = logic.new_game(STORY)
        state["flags"].update(changes)
        return state

    missing_flag = logic.new_game(STORY)
    del missing_flag["flags"]["files_viewed"]

    broken = [
        changed(scene="cafeteria"),
        changed(inventory=["usb_stick", "usb_stick"]),
        changed(inventory=[["usb_stick"]]),
        missing_flag,
        changed(flags=None),
        changed(flags=["colleague_choice", "files_viewed"]),
        changed_flags(files_viewed="yes"),
        changed_flags(colleague_choice="maybe"),
        changed(ending="x"),
        None,
    ]
    for state in broken:
        assert logic.is_valid_state(STORY, state) is False, state


def test_playing_never_changes_the_stories():
    """Playing both paths in both languages leaves every story exactly as it was."""
    before = copy.deepcopy(STORIES)
    for story in STORIES.values():
        play_path(P_HELP, story)
        play_path(P_SHORT, story)
    assert STORIES == before


def test_logic_imports_nothing_from_the_project():
    """logic.py imports no Streamlit, no database code and no project file."""
    forbidden = {"streamlit", "sqlite3", "db", "game", "story"}
    source = (Path(__file__).resolve().parent.parent / "logic.py").read_text(encoding="utf-8")
    for line in source.splitlines():
        words = line.replace(",", " ").replace(".", " ").split()
        if words and words[0] in ("import", "from"):
            assert not forbidden & set(words), line
