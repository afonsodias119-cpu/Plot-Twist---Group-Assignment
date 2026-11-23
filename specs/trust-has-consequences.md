# Trust has consequences: people you were rude to answer less, warn the others, or lie

> **Update (specs/computer-lab-backup.md):** the lies of a hostile Tomás and Leonor are now contradicted by the backup of the original conversations (and Rita's `chat` line), not by an arrival line in the chat. Leonor is no longer cracked with a card.

Extends specs/harder-campus.md (the six rude answers cost 5 minutes), specs/campus-people-and-atmosphere.md (trust 0-3 on each line), specs/cleaner-interface.md (no hearts), specs/continuous-conversations.md, specs/evidence-and-hearing.md and specs/night-schedule.md. No change to `story.py`, `logic.py`, `game.py`, `app.py`, `db.py` or any reviewed test. `talk` still writes nothing. Texts in design-notes/texts-ideas.md, part A.

## Why
A rude answer costs five minutes, and then the world forgets it: the next time you talk to the same person they greet you as if nothing happened. Rudeness should change the night, not only the clock, and the player should learn that from what people say, never from a number.

## What
1. **A hidden temper.** Leonor, Tomás and Duarte (the three people with rude answers) each have a temper tonight, worked out from the night's notes: **calm** (no rude answer to them), **wary** (one), **hostile** (two or more, for example "Say she is lying" then "Insist"). An apology does not undo it. A person who has been **cracked** (the right card on their claim, specs/evidence-and-hearing.md) is calm for the rest of the night whatever was said: the proof showed you were right. Rita, the clerk and the professor have no rude answers and are always calm. The temper is never sent to the page: no new field in any reply, no number, no hearts; the existing `trust` of each line is sent as before and still not shown.
2. **New operation `rude`**, with exactly `operation`, `player`, `language`, `npc`, `node`. It is a `talk` that is also remembered: the page sends it, instead of `talk`, when the player chooses an answer that has a `cost`. `node` must be the `next` of an answer with a `cost` in that person's tree (`harsh` and `closed` for Leonor, `hard` and `closed` for Tomás, `know` and `closed` for Duarte); then it makes the same checks as `talk` (the person is here, the line can be reached now, no ending, no hearing, not 22:45) and raises the same `ValueError`s. When accepted it adds one to the note `rude` of that person (`{"tomas": 2}`, never above 2) and replies exactly like `talk`, with the new temper already applied. It charges nothing: the page still takes the 5 minutes (`if (option.cost) penalize(option.cost)` is untouched).
3. **The note.** `campus_evidence.read_night` keeps `rude` only as a dict whose keys are `leonor`, `tomas` or `duarte` and whose values are the ints 1 or 2; anything else is dropped. `write_night` writes it when it is not empty. A restart or a new game forgets it with the night.
4. **Wary or hostile: shorter answers.** `campus_people.temper(reply, moods, language)` changes only the text and the note of the line, never its answers or its actions, so the kept topics of specs/continuous-conversations.md stay exactly as they are.
   - Curt lines (a short text, the same note, so a clue in the diary is never lost): Tomás `start`, `kind`, `password`, `who`; Leonor `start`, `messages`; Duarte `start`, `part`. Tomás's `who` is curt, not withheld, because in the `rita` case of specs/archive/culprit-of-the-night.md its note is the second sign against the culprit: the case's version of the note reaches the diary even after a rude answer.
   - Withheld lines (a short text and no note: the hint is not given): Tomás `help`, Leonor `mine`, Duarte `slide`. These are hints only; every clue needed for an ending has another source.
5. **Hostile: one lie each, which the player can check.**
   - Tomás, line `msg5`: he says he wrote the message with his name himself, three weeks ago. The message's own arrival line ("arrived yesterday, 11:49 pm") and Rita's `chat` line say otherwise. Believing him costs the flag of that message, and so `full_case`.
   - Leonor, line `messages` (instead of its curt text): the messages arrived on their dates, weeks ago. The same arrival line and Rita's `chat` line contradict her.
   - Duarte lies anyway: hostility adds no lie of his own.
   A lie has its own note, which the diary keeps like any other line: it is what you were told. A lie is not a claim: a card shown on it gets the person's usual rebuff and minutes, so the lie is beaten by not believing it.
6. **Hostile: a warning that spreads.** While a person is hostile, the next person in the chain greets the player with a different first line (the `start` text), for the rest of the night: Tomás warns Leonor, Leonor warns Rita, Duarte warns the professor (`WARNS = {"tomas": "leonor", "leonor": "rita", "duarte": "professor"}`). Only the first line changes: the warned person's answers, actions, claim and decisions are as before. Once the warner is cracked, the warning stops.
7. **Which text wins.** For `start`: the warned line, else the curt line, else the story's. For `messages`: the lie when Leonor is hostile, else the curt line when wary. A trust text never names the culprit, a date or a code, so it is never a key of specs/archive/culprit-of-the-night.md and it wins over the case's text; the names of specs/your-own-group.md are still replaced in it.
8. **What does not change.** Claim lines (`slides`, `five`, `sure`), story actions (the copy, Leonor's two decisions, computer 12, the hearing), the code rule (Tomás's `password` is only curt), every cost, the schedule (Leonor still leaves at 22:30 if undecided, a hostile Tomás who is cracked still stands in the lab door), the hearing and its caps.
9. **The page.** `talkStep(npc, node, rude = false)` sends `operation: rude ? "rude" : "talk"`; the click handler of an answer passes `Boolean(option.cost)` on the line after the pinned `penalize` line. The fake page of tests/continuous-conversations.cjs ignores the third argument. Nothing new is drawn.
10. **Files.** `campus_people.py` (`COLD`, `WITHHELD`, `LIES`, `WARNS`, `WARNED`, `temper`; the same keys in `en` and `pt`), `campus_evidence.py` (the note, `moods(night)`), `campus_game.py` (`rude` in `allowed_fields`, with `talk` in `closed_reply` and the hearing lock; `temper` on every `talk` and `rude` reply), `play.js`, `campus_text.py` (the "conversations" item of `howto_items` says a rude answer is remembered), `docs/guiao-conversas.md`.

## Reviewed tests that change
None. `talk` keeps its fields and still writes nothing; with no `rude` note every temper is calm and `temper` returns the reply unchanged; `PEOPLE` is not touched (the new texts are in their own tables), so the six costs, the node shapes and the trust values compared by the reviewed tests stay the same.

## Limits
- A hand-made client that sends `talk` instead of `rude` is never remembered as rude, as it already skips the page's 5 minutes. It only helps itself.
- The withheld lines can still be asked for by hand: they answer with the short text and no note.
- The warning chain is fixed; it does not follow the order in which the player meets people.

## Out of scope
Showing trust, earning trust back by being kind, temper for Rita, the clerk or the professor, the plain game.

## Done when
- Existing tests pass unchanged, and `tests/continuous-conversations.cjs`; `play.js` passes `--check`.
- The tests below were written first and pass.
- A browser check in both languages: "Say she is lying", "Apologise": Leonor's next greeting is curt; "Insist": Rita's first line mentions it; Tomás pushed twice tells the lie at `msg5`, and the chat's arrival line contradicts it.

## Checks
`tests/test_trust_has_consequences.py`, written before the code; "saves nothing" means the same database bytes.
- `test_talk_still_saves_nothing_after_rudeness`: `talk` to `harsh` saves nothing and changes no later line.
- `test_rude_is_a_talk_that_is_remembered`: the reply has the same keys and text as `talk`; the note `rude` is `{"leonor": 1}`, then 2, never 3.
- `test_rude_only_for_the_targets_of_a_costly_answer`: `rude` to Leonor's `soft`, to Rita, to the clerk, an extra field, a person not here: `ValueError`, saves nothing.
- `test_wary_gives_curt_lines_with_the_same_note`: Tomás's `password` after one rude answer: the curt text, the story's note, the same options.
- `test_wary_withholds_hints`: `help`, `mine`, `slide`: curt text and no note.
- `test_hostile_tomas_lies_about_his_message_and_the_chat_says_otherwise`: the lie text and note; the chat message with his name still shows its arrival line.
- `test_hostile_leonor_lies_about_the_messages`.
- `test_the_warning_reaches_the_next_person_only`: Tomás hostile → Leonor's `start` changes, Rita's does not; Leonor hostile → Rita's; Duarte hostile → the professor's.
- `test_cracking_forgives`: Tomás hostile, then `msg_5` on `slides`: his lines and Leonor's greeting are back to normal.
- `test_claims_actions_and_the_code_rule_never_change_with_temper`: options, actions and the claim lines are equal calm and hostile; the code still unlocks.
- `test_a_damaged_rude_note_counts_as_calm`: `"yes"`, `{"rita": 2}`, `{"tomas": 7}`, `{"tomas": true}`.
- `test_no_reply_ever_carries_the_temper`: no key `rude`, `mood` or `temper` in a snapshot or a `talk` reply.
- `test_the_trust_texts_have_the_same_keys_in_both_languages_and_name_no_culprit_date_or_code`: no `14`, `10 November`, `1411`, "account", "confess".
- `test_the_page_sends_rude_for_costly_answers`: `play.js` has `rude ? "rude" : "talk"` and still has `if (option.cost) penalize(option.cost)` and `operation: "talk"`.
