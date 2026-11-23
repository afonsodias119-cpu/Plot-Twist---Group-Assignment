# Base game — "O quinto elemento"

> **Update (specs/computer-lab-backup.md):** the group chat, its flags, the message cards and "The fifth element" are gone. Computer 12 saves a backup of the original conversations; Leonor's choice decides the three story endings; Duarte catches a player at computer 12 before the backup.

**Blocked by:** pull request 3 (branch `story-map`) merged into `main` and the story approved by the team. The story is in `docs/historia.md` (Portuguese texts, ids, conditions and effects) and `docs/story-en.md` (English texts); the brief is in `docs/plot-twist-brd.md` (PT01–PT05, R1–R4, A1–A6).

This spec covers the whole base game, so it is longer than a course example. It may be built as three pull requests, in the order of the checklist: rules, saving, screens. If so, each one has its own branch (`base-game-rules`, `base-game-saving`, `base-game-screens`), adds only the tests of its own part before its code, and is green before it is merged. The `db` fixture and the `import db` and `import game` lines arrive with the saving part. Adding tests to a reviewed file is allowed; changing reviewed tests is not.

## Before writing the spec

- **Product and user:** a player of the short mystery "O quinto elemento".
- **Trigger:** the player clicks an action button.
- **Before:** the saved game: current scene, inventory, remembered decisions, ending.
- **Rule:** the action must belong to the current scene, still be offered, and have its requirement met. After an ending, no story action is accepted.
- **After:** an accepted action changes the game and is saved. A rejected action shows why and changes nothing.
- **Restart:** stop the app and start it again; typing the same name continues the same game.

## Why

As a player, I want to explore the mystery, collect and use items, reach one of two endings and come back later to the same game, so that my choices matter and are never lost. Every part must be simple enough for any of the four of us to explain.

## What

### 1. Files

| File | Job |
|---|---|
| `story.py` (new) | Content only: the dictionaries `STORIES` and `UI_TEXTS` (one entry per language, `"en"` and `"pt"`) and `LANGUAGES`. No functions, no `if`. |
| `logic.py` (new) | Rules. Imports nothing from the project: the story is passed in. |
| `db.py` (new) | Storage: one table, three functions. The only file that uses `sqlite3`. |
| `game.py` (new) | One turn: load the saved game, ask the rules, save if accepted. |
| `app.py` (placeholder today) | Screens. The only file that uses Streamlit. |

Only progress is saved in SQLite. The story stays in `story.py`, because play never changes it and a Python file needs no loading or encoding code.

### 2. Story data and game state

The game is played in English or Portuguese, chosen by the player on the Start screen. There is one story per language, and the two have exactly the same structure: the same scene ids, action ids, item ids, conditions and effects. Only the texts differ. The example below is the English story; `STORY_PT` has the same shape.

```python
LANGUAGES = {"en": "English", "pt": "Português"}   # the Start screen choice
# STORIES and UI_TEXTS are written after STORY_EN, STORY_PT, UI_EN and UI_PT:
#   STORIES = {"en": STORY_EN, "pt": STORY_PT}
#   UI_TEXTS = {"en": UI_EN, "pt": UI_PT}

STORY_EN = {
    "start": {"scene": "study_room", "inventory": [],
              "flags": {"colleague_choice": "none", "files_viewed": False},
              "ending": "none"},
    "items": {"usb_stick": "USB stick with the project history",
              "original_photo": "Printed original photo"},
    "messages": {"game_over": "...", "not_here": "...", "not_offered": "...", "no_game": "..."},
    "scenes": {
        "computer_lab": {
            "title": "Computer lab",
            "texts": [
                {"when": {}, "text": "The computer lab is empty. ..."},
                {"when": {"flags": {"files_viewed": True}}, "text": "You have compared the files: ..."},
            ],
            "actions": {
                "view_files": {
                    "label": "Look at the old project files",
                    "offered_if": {"flags": {"files_viewed": False}},
                    "requires": {"has": ["usb_stick"]},
                    "blocked_text": "The shared folder only shows the current version ...",
                    "sets": {"files_viewed": True},
                    "result_text": "You plug the USB stick into computer 12 and compare. ...",
                },
                "go_study_room": {"label": "Back to the study room", "go_to": "study_room"},
            },
        },
        # the other four scenes have the same shape
    },
    "endings": [
        {"id": "impostor", "title": "The impostor",
         "when": {"flags": {"colleague_choice": "help"}}, "text": "..."},
        {"id": "stolen_credits", "title": "Stolen credit", "when": {}, "text": "..."},
    ],
}
```

