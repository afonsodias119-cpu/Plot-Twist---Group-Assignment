# Flashlight, voices and "How it was made"

Extends specs/campus-people-and-atmosphere.md. Everything is on the screen: no change to the story, the rules, the saved game or the server.

## What
1. **Flashlight.** The detective carries a warm torch: a cone of light in the direction the character faces, and the rest of the night gets a little darker while it is on. It turns on when the game starts, off at an ending. A button (🔦) or the F key switches it; the choice is remembered in this browser.
2. **Voices.** The people speak aloud with the browser's own speech (Web Speech API, free, no service), in Portuguese (pt-PT) or English (en-GB), like the game. **Only what they say is read** (the text between quotation marks), never the description of what they do; each sentence is spoken on its own for natural pauses. The most natural voice of the browser is chosen (the "Natural"/"Online" ones, then neural, then Google), by gender (Rita, Amélia and Leonor female; Tomás, the professor and Duarte male), and each person has a slightly different pitch and speed. In the endings that have dialogue the lines are read by whoever says them (`ending_voices`); the endings without dialogue are silent. A button (🗣️) switches it off; the choice is remembered; speech stops when the conversation closes; the button is hidden if the browser cannot speak. Computer 12 stays silent.
3. **"How it was made".** A button (ℹ️) opens a window that says where each part of the game lives in the repository (rules, story, saving, 3D, the bridge, conversations, screen, tests, specs, security) and how to run it. Every file named there exists (a test checks it), in English and Portuguese.

## Out of scope
Recorded voices, sound files, changing how the 3D is lit indoors, anything on the server.

## Done when
- Existing tests pass unchanged.
- New tests: the "How it was made" items are the same in both languages and name files that exist; the page has the three buttons and their code.
- A browser check shows the window, the voice calls with a different pitch per person, and the torch switching on and off.
