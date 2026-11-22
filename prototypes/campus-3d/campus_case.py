"""The case file of the 3D game: evidence cards, confrontations and the hearing. Data only.

SERVER ONLY (specs/evidence-and-hearing.md, point 3): this file is read by campus_evidence.py and is
never put in the page (page3d.py does not import it), so looking at the page cannot tell which card
breaks which claim. The page receives a card only when the player holds it, and a line only when the
player has earned it. The rules that read these tables are in campus_evidence.py.

The same keys exist in "en" and "pt"; only the texts differ.
"""

# The cards the save can give, in the order the hand shows them, and the story condition that holds
# each one (checked with logic._condition_met). The label of a flagged chat message is not here: it is
# the story's own text of that message (campus_evidence.card_label).
EVIDENCE = {
    "original_photo": {"has": ["original_photo"]},
    "files": {"flags": {"files_viewed": True}},
    "leonor_messages": {"flags": {"colleague_choice": "help"}},
    "msg_1": {"flags": {"flagged_1": True}},
    "msg_2": {"flags": {"flagged_2": True}},
    "msg_3": {"flags": {"flagged_3": True}},
    "msg_4": {"flags": {"flagged_4": True}},
    "msg_5": {"flags": {"flagged_5": True}},
}

# The facts won by cracking a person: held through the night's notes, not through the save.
FACTS = {"tomas": "tomas_word", "rita": "rita_word"}

# Who can be cracked: their claim line and the cards that break it (point 7).
CONFRONT = {
    "tomas": {"node": "slides", "breaks": ["msg_5"]},
    "rita": {"node": "five", "breaks": ["files", "original_photo"]},
    "leonor": {"node": "sure", "breaks": ["tomas_word"]},
}

# Duarte's three claims at the hearing, in order (point 10). `accepts` are the cards that break the
# claim. `wrong` names the professor's line (in CASE_TEXT[language]["wrong"]) for a wrong card that has
# a line of its own; every other wrong card gets the general wrong line of that claim (its id).
HEARING = [
    {"id": "name", "accepts": ["files"], "wrong": {}},
    {"id": "photo", "accepts": ["original_photo", "rita_word"], "wrong": {"files": "photo_files"}},
    {"id": "messages", "accepts": ["leonor_messages", "tomas_word"],
     "wrong": {"msg_1": "messages_flag", "msg_2": "messages_flag", "msg_3": "messages_flag",
               "msg_4": "messages_flag", "msg_5": "messages_flag"}},
]

