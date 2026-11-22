# Rules in the menu, a simpler menu, and a character creator

Extends specs/cleaner-interface.md and specs/flashlight-voices-howto.md. Only the 3D game's screen changes. No change to `story.py`, `logic.py`, `db.py`, `game.py`, `app.py` or the server: the look of the detective is never sent to it.

## Why
The menu had four long items (one of them, "How it was made", is for the teachers, not for the player), and two of them, Voices and Sound, looked like the same thing. Every player is the same detective, so a team of four cannot see who is who.

## What
1. **Rules.** The menu item "How it was made" becomes **Rules** (`Regras`). Its window tells the player how to play in 9 short points (the goal and the 30 minutes, the time, walking and the K key, conversations and showing evidence, the clues and the phone, the group chat and Duarte's rounds, the torch and the sound, the end of the night, saving). It does not give away any puzzle (no code, no hiding place). "How it was made" stays inside the same window, as a closed section "For the teachers", so the walkthrough help is not lost.
2. **Three items, one word each.** The menu is **Rules, Torch, Sound**. Torch and Sound show a dot that is lit when they are on (`aria-pressed`); the long texts ("Torch off (F)", "Sound on") are gone. The F key is explained in the Rules.
3. **One sound button.** The separate Voices item is removed: the Sound button turns the music, the effects **and** the voices on and off. (The key `plot-twist-voice` is not used any more.)
4. **Character creator** on the first screen, under the name: **boy or girl**, **clothes** (T-shirt, jacket, hoodie, suit, trench coat, and a dress for the girl), the **colour** of the clothes (8), the **hair** colour (5), the **skin** (4), **hat or not**, and "Surprise me". A small 3D preview of the detective turns slowly beside the choices. When the game starts the detective in the campus wears the chosen look. The girl has long hair, the boy short hair.
5. **Where the look is kept.** In this browser only (`localStorage`: the last look, and one per name, `plot-twist-look:<name>`), like the diary. Typing a name that has a look shows it again. Everything read from the browser is checked (`cleanLook`): a damaged note gives the default look (the trench-coat detective). Another browser or device starts with the default look.
6. **The torch near the sign.** Near the glowing NOVA sign (where a new game starts) the torch is weaker, so it does not burn the letters out.

## Reviewed tests that change
The requirement "the menu has four tools, including the voices" changes, so two assertions of the reviewed file `tests/test_cleaner_interface.py` change; their author must approve it in the pull request. No test is skipped or deleted.
- `test_the_top_bar_has_no_emojis`: the buttons with a label are now 5 (the voices item is gone), not 6.
- `test_the_four_tools_are_inside_the_menu` becomes `test_the_three_tools_are_inside_the_menu`: Rules, Torch and Sound are in the menu.
(`tests/test_flashlight_voices_howto.py`, written for the flashlight feature, no longer looks for the voices button either.)

## Out of scope
Saving the look on the server (so other players see it), other people's looks, more clothes, changing the NPCs, the plain game.

## Done when
- Existing tests pass, apart from the two assertions above.
- New tests (`tests/test_rules_and_character.py`): the menu texts are one word and there is no voices item; the voices follow the Sound button; the rules exist in both languages, say how to play and give no puzzle away; "How it was made" is still there; the creator texts and palettes match; what is read from the browser is checked; the look never goes to the server.
- A browser check shows the creator, the preview, all six outfits, the detective in the game with the chosen look, the menu and the Rules window.
