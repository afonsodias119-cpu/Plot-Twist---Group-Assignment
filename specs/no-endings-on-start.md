# No count of endings on the start screen

Changes specs/campus-people-and-atmosphere.md ("Collection of endings": the first screen no longer shows it). Only the 3D game changes. No change to `story.py`, `logic.py`, `db.py`, `game.py`, `app.py` or any reviewed test.

## Before writing the spec

- **Product and user:** a player who opens the 3D game.
- **Trigger:** the player types their name on the first screen.
- **Before:** under the name field, the screen says "Finais descobertos: 0/4 🔒 🔒 🔒 🔒" / "Endings found: 0/4 …".
- **Rule:** the player should discover the endings by playing, not be told how many there are before starting.
- **After:** the first screen shows only the name field and its hint. The ending screen still shows "Endings found: n/4" with the ones found.

## Why

As a player, I want to start the game without knowing how many endings exist, so that the secret ending stays a surprise.

## What

- [ ] `prototypes/campus-3d/play.js`: the first screen has no collection line (the `collection` paragraph is removed from the name box, and nothing fills it).
- [ ] The ending screen (`ending-collection`) and the share card keep the count, through `collectionText` and `collectionCount`.

## Out of scope

The ending screen, the share card, the plain game.

## Done when

- [ ] Existing tests pass unchanged.
- [ ] `tests/test_no_endings_on_start.py`: the name box holds no collection line; the ending screen still fills `ending-collection` with `collectionText()`.
- [ ] In the browser: the first screen shows no "Endings found"; after an ending, the ending screen shows it.
