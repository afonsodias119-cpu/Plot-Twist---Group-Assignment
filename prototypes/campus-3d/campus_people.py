"""The people of the 3D campus and their conversations (specs/campus-people-and-atmosphere.md).

A conversation is a small tree. Each node has what the person says, optional `trust` (0-3, not shown;
at 0 the person ends the talk), an optional `note` (a line for the player's diary) and the answers the player can choose:
{"label", "next"} where next is another node id or None (the conversation ends).
There is no "Ask something else" answer (specs/chat-dialogues.md): the screen keeps the conversation
open and offers, after each answer, the topics of the opening menu not asked yet
(specs/continuous-conversations.md).
An answer can have "if": a story condition ({"has": [...], "flags": {...}}); it is offered only when true.
An answer can have "cost": minutes taken off the countdown when the player chooses it (the rude answers,
specs/harder-campus.md). The countdown lives in the browser; the server only passes the cost on.
An answer can have "night": a campus-only key, the first night of this name on which it is offered
(a memory answer, specs/earlier-nights.md, point 5). It is never mixed with the story's "if".
The same ids, conditions and nights exist in "en" and "pt"; only the texts differ.

Talking never changes the saved game. The server only reads it (to check the person is in the saved
room and which answers are offered). A rude answer (the operation `rude`) is remembered in the
night's notes, not in the saved game, and changes how Leonor, Tomás and Duarte answer for the rest
of the night: see `temper` (specs/trust-has-consequences.md).
"""

import re
import unicodedata

import logic

# Where each person stands (the id of the story scene) and when they are not there any more.
ROOM_OF_PERSON = {
    "rita": "study_room", "amelia": "print_shop", "leonor": "library",
    "tomas": "computer_lab", "computer12": "computer_lab", "professor": "auditorium", "duarte": "auditorium",
}
# Things that are used, not talked to (the panel says "Use", the screen says "press K to use").
OBJECTS = {"computer12"}
# A scene of the story with no room of its own would be listed here (the group chat was, until
# specs/computer-lab-backup.md removed it). Every scene now has its own room.
ROOM_OF_SCENE = {}


# The story actions that are done by talking to a person: they appear as choices inside that conversation.
ACTION_PERSON = {
    "open_drawer": "rita", "request_copy": "amelia", "ask_for_help": "leonor", "accuse": "leonor",
    "view_files": "computer12", "save_backup": "computer12", "present_evidence": "professor",
}


# Who walks with the player once their clue is solved, and waits at computer 12 to help with the date
# (specs/calendar-code.md): Rita once the USB stick is found, Leonor once she agreed to help.
FOLLOWERS = ("rita", "leonor")


def followers(state):
    """The people who follow the player, from the saved game only (nothing new is saved)."""
    found = []
    if "usb_stick" in state["inventory"]:
        found.append("rita")
    if state["flags"]["colleague_choice"] == "help":
        found.append("leonor")
    return found


def room_of_scene(scene):
    """The 3D room where a story scene takes place."""
    return ROOM_OF_SCENE.get(scene, scene)


def _bye(label):
    return {"label": label, "next": None}


