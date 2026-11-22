# Phone controls, a detective card and a QR code

Extends specs/rules-and-character.md. Only the 3D game's screen changes. No change to `story.py`, `logic.py`, `db.py`, `game.py`, `app.py`, the server or any reviewed test.

## Why
1. Today the detective only walks with the keyboard, so somebody who opens the link on a phone (a teacher, a classmate) cannot move.
2. The share card is text. With the character creator the player has a detective of their own, and nothing to keep of it.
3. In a live demo the class cannot open the game: the link has to be typed.

## What
1. **Where are you playing?** The first screen asks "Computer" or "Phone", under the name and above the character creator. A touch screen (`(pointer: coarse)`) pre-selects "Phone"; otherwise "Computer". The answer is remembered in this browser (`plot-twist-device`) and can be switched later in the menu ("Joystick", with a dot that is lit in phone mode).
2. **The joystick.** In phone mode an on-screen joystick (bottom left, over the 3D picture) moves the detective in any direction, with a small dead zone, and stops when the finger is lifted. On a computer it is never shown. It is hidden while a conversation, the group chat, the ending, the time-up card or the text mode is on screen. A phone starts the game with the side panel closed so the picture fills the screen (the arrow still opens it; on a narrow screen the joystick is hidden while the panel is open). The 3D loop reads `window.campusStick` like it reads the keys, so the server is not involved. Talking and using things stay "tap the note" (the note that says "Press K") and every window has a close button.
3. **Detective card.** The ending screen has a button "Detective card". It opens a window with a 720×1040 picture and a "Download image" button (and says to press or right-click the image if the download does not start). The picture is drawn in the browser (a canvas) and has: the case, the title, the detective (a 3D picture of the player's own look, drawn once in a small scene, `campusPortrait`), the name, the ending's stamp and title, the clues, the time left and the endings found, and the address of the game, in the colour of the ending.
4. **QR code.** A menu item and a button on the first screen, "QR code", open a window with the QR code of the published link (`app_url`, the same as in the README) and the link. The code is drawn on a canvas by the small `qrcode-generator@1.4.4` library from cdnjs (pinned, loaded only when the window opens); if it cannot be loaded the window shows the address instead.

## Out of scope
Saving the card or the look on the server, a gamepad, sharing straight to other apps, changing the puzzles for touch (they already use pointer events), the plain game.

## Done when
- Existing tests pass unchanged.
- New tests (`tests/test_touch_card_qr.py`): the texts exist in both languages; the QR link is the one in the README; the joystick is hidden by default and shown only in phone mode; a touch screen pre-selects the phone and the choice is remembered; the joystick has a dead zone and stops on release; a phone starts with the panel closed; the rules mention it; the QR library is pinned and has a fallback; the card is built in the browser and never sent.
- A browser check shows: on a computer no joystick, and the menu switch; on an emulated phone the phone pre-selected, the joystick moving the character and stopping; the QR code drawn; the detective card with the player's look and a real download.
