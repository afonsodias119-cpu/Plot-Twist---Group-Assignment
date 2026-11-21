# Fresh code after a deploy

## Before writing the spec

- **Product and user:** anyone who opens the public link right after the team merged a change.
- **Trigger:** the host copies the new files of `main` into the running app without restarting it.
- **Before:** Python still holds the old version of the game's files in memory, while the 3D page is built from the new files on disk.
- **Rule:** the page and the Python code must always come from the same version of the files.
- **After:** the app notices that the files changed, loads them again, and the game keeps working.
- **Restart:** a restart already loads everything fresh; nothing changes there.

## Why

On 21 Nov 2026, after a merge, the public link stopped at the language screen: the new page asked for data (`group`) that the old Python code in memory did not send. As a player, I want the link to keep working after the team merges something, so that the demo never depends on someone rebooting the app.

## What

- [ ] New file `prototypes/campus-3d/code_refresh.py` with `version(files) -> str` (a short fingerprint of the files' contents) and `refresh(files, module_names, state=LOADED) -> bool`.
- [ ] The first call of `refresh` only remembers the fingerprint and returns `False` (a process that just started has fresh code).
- [ ] When the fingerprint is the same as the remembered one, `refresh` reloads nothing and returns `False`.
- [ ] When it differs, `refresh` reloads each named module that is already loaded, in the order given, remembers the new fingerprint and returns `True`. A module that imports from another one must come after it in the list.
- [ ] `app_3d.py` calls `refresh` at the start of every run, before it builds the page or answers a command, for `story`, `logic`, `db`, `game`, `campus_text`, `campus_people`, `campus_search`, `campus_game` and `page3d`. It sets `db.DB_PATH` again afterwards, because reloading `db` resets it.
- [ ] `app_3d.py` calls `campus_game.command` and `page3d.build_page` through their modules, so it always uses the reloaded functions.

Checks (`tests/test_code_refresh.py`):

- [ ] `test_first_call_only_remembers_the_version`
- [ ] `test_unchanged_files_reload_nothing`
- [ ] `test_changed_file_reloads_its_module`
- [ ] `test_modules_that_import_from_a_changed_one_see_the_new_value`
- [ ] `test_app_3d_recovers_from_stale_code` (AppTest): with a stale remembered version and the `group` texts removed from memory, running `app_3d.py` again raises no exception and the texts are back.

## Out of scope

- Changes to `app.py` (Streamlit already reloads what it imports from the project folder) and to the game itself.
- Rebooting the host automatically, or keeping saved games across a restart.

## Done when

- `uv run pytest` is green; the tests were written before the code.
- By hand: with the 3D app running locally, change a text in `prototypes/campus-3d/page3d.py`, save, refresh the browser: the new text shows without restarting the app.
- Own branch, pushed, reviewed by another member.

## Limits and how it could change

| Limit | How it could change |
|---|---|
| The merge that first brings this file still needs one reboot of the hosted app. | Nothing to do: it happens once. |
| A browser tab opened before the merge keeps its old page until it is refreshed. | Show a "new version, refresh" notice from the page. |
