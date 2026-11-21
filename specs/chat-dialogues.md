# Chat-style conversations and room plaques

Extends specs/campus-people-and-atmosphere.md. Only what is on the screen and the dialogue data change: no change to `story.py`, `logic.py`, `db.py`, `game.py`, `app.py`, the server rules or any reviewed test.

## Why
The conversations show only the last line and a list of buttons, and every answer offers "Ask something else", so talking feels like a menu, not a conversation. The room names float as round amber pills with an emoji, which does not look like a building.

## What
1. **Conversations look like a messaging app.** The conversation card keeps the whole conversation as message bubbles: what the person says on the left, what the player chose on the right, each with the time of the game clock (`state.clock`). While the answer is on its way, a "typing…" bubble is shown. The header has a round avatar with the person's initial, the name and the trust hearts. The answers are reply buttons under the messages. Closing the conversation (or talking to someone else) starts an empty one next time.
2. **No "Ask something else".** Every "Ask something else" / "Perguntar outra coisa" answer is removed from `campus_people.py`, in both languages. Every line still offers at least one answer (a question that goes on, or goodbye), and "End conversation" is always in the header. To ask about something else, the player talks to the person again (K). After an action done in a conversation, the person answers with its result and only "Goodbye" is offered (the "Continue the conversation" answer and its `talk_continue` text are removed).
3. **Room plaques.** The room names over the doors are plaques like the signs of a real building: a small room number (`code`: 0.01 to 0.05) over the name in capitals, a thin amber edge, no emoji. The names of the people are small dark name tags.

## Out of scope
New dialogue lines, saving conversations, changing who says what, the room card of the visual walkthrough (hidden in the playable game), anything on the server.

## Done when
- Existing tests pass unchanged.
- New tests (`tests/test_chat_dialogues.py`): no answer in either language is "Ask something else" / "Perguntar outra coisa"; every line still offers an answer; `talk_continue` is gone from the texts and from `play.js`; the playable page has the message log and the bubble styles; the room signs carry a code and no emoji.
- A browser check shows a conversation with bubbles on both sides, the typing bubble, the reply buttons, and the new plaques.
