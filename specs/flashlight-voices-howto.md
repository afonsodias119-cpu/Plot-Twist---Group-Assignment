# Flashlight, voices and "How it was made"

Extends specs/campus-people-and-atmosphere.md. Everything is on the screen: no change to the story, the rules, the saved game or the server.

## What
1. **Flashlight.** The detective carries a warm torch: a cone of light in the direction the character faces, and the rest of the night gets a little darker while it is on. It turns on when the game starts, off at an ending. A button (🔦) or the F key switches it; the choice is remembered in this browser.
2. **Voices.** The people speak their lines aloud with the browser's own speech (Web Speech API, free, no service): each person has their own pitch and speed (Portuguese or English, like the game). The narrator reads the ending. A button (🗣️) switches it off; the choice is remembered; speech stops when the conversation closes; the button is hidden if the browser cannot speak. Computer 12 stays silent.
3. **"How it was made".** A button (ℹ️) opens a window that says where each part of the game lives in the repository (rules, story, saving, 3D, the bridge, conversations, screen, tests, specs, security) and how to run it. Every file named there exists (a test checks it), in English and Portuguese.

## Out of scope
Recorded voices, sound files, changing how the 3D is lit indoors, anything on the server.

## Done when
- Existing tests pass unchanged.
- New tests: the "How it was made" items are the same in both languages and name files that exist; the page has the three buttons and their code.
- A browser check shows the window, the voice calls with a different pitch per person, and the torch switching on and off.
