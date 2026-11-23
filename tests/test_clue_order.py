"""The order of the clues, and Leonor back in the list (specs/clue-order.md)."""

import importlib
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
FOLDER = REPO / "prototypes" / "campus-3d"
sys.path.insert(0, str(FOLDER))
TEXT = importlib.import_module("campus_text").TEXT
PLAY = (FOLDER / "play.js").read_text(encoding="utf-8")

LABELS = {
    "pt": ["Encontrar a fotografia original do grupo", "Encontrar a pen do grupo", "Falar com a Leonor e pedir a sua ajuda",
           "Encontrar as imagens da câmara de vigilância junto do segurança", "Ver o histórico dos ficheiros do grupo"],
    "en": ["Find the group's original photo", "Find the group's USB stick", "Talk to Leonor and ask for her help",
           "Find the surveillance camera footage with the security guard", "See the history of the group's files"],
}


def test_the_five_labels_in_both_languages():
    for language, labels in LABELS.items():
        t = TEXT[language]
        found = [t["clues"]["original_photo"], t["clues"]["usb_stick"], t["clue_leonor"],
                 t["security"]["clue_label"], t["clues"]["files_viewed"]]
        assert found == labels, language


def test_the_page_lists_them_in_this_order_and_leonor_is_done_when_she_follows():
    assert 'return [...server("original_photo"), ...server("usb_stick"), leonor, cameras, ...server("files_viewed")];' in PLAY
    assert 'done: (current.followers?.ids || []).includes("leonor")' in PLAY
