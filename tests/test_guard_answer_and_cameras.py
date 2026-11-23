"""José's question, and a camera in every room (specs/guard-answer-and-cameras.md)."""

import importlib
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
FOLDER = REPO / "prototypes" / "campus-3d"
sys.path.insert(0, str(FOLDER))
TEXT = importlib.import_module("campus_text").TEXT
PLAY = (FOLDER / "play.js").read_text(encoding="utf-8")
HTML = (FOLDER / "game3d.html").read_text(encoding="utf-8")


def test_the_answer_and_his_agreement_exist_in_both_languages():
    for language in ("pt", "en"):
        security = TEXT[language]["security"]
        assert "23:47" in security["opt_ask_lab"], language
        assert "23:47" in security["granted"], language
        assert "confirm" not in security and "opt_yes" not in security, language


def test_watching_after_his_agreement_opens_the_computer_lab_at_2347():
    assert 'if (node === "watch_lab") {' in PLAY
    assert 'cctvCamera = "computer_lab"; cctvMinute = 23 * 60 + 47;' in PLAY


def test_a_camera_in_every_room_and_by_the_entrance_with_a_blinking_light():
    cameras = re.findall(r"^securityCamera\(", HTML, re.M)
    assert len(cameras) == 6
    assert "cameraLed.emissiveIntensity = t % 1.2 < 0.25 ? 4 : 0.15;" in HTML
