"""The security cameras in the list of clues (specs/camera-clue.md)."""

import importlib
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
FOLDER = REPO / "prototypes" / "campus-3d"
sys.path.insert(0, str(FOLDER))
TEXT = importlib.import_module("campus_text").TEXT
PLAY = (FOLDER / "play.js").read_text(encoding="utf-8")


def test_the_clue_texts_exist_in_both_languages():
    for language in ("pt", "en"):
        security = TEXT[language]["security"]
        # Changed by specs/clues-without-answers.md ("Reviewed tests that change"): the clue says what to find,
        # not the answer, so it no longer gives the minute. Was: "23:47" in the label.
        assert "23:47" not in security["clue_label"] and security["clue_label"].strip(), language
        assert security["clue_room"].strip(), language


def test_the_cameras_come_after_the_photo_and_are_done_with_the_footage():
    assert 'const after = clues.findIndex(clue => clue.id === "original_photo");' in PLAY
    assert "return [...clues.slice(0, after + 1), cameras, ...clues.slice(after + 1)];" in PLAY
    assert "done: loadSecurity().footage" in PLAY


def test_the_phone_the_start_card_and_the_share_card_use_it():
    assert "const clues = phoneClues();   // with the security cameras" in PLAY   # the phone's count
    assert "for (const clue of phoneClues()) {" in PLAY                           # the phone's list
    assert '$("clues-order").replaceChildren(...phoneClues().map(' in PLAY        # the start card
    assert "clues = phoneClues(), done = clues.filter(c => c.done).length;" in PLAY   # the share text
