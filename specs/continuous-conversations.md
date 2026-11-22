# Continuous conversations

## Why
The player currently has to close and reopen a conversation to ask about a different subject.

## What
Keep the current conversation and its message log open after each response. Show its immediate
follow-up answers first, followed by unasked topics from the opening menu. Remember the factual
follow-up topics Tomás reveals in `kind` (witness, password, chat message), so asking one does not
hide the others. Do not retain context-specific reactions such as apologising or insisting once
that exchange has moved on. Never replay the opening line when returning to its menu within the
same conversation. Keep story actions available after their results by refreshing them from the
server without repeating the greeting. Reset the topic list when closing or switching people.
Respect `closed` conversations, conditional clues, time penalties and game endings. Computer 12
keeps its existing code flow. Do not change the mystery, dialogue texts or reviewed tests.

## Done when
Rita can answer about the photo then Duarte in one log; Tomás can discuss the witness then the
password without closing; Leonor keeps other topics after an answer; a closed conversation offers
no further questions; conditional topics remain hidden until the server offers them. Existing
Python checks and a JavaScript interaction test pass.
