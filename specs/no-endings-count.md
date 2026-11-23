# No count of endings at the end

Changes the page only (`prototypes/campus-3d/play.js`, `play.css`) and removes one text of `campus_text.py`. No change to the server, `story.py`, `logic.py`, `db.py`, `game.py` or `app.py`.

## Before writing the spec

- **Product and user:** a player of the 3D game who reaches an ending.
- **Before:** the ending screen showed "Endings found: 1/2 🏆 🔒", and the share text and the share card repeated it. With only two endings (specs/three-proofs.md) the count makes no sense.
- **Rule (decided by the team):** no count of endings anywhere.
- **After:** the ending screen, the share text and the share card have no "Endings found" line (`collectionCount`, `collectionText`, the paragraph `ending-collection`, its styles and the text `collection` are removed). The list of endings seen is still kept in this browser (`plot-twist-endings`), because the fifth figure on the case file reads it (specs/earlier-nights.md, point 6).

## Reviewed tests that change

- `tests/test_no_endings_on_start.py`: the ending screen no longer shows the endings found (was: it still did).
- `tests/test_campus_people.py`: the page no longer has `collectionText`.

## Done when

- [ ] Every test passes, and the `.cjs` checks.
- [ ] In the browser: the ending screen, the share text and the share card show no count of endings.
