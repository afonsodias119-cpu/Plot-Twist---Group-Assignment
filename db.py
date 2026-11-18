"""Plot Twist — saving and loading games in SQLite.

This is the only file that uses sqlite3. One table, one row per player, holding the
progress (scene, inventory, flags, ending) and the language the game was started in.
The story itself is not stored: it stays in story.py (see specs/base-game.md, section 4).
"""

import json
import sqlite3
from contextlib import closing
from pathlib import Path

# Read every time a function runs, so the tests can point it at a temporary file.
DB_PATH = Path(__file__).resolve().parent / "data" / "plot_twist.db"


def init_db() -> None:
    """Create the data folder and the games table, if they are missing."""
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
