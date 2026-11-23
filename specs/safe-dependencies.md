# Dependencies without known vulnerabilities

Changes `pyproject.toml`, `uv.lock` and the two places that load scripts from a CDN (`prototypes/campus-3d/game3d.html` and `prototypes/campus-3d/play.js`). No game rule changes. No reviewed test changes.

## Before writing the spec

- **Product and user:** the teaching staff reviewing security, and every player of the public link.
- **Trigger:** `uv audit` on the lock file, and loading the page.
- **Before:** `uv audit` finds 62 known vulnerabilities, all in Pillow 12.3.0. Pillow comes with Streamlit, and Streamlit 1.62.0 only allows Pillow below 13 (the fixes are in 13.0.0). `pytest` is installed on the public server although only the tests use it. Three.js and the QR code library are pinned to a version but loaded without an integrity check.
- **Rule:** dependencies minimal, pinned and without known vulnerabilities (course rubric, Security).
- **After:** Streamlit 1.67.0 (which allows Pillow 13) and Pillow 13 or newer; `uv audit` finds nothing. `pytest` is a development dependency. Every script from a CDN carries a SHA-384 integrity hash, so the browser refuses a file that was changed.

## Why

As a player, I want the game to run only the code the team chose, without libraries that have known security holes.

## What

1. `pyproject.toml`: `streamlit==1.67.0` and `pillow>=13.0.0` in `dependencies`; `pytest==9.1.1` moves to `[dependency-groups] dev` (still installed by `uv sync`, so `uv run pytest` works as before). `uv.lock` is rebuilt with `uv lock`.
2. `game3d.html`: the import map gets an `integrity` table with the SHA-384 hash of every Three.js file the page imports (three.module.js and each add-on file, including the files the add-ons import themselves).
3. `play.js`: the QR library's `<script>` gets `integrity` and `crossOrigin = "anonymous"`. The address stays the pinned one that `tests/test_touch_card_qr.py` checks.

## Limits

- Browsers that do not know import-map integrity (older than Chrome 127, Firefox 138, Safari 18) ignore it and load the files as before.
- A new Streamlit version can change how components behave; the whole game is played again in the browser after the upgrade.

## Out of scope

Hosting the scripts on our own server, the Google Fonts stylesheet (a font cannot run code).

## Done when

- [ ] Existing tests pass unchanged on Streamlit 1.67.0.
- [ ] `tests/test_safe_dependencies.py`: the pins in `pyproject.toml`, pytest only in the dev group, the lock's Streamlit and Pillow versions, an integrity hash for every CDN file the page imports, and the QR script's integrity.
- [ ] `uv audit` reports no known vulnerabilities.
- [ ] In the browser: the 3D campus loads (no integrity errors in the console) and the QR code is drawn.