CASE_TEXT = {
    "en": {
        # The labels of the cards (the flagged messages use the story's own text instead).
        "labels": {
            "original_photo": "The original photo, taped back together: four people",
            "files": "The file history: four authors in every backup",
            "leonor_messages": "Leonor's screenshots: every message arrived last night",
            "tomas_word": "Tomás's word: he never wrote that message and made the slides himself",
            "rita_word": "Rita's word: she counted four people on the day of the photo",
        },
        # The right card on the claim line. `trust` is the person's trust after it (None: Rita has no trust level).
        "reveals": {
            "tomas": {"text": "Tomás reads the line under his name, then the small grey line beneath it. \"Arrived yesterday, 11:49 pm. At 11:49 I was sitting right here, one computer away from the one in the hood. I did not type a word.\" His voice drops. \"I never sent that. And the slides... I made the slides. All eleven. I was here until two on Tuesday.\" He turns his chair to face the glass wall. \"He walks the corridor, you know. Go back to the computer. If he comes, I will be standing in the door.\"",
                      "note": "Tomás never wrote the message about the slides: he made them himself and will say so. He is watching the corridor for you.",
                      "trust": 3},
            "rita": {"text": "Rita looks from your proof to her screen and back. \"So the photo did change.\" She laughs once, without any joy. \"I counted four. I said it out loud. I even wrote it in the chat: four of us, finally. That one is mine, I remember typing it.\" She closes the laptop. \"Tell the professor I counted. I will say it to his face.\"",
                     "note": "Rita counted four people on the day of the photo. The chat message that says four of them is hers. She will tell the professor.",
                     "trust": None},
            "leonor": {"text": "You tell her what Tomás said about the message with his name. Leonor stops with her thumb on the screen. \"He never wrote it?\" She scrolls back, slower this time. \"Then I do not know what I have been reading.\"",
                       "note": "Leonor did not know that Tomás never wrote the message with his name. It shook her.",
                       "trust": 3},
        },
        # Any other card, or any other line: one line per person. Duarte has one line for any card.
        "rebuffs": {
            "tomas": "Tomás glances at it and back at his screen. \"And what does that have to do with what I just said?\"",
            "rita": "Rita looks at it, then back at her laptop. \"And? I do not see what that changes.\"",
            "leonor": "Leonor looks at what you are holding, then at you. \"If you want to show me something, say what you want from me.\"",
            "amelia": "The clerk looks over her glasses. \"I print things. I do not judge them. Is there anything you need printed?\"",
            "professor": "The professor does not take it. \"Not like this. Present your evidence properly, when you are ready.\"",
            "duarte": "Duarte does not look at it. \"Keep it for the professor. I will be sitting in the front row.\"",
        },
        # The hearing: Duarte's claims, then the professor's line for each card.
        "claims": {
            "name": "Duarte stands up without hurry. \"Professor, open the report. My name is on the cover. It has been there since the first draft.\"",
            "photo": "\"Then look at the photograph. Five people, and I am the one on the right, in the long coat. A camera does not add anyone.\"",
            "messages": "Duarte raises his phone. \"And the messages? Weeks of them. Tomás wrote it himself: 'Duarte did the slides, obviously.' Is Tomás a liar too?\"",
        },
        "right": {
            "name": {"files": "\"Four authors in every backup, and a fifth name added last night at 11:47 pm. Go on.\""},
            "photo": {"original_photo": "The professor holds the taped photo next to the cover. \"The print shop's own print, with its date stamp. Four people, before anyone added a fifth.\"",
                      "rita_word": "\"A witness who counted. I will hear her tomorrow; tonight I believe her.\""},
            "messages": {"leonor_messages": "\"Every one delivered on the same night, from a number nobody knew. A date can be typed. An arrival time cannot.\"",
                         "tomas_word": "\"Then the person whose name is on it never sent it. That answers this one.\""},
        },
        "wrong": {
            "name": "\"That does not tell me who wrote a report.\" He makes a small mark on the list.",
            "photo": "\"That tells me nothing about who is in a photograph.\" He makes a mark on the list.",
            "messages": "\"That does not tell me who sent a message.\" He makes a mark on the list.",
            "photo_files": "\"The history says a photo was swapped. It does not show me the one that was there before.\"",
            "messages_flag": "\"You flagged it. That is your opinion of it. Who will stand here and tell me they never wrote it?\"",
        },
        # Duarte's line when the player says nothing, on any claim.
        "concede": "The professor waits. Duarte smiles. \"Nothing?\"",
        # The professor's first line when the player was caught at computer 12 (specs/night-schedule.md, point 8).
        "caught": "\"Before we begin: Mr Sequeira tells me you were reading the group's messages in secret tonight.\" The professor makes a mark beside your name.",
        # The professor's line above the ending text (point 11).
        "verdicts": {
            "three": "\"Three times tonight you gave me a reason to doubt you. I cannot cross out a name on a guess.\"",
            "three_help": "The professor closes the list before Leonor reaches the door. \"I have heard enough guesses for one night.\"",
            "two": "\"You are right about him, I think. But you made me doubt you twice tonight, and I write down only what I am sure of.\"",
            "no_originals": "The professor looks at Duarte's phone for a long moment. \"One message is answered. He has a phone full of them, and nobody here kept the originals.\"",
        },
    },
    "pt": {
        "labels": {
            "original_photo": "A fotografia original, colada com fita-cola: quatro pessoas",
            "files": "O histórico dos ficheiros: quatro autores em todas as cópias",
            "leonor_messages": "As capturas de ecrã da Leonor: chegaram todas ontem à noite",
            "tomas_word": "A palavra do Tomás: nunca escreveu aquela mensagem e foi ele que fez os slides",
            "rita_word": "A palavra da Rita: contou quatro pessoas no dia da fotografia",
        },
        "reveals": {
            "tomas": {"text": "O Tomás lê a linha por baixo do nome dele e depois a linha cinzenta mais pequena. \"Chegou ontem às 23h49. Às 23h49 eu estava aqui sentado, no computador ao lado do rapaz de capuz. Não escrevi uma palavra.\" Baixa a voz. \"Eu nunca enviei isto. E os slides... fui eu que fiz os slides. Os onze. Fiquei aqui até às duas na terça-feira.\" Roda a cadeira para a parede de vidro. \"Ele anda pelo corredor, sabes. Volta para o computador. Se ele vier, eu fico à porta.\"",
                      "note": "O Tomás nunca escreveu a mensagem sobre os slides: foi ele que os fez e vai dizê-lo. Fica a vigiar o corredor por ti.",
                      "trust": 3},
            "rita": {"text": "A Rita olha da tua prova para o ecrã e outra vez para a prova. \"Então a fotografia mudou mesmo.\" Ri-se uma vez, sem alegria nenhuma. \"Eu contei quatro. Disse-o em voz alta. Até o escrevi no chat: os quatro, finalmente. Essa é minha, lembro-me de a escrever.\" Fecha o portátil. \"Diz ao professor que eu contei. Eu digo-lho na cara.\"",
                     "note": "A Rita contou quatro pessoas no dia da fotografia. A mensagem do chat que fala nos quatro é dela. Vai dizê-lo ao professor.",
                     "trust": None},
            "leonor": {"text": "Contas-lhe o que o Tomás disse sobre a mensagem com o nome dele. A Leonor fica com o polegar parado no ecrã. \"Ele nunca a escreveu?\" Volta atrás na conversa, mais devagar. \"Então já não sei o que é que andei a ler.\"",
                       "note": "A Leonor não sabia que o Tomás nunca escreveu a mensagem com o nome dele. Ficou abalada.",
                       "trust": 3},
        },
        "rebuffs": {
            "tomas": "O Tomás olha de relance e volta ao ecrã. \"E o que é que isso tem a ver com o que eu acabei de dizer?\"",
            "rita": "A Rita olha para aquilo e volta ao portátil. \"E então? Não vejo o que é que isso muda.\"",
            "leonor": "A Leonor olha para o que tens na mão e depois para ti. \"Se me queres mostrar alguma coisa, diz o que queres de mim.\"",
            "amelia": "A funcionária olha por cima dos óculos. \"Eu imprimo coisas. Não as julgo. Precisas de alguma coisa impressa?\"",
            "professor": "O professor não lhe pega. \"Assim não. Apresente as provas como deve ser, quando estiver pronto.\"",
            "duarte": "O Duarte nem olha. \"Guarda isso para o professor. Eu vou estar na primeira fila.\"",
        },
        "claims": {
            "name": "O Duarte levanta-se sem pressa. \"Professor, abra o relatório. O meu nome está na capa. Está lá desde o primeiro rascunho.\"",
            "photo": "\"Então olhe para a fotografia. Cinco pessoas, e eu sou o da direita, de casaco comprido. Uma máquina fotográfica não acrescenta ninguém.\"",
            "messages": "O Duarte levanta o telemóvel. \"E as mensagens? Semanas delas. O próprio Tomás escreveu: 'Os slides foram do Duarte, claro.' O Tomás também é mentiroso?\"",
        },
        "right": {
            "name": {"files": "\"Quatro autores em todas as cópias, e um quinto nome acrescentado ontem às 23h47. Continue.\""},
            "photo": {"original_photo": "O professor põe a fotografia colada ao lado da capa. \"A impressão da própria reprografia, com o carimbo da data. Quatro pessoas, antes de alguém acrescentar um quinto.\"",
                      "rita_word": "\"Uma testemunha que contou. Ouço-a amanhã; esta noite, acredito nela.\""},
            "messages": {"leonor_messages": "\"Todas entregues na mesma noite, de um número que ninguém conhecia. Uma data escreve-se. A hora de chegada, não.\"",
                         "tomas_word": "\"Então quem a assina nunca a enviou. Essa fica respondida.\""},
        },
        "wrong": {
            "name": "\"Isso não me diz quem escreveu um relatório.\" Faz um pequeno sinal na lista.",
            "photo": "\"Isso não me diz nada sobre quem está numa fotografia.\" Faz um sinal na lista.",
            "messages": "\"Isso não me diz quem enviou uma mensagem.\" Faz um sinal na lista.",
            "photo_files": "\"O histórico diz que uma fotografia foi trocada. Não me mostra a que lá estava antes.\"",
            "messages_flag": "\"Marcou-a. Essa é a sua opinião sobre ela. Quem me vem aqui dizer que nunca a escreveu?\"",
        },
        "concede": "O professor espera. O Duarte sorri. \"Nada?\"",
        "caught": "\"Antes de começarmos: o senhor Sequeira diz-me que você esteve esta noite a ler as mensagens do grupo às escondidas.\" O professor faz um sinal ao lado do teu nome.",
        "verdicts": {
            "three": "\"Três vezes esta noite me deu razões para duvidar de si. Não risco um nome por um palpite.\"",
            "three_help": "O professor fecha a lista antes de a Leonor chegar à porta. \"Já ouvi palpites que cheguem por uma noite.\"",
            "two": "\"Acho que tem razão sobre ele. Mas fez-me duvidar duas vezes esta noite, e eu só escrevo aquilo de que tenho a certeza.\"",
            "no_originals": "O professor fica muito tempo a olhar para o telemóvel do Duarte. \"Uma mensagem está respondida. Ele tem um telemóvel cheio delas, e ninguém aqui guardou as originais.\"",
        },
    },
}
