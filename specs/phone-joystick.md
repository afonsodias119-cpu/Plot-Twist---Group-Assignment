# Phone controls: an on-screen joystick on touch screens, and touch buttons for the keys

Extends specs/playable-campus-3d.md (walking with WASD), specs/campus-people-and-atmosphere.md (walking up to a person and pressing K), specs/cleaner-interface.md and specs/hidden-object-table.md (the table already works with a finger). Only the page changes: `game3d.html`, `play.js`, `play.css` and one text of `page3d.py`. No change to the server, `story.py`, `logic.py`, `game.py`, `app.py`, `db.py` or any reviewed test. On a computer nothing changes. Texts in design-notes/texts-ideas.md, part G.

## Why
The public link is shared in chats, so many people open it on a phone. There the detective cannot move at all: walking needs the arrows or WASD, and talking needs K. The table, the torn photo and every card already work with a finger; only walking is missing.

## What
1. **Only on touch screens.** `game3d.html` decides once, at load: `const TOUCH = window.matchMedia("(pointer: coarse)").matches;` (a phone or tablet whose main pointer is a finger; a laptop with a touch screen keeps its mouse and is unchanged). When `TOUCH` is false nothing below is created, and the CSS rules are inside `@media (pointer: coarse)`, so the desktop page is exactly as before.
2. **The joystick drives the same movement as WASD.** In section 8 of `game3d.html`, after the `KEYMAP` lines (which are not edited), `makeStick()` adds `<div id="stick" class="stick"><div class="stick-knob"></div></div>` inside `#wrap`. A finger on the circle is captured (`setPointerCapture`); its distance from the centre, divided by the radius (48 px) and kept at most 1, is `x` and `y`. It sets the very same `keys` object the keyboard sets: `keys.left = x < -0.35`, `keys.right = x > 0.35`, `keys.up = y < -0.35`, `keys.down = y > 0.35`, so the loop, the speed, the walls, the doors and the footsteps are the ones of the keyboard (eight directions, like two keys at once). Inside 0.25 of the radius nothing is pressed. Lifting the finger (`pointerup`, `pointercancel`) releases all four and puts the knob back in the middle. It presses nothing while `window.playing` is false or the game is busy or ended, the same rule as the `keydown` line; the loop stops the character in those cases anyway.
3. **Layout.** The circle is 104 px with a 44 px knob, 16 px from the left and the bottom of the 3D picture, half transparent, with `touch-action: none` so dragging never scrolls the page. It is shown after "start-game", hidden in the text mode (no 3D), and stays under every card and window (a lower `z-index` than the conversation, the phone, the table and the photo), so an open card covers it. At phone width (650 px and below) the 3D picture is the top 30% of the screen while the panel is open, and the whole screen when it is hidden; the stick is in its bottom left corner in both, and the note and the buttons over the picture (`.hud-bottom`) start right of it (`left: calc(50% + 60px); width: calc(100% - 144px)` under `@media (pointer: coarse) and (max-width: 650px)`).
4. **The keys as touch buttons.** Every key has a button on a touch screen:
   | key | on a touch screen |
   |---|---|
   | arrows / WASD | the joystick |
   | K (talk, use, look) | the near note (`#near-hint`), which is already a button: on a touch screen it reads "Talk to Rita" (`tap_talk`), "Use computer 12" (`tap_use`), "Look: Price list" (`tap_look`, specs/more-to-find.md) with no `K` key drawn, is at least 48 px high, and a tap does what K does |
   | F (torch) | Menu → Torch, as today |
   | Esc | the Close button of every card, as today |
   | Backspace (case file) | a tap on the text, as today |
   | Enter (name) | "Accept the case", as today |
5. **Words that mention keys.** On a touch screen the 3D hint `#help` shows `help_touch` (in `page3d.EXTRA`, both languages, and passed in `language_data`'s `ui` beside `help`) instead of the arrows and WASD; the panel's `controls` line shows `controls_touch`; the Rules window adds `rules_touch` as one more line under its points (its nine points and their words, pinned by tests/test_rules_and_character.py, are not changed).
6. **Nothing else moves.** The table close-up, the torn photo and the cards keep their own pointer code; the phone's buttons and the menu are already buttons.

## Reviewed tests that change
None. `KEYMAP` and the two `keydown`/`keyup` lines are not edited; `press_talk` keeps `{name}` and `K` (`tests/test_campus_3d.py:383`); `id="near-hint"`, `campus-near` and `campusNear` stay; the Rules keep their nine points.

## Limits
- Touch is detected once, at load: a tablet with a mouse plugged in later keeps the joystick until a reload.
- The stick has eight directions, not a smooth angle: it is the keyboard's movement.
- The 3D on an old phone may be slow; the text mode (the panel and its buttons) works on any phone.

## Out of scope
Swiping the camera, a gamepad, vibration, a separate phone layout for the cards, the plain game.

## Done when
- Existing tests pass unchanged, and `tests/continuous-conversations.cjs`; `play.js` passes `--check` and the module script of `game3d.html` is checked by hand in the browser console.
- The tests below were written first and pass.
- A browser check with the mobile preset (375 × 812, a touch phone): the stick walks into a room and through a refused door, the near note says "Talk to Rita" and a tap opens the talk, the panel open and hidden, the text mode; then the desktop preset: no stick, the same page as before.

## Checks
`tests/test_phone_joystick.py`, written before the code. It reads `game3d.html`, `play.js` and `play.css`.
- `test_touch_is_detected_by_the_pointer`: `game3d.html` has `matchMedia("(pointer: coarse)")` and creates the stick only inside `if (TOUCH)`.
- `test_the_stick_presses_the_keyboards_keys`: `function makeStick(` sets `keys.up`, `keys.down`, `keys.left` and `keys.right` and releases them on `pointerup` and `pointercancel`.
- `test_the_keyboard_lines_are_untouched`: the `KEYMAP` line and its `keydown` and `keyup` lines are still in `game3d.html` exactly as before.
- `test_the_stick_never_scrolls_and_stays_under_the_cards`: `play.css` or `game3d.html` has `touch-action: none` for `.stick`, and the stick's `z-index` is lower than `.talk-card`'s.
- `test_the_phone_layout_keeps_the_stick_free`: `play.css` has `@media (pointer: coarse) and (max-width: 650px)` with a rule for `.hud-bottom`.
- `test_the_near_note_says_what_a_tap_does`: `play.js` uses `tap_talk`, `tap_use` and `tap_look` when touch is detected; `press_talk` is still used otherwise.
- `test_the_touch_texts_exist_in_both_languages`: `tap_talk`, `tap_use`, `tap_look` with `{name}`, `controls_touch`, `rules_touch` in `campus_text.TEXT`, `help_touch` in `page3d.EXTRA`, none mentioning WASD or K.
- `test_desktop_rules_are_only_inside_the_coarse_media_query`: every `.stick` rule of the CSS is inside `@media (pointer: coarse)`.
