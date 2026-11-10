"""Lets the tests import app files (logic.py, db.py) from the project folder."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
