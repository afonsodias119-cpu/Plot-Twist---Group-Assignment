# The professor before the podium

Extends specs/more-to-find.md (point 7, things to look at with K). Only the 3D page (`prototypes/campus-3d/game3d.html`) changes. No change to the story, the rules, the server or any reviewed test.

## Why
In the auditorium the spot to read the podium was right in front of it, and the professor stands beside it. K chooses the nearest one, so a player walking up to the professor to present the evidence was offered "Press K to look at: Podium" instead of talking to him, and could think the hearing was not possible.

## What
1. **A person comes first.** When a person of the room is close enough to talk to (2.4 m), K talks to that person; the things to look at are not offered at that moment. Rita and Leonor walking behind the player (`followers`) do not count, otherwise they would hide every thing. Things that are used (computer 12) are not people and do not hide anything.
2. **The podium spot moves** to the side of the podium away from the professor (x 5.0, z 9.2), more than 2.4 m from him, so the note on the podium can still be read.

Unchanged: the auditorium opens only when every clue is done or lost; talking to the professor offers "Present the evidence to the professor", which starts the hearing.

## Done when
- Existing tests pass unchanged (each spot stays at least 1.2 m from every person).
- New tests (`tests/test_professor_before_podium.py`): a near person (not a follower, not a usable thing) skips the things to look at; the podium spot is more than 2.4 m from the professor.
- A browser check: in front of the podium K offers the professor; beside the podium K offers the podium.
