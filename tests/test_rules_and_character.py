"""The menu (Rules, Torch, Sound) and the character creator (specs/rules-and-character.md)."""

import importlib
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "prototypes" / "campus-3d"))
TEXT = importlib.import_module("campus_text").TEXT
page3d = importlib.import_module("page3d")
PAGE = page3d.build_page(playable=True, inline=True)


# ---------- the menu ----------

def test_the_menu_items_are_one_word_and_there_is_no_separate_voices_button():
    for language in ("pt", "en"):
        t = TEXT[language]
        assert t["howto_open"] in ("Regras", "Rules")
        assert t["torch_on"] == t["torch_off"] and "(" not in t["torch_on"] and " " not in t["torch_on"]
        assert t["sound_on"] == t["sound_off"] and " " not in t["sound_on"]
        assert "voice_on" not in t and "voice_off" not in t
    assert 'id="voice-toggle"' not in PAGE and "plot-twist-voice" not in PAGE


def test_the_voices_follow_the_sound_button():
    assert "sound.isMuted()" in PAGE and "voiceOn" not in PAGE
    assert re.search(r'sound-toggle"\)\.addEventListener\("click", \(\) => \{ sound\.toggle\(\); if \(sound\.isMuted\(\)\) stopSpeaking\(\)', PAGE)


def test_the_rules_are_the_same_in_both_languages_and_say_how_to_play():
    pt, en = TEXT["pt"]["rules_items"], TEXT["en"]["rules_items"]
    assert len(pt) == len(en) >= 8
    for title, file, detail in pt + en:
        assert title.strip() and detail.strip() and file == ""
    everything = " ".join(item[2] for item in en)
    for word in ("K", "F key", "30 minutes", "phone", "auditorium", "secret"):
        assert word in everything, word


def test_the_rules_do_not_give_away_the_puzzles():
    text = " ".join(item[2] for language in ("pt", "en") for item in TEXT[language]["rules_items"]).lower()
    for secret in ("1411", "14 november", "14 de novembro", "pen", "usb", "mesa", "table", "mochila"):
        assert secret not in text.split(), secret


def test_how_it_was_made_is_still_in_the_window_for_the_teachers():
    assert 'class="howto-dev"' in PAGE and "howto_items" in PAGE
    assert TEXT["pt"]["rules_dev"] and TEXT["en"]["rules_dev"]
    assert TEXT["pt"]["howto_items"][0][1] == TEXT["en"]["howto_items"][0][1]


# ---------- the character creator ----------

def test_the_creator_texts_exist_in_both_languages_with_the_same_shape():
    pt, en = TEXT["pt"], TEXT["en"]
    assert set(pt["outfits"]) == set(en["outfits"]) == {"tee", "jacket", "hoodie", "suit", "trench", "dress"}
    for key, size in (("color_names", 8), ("hair_names", 5), ("skin_names", 4)):
        assert len(pt[key]) == len(en[key]) == size
        assert len(set(pt[key])) == size
    for key in ("creator_title", "creator_body", "body_m", "body_f", "creator_outfit", "creator_color", "creator_hair",
                "creator_skin", "creator_hat", "hat_on", "hat_off", "creator_random"):
        assert pt[key].strip() and en[key].strip(), key


def test_the_palettes_in_the_screen_match_the_texts():
    colors = re.search(r"OUTFIT_COLORS = \[(.*?)\]", PAGE).group(1).count('"#')
    hair = re.search(r"HAIR_COLORS = \[(.*?)\]", PAGE).group(1).count('"#')
    skin = re.search(r"SKIN_COLORS = \[(.*?)\]", PAGE).group(1).count('"#')
    assert (colors, hair, skin) == (len(TEXT["en"]["color_names"]), len(TEXT["en"]["hair_names"]), len(TEXT["en"]["skin_names"]))


def test_the_page_has_the_creator_its_preview_and_the_new_clothes():
    for needle in ("cleanLook", "campusSetLook", "campusPreview", "plot-twist-look", "playerLook", "shortSleeves", "o.skirt",
                   "o.shirt", "o.tie", "let player = makePerson", "creator-preview"):
        assert needle in PAGE, needle


def test_what_is_read_from_the_browser_is_checked_before_it_is_used():
    clean = PAGE[PAGE.index("function cleanLook("):PAGE.index("function readLook(")]
    for guard in ("typeof raw !== \"object\"", "Number.isInteger(raw.color)", "OUTFITS.includes(raw.outfit)", "typeof raw.hat === \"boolean\"",
                  'clean.outfit === "dress" && clean.body !== "f"'):
        assert guard in clean, guard
    assert "catch (error) { return { ...DEFAULT_LOOK }; }" in PAGE      # unreadable notes give the default look


def test_the_look_never_goes_to_the_server():
    send = PAGE[PAGE.index("async function send("):PAGE.index("async function send(") + 900]
    assert "look" not in send.lower().replace("block", "")
    campus_game = (REPO / "prototypes" / "campus-3d" / "campus_game.py").read_text(encoding="utf-8")
    assert "look" not in campus_game.lower().replace("block", "").replace("outlook", "")
