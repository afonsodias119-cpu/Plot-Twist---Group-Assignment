"""No count of endings on the start screen (specs/no-endings-on-start.md)."""

from pathlib import Path

PLAY_JS = (Path(__file__).resolve().parents[1] / "prototypes" / "campus-3d" / "play.js").read_text(encoding="utf-8")


def test_the_name_box_has_no_line_about_the_endings():
    assert "nameBox.append(nameLabel, name, nameHint, startError);" in PLAY_JS
    assert '"muted collection"' not in PLAY_JS


def test_the_ending_screen_no_longer_shows_the_endings_found():
    # Changed by specs/no-endings-count.md ("Reviewed tests that change"): "Endings found: n/2" is gone from the ending
    # screen, the share text and the share card. Was: the ending screen still showed it.
    assert "ending-collection" not in PLAY_JS and "collectionText" not in PLAY_JS and "collectionCount" not in PLAY_JS
