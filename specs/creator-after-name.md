# The detective and a closing-time warning as steps after the name, a cleaner case file, and the panel says where you are

Four small changes to the 3D game. No change to the rules (`story.py`, `logic.py`, `db.py`, `game.py`, `app.py`), to the server's answers, or to any reviewed test. Every text exists in Portuguese and English.

## Before writing the spec

- **Product and user:** a player of the 3D game, from the first screen to walking around the campus.
- **Before:**
  1. Under the photo of the case file there is a caption "PROVA 01 · Fotografia do grupo" / "EVIDENCE 01 · Group photo" that adds nothing, and the top bar of the case file says "Caso #005" / "Case #005", which means nothing to a new player.
  2. The case file shows the name field, the device choice and the whole "Your detective" creator at once: a long screen, and the player dresses a detective that has no name yet.
  4. The game starts without saying that the faculty closes in 30 minutes; the mission and the group are squeezed into the case file, next to the name.
  3. When the character walks out of a room (into the corridor or out to the entrance), the side panel still shows the saved room ("Sala de estudo") and its description.
- **After:**
  1. The caption is gone, and the top bar of the case file (and of the detective step) shows the name of the game: "O quinto elemento" / "The Fifth Element".
  2. The case file (step 2) asks for the name and the device; its button is "Seguinte →" / "Next →". It opens a new **step 3, "O teu detetive" / "Your detective"**, with the creator and its 3D preview, a back button "← O caso" / "← The case", and the button that starts the game. Without a name, "Seguinte" does not move on and says "Escreve primeiro o nome do teu detetive." / "Write your detective's name first.". Enter in the name field does the same as "Seguinte".
  4. After the detective step ("Seguinte →" / "Next →") comes **step 4**: a warning "A faculdade fecha às 22:45" / "The faculty closes at 22:45" ("São 22:15. Tens 30 minutos para recolher as provas e mostrá-las ao professor, no auditório, antes de o segurança fechar as portas." / "It is 22:15. You have 30 minutes to gather the evidence and show it to the professor, in the auditorium, before the security guard locks the doors."), then the mission and the group, moved here from the case file. "← O teu detetive" / "← Your detective" goes back; "Começar / Continuar" starts the game. The warning is only for a **first game**: once a name has started a game in this browser, the detective step starts the game directly (the browser keeps a note for each name, like the look). The order is: language → case file (name) → detective → warning → game.
  3. Outside the saved room, the panel's heading names the place where the character stands: "Corredor" / "Corridor", "Exterior" / "Outside" on the entrance plaza, or the title of the room whose door it is in. The room's description is hidden until the character walks back in. The saved room on the server does not change.

## What

- [ ] `prototypes/campus-3d/page3d.py`: no `evidence` and no `case` text; `game3d.html`: no `evidenceCaption`, and `caseNo` shows the game's title (the generated `campus3d.html` follows when `page3d.py` is run).
- [ ] `prototypes/campus-3d/play.js`: the creator moves to a new `#stepLook` section after `#stepCase`; `window.campusNext` checks the name and opens it; `#look-start` calls `window.campusStart`; errors before the game go under the step on screen.
- [ ] `game3d.html`: the case file's button calls `window.campusNext` when it exists.
- [ ] `campus_text.py`: `next_step`, `look_back`, `name_needed` in both languages.
- [ ] `play.js`: a `#stepBrief` section after `#stepLook` with the warning and the `#mission` box; `#look-start` opens it and `#brief-start` calls `window.campusStart`; `campus_text.py`: `brief_label`, `brief_title`, `brief_text`, `brief_back` in both languages.
- [ ] `game3d.html` `updateInside` also keeps `window.campusHere` (room id, `"outside"` or `null`) and tells the page when it changes; `play.js` `applyInside` uses it for the heading and hides `#scene-paragraphs` outside.

## Done when

- [ ] Existing tests pass unchanged.
- [ ] `tests/test_creator_after_name.py` checks the points above.
- [ ] In the browser: the case file has no caption and its top bar says "O quinto elemento"; "Seguinte" with an empty name shows the message; with a name it opens the detective step; "← O caso" goes back; "Seguinte" on the detective step opens the warning with the mission and the group; only its start button starts the game; walking out of the study room changes the heading to "Corredor" and back to "Sala de estudo" on return.