PEOPLE = {
    "en": {
        "rita": {"name": "Rita", "nodes": {
            # Two answers on every line, a right one and a wrong one (specs/two-answers.md): the USB stick,
            # the photo, her claim line, Duarte, then the chat. Every wrong answer upsets her; an apology
            # brings the first question back. Rita has no trust level and no rude answer that costs time.
            "start": {"text": "Rita looks up from her laptop. \"You don't look so good. Did you sleep at all?\"", "options": [
                {"label": "Ask where the USB stick is", "next": "pen"},
                {"label": "Tell her she is the one who lost the USB stick", "next": "upset"},
                # A memory answer (specs/earlier-nights.md, point 5): a shortcut to her claim line.,
                {"label": "Tell her you remember her counting heads", "next": "five", "night": 3},
                _bye("Goodbye."),
            ]},
            "pen": {"text": "\"The USB stick? It should be here somewhere, but I can't find it.\" She looks at the table. \"We stayed here late last night eating pizza, but with this mess, it could be anywhere.\"", "note": "Rita cannot find the USB stick. The group ate pizza here last night.", "options": [
                {"label": "Ask about the group photo", "next": "photo"},
                {"label": "Tell her to look for it herself, it is her mess", "next": "upset"},
            ]},
            "photo": {"text": "\"The photo? We took it after the last meeting, the four of us.\"", "note": "Rita remembers four people in the group photo.", "options": [
                {"label": "Ask why the photo in the folder shows five", "next": "five"},
                {"label": "Tell her that her memory does not count", "next": "upset"},
            ]},
            # Rita's claim line (specs/evidence-and-hearing.md, point 7): the right answer reminds her of a
            # proof and makes her give in (the photo when it is held, otherwise the files); with no proof yet,
            # the right answer moves on to Duarte. The wrong one agrees with her.
            "five": {"text": "\"Then I counted wrong.\" Rita turns the laptop towards you: five people. \"A photo cannot change. My memory can. He must have been standing right there.\"", "options": [
                {"label": "Remind her of the print shop's original photo: four people", "next": "five", "if": {"has": ["original_photo"]}, "crack": "original_photo"},
                {"label": "Remind her the file history has four authors in every copy", "next": "five", "if": {"lacks": ["original_photo"], "flags": {"files_viewed": True}}, "crack": "files"},
                {"label": "Ask what she remembers about Duarte", "next": "duarte", "if": {"lacks": ["original_photo"], "flags": {"files_viewed": False}}},
                {"label": "Agree that she must have counted wrong", "next": "counted"},
            ]},
            "counted": {"text": "Rita nods slowly. \"Yes. A photo does not lie.\" She turns the laptop back.", "options": [
                {"label": "Ask what she remembers about Duarte", "next": "duarte"},
                {"label": "Tell her that then Duarte stays in the group", "next": "upset"},
            ]},
            "duarte": {"text": "\"Duarte... honestly, I cannot picture him. Every time I try, I only see the name on the cover.\"", "options": [
                {"label": "Say you think the name was added last night", "next": "warned"},
                {"label": "Say that then he must really be part of the group", "next": "upset"},
            ]},
            "warned": {"text": "Rita goes quiet. \"If that is true, somebody wanted us to doubt ourselves.\"", "note": "Rita doubts the fifth name too.", "options": [
                {"label": "Ask about the chat messages", "next": "chat", "if": {"flags": {"files_viewed": True}}},
                {"label": "Tell her you will go and find proof", "next": "promise", "if": {"flags": {"files_viewed": False}}},
                {"label": "Tell her it is all in her head", "next": "upset"},
            ]},
            "promise": {"text": "\"Go. I will stay here.\" Rita opens her laptop again.", "options": [
                _bye("Goodbye."),
            ]},
            "chat": {"text": "\"Look at when the messages arrive. Some say three weeks ago, but my phone shows them as new, last night. That is not how old messages work.\"", "note": "Rita: an old message does not arrive as new. The messages about Duarte arrived last night.", "options": [
                _bye("Goodbye."),
            ]},
            "upset": {"text": "Rita closes her laptop slowly. \"You do not have to talk to me like that. We are all tired.\"", "options": [
                {"label": "Apologise", "next": "sorry"},
                {"label": "Say you are only being honest", "next": "closed"},
            ]},
            "sorry": {"text": "\"Fine. Go on, ask.\"", "options": [
                {"label": "Ask where the USB stick is", "next": "pen"},
                {"label": "Tell her she is the one who lost the USB stick", "next": "upset"},
            ]},
            "closed": {"text": "Rita puts her headphones on. She is not listening any more.", "options": [
                _bye("Leave."),
            ]},
        }},
        "amelia": {"name": "Clerk", "nodes": {
            "start": {"text": "The clerk adjusts her glasses. \"Hello! We close in ten minutes. What do you need?\"", "options": [
                {"label": "Ask about the cover photo order", "next": "order"},
                {"label": "Say the date before she does", "next": "again", "night": 2},
                _bye("Goodbye."),
            ]},
            "order": {"text": "\"The cover photo? You took it and had it printed here the same day. I remember there were four people in it, and I think the original order file is still saved.\"",
                      "note": "The cover photo was printed at the print shop the day it was taken. The print shop still has the original order file.", "options": [
                _bye("Goodbye.")]},
            # Reached only by her memory answer, from night 2 (specs/earlier-nights.md, point 5).
            "again": {"text": "The clerk stops with her hand on the printer. \"The seventeenth of October. Yes. How do you...?\" She looks at the clock. \"I have been closing in ten minutes for a very long time.\" She frowns at the counter. \"Odd. I do not remember you leaving.\"",
                      "note": "The clerk agreed with the date before you finished saying it: the cover photo was printed on 17 October.", "options": [
                _bye("Goodbye.")]},
        }},
        "leonor": {"name": "Leonor", "nodes": {
            "start": {"text": "Leonor closes her book slowly. \"You are here about Duarte. I know.\"", "trust": 2, "options": [
                {"label": "Ask if she is sure he was in the group", "next": "sure"},
                {"label": "Tell her you have doubts", "next": "soft"},
                {"label": "Ask which chat message is really hers", "next": "mine", "if": {"flags": {"colleague_choice": "help"}}},
                {"label": "Say she is lying", "next": "harsh", "cost": 5},
                {"label": "Tell her you knew she would say exactly that", "next": "again", "night": 3},
                _bye("Goodbye."),
            ]},
            # Leonor's claim line (point 7): broken by `tomas_word`.
            "sure": {"text": "\"He has been in every message for weeks. I have them right here.\" She taps her phone.", "trust": 2, "options": [
                {"label": "Ask to see the messages", "next": "messages"}]},
            # She vouches only for her own chat message (message 1), and names no other one.
            "mine": {"text": "\"The one asking to book the study room. I wrote that at this table, three weeks ago.\" Leonor scrolls with one finger. \"The ones from the number I did not know all arrived within minutes of each other, last night.\"", "trust": 3,
                     "note": "Leonor wrote the chat message about booking the study room herself.", "options": [
                _bye("Goodbye.")]},
            "messages": {"text": "\"Look. All from a number I did not know. Some are dated weeks ago, but they arrived last night.\"", "trust": 3,
                         "note": "Leonor received Duarte's messages last night, from an unknown number.", "options": [
                _bye("Goodbye.")]},
            "soft": {"text": "\"I wanted to believe you.\" She looks at her phone. \"Maybe I should look again.\"", "trust": 3, "options": [
                {"label": "Ask to see the messages", "next": "messages"}]},
            "harsh": {"text": "\"Excuse me?\" Her voice hardens.", "trust": 1, "options": [
                {"label": "Apologise", "next": "soft"},
                {"label": "Insist", "next": "closed", "cost": 5}]},
            "closed": {"text": "Leonor stands up. \"Come back with proof, not accusations.\"", "trust": 0, "options": [_bye("Leave.")]},
            # Reached only by her memory answer, from night 3.
            "again": {"text": "Leonor's hand stays on the book. \"Word for word? Nobody knows what I am going to say.\" She studies your scarf. \"Have we done this before?\"", "trust": 3, "options": [
                _bye("Goodbye.")]},
        }},
        "tomas": {"name": "Tomás", "nodes": {
            "start": {"text": "Tomás is hunched over computer 11, avoiding your eyes. \"Oh. Hi. It is late.\"", "trust": 2, "options": [
                {"label": "Ask kindly what he is doing here", "next": "kind"},
                {"label": "Demand to know why he lied about Duarte", "next": "hard", "cost": 5},
                # A memory answer, a shortcut to his claim line: from night 2 the player already knows the
                # message, so it has no `if` and is the one way to `slides` before the files are viewed.
                {"label": "Tell him you know what the chat says about the slides", "next": "slides", "night": 2},
                _bye("Goodbye."),
            ]},
            "kind": {"text": "\"I could not sleep, I just came here to finish the slides. And... I saw someone at computer 12 last night, near midnight.\"", "trust": 3, "options": [
                {"label": "Ask who it was", "next": "who"},
                {"label": "Tell him that sounds like an excuse", "next": "hard"}]},
            "password": {"text": "\"The password of computer 12? It is the group's: the day and the month we took the cover photo. Four digits. I can never remember the date, but between all of us we can work it out.\"", "trust": 3,
                         "note": "Tomás: the password of computer 12 is the day and month the cover photo was taken (4 digits).", "options": [
                # Two answers on every line (specs/two-answers.md): after the files, the slides; before them,
                # with the original photo, the photo.
                {"label": "Ask who made the slides", "next": "slides", "if": {"flags": {"files_viewed": True}}},
                {"label": "Show him the original photo", "next": "photo",
                 "if": {"has": ["original_photo"], "flags": {"files_viewed": False}}},
                {"label": "Tell him he should know the date by heart", "next": "hard"}]},
            "who": {"text": "\"Only a hood. Like the one Duarte wears. But nobody ever saw him arrive.\"", "trust": 3,
                    "note": "Tomás saw someone in a hood at computer 12 near midnight.", "options": [
                {"label": "Ask for the password of computer 12", "next": "password"},
                {"label": "Ask if the one in the hood was him", "next": "hard"}]},
            # Tomás's claim line (point 7): broken by `files`, the history that shows who made the slides.
            # The right answer reminds him of it and makes him give in (`crack`: the page shows that card
            # to him, the `confront` operation); the wrong one leaves him convinced (specs/two-answers.md).
            "slides": {"text": "Tomás keeps his eyes on the screen. \"The slides? I am finishing them. But the chat says Duarte did them, under my name. So maybe he did, and I only tidied up.\"", "trust": 2,
                       "note": "Tomás thinks Duarte may have made the slides, only because a chat message under his own name says so.", "options": [
                {"label": "Remind him the file history has his name on every version of the slides", "next": "slides",
                 "crack": "files", "if": {"flags": {"files_viewed": True}}},
                {"label": "Tell him that then the credit is Duarte's", "next": "convinced"}]},
            "convinced": {"text": "Tomás nods without looking up. \"Yeah. Maybe that is fairer. He did more than I think.\"", "trust": 2,
                          "options": [_bye("Goodbye.")]},
            "hard": {"text": "\"Excuse me? I did not lie!\" His voice shakes.", "trust": 1, "options": [
                {"label": "Apologise", "next": "calm"},
                {"label": "Push harder", "next": "closed", "cost": 5}]},
            "calm": {"text": "\"Fine. It has been a long night. Ask properly.\"", "trust": 2, "options": [
                {"label": "Ask kindly what he is doing here", "next": "kind"},
                {"label": "Insist that he lied", "next": "closed"}]},
            "photo": {"text": "Tomás stares at the photo. \"Four people... I never noticed.\" He swallows.", "trust": 2, "options": [
                {"label": "Ask him to help you", "next": "help"},
                {"label": "Tell him it is his fault", "next": "hard"}]},
            "help": {"text": "\"All right. Save the group's conversations before someone deletes them. Not everything on my phone is mine.\"", "trust": 3,
                     "note": "Tomás hints that some chat messages are not from the people they name.", "options": [
                _bye("Goodbye.")]},
            "closed": {"text": "Tomás crosses his arms. \"We are done here.\"", "trust": 0, "options": [_bye("Leave.")]},
        }},
        "computer12": {"name": "Computer 12", "nodes": {
            "start": {"text": "Computer 12 is still on, with the group's session open. It asks for a 4-digit password.", "options": [_bye("Step away from the computer.")]},
        }},
        "professor": {"name": "Professor", "nodes": {
            "start": {"text": "The professor looks up from the list of groups. \"Is this about tomorrow's presentations?\"", "options": [
                {"label": "Ask how many members your group has on the list", "next": "list"},
                {"label": "Say you will bring proof", "next": "proof"},
                {"label": "Ask if he has heard this case before", "next": "again", "night": 4},
                _bye("Goodbye."),
            ]},
            "list": {"text": "\"Five, according to the cover. Is something wrong with that?\"", "options": [
                {"label": "Say there are only four of you", "next": "evidence"}]},
            "evidence": {"text": "\"Then I need evidence, not a feeling. Bring me the history of the project.\"",
                         "note": "The professor wants the project history as evidence.", "options": [
                _bye("Goodbye.")]},
            "proof": {"text": "\"Evidence is welcome. Present it when you are ready.\"", "options": [
                _bye("Goodbye.")]},
            # Reached only by his memory answer, from night 4.
            "again": {"text": "The professor turns a page of the list, then turns it back. \"Every year a group comes to me with one name too many. Never the same group. Always the same name.\"", "options": [
                _bye("Goodbye.")]},
        }},
        "duarte": {"name": "Duarte", "nodes": {
            "start": {"text": "Duarte smiles calmly. \"Ah, the fourth wheel. Ready for tomorrow?\"", "trust": 3, "options": [
                {"label": "Ask which part of the project he did", "next": "part"},
                {"label": "Tell him you know the truth", "next": "know", "cost": 5},
                {"label": "Ask him how many nights this has been", "next": "again", "night": 2},
                _bye("Goodbye."),
            ]},
            "part": {"text": "\"The slides, of course. Ask anyone.\" He hesitates for a second.", "trust": 3, "options": [
                {"label": "Ask which slide", "next": "slide"}]},
            "slide": {"text": "\"The... intro. The nice one.\" Duarte glances at the door. \"Why all these questions?\"", "trust": 2,
                      "note": "Duarte could not say which slide he made.", "options": [
                _bye("Goodbye.")]},
            "know": {"text": "\"Know what? Careful with accusations.\"", "trust": 1, "options": [
                {"label": "Press him", "next": "closed", "cost": 5},
                {"label": "Back off", "next": "start"}]},
            "closed": {"text": "Duarte laughs and turns away. The conversation is over.", "trust": 0, "options": [_bye("Leave.")]},
            # Reached only by his memory answer, from night 2.
            "again": {"text": "Duarte's smile does not move. \"For you? I have lost count. For me there is only ever tonight.\" He looks at your coat as if it were his. \"You again. I was starting to enjoy the company.\"", "trust": 2, "options": [
                _bye("Goodbye.")]},
        }},
    },
    "pt": {
        "rita": {"name": "Rita", "nodes": {
            # Two answers on every line, a right one and a wrong one (specs/two-answers.md): the USB stick,
            # the photo, her claim line, Duarte, then the chat. Every wrong answer upsets her; an apology
            # brings the first question back. Rita has no trust level and no rude answer that costs time.
            "start": {"text": "A Rita levanta os olhos do portátil. \"Estás com cara de quem não dormiu nada. Conseguiste descansar alguma coisa?\"", "options": [
                {"label": "Perguntar onde está a pen", "next": "pen"},
                {"label": "Dizer-lhe que foi ela que perdeu a pen", "next": "upset"},
                # A memory answer (specs/earlier-nights.md, point 5): a shortcut to her claim line.,
                {"label": "Dizer-lhe que te lembras de ela contar as cabeças", "next": "five", "night": 3},
                _bye("Até já."),
            ]},
            "pen": {"text": "\"A pen? Devia estar aqui, mas não a encontro.\" Olha para a mesa. \"Ontem ficámos aqui até tarde a comer pizza, mas com esta confusão, pode estar em qualquer lado.\"", "note": "Rita: não encontra a pen. O grupo comeu pizza aqui ontem à noite.", "options": [
                {"label": "Perguntar pela fotografia do grupo", "next": "photo"},
                {"label": "Dizer-lhe que procure ela, que a confusão é dela", "next": "upset"},
            ]},
            "photo": {"text": "\"A fotografia? Tirámo-la depois da última reunião, nós os quatro.\"", "note": "A Rita lembra-se de quatro pessoas na fotografia do grupo.", "options": [
                {"label": "Perguntar porque é que a fotografia da pasta mostra cinco", "next": "five"},
                {"label": "Dizer-lhe que a memória dela não conta", "next": "upset"},
            ]},
            # Rita's claim line (specs/evidence-and-hearing.md, point 7): the right answer reminds her of a
            # proof and makes her give in (the photo when it is held, otherwise the files); with no proof yet,
            # the right answer moves on to Duarte. The wrong one agrees with her.
            "five": {"text": "\"Então contei mal.\" A Rita vira o portátil para ti: cinco pessoas. \"Uma fotografia não muda. A minha memória muda. Ele devia estar mesmo ali.\"", "options": [
                {"label": "Lembrar-lhe a fotografia original da reprografia: quatro pessoas", "next": "five", "if": {"has": ["original_photo"]}, "crack": "original_photo"},
                {"label": "Lembrar-lhe que o histórico dos ficheiros tem quatro autores em todas as cópias", "next": "five", "if": {"lacks": ["original_photo"], "flags": {"files_viewed": True}}, "crack": "files"},
                {"label": "Perguntar o que ela se lembra do Duarte", "next": "duarte", "if": {"lacks": ["original_photo"], "flags": {"files_viewed": False}}},
                {"label": "Concordar que ela deve ter contado mal", "next": "counted"},
            ]},
            "counted": {"text": "A Rita acena devagar. \"Pois. Uma fotografia não mente.\" Vira o portátil outra vez.", "options": [
                {"label": "Perguntar o que ela se lembra do Duarte", "next": "duarte"},
                {"label": "Dizer-lhe que então o Duarte fica no grupo", "next": "upset"},
            ]},
            "duarte": {"text": "\"O Duarte... sinceramente, não o consigo imaginar. Sempre que tento, só vejo o nome na capa.\"", "options": [
                {"label": "Dizer que achas que o nome foi acrescentado ontem à noite", "next": "warned"},
                {"label": "Dizer que então ele faz mesmo parte do grupo", "next": "upset"},
            ]},
            "warned": {"text": "A Rita fica calada. \"Se for verdade, alguém quis que duvidássemos de nós próprios.\"", "note": "A Rita também desconfia do quinto nome.", "options": [
                {"label": "Perguntar pelas mensagens do chat", "next": "chat", "if": {"flags": {"files_viewed": True}}},
                {"label": "Dizer-lhe que vais procurar provas", "next": "promise", "if": {"flags": {"files_viewed": False}}},
                {"label": "Dizer-lhe que é tudo imaginação dela", "next": "upset"},
            ]},
            "promise": {"text": "\"Vai. Eu fico aqui.\" A Rita volta a abrir o portátil.", "options": [
                _bye("Até já."),
            ]},
            "chat": {"text": "\"Repara na hora a que as mensagens chegam. Algumas dizem há três semanas, mas no meu telemóvel aparecem como novas, de ontem à noite. Mensagens antigas não funcionam assim.\"", "note": "Rita: uma mensagem antiga não chega como nova. As mensagens sobre o Duarte chegaram ontem à noite.", "options": [
                _bye("Até já."),
            ]},
            "upset": {"text": "A Rita fecha o portátil devagar. \"Não precisas de falar assim comigo. Estamos todos cansados.\"", "options": [
                {"label": "Pedir desculpa", "next": "sorry"},
                {"label": "Dizer que só estás a ser sincero", "next": "closed"},
            ]},
            "sorry": {"text": "\"Está bem. Pergunta lá.\"", "options": [
                {"label": "Perguntar onde está a pen", "next": "pen"},
                {"label": "Dizer-lhe que foi ela que perdeu a pen", "next": "upset"},
            ]},
            "closed": {"text": "A Rita põe os auscultadores. Já não te está a ouvir.", "options": [
                _bye("Sair."),
            ]},
        }},
        "amelia": {"name": "Funcionária", "nodes": {
            "start": {"text": "A funcionária ajeita os óculos. \"Fechamos daqui a dez minutos, do que precisas?\"", "options": [
                {"label": "Perguntar pelo pedido da fotografia da capa", "next": "order"},
                {"label": "Dizer a data antes dela", "next": "again", "night": 2},
                _bye("Até já."),
            ]},
            "order": {"text": "\"A fotografia da capa? Tiraram-na e mandaram-na imprimir aqui no mesmo dia. Eram quatro pessoas, ainda me lembro, e acho que o ficheiro original do pedido ainda está guardado.\"",
                      "note": "A fotografia da capa foi impressa na reprografia no dia em que foi tirada. A reprografia ainda tem o ficheiro original do pedido.", "options": [
                _bye("Até já.")]},
            "again": {"text": "A funcionária fica com a mão parada na impressora. \"Dezassete de outubro. Sim. Como é que tu...?\" Olha para o relógio. \"Há muito tempo que estou a fechar daqui a dez minutos.\" Franze a testa para o balcão. \"Estranho. Não me lembro de te ver sair.\"",
                      "note": "A funcionária confirmou a data antes de acabares de a dizer: a fotografia da capa foi impressa a 17 de outubro.", "options": [
                _bye("Até já.")]},
        }},
        "leonor": {"name": "Leonor", "nodes": {
            "start": {"text": "A Leonor fecha o livro devagar. \"Vens por causa do Duarte. Eu sei.\"", "trust": 2, "options": [
                {"label": "Perguntar se tem a certeza de que ele estava no grupo", "next": "sure"},
                {"label": "Dizer-lhe que tens dúvidas", "next": "soft"},
                {"label": "Perguntar que mensagem do chat é mesmo dela", "next": "mine", "if": {"flags": {"colleague_choice": "help"}}},
                {"label": "Dizer que ela está a mentir", "next": "harsh", "cost": 5},
                {"label": "Dizer-lhe que sabias que ela ia dizer exatamente isso", "next": "again", "night": 3},
                _bye("Até já."),
            ]},
            "sure": {"text": "\"Está em todas as mensagens há semanas. Tenho-as aqui.\" Toca no telemóvel.", "trust": 2, "options": [
                {"label": "Pedir para ver as mensagens", "next": "messages"}]},
            "mine": {"text": "\"A que pede para reservar a sala de estudo. Escrevi-a nesta mesa, há três semanas.\" A Leonor percorre o ecrã com um dedo. \"As do número que eu não conhecia chegaram todas com minutos de diferença, ontem à noite.\"", "trust": 3,
                     "note": "A Leonor escreveu ela própria a mensagem do chat sobre reservar a sala de estudo.", "options": [
                _bye("Até já.")]},
            "messages": {"text": "\"Olha. Todas de um número que eu não conhecia. Algumas têm data de há semanas, mas chegaram ontem à noite.\"", "trust": 3,
                         "note": "A Leonor recebeu as mensagens do Duarte ontem à noite, de um número desconhecido.", "options": [
                _bye("Até já.")]},
            "soft": {"text": "\"Eu queria acreditar em ti.\" Olha para o telemóvel. \"Talvez devesse ver outra vez.\"", "trust": 3, "options": [
                {"label": "Pedir para ver as mensagens", "next": "messages"}]},
            "harsh": {"text": "\"Desculpa?\" A voz dela endurece.", "trust": 1, "options": [
                {"label": "Pedir desculpa", "next": "soft"},
                {"label": "Insistir", "next": "closed", "cost": 5}]},
            "closed": {"text": "A Leonor levanta-se. \"Volta com provas, não com acusações.\"", "trust": 0, "options": [_bye("Sair.")]},
            "again": {"text": "A mão da Leonor fica em cima do livro. \"Palavra por palavra? Ninguém sabe o que eu vou dizer.\" Fica a olhar para o teu cachecol. \"Já fizemos isto antes?\"", "trust": 3, "options": [
                _bye("Até já.")]},
        }},
        "tomas": {"name": "Tomás", "nodes": {
            "start": {"text": "O Tomás está curvado sobre o computador 11, a evitar o teu olhar. \"Ah. Olá. Já é tarde.\"", "trust": 2, "options": [
                {"label": "Perguntar com calma o que está ali a fazer", "next": "kind"},
                {"label": "Exigir saber porque mentiu sobre o Duarte", "next": "hard", "cost": 5},
                {"label": "Dizer-lhe que já sabes o que o chat diz sobre os slides", "next": "slides", "night": 2},
                _bye("Até já."),
            ]},
            "kind": {"text": "\"Não conseguia dormir e vim acabar os slides. Ontem à noite, perto da meia-noite, vi alguém no computador 12.\"", "trust": 3, "options": [
                {"label": "Perguntar quem era", "next": "who"},
                {"label": "Dizer-lhe que isso parece uma desculpa", "next": "hard"}]},
            "password": {"text": "\"A password do computador? É o dia e o mês em que tirámos a fotografia da capa. São só 4 números, mas nunca me lembro da data. Entre todos havemos de lá chegar.\"", "trust": 3,
                         "note": "Tomás: a password do computador 12 é o dia e o mês em que foi tirada a fotografia da capa (4 algarismos).", "options": [
                {"label": "Perguntar quem fez os slides", "next": "slides", "if": {"flags": {"files_viewed": True}}},
                {"label": "Mostrar-lhe a fotografia original", "next": "photo",
                 "if": {"has": ["original_photo"], "flags": {"files_viewed": False}}},
                {"label": "Dizer-lhe que devia saber a data de cor", "next": "hard"}]},
            "who": {"text": "\"Só vi um capuz. Como o que o Duarte usa. Mas ninguém o viu chegar.\"", "trust": 3,
                    "note": "O Tomás viu alguém de capuz no computador 12 perto da meia-noite.", "options": [
                {"label": "Perguntar a password do computador 12", "next": "password"},
                {"label": "Perguntar se o do capuz era ele", "next": "hard"}]},
            "slides": {"text": "O Tomás não tira os olhos do ecrã. \"Os slides? Estou a acabá-los. Mas o chat diz que foram do Duarte, com o meu nome. Se calhar foram mesmo, e eu só arrumei.\"", "trust": 2,
                       "note": "O Tomás acha que os slides podem ter sido do Duarte, só porque uma mensagem do chat com o nome dele o diz.", "options": [
                {"label": "Lembrar-lhe que o histórico dos ficheiros tem o nome dele em todas as versões dos slides", "next": "slides",
                 "crack": "files", "if": {"flags": {"files_viewed": True}}},
                {"label": "Dizer-lhe que então o crédito é do Duarte", "next": "convinced"}]},
            "convinced": {"text": "O Tomás acena sem levantar os olhos. \"Pois. Se calhar é mais justo. Ele fez mais do que eu penso.\"", "trust": 2,
                          "options": [_bye("Até já.")]},
            "hard": {"text": "\"Como? Eu não menti!\" A voz dele treme.", "trust": 1, "options": [
                {"label": "Pedir desculpa", "next": "calm"},
                {"label": "Pressionar mais", "next": "closed", "cost": 5}]},
            "calm": {"text": "\"Está bem. Foi uma noite longa. Pergunta com educação.\"", "trust": 2, "options": [
                {"label": "Perguntar com calma o que está ali a fazer", "next": "kind"},
                {"label": "Insistir que ele mentiu", "next": "closed"}]},
            "photo": {"text": "O Tomás fica a olhar para a fotografia. \"Quatro pessoas... nunca tinha reparado.\" Engole em seco.", "trust": 2, "options": [
                {"label": "Pedir-lhe ajuda", "next": "help"},
                {"label": "Dizer-lhe que a culpa é dele", "next": "hard"}]},
            "help": {"text": "\"Está bem. Guarda as conversas do grupo antes que alguém as apague. Nem tudo o que está no meu telemóvel é meu.\"", "trust": 3,
                     "note": "O Tomás sugere que algumas mensagens do chat não são de quem diz.", "options": [
                _bye("Até já.")]},
            "closed": {"text": "O Tomás cruza os braços. \"Ficamos por aqui.\"", "trust": 0, "options": [_bye("Sair.")]},
        }},
        "computer12": {"name": "Computador 12", "nodes": {
            "start": {"text": "O computador 12 ainda está ligado, com a sessão do grupo aberta. Pede uma password de 4 algarismos.", "options": [_bye("Afastar-me do computador.")]},
        }},
        "professor": {"name": "Professor", "nodes": {
            "start": {"text": "O professor levanta os olhos da lista de grupos. \"É sobre as apresentações de amanhã?\"", "options": [
                {"label": "Perguntar quantos elementos tem o teu grupo na lista", "next": "list"},
                {"label": "Dizer que vais trazer provas", "next": "proof"},
                {"label": "Perguntar se já ouviu este caso", "next": "again", "night": 4},
                _bye("Até já."),
            ]},
            "list": {"text": "\"Cinco, segundo a capa. Há algum problema?\"", "options": [
                {"label": "Dizer que vocês são só quatro", "next": "evidence"}]},
            "evidence": {"text": "\"Então preciso de provas, não de uma sensação. Traga-me o histórico do projeto.\"",
                         "note": "O professor quer o histórico do projeto como prova.", "options": [
                _bye("Até já.")]},
            "proof": {"text": "\"Provas são bem-vindas. Apresente-as quando estiver pronto.\"", "options": [
                _bye("Até já.")]},
            "again": {"text": "O professor vira uma página da lista e volta a virá-la. \"Todos os anos me aparece um grupo com um nome a mais. Nunca é o mesmo grupo. É sempre o mesmo nome.\"", "options": [
                _bye("Até já.")]},
        }},
        "duarte": {"name": "Duarte", "nodes": {
            "start": {"text": "O Duarte sorri com calma. \"Ah, o quarto elemento. Pronto para amanhã?\"", "trust": 3, "options": [
                {"label": "Perguntar que parte do projeto fez", "next": "part"},
                {"label": "Dizer-lhe que sabes a verdade", "next": "know", "cost": 5},
                {"label": "Perguntar-lhe quantas noites já foram", "next": "again", "night": 2},
                _bye("Até já."),
            ]},
            "part": {"text": "\"Os slides, claro. Pergunta a qualquer um.\" Hesita por um segundo.", "trust": 3, "options": [
                {"label": "Perguntar que slide", "next": "slide"}]},
            "slide": {"text": "\"A... introdução. A bonita.\" O Duarte olha para a porta. \"Porquê tantas perguntas?\"", "trust": 2,
                      "note": "O Duarte não soube dizer que slide fez.", "options": [
                _bye("Até já.")]},
            "know": {"text": "\"Que verdade? Cuidado com as acusações.\"", "trust": 1, "options": [
                {"label": "Pressioná-lo", "next": "closed", "cost": 5},
                {"label": "Recuar", "next": "start"}]},
            "closed": {"text": "O Duarte ri-se e vira-te as costas. A conversa acabou.", "trust": 0, "options": [_bye("Sair.")]},
            "again": {"text": "O sorriso do Duarte não se mexe. \"Para ti? Já perdi a conta. Para mim só existe esta noite.\" Olha para o teu casaco como se fosse dele. \"Outra vez tu. Já estava a gostar da companhia.\"", "trust": 2, "options": [
                _bye("Até já.")]},
        }},
    },
}


