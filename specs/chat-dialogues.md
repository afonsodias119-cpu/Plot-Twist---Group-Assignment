# Chat-style conversations and room plaques

Extends specs/campus-people-and-atmosphere.md. Only what is on the screen and the dialogue data change: no change to `story.py`, `logic.py`, `db.py`, `game.py`, `app.py`, the server rules or any reviewed test.

## Why
The conversations show only the last line and a list of buttons, and every answer offers "Ask something else", so talking feels like a menu, not a conversation. The room names float as round amber pills with an emoji, which does not look like a building.

## What
1. **Conversations look like a messaging app.** The conversation card keeps the whole conversation as message bubbles: what the person says on the left, what the player chose on the right, each with the time of the game clock (`state.clock`). While the answer is on its way, a "typing…" bubble is shown. The header has a round avatar with the person's initial, the name and the trust hearts. The answers are reply buttons under the messages. Closing the conversation (or talking to someone else) starts an empty one next time.
2. **No "Ask something else".** Every "Ask something else" / "Perguntar outra coisa" answer is removed from `campus_people.py`, in both languages. Every line still offers at least one answer (a question that goes on, or goodbye), and "End conversation" is always in the header. To ask about something else, the player talks to the person again (K). After an action done in a conversation, the person answers with its result and only "Goodbye" is offered (the "Continue the conversation" answer and its `talk_continue` text are removed).
3. **Only what is said goes in a bubble.** A line is split by its quotation marks (the same rule the voices use, `partsOf` in `play.js`): what is between quotation marks is a speech bubble of the person; the rest (what the person does, for example "Rita looks up from her laptop.") is a short narration line in the middle of the conversation, outside the bubbles. A line without quotation marks (computer 12, the result of an action) is only narration.
4. **No scene description in the side panel.** In the 3D game the panel shows the room's title, the people and the actions, but not the description of the scene: the player has to look around and talk. The text mode (when the 3D cannot load) keeps the description, because there it is the only way to know where you are.
5. **Room plaques.** The room names over the doors are plaques like the signs of a real building: a small room number (`code`: 0.01 to 0.05) over the name in capitals, a thin amber edge, no emoji. The names of the people are small dark name tags.

## Out of scope
New dialogue lines, saving conversations, changing who says what, the room card of the visual walkthrough (hidden in the playable game), anything on the server.

## Done when
- Existing tests pass unchanged.
- New tests (`tests/test_chat_dialogues.py`): no answer in either language is "Ask something else" / "Perguntar outra coisa"; every line still offers an answer; `talk_continue` is gone from the texts and from `play.js`; the playable page has the message log and the bubble styles; the room signs carry a code and no emoji; the page splits lines into speech and narration; the scene description is hidden outside the text mode.
- A browser check shows a conversation with bubbles on both sides, the typing bubble, the reply buttons, and the new plaques.
