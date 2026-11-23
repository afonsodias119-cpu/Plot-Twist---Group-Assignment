"""José first hears why you came (specs/guard-explain-first.md)."""

import importlib
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
FOLDER = REPO / "prototypes" / "campus-3d"
sys.path.insert(0, str(FOLDER))
TEXT = importlib.import_module("campus_text").TEXT
PLAY = (FOLDER / "play.js").read_text(encoding="utf-8")


def body(name):
    """The source of one function of play.js, up to the next function."""
    start = PLAY.index(f"function {name}(")
    return PLAY[start:PLAY.index("\n  function ", start + 1)]


def test_the_first_menu_offers_only_explain_the_situation():
    menu = body("guardMenu")
    assert 'if (!asked.has("explain")) return [{ label: t.opt_explain, next: "explain" }];' in menu
    assert "opt_broken" not in menu   # never on the first line any more


def test_after_explaining_the_menu_offers_the_follow_ups():
    menu = body("guardMenu")
    assert menu.rstrip().endswith("return guardFollowUps(t);\n  }") or "return guardFollowUps(t);" in menu
    assert menu.index('if (!asked.has("explain"))') < menu.index("return guardFollowUps(t);")


def test_the_follow_ups_are_the_monitors_and_demanding_with_its_cost():
    follow = body("guardFollowUps")
    assert 'return [{ label: t.opt_broken, next: "broken" }, { label: t.opt_rude, next: "rude", cost: 2 }];' in follow


def test_explain_broken_and_rude_lines_offer_the_follow_ups():
    step = body("guardStep")
    assert 'const options = ["explain", "broken", "rude"].includes(node) ? guardFollowUps(t)' in step
    assert ': node === "granted" ? [{ label: t.opt_watch, next: "watch_lab" }] : [];' in step   # unchanged


def test_the_menus_once_he_is_convinced_do_not_change():
    menu = body("guardMenu")
    assert 'if (state.footage) return [{ label: t.opt_rewatch, next: "watch" }];' in menu
    assert 'if (state.wired) return [{ label: t.opt_ask_lab, next: "granted" }];' in menu
    assert 'if (state.convinced) return [{ label: t.opt_wire, next: "wire" }, { label: t.opt_who, next: "who" }];' in menu
    assert menu.index("state.convinced") < menu.index('asked.has("explain")')


def test_show_evidence_still_waits_for_explain():
    assert 'const guardWaits = line.npc === "guard" && line.node !== "explain" && !asked.has("explain");' in PLAY


def test_the_monitors_answer_says_he_still_needs_a_proof():
    assert TEXT["en"]["security"]["broken"] == (
        "\"The monitors have had no signal since last night. Somebody unplugged the cables behind the rack, "
        "and it was not me. And I still need to see a proof before I let you near them.\"")
    assert TEXT["pt"]["security"]["broken"] == (
        "\"Desde ontem à noite que os monitores estão sem sinal. Alguém desligou os cabos atrás do rack, "
        "e não fui eu. E continuo a precisar de ver uma prova antes de te deixar chegar perto deles.\"")
    assert "why you want footage" not in TEXT["en"]["security"]["broken"]
    assert "porque queres imagens" not in TEXT["pt"]["security"]["broken"]