# ---------- trust has consequences (specs/trust-has-consequences.md) ----------
# The texts below are in their own tables, so PEOPLE (and the trust values the reviewed tests compare)
# is never touched. They are used only while a person is wary or hostile: see `temper`.
# None of them names the culprit, a date of the photo or a code.

# The three people who have rude answers (the answers with a `cost`): only they have a temper (point 1).
TEMPERS = ("leonor", "tomas", "duarte")

# Curt lines, wary or hostile (point 4): a short text, the same note, so no clue in the diary is lost.
COLD = {
    "en": {
        "tomas": {"start": 'Tomás does not look up from computer 11. "What now?"',
                  "kind": '"Finishing the slides." He keeps typing. "Someone was at computer 12 last night. That is all I know."',
                  "password": '"The day and month of the cover photo. Four digits." He does not look up.',
                  "who": '"Someone in a hood, at computer 12." He keeps typing.'},
        "leonor": {"start": 'Leonor does not close her book this time. "Yes?"',
                   "messages": '"From a number I did not know. Last night."'},
        "duarte": {"start": 'Duarte does not bother to smile. "Still here?"',
                   "part": '"The slides. Ask anyone." He looks past you.'},
    },
    "pt": {
        "tomas": {"start": 'O Tomás nem levanta os olhos do computador 11. "O que foi agora?"',
                  "kind": '"A acabar os slides." Continua a escrever. "Esteve alguém no computador 12 ontem à noite. É tudo o que sei."',
                  "password": '"O dia e o mês da fotografia da capa. Quatro algarismos." Nem levanta os olhos.',
                  "who": '"Alguém de capuz, no computador 12." Continua a escrever.'},
        "leonor": {"start": 'Desta vez a Leonor não fecha o livro. "Sim?"',
                   "messages": '"De um número que eu não conhecia. Ontem à noite."'},
        "duarte": {"start": 'O Duarte nem se dá ao trabalho de sorrir. "Ainda por aqui?"',
                   "part": '"Os slides. Pergunta a qualquer um." Olha para além de ti.'},
    },
}