- **Game state:** a dictionary shaped like `start`, with four keys: `scene`, `inventory`, `flags`, `ending`.
- **Condition** (`when`, `offered_if`, `requires`): a dictionary with up to three keys. `has` lists items that must be in the inventory. `lacks` lists items that must not be. `flags` gives values the flags must equal. An empty or missing condition is always true.
- **Effect:** `go_to` (a scene id) changes the scene. `gives` (one item id, as in `"gives": "usb_stick"`) adds that item. `sets` (a dictionary) changes those flags. `"ends_game": True` sets `ending` to the `id` of the first ending in the list whose `when` is true.
- **Scene text:** every `texts` entry whose `when` is true, in order.
- **Texts:** the Portuguese scene, action and ending texts are copied from `docs/historia.md` sections 6 and 7, and the English ones from the same sections of `docs/story-en.md`. The premise on the Start screen is the first paragraph of section 1 of each file. The four `messages` and the `UI_TEXTS` sentences are not in those files: the builder writes each as one short sentence in both languages (European Portuguese uses "tu", like the story) and lists them in the pull request for the team to approve.
- `UI_TEXTS[language]` holds every sentence of the screens, so changing a text edits `story.py` only. The checks use four keys, present in both languages: `started`, `continued`, `invalid_name`, `no_game`.
- **Language is not part of the game state dictionary.** The ids saved in SQLite are the same in both languages. The language is saved in the same row as the player's name (section 4) and only chooses which story and which sentences to show. A returning player always gets the language of the saved game.

The seven actions with a condition or effect (the other seven are plain moves):

| Scene | Action id | `offered_if` | `requires` | Effect |
|---|---|---|---|---|
| `study_room` | `open_drawer` | lacks `usb_stick` | | gives `usb_stick` |
| `study_room` | `go_auditorium` | | `files_viewed` is `True` | go to `auditorium` |
| `print_shop` | `request_copy` | lacks `original_photo` | | gives `original_photo` |
| `library` | `ask_for_help` | `colleague_choice` is `none` | has `original_photo` | sets `colleague_choice` to `help` |
| `library` | `accuse` | `colleague_choice` is `none` | has `original_photo` | sets `colleague_choice` to `accused` |
| `computer_lab` | `view_files` | `files_viewed` is `False` | has `usb_stick` | sets `files_viewed` to `True` |
| `auditorium` | `present_evidence` | | | ends the game |

Moves: `go_print_shop`, `go_library` and `go_computer_lab` from `study_room`; `go_study_room` from each of the other four scenes.

### 3. Rules (`logic.py`)

| Function | Returns |
|---|---|
| `new_game(story) -> dict` | A fresh copy of `story["start"]` |
| `available_actions(story, state) -> list[dict]` | The current scene's offered actions, in story order, each `{"id", "label", "allowed"}`. `allowed` is `True` when the action's `requires` is true. `[]` after an ending |
| `apply_action(story, state, action_id) -> dict` | `{"accepted", "reason", "message", "state"}` |
| `scene_text(story, state) -> list[str]` | The paragraphs of the current scene |
| `is_valid_state(story, state) -> bool` | `True` only if `state` is a dictionary with the four keys; `scene` is a scene id; `inventory` is a list of item ids (text) with no repeats; `flags` is a dictionary with exactly the keys of `story["start"]["flags"]`, each holding its start value or a value some action's `sets` gives it; and `ending` is `"none"` or an ending id. Never raises an error |

`apply_action` checks in this order. The first failure decides:

| Check | `reason` | `message` |
|---|---|---|
| 1. No ending has been reached | `game_over` | `story["messages"]["game_over"]` |
| 2. `action_id` is an action of the current scene | `not_here` | `story["messages"]["not_here"]` |
| 3. Its `offered_if` is true | `not_offered` | `story["messages"]["not_offered"]` |
| 4. Its `requires` is true | `blocked` | its `blocked_text` |
| All pass | `ok` | its `result_text` (`""` for a move and for `present_evidence`) |

- **Accepted:** `accepted` is `True` and `state` is a new dictionary with the effect applied.
- **Rejected:** `accepted` is `False` and `state` equals the one given.
- The rules never change the story or the state they were given. They build new lists and dictionaries.

