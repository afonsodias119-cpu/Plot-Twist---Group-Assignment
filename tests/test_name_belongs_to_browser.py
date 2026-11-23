"""A saved name belongs to the browser that started it (specs/name-belongs-to-browser.md).

The checks follow the spec's "What" points: the key (1), the storage (2), the command (3), the app (4),
the bridge (5), the page (6) and the texts (7).
"""

import hashlib
import sqlite3
import sys
from contextlib import closing
from pathlib import Path

import pytest

PROJECT = Path(__file__).resolve().parent.parent
FOLDER = PROJECT / "prototypes" / "campus-3d"
sys.path.insert(0, str(FOLDER))

import campus_game  # noqa: E402
import db  # noqa: E402
import game  # noqa: E402
from campus_text import TEXT  # noqa: E402

APP = (PROJECT / "app_3d.py").read_text(encoding="utf-8")   # read, not run: running it starts Streamlit
PLAY = (FOLDER / "play.js").read_text(encoding="utf-8")


def open_payload(player="Ana", language="en", **extra):
    return dict({"operation": "open", "player": player, "language": language}, **extra)


# ---------- point 1: the key ----------

def test_a_free_name_gets_a_new_key():
    key = game.claim_name("Ana", None)
    assert isinstance(key, str) and len(key) >= 32


def test_the_owner_gets_the_same_key_back():
    key = game.claim_name("Ana", None)
    assert game.claim_name("Ana", key) == key
    assert game.claim_name("  ANA ", key) == key   # the same name as game.clean_name sees it


@pytest.mark.parametrize("other", [None, "", "wrong-key", 42, ["x"]])
def test_a_claimed_name_refuses_any_other_key(other):
    game.claim_name("Ana", None)
    assert game.claim_name("Ana", other) is None


def test_two_names_get_different_keys():
    assert game.claim_name("Ana", None) != game.claim_name("Rui", None)


@pytest.mark.parametrize("player", [None, "", "<script>!!", "x" * 21, 7])
def test_an_invalid_name_claims_nothing(player):
    assert game.claim_name(player, None) == ""
    db.init_db()
    with closing(sqlite3.connect(db.DB_PATH)) as connection:
        assert connection.execute("SELECT COUNT(*) FROM keys").fetchone()[0] == 0


# ---------- point 2: the storage ----------

def test_init_db_creates_the_keys_table_next_to_the_others():
    db.init_db()
    with closing(sqlite3.connect(db.DB_PATH)) as connection:
        tables = {row[0] for row in connection.execute("SELECT name FROM sqlite_master WHERE type = 'table'")}
    assert {"games", "nights", "runs", "keys"} <= tables


def test_only_the_hash_of_the_key_is_stored():
    key = game.claim_name("Ana", None)
    stored = db.load_key_hash("ana")
    assert stored == hashlib.sha256(key.encode("utf-8")).hexdigest()
    assert key not in db.DB_PATH.read_bytes().decode("latin-1")


def test_load_and_save_key_hash():
    assert db.load_key_hash("ana") is None
    db.save_key_hash("ana", "abc")
    assert db.load_key_hash("ana") == "abc"


# ---------- point 3: the command ----------

def test_keyed_command_starts_a_game_and_returns_the_key():
    result, key = campus_game.keyed_command(open_payload())
    assert result["player"] == "ana"
    assert game.claim_name("Ana", key) == key


def test_keyed_command_lets_the_owner_continue():
    _, key = campus_game.keyed_command(open_payload())
    result, again = campus_game.keyed_command(open_payload(key=key))
    assert again == key
    assert result["player"] == "ana"


@pytest.mark.parametrize("language", ["en", "pt"])
def test_keyed_command_refuses_someone_else_before_anything_changes(language):
    campus_game.keyed_command(open_payload())
    before = db.load_game("ana")
    with pytest.raises(ValueError) as error:
        campus_game.keyed_command({"operation": "restart", "player": "ana", "language": language,
                                   "confirmed": True, "key": "someone-else"})
    assert str(error.value) == TEXT[language]["name_taken"]
    assert db.load_game("ana") == before


def test_the_key_never_reaches_command(monkeypatch):
    seen = []
    monkeypatch.setattr(campus_game, "command", lambda payload: seen.append(payload) or {"player": "ana"})
    campus_game.keyed_command(open_payload(key="anything"))
    assert seen == [open_payload()]


def test_keyed_command_does_not_change_the_callers_payload():
    payload = open_payload(key=None)
    campus_game.keyed_command(payload)
    assert "key" in payload


def test_keyed_command_still_refuses_bad_requests():
    for payload in (None, [], {"operation": "open"}, open_payload(player="<b>")):
        with pytest.raises(ValueError):
            campus_game.keyed_command(payload)


def test_command_itself_is_unchanged():
    # Every reviewed test calls command() without a key: it still works by name only.
    assert campus_game.command(open_payload())["player"] == "ana"
    with pytest.raises(ValueError):
        campus_game.command(open_payload(key="x"))   # its allowed fields did not grow


# ---------- points 4 and 5: the app and the bridge ----------

def test_answer_uses_the_keyed_command_and_returns_the_key():
    assert "campus_game.keyed_command(payload)" in APP
    assert '"key": key' in APP


def test_the_bridge_sends_and_keeps_the_key():
    assert "plot-twist-keys" in APP
    assert "payload.player" in APP and ".trim().toLowerCase()" in APP
    assert "reply.key" in APP
    assert "localStorage" in APP


# ---------- points 6 and 7: the page and the texts ----------

def test_the_texts_exist_in_both_languages():
    assert TEXT["en"]["name_taken"] == ("Someone on another device or browser is already playing with this name. "
                                        "Choose another name.")
    assert TEXT["pt"]["name_taken"] == ("Alguém noutro dispositivo ou browser já está a jogar com este nome. "
                                        "Escolhe outro nome.")


def test_the_page_goes_back_to_the_name_when_it_is_taken():
    assert "ui().name_taken" in PLAY
    assert "goStep(" in PLAY[PLAY.index("ui().name_taken"):PLAY.index("ui().name_taken") + 400]