# Withheld lines, wary or hostile (point 4): a short text and no note, the hint is not given. They are
# hints only: every clue needed for an ending has another source.
WITHHELD = {
    "en": {
        "tomas": {"help": 'Tomás looks at the photo a second too long. "Check what you like. I am busy."'},
        "leonor": {"mine": '"Work it out yourself."'},
        "duarte": {"slide": '"Why would I tell you?" Duarte glances at the door.'},
    },
    "pt": {
        "tomas": {"help": 'O Tomás fica a olhar para a fotografia um segundo a mais. "Vê o que quiseres. Estou ocupado."'},
        "leonor": {"mine": '"Descobre tu."'},
        "duarte": {"slide": '"Porque é que te havia de dizer?" O Duarte olha para a porta.'},
    },
}

# The lie of a hostile Leonor (point 5). The player can check it: the backup of the original
# conversations (specs/computer-lab-backup.md) and Rita's `chat` line say otherwise. Tomás's lie was on
# his line about message 5, which is gone with the chat (specs/two-answers.md). A lie is not a claim: a card shown on it
# gets the usual rebuff. Its note is what the player was told.
LIES = {
    "en": {
        "leonor": {"messages": {"text": '"Nothing strange about them. They came on the dates they say, weeks ago." She turns the phone face down.',
                                "note": "Leonor says the messages arrived on their dates, weeks ago."}},
    },
    "pt": {
        "leonor": {"messages": {"text": '"Não têm nada de estranho. Chegaram nas datas que lá dizem, há semanas." Vira o telemóvel ao contrário.',
                                "note": "A Leonor diz que as mensagens chegaram nas datas delas, há semanas."}},
    },
}

