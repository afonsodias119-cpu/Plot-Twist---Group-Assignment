# Duarte only speaks in the hearing, and the professor can be reached

Changes the page only (`prototypes/campus-3d/play.js`, `game3d.html`). No change to the server, `story.py`, `logic.py`, `db.py`, `game.py` or `app.py`.

## Before writing the spec

- **Product and user:** a player of the 3D game in the auditorium.
- **Before:** Duarte stands near the auditorium door and is a person to talk to: K and the "Talk to Duarte" button open his conversation, and when he is the nearest person K talks to him instead of the professor. The aisle between the seats is 0.8 m of free floor for a character 0.6 m wide, so walking up to the professor is hard.
- **Rule (decided by the team):** the player never talks to Duarte. He speaks only in the hearing, making his claims to the professor.
- **After:**
  1. Duarte is never offered: no "Talk to Duarte" button, K never picks him (he is skipped when the 3D looks for the nearest person), and `talkStep` ignores him. He still stands in the auditorium, walks his rounds to the lab door and catches the player at computer 12 (specs/night-schedule.md).
  2. The aisle in the middle of the seats is wider: the three seats nearest the middle of each row are gone (free floor from x 5.46 to 7.84), and the collision blocks follow the seats that are left. The player walks straight from the door to the front of the stage, beside the professor.
  3. His conversation lines stay on the server, unused by the page, because reviewed tests of other features still read them (the memory answer, the rude answers). Removing them is a separate decision.

## Reviewed tests that change

To be approved by the team in the review of the pull request.

- `tests/test_night_schedule.py`: route 11 no longer talks to Duarte or shows him a card; "doing everything" leaves out his lines and his card (29 other commands) and still does not fit at 30 seconds; route 11 now fits up to 30 seconds a command and no longer at 31.

## Done when

- [ ] Every test passes, and the `.cjs` checks.
- [ ] `tests/test_duarte_only_in_the_hearing.py`: no talk button and no talk for Duarte, K skips him, the aisle and its blocks.
- [ ] In the browser: in the auditorium K never offers Duarte; walking up the aisle, K talks to the professor.
