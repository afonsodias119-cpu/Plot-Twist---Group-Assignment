# "Show evidence" in the hearing

Changes only the page (`prototypes/campus-3d/play.js`, `showHearing`). No change to the server, `story.py`, `logic.py`, `db.py`, `game.py` or `app.py`.

## Before writing the spec

- **Product and user:** a player of the 3D game in the hearing, when Duarte makes a claim.
- **Before:** the proofs held are shown straight away as answers under the claim. The auditorium is always open (specs/three-proofs.md), so a player who comes with no proof sees only "Say nothing" and no way to show anything.
- **Rule:** the hearing answers like every other conversation: "📁 Show evidence" and "Say nothing".
- **After:** under the claim, "📁 Show evidence" / "📁 Mostrar uma prova" and "Say nothing". "Show evidence" opens the tray "What do you show?" with the proofs held (each one answers the claim, as before), or "You have nothing to show yet." when there are none, and "Put it away" goes back to the claim. The server is unchanged: the answer is still the card's id or "concede".

## Reviewed tests that change

None.

## Done when

- [ ] Every test passes, and the `.cjs` checks.
- [ ] `tests/test_hearing_show_evidence.py`: the hearing card has the button, the tray, the empty line and the way back.
- [ ] In the browser: in the hearing, "Show evidence" opens the proofs (or says there are none); a proof answers the claim; "Put it away" goes back.
