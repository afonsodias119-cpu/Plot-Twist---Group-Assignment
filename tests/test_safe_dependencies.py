"""Dependencies without known vulnerabilities (specs/safe-dependencies.md)."""

import re
import tomllib
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
FOLDER = PROJECT / "prototypes" / "campus-3d"
PYPROJECT = tomllib.loads((PROJECT / "pyproject.toml").read_text(encoding="utf-8"))
LOCK = tomllib.loads((PROJECT / "uv.lock").read_text(encoding="utf-8"))
HTML = (FOLDER / "game3d.html").read_text(encoding="utf-8")
PLAY = (FOLDER / "play.js").read_text(encoding="utf-8")


def locked(name):
    return next(package["version"] for package in LOCK["package"] if package["name"] == name)


def version(text):
    return tuple(int(part) for part in text.split(".")[:3])


def test_the_app_dependencies_are_pinned_and_minimal():
    assert PYPROJECT["project"]["dependencies"] == ["streamlit==1.67.0", "pillow>=13.0.0"]


def test_pytest_is_only_a_development_dependency():
    assert PYPROJECT["dependency-groups"]["dev"] == ["pytest==9.1.1"]


def test_the_lock_has_the_fixed_versions():
    assert locked("streamlit") == "1.67.0"
    assert version(locked("pillow")) >= (13, 0, 0)


def test_every_three_js_file_the_page_imports_has_an_integrity_hash():
    import_map = HTML[HTML.index('<script type="importmap">'):]
    import_map = import_map[:import_map.index("</script>")]
    hashes = dict(re.findall(r'"(https://cdn\.jsdelivr\.net/npm/three@0\.160\.0/[^"]+)":\s*"(sha384-[A-Za-z0-9+/=]+)"', import_map))
    assert "https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js" in hashes
    addons = re.findall(r'from "three/addons/([^"]+)"', HTML)
    assert addons
    for addon in addons:
        assert f"https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/{addon}" in hashes, addon


def test_the_qr_script_has_an_integrity_hash():
    assert re.search(r'script\.integrity = "sha384-[A-Za-z0-9+/=]+";', PLAY)
    assert 'script.crossOrigin = "anonymous";' in PLAY
