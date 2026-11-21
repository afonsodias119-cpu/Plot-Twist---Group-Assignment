# Campus 3D: people, dialogues, clock, diary, chat, sounds and light

Extends specs/playable-campus-3d.md and specs/campus-3d-streamlit.md. No change to `logic.py`, `story.py`, `db.py`, `game.py`, `app.py` or any reviewed test.

## Why
The 3D campus has the mystery but little life: three silent characters, and the group chat puzzle (specs/spot-the-fake.md) only works in the plain app. This adds people to talk to, a clock, a diary, the chat in 3D, and sound and light.

## What
1. **People in every room.** Rita (study room), the print shop clerk Amélia, Leonor (library), Tomás (computer lab), the Professor and Duarte (auditorium). Walking up to a person (about 2.4 units) shows a note "Press the K key to talk to <name>" over the picture; the key starts the conversation, also with the side panel hidden. The panel still lists "Talk to <name>" for the people in the saved room (it works from anywhere, because talking only reads the saved game), and it is the only way in text mode. The "play without 3D" button was removed; the text mode still starts by itself when the 3D scenery cannot load.
2. **Dialogues with choices.** A conversation is a small tree in `campus_people.py` (English and Portuguese, same ids and conditions). The page shows what the person says and 2–3 answers to choose from. Answers can be offered only when the player has the right item or has viewed the old files (`if`). Some people have trust (0–3): a kind answer keeps it, a hard one lowers it, and at 0 the person ends the conversation. Hints never reveal a clue the player has not found yet.
3. **Server rule.** New operation `talk` (`player`, `language`, `npc`, `node`). It reads the saved game, checks that the person is in the saved room and that the node's condition holds, and returns the node. It never writes anything: conversations do not change the saved game or the endings; the decisions stay the story's own actions.
4. **Clock.** `clock` in the snapshot is computed from the saved state: 22:15 plus 40 minutes for each clue done and 5 for each flagged chat message. It is shown beside the title. It never ends the game.
5. **Diary.** A third phone app. It shows the notebook (already in the snapshot), the chat messages the player flagged, and what people told them (kept in this browser only, `localStorage`, never trusted by the server).
6. **Group chat in 3D.** The `group_chat` scene is played inside the computer lab: the snapshot sends `room` (the 3D room of the saved scene), the panel shows the messages and the flag buttons. Walking between rooms uses the shortest path of the story's own `go_` actions.
7. **Sound.** Generated in the browser (Web Audio, no files): sea outside, footsteps, soft clicks, a chime for a new item, a low tone for a refusal. Starts after the first click; a button mutes it and the choice is remembered.
8. **Light.** Entering the auditorium dims the corridor lamps and lights the stage; leaving restores them.

## Reviewed tests that change
One test of the reviewed file `tests/test_campus_3d.py` changes because the requirement changes: `test_the_3d_campus_offers_only_rooms_it_can_draw` (written for the group chat puzzle) said the 3D campus never offers the chat. It becomes `test_the_group_chat_is_played_inside_the_computer_lab_in_3d`. The author of that test (Guilherme) must approve the change in the pull request. No test is skipped or deleted.

## Out of scope
A real time limit, saving conversations on the server, new endings, changing the story's rules or texts.

## Done when
- Existing tests pass unchanged.
- New tests cover: both languages have the same dialogue structure; `talk` only in the person's room, with unknown npc/node/extra fields rejected and no write; options hidden until their condition holds; trust reaching 0 ends the talk; the clock; `room` for the chat; walking from the chat to another room; the chat flags in the diary without telling which are fake.
- A browser check shows the people, a full conversation with choices, the diary, the clock, and no script errors.

## Interface update (same feature)
- The investigation actions are **choices inside the conversation** with the person of the room, not buttons on the screen: Rita (open the group drawer), Amélia (ask for a copy of the original order), Leonor (the two decisions, marked as decisions), Tomás (look at the old files, open the group chat) and the Professor (present the evidence). `talk` returns them as `actions` (id, label, allowed, blocked_text, decision); choosing one runs the story's own action through `play`, and the person answers with its result. A blocked action is still offered; choosing it shows the reason and changes nothing. While the character is outside the room these choices are disabled. The mapping is `ACTION_PERSON` in `campus_people.py`; each action row of the snapshot has `person`.
- Only the group chat flags (reading the messages on the computer) have no person, so they stay as buttons over the picture, which step aside while a conversation is open.
- The "hide panel" button is gone. The panel has a small arrow on its edge (› closes it, ‹ opens it). The panel starts open and the last choice is remembered in this browser.

## Computer 12 and the chat screen (same feature)
- Computer 12 (the right-hand screen of the sixth desk of the lab) is an object the player uses, not a person: walking up to it shows "Press the K key to use computer 12" (the panel lists "Use Computer 12"). Looking at the old files and opening the group chat are choices in its menu (`ACTION_PERSON`), no longer asked of Tomás.
- In the group chat the five messages are shown on a computer screen over the 3D picture, each with a "Flag as fake" button, so the side panel does not have to be open. The snapshot has `chat` (the intro and the five messages with their flagged state, never which are fake) only in the chat scene; the flag actions have `kind: "chat"`. "Close the computer" (or Esc) goes back to the lab.
