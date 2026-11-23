"""The choice of device and the joystick, the detective card and the QR code (specs/touch-card-qr.md)."""

import importlib
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "prototypes" / "campus-3d"))
TEXT = importlib.import_module("campus_text").TEXT
page3d = importlib.import_module("page3d")
PAGE = page3d.build_page(playable=True, inline=True)
CSS = (REPO / "prototypes" / "campus-3d" / "play.css").read_text(encoding="utf-8")

KEYS = ["device_title", "device_computer", "device_phone", "device_hint_computer", "device_hint_phone", "joystick", "qr_open", "qr_title",
        "qr_intro", "qr_failed", "qr_close", "app_url", "card_open", "card_title", "card_download", "card_hint", "card_close", "card_case",
        "card_clues", "card_time", "card_name"]


def test_the_texts_exist_in_both_languages():
    for language in ("pt", "en"):
        for key in KEYS:
            assert TEXT[language][key].strip(), (language, key)
    assert TEXT["pt"]["app_url"] == TEXT["en"]["app_url"]


def test_the_qr_code_points_to_the_link_in_the_readme():
    readme = (REPO / "README.md").read_text(encoding="utf-8")
    assert TEXT["en"]["app_url"] in readme


# ---------- where the game is played, and the joystick ----------

def test_the_joystick_is_hidden_unless_the_player_chose_the_phone():
    assert re.search(r"\.joystick \{ display: none;", CSS)                      # hidden by default (on a computer)
    assert ".device-phone .joystick { display: block; }" in CSS                  # shown only in phone mode
    assert 'classList.toggle("device-phone", mode === "phone")' in PAGE


def test_a_touch_screen_pre_selects_the_phone_and_the_choice_is_remembered():
    assert 'matchMedia("(pointer: coarse)")' in PAGE and "plot-twist-device" in PAGE
    assert 'id="joystick"' in PAGE and "campusStick" in PAGE


def test_the_joystick_has_a_dead_zone_stops_when_released_and_the_3d_scene_reads_it():
    assert "length < 0.18" in PAGE                                   # a small dead zone in the middle
    assert 'stick.x' in PAGE and "window.campusStick" in PAGE
    assert re.search(r'function stickEnd\(event\) \{[^}]*campusStick = \{ x: 0, z: 0 \}', PAGE)


def test_a_phone_starts_with_the_panel_closed_and_the_menu_can_switch_the_joystick():
    assert 'if (deviceMode === "phone") setPanelHidden(true);' in PAGE
    assert 'id="joystick-toggle"' in PAGE and 'id="qr-open"' in PAGE


def test_the_rules_tell_phone_players_about_the_joystick():
    assert "joystick" in " ".join(item[2] for item in TEXT["pt"]["rules_items"]).lower()
    assert "joystick" in " ".join(item[2] for item in TEXT["en"]["rules_items"]).lower()


# ---------- the QR code ----------

def test_the_qr_library_is_a_pinned_version_from_the_same_cdn_family_as_the_other_scripts():
    assert "https://cdnjs.cloudflare.com/ajax/libs/qrcode-generator/1.4.4/qrcode.min.js" in PAGE


def test_the_qr_code_falls_back_to_the_address_if_the_library_cannot_load():
    assert 'catch (error) { $("qr-canvas").hidden = true; $("qr-failed").hidden = false; }' in PAGE
    assert 'id="qr-link"' in PAGE and "noopener" in PAGE


# ---------- the detective card ----------

def test_the_ending_screen_has_the_detective_card_button_and_the_page_can_draw_it():
    for needle in ('id="ending-card-btn"', "campusPortrait", "drawCard", "openCard", "toBlob", 'download = `plot-twist-'):
        assert needle in PAGE, needle


def test_the_card_is_built_in_the_browser_and_never_sent_anywhere():
    card = PAGE[PAGE.index("async function drawCard("):PAGE.index("async function openCard(")]
    assert "fetch(" not in card and "request(" not in card
    assert "readLook(lookKey(" in card                # the look comes from the browser, for this player
    assert "minutesSeconds(msLeft())" in card         # the time left, like the share card