### 4. Storage (`db.py`)

- `init_db() -> None`: creates the folder that holds `DB_PATH` and the table, if they are missing.
- `save_game(player: str, state: dict, language: str = "en") -> None`: writes or replaces that player's row, with the language.
- `load_game(player: str) -> dict or None`: that player's state. `None` if there is no row or the row cannot be read.
- `load_language(player: str) -> str or None`: the language saved in that player's row. `None` if there is no row or it cannot be read. It does not check that the language is one of `LANGUAGES`; `game.py` does.

```sql
CREATE TABLE IF NOT EXISTS games (
    player    TEXT PRIMARY KEY,
    scene     TEXT NOT NULL,
    inventory TEXT NOT NULL,   -- a JSON list, for example ["usb_stick"]
    flags     TEXT NOT NULL,   -- a JSON dictionary
    ending    TEXT NOT NULL,
    language  TEXT NOT NULL    -- "en" or "pt", chosen when the game was started
);
```

- `DB_PATH` is `data/plot_twist.db` next to `db.py`. It is read when a function runs, so tests can point it at a temporary file.
- `save_game` and `load_game` call `init_db()` first. Each function opens and closes its own connection.
- Values enter SQL only through `?` placeholders. They are sent apart from the SQL text, so they cannot run as SQL.
- `flags` is stored as text, so a new remembered fact needs no table change.

### 5. One turn (`game.py`)

| Function | Does |
|---|---|
| `clean_name(text) -> str or None` | The name trimmed and in lower case, or `None`. Valid: 1 to 20 characters; letters (accented ones too), digits, space, `-`, `_` |
| `load(player) -> dict or None` | The saved state if it exists and `is_valid_state` is true; otherwise `None` |
| `open_game(player, language) -> dict` | `{"state", "continued", "language"}`. Continues a valid save and returns the language saved with it; if that language is not in `LANGUAGES`, it uses the given one and saves it. With no valid save, it saves a new game with the given language and returns it |
| `play(player, action_id, language="en") -> dict` | Loads the save and its saved language, calls `apply_action` with that language's story, saves (keeping the same language) only if accepted, returns the result. With no valid save it saves nothing and returns `{"accepted": False, "reason": "no_game", "message": STORIES[language]["messages"]["no_game"], "state": None}`, where `language` is the argument, the only case in which it is used |
| `restart(player) -> dict` | Saves a new game over that player's row, keeping the saved language, and returns it |

- SQLite is the only copy of the game. Players are kept apart by the name typed on the Start screen, which is the row key.

### 6. Screens (`app.py`)

| Screen | Shows | Buttons (keys) |
|---|---|---|
| Start | Language choice (`language`), title, premise, "type the same name to continue", name box (`player_name`) | `play` |
| Scene | Scene title, text, last result, inventory or an "empty" line | `action_<id>` for each offered action, `new_game` |
| Ending | Ending title and text, inventory | `new_game` only |

- The language choice is an `st.radio(key="language")` above the form, with the options of `LANGUAGES`, English first. Changing it reruns the page by itself, so the title, premise and name box change language at once. The choice is used when a **new** game is started. A player who already has a save (same name) continues in the language saved with it, whatever the radio shows. After Play, every screen is drawn with the language that `open_game` returned, kept in `st.session_state["lang"]`. A saved game cannot change language.
- The Start screen is one `st.form` with `st.text_input(key="player_name", max_chars=20)` and `st.form_submit_button(key="play")`. An invalid name shows an error and saves nothing. After Play, the message says whether the game was started or continued.
- Every button uses `on_click`. No `if st.button(...)` and no `st.rerun()`.
- Apart from the widget keys, which Streamlit adds by itself (`language`, `player_name`, `play`, `action_<id>` and so on), `st.session_state` holds only `player`, `lang`, `message` and `confirming`.
- `message` is `None` or `{"kind", "text"}`, where `kind` is `"success"` (accepted action, game started or continued), `"warning"` (rejected action) or `"error"` (invalid name, missing save). It is replaced on every click and drawn only when the text is not empty, with `st.success`, `st.warning` or `st.error`.
- Blocked actions are shown. Clicking one shows its explanation.
- `new_game` writes nothing. It shows a warning with `confirm_yes` and `confirm_cancel`, and the action buttons are not drawn while it shows. Cancel writes nothing. Yes calls `restart`.
- If `play` returns `no_game` (the save is missing or broken), `player` and `lang` are cleared and the Start screen returns with an error message. Never an error page.

