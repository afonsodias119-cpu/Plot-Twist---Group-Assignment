# Specs

One spec per feature, written **before** its tests and code. Each one has the same parts:
1. **Before writing the spec:** who uses it, when it happens, how it was before, the rule, and how it is after.
2. **What:** the files that change.
3. **Reviewed tests that change:** tests already approved by the team that this feature changes, and who approves them.
4. **Done when:** the tests and the browser check that prove it is done.

A spec is not rewritten after its feature is merged: a later change gets its own spec, and the older one gets an
**Update** note at the top. So the folder is also the history of our decisions.

## Start here: the game of today in eight specs

| # | Spec | What it explains |
|---|---|---|
| 1 | [base-game](base-game.md) | The rules every version shares: scenes, items, saving, restarting (the course brief's requirements) |
| 2 | [campus-3d-streamlit](campus-3d-streamlit.md) | How the 3D game runs inside Streamlit (the published app) |
| 3 | [name-belongs-to-browser](name-belongs-to-browser.md) | Access control: a name belongs to the browser that started it |
| 4 | [night-schedule](night-schedule.md) and [night-and-clues](night-and-clues.md) | The clock of the night, who leaves, Duarte's rounds, what costs time |
| 5 | [three-proofs](three-proofs.md) | Why the proofs decide the ending (and what was removed) |
| 6 | [camera-proof](camera-proof.md) | The fourth proof: the security recording |
| 7 | [select-the-proofs](select-the-proofs.md) and [missing-proof-is-a-warning](missing-proof-is-a-warning.md) | Handing the proofs to the professor, and what happens when one is missing |
| 8 | [safe-dependencies](safe-dependencies.md) | Pinned dependencies with no known vulnerabilities |

Every other spec below adds one feature to these. "Later" lists the specs that changed it.

## The base game and the project

| Spec | What | Later |
|---|---|---|
| [base-game](base-game.md) | The plain game (`app.py`): scenes, items, endings, saving | computer-lab-backup, three-proofs |
| [scene-images](scene-images.md) | Pictures and the mystery theme of the plain game | |
| [tests-on-github](tests-on-github.md) | The tests run on GitHub on every push | |
| [safe-dependencies](safe-dependencies.md) | Pinned dependencies with no known vulnerabilities | |
| [name-belongs-to-browser](name-belongs-to-browser.md) | A saved name belongs to the browser that started it | |
| [name-check-first-step](name-check-first-step.md) | The name is checked where it is typed | |
| [warm-start](warm-start.md) | The first click never times out | |
| [fresh-code-after-deploy](fresh-code-after-deploy.md) | Fresh code after a deploy | |

## The 3D campus

| Spec | What | Later |
|---|---|---|
| [playable-campus-3d](playable-campus-3d.md) | The playable 3D campus | campus-3d-streamlit |
| [campus-3d-streamlit](campus-3d-streamlit.md) | The 3D game inside Streamlit (the published app) | |
| [campus-people-and-atmosphere](campus-people-and-atmosphere.md) | People, dialogues, clock, diary, sounds and light | computer-lab-backup |
| [chat-dialogues](chat-dialogues.md) | Chat-style conversations and room plaques | |
| [cleaner-interface](cleaner-interface.md) | A cleaner interface | |
| [rules-and-character](rules-and-character.md) | Rules in the menu and the character creator | |
| [creator-after-name](creator-after-name.md) | The detective after the name, the closing-time warning | |
| [combined-start-briefing](combined-start-briefing.md) | One start card with the briefing and the clues | |
| [flashlight-voices-howto](flashlight-voices-howto.md) | Flashlight, voices and "How it was made" | |
| [sounds-that-tell](sounds-that-tell.md) | Sounds that tell you things | |
| [study-room-detail](study-room-detail.md) | A lived-in study room | |
| [library-study-hall](library-study-hall.md) | The library as a study hall | |
| [more-to-find](more-to-find.md) | Things to look at, and two red herrings | computer-lab-backup |
| [professor-before-podium](professor-before-podium.md) | K talks to the professor, not to the podium | duarte-only-in-the-hearing |
| [auditorium-door-keeps-room](auditorium-door-keeps-room.md) | A refused door does not move the character | (the auditorium is always open now: three-proofs) |
| [touch-card-qr](touch-card-qr.md) | Phone controls, the detective card and a QR code | |
| [case-of-the-day](case-of-the-day.md) | The case of the day | night-and-clues (no date on screen) |
| [your-own-group](your-own-group.md) | Your friends' names for the three teammates | computer-lab-backup |

## The clues and the puzzles

| Spec | What | Later |
|---|---|---|
| [hidden-object-table](hidden-object-table.md) | The USB stick hidden on the table | table-hint-and-guard-check |
| [pen-and-code](pen-and-code.md) | The USB stick and the code of computer 12 | calendar-code |
| [calendar-code](calendar-code.md) | The group remembers the day; the phone's Weather and Calendar | |
| [torn-photo](torn-photo.md) | The torn photo puzzle in the print shop | calendar-code |
| [computer-lab-backup](computer-lab-backup.md) | Computer 12 saves the backup of the conversations | three-proofs |
| [security-desk](security-desk.md) | José, the cables and last night's recordings | camera-proof |
| [guard-explain-first](guard-explain-first.md) | José first hears why you came | |
| [guard-answer-and-cameras](guard-answer-and-cameras.md) | José's question, and a camera in every room | |
| [table-hint-and-guard-check](table-hint-and-guard-check.md) | The table note (point 2 replaced by guard-answer-and-cameras) | |
| [night-and-clues](night-and-clues.md) | The night 22:30–23:00, free clues, the start card | three-proofs, clue-order |
| [camera-clue](camera-clue.md) | The cameras in the list of clues | clue-order |
| [clues-without-answers](clues-without-answers.md) | The clues say what to find, not where | clue-order |
| [clue-order](clue-order.md) | The five clues in the team's order | |

## The conversations

| Spec | What | Later |
|---|---|---|
| [continuous-conversations](continuous-conversations.md) | Conversations that continue | |
| [actions-when-they-make-sense](actions-when-they-make-sense.md) | Actions appear when they make sense | calendar-code |
| [two-answers](two-answers.md) | One right and one wrong answer for Tomás and Rita | evidence-after-monitors |
| [leonor-two-answers](leonor-two-answers.md) | The same for Leonor | |
| [leonor-after-help](leonor-after-help.md) | Leonor after she agrees to help | |
| [tomas-password-end](tomas-password-end.md) | The end of Tomás's password explanation | |
| [evidence-after-monitors](evidence-after-monitors.md) | "Show evidence" with José only when he asks; none with Rita | |
| [trust-has-consequences](trust-has-consequences.md) | People you were rude to answer less, warn or lie | computer-lab-backup |
| [duarte-only-in-the-hearing](duarte-only-in-the-hearing.md) | Duarte only speaks in the hearing | |

## The professor, the proofs and the endings

Read in this order: evidence-and-hearing → three-proofs → camera-proof → select-the-proofs → missing-proof-is-a-warning.

| Spec | What | Later |
|---|---|---|
| [evidence-and-hearing](evidence-and-hearing.md) | Evidence cards and the hearing | three-proofs, camera-proof, select-the-proofs |
| [three-proofs](three-proofs.md) | The proofs decide the ending; no accusing Leonor, no true ending | camera-proof |
| [camera-proof](camera-proof.md) | The security recording is the fourth proof | |
| [professor-line-of-thought](professor-line-of-thought.md) | The professor's conversation in one line | select-the-proofs |
| [hearing-show-evidence](hearing-show-evidence.md) | "Show evidence" in the hearing | select-the-proofs |
| [hand-over-the-proofs](hand-over-the-proofs.md) | Handing every proof at once | select-the-proofs, missing-proof-is-a-warning |
| [select-the-proofs](select-the-proofs.md) | **Today:** "Show evidence" or ask; tick the proofs to hand over | |
| [missing-proof-is-a-warning](missing-proof-is-a-warning.md) | **Today:** a missing proof is a warning, the night goes on | |
| [no-endings-on-start](no-endings-on-start.md) | No count of endings on the start screen | no-endings-count |
| [no-endings-count](no-endings-count.md) | No count of endings anywhere | |

## Time and earlier nights

| Spec | What | Later |
|---|---|---|
| [harder-campus](harder-campus.md) | 30 minutes before the faculty closes | night-schedule |
| [night-schedule](night-schedule.md) | The server's clock, who leaves, Duarte's rounds | night-and-clues, three-proofs |
| [earlier-nights](earlier-nights.md) | The game remembers earlier nights | three-proofs (no true ending) |

## Archive

The specs of features that are no longer in the game are in [archive/](archive/README.md): the group chat puzzle, the
secret ending "The fifth element" and a different culprit some nights. They are kept only as a record of decisions.
