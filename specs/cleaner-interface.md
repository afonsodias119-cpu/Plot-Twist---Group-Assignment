# A cleaner and more intuitive interface

Only the 3D game changes. No change to `story.py`, `logic.py`, `db.py`, `game.py`, `app.py` or any reviewed test; the server still sends everything it sent before (clue rooms, trust), the screen just shows less.

## Before writing the spec

- **Product and user:** a player of the 3D game, from the case file to the end of the night.
- **Trigger:** the player reads the case file, looks at the top bar, opens the clue list on the phone, and talks to people.
- **Before:**
  1. The case file says "O teu grupo (são só quatro)" / "Your group (only four of you)", although the four name chips are right below it.
  2. The top bar has a row of emoji buttons: ℹ️ (How it was made), 🗣️/🤐 (voices), 🔦/🌑 (torch), 🔊/🔇 (sound) and "📱 Phone". They look unprofessional and the player has to guess what each one does.
  3. The phone's clue list ("Clues to collect") says where each clue is ("Where: Print shop"), which makes the game too easy.
  4. Conversations show trust hearts (♥♥♡) next to the person's name, like lives in a game.
  5. The case file's text appears letter by letter; the only way to see it all at once is to click it.
- **Rule:** say things once, use words instead of emojis, and do not give away where the clues are.
- **After:**
  1. The case file says "O teu grupo" / "Your group".
  2. The top bar has two buttons with words: "Telemóvel" / "Phone" and "Menu". The menu opens a short list: How it was made, voices, torch and sound, each saying how it is now ("Vozes ligadas", "Torch off (F)").
  3. The clue list shows only what to collect, not where.
  4. No hearts: the player reads the mood in what the person says.
  5. Backspace also shows the whole text at once.

## Why

As a player, I want the screens to be clear and look finished, and I want to find the clues myself, so that the game feels like an investigation and not like a checklist.

## What

- [ ] `prototypes/campus-3d/page3d.py`: `group_label` is "O teu grupo" / "Your group"; `skip` mentions Backspace ("Clica no texto ou carrega em Backspace para ler tudo" / "Click the text or press Backspace to read it all").
- [ ] `prototypes/campus-3d/game3d.html`: on the case file, Backspace calls `finish()` while the text is still being typed.
- [ ] `prototypes/campus-3d/campus_text.py`: new text `menu` ("Menu"); the unused `todo_where` and `trust` are removed.
- [ ] `prototypes/campus-3d/play.js`, top bar: the phone button shows only `t.phone` (no 📱). A new button `menu-toggle` (text `t.menu`, `aria-expanded`) opens and closes `menu-list`, which holds `howto-open`, `voice-toggle`, `torch-toggle` and `sound-toggle` (same ids, so the keys and the code that uses them keep working). The items show `t.howto_open`, `t.voice_on`/`t.voice_off`, `t.torch_on`/`t.torch_off`, `t.sound_on`/`t.sound_off`. The menu closes on a click outside it, on Escape, or when How it was made opens.
- [ ] `play.js`, phone: the clue list shows each clue's label and whether it is done, without its room.
- [ ] `play.js`, conversations: no `talk-trust` element and no hearts. The server's `trust` and the end of the talk at trust 0 do not change.
- [ ] `prototypes/campus-3d/play.css`: the menu is a small dark box under its button (on a narrow screen it opens to the right); the old `icon-btn` and trust styles are removed.

## Out of scope

The emojis in other places (the "🕵️" chip of the player on the case file, the arrows of the movement hint, the 📱 of a new message notice), renaming the clerk's id `amelia`, the key to talk (it stays K), the plain game.

## Done when

- [ ] Existing tests pass unchanged.
- [ ] `tests/test_cleaner_interface.py`: the group label has no "quatro"/"four"; `menu` exists in both languages; the top bar markup and the labels of its buttons have no emojis; the four tools are inside `menu-list`; the menu closes on a click outside and on Escape; the clue list does not show the room; there are no hearts; Backspace finishes the typed text and the hint says so.
- [ ] `tests/continuous-conversations.cjs` still passes.
- [ ] In the browser: the case file shows "O teu grupo" and Backspace shows the whole text; the top bar shows "Telemóvel" and "Menu", the menu works and closes on a click outside; the phone's clue list has no rooms; conversations have no hearts.
