# The name is checked where it is typed

Extends specs/creator-after-name.md (the start screen in steps). Only `prototypes/campus-3d/play.js`, `game3d.html` and `campus_text.py` change. The server still checks every name (`game.clean_name`); this only tells the player sooner. No reviewed test changes.

## Before writing the spec

- **Product and user:** a player on the first screen of the 3D game.
- **Trigger:** "Next" on the case file with a name like `<script>!!` or `Ana.`.
- **Before:** the page moves on to the detective and the warning; only "Start / Continue", two steps later, shows "Use 1 to 20 characters…", far from the name field. Also, if the player starts typing the name while the case text is still being typed out, the end of the text moves the focus to "Next" in the middle of the name.
- **Rule:** an error is shown where it can be fixed (course rubric, interface: "results and errors are clearly shown").
- **After:** "Next" stays on the case file and shows the rule under the name field, which keeps the focus. The focus only moves to "Next" when the player is not typing in a field.

## Why

As a player, I want to know at once that my name cannot be used, next to the field where I can change it.

## What

1. `play.js`, `window.campusNext`: after the existing empty-name check, a name (trimmed) that does not match `^[\p{L}\p{N}_ -]{1,20}$` (the page's copy of `game.NAME_PATTERN`) shows `ui().name_invalid` in `startError` and focuses the field.
2. `campus_text.TEXT`, both languages, `name_invalid`: the same words as `story.UI_TEXTS[...]["invalid_name"]`.
3. `game3d.html`, `finish()` of the typewriter: the focus moves to "Next" only when the focused element is not an `input`.

## Out of scope

The server's rules for names, the plain game.

## Done when

- [ ] Existing tests pass unchanged.
- [ ] `tests/test_name_check_first_step.py`: the check in `campusNext` after the empty-name line, the pattern, the texts equal to `invalid_name`, and the focus rule in `finish()`.
- [ ] In the browser: `<script>!!` stays on the case file with the message under the field; `Ana Lú` moves on; typing during the typewriter keeps the focus in the field.
