# Story — The Fifth Element (English texts)

English version of the player-facing texts of [historia.md](historia.md). The game offers a language choice at the start (Portuguese or English), so every text exists in both languages.

**Status: proposal, to be reviewed by the team.**

## Rules for keeping the two versions in sync

- Ids, conditions and effects are **only** in `historia.md`. They are identical in both languages. This file translates texts and nothing else.
- Sections here use the same numbers as `historia.md` (1 premise, 4 items, 6 scenes, 7 endings).
- If a text changes in one language, change it in the other in the same pull request.
- Working title: "The Fifth Element" (translation of "O quinto elemento"). It is also a well known film, so the team may prefer another title. The intruder is called just "Duarte", with no surname (decided 22/11/2026). Both are open decisions in `historia.md` section 11.

## 1. Premise (Start screen)

On the eve of the presentation, a fifth person appears in the photo of your group of four. Their name is in the report, and all your teammates received messages that seem to prove they were always part of the team. Only you know that something is wrong.

## 4. Items

| Id | Name |
|---|---|
| `usb_stick` | USB stick with the project history |
| `original_photo` | Printed original photo |

## 6. Scenes

Text the player reads is in italics in `historia.md`; here it is plain.

### 6.1 Study room — `study_room`

**Text:**
> It is night, the eve of the presentation. In the group folder, the photo shows five people. There are four of you. On the cover of the report there is a fifth name: Duarte. In the chat, your teammates insist that he "was with us all along". Only you know that is a lie.

**Extra text after you take the USB stick:**
> The group drawer is empty.

| Action | Label | Result text |
|---|---|---|
| `open_drawer` | Open the group drawer | You find the USB stick where the group kept the project backups. You take the USB stick. |
| `go_print_shop` | Go to the print shop | |
| `go_library` | Go to the library | |
| `go_computer_lab` | Go to the computer lab | |
| `go_auditorium` | Go to the auditorium | |

**Blocked text of `go_auditorium`:**
> You have no proof yet. The professor will not listen to you on a suspicion alone.

### 6.2 Print shop — `print_shop`

**Text:**
> The print shop is about to close. The clerk remembers your group: you printed the photo for the report cover here last week.

**Extra text after you take the photo:**
> The clerk has already given you a copy of the original order.

| Action | Label | Result text |
|---|---|---|
| `request_copy` | Ask for a copy of the original order | The clerk prints again the file that was saved with the order. The original photo shows four people. You take the photo. |
| `go_study_room` | Back to the study room | |

### 6.3 Library — `library`

**Text (before the decision):**
> Leonor, your teammate, is studying at a table at the back. She was one of the people who received Duarte's messages.

**Text after asking for help:**
> Leonor is saving screenshots of the messages. "I will take care of this. See you in the auditorium."

**Text after accusing her:**
> Leonor's table is empty.

| Action | Label | Result text |
|---|---|---|
| `ask_for_help` | Show the photo and quietly ask for help | Leonor compares the photo with the one in the report and turns pale. "I got all these messages last night, from a number I did not know. And some of them are dated three weeks ago." She promises to keep the original messages and to meet you in the auditorium. |
| `accuse` | Show the photo and accuse her of helping Duarte | "You think I would do that to the group?" Leonor stands up, offended. "Then you do not need these messages for anything." She deletes the conversation in front of you and leaves. |
| `go_study_room` | Back to the study room | |

**Blocked text of `ask_for_help` and `accuse` (without the photo):**
> Leonor shrugs. "Duarte has always been in the group, I have the messages right here. Do you have any proof otherwise?"

### 6.4 Computer lab — `computer_lab`

**Text:**
> The computer lab is empty. Computer 12 is still on: it is the one the group used to work on the project.

**Extra text after viewing the files:**
> You have compared the files: four authors in every copy on the USB stick, and a change in the shared folder yesterday at 11:47 pm.

| Action | Label | Result text |
|---|---|---|
| `view_files` | Look at the old project files | You plug the USB stick into computer 12 and compare. In the backups on the USB stick, every version has four authors. In the shared folder, the current version was changed yesterday at 11:47 pm, from this same computer: someone added "Duarte" to the report and swapped the photo. You recover the original version of the work. |
| `go_study_room` | Back to the study room | |

**Blocked text of `view_files` (without the USB stick):**
> The shared folder only shows the current version, already with five names. You need the group's backup copy.

### 6.5 Auditorium — `auditorium`

**Text:**
> The professor is in the auditorium, closing the list of groups for tomorrow. Duarte is sitting in the front row with a calm smile.

| Action | Label | Result text |
|---|---|---|
| `present_evidence` | Present the evidence to the professor | |
| `go_study_room` | Back to the study room | |

## 7. Endings

### Ending 1 — "The impostor" (`impostor`)

> You show the history on the USB stick: four authors until last night. Leonor walks in and hands over the messages she kept: they were all sent on the same night, from a new number, with fake dates. The professor crosses the fifth name off the list. Duarte leaves the auditorium without a word. Tomorrow, the four of you present.

### Ending 2 — "Stolen credit" (`stolen_credits`)

> You show the history on the USB stick: the original work is recovered and had four authors until last night. But Duarte raises his phone: "I have messages from everyone proving I took part." Without the original messages, you cannot prove they are fake. The professor sighs: "Without proof that the messages are fake, the name stays." Tomorrow, the five of you present.
