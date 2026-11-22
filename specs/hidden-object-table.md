# The USB stick is hidden in the mess of the table

Changes item 1 of specs/pen-and-code.md (search the study room). Only the 3D game changes. No change to `story.py`, `logic.py`, `db.py`, `game.py`, `app.py` or any reviewed test: the server keeps the `search` operation exactly as it is, only the list of places in `campus_search.py` changes.

## Before writing the spec

- **Product and user:** a player of the 3D game looking for the group's USB stick in the study room.
- **Trigger:** the player is in the study room and has not found the USB stick yet.
- **Before:** nine places of the room can be clicked (drawer, coat, mug, backpack, books, papers, bin, plant pot, pizza box). The stick is under the pizza box. With nine places it is found in a few clicks.
- **Rule:** the stick is somewhere on an extremely messy table, and the player has to find it with their own eyes, like a hidden-object game.
- **After:**
  - Only the table can be searched. In the 3D picture the table is covered in clutter; clicking it, or the "Ver a mesa" / "Look at the table" button of the side panel, opens a close-up of the table seen from above.
  - The close-up is a drawing with dozens of objects piled up: report pages, pizza boxes and slices, napkins, cans, mugs, cables, sticky notes, pens, highlighters, headphones, keys, a calculator, crisps and notebooks. Nothing is made to look like a USB stick (an eraser, chewing gum, a lighter, a memory card and a charger were tried and removed: they made no sense on the table). The stick is small, dark, and half under a napkin. It is always in the same place.
  - Every object can be clicked. A wrong one says what it is ("An empty can of soda.") and costs 1 minute; then every object of that kind is marked with ✗ and its name, and does not cost again. The right one gives the stick, exactly as before.
  - The drawer, the coat and the plants are only scenery, and nothing lies on the floor (the backpack, the books, the papers and the bin are gone): all the mess is on the table.
  - No text says where the stick is: the side panel has only the "Ver a mesa" / "Look at the table" button, and the close-up only says "Encontra a pen do grupo." / "Find the group's USB stick." (the cost of a wrong object shows when it happens, as "−1 minute").
  - A magnifying glass is drawn in a corner of the table. The player drags it by its ring or handle; its glass shows the table 2.5 times bigger, and it stays where it is left. A click through the glass reaches the object below.
  - Objects can be dragged: press and move to lift an object and put it somewhere else (it goes on top of the others), for example to uncover what is under a napkin. Dragging is free; only a press without moving checks the object. Moved objects stay where they were put while the page is open.
  - The signs of the 3D scene (door plaques, name tags) never show over the close-up.

## Why

As a player, I want finding the USB stick to be a real search that needs attention, so that the first clue feels earned and the game is harder.

## What

- [ ] `prototypes/campus-3d/campus_search.py` (server only): `SPOTS` are the kinds of objects on the table plus `usb_stick`; `PEN_SPOT = "usb_stick"`; `SEARCH_TEXT` has one "nothing" text for each wrong kind and a new "found" text, in both languages.
- [ ] `prototypes/campus-3d/campus_text.py`: `spots` has a label for each kind (shown next to ✗ after a wrong click, and for the stick after it is found); new texts `table_open`, `table_title`, `table_hint` (only "find the stick"), `table_close` and `table_lens` (the tooltip of the magnifier); `search_title` and `search_hint` are removed, in both languages.
- [ ] New file `prototypes/campus-3d/table.js`: the drawing of the close-up (the list of objects, where each one is, and how it is drawn as SVG) and the window that shows it, with the magnifier (a copy of the drawing, 2.5 times bigger, cut in a circle; only its ring and handle take the mouse) and the dragging of objects (a press without moving is a click). It only draws and reports which kind was clicked; it knows nothing about the rules.
- [ ] `prototypes/campus-3d/play.js`: the side panel of the study room shows only the "Ver a mesa" button (3D and text mode), with no title or hint, instead of the list of places; `window.campusOpenTable()` opens the close-up (only inside the study room, before the stick is found); a click on an object calls `window.campusSearch(kind)`, which asks the server as before, takes 1 minute for a wrong kind and tells the close-up the result.
- [ ] `prototypes/campus-3d/game3d.html`: the layer of the 3D signs gets `z-index: 1`, so the signs stay under the windows. The table of the study room gets much more clutter and is the only thing that can be clicked to search; clicking it opens the close-up. The drawer and the coat become scenery; the backpack, the books, the papers on the floor and the bin are removed.
- [ ] `prototypes/campus-3d/page3d.py`, `server3d.py` and `app_3d.py`: `table.js` is put in the page (inline for Streamlit, `/table.js` for the local server) and counts for the page version.
- [ ] `prototypes/campus-3d/play.css`: the close-up window over the game, with the drawing as large as the screen allows.

## Limits

Like the old search, this is a puzzle, not security: the drawing must be in the page, so someone reading the page's source can find which object is the stick. The texts of what each object is, and the "found" text, stay on the server. Which kinds were already checked is remembered only while the page is open.

## Out of scope

The code of computer 12, Rita's lines, other hidden objects, the plain game.

## Done when

- [ ] Existing tests pass unchanged (including `tests/test_pen_and_code.py`, which works with any list of places).
- [ ] `tests/test_hidden_object_table.py`: `PEN_SPOT` is `usb_stick`; the old places are gone; every kind has a label in both languages; every kind is drawn at least once in `table.js` and nothing else is drawn as clickable; the stick is drawn exactly once; no kind is made to look like the stick; the page carries `table.js` inline and the local server serves `/table.js`; the side panel uses `table_open`, has no title or hint and no longer lists the places; the close-up's hint does not mention the cost; the magnifier is a picture with a ring and a handle, and its glass lets clicks through; objects can be dragged and a drag is not a click; the 3D signs have their own layer; the floor of the study room is clear; the 3D scene has only the table to click.
- [ ] `tests/continuous-conversations.cjs` still passes.
- [ ] In the browser: the table looks messy in 3D; clicking it (or the button) opens the close-up; dragging the magnifier shows the table bigger under it; dragging an object moves it without costing time; no door plaque shows over the close-up; a wrong object costs 1 minute and is marked; the stick gives the USB stick and the close-up closes; no text says where the stick is.
