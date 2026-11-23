"""The case file of the 3D game: evidence cards, confrontations and the hearing. Data only.

SERVER ONLY (specs/evidence-and-hearing.md, point 3): this file is read by campus_evidence.py and is
never put in the page (page3d.py does not import it), so looking at the page cannot tell which card
breaks which claim. The page receives a card only when the player holds it, and a line only when the
player has earned it. The rules that read these tables are in campus_evidence.py. At the end, the
secret texts of earlier nights (specs/earlier-nights.md): the unknown number's whispers and the true
ending, read by campus_memory.py.

The same keys exist in "en" and "pt"; only the texts differ.
"""

# The cards the save can give, in the order the hand shows them, and the story condition that holds
# each one (checked with logic._condition_met). The flagged chat messages were cards too, until
# specs/computer-lab-backup.md removed the chat.
# The proofs for the professor (specs/computer-lab-backup.md): the USB stick's history, the photo and
# the backup of the conversations. The security camera is the fourth, added by specs/security-desk.md.
EVIDENCE = {
    "original_photo": {"has": ["original_photo"]},
    "files": {"flags": {"files_viewed": True}},
    "backup": {"flags": {"backup_saved": True}},
}

# The facts won by cracking a person: kept in the night's notes. They are no longer cards for the
# hearing (specs/computer-lab-backup.md); the true ending still needs both (specs/earlier-nights.md).
FACTS = {"tomas": "tomas_word", "rita": "rita_word"}

# Who can be cracked: their claim line and the cards that break it (point 7).
CONFRONT = {
    "tomas": {"node": "slides", "breaks": ["files"]},   # the history shows who made the slides
    "rita": {"node": "five", "breaks": ["files", "original_photo"]},
}

# Duarte's three claims at the hearing, in order (point 10). `accepts` are the cards that break the
# claim. `wrong` names the professor's line (in CASE_TEXT[language]["wrong"]) for a wrong card that has
# a line of its own; every other wrong card gets the general wrong line of that claim (its id).
HEARING = [
    {"id": "name", "accepts": ["files"], "wrong": {}},
    {"id": "photo", "accepts": ["original_photo"], "wrong": {"files": "photo_files"}},
    {"id": "messages", "accepts": ["backup"], "wrong": {}},   # specs/computer-lab-backup.md
]

