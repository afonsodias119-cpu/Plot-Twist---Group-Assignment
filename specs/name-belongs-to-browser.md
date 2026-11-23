# A saved name belongs to the browser that started it

Extends specs/campus-3d-streamlit.md (the bridge between the page and Python) and specs/base-game.md (saves by name). Only the published 3D game (`app_3d.py`) changes. The plain game (`app.py`) and the local 3D server (`server3d.py`, for the team's own computers) keep working by name only. No reviewed test changes.

## Before writing the spec

- **Product and user:** anyone who opens the public link and types a detective name.
- **Trigger:** a command from the page (start, continue, any action) for a name that already has a save.
- **Before:** the save is chosen by the name alone. Anyone who types "afonso" continues, changes or restarts Afonso's game, and sees his earlier nights. The course rubric (Security) asks for access control.
- **Rule:** the first browser that uses a name gets a secret key for it. From then on, a command for that name is accepted only with that key.
- **After:** the owner plays as before. Someone else who types the same name is told it is taken and is sent back to choose another name.

## Why

As a player, I want nobody else to be able to continue, change or restart my game, so that my progress and my earlier nights stay mine.

## What

1. **The key.** `game.claim_name(player, key)` (in `game.py`, next to `clean_name`):
   - a name that is not valid returns `""` (nothing is claimed; the command refuses the name as before);
   - a name nobody has claimed gets a new key (`secrets.token_urlsafe(24)`), which is returned;
   - a claimed name returns the same key when the given key matches, and `None` when it does not (or when no key is given).
   - Only a SHA-256 hash of the key is stored, so a copy of the database does not reveal any key. Keys are compared with `hmac.compare_digest`.
2. **Storage.** `db.py` gets a fourth table, `keys (player TEXT PRIMARY KEY, key_hash TEXT NOT NULL)`, created in `init_db` with the others, and two functions: `load_key_hash(player)` and `save_key_hash(player, key_hash)`. The `games`, `nights` and `runs` tables do not change.
3. **The command.** `campus_game.keyed_command(payload)` takes the `key` out of the payload, calls `game.claim_name` and then `command` with the rest (so `command` and its allowed fields stay exactly as they are). A taken name raises `ValueError` with `TEXT[language]["name_taken"]`. It returns `(result, key)`.
4. **The app.** `app_3d.answer` calls `keyed_command` and adds `"key"` to the reply.
5. **The bridge** (the script `app_3d.py` puts before the page): before sending, it adds the key this browser keeps for that name (lower case, trimmed, as `game.clean_name`); when a reply brings a key, it keeps it. Keys are kept in `localStorage` under `plot-twist-keys`, and in memory when storage is blocked.
6. **The page.** When the reply before the game starts is the "name taken" message, the start screen goes back to the name step and shows the message under the name field.
7. **Texts** (`campus_text.TEXT`, both languages): `name_taken`:
   - en: "Someone on another device or browser is already playing with this name. Choose another name."
   - pt: "Alguém noutro dispositivo ou browser já está a jogar com este nome. Escolhe outro nome."

## Limits

- The key lives in one browser. Clearing the browser's data, a private window, or another device means the name cannot be continued: the player chooses another name. This is the price of having no accounts and no passwords.
- Saves made before this change have no key: the first browser that uses such a name claims it.
- Streamlit Community Cloud can wipe the database when the app restarts; the keys go with the saves, so nothing is left half-claimed.

## Out of scope

Accounts, passwords, e-mail, sharing a game between devices, the plain game, the local server.

## Done when

- [ ] Existing tests pass unchanged.
- [ ] `tests/test_name_belongs_to_browser.py`: claiming a free name, the same key again, a wrong or missing key, an invalid name, only the hash stored, the table created by `init_db`, `keyed_command` refusing a taken name before anything is saved and accepting the owner, the key never reaching `command`, both texts, and the bridge and `answer` source carrying the key.
- [ ] In the browser: a name started in one browser profile is refused in another with the message under the name field; the first browser continues normally after a reload.
