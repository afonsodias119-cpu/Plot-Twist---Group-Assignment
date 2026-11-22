"""The people of the 3D campus and their conversations (specs/campus-people-and-atmosphere.md).

A conversation is a small tree. Each node has what the person says, optional `trust` (0-3, shown as
hearts), an optional `note` (a line for the player's diary) and the answers the player can choose:
{"label", "next"} where next is another node id or None (the conversation ends).
There is no "Ask something else" answer (specs/chat-dialogues.md): the screen keeps the conversation
open and offers, after each answer, the topics of the opening menu not asked yet
(specs/continuous-conversations.md).
An answer can have "if": a story condition ({"has": [...], "flags": {...}}); it is offered only when true.
An answer can have "cost": minutes taken off the countdown when the player chooses it (the rude answers,
specs/harder-campus.md). The countdown lives in the browser; the server only passes the cost on.
The same ids and conditions exist in "en" and "pt"; only the texts differ.

Talking never changes the saved game. The server only reads it (to check the person is in the saved
room and which answers are offered).
"""

import logic

# Where each person stands (the id of the story scene) and when they are not there any more.
ROOM_OF_PERSON = {
    "rita": "study_room", "amelia": "print_shop", "leonor": "library",
    "tomas": "computer_lab", "computer12": "computer_lab", "professor": "auditorium", "duarte": "auditorium",
}
# Things that are used, not talked to (the panel says "Use", the screen says "press K to use").
OBJECTS = {"computer12"}
# The group chat is a scene of the story that has no room of its own: it happens in the computer lab.
ROOM_OF_SCENE = {"group_chat": "computer_lab"}


# The story actions that are done by talking to a person: they appear as choices inside that conversation.
# (The chat flags are done on the chat screen of computer 12, which the page draws over the picture.)
ACTION_PERSON = {
    "open_drawer": "rita", "request_copy": "amelia", "ask_for_help": "leonor", "accuse": "leonor",
    "view_files": "computer12", "open_chat": "computer12", "present_evidence": "professor",
}


def room_of_scene(scene):
    """The 3D room where a story scene takes place."""
    return ROOM_OF_SCENE.get(scene, scene)


def _bye(label):
    return {"label": label, "next": None}


