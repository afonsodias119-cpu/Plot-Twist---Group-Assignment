# Sounds that tell you things: footsteps, the shutter, a buzz for each message

Extends specs/night-schedule.md (which left "sounds for the rounds" out of scope), specs/flashlight-voices-howto.md and specs/rules-and-character.md (one Sound button for music, effects and voices). Only `play.js` changes. No change to the server, `story.py`, `logic.py`, `game.py`, `app.py`, `db.py` or any reviewed test. No new file, no sound file: everything is made with Web Audio inside the existing `sound` module of `play.js`, like the sea, the music and the footsteps of the detective.

## Why
The night already has events the player can miss while reading: Duarte walking to the lab door before a round, the clerk going home, a new message from the unknown number. A sound tells the player something happened without another note on the screen, and it rewards the player who listens.

## What
1. **Duarte's footsteps.** When a snapshot's `night.duarte` becomes `"lab_door"` (it was `"auditorium"` in the snapshot before, specs/night-schedule.md, point 10) and the saved room is the computer lab (the lab or the group chat), the page plays footsteps that come closer: 8 steps, 0.42 s apart, louder from step to step. When it goes back to `"auditorium"` while the player is still in the lab, the same steps go away (softer from step to step). Outside the lab nothing is heard: the warning of the unknown number already speaks for the other rooms. When Tomás stands in the door (specs/evidence-and-hearing.md) the steps still come and go: Duarte walks on.
2. **Leonor leaving.** When `night.gone` gains `"leonor"` and the saved room is the library, a chair scrape (a short low noise) and her steps going away.
3. **The shutter.** When `night.gone` gains `"amelia"` (22:25), a metal shutter rolls down: about 1.4 s of rattle and a thump at the end. Full volume in the print shop, softer (0.4) in any other room: it is heard down the corridor.
4. **A buzz for each new message.** `checkNotices` buzzes once for every message it adds to the phone, 0.7 s apart, at most three buzzes for one snapshot (today it buzzes once however many arrive). The banner still shows only the newest.
5. **When a cue plays.** `render` keeps the snapshot it replaces and calls `soundCues(before, state, operation)` after drawing. No cue when there is no snapshot before, when it belonged to another player, after `open`, `begin` and `restart` (a reload at 22:40 must not replay the shutter), and when the new snapshot has an ending.
6. **How they are made**, inside `sound` (new functions beside `step`, `buzz` and `chime`; the existing ones are not edited):
   - `thump(volume, filtered)`: a triangle wave falling from 90 to 45 Hz in 0.1 s; for steps heard through a wall, through a low-pass filter at 600 Hz.
   - `footsteps(coming)`: 8 `thump`s with `setTimeout`, volume from 0.015 to 0.08 when `coming`, the other way round when not.
   - `noise(seconds, from, to, volume)`: a short buffer of random samples (as the sea is made) through a band-pass filter whose frequency slides `from` → `to`; the shutter is `noise(1.4, 2200, 700, 0.06 * level)` with the gain shaken by a 14 Hz oscillator, then a `thump`; the chair is `noise(0.25, 400, 200, 0.05)`.
   - Each new function starts with `if (!ctx || muted) return;`, like `tone` and `step`, so the Sound button silences them, and the steps already scheduled check it again before each step (turning the sound off in the middle stops them). Nothing plays before the first click of the page (the browser's own rule; `sound.start` already waits for it).
7. **The Rules** say nothing new: the Sound item already says the button turns the sound on and off.

## Reviewed tests that change
None. The lines the reviewed tests pin are not edited (`AudioContext`, `sound.isMuted()`, the `sound-toggle` handler, `campusMoving`); `sound.buzz` keeps its body and is called more often.

## Limits
- The footsteps follow the server's minute, which the page reports only at the marks (specs/night-schedule.md, point 4): they start when the minute before a round is reported, not at a second of the countdown.
- Sounds are page code: they need the browser check. The tests can only read the source.
- Some phones play nothing until the player has touched the screen once; the first tap on "Accept the case" does it.

## Out of scope
Sound files, footsteps of the clerk or the professor, a sound for every story action, music changes, the plain game.

## Done when
- Existing tests pass unchanged, and `tests/continuous-conversations.cjs`; `play.js` passes `--check`.
- The tests below were written first and pass.
- A browser check with sound on, at a scratch database (reports by hand with the operation `time`): footsteps at 22:26 in the lab and away at 22:28, the shutter at 22:25 in the print shop and softer in the study room, Leonor's chair at 22:30 in the library, three buzzes when three messages arrive; with sound off, none of them.

## Checks
`tests/test_sounds_that_tell.py`, written before the code. It reads the source of `play.js`, as tests/test_harder_campus.py does.
- `test_the_sound_module_has_the_new_sounds`: `function thump(`, `function footsteps(`, `function noise(`, `shutter`, `chair` inside the `sound` module (between `const sound = (() => {` and its `})();`).
- `test_every_new_sound_follows_the_sound_button`: each of the new functions has `if (!ctx || muted) return;` as its first line, and the steps check `muted` again inside the `setTimeout`.
- `test_render_plays_cues_only_between_two_snapshots_of_one_night`: `function soundCues(` exists, is called from `render`, and returns early for `open`, `begin`, `restart`, an ending and a missing `before`.
- `test_the_cues_read_the_server_schedule`: `soundCues` reads `night.duarte`, `"lab_door"`, `night.gone`, `"amelia"` and `"leonor"`.
- `test_one_buzz_for_each_new_message_at_most_three`: `checkNotices` calls the buzz with `Math.min(due.length, 3)`.
- `test_no_new_sound_file_and_no_new_script`: no `.mp3`, `.wav`, `.ogg` or `new Audio(` in `play.js`; `page3d.py` still puts exactly `table.js`, `photo.js` and `play.js` in the page.
- `test_the_pinned_sound_lines_are_still_there`: `AudioContext`, `sound.isMuted()`, `campusMoving` and the `sound-toggle` handler of `tests/test_rules_and_character.py`.
