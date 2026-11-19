# Campus visuals: arriving outside, the hallway and a cinematic look

**Blocked by:** scene images and mystery theme (`specs/scene-images.md`, merged). The new image prompts go in `docs/imagens.md`.

Phase D extra 2 of 2 on design. It changes only how the game looks. The rules (`logic.py`), the endings, the saved games (`db.py`) and every existing test stay exactly as they are.

## Before writing the spec

- **Product and user:** a player of "O quinto elemento" who should feel they are walking into a seaside university campus at night, not reading a list of buttons.
- **Trigger:** the Start screen is drawn, the player presses Play, or the study room is drawn.
- **Before:** the Start screen shows the cover photo, Play goes straight to the study room, and the study room lists four plain "Go to …" buttons.
- **Rule:** every picture is optional. A missing file draws nothing (or the fallback named below) and never an error. Doors are still the story's own actions: clicking one calls `game.play` with the same action id as today.
- **After:** the Start screen shows the campus at night, Play shows a short "entering the building" moment above the study room, the study room shows a hallway of door cards with a thumbnail, a name and a teaser, and the whole app has a cinematic dark and amber style.

## Why

As a player, I want to arrive at the building and walk down its hallway, so that the mystery feels like a real place. As a team, we want the design criterion to be clearly met without touching the rules, so the reviewed tests still prove the game works.

## What

### 0. Two phases: a preview first

The team wants to try the new look before it touches the real game. So:

- **Phase 1 (this branch):** everything is built in **new files**. `app.py`, `story.py`, `logic.py`, `db.py`, `game.py` and the existing tests are not changed at all. The preview runs next to the real game:
  `uv run streamlit run app_campus.py --server.port 8502`
- **Phase 2 (only after the team approves, in a later pull request):** `app_campus.py` replaces `app.py`, the texts of `campus_texts.py` move into `story.py`, and the import block at the top of `tests/test_campus_visuals.py` is deleted (the moved tests then check `app.py` directly).

### 1. Files

| File | Job |
|---|---|
| `app_campus.py` (new) | A copy of `app.py` with the new look: loads `style.css`, draws the Start picture, the entering moment, the hallway and the item cards. Same buttons, same keys, same calls to `game.py`. |
| `campus_texts.py` (new) | Data only: `TEASERS` (one short text per scene) and `CAMPUS_UI` (`hallway`, `entering`), in `en` and `pt`. |
| `style.css` (new) | All the custom CSS, in one file. |
| `assets/campus_exterior.jpg` (new, optional) | The campus at night, seen from outside. Start screen. |
| `assets/entrance_hall.jpg` (new, optional) | The entrance hall, seen just inside the glass doors. Entering moment. |
| `docs/imagens.md` | New style block, character sheets and prompts for all 12 pictures. |

`app.py`, `story.py`, `logic.py`, `db.py`, `game.py`, `pyproject.toml`, `uv.lock` and the existing tests do not change. The preview uses the same database, so a game started in one app continues in the other.

### 2. Start screen: arriving outside

- Shows `campus_exterior` under the title. If that file is missing, it shows `cover` as today. Never both.
- `show_image(name)` returns `True` when it drew a picture and `False` otherwise, so the fallback reads `show_image("campus_exterior") or show_image("cover")`.

### 3. The entering moment

- When Play succeeds (a new game or a continued one), `start_game` in `app_campus.py` sets `st.session_state["entering"] = True`.
- On the next run of the game screen, the app draws one HTML block with the `entering` text (for example "You push the glass door. The hall is silent, the sea is still behind you.") over the `entrance_hall` picture, then sets `"entering"` back to `False`. The text is `CAMPUS_UI[language]["entering"]`. The block is drawn only on that one run.
- CSS makes the block fade in, hold and fade out by itself in about 4 seconds. It never blocks clicks (`pointer-events: none`), and with "reduce motion" turned on it is shown and hidden without fading or moving.
- The picture goes into the HTML as a data URL (`data:image/jpeg;base64,…`), because HTML cannot read files from `assets/`. Without the picture, the block is the text on a dark background.
- The block uses no `st.header`, no `st.image` and no message box, so the screen still starts with the scene title, the image count and the message boxes are the same as today.

### 4. The hallway (doors)

- In any scene, an action with `go_to` is drawn as a **door card**, **except** an action that goes to the starting scene (`story["start"]["scene"]`). Those "Back to the study room" actions stay plain buttons. In practice the hallway appears only in the study room.
- The cards come under the `CAMPUS_UI` `hallway` subheading, in a row of columns (they stack on a phone). Each card is a `st.container(border=True, key="door_<scene id>")`, and contains:
  1. the thumbnail of the room it leads to (`image_file(<go_to scene id>)`, drawn only if it exists);
  2. the room name (the title of the `go_to` scene), with `🔒` in front when the action is not `allowed`;
  3. the room's teaser, `TEASERS[language][<scene id>]`, as a small caption;
  4. a button with the action's label and the same key as today, `action_<action id>`, calling `take_action`.
- A locked door is still clickable: `game.play` refuses it and the existing `blocked_text` appears in the warning box, exactly as now.
- Other actions (for example "Open the group drawer") stay plain buttons above the hallway.

### 5. Look (`style.css`)

Loaded once per run with `st.markdown("<style>…</style>", unsafe_allow_html=True)`. It only styles, and it never hides content:

