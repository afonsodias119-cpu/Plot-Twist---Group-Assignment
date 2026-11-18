# Scene images and mystery theme

**Blocked by:** the base game merged into `main` (done). The illustrations are listed in `docs/historia.md` section 10; their prompts are in `docs/imagens.md`.

Phase D extra 1 of 2. It changes how the game looks and never changes the rules or the saved games.

## Before writing the spec

- **Product and user:** a player of "O quinto elemento", who should feel in a mystery from the first screen.
- **Trigger:** any screen is drawn.
- **Before:** the screens are plain text on the default white theme.
- **Rule:** an image is shown only if its file exists. A missing file shows nothing and never an error.
- **After:** the Start, Scene and Ending screens show their illustration, the inventory shows small item pictures, and the whole app uses a dark theme with amber as the accent colour.

## Why

As a player, I want to see where I am, so that the story feels like a place and not a list of buttons. As a team, we want the design criterion (20% of the grade) to be clearly met, with very little code.

## What

### 1. Files

| File | Job |
|---|---|
| `assets/<name>.jpg` (new) | The illustrations. Names below. |
| `.streamlit/config.toml` (new) | The theme: `base = "dark"`, navy background, off-white text, amber `primaryColor`. |
| `game.py` | Gets `ASSETS_DIR` and `image_file(name)`. |
| `app.py` | Calls `game.image_file` and shows the result with `st.image`. |

### 2. Image names

Ten files, 1280 x 720 for scenes, endings and cover, and about 400 x 400 for items, each under 400 KB:

| Where it is shown | File |
|---|---|
| Start screen | `cover.jpg` |
| Scene screen, above the text | `<scene id>.jpg`: `study_room`, `print_shop`, `library`, `computer_lab`, `auditorium` |
| Ending screen, above the text | `ending_<ending id>.jpg`: `ending_impostor.jpg`, `ending_stolen_credits.jpg` |
| Inventory, next to each item | `<item id>.jpg`: `usb_stick`, `original_photo` (shown 80 pixels wide) |

The pictures are the same in both languages: they contain no text.

### 3. `game.image_file(name) -> str or None`

- `ASSETS_DIR` is the `assets` folder next to `game.py`. It is read when the function runs, so tests can point it at a temporary folder.
- Returns the path of `<name>.jpg` as text if the file exists, otherwise `None`.
- `name` must be text made only of lower-case letters, digits and `_`. Anything else (`"../secret"`, `"a/b"`, `""`, `None`, a number) returns `None`, even if such a file exists. The names come from story ids, never from what the player types.

### 4. Screens (`app.py`)

- Start: the cover under the title. Scene: the scene image under the scene title, above the message. Ending: the ending image under the ending title. Inventory: each item's picture beside its name.
- Each image is drawn only when `image_file` is not `None`. No other change to the screens, keys or buttons.

### 5. Theme

`.streamlit/config.toml` sets the colours listed in section 1. Text and buttons must stay readable: off-white text on navy, and amber used only for accents. No other setting.

## Checklist (one line, one test) — `tests/test_images.py`

- [ ] `test_image_file_returns_the_file_when_it_exists` — with a temporary `ASSETS_DIR` holding `study_room.jpg`, `image_file("study_room")` is its path; `image_file("library")` is `None`. A fixture sets `game.ASSETS_DIR`.
- [ ] `test_image_file_refuses_names_that_are_not_ids` — with `study_room.jpg` and a file one folder up, `"../secret"`, `"a/b"`, `"Study_Room"`, `""`, `None` and `7` give `None`.
- [ ] `test_screens_work_without_any_image` — with an empty `ASSETS_DIR`: the Start, Scene and Ending screens open and play with no exception and no image element.
- [ ] `test_start_scene_and_ending_show_their_image` — with real small `.jpg` files in a temporary `ASSETS_DIR`, the Start screen shows one image; the study room shows its image; after `P_SHORT` the ending screen shows the image of `stolen_credits`.
- [ ] `test_inventory_shows_item_pictures` — holding `usb_stick` with `usb_stick.jpg` present, the scene shows two images (scene and item).
- [ ] `test_theme_file_is_a_dark_theme` — `.streamlit/config.toml` can be read as TOML and has `theme.base` equal to `"dark"` and a `primaryColor`.

## Out of scope

- Making pictures inside the app, animations, sound and a typewriter effect.
- Different images per language, or per game state (for example an open drawer).
- Alt texts and captions. A later spec may add `caption` with the scene title.

## Done when

- `uv run pytest` is green, with the tests written from the checklist and reviewed before the code.
- The 10 files are in `assets/`, each under 400 KB, made with one tool and one style as `docs/imagens.md` explains. Missing images are allowed for the first deploy: the app must still work.
- By clicking, in both languages: every scene, both endings and the Start screen show their picture, and the text is readable on the dark theme.
- `pyproject.toml` and `uv.lock` are unchanged.
- The work is on its own branch, pushed, and reviewed by another member.

## Limits and how it could change

| Limit | How it could change |
|---|---|
| The pictures are made by AI tools and may need two to four tries each. | The app does not depend on them: any missing file is just not shown. |
| One picture per scene, whatever the player did. | `image_file` could take a state and choose a variant. Only `game.py` and `app.py` change. |
| The files are in the repository, so they count for its size and for the deploy. | Keep each file under 400 KB. |
