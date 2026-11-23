"""The night and the clues (specs/night-and-clues.md)."""

import importlib
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
FOLDER = REPO / "prototypes" / "campus-3d"
sys.path.insert(0, str(FOLDER))
clock = importlib.import_module("campus_clock")
campus = importlib.import_module("campus_game")
TEXT = importlib.import_module("campus_text").TEXT
PLAY = (FOLDER / "play.js").read_text(encoding="utf-8")


def test_the_night_runs_from_half_past_ten_to_eleven():
    assert clock.time_text(0) == "22:30"
    assert clock.time_text(clock.NIGHT_MINUTES) == "23:00"
    assert "const NIGHT_STARTS = 22 * 60 + 30;" in PLAY
    assert "23:00" in TEXT["pt"]["brief_title"] and "22:30" in TEXT["pt"]["brief_text"]
    assert "23:00" in TEXT["en"]["brief_title"] and "22:30" in TEXT["en"]["brief_text"]


def test_finding_a_clue_costs_nothing_and_wrong_choices_still_do():
    for action in ("request_copy", "ask_for_help", "view_files"):
        assert clock.COSTS[action] == 0, action
    for wrong in ("accuse", "card_wrong", "caught"):
        assert clock.COSTS[wrong] > 0, wrong
    assert all(minutes > 0 for minutes in clock.PAGE_COSTS.values())


def test_the_print_shop_never_closes():
    assert clock.LEAVES == {"leonor": 15}
    state = {"flags": {"colleague_choice": "none"}, "inventory": []}
    assert "amelia" not in campus.gone_people(state, clock.NIGHT_MINUTES)
    assert not campus.clue_lost(state, "original_photo", clock.NIGHT_MINUTES)
    for language in ("pt", "en"):
        assert "warn_shop" not in TEXT[language]["schedule"]


def test_the_clues_are_in_the_order_they_are_done():
    assert [clue for clue, _room in campus.CLUES] == ["usb_stick", "original_photo", "leonor", "files_viewed"]
    for language in ("pt", "en"):
        t = TEXT[language]
        assert list(t["clues"]) == ["usb_stick", "original_photo", "leonor", "files_viewed"]
        for key in ("clues_notice_title", "clues_notice_intro", "clues_notice_end", "clues_notice_ok"):
            assert t[key].strip(), (language, key)


def test_the_clues_card_opens_at_the_start_and_after_a_new_game():
    assert 'id="clues-card"' in PLAY
    assert PLAY.count("showCluesNotice();") == 2   # campusStart and the confirmed restart
    assert '$("clues-card").hidden;   // reading the clues is free' in PLAY


def test_no_date_and_no_night_line_on_screen():
    assert "case-day" not in PLAY and "todayLabel" not in PLAY and "current.day.label" not in PLAY
    assert "t.night_lines[" not in PLAY
    assert "nightLine.hidden = true;" in PLAY


def test_flashlight_in_english():
    assert TEXT["en"]["torch_on"] == TEXT["en"]["torch_off"] == "Flashlight"
    assert TEXT["pt"]["torch_on"] == "Lanterna"
