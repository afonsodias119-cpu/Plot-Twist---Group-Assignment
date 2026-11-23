# The first click never times out

Extends specs/campus-3d-streamlit.md (the bridge between the page and Python) and specs/name-belongs-to-browser.md. Only `app_3d.py` and `prototypes/campus-3d/campus_game.py` change. No reviewed test changes.

## Before writing the spec

- **Product and user:** the first player after the public app wakes up, for example the team at the start of the live demo.
- **Trigger:** the first command after the server starts ("Start / Continue").
- **Before:** Python answers a command in under 0.1 s, but the first round trip through Streamlit after the server starts takes about 2 s, and while the 3D world is still loading the page itself answers late. Measured: 8.5 s on Streamlit 1.67 and 14.7 s on 1.62 for the first start. The bridge gives up after 20 s and shows "The action could not be confirmed", which happened once in testing.
- **Rule:** the deployed app runs all workflows without errors (course rubric, It works).
- **After:** the page wakes the server up as soon as it opens, while the player reads the case, and the bridge waits up to 60 s before giving up.

## Why

As a player, I want my first click to work even when the app has just woken up, so that the game never starts with an error.

## What

1. **Warm-up request.** Right after the bridge tells Streamlit it is ready, it sends one `{"warmup": true}` request and ignores the answer. `campus_game.keyed_command` answers exactly that payload with `({"warm": True}, "")` before anything else: no name, no key, no database, nothing saved. Any other payload goes on as before.
2. **Longer wait.** The bridge gives up after 60 s instead of 20 s. A command that really fails still shows the same message, only later.

## Limits

- The warm-up does not make the 3D world load faster; it only means the server side is ready when the player clicks.
- A host that is asleep (Streamlit Community Cloud after a long time without visitors) still shows its own "wake up" screen first.

## Out of scope

The local server (`server3d.py`), the plain game.

## Done when

- [ ] Existing tests pass unchanged.
- [ ] `tests/test_warm_start.py`: `keyed_command({"warmup": True})` answers `({"warm": True}, "")` and writes nothing; a payload with `warmup` and anything else is still refused by `command`; the bridge sends the warm-up after `componentReady` and waits 60000 ms.
- [ ] In the browser: a fresh server's first "Start / Continue" works; the warm-up shows no message on the page.
