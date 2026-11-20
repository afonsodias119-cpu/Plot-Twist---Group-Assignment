# Playable Campus 3D

## Why
The campus prototype lets the player walk, but does not play the mystery. Connect it to the existing Python game so the player can investigate **The Fifth Element**, save and reach either original ending.

## What
- Keep the colleague's 3D campus and opening case file. Keep all story texts, choices, rules and both endings in the existing `story.py` / `logic.py` / `game.py`.
- Add a small local HTTP server (`server3d.py`) using Python's standard library. It serves only the generated page and two UI files, and accepts JSON commands. It binds to 127.0.0.1; it is not a public deployment server.
- A separate adapter (`campus_game.py`) validates commands, calls `game.py`, and returns only the current scene's texts and offered actions. The browser cannot supply game state, inventory, flags or endings.
- Names and language work like the base game. The 3D prototype uses its own SQLite file by default, so trying it cannot replace the original Streamlit saves.
- Movement between scenes uses the original action buttons. The character follows the saved scene. WASD / arrows only explore within that room: they never bypass a locked route. On-screen buttons support keyboard, touch and a text-only fallback when WebGL/CDN is unavailable.
- Separate investigation and travel actions. Explain blocked choices beside their buttons. Mark irreversible dialogue decisions before the player selects them.
- Add an evidence notebook derived from collected items and remembered flags. Use the existing action result texts, and never reveal undiscovered clues. No new storyline or third ending.
- Save each accepted action through `game.play`. Show success only after the server replies. Disable controls during requests; errors do not claim progress was saved.
- New game opens a confirmation dialog. Cancel sends no command. Server restart commands require explicit `confirmed: true`. On an ending, hide all ordinary actions and stop character movement.
- Render player names and story text with `textContent`. Validate request shape, name, language and operation before any write. Reject cross-origin JSON requests and do not serve repository files or databases.

## Out of scope
Public hosting/authentication, multiplayer, new mysteries, new puzzles, changing the course-approved Streamlit interface, replacing artwork, changing existing tests, merging without a teammate's review.

## Done when
- Existing tests pass unchanged.
- New adapter and HTTP tests cover both endings in both languages, locked actions with unchanged saves, duplicate collection, resume including language/decision, confirmed restart, invalid input and no spoiler leakage.
- Browser checks cover a complete playthrough, reload/resume, cancellation, responsive layout and text-only play.
- README explains how to start/stop and which SQLite file holds prototype progress. A Portuguese handover identifies changes, limitations and how each file works.
