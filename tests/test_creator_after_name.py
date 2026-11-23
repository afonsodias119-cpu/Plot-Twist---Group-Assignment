"""The detective step after the name, no caption on the case file, and the panel names the place
(specs/creator-after-name.md)."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CAMPUS = ROOT / "prototypes" / "campus-3d"
sys.path[:0] = [str(ROOT), str(CAMPUS)]
import campus_text  # noqa: E402
import page3d  # noqa: E402

PLAY = (CAMPUS / "play.js").read_text(encoding="utf-8")
GAME = (CAMPUS / "game3d.html").read_text(encoding="utf-8")


def test_the_case_file_has_no_evidence_caption():
    for language in ("pt", "en"):
        assert "evidence" not in page3d.EXTRA[language]
    assert "evidenceCaption" not in GAME


def test_the_case_file_shows_the_name_of_the_game_not_a_case_number():
    for language in ("pt", "en"):
        assert "case" not in page3d.EXTRA[language]
    assert '$("caseNo").textContent = t.title;' in GAME
    assert '$("look-case").textContent = data[window.lang || "pt"].intro.title;' in PLAY


def test_the_new_texts_exist_in_both_languages():
    for language in ("pt", "en"):
        for key in ("next_step", "look_back", "name_needed", "brief_label", "brief_title", "brief_text", "brief_back"):
            assert campus_text.TEXT[language][key].strip()


def test_the_creator_is_its_own_step_after_the_case_file():
    assert 'stepLook.id = "stepLook"' in PLAY
    assert 'stepLook.querySelector(".look-body").append(creator)' in PLAY
    assert '$("stepCase").after(stepLook)' in PLAY
    assert "nameBox.append(creator)" not in PLAY


def test_the_case_file_button_and_enter_open_the_step_and_only_it_starts_the_game():
    assert "if (window.campusNext) { window.campusNext(); return; }" in GAME
    assert "window.campusNext = () => {" in PLAY
    assert "if (!name.value.trim()) { startError.textContent = ui().name_needed;" in PLAY
    assert "goStep(stepLook, stepBrief)" in PLAY
    assert '$("brief-start").addEventListener("click", () => window.campusStart())' in PLAY
    assert PLAY.count("window.campusStart()") == 2   # the warning's button, or the detective's when the warning was seen
    assert '$("accept").classList.contains("ready")) window.campusNext()' in PLAY


def test_outside_the_room_the_panel_names_the_place_and_hides_the_description():
    assert "window.campusHere = here;" in GAME
    assert '$("scene-heading").textContent = outside ? place : current.title;' in PLAY
    assert '$("scene-paragraphs").hidden = outside;' in PLAY


def test_the_warning_says_when_the_faculty_closes_and_includes_the_clues():
    briefing = PLAY.split("stepBrief.innerHTML = ", 1)[1].split("stepLook.after(stepBrief)", 1)[0]
    assert 'id="brief-title"' in briefing and 'id="brief-clues-order"' in briefing
    assert "stepLook.after(stepBrief)" in PLAY
    for language in ("pt", "en"):
        text = campus_text.TEXT[language]
        # Changed by specs/night-and-clues.md ("Reviewed tests that change"): the night runs from 22:30 to
        # 23:00. Was: "22:45" in the title and "22:15" in the text.
        assert "23:00" in text["brief_title"]
        assert "30" in text["brief_text"] and "22:30" in text["brief_text"]


def test_the_warning_is_only_shown_before_a_first_game():
    assert "if (briefSeen(name.value)) window.campusStart();" in PLAY
    assert "else goStep(stepLook, stepBrief);" in PLAY
    start = PLAY[PLAY.index("window.campusStart = async () => {"):]
    assert 'localStorage.setItem(briefKey(current.player), "yes")' in start[:start.index("};")]
