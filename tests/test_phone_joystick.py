"""Phone controls: an on-screen joystick on touch screens, and touch buttons for the keys
(specs/phone-joystick.md).

Written before the code: one test for every line under "Checks" in the spec, in the same order.

How to read this file:
- The joystick is page code, so these tests read the source of game3d.html, play.js and play.css.
  Whether a finger really walks is the browser check of the spec (the mobile preset).
- The CSS of the stick can live in play.css or in the <style> of game3d.html (the spec allows both):
  `CSS` is the two together.
- `blocks(css)` reads a stylesheet as its top-level pieces: (header, body) for each `@media ... { }`
  and (selector, rule) for each plain rule, by counting braces.
- The texts are copied word for word from design-notes/texts-ideas.md, part G.
- `test_the_keyboard_lines_are_untouched` is a guard: it passes before the code and must still pass after it.
"""

import importlib
import re
import sys
from pathlib import Path

FOLDER = Path(__file__).resolve().parents[1] / "prototypes" / "campus-3d"
sys.path.insert(0, str(FOLDER))
page3d = importlib.import_module("page3d")
TEXT = importlib.import_module("campus_text").TEXT

GAME_HTML = (FOLDER / "game3d.html").read_text(encoding="utf-8")
PLAY_JS = (FOLDER / "play.js").read_text(encoding="utf-8")
PLAY_CSS = (FOLDER / "play.css").read_text(encoding="utf-8")
GAME_CSS = GAME_HTML[GAME_HTML.index("<style>") + len("<style>"):GAME_HTML.index("</style>")]
CSS = PLAY_CSS + "\n" + GAME_CSS

COARSE = '"(pointer: coarse)"'
# The three keyboard lines of section 8 of game3d.html, exactly as they are before this spec.
KEYBOARD = (
    'const KEYMAP = { ArrowUp: "up", KeyW: "up", ArrowDown: "down", KeyS: "down", ArrowLeft: "left", KeyA: "left", ArrowRight: "right", KeyD: "right" };\n'
    'window.addEventListener("keydown", e => { if (KEYMAP[e.code] && window.playing && !window.campusBusy && !window.campusState?.ending && !e.target.closest("input, button, dialog, textarea")) { keys[KEYMAP[e.code]] = true; e.preventDefault(); } });\n'
    'window.addEventListener("keyup", e => { if (KEYMAP[e.code]) keys[KEYMAP[e.code]] = false; });'
)
# Part G: the texts of campus_text.py and page3d.EXTRA.
TOUCH_TEXT = {
    "en": {"tap_talk": "Talk to {name}", "tap_use": "Use {name}", "tap_look": "Look: {name}",
           "controls_touch": "Walk with the circle at the bottom left of the picture: walking through a room's door takes you in (or use the buttons).",
           "rules_touch": "On a phone: drag the circle at the bottom left to walk, and tap the note that appears near a person or an object to talk to them or use it."},
    "pt": {"tap_talk": "Falar com {name}", "tap_use": "Usar: {name}", "tap_look": "Ver: {name}",
           "controls_touch": "Anda com o círculo no canto inferior esquerdo da imagem: ao atravessares a porta de uma sala, entras nela (ou os botões levam-te lá).",
           "rules_touch": "No telemóvel: arrasta o círculo no canto inferior esquerdo para andar, e toca na nota que aparece perto de uma pessoa ou de um objeto para falar ou usar."},
}
HELP_TOUCH = {"en": "Drag the circle to move", "pt": "Arrasta o círculo para andar"}


# ---------- helpers: reading the sources ----------

def body(source, name, indent=0):
    """One function of `source`, from `function name(` to its closing brace at `indent` spaces."""
    start = source.index(f"function {name}(")
    return source[start:source.index("\n" + " " * indent + "}\n", start)]


def blocks(css):
    """The top-level pieces of a stylesheet: (header, body) for every `@media` and every rule."""
    found, depth, start = [], 0, 0
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)   # comments are not rules
    for i, char in enumerate(css):
        if char == "{":
            if depth == 0:
                header, opened = css[start:i].strip(), i
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                found.append((header, css[opened + 1:i]))
                start = i + 1
    return found


def rules(css):
    """Every plain rule of a stylesheet as (selector, declarations, media header or "")."""
    found = []
    for header, inside in blocks(css):
        if header.startswith("@media"):
            found += [(selector, rule, header) for selector, rule in blocks(inside)]
        else:
            found.append((header, inside, ""))
    return found


