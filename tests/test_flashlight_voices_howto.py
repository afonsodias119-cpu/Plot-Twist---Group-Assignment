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


# ---------- only the spoken lines are read aloud ----------

import re

from story import STORIES

SPOKEN = re.compile(r'"([^"]+)"|«([^»]+)»|“([^”]+)”')   # the same rule as quotesOf in play.js


def test_every_ending_with_dialogue_says_who_speaks_each_line():
    for language in ("en", "pt"):
        voices = TEXT[language]["ending_voices"]
        known = {"rita", "amelia", "leonor", "tomas", "professor", "duarte", "narrator"}
        for ending in STORIES[language]["endings"]:
            lines = SPOKEN.findall(ending["text"])
            if lines:
                assert len(voices[ending["id"]]) == len(lines), (language, ending["id"])
                assert set(voices[ending["id"]]) <= known
            else:
                assert ending["id"] not in voices     # no dialogue: nothing to read aloud


def test_the_people_speak_in_every_conversation_start_and_the_description_is_not_read():
    people = importlib.import_module("campus_people")
    for language in ("en", "pt"):
        for person, data in people.PEOPLE[language].items():
            if person in people.OBJECTS:
                continue
            start = data["nodes"]["start"]["text"]
            lines = ["".join(g) for g in SPOKEN.findall(start)]
            assert lines, (language, person)
            assert all(line.strip() for line in lines)
            # what is read is what is between the quotation marks, never the sentence that describes the person
            assert not any(("looks up" in line or "levanta os olhos" in line) for line in lines)


def test_the_page_picks_natural_voices_and_reads_only_quotes():
    page = page3d.build_page(playable=True, inline=True)
    for needle in ("quotesOf", "pickVoice", "speakEnding", "voiceQuality", "natural|online"):
        assert needle in page