# Who warns whom while hostile (point 6): the chain is fixed.
WARNS = {"tomas": "leonor", "leonor": "rita", "duarte": "professor"}

# The first line (`start`) of the person who was warned, while the warner is hostile and not cracked.
WARNED = {
    "en": {"leonor": 'Leonor closes her book before you reach the table. "Tomás texted me. He says you are going round calling people liars."',
           "rita": 'Rita looks up and does not smile. "Leonor says you shouted at her in the library. Is that true?"',
           "professor": 'The professor looks up from the list and does not smile. "Duarte tells me you threatened him. I hope you bring evidence tomorrow, not that."'},
    "pt": {"leonor": 'A Leonor fecha o livro antes de chegares à mesa. "O Tomás mandou-me mensagem. Diz que andas por aí a chamar mentirosos às pessoas."',
           "rita": 'A Rita levanta os olhos e não sorri. "A Leonor diz que lhe gritaste na biblioteca. É verdade?"',
           "professor": 'O professor levanta os olhos da lista e não sorri. "O Duarte diz-me que o ameaçou. Espero que amanhã me traga provas, e não isso."'},
}


def people_in_room(scene, state, language, gone=()):
    """Who stands in the room of this saved scene (Leonor leaves after being accused).

    `gone` are the people who have left by the night's schedule (specs/night-schedule.md, point 5).
    """
    room = room_of_scene(scene)
    found = []
    for person, where in ROOM_OF_PERSON.items():
        if where != room or person in gone:
            continue
        if person == "leonor" and state["flags"]["colleague_choice"] == "accused":
            continue
        found.append({"id": person, "name": PEOPLE[language][person]["name"], "object": person in OBJECTS})
    return found


