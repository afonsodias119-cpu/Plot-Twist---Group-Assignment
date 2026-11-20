"""Plot Twist — the story content (data only).

Everything the player reads lives here, in English ("en") and Portuguese ("pt").
The two stories have exactly the same structure (scene ids, action ids, item ids,
conditions and effects); only the texts differ.

Sources: docs/story-en.md (English texts) and docs/historia.md (Portuguese texts,
ids, conditions and effects). See specs/base-game.md, section 2, for the shape.

How to read an action:
- offered_if: the action is shown only while this is true.
- requires: the action is accepted only when this is true; otherwise blocked_text.
- go_to / gives / sets / ends_game: what an accepted action changes.
A condition can have "has" (items held), "lacks" (items not held) and "flags".
"""

LANGUAGES = {"en": "English", "pt": "Português"}


STORY_EN = {
    "start": {
        "scene": "study_room",
        "inventory": [],
        "flags": {
            "colleague_choice": "none",
            "files_viewed": False,
            # One flag per group chat message: True once the player flags it as fake.
            "flagged_1": False,
            "flagged_2": False,
            "flagged_3": False,
            "flagged_4": False,
            "flagged_5": False,
        },
        "ending": "none",
    },
    "items": {
        "usb_stick": "USB stick with the project history",
        "original_photo": "Printed original photo",
    },
    "messages": {
        "game_over": "The story has ended. Start a new game to play again.",
        "not_here": "You cannot do that here.",
        "not_offered": "You have already done that.",
        "no_game": "Your saved game could not be found. Type your name to start again.",
    },
    "scenes": {
        "study_room": {
            "title": "Study room",
            "texts": [
                {
                    "when": {},
                    "text": 'It is night, the eve of the presentation. In the group folder, the photo shows five people. There are four of you. On the cover of the report there is a fifth name: Duarte Sequeira. In the chat, your teammates insist that he "was with us all along". Only you know that is a lie.',
                },
                {
                    "when": {"has": ["usb_stick"]},
                    "text": "The group drawer is empty.",
                },
            ],
            "actions": {
                "open_drawer": {
                    "label": "Open the group drawer",
                    "offered_if": {"lacks": ["usb_stick"]},
                    "gives": "usb_stick",
                    "result_text": "You find the USB stick where the group kept the project backups. You take the USB stick.",
                },
                "go_print_shop": {"label": "Go to the print shop", "go_to": "print_shop"},
                "go_library": {"label": "Go to the library", "go_to": "library"},
                "go_computer_lab": {"label": "Go to the computer lab", "go_to": "computer_lab"},
                "go_auditorium": {
                    "label": "Go to the auditorium",
                    "requires": {"flags": {"files_viewed": True}},
                    "blocked_text": "You have no proof yet. The professor will not listen to you on a suspicion alone.",
                    "go_to": "auditorium",
                },
            },
        },
        "print_shop": {
            "title": "Print shop",
            "texts": [
                {
                    "when": {},
                    "text": "The print shop is about to close. The clerk remembers your group: you printed the photo for the report cover here last week.",
                },
                {
                    "when": {"has": ["original_photo"]},
                    "text": "The clerk has already given you a copy of the original order.",
                },
            ],
            "actions": {
                "request_copy": {
                    "label": "Ask for a copy of the original order",
                    "offered_if": {"lacks": ["original_photo"]},
                    "gives": "original_photo",
                    "result_text": "The clerk prints again the file that was saved with the order. The original photo shows four people. You take the photo.",
                },
                "go_study_room": {"label": "Back to the study room", "go_to": "study_room"},
            },
        },
        "library": {
            "title": "Library",
            "texts": [
                {
                    "when": {"flags": {"colleague_choice": "none"}},
                    "text": "Leonor, your teammate, is studying at a table at the back. She was one of the people who received Duarte's messages.",
                },
                {
                    "when": {"flags": {"colleague_choice": "help"}},
                    "text": 'Leonor is saving screenshots of the messages. "I will take care of this. See you in the auditorium."',
                },
                {
                    "when": {"flags": {"colleague_choice": "accused"}},
                    "text": "Leonor's table is empty.",
                },
            ],
            "actions": {
                "ask_for_help": {
                    "label": "Show the photo and quietly ask for help",
                    "offered_if": {"flags": {"colleague_choice": "none"}},
                    "requires": {"has": ["original_photo"]},
                    "blocked_text": 'Leonor shrugs. "Duarte has always been in the group, I have the messages right here. Do you have any proof otherwise?"',
                    "sets": {"colleague_choice": "help"},
                    "result_text": 'Leonor compares the photo with the one in the report and turns pale. "I got all these messages last night, from a number I did not know. And some of them are dated three weeks ago." She promises to keep the original messages and to meet you in the auditorium.',
                },
                "accuse": {
                    "label": "Show the photo and accuse her of helping Duarte",
                    "offered_if": {"flags": {"colleague_choice": "none"}},
                    "requires": {"has": ["original_photo"]},
                    "blocked_text": 'Leonor shrugs. "Duarte has always been in the group, I have the messages right here. Do you have any proof otherwise?"',
                    "sets": {"colleague_choice": "accused"},
                    "result_text": '"You think I would do that to the group?" Leonor stands up, offended. "Then you do not need these messages for anything." She deletes the conversation in front of you and leaves.',
                },
                "go_study_room": {"label": "Back to the study room", "go_to": "study_room"},
            },
        },
        "computer_lab": {
            "title": "Computer lab",
            "texts": [
                {
                    "when": {},
                    "text": "The computer lab is empty. Computer 12 is still on: it is the one the group used to work on the project.",
                },
                {
                    "when": {"flags": {"files_viewed": True}},
                    "text": "You have compared the files: four authors in every copy on the USB stick, and a change in the shared folder yesterday at 11:47 pm.",
                },
            ],
            "actions": {
                "view_files": {
                    "label": "Look at the old project files",
                    "offered_if": {"flags": {"files_viewed": False}},
                    "requires": {"has": ["usb_stick"]},
                    "blocked_text": "The shared folder only shows the current version, already with five names. You need the group's backup copy.",
                    "sets": {"files_viewed": True},
                    "result_text": 'You plug the USB stick into computer 12 and compare. In the backups on the USB stick, every version has four authors. In the shared folder, the current version was changed yesterday at 11:47 pm, from this same computer: someone added "Duarte Sequeira" to the report and swapped the photo. You recover the original version of the work.',
                },
                "open_chat": {
                    "label": "Open the group chat on computer 12",
                    "offered_if": {"flags": {"files_viewed": True}},
                    "go_to": "group_chat",
                },
                "go_study_room": {"label": "Back to the study room", "go_to": "study_room"},
            },
        },
        # The group chat puzzle (specs/spot-the-fake.md). Messages 2, 4 and 5 are fake; 1 and 3 are real.
        "group_chat": {
            "title": "Group chat",
            "texts": [
                {
                    "when": {},
                    "text": "Computer 12 still has the group chat open. Flag the messages you think are fake; a message that arrived late shows when it arrived.",
                },
                {"when": {}, "text": 'Leonor, 3 weeks ago, 9:05 pm: "Can someone book the study room for Thursday?"'},
                {"when": {"flags": {"flagged_1": True}}, "text": "Flagged."},
                {"when": {}, "text": 'Unknown number, 3 weeks ago, 9:07 pm: "Booked it. I wrote the conclusion too, like always."'},
                {"when": {"flags": {"flagged_2": True}}, "text": "Flagged."},
                {"when": {}, "text": 'Rita, 2 weeks ago, 6:40 pm: "Photo for the cover is ready. Four of us, finally!"'},
                {"when": {"flags": {"flagged_3": True}}, "text": "Flagged."},
                {"when": {}, "text": "Duarte, 3 weeks ago, 10:10 pm: \"Can't wait for the five of us to present.\""},
                {"when": {"flags": {"flagged_4": True}}, "text": "Flagged."},
                {"when": {}, "text": 'Tomás, 3 weeks ago, 10:12 pm (arrived yesterday, 11:49 pm): "Duarte did the slides, obviously."'},
                {"when": {"flags": {"flagged_5": True}}, "text": "Flagged."},
            ],
            "actions": {
                "flag_1": {
                    "label": "Flag message 1",
                    "offered_if": {"flags": {"flagged_1": False}},
                    "sets": {"flagged_1": True},
                    "result_text": "You flag message 1 for the professor.",
                },
                "flag_2": {
                    "label": "Flag message 2",
                    "offered_if": {"flags": {"flagged_2": False}},
                    "sets": {"flagged_2": True},
                    "result_text": "You flag message 2 for the professor.",
                },
                "flag_3": {
                    "label": "Flag message 3",
                    "offered_if": {"flags": {"flagged_3": False}},
                    "sets": {"flagged_3": True},
                    "result_text": "You flag message 3 for the professor.",
                },
                "flag_4": {
                    "label": "Flag message 4",
                    "offered_if": {"flags": {"flagged_4": False}},
                    "sets": {"flagged_4": True},
                    "result_text": "You flag message 4 for the professor.",
                },
                "flag_5": {
                    "label": "Flag message 5",
                    "offered_if": {"flags": {"flagged_5": False}},
                    "sets": {"flagged_5": True},
                    "result_text": "You flag message 5 for the professor.",
                },
                "go_computer_lab": {"label": "Back to the computer lab", "go_to": "computer_lab"},
            },
        },
        "auditorium": {
            "title": "Auditorium",
            "texts": [
                {
                    "when": {},
                    "text": "The professor is in the auditorium, closing the list of groups for tomorrow. Duarte is sitting in the front row with a calm smile.",
                },
            ],
            "actions": {
                "present_evidence": {"label": "Present the evidence to the professor", "ends_game": True},
                "go_study_room": {"label": "Back to the study room", "go_to": "study_room"},
            },
        },
    },
    "endings": [
        # The best ending comes first: the first ending whose "when" is true wins.
        {
            "id": "full_case",
            "title": "Case closed",
            "when": {"flags": {
                "colleague_choice": "help",
                "flagged_1": False, "flagged_2": True, "flagged_3": False, "flagged_4": True, "flagged_5": True,
            }},
            "text": "You show the history on the USB stick and the three messages you flagged: one from a number outside the group, one that counts five of you when there were four, and one that arrived last night, two minutes after the shared folder was changed. Leonor walks in with the original messages, and they match. The professor crosses the fifth name off the list and asks Duarte to explain. He has no answer. Tomorrow, the four of you present, with the case closed.",
        },
        {
            "id": "impostor",
            "title": "The impostor",
            "when": {"flags": {"colleague_choice": "help"}},
            "text": "You show the history on the USB stick: four authors until last night. Leonor walks in and hands over the messages she kept: they were all sent on the same night, from a new number, with fake dates. The professor crosses the fifth name off the list. Duarte leaves the auditorium without a word. Tomorrow, the four of you present.",
        },
        {
            "id": "stolen_credits",
            "title": "Stolen credit",
            "when": {},
            "text": 'You show the history on the USB stick: the original work is recovered and had four authors until last night. But Duarte raises his phone: "I have messages from everyone proving I took part." Without the original messages, you cannot prove they are fake. The professor sighs: "Without proof that the messages are fake, the name stays." Tomorrow, the five of you present.',
        },
    ],
}


