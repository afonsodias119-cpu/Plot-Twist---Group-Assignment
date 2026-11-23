# Your own group in the story: three friends' names for the three teammates

> **Update (specs/computer-lab-backup.md):** there is no chat and no flagged card any more; the names still reach every other text (dialogue, clues, hearing, endings).

Extends specs/case-of-the-day.md (the names travel with `begin` and live in the night's notes), specs/archive/culprit-of-the-night.md (the same `retell` swaps them in), specs/rules-and-character.md (the start screen) and specs/cleaner-interface.md (the case file's "Your group"). No change to `story.py`, `logic.py`, `game.py`, `app.py`, `db.py` or any reviewed test. Texts in design-notes/texts-ideas.md, part D.

> **Update (merge with specs/creator-after-name.md and specs/calendar-code.md):** the start screen is now in steps, so the "Your group (optional)" box sits in step 3, "Your detective", under the creator (point 1). At computer 12 the group's memories and the names over them are the page's own texts, so the page renames them with the same rule as the server (point 5); the people who follow the player carry their 3D name tags, which already show the group (point 6).

## Why
The story is about a group of four where one name is too many. It hits harder when the other three are your real friends: their names in the chat, in the confession, in "Tomorrow, the four of you present".

## What
1. **Three optional fields on the start screen**, in the "Your detective" step, under the character creator (specs/creator-after-name.md), inside a closed `<details>` titled "Your group (optional)" (`group_title`), so a first player still sees only the name field, its hint and the creator (specs/no-endings-on-start.md). One line explains the mapping (`group_hint`) and each field says whose place it takes (`group_slots`), with the story's name as its placeholder:
   - friend 1 takes **Leonor**'s place (the library; she);
   - friend 2 takes **Rita**'s place (the study room; she);
   - friend 3 takes **Tomás**'s place (the computer lab; he).
   Each field has `maxLength` 14. An empty field keeps the story's name. While the player types, the name chips of the group (`#groupList`, specs/chat-dialogues.md, now in the warning step of specs/creator-after-name.md) show the names typed. The last group typed is remembered in this browser (`plot-twist-group`, read with `try` and checked like `cleanLook`); the server never trusts it.
