"""The first click never times out (specs/warm-start.md)."""

import sqlite3
import sys
from contextlib import closing
from pathlib import Path

import pytest

PROJECT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT / "prototypes" / "campus-3d"))

import campus_game  # noqa: E402
import db  # noqa: E402

APP = (PROJECT / "app_3d.py").read_text(encoding="utf-8")   # read, not run: running it starts Streamlit


def test_the_warm_up_is_answered_without_a_name_or_a_key():
    assert campus_game.keyed_command({"warmup": True}) == ({"warm": True}, "")


def test_the_warm_up_writes_nothing():
    campus_game.keyed_command({"warmup": True})
    assert not db.DB_PATH.exists()


def test_the_warm_up_never_reaches_command(monkeypatch):
    monkeypatch.setattr(campus_game, "command", lambda payload: pytest.fail("command was called"))
    campus_game.keyed_command({"warmup": True})


@pytest.mark.parametrize("payload", [
    {"warmup": False},
    {"warmup": 1},
    {"warmup": True, "operation": "open", "player": "Ana", "language": "en"},
])
def test_anything_else_is_still_checked_by_command(payload):
    with pytest.raises(ValueError):
        campus_game.keyed_command(payload)


def test_a_real_command_still_works_after_a_warm_up():
    campus_game.keyed_command({"warmup": True})
    result, key = campus_game.keyed_command({"operation": "open", "player": "Ana", "language": "en"})
    assert result["player"] == "ana" and key
    with closing(sqlite3.connect(db.DB_PATH)) as connection:
        assert connection.execute("SELECT COUNT(*) FROM games").fetchone()[0] == 1


def test_the_bridge_warms_up_right_after_it_is_ready():
    ready = APP.index('post({ type: "streamlit:componentReady", apiVersion: 1 });')
    warm = APP.index("window.campusBridge.call({ warmup: true })")
    assert ready < warm
    assert ".catch(() => {})" in APP[warm:warm + 120]   # its answer (or its failure) is never shown


def test_the_bridge_waits_sixty_seconds():
    assert 'reject(new TypeError("timeout")); }, 60000);' in APP
    assert "}, 20000);" not in APP
