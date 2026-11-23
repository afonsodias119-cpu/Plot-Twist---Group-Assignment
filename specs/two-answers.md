# Two answers on every line of Tomás and Rita, and no "Show evidence" in the print shop and the computer lab

Changes specs/evidence-and-hearing.md (point 5), specs/continuous-conversations.md and specs/trust-has-consequences.md, in the 3D game. No change to `story.py`, `logic.py`, `db.py`, `game.py`, `app.py` or the `confront` operation. Every text exists in Portuguese and English.

## Before writing the spec

- **Product and user:** a player of the 3D game talking to Tomás and Rita.
- **Trigger:** any line of a conversation.
- **Before:** every line of every person has a "📁 Show evidence" row; Tomás's lines offer from one to five answers (and the kept topics of earlier lines); Tomás and Rita give in only when the right card is shown.
- **Rule:** no "Show evidence" in the conversations of the print shop (the clerk) and the computer lab (Tomás, computer 12); everywhere else (Rita, Leonor, the professor, Duarte, the security guard) it stays. Each line of Tomás offers exactly two answers, a right one (✓) and a wrong one (✗). On a line where someone says something false, the right answer reminds them of a proof and makes them give in.
- **After:**
  1. **Tomás**, in this order: "Ask kindly what he is doing here" (`kind`) → "Ask who it was" (`who`) → "Ask for the password of computer 12" (`password`) → after the files, "Ask who made the slides" (`slides`); before the files, holding the original photo, "Show him the original photo" (`photo` → `help`). Each line's wrong answer leads to his offended line (`hard`), where "Apologise" (`calm`) brings back "Ask kindly…". On `slides`, the right answer ("Remind him the file history has his name on every version of the slides") makes him give in exactly as the card `files` did (he guards the lab door, and his word counts for the true ending); the wrong one ("Tell him that then the credit is Duarte's") leaves him convinced (`convinced`). The question about message 5 is gone (the chat is gone). His lines are not changed; the new wrong answers cost nothing (only the two rude answers of before cost 5 minutes). The memory answer of night 2 (↺) stays as a third answer on his first line.
  2. **Rita**, two answers on every line too, in this order: "Ask where the USB stick is" (`pen`) → "Ask about the group photo" (`photo`) → "Ask why the photo in the folder shows five" (`five`, her claim line) → "Ask what she remembers about Duarte" (`duarte`) → "Say you think the name was added last night" (`warned`) → after the files "Ask about the chat messages" (`chat`), before them "Tell her you will go and find proof" (`promise`). On `five` the right answer reminds her of the original photo (when it is held) or of the file history (otherwise, once the files are seen) and makes her give in; with no proof yet it moves on to Duarte; the wrong one agrees with her (`counted`, from where Duarte is the right answer). Every wrong answer upsets her (`upset`: "You do not have to talk to me like that…"): "Apologise" (`sorry`) brings back the USB stick question, "Say you are only being honest" ends the talk (`closed`). Rita has no trust level, so no answer of hers costs time. Her memory answer of night 3 (↺) stays as a third answer on her first line.
  3. **The page** shows no evidence row for the clerk, Tomás and computer 12 (`NO_EVIDENCE`); it stays for everyone else, and the security desk is not changed. A right answer that makes someone give in (`crack` in the answer) is sent as `confront` with its card, and is shown as the player's message. Tomás's and Rita's lines keep no topics from earlier lines (`TWO_ANSWERS`), and a right answer chosen before is offered again (after an apology).
  4. **Trust:** a hostile Tomás no longer lies (his lie was on the message-5 line). Leonor's lie stays.

## What

- [ ] `prototypes/campus-3d/campus_people.py`: Tomás's answers; `convinced`; no `msg5`; Rita's answers and her new lines `counted`, `promise`, `upset`, `sorry`, `closed`; `offered` passes `crack`; Tomás's entry of `LIES` removed.
- [ ] `prototypes/campus-3d/play.js`: `NO_EVIDENCE` hides the evidence row for the clerk, Tomás and computer 12; `TWO_ANSWERS` in `showLine`; an answer with `crack` calls `confrontWith(line, card, true)`.
- [ ] `docs/guiao-conversas.md`: Tomás and Rita with ✓ and ✗.

## Reviewed tests that change

Approved by the team.
- `tests/continuous-conversations.cjs`: Tomás and Rita keep no topics; their two answers each time; the right answer of a claim line is sent as a card; the checks of kept topics use Duarte instead of Rita.
- `tests/test_campus_people.py::test_the_right_items_unlock_more_answers`: the photo and the slides are offered after the password; no `msg5`.
- `tests/test_evidence_and_hearing.py`: the slides are asked after the password; no `msg5`. (The page test of the tray is unchanged: the tray stays.)
- `tests/test_trust_has_consequences.py`: Tomás's lie is gone (the table, the hostile Tomás test, `test_cracking_forgives`, the count of texts).
- `tests/test_night_schedule.py`: routes 7, 9 and 11 ask Tomás in the new order; route 11 now fits up to 34 seconds a command and no longer at 35.

## Done when

- [ ] Every test passes, and `node tests/continuous-conversations.cjs`.
- [ ] `tests/test_two_answers.py`: at most two answers on every line of Tomás and Rita whatever is held; the orders of Tomás and Rita; the right answer names a card that breaks the claim; Tomás gives in through it; "Show evidence" is gone only for the clerk, Tomás and computer 12, and the guard is not touched.
- [ ] In the browser: Tomás's conversation shows two answers on each line in that order, and the right answer on the slides makes him give in.
