# Spot the fake — the group chat puzzle

> **Replaced by specs/computer-lab-backup.md:** the group chat and its flags no longer exist; the player saves a backup of the original conversations instead.

**Blocked by:** the base game merged into `main` (done), and the team approving this spec, because it changes one reviewed test (see "Reviewed tests that change").

Phase D extra 2 of 2. It adds one scene, five new remembered facts and a third ending, using only the rules that already exist: no change to `logic.py`.

## Before writing the spec

- **Product and user:** a player who has seen the old files on computer 12 and now wants to prove which messages are fake.
- **Trigger:** the player clicks "Open the group chat" in the computer lab, then clicks "Flag message N".
- **Before:** the game remembers `files_viewed` and `colleague_choice`.
- **Rule:** the chat is offered only after `files_viewed` is true. Each message can be flagged once, and a flag cannot be undone.
- **After:** the game remembers which messages were flagged. At the auditorium, the best ending needs the right messages flagged, no real message flagged, and Leonor's help.

## Why

As a player, I want to reason from clues and not only collect items, so that a careful reading is rewarded. As a team, this is the most original part of the game, and it fits the story: the fake messages are the heart of the mystery.

## What

### 1. Where the data goes

Everything is data in `story.py`, in both languages, with the same ids and conditions in each (the existing structure test checks this):

- `computer_lab` gets one more action, `open_chat`: label "Open the group chat on computer 12", `offered_if` `{"flags": {"files_viewed": True}}`, `go_to` `group_chat`.
- A new scene `group_chat`: five messages as scene texts, five `flag_<n>` actions and `go_computer_lab` (back).
- Five new flags in `start`, all `False`: `flagged_1` to `flagged_5`.
- A third ending, `full_case`, first in the list.

`logic.py` does not change: it already compares flags, and an ending is the first one whose `when` is true.

### 2. The five messages (English; the Portuguese version translates the texts and keeps every clue)

Messages 2, 4 and 5 are fake. Messages 1 and 3 are real. A message that arrived late shows when it arrived.

| # | Text | Why it is real or fake |
|---|---|---|
| 1 | Leonor, 3 weeks ago, 21:05: "Can someone book the study room for Thursday?" | Real. Old, but it arrived the same day. |
| 2 | Unknown number, 3 weeks ago, 21:07: "Booked it. I wrote the conclusion too, like always." | Fake. The sender is not in the group. |
| 3 | Rita, 2 weeks ago, 18:40: "Photo for the cover is ready. Four of us, finally!" | Real. Says "four of us". |
| 4 | Duarte, 3 weeks ago, 22:10: "Can't wait for the five of us to present." | Fake. The group had four members. |
| 5 | Tomás, 3 weeks ago, 22:12 (arrived yesterday, 23:49): "Duarte did the slides, obviously." | Fake. It arrived yesterday, minutes after the shared folder was changed. |

The scene text starts with one sentence of instruction: a message that arrived late shows its arrival time. Rita and Tomás are the two other teammates; the team may rename them.

### 3. Flags, actions and texts of `group_chat`

- Each `flag_<n>` has `offered_if` `{"flags": {"flagged_<n>": False}}`, `sets` `{"flagged_<n>": True}` and the same neutral `result_text` for every message ("You flag message <n> for the professor."), so the answer is not given away.
- Scene texts alternate: message 1, then a line "Flagged." shown only when `flagged_1` is true, then message 2, and so on.

### 4. The new ending

`full_case` ("Case closed") has `when`: `colleague_choice` is `help`, `flagged_2`, `flagged_4` and `flagged_5` are `True`, and `flagged_1` and `flagged_3` are `False`. It is placed before `impostor`, so it wins when its condition is true. `impostor` and `stolen_credits` keep their conditions.

### 5. Saved games and screens

- `is_valid_state` already requires exactly the flags of `start`, so a game saved before this feature is treated as no save and the player starts again. This is accepted and written in "Limits".
- The screens need no change: they draw whatever scenes, actions and endings the story has.

## Reviewed tests that change

One assertion of the reviewed file changes, because the requirement changes: in `test_every_ending_is_reachable_from_a_new_game`, the endings found become exactly `impostor`, `stolen_credits` and `full_case`. The reviewer of this spec (the author of that test) approves the change. No test is skipped or deleted, and all the others pass as they are.

## Checklist (one line, one test) — `tests/test_base_game.py`

New paths: `P_FULL` is the first 9 actions of `P_HELP`, then `open_chat`, `flag_2`, `flag_4`, `flag_5`, `go_computer_lab`, `go_study_room`, `go_auditorium`, `present_evidence`.

- [ ] `test_chat_is_offered_only_after_the_files_are_viewed` — in a new game, in the computer lab, `open_chat` is not offered; after `view_files` it is, and it leads to `group_chat`.
- [ ] `test_a_message_is_flagged_once_and_remembered` — after `flag_2`, `flagged_2` is `True`, `flag_2` is not offered and asking for it gives `not_offered`; the scene shows the "Flagged." line right after message 2.
- [ ] `test_a_perfect_report_with_help_reaches_full_case` — `P_FULL` ends in `full_case`.
- [ ] `test_flagging_a_real_message_loses_the_full_case` — `P_FULL` with `flag_1` added ends in `impostor`.
- [ ] `test_missing_a_fake_message_loses_the_full_case` — `P_FULL` without `flag_5` ends in `impostor`.
- [ ] `test_a_perfect_report_without_help_does_not_reach_full_case` — the same flags with `accuse` instead of `ask_for_help` end in `stolen_credits`.
- [ ] `test_the_chat_works_in_both_languages` — `P_FULL` ends in `full_case` with each story in `STORIES`.
- [ ] `test_a_save_without_the_new_flags_starts_again` — `is_valid_state` is `False` for a state whose `flags` has only `colleague_choice` and `files_viewed`.

The existing checks keep passing: the structure test between languages, the content baseline, `is_valid_state`, and that playing never changes the story.

## Out of scope

- Undoing a flag, a score, hints, and more than five messages.
- New items, new engine rules, or changes to the screens.
- An image for the chat or for the third ending (a later `scene-images` update may add `assets/ending_full_case.jpg` and `assets/group_chat.jpg`).

## Done when

- `uv run pytest` is green, with the tests written from the checklist and reviewed before the code.
- By clicking, in both languages: reach `full_case` with the right three flags; reach `impostor` with a wrong flag; the chat button does not appear before viewing the files.
- A player can solve it from the texts alone, without being told which messages are fake. One person outside the team tries it once.
- `pyproject.toml`, `uv.lock` and `logic.py` are unchanged.
- The work is on its own branch, pushed, and reviewed by another member.

## Limits and how it could change

| Limit | How it could change |
|---|---|
| Flags cannot be undone, so one wrong click loses the third ending (the other two stay possible). | Add `unflag_<n>` actions that set the flag back to `False`. Only `story.py` changes. |
| Saves made before this feature start again. | Fill missing flags with their start value in `game.load`. |
| Five fixed messages, always the same. | A new message is one more text, one action and one flag. |
| The player is not told how many messages are fake. | Say it in the scene text. |
