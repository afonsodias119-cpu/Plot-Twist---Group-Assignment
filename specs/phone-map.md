# Phone map — where am I on campus?

**Blocked by:** nothing. The base game and the group chat puzzle are on `main`.

## Before writing the spec

- **Product and user:** a player who is moving between rooms and wants to see where they are.
- **Trigger:** the player opens the "📱 Phone" panel on the scene screen.
- **Before:** the saved game (scene, inventory, flags).
- **Rule:** the map only shows the game; it never changes it. A room is locked when the study room's way into it is not allowed yet.
- **After:** the panel shows the five rooms in their places, the current room marked, and locked rooms with a lock.
- **Restart:** nothing new is saved, so nothing changes on a restart.

## Why

As a player, I want to pull out my phone and see the campus map, so that I always know where I am and which door is still locked. It answers the team's idea of "checking the map on the phone" with a small, explainable change.

## What

- [ ] `story.py` has `CAMPUS_MAP`, the layout of `docs/historia.md` section 3 as three rows of three cells (`None` for an empty cell), and `MAP_LOCATION`, which says on which room a scene without its own place is shown (`group_chat` is shown on `computer_lab`). Every scene appears exactly once, either in `CAMPUS_MAP` or in `MAP_LOCATION`.
- [ ] `game.campus_map(language, state) -> list[list[dict | None]]`: the same rows, each room as `{"id", "title", "here", "locked"}`. `title` is the scene title in that language. `here` is `True` only for the room of the current scene (using `MAP_LOCATION`). `locked` is `True` when the study room's action that leads to that room is offered but not allowed. It never changes the state it is given.
- [ ] On the scene screen, `app.py` shows an `st.expander` with the label `UI["phone"]`. Inside it, each room is a bordered box in its place: the current room with 📍 and `UI["map_here"]`, a locked room with 🔒. The ending screen has no map.
- [ ] `UI_TEXTS` has `phone`, `map_here` and `map_locked` in both languages.

Checks (`tests/test_map.py`):

- [ ] `test_map_shows_every_scene_once`
- [ ] `test_new_game_is_in_the_study_room`
- [ ] `test_the_chat_is_shown_in_the_computer_lab`
- [ ] `test_auditorium_is_locked_until_the_files_are_viewed`
- [ ] `test_map_uses_the_language_of_the_game`
- [ ] `test_map_never_changes_the_game`
- [ ] `test_phone_map_is_on_the_scene_screen` (AppTest)
- [ ] `test_ending_screen_has_no_map` (AppTest)

## Out of scope

- Moving by clicking on the map (travel stays with the action buttons and the story's rules).
- Remembering which rooms were visited (that would be new saved state).
- An image of the map, or changes to the 3D prototype (it has its own phone).

## Done when

- `uv run pytest` is green; the tests were written before the code.
- By clicking: the panel shows 📍 in the study room at the start, follows the player into each room, shows the chat on the computer lab, and the 🔒 on the auditorium disappears after viewing the files.
- `logic.py`, `db.py`, `pyproject.toml` and `uv.lock` are unchanged.
- Own branch, pushed, reviewed by another member.

## Limits and how it could change

| Limit | How it could change |
|---|---|
| The map does not show visited rooms. | Add one flag per room, set by each `go_` action. |
| The layout is fixed in `story.py`. | A second mystery adds its own `CAMPUS_MAP`. |
