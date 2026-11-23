"""'Show evidence' in the hearing (specs/hearing-show-evidence.md)."""

from pathlib import Path

PLAY_JS = (Path(__file__).resolve().parents[1] / "prototypes" / "campus-3d" / "play.js").read_text(encoding="utf-8")


def hearing_card():
    start = PLAY_JS.index("  function showHearing(hearing) {")
    return PLAY_JS[start:PLAY_JS.index("  function speakHeard(", start)]


def test_the_claim_is_answered_with_show_evidence_or_say_nothing():
    code = hearing_card()
    assert 'make("button", t.evidence_show, "answer evidence-show")' in code
    assert "replaceChildren(step, how, doubt, show, silent)" in code


def test_the_tray_shows_the_proofs_held_or_says_there_are_none_and_goes_back():
    code = hearing_card()
    assert "t.evidence_title" in code and "t.evidence_empty" in code and "t.evidence_back" in code
    assert "answerHearing(card.id)" in code            # a proof still answers the claim
    assert "showHearing(current.hearing)" in code      # "Put it away" goes back to the claim
