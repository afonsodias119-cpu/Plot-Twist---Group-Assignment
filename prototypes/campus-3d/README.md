# Campus 3D — the published game

This folder is the 3D game that runs online (`app_3d.py` at the project root puts it inside Streamlit). It is called
`prototypes/` for historical reasons: it started as a prototype. The plain game without 3D is `app.py`; both share
`story.py`, `logic.py`, `game.py` and `db.py`.

## Run it

From the project root:

```sh
uv sync
uv run streamlit run app_3d.py
```

For a quick local demo without Streamlit there is also `uv run python prototypes/campus-3d/server3d.py`
(http://127.0.0.1:8765, local only). Saves go to `data/campus3d.db`, separate from the plain game's `data/plot_twist.db`.

## Files

The server side (Python) decides everything; the page only draws and sends one command per action.

| File | Job |
|---|---|
| `campus_game.py` | Checks every command from the page (allowed fields, types, the clock), runs it and builds the snapshot the page draws. |
| `campus_evidence.py` | The rules of the evidence and the hearing: the cards held, confronting a person, handing the proofs to the professor. |
| `campus_case.py` | Data only, server only: the cards, Duarte's claims and the professor's lines. Never sent to the page. |
| `campus_people.py` | Data and rules of the conversations: who is in which room and what each person says, in both languages. |
| `campus_clock.py` | The night's clock: the costs, when Leonor leaves, Duarte's rounds. |
| `campus_memory.py` | Earlier nights: the night number and the unknown number's messages. |
| `campus_search.py` | The study room table, the code of computer 12 and the torn photo. |
| `campus_text.py` | The interface texts of the page, in both languages. |
| `page3d.py` | Builds the page: puts the texts and pictures into `game3d.html`. |
| `game3d.html` | The Three.js campus: rooms, people, the character, the cameras. |
| `play.js`, `play.css` | The panel, the phone, the conversations, the security desk, the ending card. |
| `table.js`, `photo.js` | The close-up of the study room table and the torn photo puzzle. |
| `server3d.py`, `code_refresh.py` | The local demo server, and reloading the code after a deploy. |

## Tests

`uv run pytest` from the project root runs every test, including this folder's. Each feature has its spec in
`specs/` (see [specs/README.md](../../specs/README.md)).