### 7. Checklist (one line, one test)

Paths used below:

- `P_SHORT` (6 actions): `open_drawer`, `go_computer_lab`, `view_files`, `go_study_room`, `go_auditorium`, `present_evidence`.
- `P_HELP` (12 actions): `open_drawer`, `go_print_shop`, `request_copy`, `go_study_room`, `go_library`, `ask_for_help`, `go_study_room`, `go_computer_lab`, `view_files`, `go_study_room`, `go_auditorium`, `present_evidence`.
- `P_ACCUSE`: `P_HELP` with `accuse` in place of `ask_for_help`.

Every rejected step also checks that the state equals the state before. Expected messages are read from the story, never typed into a test. In this checklist, `STORY` means `STORIES["en"]` and `UI` means `UI_TEXTS["en"]`, unless a test names another language.

**Rules** — `tests/test_base_game.py`

- [ ] `test_new_game_is_the_opening_state` — equals `STORY["start"]`; two new games do not share one inventory list or one flags dictionary. (PT01, R4)
- [ ] `test_study_room_offers_its_five_actions` — ids are `open_drawer`, `go_print_shop`, `go_library`, `go_computer_lab`, `go_auditorium`; only `go_auditorium` has `allowed` `False`. (PT02)
- [ ] `test_auditorium_is_blocked_until_files_are_viewed` — `go_auditorium` in a new game, and again holding `usb_stick`: `blocked`, message is its `blocked_text`. (A1, R1, PT04)
- [ ] `test_item_actions_are_blocked_without_their_item` — `view_files` holding only `original_photo`; `ask_for_help` and `accuse` holding only `usb_stick` with `files_viewed` `True`: `blocked`. (A1)
- [ ] `test_usb_stick_opens_the_files_then_the_auditorium_and_is_kept` — the first 5 steps of `P_SHORT` are accepted; then scene `auditorium`, `files_viewed` `True`, inventory `["usb_stick"]`. The brief's key is `usb_stick`, its lock `files_viewed`, its route `auditorium`. (A2, R2)
- [ ] `test_original_photo_allows_the_decision_and_is_kept` — after `ask_for_help`: `colleague_choice` `help`, `original_photo` still held. (A2, PT03)
- [ ] `test_collected_item_is_not_collected_again` — after `open_drawer`, go to `print_shop` and back: `open_drawer` is not offered; asking for it gives `not_offered`; inventory `["usb_stick"]`. Same for `request_copy`. (A3, R2, R3)
- [ ] `test_actions_already_done_are_not_offered` — a second `view_files`; `accuse` after `ask_for_help`: `not_offered`. (PT04, R3)
- [ ] `test_action_of_another_scene_is_rejected` — `request_copy` in `study_room`: `not_here`; the same id is accepted in `print_shop`. (R1)
- [ ] `test_unknown_action_ids_are_rejected` — `"fly"`, `""`, `None`, `7`: `not_here`.
- [ ] `test_three_paths_reach_their_endings` — `P_HELP` ends in `impostor`; `P_SHORT` and `P_ACCUSE` end in `stolen_credits`. (A5, PT04)
- [ ] `test_every_action_is_rejected_after_an_ending` — after each ending, every action id of the story gives `game_over`, and `available_actions` is `[]`. (A5, PT05)
- [ ] `test_every_ending_is_reachable_from_a_new_game` — start a list with a new game; for each state try every offered action and add each new state; stop when nothing is new. The endings found are exactly `impostor` and `stolen_credits`. (R4)
- [ ] `test_playing_never_changes_the_story` — a deep copy of `STORY` taken before playing `P_HELP` and `P_SHORT` still equals `STORY`. (R4)
- [ ] `test_apply_action_never_changes_the_state_it_was_given` — at every step of `P_HELP` and for one rejected action, the state passed in equals its copy.
- [ ] `test_scene_text_follows_remembered_changes` — `library` shows exactly one entry for each of `none`, `help`, `accused`, and the three differ; `computer_lab` shows its second entry only after `view_files`; `study_room` and `print_shop` show theirs only once the item is held. (R3)
- [ ] `test_both_languages_have_the_same_structure` — `STORIES` has exactly the keys `en` and `pt`. For both stories, the scene ids, action ids (in order), item ids, `start`, `go_to`, `gives`, `sets`, `ends_game`, every `when`, `offered_if` and `requires`, the number of `texts` entries per scene and the ending ids (in order) are equal. Every text (titles, labels, `texts`, `blocked_text`, `result_text`, items, endings, `messages`) is a non-empty string. `UI_TEXTS` has the same keys in both languages.
- [ ] `test_paths_work_in_every_language` — for each story in `STORIES`, `P_HELP` ends in `impostor`, and `P_SHORT` and `P_ACCUSE` end in `stolen_credits`. (A5)
- [ ] `test_story_meets_the_content_baseline` — for each story in `STORIES`: at least 5 scenes, 2 items, 2 endings; every `go_to` names a scene; every item and flag named in a condition or effect exists; every action with `gives` or `sets` has a `result_text`; every action with `requires` has a `blocked_text`; the last ending's `when` is `{}`. (PT02, PT04)
- [ ] `test_is_valid_state_rejects_broken_saves` — scene `"cafeteria"`; a repeated item; inventory `[["usb_stick"]]`; a missing flag; flags `None`; flags as a list; `files_viewed` `"yes"`; `colleague_choice` `"maybe"`; ending `"x"`; `None`. Each gives `False` without an error.
- [ ] `test_playing_never_changes_the_stories` — a deep copy of `STORIES` taken before playing `P_HELP` and `P_SHORT` in both languages still equals `STORIES`. (R4)
- [ ] `test_logic_imports_nothing_from_the_project` — no `import` or `from` line of `logic.py` names `streamlit`, `sqlite3`, `db`, `game` or `story`.

