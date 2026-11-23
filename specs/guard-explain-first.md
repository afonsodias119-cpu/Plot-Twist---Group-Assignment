# José first hears why you came

Changes specs/security-desk.md and specs/evidence-after-monitors.md (on the page only). No change to the server, `story.py`, `logic.py`, `db.py`, `game.py` or `app.py`. No reviewed test changes. Every text exists in Portuguese and English.

## Before writing the spec

- **Product and user:** a player of the 3D game talking to José, the guard, before he is convinced.
- **Trigger:** opening the conversation with José.
- **Before:** his first line offers two answers, "Explain the situation" and "Ask about the monitors". Asking about the monitors first gets "But first tell me why you want footage": the answer itself says it came too early. After "Explain the situation" the only answer left is "Demand the footage".
- **Rule:** an answer is offered only when it makes sense (as in specs/actions-when-they-make-sense.md). José has to hear why you came before talking about his cameras.
- **After:** his first line offers only "Explain the situation". Once the player has explained, he asks for a proof, and the answers are "Ask about the monitors" and "Demand the footage" (2 minutes, as before), each until it is chosen. His answer about the monitors no longer asks why you want footage: it says he still needs the proof.

## Why

As a player, I want José's answers to follow the conversation, so that I am never offered a question he will refuse to answer yet.

## What

1. `play.js`, `guardMenu`: before he is convinced, only `opt_explain` while "explain" has not been asked in this conversation; after it, `guardFollowUps` (below). The menus once he is convinced, wired or has given the footage do not change.
2. `play.js`, `guardFollowUps(t)`: `[{ label: t.opt_broken, next: "broken" }, { label: t.opt_rude, next: "rude", cost: 2 }]`. The lines `explain`, `broken` and `rude` offer them; a question already chosen is not offered again (the conversation's own rule).
3. `campus_text.py`, `security.broken`, both languages:
   - en: "The monitors have had no signal since last night. Somebody unplugged the cables behind the rack, and it was not me. And I still need to see a proof before I let you near them."
   - pt: "Desde ontem à noite que os monitores estão sem sinal. Alguém desligou os cabos atrás do rack, e não fui eu. E continuo a precisar de ver uma prova antes de te deixar chegar perto deles."
4. "Show evidence" keeps its rule (specs/evidence-after-monitors.md): it appears after "Explain the situation".

## Limits

- "Explain the situation" is remembered for the open conversation only, as every answer is: closing the conversation and talking to José again starts with "Explain the situation" again.

## Out of scope

The cables, the recordings, the server, the other people.

## Done when

- [ ] Existing tests pass unchanged, and `node tests/continuous-conversations.cjs`.
- [ ] `tests/test_guard_explain_first.py`: the first menu, the follow-ups and where they are offered, the cost kept, the new text in both languages without "why you want footage", and the unchanged menus after he is convinced.
- [ ] In the browser: José's first line shows only "Explain the situation"; after it, "Ask about the monitors" and "Demand the footage"; the monitors answer says he still needs a proof; showing the photo still convinces him.