CASE_TEXT = {
    "en": {
        # The labels of the cards.
        "labels": {
            "original_photo": "The original photo, taped back together: four people",
            "files": "The file history: four authors in every backup",
            "backup": "The backup of the original conversations: four people, not one message from Duarte",
        },
        # The right card on the claim line. `trust` is the person's trust after it (None: Rita has no trust level).
        "reveals": {
            "tomas": {"text": "Tomás reads the history of the slides: every version saved under his name, the last one on Tuesday at two in the morning. \"So the message says Duarte did them. The files say I did.\" His voice drops. \"I never sent that message. And the slides... I made the slides. All eleven. I was here until two on Tuesday.\" He turns his chair to face the glass wall. \"He walks the corridor, you know. Go back to the computer. If he comes, I will be standing in the door.\"",
                      "note": "Tomás never wrote the message about the slides: he made them himself and will say so. He is watching the corridor for you.",
                      "trust": 3},
            "rita": {"text": "Rita looks from your proof to her screen and back. \"So the photo did change.\" She laughs once, without any joy. \"I counted four. I said it out loud. I even wrote it in the chat: four of us, finally. That one is mine, I remember typing it.\" She closes the laptop. \"Tell the professor I counted. I will say it to his face.\"",
                     "note": "Rita counted four people on the day of the photo. The chat message that says four of them is hers. She will tell the professor.",
                     "trust": None},
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
            "photo": {"original_photo": "The professor holds the taped photo next to the cover. \"The print shop's own print, with its date stamp. Four people, before anyone added a fifth.\""},
            "messages": {"backup": "The professor scrolls through the backup. \"The group's own conversations, as they were before last night: four people, and not one message from him. A date can be typed. A backup of weeks cannot.\""},
        },
        "wrong": {
            "name": "\"That does not tell me who wrote a report.\" He makes a small mark on the list.",
            "photo": "\"That tells me nothing about who is in a photograph.\" He makes a mark on the list.",
            "messages": "\"That does not tell me who sent a message.\" He makes a mark on the list.",
            "photo_files": "\"The history says a photo was swapped. It does not show me the one that was there before.\"",
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
        },
    },
    "pt": {
        "labels": {
            "original_photo": "A fotografia original, colada com fita-cola: quatro pessoas",
            "files": "O histórico dos ficheiros: quatro autores em todas as cópias",
            "backup": "O backup das conversas originais: quatro pessoas, nem uma mensagem do Duarte",
        },
        "reveals": {
            "tomas": {"text": "O Tomás lê o histórico dos slides: todas as versões guardadas com o nome dele, a última na terça-feira às duas da manhã. \"Então a mensagem diz que foi o Duarte. Os ficheiros dizem que fui eu.\" Baixa a voz. \"Eu nunca enviei aquela mensagem. E os slides... fui eu que fiz os slides. Os onze. Fiquei aqui até às duas na terça-feira.\" Roda a cadeira para a parede de vidro. \"Ele anda pelo corredor, sabes. Volta para o computador. Se ele vier, eu fico à porta.\"",
                      "note": "O Tomás nunca escreveu a mensagem sobre os slides: foi ele que os fez e vai dizê-lo. Fica a vigiar o corredor por ti.",
                      "trust": 3},
            "rita": {"text": "A Rita olha da tua prova para o ecrã e outra vez para a prova. \"Então a fotografia mudou mesmo.\" Ri-se uma vez, sem alegria nenhuma. \"Eu contei quatro. Disse-o em voz alta. Até o escrevi no chat: os quatro, finalmente. Essa é minha, lembro-me de a escrever.\" Fecha o portátil. \"Diz ao professor que eu contei. Eu digo-lho na cara.\"",
                     "note": "A Rita contou quatro pessoas no dia da fotografia. A mensagem do chat que fala nos quatro é dela. Vai dizê-lo ao professor.",
                     "trust": None},
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
            "photo": {"original_photo": "O professor põe a fotografia colada ao lado da capa. \"A impressão da própria reprografia, com o carimbo da data. Quatro pessoas, antes de alguém acrescentar um quinto.\""},
            "messages": {"backup": "O professor percorre o backup. \"As conversas do próprio grupo, tal como estavam antes de ontem à noite: quatro pessoas, e nem uma mensagem dele. Uma data escreve-se. Um backup de semanas, não.\""},
        },
        "wrong": {
            "name": "\"Isso não me diz quem escreveu um relatório.\" Faz um pequeno sinal na lista.",
            "photo": "\"Isso não me diz nada sobre quem está numa fotografia.\" Faz um sinal na lista.",
            "messages": "\"Isso não me diz quem enviou uma mensagem.\" Faz um sinal na lista.",
            "photo_files": "\"O histórico diz que uma fotografia foi trocada. Não me mostra a que lá estava antes.\"",
        },
        "concede": "O professor espera. O Duarte sorri. \"Nada?\"",
        "caught": "\"Antes de começarmos: o senhor Sequeira diz-me que você esteve esta noite a ler as mensagens do grupo às escondidas.\" O professor faz um sinal ao lado do teu nome.",
        "verdicts": {
            "three": "\"Três vezes esta noite me deu razões para duvidar de si. Não risco um nome por um palpite.\"",
            "three_help": "O professor fecha a lista antes de a Leonor chegar à porta. \"Já ouvi palpites que cheguem por uma noite.\"",
            "two": "\"Acho que tem razão sobre ele. Mas fez-me duvidar duas vezes esta noite, e eu só escrevo aquilo de que tenho a certeza.\"",
        },
    },
}


# ---------- earlier nights (specs/earlier-nights.md) ----------
# Read by campus_memory.py, the server only, like everything above: the page gets one of these texts
# only on the night that earned it (points 4 and 9).

# The id of the true ending, a campus layer over a saved full_case (point 8). It is never in the page.
TRUE_ENDING = "night_over"