PEOPLE = {
    "en": {
        "rita": {"name": "Rita", "nodes": {
            "start": {"text": "Rita looks up from her laptop. \"You look awful. Did you sleep at all?\"", "options": [
                {"label": "Ask about the group photo", "next": "photo"},
                {"label": "Ask what she remembers about Duarte", "next": "duarte"},
                {"label": "Ask where the USB stick is", "next": "pen"},
                {"label": "Ask about the chat messages", "next": "chat", "if": {"flags": {"files_viewed": True}}},
                _bye("Goodbye."),
            ]},
            "photo": {"text": "\"The photo? We took it after the last meeting. Four of us, Leonor held the timer. I remember counting heads.\"",
                      "note": "Rita remembers four people in the group photo.", "options": [
                _bye("Goodbye.")]},
            "pen": {"text": "\"The USB stick? It should be in the group drawer, but it is not.\" She looks at the table. \"We stayed here late last night eating pizza. With this mess, it could be anywhere.\"",
                    "note": "Rita: the USB stick is not in the drawer. The group ate pizza here last night.", "options": [_bye("Goodbye.")]},
            "duarte": {"text": "\"Duarte... honestly, I cannot picture him. Every time I try, I only see the name on the cover.\"", "options": [
                {"label": "Say you think the name was added last night", "next": "warned"}]},
            "warned": {"text": "Rita goes quiet. \"If that is true, somebody wanted us to doubt ourselves.\"",
                       "note": "Rita doubts the fifth name too.", "options": [
                _bye("Goodbye.")]},
            "chat": {"text": "\"Look at when the messages arrive. Some say three weeks ago, but my phone shows them as new, last night. That is not how old messages work.\"",
                     "note": "Rita: an old message does not arrive as new. Compare the arrival times in the group chat.", "options": [
                _bye("Goodbye.")]},
        }},
        "amelia": {"name": "Clerk", "nodes": {
            "start": {"text": "The clerk adjusts her glasses. \"We close in ten minutes. What do you need?\"", "options": [
                {"label": "Ask about the cover photo order", "next": "order"},
                {"label": "Ask if anyone else came asking", "next": "visitor"},
                _bye("Goodbye."),
            ]},
            "order": {"text": "\"On 14 November, last week. You took the photo and had it printed the same day. Four people in it, I remember because I had to crop the print. The original order file is still saved.\"",
                      "note": "The cover photo was taken and printed on 14 November. The print shop still has the original order file.", "options": [
                _bye("Goodbye.")]},
            "visitor": {"text": "\"A young man in a hood came by yesterday evening. He asked to reprint the cover with a different photo.\"",
                        "note": "A hooded stranger asked the print shop to change the cover photo.", "options": [
                {"label": "Ask what he looked like", "next": "hood"}]},
            "hood": {"text": "\"A calm smile. He did not want to leave a name. I thought he was one of your group.\"", "options": [
                _bye("Goodbye.")]},
        }},
        "leonor": {"name": "Leonor", "nodes": {
            "start": {"text": "Leonor closes her book slowly. \"You are here about Duarte. I know.\"", "trust": 2, "options": [
                {"label": "Ask if she is sure he was in the group", "next": "sure"},
                {"label": "Tell her you have doubts", "next": "soft"},
                {"label": "Say she is lying", "next": "harsh", "cost": 5},
                _bye("Goodbye."),
            ]},
            "sure": {"text": "\"He has been in every message for weeks. I have them right here.\" She taps her phone.", "trust": 2, "options": [
                {"label": "Ask to see the messages", "next": "messages"}]},
            "messages": {"text": "\"Look. All from a number I did not know. Some are dated weeks ago, but they arrived last night.\"", "trust": 3,
                         "note": "Leonor received Duarte's messages last night, from an unknown number.", "options": [
                _bye("Goodbye.")]},
            "soft": {"text": "\"I wanted to believe you.\" She looks at her phone. \"Maybe I should look again.\"", "trust": 3, "options": [
                {"label": "Ask to see the messages", "next": "messages"}]},
            "harsh": {"text": "\"Excuse me?\" Her voice hardens.", "trust": 1, "options": [
                {"label": "Apologise", "next": "soft"},
                {"label": "Insist", "next": "closed", "cost": 5}]},
            "closed": {"text": "Leonor stands up. \"Come back with proof, not accusations.\"", "trust": 0, "options": [_bye("Leave.")]},
        }},
        "tomas": {"name": "Tomás", "nodes": {
            "start": {"text": "Tomás is hunched over computer 11, avoiding your eyes. \"Oh. Hi. It is late.\"", "trust": 2, "options": [
                {"label": "Ask kindly what he is doing here", "next": "kind"},
                {"label": "Demand to know why he lied about Duarte", "next": "hard", "cost": 5},
                {"label": "Show him the original photo", "next": "photo", "if": {"has": ["original_photo"]}},
                _bye("Goodbye."),
            ]},
            "kind": {"text": "\"Could not sleep. I came to finish the slides. And... I saw someone at computer 12 last night, near midnight.\"", "trust": 3, "options": [
                {"label": "Ask who it was", "next": "who"},
                {"label": "Ask for the password of computer 12", "next": "password"},
                {"label": "Ask about message 5, the one with his name", "next": "msg5", "if": {"flags": {"files_viewed": True}}}]},
            "password": {"text": "\"The password of computer 12? It is the group's: the day and the month we took the cover photo. Four digits. I can never remember the date.\"", "trust": 3,
                         "note": "Tomás: the password of computer 12 is the day and month the cover photo was taken (4 digits).", "options": [_bye("Goodbye.")]},
            "who": {"text": "\"Only a hood. Like the one Duarte wears. But nobody ever saw him arrive.\"", "trust": 3,
                    "note": "Tomás saw someone in a hood at computer 12 near midnight.", "options": [
                _bye("Goodbye.")]},
            "msg5": {"text": "\"'Duarte did the slides'? I never wrote that. My phone buzzed with it at midnight, as if it was sent three weeks ago.\"", "trust": 3,
                     "note": "Tomás says he never wrote message 5; it arrived last night.", "options": [
                _bye("Goodbye.")]},
            "hard": {"text": "\"Excuse me? I did not lie!\" His voice shakes.", "trust": 1, "options": [
                {"label": "Apologise", "next": "calm"},
                {"label": "Push harder", "next": "closed", "cost": 5}]},
            "calm": {"text": "\"Fine. It has been a long night. Ask properly.\"", "trust": 2, "options": [
                {"label": "Ask kindly what he is doing here", "next": "kind"}, _bye("Goodbye.")]},
            "photo": {"text": "Tomás stares at the photo. \"Four people... I never noticed.\" He swallows.", "trust": 2, "options": [
                {"label": "Ask him to help you", "next": "help"}]},
            "help": {"text": "\"All right. Check the group chat. Not everything in there is mine.\"", "trust": 3,
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
                _bye("Goodbye."),
            ]},
            "list": {"text": "\"Five, according to the cover. Is something wrong with that?\"", "options": [
                {"label": "Say there are only four of you", "next": "evidence"}]},
            "evidence": {"text": "\"Then I need evidence, not a feeling. Bring me the history of the project.\"",
                         "note": "The professor wants the project history as evidence.", "options": [
                _bye("Goodbye.")]},
            "proof": {"text": "\"Evidence is welcome. Present it when you are ready.\"", "options": [
                _bye("Goodbye.")]},
        }},
        "duarte": {"name": "Duarte", "nodes": {
            "start": {"text": "Duarte smiles calmly. \"Ah, the fourth wheel. Ready for tomorrow?\"", "trust": 3, "options": [
                {"label": "Ask which part of the project he did", "next": "part"},
                {"label": "Tell him you know the truth", "next": "know", "cost": 5},
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
        }},
    },
    "pt": {
        "rita": {"name": "Rita", "nodes": {
            "start": {"text": "A Rita levanta os olhos do portátil. \"Estás com um ar péssimo. Dormiste alguma coisa?\"", "options": [
                {"label": "Perguntar pela fotografia do grupo", "next": "photo"},
                {"label": "Perguntar o que ela se lembra do Duarte", "next": "duarte"},
                {"label": "Perguntar onde está a pen", "next": "pen"},
                {"label": "Perguntar pelas mensagens do chat", "next": "chat", "if": {"flags": {"files_viewed": True}}},
                _bye("Até já."),
            ]},
            "photo": {"text": "\"A fotografia? Tirámo-la depois da última reunião. Quatro pessoas, a Leonor ficou com o temporizador. Lembro-me de contar as cabeças.\"",
                      "note": "A Rita lembra-se de quatro pessoas na fotografia do grupo.", "options": [
                _bye("Até já.")]},
            "pen": {"text": "\"A pen? Devia estar na gaveta do grupo, mas não está.\" Olha para a mesa. \"Ontem ficámos aqui até tarde a comer pizza. Com esta confusão, pode estar em qualquer lado.\"",
                    "note": "Rita: a pen não está na gaveta. O grupo comeu pizza aqui ontem à noite.", "options": [_bye("Até já.")]},
            "duarte": {"text": "\"O Duarte... sinceramente, não o consigo imaginar. Sempre que tento, só vejo o nome na capa.\"", "options": [
                {"label": "Dizer que achas que o nome foi acrescentado ontem à noite", "next": "warned"}]},
            "warned": {"text": "A Rita fica calada. \"Se for verdade, alguém quis que duvidássemos de nós próprios.\"",
                       "note": "A Rita também desconfia do quinto nome.", "options": [
                _bye("Até já.")]},
            "chat": {"text": "\"Repara na hora a que as mensagens chegam. Algumas dizem há três semanas, mas no meu telemóvel aparecem como novas, de ontem à noite. Mensagens antigas não funcionam assim.\"",
                     "note": "Rita: uma mensagem antiga não chega como nova. Compara as horas de chegada no chat do grupo.", "options": [
                _bye("Até já.")]},
        }},
        "amelia": {"name": "Funcionária", "nodes": {
            "start": {"text": "A funcionária ajeita os óculos. \"Fechamos daqui a dez minutos. Do que precisas?\"", "options": [
                {"label": "Perguntar pelo pedido da fotografia da capa", "next": "order"},
                {"label": "Perguntar se mais alguém veio perguntar", "next": "visitor"},
                _bye("Até já."),
            ]},
            "order": {"text": "\"A 14 de novembro, na semana passada. Tiraram a fotografia e mandaram-na imprimir no mesmo dia. Quatro pessoas, lembro-me porque tive de cortar a impressão. O ficheiro original do pedido ainda está guardado.\"",
                      "note": "A fotografia da capa foi tirada e impressa a 14 de novembro. A reprografia ainda tem o ficheiro original do pedido.", "options": [
                _bye("Até já.")]},
            "visitor": {"text": "\"Ontem ao fim da tarde passou por aqui um rapaz de capuz. Pediu para reimprimir a capa com outra fotografia.\"",
                        "note": "Um desconhecido de capuz pediu à reprografia para mudar a fotografia da capa.", "options": [
                {"label": "Perguntar como era ele", "next": "hood"}]},
            "hood": {"text": "\"Um sorriso calmo. Não quis deixar o nome. Pensei que fosse do vosso grupo.\"", "options": [
                _bye("Até já.")]},
        }},
        "leonor": {"name": "Leonor", "nodes": {
            "start": {"text": "A Leonor fecha o livro devagar. \"Vens por causa do Duarte. Eu sei.\"", "trust": 2, "options": [
                {"label": "Perguntar se tem a certeza de que ele estava no grupo", "next": "sure"},
                {"label": "Dizer-lhe que tens dúvidas", "next": "soft"},
                {"label": "Dizer que ela está a mentir", "next": "harsh", "cost": 5},
                _bye("Até já."),
            ]},
            "sure": {"text": "\"Está em todas as mensagens há semanas. Tenho-as aqui.\" Toca no telemóvel.", "trust": 2, "options": [
                {"label": "Pedir para ver as mensagens", "next": "messages"}]},
            "messages": {"text": "\"Olha. Todas de um número que eu não conhecia. Algumas têm data de há semanas, mas chegaram ontem à noite.\"", "trust": 3,
                         "note": "A Leonor recebeu as mensagens do Duarte ontem à noite, de um número desconhecido.", "options": [
                _bye("Até já.")]},
            "soft": {"text": "\"Eu queria acreditar em ti.\" Olha para o telemóvel. \"Talvez devesse ver outra vez.\"", "trust": 3, "options": [
                {"label": "Pedir para ver as mensagens", "next": "messages"}]},
            "harsh": {"text": "\"Desculpa?\" A voz dela endurece.", "trust": 1, "options": [
                {"label": "Pedir desculpa", "next": "soft"},
                {"label": "Insistir", "next": "closed", "cost": 5}]},
            "closed": {"text": "A Leonor levanta-se. \"Volta com provas, não com acusações.\"", "trust": 0, "options": [_bye("Sair.")]},
        }},
        "tomas": {"name": "Tomás", "nodes": {
            "start": {"text": "O Tomás está curvado sobre o computador 11, a evitar o teu olhar. \"Ah. Olá. Já é tarde.\"", "trust": 2, "options": [
                {"label": "Perguntar com calma o que está ali a fazer", "next": "kind"},
                {"label": "Exigir saber porque mentiu sobre o Duarte", "next": "hard", "cost": 5},
                {"label": "Mostrar-lhe a fotografia original", "next": "photo", "if": {"has": ["original_photo"]}},
                _bye("Até já."),
            ]},
            "kind": {"text": "\"Não conseguia dormir. Vim acabar os slides. E... vi alguém no computador 12 ontem à noite, perto da meia-noite.\"", "trust": 3, "options": [
                {"label": "Perguntar quem era", "next": "who"},
                {"label": "Perguntar a password do computador 12", "next": "password"},
                {"label": "Perguntar pela mensagem 5, a que tem o nome dele", "next": "msg5", "if": {"flags": {"files_viewed": True}}}]},
            "password": {"text": "\"A password do 12? É a do grupo: o dia e o mês em que tirámos a fotografia da capa. Quatro algarismos. Eu nunca me lembro da data.\"", "trust": 3,
                         "note": "Tomás: a password do computador 12 é o dia e o mês em que foi tirada a fotografia da capa (4 algarismos).", "options": [_bye("Até já.")]},
            "who": {"text": "\"Só vi um capuz. Como o que o Duarte usa. Mas ninguém o viu chegar.\"", "trust": 3,
                    "note": "O Tomás viu alguém de capuz no computador 12 perto da meia-noite.", "options": [
                _bye("Até já.")]},
            "msg5": {"text": "\"'O Duarte fez os slides'? Eu nunca escrevi isso. O meu telemóvel apitou com ela à meia-noite, como se tivesse sido enviada há três semanas.\"", "trust": 3,
                     "note": "O Tomás diz que nunca escreveu a mensagem 5; chegou ontem à noite.", "options": [
                _bye("Até já.")]},
            "hard": {"text": "\"Como? Eu não menti!\" A voz dele treme.", "trust": 1, "options": [
                {"label": "Pedir desculpa", "next": "calm"},
                {"label": "Pressionar mais", "next": "closed", "cost": 5}]},
            "calm": {"text": "\"Está bem. Foi uma noite longa. Pergunta com educação.\"", "trust": 2, "options": [
                {"label": "Perguntar com calma o que está ali a fazer", "next": "kind"}, _bye("Até já.")]},
            "photo": {"text": "O Tomás fica a olhar para a fotografia. \"Quatro pessoas... nunca tinha reparado.\" Engole em seco.", "trust": 2, "options": [
                {"label": "Pedir-lhe ajuda", "next": "help"}]},
            "help": {"text": "\"Está bem. Vê o chat do grupo. Nem tudo o que lá está é meu.\"", "trust": 3,
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
                _bye("Até já."),
            ]},
            "list": {"text": "\"Cinco, segundo a capa. Há algum problema?\"", "options": [
                {"label": "Dizer que vocês são só quatro", "next": "evidence"}]},
            "evidence": {"text": "\"Então preciso de provas, não de uma sensação. Traga-me o histórico do projeto.\"",
                         "note": "O professor quer o histórico do projeto como prova.", "options": [
                _bye("Até já.")]},
            "proof": {"text": "\"Provas são bem-vindas. Apresente-as quando estiver pronto.\"", "options": [
                _bye("Até já.")]},
        }},
        "duarte": {"name": "Duarte", "nodes": {
            "start": {"text": "O Duarte sorri com calma. \"Ah, o quarto elemento. Pronto para amanhã?\"", "trust": 3, "options": [
                {"label": "Perguntar que parte do projeto fez", "next": "part"},
                {"label": "Dizer-lhe que sabes a verdade", "next": "know", "cost": 5},
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
        }},
    },
}


def people_in_room(scene, state, language):
    """Who stands in the room of this saved scene (Leonor leaves after being accused)."""
    room = room_of_scene(scene)
    found = []
    for person, where in ROOM_OF_PERSON.items():
        if where != room:
            continue
        if person == "leonor" and state["flags"]["colleague_choice"] == "accused":
            continue
        found.append({"id": person, "name": PEOPLE[language][person]["name"], "object": person in OBJECTS})
    return found


def talk(state, language, person, node):
    """One step of a conversation: what the person says and the answers offered now. Writes nothing."""
    if not isinstance(person, str) or person not in ROOM_OF_PERSON:
        raise ValueError("Unknown person / Pessoa desconhecida.")
    if not isinstance(node, str) or node not in PEOPLE[language][person]["nodes"]:
        raise ValueError("Unknown answer / Resposta desconhecida.")
    if state["ending"] != "none" or person not in [p["id"] for p in people_in_room(state["scene"], state, language)]:
        raise ValueError("This person is not here / Esta pessoa não está aqui.")
    data = PEOPLE[language][person]
    line = data["nodes"][node]
    # A line that is reached only through conditional answers cannot be asked for directly.
    inbound = [o for n in data["nodes"].values() for o in n["options"] if o["next"] == node]
    if inbound and all("if" in o for o in inbound) and not any(logic._condition_met(o["if"], state) for o in inbound):
        raise ValueError("Unknown answer / Resposta desconhecida.")
    options = [dict({"label": o["label"], "next": o["next"]}, **({"cost": o["cost"]} if "cost" in o else {}))
               for o in line["options"]
               # logic._condition_met is the story's own rule for "has" / "flags" conditions.
               if logic._condition_met(o.get("if", {}), state)]
    return {"npc": person, "name": data["name"], "node": node, "text": line["text"],
            "trust": line.get("trust"), "note": line.get("note", ""), "options": options}
