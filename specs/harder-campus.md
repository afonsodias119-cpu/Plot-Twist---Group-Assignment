# A harder campus: no list of missing clues, and 30 minutes before the faculty closes

Extends specs/chat-dialogues.md and specs/campus-people-and-atmosphere.md. No change to `story.py`, `logic.py`, `db.py`, `game.py` or `app.py`: the rules, the endings and the saved game stay the same.

## Why
The game is too easy. The locked auditorium door lists exactly which clues are missing, and choosing a rude answer in a conversation has no consequence: the player can talk again at once. The night also has no pressure: nothing ever runs out.

## What
1. **The door does not list what is missing.** Trying the auditorium too early only says "You do not have all the proof yet to face the professor." (`auditorium_note`), without the list of missing clues. `missing_clues_note` keeps its name: it returns that sentence while a clue is missing and an empty text once every clue is done. The `missing` text is removed. (The phone's "Clues" app is not changed.)
2. **A countdown: 30 minutes before the faculty closes.** When the player opens a game, a countdown of 30 minutes starts. It only goes down while the game is really being played (the page open and in sight, before an ending): closing the game pauses it, so a saved game can be continued later with the time it had. The night starts at 22:15 (the time on the case file), so the faculty closes at 22:45. The top of the screen shows the time left (`⏳ 29:41`), red in the last 5 minutes. The bubbles of the conversations and the messages from the unknown number show the campus time (22:15 plus the time already used), and the music gets faster as the time runs out. The time the server computes (`clock` in the snapshot) is not shown any more.
3. **A rude answer costs 5 minutes.** In `campus_people.py`, the answers that make a person lose trust have `"cost": 5`, in both languages: Leonor ("Say she is lying", "Insist"), Tomás ("Demand to know why he lied about Duarte", "Push harder") and Duarte ("Tell him you know the truth", "Press him"). `talk` returns the cost with the answer. Choosing one takes 5 minutes off the countdown, and a note says so.
4. **Time up.** If the countdown reaches 0 before an ending, the game stops: the conversation closes, the detective cannot move, and a card "The faculty is closed" explains what happened. Its only button, "Try again", starts a new game (the existing confirmed restart). Reloading the page shows the card again. Reaching an ending stops the countdown, and the share card shows the time that was left.
5. **Where the time is kept.** The time left, in this browser (`localStorage`, key `plot-twist-time-left:<player>`), like the diary and the messages. A new game gives 30 new minutes. A game that was never played (`fresh`) whose countdown already ran out also gets 30 new minutes. (A first version kept the closing moment instead, so the time ran out while the game was closed and a saved game could not be continued: fixed.)

## Reviewed tests that change
The requirement "the door lists every missing clue" changes, so two tests of the reviewed file `tests/test_campus_3d.py` change. Their author (Afonso) must approve the change in the pull request. No test is skipped or deleted.
- `test_entering_the_auditorium_is_refused_without_the_clues`: it checked that all four missing clues are named; it now checks that the message is exactly `auditorium_note` and names no clue.
- `test_the_story_rule_alone_is_not_enough_for_the_auditorium`: it checked which clues are named; it now checks that the message is exactly `auditorium_note`.

## Out of scope
Making the server know the time (a cleared browser or another browser gives 30 new minutes), a saved "time up" ending, changing the story, the rules, the endings or the phone's "Clues" app.

## Done when
- Existing tests pass; only the two tests above change, as described.
- New tests (`tests/test_harder_campus.py`): the door message names no clue and the `missing` text is gone; exactly the six rude answers cost 5 minutes, the same in both languages; `talk` returns the cost only for them; the countdown texts exist in both languages; the page has the countdown, the 30 minutes, the time-up card and the key of the time left, and the time only goes down while the game is running.
- A browser check shows the countdown, a rude answer taking 5 minutes off, and the time-up card.