def z_index(selector_part):
    """The z-index of the first rule whose selector contains `selector_part`."""
    rule = next(rule for selector, rule, _media in rules(CSS) if selector_part in selector and "z-index" in rule)
    return int(re.search(r"z-index:\s*(\d+)", rule).group(1))


# ---------- Checks ----------

def test_touch_is_detected_by_the_pointer():
    assert f"const TOUCH = window.matchMedia({COARSE}).matches;" in GAME_HTML
    calls = [match.start() for match in re.finditer(r"(?<!function )makeStick\(\)", GAME_HTML)]   # not its definition
    assert calls, "makeStick() is never called"
    for start in calls:   # every call is guarded
        assert GAME_HTML[start - len("if (TOUCH) "):start] == "if (TOUCH) ", GAME_HTML[start - 40:start + 12]
    # The stick is made only inside makeStick.
    stick = body(GAME_HTML, "makeStick")
    assert GAME_HTML.count('"stick"') == stick.count('"stick"') >= 1


def test_the_stick_presses_the_keyboards_keys():
    stick = body(GAME_HTML, "makeStick")
    for needle in ("keys.up", "keys.down", "keys.left", "keys.right", "setPointerCapture",
                   '"pointerup"', '"pointercancel"', "0.35", "0.25", "stick-knob"):
        assert needle in stick, needle
    assert "48" in GAME_HTML[GAME_HTML.index(KEYBOARD):GAME_HTML.index("function makeStick(") + len(stick)]   # the radius
    # The same rule as the keydown line: nothing is pressed while the game does not let the character walk.
    for needle in ("window.playing", "window.campusBusy", "window.campusState?.ending"):
        assert needle in stick, needle
    assert GAME_HTML.index(KEYBOARD) < GAME_HTML.index("function makeStick(")   # in section 8, after the keyboard


def test_the_keyboard_lines_are_untouched():
    assert KEYBOARD in GAME_HTML
    assert GAME_HTML.count("const KEYMAP =") == 1


def test_the_stick_never_scrolls_and_stays_under_the_cards():
    stick = [rule for selector, rule, _media in rules(CSS) if re.search(r"\.stick(?![-\w])", selector)]
    assert stick and any(re.search(r"touch-action:\s*none", rule) for rule in stick)
    assert z_index(".stick") < z_index(".talk-card")


def test_the_phone_layout_keeps_the_stick_free():
    phone = [inside for header, inside in blocks(PLAY_CSS) if header == "@media (pointer: coarse) and (max-width: 650px)"]
    assert phone, "no phone rules for touch screens"
    hud = [rule for selector, rule in blocks("\n".join(phone)) if ".hud-bottom" in selector]
    assert any("left: calc(50% + 60px)" in rule and "width: calc(100% - 144px)" in rule for rule in hud)


def test_the_near_note_says_what_a_tap_does():
    assert f"const TOUCH = window.matchMedia({COARSE}).matches;" in PLAY_JS
    near = body(PLAY_JS, "updateNear", 2)
    for needle in ("TOUCH", "tap_talk", "tap_use", "tap_look", "press_talk", "press_use", "press_look"):
        assert needle in near, needle
    # The tap words are chosen only when touch is detected, the K words otherwise.
    assert re.search(r"TOUCH \? [^:]*tap_", near)


def test_the_touch_texts_exist_in_both_languages():
    for language in ("en", "pt"):
        for key, text in TOUCH_TEXT[language].items():
            assert TEXT[language][key] == text, (language, key)
        for key in ("tap_talk", "tap_use", "tap_look"):
            assert "{name}" in TEXT[language][key]
        assert page3d.EXTRA[language]["help_touch"] == HELP_TOUCH[language]
        assert page3d.language_data(language)["ui"]["help_touch"] == HELP_TOUCH[language]
        for text in [*TOUCH_TEXT[language].values(), HELP_TOUCH[language]]:
            assert "WASD" not in text and not re.search(r"\bK\b", text), text
        assert "{name}" in TEXT[language]["press_talk"] and "K" in TEXT[language]["press_talk"]   # the keyboard's note stays


def test_desktop_rules_are_only_inside_the_coarse_media_query():
    found = [(selector, media) for selector, _rule, media in rules(CSS) if ".stick" in selector]
    assert found
    for selector, media in found:
        assert "(pointer: coarse)" in media, selector
    # The other touch rules too: the phone layout and the bigger near note.
    for selector, _rule, media in rules(PLAY_CSS):
        if "min-height: 48px" in _rule:
            assert "(pointer: coarse)" in media, selector
