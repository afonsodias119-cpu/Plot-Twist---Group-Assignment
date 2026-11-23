"""Plot Twist — saving and loading games in SQLite.

This is the only file that uses sqlite3. The table `games` has one row per player, holding the
progress (scene, inventory, flags, ending) and the language the game was started in.
The story itself is not stored: it stays in story.py (see specs/base-game.md, section 4).
The table `nights` keeps the 3D campus's notes for tonight (specs/evidence-and-hearing.md, point 1),
and the table `runs` one row for every night a name has finished (specs/earlier-nights.md, point 1).
The table `keys` keeps, for each name of the published game, the hash of the secret key of the browser
that started it (specs/name-belongs-to-browser.md, point 2).
"""

import json
import sqlite3
from contextlib import closing
from pathlib import Path

# Read every time a function runs, so the tests can point it at a temporary file.
DB_PATH = Path(__file__).resolve().parent / "data" / "plot_twist.db"


def init_db() -> None:
    """Create the data folder and the four tables, if they are missing.

    Every table is created here, in the same call, so no read ever creates a table on its own
    (specs/evidence-and-hearing.md, point 1). An older file gets the tables it lacks and keeps its rows.
    """
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with closing(sqlite3.connect(DB_PATH)) as connection, connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS games (
                player    TEXT PRIMARY KEY,
                scene     TEXT NOT NULL,
                inventory TEXT NOT NULL,
                flags     TEXT NOT NULL,
                ending    TEXT NOT NULL,
                language  TEXT NOT NULL
            )
            """
        )
        # The notes of the 3D campus for tonight (who was cracked, the answers of the hearing).
        # They cannot live in `games`: a save must have exactly the story's flags.
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS nights (
                player TEXT PRIMARY KEY,
                minute INTEGER NOT NULL,
                notes  TEXT NOT NULL
            )
            """
        )
        # One row per finished night of the 3D campus, never deleted (specs/earlier-nights.md, point 1):
        # the ending that was shown, or "time_up" when the faculty closed first.
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS runs (
                id     INTEGER PRIMARY KEY AUTOINCREMENT,
                player TEXT NOT NULL,
                ending TEXT NOT NULL
            )
            """
        )
        # The SHA-256 hash of each name's browser key, never the key itself (specs/name-belongs-to-browser.md).
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS keys (
                player   TEXT PRIMARY KEY,
                key_hash TEXT NOT NULL
            )
            """
        )


def save_game(player: str, state: dict, language: str = "en") -> None:
    """Write or replace that player's row. The inventory and flags are stored as JSON text."""
    init_db()
    # The values go in through "?" placeholders, so they are data and can never run as SQL.
    with closing(sqlite3.connect(DB_PATH)) as connection, connection:
        connection.execute(
            "INSERT OR REPLACE INTO games (player, scene, inventory, flags, ending, language) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (
                player,
                state["scene"],
                json.dumps(state["inventory"]),
                json.dumps(state["flags"]),
                state["ending"],
                language,
            ),
        )


def _read_row(player: str, columns: str):
    """The given columns of that player's row, or None if there is no row."""
    init_db()
    with closing(sqlite3.connect(DB_PATH)) as connection:
        return connection.execute(f"SELECT {columns} FROM games WHERE player = ?", (player,)).fetchone()


def load_game(player: str) -> dict | None:
    """That player's saved state, or None if there is no row or it cannot be read."""
    row = _read_row(player, "scene, inventory, flags, ending")
    if row is None:
        return None
    scene, inventory, flags, ending = row
    try:
        return {"scene": scene, "inventory": json.loads(inventory), "flags": json.loads(flags), "ending": ending}
    except ValueError:
        # The text is not valid JSON, so this save is broken and counts as no save.
        return None


def load_language(player: str) -> str | None:
    """The language saved in that player's row, or None if there is no row.

    It does not check that the language exists: game.py does.
    """
    row = _read_row(player, "language")
    return None if row is None else row[0]


def load_night(player: str) -> dict:
    """That player's night as {"minute", "notes"}. Minute 0 and no notes when there is no row
    or it cannot be read. It never writes: a broken row stays as it is.

    It only checks that the notes are a JSON object: campus_evidence.read_night checks what is inside.
    """
    init_db()
    with closing(sqlite3.connect(DB_PATH)) as connection:
        row = connection.execute("SELECT minute, notes FROM nights WHERE player = ?", (player,)).fetchone()
    if row is None:
        return {"minute": 0, "notes": {}}
    minute, text = row
    try:
        notes = json.loads(text)
    except (TypeError, ValueError, RecursionError):   # RecursionError: text nested too deep to read
        notes = {}
    if not isinstance(notes, dict):
        notes = {}
    if not isinstance(minute, int):
        minute = 0
    return {"minute": minute, "notes": notes}


def save_night(player: str, minute: int, notes: dict) -> None:
    """Write or replace that player's night. The notes are stored as JSON text."""
    init_db()
    with closing(sqlite3.connect(DB_PATH)) as connection, connection:
        connection.execute("INSERT OR REPLACE INTO nights (player, minute, notes) VALUES (?, ?, ?)",
                           (player, minute, json.dumps(notes)))


def delete_night(player: str) -> None:
    """Forget that player's night (a restart or a new game). Nothing happens if there is no row."""
    init_db()
    with closing(sqlite3.connect(DB_PATH)) as connection, connection:
        connection.execute("DELETE FROM nights WHERE player = ?", (player,))


def add_run(player: str, ending: str) -> None:
    """Add one row to `runs`: that player has finished a night with this ending."""
    init_db()
    with closing(sqlite3.connect(DB_PATH)) as connection, connection:
        connection.execute("INSERT INTO runs (player, ending) VALUES (?, ?)", (player, ending))


def load_runs(player: str) -> list:
    """The endings of that player's finished nights, oldest first ([] when there is none). It never writes."""
    init_db()
    with closing(sqlite3.connect(DB_PATH)) as connection:
        rows = connection.execute("SELECT ending FROM runs WHERE player = ? ORDER BY id", (player,)).fetchall()
    return [row[0] for row in rows]


def load_key_hash(player: str) -> str | None:
    """The stored hash of that name's browser key, or None if no browser has claimed the name."""
    init_db()
    with closing(sqlite3.connect(DB_PATH)) as connection:
        row = connection.execute("SELECT key_hash FROM keys WHERE player = ?", (player,)).fetchone()
    return None if row is None else row[0]


def save_key_hash(player: str, key_hash: str) -> None:
    """Remember the hash of the key of the browser that claimed that name."""
    init_db()
    with closing(sqlite3.connect(DB_PATH)) as connection, connection:
        connection.execute("INSERT OR REPLACE INTO keys (player, key_hash) VALUES (?, ?)", (player, key_hash))