**Saving** — same file. A fixture in `tests/conftest.py` points `db.DB_PATH` at a file in pytest's `tmp_path` (a throwaway folder) for every test.

- [ ] `test_first_run_creates_the_folder_and_table` — with `DB_PATH` inside a folder that does not exist yet, `init_db` twice: no error, the folder and file exist; `load_game("ana")` is `None`.
- [ ] `test_clean_name_accepts_valid_names` — `"  Ana "` gives `"ana"`; `"João"` gives `"joão"`; `"Ana-Rita_2"` is accepted.
- [ ] `test_clean_name_rejects_invalid_names` — `""`, `"   "`, 21 letters, `"<b>"`, `"a;b"`, `None`.
- [ ] `test_open_game_starts_then_continues` — `open_game("ana", "en")`: `continued` `False`, state equals a new game and is saved. After `open_drawer`, `open_game("ana", "en")` again: `continued` `True`, inventory `["usb_stick"]`. (PT01)
- [ ] `test_every_accepted_action_is_saved` — after each step of `P_HELP`, `load_game` equals the returned state. (A4)
- [ ] `test_rejected_actions_leave_the_saved_game_unchanged` — one case each for `blocked`, `not_offered`, `not_here` and `game_over`, each from a game with progress.
- [ ] `test_play_without_a_save_is_rejected` — `play("rui", "open_drawer")` with no row: `no_game`, message is `STORY["messages"]["no_game"]`, and `load_game("rui")` is still `None`.
- [ ] `test_a_save_keeps_its_language` — `open_game("ana", "pt")` returns language `"pt"`; after `open_drawer`, `open_game("ana", "en")` continues (`continued` `True`) and still returns `"pt"`; `load_language("ana")` is `"pt"`. `play("ana", "go_library", "en")` is accepted, its message is read from `STORIES["pt"]`, and the language is still `"pt"` in the row. `restart("ana")` keeps `"pt"`. (PT01, A4)
- [ ] `test_unknown_saved_language_falls_back` — the test writes a row for `ana` with language `"xx"` and valid progress: `open_game("ana", "en")` continues that progress, returns `"en"` and saves it. (A4)
- [ ] `test_play_without_a_save_uses_the_given_language` — `play("rui", "open_drawer", "pt")` with no row gives the `no_game` message of `STORIES["pt"]` and saves nothing.
- [ ] `test_resumed_game_offers_the_same_actions` — after the first 9 steps of `P_HELP`, a fresh `load` gives scene `computer_lab`, both items, `help`, `files_viewed` `True` and the same `available_actions`; then `go_study_room` and `go_auditorium` are accepted. (A4)
- [ ] `test_finished_game_loads_back_finished` — after `P_SHORT`: ending `stolen_credits`; any action gives `game_over`. (A4, PT05)
- [ ] `test_restart_resets_only_this_player` — `ana` and `rui` both have progress; `restart("ana")`: her save equals a new game, his is unchanged. (A6, R4)
- [ ] `test_new_game_after_an_ending_reaches_the_other_ending` — reach `impostor`, `restart`, play `P_SHORT`: `stolen_credits`. (PT05, R4)
- [ ] `test_players_have_separate_saves` — `ana` and `rui` play in turn; each save shows only its own actions.
- [ ] `test_hostile_text_is_saved_as_plain_data` — `save_game` with player `"x'; DROP TABLE games; --"` and language `"en"`: it loads back, and a second player's save still loads.
- [ ] `test_broken_save_counts_as_no_save` — the test writes two rows with its own SQL: one with scene `"cafeteria"`, one whose `flags` text is not JSON. For each, `load` is `None` and `open_game("ana", "en")` starts a new game.