STORY_PT = {
    "start": {
        "scene": "study_room",
        "inventory": [],
        "flags": {
            "colleague_choice": "none",
            "files_viewed": False,
            # One flag per group chat message: True once the player flags it as fake.
            "flagged_1": False,
            "flagged_2": False,
            "flagged_3": False,
            "flagged_4": False,
            "flagged_5": False,
        },
        "ending": "none",
    },
    "items": {
        "usb_stick": "Pen com o histórico do projeto",
        "original_photo": "Fotografia original impressa",
    },
    "messages": {
        "game_over": "A história terminou. Começa um jogo novo para voltar a jogar.",
        "not_here": "Não podes fazer isso aqui.",
        "not_offered": "Já fizeste isso.",
        "no_game": "Não foi possível encontrar o teu jogo gravado. Escreve o teu nome para recomeçar.",
    },
    "scenes": {
        "study_room": {
            "title": "Sala de estudo",
            "texts": [
                {
                    "when": {},
                    "text": 'É noite, véspera da apresentação. Na pasta do grupo, a fotografia mostra cinco pessoas. Vocês são quatro. Na capa do relatório há um quinto nome: Duarte Sequeira. No chat, os teus colegas garantem que ele "esteve sempre connosco". Só tu sabes que isso é mentira.',
                },
                {
                    "when": {"has": ["usb_stick"]},
                    "text": "A gaveta do grupo está vazia.",
                },
            ],
            "actions": {
                "open_drawer": {
                    "label": "Abrir a gaveta do grupo",
                    "offered_if": {"lacks": ["usb_stick"]},
                    "gives": "usb_stick",
                    "result_text": "Encontras a pen onde o grupo guardava as cópias de segurança do projeto. Guardas a pen.",
                },
                "go_print_shop": {"label": "Ir para a reprografia", "go_to": "print_shop"},
                "go_library": {"label": "Ir para a biblioteca", "go_to": "library"},
                "go_computer_lab": {"label": "Ir para a sala de informática", "go_to": "computer_lab"},
                "go_auditorium": {
                    "label": "Ir para o auditório",
                    "requires": {"flags": {"files_viewed": True}},
                    "blocked_text": "Ainda não tens provas. O professor não te vai ouvir só com uma suspeita.",
                    "go_to": "auditorium",
                },
            },
        },
        "print_shop": {
            "title": "Reprografia",
            "texts": [
                {
                    "when": {},
                    "text": "A reprografia está quase a fechar. A funcionária lembra-se do vosso grupo: imprimiram aqui a fotografia para a capa do relatório na semana passada.",
                },
                {
                    "when": {"has": ["original_photo"]},
                    "text": "A funcionária já te deu a cópia do pedido original.",
                },
            ],
            "actions": {
                "request_copy": {
                    "label": "Pedir uma cópia do pedido original",
                    "offered_if": {"lacks": ["original_photo"]},
                    "gives": "original_photo",
                    "result_text": "A funcionária volta a imprimir o ficheiro que ficou guardado no pedido. Na fotografia original estão quatro pessoas. Guardas a fotografia.",
                },
                "go_study_room": {"label": "Voltar à sala de estudo", "go_to": "study_room"},
            },
        },
        "library": {
            "title": "Biblioteca",
            "texts": [
                {
                    "when": {"flags": {"colleague_choice": "none"}},
                    "text": "A Leonor, a tua colega de grupo, está a estudar numa mesa ao fundo. Foi uma das pessoas que recebeu as mensagens do Duarte.",
                },
                {
                    "when": {"flags": {"colleague_choice": "help"}},
                    "text": 'A Leonor está a guardar capturas de ecrã das mensagens. "Eu trato disto. Vemo-nos no auditório."',
                },
                {
                    "when": {"flags": {"colleague_choice": "accused"}},
                    "text": "A mesa da Leonor está vazia.",
                },
            ],
            "actions": {
                "ask_for_help": {
                    "label": "Mostrar a fotografia e pedir ajuda discretamente",
                    "offered_if": {"flags": {"colleague_choice": "none"}},
                    "requires": {"has": ["original_photo"]},
                    "blocked_text": 'A Leonor encolhe os ombros. "O Duarte esteve sempre no grupo, tenho aqui as mensagens. Tens alguma prova do contrário?"',
                    "sets": {"colleague_choice": "help"},
                    "result_text": 'A Leonor compara a fotografia com a do relatório e fica pálida. "Recebi estas mensagens todas ontem à noite, de um número que não conhecia. E algumas têm datas de há três semanas." Promete guardar as mensagens originais e ir ter contigo ao auditório.',
                },
                "accuse": {
                    "label": "Mostrar a fotografia e acusá-la de ajudar o Duarte",
                    "offered_if": {"flags": {"colleague_choice": "none"}},
                    "requires": {"has": ["original_photo"]},
                    "blocked_text": 'A Leonor encolhe os ombros. "O Duarte esteve sempre no grupo, tenho aqui as mensagens. Tens alguma prova do contrário?"',
                    "sets": {"colleague_choice": "accused"},
                    "result_text": '"Achas que eu fazia isso ao grupo?" A Leonor levanta-se, ofendida. "Então não preciso destas mensagens para nada." Apaga a conversa à tua frente e sai.',
                },
                "go_study_room": {"label": "Voltar à sala de estudo", "go_to": "study_room"},
            },
        },
        "computer_lab": {
            "title": "Sala de informática",
            "texts": [
                {
                    "when": {},
                    "text": "A sala de informática está vazia. O computador 12 ainda está ligado: é o que o grupo usava para trabalhar no projeto.",
                },
                {
                    "when": {"flags": {"files_viewed": True}},
                    "text": "Já comparaste os ficheiros: quatro autores em todas as cópias da pen, e uma alteração na pasta partilhada ontem às 23h47.",
                },
            ],
            "actions": {
                "view_files": {
                    "label": "Consultar os ficheiros antigos do projeto",
                    "offered_if": {"flags": {"files_viewed": False}},
                    "requires": {"has": ["usb_stick"]},
                    "blocked_text": "A pasta partilhada só mostra a versão atual, já com cinco nomes. Precisas da cópia de segurança do grupo.",
                    "sets": {"files_viewed": True},
                    "result_text": 'Ligas a pen ao computador 12 e comparas. Nas cópias de segurança da pen, todas as versões têm quatro autores. Na pasta partilhada, a versão atual foi alterada ontem às 23h47, a partir deste mesmo computador: alguém acrescentou "Duarte Sequeira" ao relatório e trocou a fotografia. Recuperas a versão original do trabalho.',
                },
                "open_chat": {
                    "label": "Abrir o chat do grupo no computador 12",
                    "offered_if": {"flags": {"files_viewed": True}},
                    "go_to": "group_chat",
                },
                "go_study_room": {"label": "Voltar à sala de estudo", "go_to": "study_room"},
            },
        },
        # O puzzle do chat do grupo (specs/spot-the-fake.md). As mensagens 2, 4 e 5 são falsas; a 1 e a 3 são verdadeiras.
        "group_chat": {
            "title": "Chat do grupo",
            "texts": [
                {
                    "when": {},
                    "text": "O computador 12 ainda tem o chat do grupo aberto. Marca as mensagens que achas falsas; uma mensagem que chegou mais tarde mostra quando chegou.",
                },
                {"when": {}, "text": 'Leonor, há 3 semanas, 21h05: "Alguém pode reservar a sala de estudo para quinta-feira?"'},
                {"when": {"flags": {"flagged_1": True}}, "text": "Marcada."},
                {"when": {}, "text": 'Número desconhecido, há 3 semanas, 21h07: "Já reservei. Também escrevi a conclusão, como sempre."'},
                {"when": {"flags": {"flagged_2": True}}, "text": "Marcada."},
                {"when": {}, "text": 'Rita, há 2 semanas, 18h40: "A fotografia para a capa está pronta. Os quatro, finalmente!"'},
                {"when": {"flags": {"flagged_3": True}}, "text": "Marcada."},
                {"when": {}, "text": 'Duarte, há 3 semanas, 22h10: "Mal posso esperar para apresentarmos os cinco."'},
                {"when": {"flags": {"flagged_4": True}}, "text": "Marcada."},
                {"when": {}, "text": 'Tomás, há 3 semanas, 22h12 (chegou ontem às 23h49): "Os slides foram do Duarte, claro."'},
                {"when": {"flags": {"flagged_5": True}}, "text": "Marcada."},
            ],
            "actions": {
                "flag_1": {
                    "label": "Marcar a mensagem 1",
                    "offered_if": {"flags": {"flagged_1": False}},
                    "sets": {"flagged_1": True},
                    "result_text": "Marcas a mensagem 1 para mostrar ao professor.",
                },
                "flag_2": {
                    "label": "Marcar a mensagem 2",
                    "offered_if": {"flags": {"flagged_2": False}},
                    "sets": {"flagged_2": True},
                    "result_text": "Marcas a mensagem 2 para mostrar ao professor.",
                },
                "flag_3": {
                    "label": "Marcar a mensagem 3",
                    "offered_if": {"flags": {"flagged_3": False}},
                    "sets": {"flagged_3": True},
                    "result_text": "Marcas a mensagem 3 para mostrar ao professor.",
                },
                "flag_4": {
                    "label": "Marcar a mensagem 4",
                    "offered_if": {"flags": {"flagged_4": False}},
                    "sets": {"flagged_4": True},
                    "result_text": "Marcas a mensagem 4 para mostrar ao professor.",
                },
                "flag_5": {
                    "label": "Marcar a mensagem 5",
                    "offered_if": {"flags": {"flagged_5": False}},
                    "sets": {"flagged_5": True},
                    "result_text": "Marcas a mensagem 5 para mostrar ao professor.",
                },
                "go_computer_lab": {"label": "Voltar à sala de informática", "go_to": "computer_lab"},
            },
        },
        "auditorium": {
            "title": "Auditório",
            "texts": [
                {
                    "when": {},
                    "text": "O professor está no auditório a fechar a lista de grupos para amanhã. O Duarte está sentado na primeira fila, com um sorriso calmo.",
                },
            ],
            "actions": {
                "present_evidence": {"label": "Apresentar as provas ao professor", "ends_game": True},
                "go_study_room": {"label": "Voltar à sala de estudo", "go_to": "study_room"},
            },
        },
    },
    "endings": [
        # O melhor final vem primeiro: ganha o primeiro final cujo "when" é verdadeiro.
        {
            "id": "full_case",
            "title": "Caso encerrado",
            "when": {"flags": {
                "colleague_choice": "help",
                "flagged_1": False, "flagged_2": True, "flagged_3": False, "flagged_4": True, "flagged_5": True,
            }},
            "text": "Mostras o histórico da pen e as três mensagens que marcaste: uma de um número fora do grupo, uma que fala em cinco quando eram quatro, e uma que chegou ontem à noite, dois minutos depois de a pasta partilhada ser alterada. A Leonor entra com as mensagens originais, e batem certo. O professor risca o quinto nome da lista e pede ao Duarte que se explique. Ele não tem resposta. Amanhã apresentam os quatro, com o caso encerrado.",
        },
        {
            "id": "impostor",
            "title": "O impostor",
            "when": {"flags": {"colleague_choice": "help"}},
            "text": "Mostras o histórico da pen: quatro autores até ontem à noite. A Leonor entra e entrega as mensagens que guardou: foram todas enviadas na mesma noite, de um número novo, com datas falsas. O professor risca o quinto nome da lista. O Duarte sai do auditório sem dizer nada. Amanhã apresentam os quatro.",
        },
        {
            "id": "stolen_credits",
            "title": "Créditos roubados",
            "when": {},
            "text": 'Mostras o histórico da pen: o trabalho original está recuperado e tinha quatro autores até ontem à noite. Mas o Duarte levanta o telemóvel: "Tenho mensagens de todos a provar que participei." Sem as mensagens originais, não consegues provar que são falsas. O professor suspira: "Sem provas de que as mensagens são falsas, o nome fica." Amanhã apresentam os cinco.',
        },
    ],
}