def is_open(option, state, night):
    """True when an answer can be chosen now: its story condition `if` is true and its `night` has
    come (specs/earlier-nights.md, point 5). An answer without them is always open."""
    # logic._condition_met is the story's own rule for "has" / "flags" conditions.
    return logic._condition_met(option.get("if", {}), state) and night >= option.get("night", 1)


def offered(option):
    """An answer as the reply sends it: its label and next line, its cost, and `memory` for an
    answer you have heard before (the page draws a small ↺ in front of it)."""
    shown = {"label": option["label"], "next": option["next"]}
    if "cost" in option:
        shown["cost"] = option["cost"]
    if "night" in option:
        shown["memory"] = True
    if "crack" in option:   # the answer that makes the person give in (specs/two-answers.md)
        shown["crack"] = option["crack"]
    return shown


def talk(state, language, person, node, gone=(), night=1):
    """One step of a conversation: what the person says and the answers offered now. Writes nothing.

    `gone` are the people who have left by the night's schedule: they are not here any more.
    `night` is which night of this name tonight is (campus_memory.night_number): a memory answer is
    offered only from its own night on (specs/earlier-nights.md, point 5).
    """
    if not isinstance(person, str) or person not in ROOM_OF_PERSON:
        raise ValueError("Unknown person / Pessoa desconhecida.")
    if not isinstance(node, str) or node not in PEOPLE[language][person]["nodes"]:
        raise ValueError("Unknown answer / Resposta desconhecida.")
    here = [p["id"] for p in people_in_room(state["scene"], state, language, gone)]
    if state["ending"] != "none" or person not in here:
        raise ValueError("This person is not here / Esta pessoa não está aqui.")
    data = PEOPLE[language][person]
    line = data["nodes"][node]
    # A line cannot be asked for directly when every answer that leads to it is closed now (its `if`
    # is false, or its `night` has not come). A line no answer leads to (`start`) is never refused.
    inbound = [o for n in data["nodes"].values() for o in n["options"] if o["next"] == node]
    if inbound and not any(is_open(o, state, night) for o in inbound):
        raise ValueError("Unknown answer / Resposta desconhecida.")
    options = [offered(o) for o in line["options"] if is_open(o, state, night)]
    return {"npc": person, "name": data["name"], "node": node, "text": line["text"],
            "trust": line.get("trust"), "note": line.get("note", ""), "options": options}