**Screens** — `tests/test_smoke.py`, with `AppTest`, Streamlit's built-in screen tester. Each test builds the path to `app.py` from its own folder, uses `default_timeout=10`, and checks that no exception happened.

- [ ] `test_app_opens_on_an_empty_database` — the Start screen shows `language` (set to English) and `play`. (PT01)
- [ ] `test_language_choice_changes_the_texts` — on Start, choosing `Português` shows the Portuguese premise and `UI_TEXTS["pt"]` sentences; as a new player `ana`, the first scene shows the Portuguese title and its buttons use the Portuguese labels. A new player `rui` with English sees the English ones.
- [ ] `test_returning_player_keeps_the_saved_language` — as `ana` with `Português`, `action_open_drawer`; a new session left on the default English, same name: the message is `UI_TEXTS["pt"]["continued"]`, the screen is in Portuguese, there is no `action_open_drawer`, and the item is shown with its Portuguese name. (A4)
- [ ] `test_invalid_name_shows_an_error` — `"<b>"`: one `st.error` equal to `UI["invalid_name"]`, still on Start; then the test calls `db.init_db()` and counts 0 rows in `games`.
- [ ] `test_new_name_starts_and_same_name_continues` — `ana` gets `UI["started"]`; after `action_open_drawer`, a new session as `ana` gets `UI["continued"]`, has no `action_open_drawer` and shows the item's name. (PT01, A4)
- [ ] `test_missing_save_returns_to_start` — as `ana`, the test deletes her row, then clicks `action_open_drawer`: no exception, the Start screen with `play`, and one `st.error`.
- [ ] `test_accepted_click_shows_its_result` — `action_open_drawer`: one success box equal to its `result_text`; the button is gone. (PT02)
- [ ] `test_blocked_click_is_explained` — `action_go_auditorium`: one warning equal to its `blocked_text`; the scene is still the study room. (A1, PT04)
- [ ] `test_new_game_asks_first` — after `action_open_drawer`: `new_game` shows `confirm_yes` and `confirm_cancel` and no action buttons. Cancel: saved inventory still `["usb_stick"]`. `new_game` then `confirm_yes`: the saved game equals a new game and `action_open_drawer` is back. (A6)
- [ ] `test_finished_game_shows_only_new_game` — after `P_SHORT` by clicks: the ending title, no `action_` buttons, `new_game`. (PT05)
- [ ] `test_click_from_an_old_tab_is_judged_against_the_saved_game` — two sessions as `ana`; the second clicks `action_open_drawer`; then the first, still showing that button, clicks it: one warning, saved inventory exactly `["usb_stick"]`.

## Out of scope

- The brief's exclusions: story editor, procedural generation, multiplayer, combat, live AI dialogue, paid or external services.
- Phase D extras: code puzzle, detective notebook and accusation, action limit, more mysteries, map, achievements, statistics.
- Images and sound. A later spec shows `assets/<scene id>.jpg` when the file exists.
- Accounts and passwords. Deployment (phase E).
- A language switch after a game has started, and languages other than English and Portuguese. A third language is another entry in `STORIES` and `UI_TEXTS`.
- Not to add unasked: extra scenes, `st.dialog`, `st.cache_*`, URL parameters, a story table, new libraries, version changes.

## Done when

