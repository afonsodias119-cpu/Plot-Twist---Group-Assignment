"""Sounds that tell you things: footsteps, the shutter, a buzz for each message (specs/sounds-that-tell.md).

Written before the code: one test for every line under "Checks" in the spec, in the same order.

How to read this file:
- Sounds are page code, so these tests can only read the source of play.js, as
  tests/test_harder_campus.py does. Whether they really play is the browser check of the spec.
- `module()` is the `sound` module of play.js: from `const sound = (() => {` to its `})();`.
- `body(source, name, indent)` is one function of a source: from `function name(` to its closing
  brace, the first `}` alone on a line at the same indentation. The functions of the `sound` module
  are indented by 4 spaces, the other functions of play.js by 2.
- The spec names five new sounds: `thump`, `footsteps` and `noise`, and the shutter and the chair
  made with them. This file reads the last two as functions too (`function shutter(`,
  `function chair(`), so each of the five can be checked to start with the Sound button's guard.
- The last two tests are guards: they pass before the code and must still pass after it.
"""

import re
from pathlib import Path

FOLDER = Path(__file__).resolve().parents[1] / "prototypes" / "campus-3d"
PLAY_JS = (FOLDER / "play.js").read_text(encoding="utf-8")
PAGE3D = (FOLDER / "page3d.py").read_text(encoding="utf-8")
RULES_TEST = (Path(__file__).resolve().parent / "test_rules_and_character.py").read_text(encoding="utf-8")

NEW_SOUNDS = ("thump", "footsteps", "noise", "shutter", "chair")
GUARD = "if (!ctx || muted) return;"
# The body of sound.buzz today: the spec says it is kept and only called more often.
BUZZ = 'buzz() { tone(110, 0.13, "square", 0.07); setTimeout(() => tone(110, 0.13, "square", 0.07), 180); },'


# ---------- helpers: reading play.js ----------

def module():
    """The `sound` module of play.js: from its first line to its `})();`."""
    start = PLAY_JS.index("const sound = (() => {")
    return PLAY_JS[start:PLAY_JS.index("})();", start)]


def body(source, name, indent):
    """One function of `source`, from `function name(` to its closing brace at `indent` spaces."""
    start = source.index(f"function {name}(")
    return source[start:source.index("\n" + " " * indent + "}\n", start)]


def first_line(function):
    """The first line inside a function (the line after its signature)."""
    return function.split("\n")[1].strip()


def early_return(function):
    """The lines of a function up to its first `return;`: the cases in which it does nothing."""
    return function[:function.index("return;")]


# ---------- Checks ----------

def test_the_sound_module_has_the_new_sounds():
    sound = module()
    for needle in ("function thump(", "function footsteps(", "function noise(", "shutter", "chair"):
        assert needle in sound, needle


def test_every_new_sound_follows_the_sound_button():
    sound = module()
    for name in NEW_SOUNDS:
        assert first_line(body(sound, name, 4)) == GUARD, name
    # The steps already scheduled check the button again: turning the sound off stops them.
    steps = body(sound, "footsteps", 4)
    assert "setTimeout(" in steps
    assert "muted" in steps[steps.index("setTimeout("):]


def test_render_plays_cues_only_between_two_snapshots_of_one_night():
    cues = body(PLAY_JS, "soundCues", 2)
    assert "soundCues(before, state, operation)" in body(PLAY_JS, "render", 2)
    quiet = early_return(cues)
    for needle in ('"open"', '"begin"', '"restart"', "state.ending", "!before", "before.player !== state.player"):
        assert needle in quiet, needle


def test_the_cues_read_the_server_schedule():
    cues = body(PLAY_JS, "soundCues", 2)
    for needle in ("night.duarte", '"lab_door"', "night.gone", '"amelia"', '"leonor"'):
        assert needle in cues, needle


def test_one_buzz_for_each_new_message_at_most_three():
    notices = body(PLAY_JS, "checkNotices", 2)
    assert "Math.min(due.length, 3)" in notices
    assert "sound.buzz()" in notices
    assert BUZZ in module()   # the buzz itself keeps its body


def test_no_new_sound_file_and_no_new_script():
    for needle in (".mp3", ".wav", ".ogg", "new Audio("):
        assert needle not in PLAY_JS, needle
    # The inline page reads exactly these three files, and the served page links exactly these three.
    assert sorted(re.findall(r'\(HERE / "(\w+)\.js"\)', PAGE3D)) == ["photo", "play", "table"]
    assert sorted(re.findall(r'src="/(\w+)\.js"', PAGE3D)) == ["photo", "play", "table"]


def test_the_pinned_sound_lines_are_still_there():
    for needle in ("AudioContext", "sound.isMuted()", "campusMoving"):
        assert needle in PLAY_JS, needle
    # The same pattern tests/test_rules_and_character.py pins for the Sound button's handler.
    assert "sound-toggle" in RULES_TEST
    assert re.search(r'sound-toggle"\)\.addEventListener\("click", \(\) => \{ sound\.toggle\(\); if \(sound\.isMuted\(\)\) stopSpeaking\(\)', PLAY_JS)
