"""The torch, the voices and the "How it was made" window (specs/flashlight-voices-howto.md)."""

import importlib
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "prototypes" / "campus-3d"))
TEXT = importlib.import_module("campus_text").TEXT
page3d = importlib.import_module("page3d")


def test_how_it_was_made_is_the_same_in_both_languages_and_names_files_that_exist():
    pt, en = TEXT["pt"]["howto_items"], TEXT["en"]["howto_items"]
    assert len(pt) == len(en) >= 8
    assert [item[1] for item in pt] == [item[1] for item in en]
    for title, file, detail in pt + en:
        assert title.strip() and detail.strip()
        assert (REPO / file).exists(), file


def test_how_it_was_made_covers_the_main_parts_of_the_game():
    files = {item[1] for item in TEXT["en"]["howto_items"]}
    assert {"story.py", "logic.py", "db.py", "game.py", "app_3d.py", "tests/", "specs/"} <= files


def test_the_page_has_the_torch_the_voices_and_the_how_it_was_made_window():
    page = page3d.build_page(playable=True, inline=True)
    for needle in ('id="howto-open"', 'id="torch-toggle"', 'id="voice-toggle"', "SpeechSynthesisUtterance", "plot-twist-torch",
                   "plot-twist-voice", "campusTorchOn", "SpotLight(0xfff0d2", "openHowto"):
        assert needle in page


def test_every_person_who_talks_has_a_voice_and_computer_12_has_none():
    page = page3d.build_page(playable=True, inline=True)
    people = importlib.import_module("campus_people")
    voices_line = next(line for line in page.splitlines() if "const VOICES" in line or "rita: [" in line)
    block = page[page.index("const VOICES"):page.index("function stopSpeaking")]
    for person in people.ROOM_OF_PERSON:
        assert (f"{person}:" in block) == (person not in people.OBJECTS), person
    assert voices_line