2. **They are sent with `begin`** as `names` (specs/case-of-the-day.md, point 2): a new game saves them, a continued game keeps its own group, a restart keeps the group.
3. **Cleaning, on the server** (`campus_people.clean_group(names)`; `DEFAULT_GROUP = ["Leonor", "Rita", "Tomás"]`, the order of the slots). Each name: strip, inner spaces made single; empty → the story's name; only letters (accented ones too), spaces, apostrophes and hyphens, 1 to 14 characters and at least one letter, otherwise the story's name; the first letter upper-cased ("ana" → "Ana"). Then the group as a whole: if two names are the same (ignoring case), or one is "Duarte", or one is the story's name of another slot ("Rita" in Leonor's place), all three go back to the story's names. A bad name never raises: the fields are optional.
4. **Where they live.** In the night's notes as `names` (a list of three), next to `case`. `read_night` keeps it only when `clean_group` gives it back unchanged; anything else counts as the story's names. The `games` row never holds them, so every save stays valid for `logic.is_valid_state` and for `app.py`. The snapshot gets `group`: the three names in slot order (the story's names in a classic game).
5. **Used everywhere a teammate is named.** `retell` (specs/archive/culprit-of-the-night.md, point 6) ends with one more step: in every string of the reply, one regular expression replaces the whole words `Leonor`, `Rita` and `Tomás` in a single pass (`\b(Leonor|Rita|Tomás)\b`, each match looked up in a small dict), so "Leonor → Rita, Rita → Ana" can never chain. It runs after the case's texts, on every reply, so it reaches the teammates' dialogue and their names on cards, the chat messages, the card labels, the clue list, the schedule sentences and warnings, the trust lines, the hearing, the verdicts and the endings, the true ending included, in both languages. Ids are lower case (`leonor`, `tomas_word`, `"player": "rita"`) and are never touched. `group` is added to the snapshot after `retell`. The few lines the page writes itself about the teammates, the memories of computer 12 and the names above them (`group_clues`, specs/calendar-code.md), are renamed in the page with the same rule (`inGroup` in play.js: one regular expression over the whole words, with tonight's `group`).
6. **In 3D**, the name tags over Leonor, Rita and Tomás show `group` (game3d.html updates the three signs on `campus-state`). The voices stay the slot's voices.
7. **The Portuguese rule** (and the English pronouns): a friend takes the slot's grammar. Friends 1 and 2 are "she" and "a Ana", "da Ana"; friend 3 is "he" and "o João", "do João". The texts are not rewritten for another gender. `group_slots` says so on the screen ("No lugar da Leonor (ela)").
8. **The page** shows `group_reset` as a note when the server used the story's names for a field that was not empty (`group` differs from what was typed), and `group_kept` when a continued game kept a different group. Nothing else changes.

## Reviewed tests that change
None. With no names (`open`, and every reviewed test) the group is the story's and the regular expression replaces each name by itself; `page3d.EXTRA[language]["group"]` keeps its four names (`tests/test_chat_dialogues.py:94`, `tests/test_earlier_nights.py:813`): only the page changes the chips' text while the player types.

## Limits
- A friend whose gender is not the slot's gets the slot's articles and pronouns ("a João"). Changing them would mean rewriting every line twice; the field labels say which slot is "she" and which is "he".
- A few texts the page keeps for itself still say the story's names: the Rules window's "How it was made" section, the docs and the 3D start screen's room cards. The game never relies on them.
- The diary keeps the lines as they were said: a group changed by a new game leaves the old names in old notes until the restart clears the diary.
- The names are kept with the night like the save itself: whoever types the same detective name sees them. Do not type anything private.

## Out of scope
More than three friends, renaming the player, Duarte, the professor or the clerk, another gender for a slot, the plain game.

## Done when
- Existing tests pass unchanged, and `tests/continuous-conversations.cjs`; `play.js` passes `--check`.
- The tests below were written first and pass.
- A browser check with "Ana, Bea, João" in both languages: the chips, the 3D tags, a conversation, a flagged message's card, the clue list, the hearing and an ending say the friends' names; "Rita" in Leonor's place falls back with the note.

## Checks
`tests/test_your_own_group.py`, written before the code. `begin(names)` begins a game with these names.
- `test_no_names_keeps_the_story`: `begin(["", "", ""])` and `open` give the same texts; `group` is the story's.
- `test_the_names_reach_dialogue_chat_cards_hearing_and_endings`: with `["Ana", "Bea", "João"]`, Rita's greeting has `Bea`, Leonor's name in `people` is `Ana`, the chat has `Ana` and `Bea` where the story has Leonor and Rita, a flagged card's label too, Duarte's third claim says `João`, the `stolen_credits` and `impostor` endings and a verdict line have no story name left; both languages.
- `test_names_never_chain`: `["Rita", "Ana", "João"]` is refused as a whole (another slot's name); `["Bea", "Ana", "João"]` gives Leonor → Bea and Rita → Ana with no `Ana` where Leonor was.
- `test_bad_names_fall_back_one_by_one`: `"<b>"`, `"x" * 15`, `"123"`, `"  "` become the slot's story name; `"ana  maria"` becomes `Ana maria`.
- `test_a_clash_or_duarte_brings_back_the_whole_story_group`: two equal names (ignoring case), `"duarte"`.
- `test_ids_are_never_renamed`: card ids, `npc`, `people[*].id`, `night.gone` and `player` are unchanged with a group.
- `test_the_save_never_holds_the_names`: the `games` row is the same as without names; `logic.is_valid_state` accepts it.
- `test_a_damaged_names_note_gives_the_story_names`: `names` as `"Ana"`, `[1, 2, 3]`, two names, `["Duarte", "Bea", "João"]`.
- `test_a_restart_keeps_the_group_and_a_continued_game_ignores_new_names`.
- `test_the_names_box_is_in_the_detective_step_under_the_creator`: the group box is appended to the detective step after the creator, not to the name box.
- `test_the_groups_memories_at_computer_12_say_the_friends_names`: play.js renames `group_clues` and the speakers with `inGroup`; with "Ana, Bea, João" no story name is left and Tomás's memory says Bea; with the story's names nothing changes.
- `test_the_start_screen_has_three_fields_and_the_page_renames_the_tags`: `play.js` has `plot-twist-group`, `group_slots` and `names:`; `game3d.html` reads `state.group`; the new texts exist in both languages and `group_slots` has three entries with "Leonor", "Rita" and "Tomás".