def is_rude(language, person, node):
    """True when `node` is where an answer with a `cost` leads in this person's tree: the only lines
    the operation `rude` accepts (specs/trust-has-consequences.md, point 2)."""
    if not isinstance(person, str) or person not in PEOPLE[language]:
        return False
    lines = PEOPLE[language][person]["nodes"].values()
    return any(option["next"] == node and "cost" in option for line in lines for option in line["options"])


def temper(reply, moods, language):
    """A `talk` reply as a person with this temper says it (points 4 to 7). Writes nothing.

    `moods` is campus_evidence.moods(night): "calm", "wary" or "hostile" for Leonor, Tomás and Duarte.
    Only the text and the note change, never the answers or the actions, so the kept topics of
    specs/continuous-conversations.md stay the same. Which text wins: on `start`, the warning of a
    hostile warner, else the curt line; on any line, the lie when hostile, else the curt or the
    withheld line when wary or hostile. A calm person says the story's own line.
    """
    person, node = reply["npc"], reply["node"]
    mood = moods.get(person, "calm")   # Rita, the clerk and the professor are always calm
    warners = [warner for warner, listener in WARNS.items() if listener == person and moods.get(warner) == "hostile"]
    if node == "start" and warners:
        return dict(reply, text=WARNED[language][person])
    if mood == "hostile" and node in LIES[language].get(person, {}):
        lie = LIES[language][person][node]
        return dict(reply, text=lie["text"], note=lie["note"])
    if mood == "calm":
        return reply
    if node in COLD[language].get(person, {}):
        return dict(reply, text=COLD[language][person][node])   # the story's note stays
    if node in WITHHELD[language].get(person, {}):
        return dict(reply, text=WITHHELD[language][person][node], note="")
    return reply


