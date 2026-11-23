# The security desk: a guard, five cables and last night's recordings

Extends specs/evidence-and-hearing.md, specs/harder-campus.md and specs/campus-people-and-atmosphere.md. **Phase 1: everything is on the screen.** No change to `story.py`, `logic.py`, `db.py`, `game.py`, `app.py`, the server (`campus_*.py` other than the texts) or any reviewed test, so it cannot clash with the work on the server side.

## Why
The game has no way to see who was in the computer lab at 23:47 (the moment the group folder was changed from computer 12). A security guard with cameras gives the player a proof to go and get, with a new kind of action (plugging in cables) that none of the other rooms has: the study room is a search by clicking, the print shop is a jigsaw, computer 12 is a code, the chat is reading.

## What
1. **A security desk next to the main entrance**, in the corridor (a desk, a wall of dark monitors on a rack, a lamp) with a guard, Anselmo. He is in the corridor, which belongs to every room, so the player can talk to him wherever the saved scene is. Walking up to him shows "Press K to talk to Anselmo" (or tap the note on a phone). He is on the screen only: the server does not know him.
2. **Convincing him.** He will not give recordings to anyone. The player explains the situation and has to show him a piece of evidence: the original photo (four people) or the old files (four authors) convince him; any other card is refused. A rude demand costs 2 minutes and a wrong card 1 minute (the page's own countdown, like a rude answer in a conversation). With no evidence at all he says to come back with some.
3. **The cables.** The cables of the cameras were unplugged on purpose just after 23:47 (he says so: it is a clue that somebody planned to hide the recording). A window shows five cables, each named after a room, and five monitor ports placed like the rooms on the plan of the building (print shop, study room and library above the corridor; computer lab and auditorium below it; the entrance on the left). The player picks a cable and then the port (click or tap, also with the keyboard). "Plug in" is enabled when every cable is linked; a wrong arrangement says how many are right, shakes with sparks and costs 1 minute; the right one lights the monitors of the 3D desk one by one.
4. **The recordings.** A window like an old security monitor: one tab for each camera (entrance and the five rooms), a bar for the minute (22:00 to 23:59, with one-minute buttons), grain, lines, "REC", the camera name and "YESTERDAY hh:mm:ss". There is movement only when something happened: at 23:38 a hooded figure comes in at the entrance, at 23:41 it comes in at the computer lab, and from 23:46 to 23:49 it sits at computer 12, whose screen glows. The player has to find that minute. There, a button "Keep this picture as proof" saves the proof in the diary (an entry "Security cameras"). The figure is drawn by the 3D scene (`campusFigure`, seen from the back, with no face).
5. **What is kept.** In this browser (`localStorage`, `plot-twist-security:<name>`), like the diary: `convinced`, `wired`, `footage` (each only true if it is exactly `true`). A new game forgets it. The monitors of the desk follow `wired`.

## Limits (phase 1)
- It is a puzzle, not security: the solution of the cables and the minute are in the page. The server does not know the result, so **the proof is not yet a card that can be shown to the professor**; it is a diary entry.
- The guard is reached by walking up to him (3D). The text-only mode has no way to him.

## Phase 2 (a separate pull request, only with the author of the hearing)
Make the picture an evidence card (`footage`) accepted at the professor's claim about the name. That needs a note in the night's notes, a card in `campus_case.py` and changes to tests of `tests/test_evidence_and_hearing.py` (the list of cards), so it must be reviewed by the person who wrote them.

## Out of scope
A new room, a new scene in the story, saving the result on the server, other guards.

## Done when
- Existing tests pass unchanged.
- New tests (`tests/test_security_desk.py`): the texts exist in both languages with the same keys; the monitor ports are placed like the rooms of the 3D building; only the photo or the old files convince the guard; the guard code never calls the server; a new game forgets it; what is read from the browser must be exactly `true`; the page has the desk, the cables and the recordings.
- A browser check shows: the note next to the guard, the conversation, the cables (wrong, then right), the monitors lighting up, the recordings and the saved proof.
