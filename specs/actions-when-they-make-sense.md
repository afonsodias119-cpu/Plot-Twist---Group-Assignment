# Conversation actions appear when they make sense

> **Update (specs/calendar-code.md):** the cover photo is now dated Saturday 17 October, so the code of computer 12 is `1710`, the photo's stamp says 17.10 and the slip on the shutter says 17 October. The clerk's `order` line no longer says the date.

Extends specs/campus-people-and-atmosphere.md (story actions inside the conversation) and follows the same idea as specs/pen-and-code.md item 3 (the server offers an action, the screen leaves it out). Only the 3D game changes. No change to `story.py`, `logic.py`, `db.py`, `game.py`, `app.py` or any reviewed test; the plain game (`app.py`) plays as before.

## Before writing the spec

- **Product and user:** a player of the 3D game who talks to Leonor in the library or to the clerk at the print shop.
- **Trigger:** the player opens one of these conversations.
- **Before:**
  - Leonor: the two yellow decisions ("▶ Show the photo and quietly ask for help" and "▶ Show the photo and accuse her of helping Duarte") are there from the first line, even without the photo. Clicking one only gets Leonor's refusal ("Do you have any proof otherwise?"), because both need `original_photo`. With the photo, they appear next to her normal questions.
  - Clerk: "▶ Ask for a copy of the original order" is there from the first line, before the player knows an original order exists.
- **Rule:** a story action appears in a conversation only when the player could think of it, and it looks like any other answer.
- **After:**
  - Leonor: without the photo, only her normal answers. With the photo, only the two decisions: it is the moment of the choice.
  - Clerk: the copy appears only after she mentions the original order file (her answer to "Ask about the cover photo order").

## Why

The actions talk about things the player does not have or know yet, so they give away the solution and make the conversation look like a menu. Next to Leonor's decisions, the normal questions make the choice look like one more question. As a player, I want an action to appear when the story has given me a reason for it, so that each clue feels like it opens something new.

## What

### Leonor's decisions
- [ ] In `prototypes/campus-3d/play.js`, `showLine` leaves out every action that is a decision (`action.decision`) and is not allowed (`!action.allowed`). Today the only decisions are Leonor's `ask_for_help` and `accuse`.
- [ ] When at least one decision is allowed, `showLine` offers no normal answers (for Leonor: "Ask if she is sure…", "Tell her you have doubts", "Say she is lying"), only the decisions. "End conversation" in the header still works. After the choice the decisions are no longer offered (`colleague_choice` is not `none`), so the normal answers come back.

### The clerk's copy
- [ ] `showLine` leaves out `request_copy` until the player has chosen the clerk's `order` question in the open conversation (`asked` has `"order"`). From then on, it stays until the conversation is closed.
- [ ] The clerk's questions do not change: her answer to `order` gives the date 14 November, half of the code of computer 12 (specs/pen-and-code.md item 5).

### They look like the other answers
- [ ] Every action inside a conversation (Leonor, the clerk, computer 12, the professor) is drawn like a normal answer: same grey bubble (`answer` class), no "▶", no yellow, no "This decision is remembered…" note. They come after the questions. This replaces "Mark irreversible dialogue decisions" of specs/playable-campus-3d.md for the conversation (team decision, 22/11/2026); the side panel does not change.
- [ ] In `play.css`, the box of the actions (`.talk-actions`) uses `display: contents`, so its buttons line up with the other answers; the old yellow row styles are removed.

### Both
- [ ] Other actions do not change: a blocked one is still shown and explained when clicked (specs/base-game.md, decision 3).
- [ ] The server does not change: it still offers the actions, with `allowed` and `blocked_text` (the reviewed test `test_blocked_actions_are_still_offered_with_their_reason_and_change_nothing` keeps passing).
- [ ] The text mode (when the 3D cannot load) uses the same conversation, so it behaves the same.

## Limits

Leonor's refusal line (`blocked_text`) is no longer reached from the 3D screen. The clerk's line and the photo itself still lead the player to Leonor.

A player who brings the photo the first time they talk to Leonor never hears her normal lines: the diary note about the messages arriving last night from an unknown number, and the rude answers that cost 5 minutes. The team accepted this (22/11/2026): Rita gives a similar hint about arrival times after the files are viewed.

The clerk's copy is remembered only inside the open conversation: a player who closes it and talks to her again asks about the order again (one click) before the copy appears.

## Out of scope

Other people's actions, changing any line, the plain game.

## Done when

- [ ] Existing tests pass unchanged.
- [ ] `tests/test_actions_when_they_make_sense.py`: without the photo the server still offers both decisions, not allowed and marked as decisions; with the photo they are allowed; `showLine` in `play.js` skips decisions that are not allowed, offers no answers while a decision is allowed, skips `request_copy` until `order` was asked, and draws the actions as answers after the questions.
- [ ] `tests/continuous-conversations.cjs` (needs Node): Leonor shows no decision and her answers when they are not allowed, and both decisions and no answers when they are; the clerk shows no copy at the start and shows it after `order`.
- [ ] In the browser: talk to Leonor without the photo (no yellow buttons, her normal answers); at the print shop, the copy appears only after asking about the order; talk to Leonor again with the photo (only the two yellow buttons).
