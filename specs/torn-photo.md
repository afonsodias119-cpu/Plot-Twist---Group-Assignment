# The torn photo

> **Update (specs/calendar-code.md):** the cover photo is now dated Saturday 17 October, so the code of computer 12 is `1710`, the photo's stamp says 17.10 and the slip on the shutter says 17 October. The clerk's `order` line no longer says the date.

Changes how the original photo is obtained in the 3D game (specs/actions-when-they-make-sense.md made the copy appear after the clerk mentions the order). Only the 3D game changes. No change to `story.py`, `logic.py`, `db.py`, `game.py`, `app.py` or any reviewed test.

## Before writing the spec

- **Product and user:** a player of the 3D game at the print shop.
- **Trigger:** the player has asked the clerk about the cover photo order and chooses to get the original.
- **Before:** one click on "Ask for a copy of the original order" gives the photo.
- **Rule:** the original photo has to be rebuilt by the player, like a jigsaw puzzle.
- **After:**
  - The clerk goes to the archive and comes back: someone shredded the original print of your order last night. She pours the pieces on the counter.
  - A window shows a frame and 9 torn pieces around it, scattered and turned. The player drags a piece into a place of the frame (it snaps there) and taps a piece to turn it 90°.
  - When the frame is full, the page sends the arrangement to the server. A wrong arrangement only says it does not fit yet (no time is taken). The right one gives the original photo, exactly as before, and the rebuilt photo shows four people and the date stamp "14.11".

## Why

As a player, I want getting the original photo to be a puzzle I solve with my hands, so that the second clue feels earned, and seeing the four people and the date with my own eyes proves the point of the story.

## What

- [ ] `prototypes/campus-3d/campus_search.py` (server only): `PHOTO_PIECES` (the 9 piece ids) and `PHOTO_SOLUTION` (which piece goes in each place of the frame, in reading order, all upright); `PHOTO_TEXT` with the text of the rebuilt photo, in both languages.
- [ ] `prototypes/campus-3d/campus_game.py`: new operation `assemble` (`player`, `language`, `pieces`): `pieces` is a list of 9 `[piece id, rotation]`, one for each place of the frame in reading order, each piece once, rotation 0, 90, 180 or 270. Anything else is rejected. Outside the print shop, or with the photo already taken, nothing happens. A wrong arrangement saves nothing and answers `assembled: false`; the right one plays the story's own `request_copy` action and answers `assembled: true` with `PHOTO_TEXT`.
- [ ] New file `prototypes/campus-3d/photo.js`: draws the photo (four people of the group in front of the campus, with the date stamp), cuts it into 9 pieces with torn edges, and shows the window with the frame. It only draws, moves, turns and snaps the pieces; it does not know the solution and asks play.js when the frame is full.
- [ ] `prototypes/campus-3d/play.js`: in the clerk's conversation, the copy (`request_copy`) keeps its label ("Pedir uma cópia do pedido original" / "Ask for a copy of the original order", as the reviewed conversation test asks); choosing it adds the clerk's line about the shredded photo and opens the window instead of playing the action. When the server says the photo is rebuilt, the window closes and the conversation shows the result.
- [ ] `prototypes/campus-3d/campus_text.py`: `photo_intro`, `photo_title`, `photo_hint` (only how to move and turn the pieces), `photo_wrong`, `photo_close`, in both languages.
- [ ] `page3d.py`, `server3d.py`, `app_3d.py`: `photo.js` goes in the page like `table.js`. `play.css`: the window reuses the style of the table's window.

## Limits

Like the other puzzles, this is not security: the drawing is in the page, so someone reading the source can work out the solution. Only the server decides if the photo is right, and the reviewed tests still play `request_copy` directly.

## Out of scope

Leonor, the code of computer 12, the plain game.

## Done when

- [ ] Existing tests pass unchanged.
- [ ] `tests/test_torn_photo.py`: a wrong arrangement saves nothing; the right one gives the photo once; outside the print shop nothing happens; bad arrangements (wrong length, unknown or repeated pieces, bad rotations, wrong types, extra fields) are rejected; the solution and the rebuilt text are not in the page; `photo.js` draws 9 pieces and the date stamp; choosing the copy in the conversation opens the pieces; the texts exist in both languages; the page carries `photo.js`.
- [ ] In the browser: at the print shop, after asking about the order, the pieces appear; dragging snaps them, tapping turns them; a wrong full frame says it does not fit; the right one gives the photo.