# ---------- your own group (specs/your-own-group.md) ----------
# Three friends' names can take the teammates' places. They are only names: the ids (leonor, rita,
# tomas), the voices and the grammar of each place stay the story's (point 7).

# The story's names of the three places, in the order of the three fields of the start screen.
DEFAULT_GROUP = ["Leonor", "Rita", "Tomás"]
# 1 to 14 characters: letters (accented ones too), spaces, apostrophes (' and the ’ of phone
# keyboards) and hyphens. [^\W\d_] is "a letter": a word character that is not a digit or "_".
FRIEND_NAME = re.compile(r"(?:[^\W\d_]|[ '’-]){1,14}")


def clean_friend(text, story_name):
    """One field of the start screen, cleaned (point 3): spaces trimmed and made single, the first
    letter upper-cased ("ana" -> "Ana"). An empty or bad field gives the story's name of its place."""
    if not isinstance(text, str):
        return story_name
    name = " ".join(unicodedata.normalize("NFC", text).split())   # NFC: "João" typed as J-o-a-~-o is one letter ã
    if not FRIEND_NAME.fullmatch(name) or not any(letter.isalpha() for letter in name):
        return story_name
    first = next(place for place, letter in enumerate(name) if letter.isalpha())
    return name[:first] + name[first].upper() + name[first + 1:]


def clean_group(names):
    """The group of a new game: three names in the order of DEFAULT_GROUP (point 3). Each field is
    cleaned on its own; then, if two names are the same (ignoring case), one is Duarte, or one is the
    story's name of another place ("Rita" in Leonor's place), all three are the story's again, so a
    name can never stand for two people. It never raises: the fields are optional."""
    if not isinstance(names, list) or len(names) != len(DEFAULT_GROUP):
        return list(DEFAULT_GROUP)
    group = [clean_friend(text, story_name) for text, story_name in zip(names, DEFAULT_GROUP)]
    lower = [name.lower() for name in group]
    another_place = any(name.lower() == other.lower() for place, name in enumerate(group)
                        for other in DEFAULT_GROUP if other != DEFAULT_GROUP[place])
    if len(set(lower)) < len(group) or "duarte" in lower or another_place:
        return list(DEFAULT_GROUP)
    return group
