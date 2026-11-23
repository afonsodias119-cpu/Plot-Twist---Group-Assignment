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
            # True once the backup of the original group conversations is saved (specs/computer-lab-backup.md).
            "backup_saved": False,
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
                    "text": 'It is night, the eve of the presentation. In the group folder, the photo shows five people. There are four of you. On the cover of the report there is a fifth name: Duarte. In the chat, your teammates insist that he "was with us all along". Only you know that is a lie.',
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
                {
                    "when": {"flags": {"backup_saved": True}},
                    "text": "The backup of the original group conversations is saved on the USB stick, next to the project history.",
                },
            ],
            "actions": {
                "view_files": {
                    "label": "Look at the old project files",
                    "offered_if": {"flags": {"files_viewed": False}},
                    "requires": {"has": ["usb_stick"]},
                    "blocked_text": "The shared folder only shows the current version, already with five names. You need the group's backup copy.",
                    "sets": {"files_viewed": True},
                    "result_text": 'You plug the USB stick into computer 12 and compare. In the backups on the USB stick, every version has four authors. In the shared folder, the current version was changed yesterday at 11:47 pm, from this same computer: someone added "Duarte" to the report and swapped the photo. You recover the original version of the work.',
                },
                # The original conversations, saved for the professor (specs/computer-lab-backup.md).
                "save_backup": {
                    "label": "Save a backup of the original conversations",
                    "offered_if": {"flags": {"files_viewed": True, "backup_saved": False}},
                    "sets": {"backup_saved": True},
                    "result_text": "Computer 12 still has the group's account open. You copy the whole history of the group's conversations onto the USB stick, as it was before last night: four people, and not one message from Duarte. Now the professor can see the original conversations.",
                },
                "go_study_room": {"label": "Back to the study room", "go_to": "study_room"},
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
        # Two endings (specs/three-proofs.md): every proof for the professor, or a proof missing.
        # The first ending whose "when" is true wins.
        {
            "id": "full_case",
            "title": "Case closed",
            "when": {"has": ["original_photo"], "flags": {"files_viewed": True, "backup_saved": True}},
            "text": "You put your proofs on the professor's desk: the history on the USB stick, four authors until last night; the original photo from the print shop, four people; and the backup of the group's conversations, without a single message from Duarte. The professor looks from one to the other, then at Duarte. He has no answer. The professor crosses the fifth name off the list. Tomorrow, the four of you present, with the case closed.",
        },
        {
            "id": "stolen_credits",
            "title": "Stolen credit",
            "when": {},
            "text": 'You do not have every proof the professor needs. Duarte raises his phone: "I have messages from everyone proving I took part." For each claim of his you cannot answer, the professor makes a mark on the list. Then he sighs: "I cannot cross out a name on a hunch." Tomorrow, the five of you present.',
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
            # True once the backup of the original group conversations is saved (specs/computer-lab-backup.md).
            "backup_saved": False,
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
                    "text": 'É noite, véspera da apresentação. Na pasta do grupo, a fotografia mostra cinco pessoas, no entanto vocês são quatro. Na capa do relatório há um quinto nome: Duarte. No chat, os teus colegas garantem que ele "esteve sempre connosco". Só tu sabes que isso é mentira.',
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
                {
                    "when": {"flags": {"backup_saved": True}},
                    "text": "O backup das conversas originais do grupo está guardado na pen, ao lado do histórico do projeto.",
                },
            ],
            "actions": {
                "view_files": {
                    "label": "Consultar os ficheiros antigos do projeto",
                    "offered_if": {"flags": {"files_viewed": False}},
                    "requires": {"has": ["usb_stick"]},
                    "blocked_text": "A pasta partilhada só mostra a versão atual, já com cinco nomes. Precisas da cópia de segurança do grupo.",
                    "sets": {"files_viewed": True},
                    "result_text": 'Ligas a pen ao computador 12 e comparas. Nas cópias de segurança da pen, todas as versões têm quatro autores. Na pasta partilhada, a versão atual foi alterada ontem às 23h47, a partir deste mesmo computador: alguém acrescentou "Duarte" ao relatório e trocou a fotografia. Recuperas a versão original do trabalho.',
                },
                # As conversas originais, guardadas para o professor (specs/computer-lab-backup.md).
                "save_backup": {
                    "label": "Guardar o backup das conversas originais",
                    "offered_if": {"flags": {"files_viewed": True, "backup_saved": False}},
                    "sets": {"backup_saved": True},
                    "result_text": "O computador 12 ainda tem a conta do grupo aberta. Copias todo o histórico das conversas do grupo para a pen, tal como estava antes de ontem à noite: quatro pessoas, e nem uma mensagem do Duarte. Agora o professor pode ver as conversas originais.",
                },
                "go_study_room": {"label": "Voltar à sala de estudo", "go_to": "study_room"},
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
        # Dois finais (specs/three-proofs.md): todas as provas para o professor, ou uma prova a faltar.
        # Ganha o primeiro final cujo "when" é verdadeiro.
        {
            "id": "full_case",
            "title": "Caso encerrado",
            "when": {"has": ["original_photo"], "flags": {"files_viewed": True, "backup_saved": True}},
            "text": "Pões as tuas provas na mesa do professor: o histórico da pen, quatro autores até ontem à noite; a fotografia original da reprografia, quatro pessoas; e o backup das conversas do grupo, sem uma única mensagem do Duarte. O professor olha de uma para a outra, e depois para o Duarte. Ele não tem resposta. O professor risca o quinto nome da lista. Amanhã, apresentam os quatro, com o caso encerrado.",
        },
        {
            "id": "stolen_credits",
            "title": "Créditos roubados",
            "when": {},
            "text": 'Não tens todas as provas de que o professor precisa. O Duarte levanta o telemóvel: "Tenho mensagens de todos a provar que participei." Por cada afirmação dele a que não consegues responder, o professor faz um sinal na lista. Depois suspira: "Não risco um nome por um palpite." Amanhã, apresentam os cinco.',
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
