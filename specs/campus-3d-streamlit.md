# Campus 3D inside Streamlit

## Why
The 3D game (specs/playable-campus-3d.md) needs its own local server, so the public Streamlit link still shows the plain game. The course demo must run at the deployed URL, so the 3D version has to run on Streamlit itself.

## What
- New file `app_3d.py`, the file to publish. `app.py` and all existing tests stay unchanged and `app.py` remains the fallback.
- The 3D page runs in a Streamlit component (an iframe). Instead of `fetch("/api/command")`, `play.js` calls `window.campusBridge.call(payload)` when that object exists. The bridge sends the same JSON command to Python with `setComponentValue`; Python answers through the component argument `reply`.
- Python runs the command with the existing `campus_game.command()`. All rules, validation and saving stay in `campus_game.py`, `game.py`, `logic.py` and `db.py`. The browser still cannot set state, inventory, flags or endings.
- Invalid commands and unexpected errors come back as an `error` text; errors never claim progress was saved and never show file paths.
- The page loads `play.js` and `play.css` inline (`build_page(playable=True, inline=True)`), because a component has no server to fetch them from. Running the local server (`server3d.py`) works as before.
- Saves go to `data/campus3d.db`, the same file as the local 3D server, not to the plain game's database.

## Out of scope
Authentication, persistent hosting (saved games can still be lost when the hosted app restarts), changing the 3D story or rules, changing `app.py`.

## Done when
- Existing tests pass unchanged.
- Tests cover: the inline page (no external `/play.js`, all UI code inside, valid in an HTML script block), the bridge used only inside Streamlit, and `app_3d.py` running without an exception.
- A browser check shows the 3D campus inside Streamlit, a started game saved by Python, and a bad command refused.
