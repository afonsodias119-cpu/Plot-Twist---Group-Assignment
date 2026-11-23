"""Conversation actions appear when they make sense: Leonor's decisions and the clerk's copy (specs/actions-when-they-make-sense.md)."""

import importlib
import sys
from pathlib import Path

FOLDER = Path(__file__).resolve().parents[1] / "prototypes" / "campus-3d"
sys.path.insert(0, str(FOLDER))
campus = importlib.import_module("campus_game")

# Changed by specs/three-proofs.md ("Reviewed tests that change"): no accusation.
DECISIONS = {"ask_for_help"}


def leonor_actions(*actions, player):
    """Walk the given story actions, then return what Leonor offers inside her conversation, by id."""
    call = lambda operation, **extra: campus.command(dict(operation=operation, language="en", player=player, **extra))
    call("open")
    for action in actions:
        assert call("play", action=action)["accepted"], action
    talk = call("talk", npc="leonor", node="start")
    return {a["id"]: a for a in talk["actions"]}


def test_without_the_photo_the_server_still_offers_the_decisions_but_not_allowed():
    leonor = leonor_actions("go_library", player="no_photo")
    assert set(leonor) == DECISIONS
    assert all(a["decision"] and not a["allowed"] and a["blocked_text"] for a in leonor.values())


def test_with_the_photo_the_decisions_are_allowed():
    leonor = leonor_actions("go_print_shop", "request_copy", "go_study_room", "go_library", player="with_photo")
    assert set(leonor) == DECISIONS
    assert all(a["decision"] and a["allowed"] for a in leonor.values())


def show_line():
    """The source of showLine in play.js: the function that draws one line of a conversation."""
    play_js = (FOLDER / "play.js").read_text(encoding="utf-8")
    return play_js[play_js.index("function showLine("):play_js.index("async function talkAction(")]


def test_the_conversation_skips_decisions_that_are_not_allowed():
    assert "if (action.decision && !action.allowed) continue;" in show_line()


def test_while_a_decision_can_be_taken_the_conversation_offers_no_answers():
    source = show_line()
    assert "const deciding = (line.actions || []).some(action => action.decision && action.allowed);" in source
    assert "const answers = deciding ? [] :" in source


def test_the_copy_appears_only_after_the_clerk_mentions_the_original_order():
    assert 'if (action.id === "request_copy" && !asked.has("order")) continue;' in show_line()


def test_conversation_actions_look_like_the_other_answers():
    source = show_line()
    assert 'make("button", isCode ? t.code_enter : action.label, "answer")' in source
    assert "▶" not in source and "t.decision" not in source
    assert "replaceChildren(...answers, ...(doing.children.length ? [doing] : []))" in source   # after the questions
