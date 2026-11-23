"""Leonor: one right answer, one wrong answer (specs/leonor-two-answers.md)."""

from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PLAY = (REPO / "prototypes" / "campus-3d" / "play.js").read_text(encoding="utf-8")


def test_leonor_shows_only_the_right_and_the_wrong_answer():
    assert 'const leonorDeciding = line.npc === "leonor" && (line.actions || []).some(action => action.id === "ask_for_help");' in PLAY
    assert 'actions: line.actions.filter(action => !action.decision)' in PLAY
    assert 'line.options.filter(option => ["soft", "harsh", "closed"].includes(option.next))' in PLAY


def test_the_evidence_button_waits_for_the_right_answer():
    assert 'const evidenceNow = showsEvidence && !(leonorDeciding && !asked.has("soft"));' in PLAY
    assert '$("talk-evidence").hidden = !evidenceNow;' in PLAY


def test_showing_the_original_photo_asks_her_for_help():
    assert 'if (line.npc === "leonor" && line.help && card.id === "original_photo") { talkAction(line, line.help); return; }' in PLAY


def test_the_server_dialogue_still_has_both_answers():
    source = (REPO / "prototypes" / "campus-3d" / "campus_people.py").read_text(encoding="utf-8")
    for node in ('"soft"', '"harsh"', '"closed"'):
        assert node in source