- `uv run pytest` is green. The tests were written from the checklist, reviewed before the code, and not changed afterwards.
- By clicking, as player `ana`:
  - **Accepted:** open the drawer. The result text appears and the pen is in the inventory.
  - **Rejected:** go to the auditorium. The explanation appears, the scene is still the study room and the inventory is unchanged.
  - **Restart:** stop the app (Ctrl+C) and start it again, not just refresh. `ana` continues in the same scene with the pen.
- Both endings are reached by clicking. Each shows its own title and no story buttons.
- Language: play once in English and once in Portuguese. As `ana` with Português, open the drawer, stop the app and start it again, leave the radio on English and type `ana`: the game continues in Portuguese, in the same scene, with the item.
- New game: Cancel keeps the game. Yes returns to the study room with an empty inventory.
- Two browsers with two names do not affect each other. A fresh clone with no `data` folder runs.
- One play-through is timed and noted in the pull request. The brief asks for about ten minutes.
- `pyproject.toml` and `uv.lock` are unchanged.
- `AGENTS.md` names `story.py` and `game.py` under Structure, and records the reset step: stop the app and delete `data/plot_twist.db`.
- The work is on branch `base-game`, pushed, and reviewed by another member.

## Limits and how it could change

| Limit | How it could change |
|---|---|
| The name is not a password. The same name opens the same game. Only the typed name and the game progress are stored. | Add sign-in. Only `game.py` and the Start screen change. |
| The host's disk is temporary. Assume saved games are lost when the deployed app restarts. | A hosted database. Only `db.py` changes. |
| Two tabs under one name: each click is judged against the saved game. | No change planned. |
| Tests do not cover how the screens look or a real stop and start of the app. | Checked by clicking (see Done when). |
| One mystery, in two languages. Every text change must be made twice, and the structure test fails if the two stories drift apart. | A second mystery is another pair of dictionaries shaped like `STORY_EN` and `STORY_PT`. The rules already take the story as input. |
| The language is chosen when a game starts and cannot be changed afterwards. | A language switch on the Scene screen that calls `save_game` with the new language. Only `app.py` and `game.py` change. |
| `uv audit` reports known vulnerabilities in Pillow 12.3.0, which Streamlit 1.62.0 installs and does not let us upgrade. The game opens no files from users. | Ask the staff. Upgrade when Streamlit allows it. |

## Open decisions

Rows 1 to 5 are section 11 of `docs/historia.md`. This spec follows the proposals made there.

| # | Question | This spec assumes | If the team decides otherwise |
|---|---|---|---|
| 1 | Names | Leonor, Duarte (no surname since 2026-11-22) | Edit texts in `story.py`. No test uses a name. |
| 2 | Language | Decided by the team (2026-11-15): the player chooses English or Portuguese on the Start screen. English is the default. | Remove one entry from `STORIES` and `UI_TEXTS`, and remove the `language` radio and its tests. |
| 3 | Blocked actions | Shown, and explained on click | `app.py` draws only actions with `allowed` `True`. The rules stay. `test_blocked_click_is_explained` checks that the button is absent instead. The section 6 bullet and the Done when "Rejected" click change: a rejection is then only visible through the old-tab case, which becomes the click check. `blocked_text` stays in the rules but is never shown. |
| 4 | Pen and auditorium | Two steps: the pen opens the files, and the files open the auditorium | `go_auditorium` requires `{"has": ["usb_stick"]}`. The two auditorium tests are rewritten and `P_SHORT` drops to 3 actions. In Done when, do the "Rejected" click before opening the drawer. Any check whose blocked case is the auditorium with the pen uses `view_files` without the pen instead. |
| 5 | Shortcuts between rooms | None | Add `go_...` actions in `story.py`. Any new way into `auditorium` needs the same `requires`. |
| 6 | Telling players apart | The typed name | A random code in the page address: survives a refresh and never clashes, but is more to explain. One shared save: least code, but everyone on the public link plays and resets one game. |
| 7 | "Store the story content" (`docs/plot-twist-brd.md` line 41) | The story stays in `story.py`. The original brief says "keep", not "store" | If the staff want it in SQLite, `init_db` also fills a story table from `story.py`. |
| 8 | Language: session or saved | Saved with the player's name (decided 2026-11-15): a returning player gets the saved language | Only the session: remove the `language` column and `load_language`, and let the radio decide every time. The same save then continues in either language. |
