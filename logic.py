"""Plot Twist — the rules of the game (no screens, no database, no story file).

The story is passed in as an argument, so these functions work with any story
shaped like the ones in story.py (see specs/base-game.md, sections 2 and 3).

The game state is a dictionary with four keys: "scene", "inventory", "flags" and
"ending". The rules never change the state or the story they are given: they build
a new state and return it.
"""

import copy


def _same(a, b):
    """True when a and b are equal and of the same type (so True is not equal to 1)."""
    return type(a) is type(b) and a == b


def _condition_met(condition, state):
    """True when the state satisfies the condition. An empty condition is always true.

    A condition can have "has" (items that must be held), "lacks" (items that must
    not be held) and "flags" (values the flags must have).
    """
    for item in condition.get("has", []):
        if item not in state["inventory"]:
            return False
    for item in condition.get("lacks", []):
        if item in state["inventory"]:
            return False
    for flag, value in condition.get("flags", {}).items():
        if not _same(state["flags"][flag], value):
            return False
    return True


def new_game(story: dict) -> dict:
    """A fresh game: a copy of the story's start, so two games never share a list."""
    return copy.deepcopy(story["start"])


def available_actions(story: dict, state: dict) -> list[dict]:
    """The actions the current scene offers, in story order.

    Each one is {"id", "label", "allowed"}. "allowed" is False when the action is
    shown but its requirement is not met yet. After an ending, nothing is offered.
    """
    if state["ending"] != "none":
        return []
    actions = []
    for action_id, action in story["scenes"][state["scene"]]["actions"].items():
        if _condition_met(action.get("offered_if", {}), state):
            actions.append({
                "id": action_id,
                "label": action["label"],
                "allowed": _condition_met(action.get("requires", {}), state),
            })
    return actions


def _reject(state, reason, message):
    """The answer for a rejected action: nothing changes, so the state comes back as it was."""
    return {"accepted": False, "reason": reason, "message": message, "state": copy.deepcopy(state)}


def apply_action(story: dict, state: dict, action_id) -> dict:
    """Try one action. Returns {"accepted", "reason", "message", "state"}.

    The checks run in this order and the first one that fails decides:
    game_over, not_here, not_offered, blocked. If all pass, the reason is "ok".
    """
    messages = story["messages"]
    if state["ending"] != "none":
        return _reject(state, "game_over", messages["game_over"])

    actions = story["scenes"][state["scene"]]["actions"]
    # Only text can be an action id; this also keeps a list or a dictionary from raising an error.
    if not isinstance(action_id, str) or action_id not in actions:
        return _reject(state, "not_here", messages["not_here"])

    action = actions[action_id]
    if not _condition_met(action.get("offered_if", {}), state):
        return _reject(state, "not_offered", messages["not_offered"])
    if not _condition_met(action.get("requires", {}), state):
        return _reject(state, "blocked", action["blocked_text"])

    new_state = copy.deepcopy(state)
    if "go_to" in action:
        new_state["scene"] = action["go_to"]
    if "gives" in action and action["gives"] not in new_state["inventory"]:
        new_state["inventory"].append(action["gives"])
    if "sets" in action:
        new_state["flags"].update(action["sets"])
    if action.get("ends_game"):
        # The first ending whose condition is true. The last one has an empty condition.
        for ending in story["endings"]:
            if _condition_met(ending["when"], new_state):
                new_state["ending"] = ending["id"]
                break
    return {"accepted": True, "reason": "ok", "message": action.get("result_text", ""), "state": new_state}


def scene_text(story: dict, state: dict) -> list[str]:
    """The paragraphs of the current scene: every text whose condition is true, in order."""
    scene = story["scenes"][state["scene"]]
    return [entry["text"] for entry in scene["texts"] if _condition_met(entry["when"], state)]


def _allowed_flag_values(story, flag):
    """The values a flag can have: its start value, plus every value an action sets it to."""
    values = [story["start"]["flags"][flag]]
    for scene in story["scenes"].values():
        for action in scene["actions"].values():
            if flag in action.get("sets", {}):
                values.append(action["sets"][flag])
    return values


def is_valid_state(story: dict, state) -> bool:
    """True only if the state fits the story. Used to check a saved game. Never raises an error."""
    if not isinstance(state, dict) or set(state) != {"scene", "inventory", "flags", "ending"}:
        return False

    scene = state["scene"]
    if not isinstance(scene, str) or scene not in story["scenes"]:
        return False

    inventory = state["inventory"]
    if not isinstance(inventory, list):
        return False
    for item in inventory:
        if not isinstance(item, str) or item not in story["items"]:
            return False
    if len(set(inventory)) != len(inventory):
        return False

    flags = state["flags"]
    if not isinstance(flags, dict) or set(flags) != set(story["start"]["flags"]):
        return False
    for flag, value in flags.items():
        if not any(_same(value, allowed) for allowed in _allowed_flag_values(story, flag)):
            return False

    ending = state["ending"]
    ending_ids = [e["id"] for e in story["endings"]]
    return isinstance(ending, str) and (ending == "none" or ending in ending_ids)
