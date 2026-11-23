# Story — The Fifth Element

The English translation of [historia.md](historia.md): the map of the story **as it is in the game today**, who is who,
where each proof is and how the night ends. The two files say the same thing; if one changes, the other changes too.
The exact texts are in the code: `story.py` (scenes and endings, in both games), `prototypes/campus-3d/campus_people.py`
(the conversations) and `prototypes/campus-3d/campus_case.py` (the proofs and the hearing). Every line of dialogue, in
Portuguese and English, is in [guiao-conversas.md](guiao-conversas.md). Every change has its spec in `specs/` (see
[specs/README.md](../specs/README.md)).

Names in code font (for example `study_room`) are the identifiers used in the code.

## 1. Summary

The night before the presentation, a fifth person appears in the photo of your group of four. His name, Duarte, is on
the cover of the report, and the group has received messages that seem to prove he always took part. You have the night
(from 22:30 to 23:00, in the 3D game) to gather the proofs and show them to the professor in the auditorium, before he
closes the list of groups.

## 2. Characters

| Character | Where | Role |
|---|---|---|
| **You** | — | The player, a member of the group of four. |
| **Rita** | Study room | Teammate. Helps you find the USB stick and remembers that the day of the photo was a Saturday. |
| **The clerk** | Print shop | Keeps the original order of the photo; with you, she puts the torn photo back together. |
| **Leonor** | Library | Teammate. If you show her the photo, she helps you; she remembers the Finance test. She leaves at 22:45 if she has not agreed to help yet. |
| **Tomás** | Computer lab | Teammate. Explains the rule of computer 12's code. |
| **José, the guard** | Entrance | Has the camera recordings. He only shows them after you explain the situation and show him a proof. |
| **Duarte** | Auditorium | The intruder. You do not talk to him: he only speaks in the hearing, when you hand over the proofs. He walks rounds to the computer lab. |
| **The professor** | Auditorium | Closes the list of groups. You hand the proofs to him. |

The names of Rita, Leonor and Tomás can be replaced by your friends' names at the start (specs/your-own-group.md).

## 3. Map

Every room opens onto the corridor; the auditorium is always open.

```
              Print shop    Study room     Library
Entrance ──────────────────── corridor ─────────────────────
(guard)             Computer lab           Auditorium
```

## 4. The four proofs for the professor

| Proof | How you get it | It breaks Duarte's claim |
|---|---|---|
| **The file history** | You find the USB stick on the study room table; at computer 12 you type the code (the day of the photo, which the group helps you work out) and open the files. | "My name has been on the cover since the first draft." |
| **The original photo** | In the print shop, you put the torn photo back together with the clerk. | "Five people in the photo, and I am the one on the right." |
| **The backup of the conversations** | At computer 12, after opening the files, you save the backup of the original conversations. | "I have weeks of messages in the group." |
| **The security recording** | With José: you explain the situation, show him the photo or the files, plug in the cables and keep the picture of the computer lab at 23:47. | "I was not even here last night." |

The USB stick alone is not a proof: the proof is the history inside it, once you open it.

## 5. The professor and the end of the night

On his first line, the professor offers two things:
- **"📁 Show evidence":** you pick the proofs you have and hand them to him.
  - If one is missing, he only says how many are missing ("One of the proofs is missing. Come back when you have it.") and the night goes on.
  - With all four, Duarte makes his claims, each one falls to its proof, and the case is closed.
- **"Ask how many members your group has":** "Five" → "There are only four of us" → "I will bring proof", and the conversation ends.

## 6. Endings

| Ending | When |
|---|---|
| **Case closed** (`full_case`) | You hand the four proofs to the professor. The fifth name is crossed out. |
| **The faculty is closed** | 23:00 comes before you have handed over every proof: the fifth name stays on the cover. |
| **Stolen credit** (`stolen_credits`) | In the plain game (`app.py`), when you present the evidence with a proof missing. |

There are no other endings: accusing Leonor, "The impostor" and the secret ending were removed (specs/three-proofs.md).

## 7. What costs time

Finding a clue costs nothing. Wrong choices cost minutes: a wrong proof (2), a wrong place on the table (1), a wrong
code (2), a rude answer (5), and being caught by Duarte at computer 12 before you save the backup (3).
The plain game (`app.py`) has no clock.

## 8. Pictures

Illustrations in `assets/`, used by the plain game (`app.py`).

| Picture | File |
|---|---|
| Cover (the group photo with five people) | `assets/cover.jpg` |
| Study room, print shop, library, computer lab, auditorium | `assets/study_room.jpg`, `print_shop.jpg`, `library.jpg`, `computer_lab.jpg`, `auditorium.jpg` |
| USB stick and original photo | `assets/usb_stick.jpg`, `assets/original_photo.jpg` |
| Ending "Stolen credit" | `assets/ending_stolen_credits.jpg` |

`assets/ending_impostor.jpg` belongs to the removed ending and is no longer used.