# The unknown number on earlier nights (point 4): the message as a night starts, the dare that takes
# its place once every story ending was seen, and the round warning from night 3 on. Then the
# true ending (point 8): its `voices` say who speaks each of the four spoken quotes of `text`, in order.
NIGHT_TEXT = {
    "en": {
        # The message of night 2, night 3, night 4, and then of night 5 and every later night.
        "whispers": ["You again?",
                     "You again. Same coat, same scarf.",
                     "I have stopped counting the nights. You have not.",
                     "Look at the photo on your case file. Then tell me which of us is the fifth."],
        "dare": "Three endings, and still here. You will never get all three of them to stand with you. Not in thirty minutes.",
        "round": "Close the computer. He is walking.",
        "ending": {
            "title": "22:46", "stamp": "THE NIGHT IS OVER", "emoji": "🌅",
            "voices": ["rita", "duarte", "duarte", "professor"],
            "text": "You do not wait for Duarte to finish his sentences; you have heard them before. Three claims, three answers, each one on the table before he stops speaking, and the professor never once looks away from you. Then the door opens and nobody is alone any more. Leonor comes in with her phone, Tomás with his slides, Rita counting under her breath. \"Four. I counted.\" Duarte looks at the four of you standing together, and for the first time his smile has nowhere to go. \"You again.\" It is not a question. \"I only ever needed one of you to doubt the other three.\" He pushes back his hood. There is no stranger under it: only a hat, a scarf and a long coat, and they are yours. The professor crosses out the fifth name. When you look back at the front row the seat is empty; on it lies a phone with every message you ever received from the unknown number, written and never sent. Your own phone buzzes one last time. The sender is no longer unknown: the name on the screen is your own. The clock on the wall reads 22:46. Nobody has switched off the lights. \"Tomorrow, the four of you present.\" In the photo on the cover there are four people, and you know every one of them.",
        },
    },
    "pt": {
        "whispers": ["Outra vez tu?",
                     "Outra vez tu. O mesmo casaco, o mesmo cachecol.",
                     "Eu já deixei de contar as noites. Tu não.",
                     "Olha para a fotografia do teu caso. Depois diz-me qual de nós é o quinto."],
        "dare": "Três finais, e continuas aqui. Nunca vais conseguir que os três fiquem do teu lado. Não em trinta minutos.",
        "round": "Fecha o computador. Ele vem aí.",
        "ending": {
            "title": "22:46", "stamp": "A NOITE ACABOU", "emoji": "🌅",
            "voices": ["rita", "duarte", "duarte", "professor"],
            "text": "Não esperas que o Duarte acabe as frases; já as ouviste antes. Três afirmações, três respostas, cada uma em cima da mesa antes de ele se calar, e o professor não tira os olhos de ti uma única vez. Depois a porta abre-se e já ninguém está sozinho. A Leonor entra com o telemóvel, o Tomás com os slides, a Rita a contar baixinho. «Quatro. Eu contei.» O Duarte olha para os quatro, juntos, e pela primeira vez o sorriso dele não tem para onde ir. «Outra vez tu.» Não é uma pergunta. «Só precisava que um de vocês duvidasse dos outros três.» Puxa o capuz para trás. Por baixo não há nenhum desconhecido: só um chapéu, um cachecol e um casaco comprido, e são os teus. O professor risca o quinto nome. Quando voltas a olhar para a primeira fila, a cadeira está vazia; em cima dela ficou um telemóvel com todas as mensagens que recebeste do número desconhecido, escritas e nunca enviadas. O teu telemóvel vibra uma última vez. O remetente já não é desconhecido: o nome no ecrã é o teu. O relógio da parede marca 22:46. Ninguém apagou as luzes. «Amanhã apresentam os quatro.» Na fotografia da capa estão quatro pessoas, e tu conheces todas.",
        },
    },
}


# ---------- the cases (specs/case-of-the-day.md) ----------
# The date picks one of these cases (campus_clock.case_of_day); a saved game keeps its own. Server only.
# - `accepts`: more cards that break a claim of the hearing, by claim id; `right`: the professor's
#   line for each of those new pairs.
# - `texts`: {exact classic text: what this case says instead}, in each language (campus_evidence.retell).
# Only the classic case is left (specs/computer-lab-backup.md): the culprit is always Duarte. The cases
# "tomas" and "rita" of specs/culprit-of-the-night.md changed the fake chat messages, and the chat is gone.
CASES = {
    "outsider": {"accepts": {}, "right": {"en": {}, "pt": {}}, "texts": {"en": {}, "pt": {}}},
}