- titles in a serif font from the computer itself (`Georgia, "Times New Roman", serif`), no web fonts, so no external request;
- a dark vignette and rounded corners on scene pictures;
- door cards that look like doors along a corridor (amber frame, light on hover) and a dimmed look for locked ones;
- message boxes with an amber left edge;
- inventory items as small cards (`st.container(border=True, key="item_<item id>")`).

Body text stays off-white on navy, as `.streamlit/config.toml` already sets.

### 6. Pictures (`docs/imagens.md`)

- One photorealistic, cinematic style block for all pictures: night, warm amber interior light, cool blue exterior, 35 mm film look, no text anywhere.
- A character sheet for the four people who appear (Leonor, Duarte, the professor and the print-shop clerk), pasted unchanged into every prompt where they appear, so they look the same in every picture.
- Prompts for the 12 files: the 10 existing ones plus `campus_exterior` and `entrance_hall`. The room thumbnails are the room pictures themselves, so there are no extra files.
- The same sizes and limits as `specs/scene-images.md`: 1280 × 720 (items 512 × 512), JPG, under 300 KB each.

## Checklist (one line, one test) — `tests/test_campus_visuals.py`

An automatic fixture in this file points the helpers of `tests/test_smoke.py` (`open_app`, `start_game`, `click`) at `app_campus.py`. The `assets` fixture comes from `tests/test_images.py`.

- [ ] **The preview passes every existing screen test.** The file imports the screen tests of `tests/test_smoke.py` and `tests/test_images.py`, so pytest runs them a second time, this time on `app_campus.py`. They are imported, not copied or edited.

- [ ] `test_start_screen_shows_the_exterior_instead_of_the_cover` — with `campus_exterior.jpg` only: 1 image. With `campus_exterior.jpg` and `cover.jpg`: still 1 image. With neither: 0.
- [ ] `test_play_shows_the_entering_moment_once` — after Play, the `entering` text is on the screen once and the first header is still the study room title; after the next click it is gone.
- [ ] `test_entering_moment_after_continuing_a_game` — the same name played again also shows the `entering` text, in the saved language.
- [ ] `test_invalid_name_shows_no_entering_moment` — Play with `"<b>"` keeps the Start screen and shows no `entering` text.
- [ ] `test_study_room_shows_one_door_per_room` — with the four room pictures and `study_room.jpg`: 5 images in the study room; the buttons `action_go_print_shop`, `action_go_library`, `action_go_computer_lab` and `action_go_auditorium` are there; `action_open_drawer` is still there.
- [ ] `test_back_to_the_study_room_stays_a_button` — in the library with `study_room.jpg` and `library.jpg`: 1 image (no thumbnail of the study room).
- [ ] `test_locked_door_shows_a_padlock_until_it_opens` — at the start the text `🔒 Auditorium` is on the screen and clicking `action_go_auditorium` shows its `blocked_text`; after viewing the files the padlock is gone and the click opens the auditorium.
- [ ] `test_every_scene_has_a_teaser_in_both_languages` — `TEASERS` and `CAMPUS_UI` have the same keys in `en` and `pt`, every scene id of the story is in `TEASERS`, every text is non-empty, and each door shows its teaser.
- [ ] `test_style_file_is_loaded_on_every_screen` — `style.css` exists, and the Start, Scene and Ending screens each contain the CSS once.

## Out of scope

- A 3D map, walking with the keyboard, or any JavaScript.
- New scenes, new actions, a new starting scene or any change to what is saved.
- Sounds, music, a typewriter effect, web fonts and new libraries.
- Different pictures per game state (for example the drawer open).

## Done when

- `uv run pytest` is green: the existing tests unchanged, passing on `app.py` and again on `app_campus.py`, and the new checklist tests written and reviewed before the code.
- `git diff main -- app.py story.py logic.py db.py game.py tests/test_smoke.py tests/test_images.py tests/test_base_game.py` is empty.
- With no new pictures at all, the game looks as today plus the hallway, the entering text and the CSS, and nothing breaks.
- By clicking, in both languages: the Start screen, the entering moment, the hallway with a padlock on the auditorium, both endings, and readable text everywhere, also on a phone-width window.
- `docs/imagens.md` has the new style block, the character sheets and 12 prompts.
- `pyproject.toml` and `uv.lock` are unchanged.
- The work is on the branch `campus-visuals`, pushed, and reviewed by another member.

## Limits and how it could change

| Limit | How it could change |
|---|---|
| The CSS targets Streamlit's own HTML (for example `[data-testid="stImage"]`), which can change in a new Streamlit version. | Streamlit is pinned in `pyproject.toml`. If a style stops working, only `style.css` changes; the game still works without it. |
| The entering moment fades with CSS only, so it plays once per Play and cannot be skipped. | A "skip" button would need one more run; not worth it for 4 seconds. |
| The pictures are a data URL in the page, so a large `entrance_hall.jpg` makes that one run slower. | Keep the file under 300 KB, like the others. |
| Photorealistic people can look like real people. | The character sheets describe invented people; if a face looks like someone real, generate it again. |
| The current 10 pictures are illustrations; mixing them with photorealistic new ones looks odd. | Regenerate all 12 with the new style block, or keep the old style block for the 2 new pictures until there is time. |
