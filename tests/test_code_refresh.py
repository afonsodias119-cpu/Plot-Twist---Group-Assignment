"""Checks for loading fresh code after a deploy (specs/fresh-code-after-deploy.md).

The hosted app can receive new files without being restarted. code_refresh.refresh notices
that and loads the changed modules again, so the 3D page and the Python code always match.
"""

import importlib
import sys
from pathlib import Path

import pytest

PROJECT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT / "prototypes" / "campus-3d"))
code_refresh = importlib.import_module("code_refresh")


@pytest.fixture
def temp_modules(tmp_path, monkeypatch):
    """Two throwaway modules in a temporary folder: tmp_story, and tmp_reader that imports from it."""
    story_file = tmp_path / "tmp_story.py"
    reader_file = tmp_path / "tmp_reader.py"
    story_file.write_text("VALUE = 1\n", encoding="utf-8")
    reader_file.write_text("from tmp_story import VALUE\n", encoding="utf-8")
    monkeypatch.syspath_prepend(str(tmp_path))
    monkeypatch.setattr(sys, "dont_write_bytecode", True)
    importlib.invalidate_caches()
    story = importlib.import_module("tmp_story")
    reader = importlib.import_module("tmp_reader")
    yield story_file, reader_file, story, reader
    sys.modules.pop("tmp_story", None)
    sys.modules.pop("tmp_reader", None)


def test_first_call_only_remembers_the_version(temp_modules):
    """A process that just started has fresh code: the first call reloads nothing."""
    story_file, reader_file, story, _reader = temp_modules
    story.MARK = "still here"
    state = {"version": None}
    assert code_refresh.refresh([story_file, reader_file], ["tmp_story", "tmp_reader"], state) is False
    assert state["version"] == code_refresh.version([story_file, reader_file])
    assert story.MARK == "still here"


def test_unchanged_files_reload_nothing(temp_modules):
    """While the files stay the same, nothing is reloaded."""
    story_file, reader_file, story, _reader = temp_modules
    files, names, state = [story_file, reader_file], ["tmp_story", "tmp_reader"], {"version": None}
    code_refresh.refresh(files, names, state)
    story.VALUE = "changed only in memory"
    assert code_refresh.refresh(files, names, state) is False
    assert story.VALUE == "changed only in memory"


def test_changed_file_reloads_its_module(temp_modules):
    """When a file changes on disk, its module is loaded again."""
    story_file, reader_file, story, _reader = temp_modules
    files, names, state = [story_file, reader_file], ["tmp_story", "tmp_reader"], {"version": None}
    code_refresh.refresh(files, names, state)
    story_file.write_text("VALUE = 'a new, longer value'\n", encoding="utf-8")
    assert code_refresh.refresh(files, names, state) is True
    assert story.VALUE == "a new, longer value"
    assert state["version"] == code_refresh.version(files)


def test_modules_that_import_from_a_changed_one_see_the_new_value(temp_modules):
    """A module listed after the changed one gets the new value too."""
    story_file, reader_file, _story, reader = temp_modules
    files, names, state = [story_file, reader_file], ["tmp_story", "tmp_reader"], {"version": None}
    code_refresh.refresh(files, names, state)
    assert reader.VALUE == 1
    story_file.write_text("VALUE = 'a new, longer value'\n", encoding="utf-8")
    code_refresh.refresh(files, names, state)
    assert reader.VALUE == "a new, longer value"


def test_app_3d_recovers_from_stale_code(monkeypatch):
    """Old code in memory with new files on disk (a deploy without a restart): the app loads them again."""
    from streamlit.testing.v1 import AppTest

    page3d = importlib.import_module("page3d")
    app = AppTest.from_file(str(PROJECT / "app_3d.py"), default_timeout=30)
    app.run()
    assert not app.exception

    # Pretend the code in memory is older than the files: the bug of 21 Nov 2026.
    monkeypatch.setitem(code_refresh.LOADED, "version", "an older version")
    # Changed by specs/combined-start-briefing.md ("Reviewed tests that change"): "group" is no longer a text of the
    # case file, so the stale text removed here is "stamp". Was: "group".
    del page3d.EXTRA["en"]["stamp"]
    with pytest.raises(KeyError):
        page3d.EXTRA["en"]["stamp"]

    app.run()
    assert not app.exception
    assert page3d.EXTRA["en"]["stamp"]   # was "group" (specs/combined-start-briefing.md)
    assert '"stamp"' in page3d.build_page(playable=True, inline=True)
