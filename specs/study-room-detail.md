# A lived-in study room

Extends specs/hidden-object-table.md and specs/campus-people-and-atmosphere.md. Only the 3D picture changes (`prototypes/campus-3d/game3d.html`). No change to `story.py`, `logic.py`, `db.py`, `game.py`, `app.py`, `play.js`, the server or any reviewed test.

## Why
The study room had one table, a whiteboard and two plants: it looked empty next to the library and the computer lab, although it is the room the player comes back to most.

## What
Furniture along the walls and in the free corner, so the room looks like a real student study room at night:
1. **West wall:** a low cabinet with standing binders, a printer with a sheet in it, a tray of paper and a pot of pens; a corkboard above it with four notes (the deadline, a study group, a lost charger, the exam timetable); a row of three student lockers nearer the door, and a small "Silêncio" sign.
2. **East wall:** a sofa with two cushions, a low coffee table with a mug and a magazine, a lit floor lamp, a framed "NOVA SBE" poster and a wall clock without hands (the time is the one on the screen); a water cooler near the door.
3. **South-west corner:** a small round table for two with a laptop left open and a cup, and a coat stand with a coat and a scarf.
4. **Under the windows:** two radiators.

Rules: every new piece stands against a wall or in the south-west corner and has a collision box (`block`); the way from the door to the table, the floor around the table and Rita's place stay clear; nothing new can be clicked or searched (the table close-up of specs/hidden-object-table.md is unchanged); the floor stays clear of clutter. No new light is added (the floor lamp only glows), so the game does not get slower.

## Out of scope
New clues or things to look at, new people, other rooms, the plain game.

## Done when
- Existing tests pass unchanged.
- New tests (`tests/test_study_room_detail.py`): the new block exists before the hidden-object section; it has the cabinet, corkboard, lockers, sofa, coffee table, floor lamp, poster, clock, water cooler, round table, coat stand and radiators; every piece has a collision box; it adds no `lamp(` (no new light) and nothing to `mess`.
- A browser check shows the furnished room with no errors and the player able to walk from the door to the table.
