# The professor, not the podium

Extends specs/more-to-find.md (point 7, things to look at with K). Changes `prototypes/campus-3d/campus_search.py` (the things to look at) and `prototypes/campus-3d/game3d.html`. No change to `story.py`, `logic.py`, `db.py`, `game.py` or `app.py`.

## Why
In the auditorium the spot to read the podium was right in front of it, and the professor stands beside it. K chooses the nearest one, so a player walking up to the professor to present the evidence was offered "Press K to look at: Podium" instead of talking to him, and could think the hearing was not possible. The team wants the auditorium to be only this: you get in when you have every piece of evidence, and you present it to the professor.

## What
1. **No podium.** The podium is no longer a thing to look at: `FINDS["auditorium"]` is empty, its texts are removed, and the 3D has no spot for it. The podium itself stays as furniture.
2. **A person comes first.** When a person of the room is close enough to talk to (2.4 m), K talks to that person; the things to look at are not offered at that moment. Rita and Leonor walking behind the player (`followers`) do not count, otherwise they would hide every thing. Things that are used (computer 12) are not people and do not hide anything.

Unchanged: the auditorium opens only when every clue is done or lost; talking to the professor offers "Present the evidence to the professor", which starts the hearing.

## Reviewed tests that change
- `tests/test_more_to_find.py` (Guilherme): `ROOM` and `FLAVOUR` lose `"podium"`; `FIND_TEXTS` loses the podium texts; the checks that used `"podium"` as an example use another thing (`"noticeboard"` after an ending, `"price_list"` during the hearing, which is refused before the room is checked); `"podium"` is added to the unknown things. The auditorium's `finds` are still checked (now an empty list). **Needs Guilherme's approval in the pull request.**

## Done when
- Existing tests pass, with the change above.
- New tests (`tests/test_professor_before_podium.py`): the auditorium has nothing to look at (server and 3D); a near person (not a follower, not a usable thing) skips the things to look at.
- A browser check: in front of the podium K offers the professor, and nowhere in the auditorium does K offer the podium.