# Sentences of the screens (not part of the story). Proposals, to be approved by the team.
UI_EN = {
    "title": "The Fifth Element",
    "premise": "On the eve of the presentation, a fifth person appears in the photo of your group of four. Their name is in the report, and all your teammates received messages that seem to prove they were always part of the team. Only you know that something is wrong.",
    "language_label": "Language",
    "continue_hint": "To continue a saved game, type the same name you used before.",
    "name_label": "Your name",
    "play": "Play",
    "started": "A new game has started. Good luck!",
    "continued": "Welcome back. Your saved game continues where you left it.",
    "invalid_name": "Use 1 to 20 characters: letters, digits, spaces, - or _.",
    "no_game": "Your saved game could not be found. Type your name to start again.",
    "inventory": "Inventory",
    "inventory_empty": "You are not carrying anything yet.",
    "new_game": "New game",
    "confirm_question": "Start a new game? Your current progress will be lost.",
    "confirm_yes": "Yes, start again",
    "confirm_cancel": "Cancel",
    "the_end": "The end",
}

UI_PT = {
    "title": "O quinto elemento",
    "premise": "Na véspera da apresentação, aparece uma quinta pessoa na fotografia do teu grupo de quatro. O nome dela está no relatório e todos os colegas receberam mensagens que parecem provar que sempre participou. Só tu sabes que há alguma coisa errada.",
    "language_label": "Língua",
    "continue_hint": "Para continuar um jogo gravado, escreve o mesmo nome que usaste antes.",
    "name_label": "O teu nome",
    "play": "Jogar",
    "started": "Começou um jogo novo. Boa sorte!",
    "continued": "Olá outra vez. O teu jogo continua onde o deixaste.",
    "invalid_name": "Usa 1 a 20 caracteres: letras, algarismos, espaços, - ou _.",
    "no_game": "Não foi possível encontrar o teu jogo gravado. Escreve o teu nome para recomeçar.",
    "inventory": "Inventário",
    "inventory_empty": "Ainda não tens nada contigo.",
    "new_game": "Jogo novo",
    "confirm_question": "Começar um jogo novo? Perdes o progresso atual.",
    "confirm_yes": "Sim, recomeçar",
    "confirm_cancel": "Cancelar",
    "the_end": "Fim",
}


STORIES = {"en": STORY_EN, "pt": STORY_PT}
UI_TEXTS = {"en": UI_EN, "pt": UI_PT}
