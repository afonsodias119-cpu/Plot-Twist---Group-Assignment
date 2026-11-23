# Combine the starting briefing and clues

Show the closing-time warning and the ordered phone clues on the same screen before a first game. Remove the mission and group summary from that screen. Starting or continuing from the introduction opens the game directly. The phone still tracks clues, and an in-game restart can still show its clue reminder.

The phone's Clues app shows a localized hint about kindness below the checklist.

## Reviewed tests that change
Added afterwards by Afonso. The pull request was merged with these six tests failing, and this fixes them. Each changed line has a comment saying what it was before.
- `tests/test_chat_dialogues.py` (Mariana): the case file no longer has the group box.
- `tests/test_cleaner_interface.py` (Mariana): there is no group label any more.
- `tests/test_creator_after_name.py` (Mariana): the warning shows the clues in order instead of the mission.
- `tests/test_code_refresh.py` (Guilherme): the stale text it removes is now `stamp`, because `group` no longer exists.
- `tests/test_earlier_nights.py` (Guilherme): no group on the case file.
- `tests/test_night_and_clues.py` (Afonso): the clue card opens only after "New game", because the start shows the clues on the warning screen.
