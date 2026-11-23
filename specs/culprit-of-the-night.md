# A different culprit some nights: Duarte alone, or a teammate who let him in

Extends specs/evidence-and-hearing.md, specs/spot-the-fake.md, specs/pen-and-code.md, specs/torn-photo.md, specs/night-schedule.md and specs/earlier-nights.md. The case is picked by specs/case-of-the-day.md (the date picks the variant; a saved game keeps it). No change to `story.py`, `logic.py`, `game.py`, `app.py`, `db.py` or any reviewed test: the game is always played with the story's own actions, flags and endings, and the campus layer only renumbers the chat and swaps texts on the way out. Every text is in design-notes/texts-ideas.md, part B.

> **Update (merge with specs/calendar-code.md):** computer 12 is now solved with the group, and its puzzle is the same in every case: the cover photo is from Saturday 17 October, the code is `1710`, the stamp 17.10, the slip on the shutter says 17 October, and the clerk no longer says the date. So no case has a code or a photo date of its own any more (the codes `1011` / `1311`, the stamps 10.11 / 13.11, the clerk's dated lines in the case texts, the `stamp` option of `photo.js` and `day.photo_date` are gone). What still changes per case: which chat messages are fake (and the order they are shown in), the account in the file history, who lies and the contradiction that gives them away, the confessions, the professor's lines of the hearing and the endings. No case text speaks of the day of the photo, so what Tomás, Rita and Leonor remember of it at computer 12 is true in every case.

## Why
Once a player knows that messages 2, 4 and 5 are fake, the mystery is over for them and for every friend they tell. Some nights Duarte should be exactly what he seems; some nights a teammate should have added him, and the clues should change to match, so that what you were told is not what you find.

## What
1. **Three cases**, in `campus_case.py` (server only, data only, like the rest of that file): specs/case-of-the-day.md created `CASES = {"outsider": ...}`; this spec adds `"tomas"` and `"rita"` (shape and texts in design-notes/texts-ideas.md, part B) and makes `campus_clock.CASE_ORDER = ("outsider", "tomas", "rita")`. Leonor is never the culprit: her decision (help or accuse) is the pivot of the story's endings, and it must stay honest.
   - `outsider`: the classic case, exactly as today. Duarte forged everything; no teammate lies on purpose.
   - `tomas`: Tomás let Duarte in. He never made his slides; Duarte, who repeats the course, promised to make them if his name went on the report. Tomás changed the report and swapped the photo at 23:47 from computer 12 and wrote the late message under his own name himself. He lies about being near computer 12 and about the slides.
   - `rita`: Rita let Duarte in. He needed a group with a good grade and she said yes without asking anyone. She changed the files at 23:47, from computer 12, and says she went home early; she says she does not know where the USB stick is.
2. **What each case changes** (the data of each case; `outsider` has the classic values):

   | | `outsider` | `tomas` | `rita` |
   |---|---|---|---|
   | chat as shown (position → story message) | 1 2 3 4 5 | 5 1 2 3 4 | 2 4 3 5 1 |
   | fake ones, as shown | 2, 4, 5 | 1, 3, 5 | 1, 2, 4 |
   | real messages | Leonor (room), Rita (photo) | Rita (room), Leonor (photo) | Tomás (room), Leonor (photo) |
   | the fakes | unknown number; Duarte "five"; late, under Tomás | Duarte "conclusion"; unknown number "five"; late, under Tomás (by Tomás) | unknown number; Duarte "five"; late, under Tomás |
   | the file history names the account | no | Tomás's | Rita's |
   | who lies | nobody on purpose | Tomás (`who`, `slides`, `msg5`) | Rita (`pen`, `duarte`, `warned`) |
   | date of the photo, code | 17.10, `1710` | 17.10, `1710` | 17.10, `1710` (the same in every case, specs/calendar-code.md) |
   | hearing, claim `name` accepts | `files` | `files`, `tomas_word` | `files`, `rita_word` |
   | the cracked teammate | witness / never wrote it | Tomás confesses | Rita confesses |

   The fake messages are always the story's messages 2, 4 and 5 and the real ones 1 and 3, so the story's endings (`full_case` needs exactly 2, 4 and 5 flagged) keep working; only their texts and the order they are shown in change. The tell of each fake is always on the screen: a sender outside the group (Duarte or an unknown number, weeks before anyone had heard of him), a message that counts five, or a late arrival line. The USB stick does not move: specs/hidden-object-table.md keeps it "always in the same place", half under the napkin, and moving it would put the case in the page. What changes around it is who says what about it.
3. **Shown numbers.** The page only ever sees the chat as shown. `chat_view` lists the messages in the case's order with `n` and `action` (`flag_<shown n>`) of the shown position; the flag rows of `actions` and the notebook titles (`Group chat · n`) use shown numbers too; the reply message of a flag is the story's own `result_text` of the shown number ("You flag message 3 for the professor."). `play` turns `flag_<shown>` into the story's `flag_<message>` before anything else. The cards of flagged messages are `msg_<shown>` in `evidence`, listed in the order they are shown, and `confront` and `hearing` turn them back before checking (`campus_evidence.story_card(card, night)` and `shown_card(card, night)`), so `CONFRONT` (`msg_5` breaks Tomás) is untouched. In the classic case every number is its own. So a friend who says "flag 2, 4 and 5" or reads `data-action` in the page source tells nothing.
4. **The code and the photo are the same in every case.** `unlock` compares with `campus_search.PC12_CODE` (`1710`) in every case. Tomás's rule (day and month of the cover photo), the group's memories at computer 12, the Weather and Calendar apps, the photo's stamp (17.10), the shutter slip and the clerk's lines are those of specs/calendar-code.md in every case: no case swaps them, and no case text (swapped or new) mentions that day, so a culprit's lie never touches what the group remembers.
5. **The hearing.** Duarte's three claims and the caps do not change. Every rule that reads `HEARING` reads `claims_of(night)` instead: `HEARING` itself for the classic case, with the case's `accepts` for the others (a confession of the person who added the name also breaks the claim "my name has been there since the first draft"). The professor's lines for the new pairs are in the case (`right`). `perfect_night` still needs both words, so the true ending is reachable in every case.
6. **Texts are swapped on the way out.** Each case has `texts = {"en": {classic text: case text}, "pt": {...}}`: the key is the exact classic text (from `story.py`, `campus_people.py`, `campus_case.CASE_TEXT`, `campus_clock.SHUTTER`, `campus_search.PHOTO_TEXT`, `campus_case.NIGHT_TEXT`), the value is what the case says instead. New `campus_evidence.retell(reply, night, language)` walks a reply (dicts, lists, strings) and, in every string, replaces each key by its value (`str.replace`, each key once, longest key first, so a value is never searched again); then specs/your-own-group.md replaces the names. `campus_game.command` calls it once, on every reply, after the operation has run (so it reads the notes as they are now). Reading writes nothing. A case text reaches the page exactly when its classic text would have: secrets stay on the server.
7. **What is swapped** (keys in design-notes/texts-ideas.md, part B): the four changed chat messages, the result of `view_files` and the lab's paragraph after it, the card labels `files`, `tomas_word` / `rita_word`, the reveals of Tomás, Rita and Leonor, the lines of the liar, Leonor's `mine`, Leonor's `messages` (text and note) and the professor's line for `leonor_messages` (no "number nobody knew", since a teammate sent fakes too), Duarte's `part`, the professor's lines of the new pairs, the endings `full_case`, `impostor`, `stolen_credits`, and one sentence of the true ending. `fifth_element` keeps its text in every case: it never says who added the name. A case text keeps the spoken quotes of the text it replaces, in number and speaker, so `ending_voices` and the true ending's `voices` still fit.
8. **Every case is fair.** Each clue needed for each ending is still findable: the USB stick (the table), the date (the group at computer 12 with the phone's Weather and Calendar, the slip, the stamp), the code rule (Tomás's `password`, never withheld by specs/trust-has-consequences.md), the file history and its account (computer 12), Leonor's decision, the three tells in the chat, and, for the culprit, two independent signs (the account, and the liar's story against another person's: Rita's "went outside before half past eleven, with his hood up" against Tomás's "never went near it"; Tomás's hooded figure with long hair under the hood and a pink sleeve against Rita's "went home early"). Both fit the recordings of specs/security-desk.md, the same in every case: a hooded figure comes in at the main entrance at 23:38 and enters the computer lab at 23:41. A rude answer to Tomás keeps his `who` note (it is a curt line, specs/trust-has-consequences.md, point 4), so the diary still holds the case's version of it.
9. **With the other ideas.** A line of specs/trust-has-consequences.md (curt, withheld, lie, warned) replaces the line first, and a trust line is never a key here, so it wins over the case. The names of specs/your-own-group.md are replaced after the case's texts.
10. **Files.** `campus_case.py` (`CASES`), `campus_evidence.py` (`retell`, `claims_of`, `story_card`, `shown_card`, the notes), `campus_game.py` (shown numbers), `docs/guiao-conversas.md` and `docs/historia.md` (the three cases).

## Reviewed tests that change
None. The classic case is the identity: same order, same code, `HEARING` and `CONFRONT` as they are, no text swapped; every reviewed test plays it (`open`). The module constants the reviewed tests pin (`PC12_CODE`, `PHOTO_TEXT`, `PHOTO_SOLUTION`, `CONFRONT`, `FACTS`, `EVIDENCE`, the stamp in `photo.js`) keep the values of specs/calendar-code.md; no case changes them.

## Limits
- The repository is public: whoever reads `campus_case.py` and knows the date knows the case. The page and the snapshots never say it.
- A swapped text is found by its exact classic text: if someone edits a classic line, its case text stops being used. A test fails when that happens.
- `present_evidence`, `open_drawer` and `view_files` played directly still work (specs/pen-and-code.md).

## Out of scope
More cases, a culprit chosen at random per player, Leonor as culprit, moving the USB stick, the plain game.

## Done when
- Existing tests pass unchanged, and `tests/continuous-conversations.cjs`; `play.js` and `photo.js` pass `--check`.
- The tests below were written first and pass.
- A browser check plays each case to `full_case` in one language and one case in the other: the shown order, the right code, the confession, the case's ending.

## Checks
`tests/test_culprit_of_the_night.py`, written before the code. `play_case(variant)` begins a game on a date that gives that case (patching `campus_game.case_day`).
- `test_the_classic_case_changes_nothing`: for the same commands, `open` and a `begin` on an `outsider` day give the same replies, apart from `day`.
- `test_each_case_shows_the_chat_in_its_own_order`: the shown texts are the case's, in its order; flagging the shown fakes and asking Leonor for help gives `full_case`.
- `test_the_page_sees_only_shown_numbers`: `chat.messages[*].action`, the flag rows and the `msg_` cards use shown numbers; `confront` with `msg_<shown of 5>` cracks Tomás; `flag_<n>` outside the chat is refused as before.
- `test_every_case_has_the_one_code_of_the_photo`: `1710` unlocks every case; `1411`, `1011`, `1311` and computer 7's `2311` are wrong in every case.
- `test_every_case_has_the_same_photo_and_date`: in every case and language the clerk's `order` line, the taped photo's text and the shutter slip are the classic ones; `photo.js` draws 17.10.2026 with no `stamp` option and `play.js` has no `photo_date`.
- `test_the_groups_memories_are_true_in_every_case`: no key of a case is, or is part of, a memory of `group_clues` or Tomás's `password` line; no case text (key, value or new professor line) has a word of that day (October, Saturday, Finance, sun, 15, 17, in both languages).
- `test_the_confession_breaks_the_name_claim`: `tomas_word` on claim 1 in `tomas`, `rita_word` in `rita`, a doubt in `outsider`.
- `test_the_true_ending_can_be_earned_in_every_case`.
- `test_every_key_is_a_classic_text`: each key of each case's `texts` is a whole text, or a whole sentence of the true ending, found in exactly one classic source; no key is part of another; no value contains another key; more than three words.
- `test_case_texts_keep_their_spoken_quotes`: with the rule of `partsOf`, same number of quotes as the key for endings, the true ending and the professor's lines; `en` and `pt` have the same keys and the same quote counts.
- `test_no_case_text_is_in_the_page_or_a_new_snapshot`: the built page has none; a fresh `begin` snapshot of each case has none of its reveals, endings or file history.
- `test_each_case_names_the_account_and_the_liar_can_be_checked`: the file history of `tomas` says Tomás, of `rita` Rita; Rita's `pen` (tomas) and Tomás's `who` (rita) are the second signs.
- `test_campus_case_is_still_data_only`: no `def` in `campus_case.py`; `CASES["outsider"]` has the classic order and accepts; no case has a `code` or a `photo_date`; `PC12_CODE` is `1710`.
