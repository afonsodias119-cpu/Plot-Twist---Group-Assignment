"""Duarte only speaks in the hearing, and the professor can be reached (specs/duarte-only-in-the-hearing.md)."""

import re
from pathlib import Path

FOLDER = Path(__file__).resolve().parents[1] / "prototypes" / "campus-3d"
PLAY_JS = (FOLDER / "play.js").read_text(encoding="utf-8")
HTML = (FOLDER / "game3d.html").read_text(encoding="utf-8")


def test_duarte_is_never_a_conversation():
    assert 'const NOT_TALKED_TO = ["duarte"];' in PLAY_JS
    assert "if (NOT_TALKED_TO.includes(person.id)) continue;" in PLAY_JS        # no "Talk to Duarte" button
    assert '|| !current || npc === "duarte") return;' in PLAY_JS               # talkStep ignores him


def test_k_never_picks_duarte():
    assert 'if (n.userData.id === "duarte") continue;' in HTML


def test_the_aisle_is_wide_and_the_blocks_follow_the_seats():
    assert "if (Math.abs(x - 6.55) < 0.9) continue;" in HTML
    blocks = re.search(r"block\(([\d.]+), z - 0\.05, ([\d.]+), 0\.7\); block\(([\d.]+), z - 0\.05, ([\d.]+), 0\.7\);", HTML)
    left = (float(blocks.group(1)) - float(blocks.group(2)) / 2, float(blocks.group(1)) + float(blocks.group(2)) / 2)
    right = (float(blocks.group(3)) - float(blocks.group(4)) / 2, float(blocks.group(3)) + float(blocks.group(4)) / 2)
    seats = [round(1.4 + 0.75 * i, 2) for i in range(14) if 1.4 + 0.75 * i <= 11.8 and abs(1.4 + 0.75 * i - 6.55) >= 0.9]
    # every seat (0.62 wide) is inside a block, and the free floor between the blocks fits the character (0.6) easily
    for x in seats:
        assert any(low - 0.01 <= x - 0.31 and x + 0.31 <= high + 0.01 for low, high in (left, right)), x
    assert right[0] - left[1] >= 2.0
