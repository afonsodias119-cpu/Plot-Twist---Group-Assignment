"""Lets the tests import app files (logic.py, db.py) from the project folder."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


@pytest.fixture(autouse=True)
def temp_database(tmp_path, monkeypatch):
    """Point db.DB_PATH at a file in a throwaway folder, so no test touches the real saved games."""
    import db

    monkeypatch.setattr(db, "DB_PATH", tmp_path / "plot_twist.db")
