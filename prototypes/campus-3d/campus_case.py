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


# ---------- earlier nights (specs/earlier-nights.md) ----------
# Read by campus_memory.py, the server only, like everything above: the page gets one of these texts
# only on the night that earned it (points 4 and 9).

# The id of the true ending, a campus layer over a saved full_case (point 8). It is never in the page.
TRUE_ENDING = "night_over"

# The unknown number on earlier nights (point 4): the message as a night starts, the dare that takes
# its place once the four story endings were seen, and the round warning from night 3 on. Then the
# true ending (point 8): its `voices` say who speaks each of the four spoken quotes of `text`, in order.
NIGHT_TEXT = {
    "en": {
        # The message of night 2, night 3, night 4, and then of night 5 and every later night.
        "whispers": ["You again?",
                     "You again. Same coat, same scarf.",
                     "I have stopped counting the nights. You have not.",
                     "Look at the photo on your case file. Then tell me which of us is the fifth."],
        "dare": "Four endings, and still here. You will never get all three of them to stand with you. Not in thirty minutes.",
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
        "dare": "Quatro finais, e continuas aqui. Nunca vais conseguir que os três fiquem do teu lado. Não em trinta minutos.",
        "round": "Fecha o computador. Ele vem aí.",
        "ending": {
            "title": "22:46", "stamp": "A NOITE ACABOU", "emoji": "🌅",
            "voices": ["rita", "duarte", "duarte", "professor"],
            "text": "Não esperas que o Duarte acabe as frases; já as ouviste antes. Três afirmações, três respostas, cada uma em cima da mesa antes de ele se calar, e o professor não tira os olhos de ti uma única vez. Depois a porta abre-se e já ninguém está sozinho. A Leonor entra com o telemóvel, o Tomás com os slides, a Rita a contar baixinho. «Quatro. Eu contei.» O Duarte olha para os quatro, juntos, e pela primeira vez o sorriso dele não tem para onde ir. «Outra vez tu.» Não é uma pergunta. «Só precisava que um de vocês duvidasse dos outros três.» Puxa o capuz para trás. Por baixo não há nenhum desconhecido: só um chapéu, um cachecol e um casaco comprido, e são os teus. O professor risca o quinto nome. Quando voltas a olhar para a primeira fila, a cadeira está vazia; em cima dela ficou um telemóvel com todas as mensagens que recebeste do número desconhecido, escritas e nunca enviadas. O teu telemóvel vibra uma última vez. O remetente já não é desconhecido: o nome no ecrã é o teu. O relógio da parede marca 22:46. Ninguém apagou as luzes. «Amanhã apresentam os quatro.» Na fotografia da capa estão quatro pessoas, e tu conheces todas.",
        },
    },
}


# ---------- the cases (specs/case-of-the-day.md and specs/culprit-of-the-night.md) ----------
# The date picks one of these cases (campus_clock.case_of_day); a saved game keeps its own. Server
# only, like everything above: the ids and the texts never reach the page.
# - `order`: the chat as shown. order[shown - 1] is the story's message number shown at that place.
# - `accepts`: more cards that break a claim of the hearing, by claim id; `right`: the professor's
#   line for each of those new pairs.
# - `texts`: {exact classic text: what this case says instead}, in each language (campus_evidence.retell).
# "outsider" is the classic case, exactly as before: nothing is added and no text is swapped.
# The cover photo, its date (Saturday 17 October) and the code of computer 12 are the same in every
# case (specs/calendar-code.md): no case swaps a dated line, and no case text touches the group's
# memories at computer 12, so what Tomás, Rita and Leonor remember of that day is true in every case.
CASES = {
    "outsider": {"order": [1, 2, 3, 4, 5],
                 "accepts": {}, "right": {"en": {}, "pt": {}}, "texts": {"en": {}, "pt": {}}},
    # Tomás let Duarte in (design-notes/texts-ideas.md, B1): he never made his slides, and Duarte, who
    # repeats the course, promised to make them if his name went on the report. Tomás lies about
    # computer 12 and the slides; the file history names his account.
    "tomas": {
        "order": [5, 1, 2, 3, 4],
        "accepts": {"name": ["files", "tomas_word"]},
        # The professor's line when the confession answers the claim "name" (point 5).
        "right": {"en": {"name": {"tomas_word": "\"The person who put the name there has told me so himself. So much for 'since the first draft'.\""}},
                  "pt": {"name": {"tomas_word": "\"Quem pôs lá o nome já mo disse ele próprio. Lá se vai o 'desde o primeiro rascunho'.\""}}},
        "texts": {
            "en": {
                # the chat (story.py, group_chat): messages 1 to 4 (B1.1 to B1.4); message 5 does not change
                "Leonor, 3 weeks ago, 9:05 pm: \"Can someone book the study room for Thursday?\"":
                    "Rita, 3 weeks ago, 9:05 pm: \"Can someone book the study room for Thursday?\"",
                "Unknown number, 3 weeks ago, 9:07 pm: \"Booked it. I wrote the conclusion too, like always.\"":
                    "Duarte, 3 weeks ago, 9:07 pm: \"Booked it. I wrote the conclusion too, like always.\"",
                "Rita, 2 weeks ago, 6:40 pm: \"Photo for the cover is ready. Four of us, finally!\"":
                    "Leonor, 2 weeks ago, 6:40 pm: \"Photo for the cover is ready. Four of us, finally!\"",
                "Duarte, 3 weeks ago, 10:10 pm: \"Can't wait for the five of us to present.\"":
                    "Unknown number, 3 weeks ago, 10:10 pm: \"Can't wait for the five of us to present.\"",
                # the file history names the account (B1.5, B1.6)
                "You plug the USB stick into computer 12 and compare. In the backups on the USB stick, every version has four authors. In the shared folder, the current version was changed yesterday at 11:47 pm, from this same computer: someone added \"Duarte\" to the report and swapped the photo. You recover the original version of the work.":
                    "You plug the USB stick into computer 12 and compare. In the backups on the USB stick, every version has four authors. In the shared folder, the current version was changed yesterday at 11:47 pm, from this same computer, and the folder says from which account: Tomás's. \"Duarte\" was added to the report and the photo was swapped. You recover the original version of the work.",
                "You have compared the files: four authors in every copy on the USB stick, and a change in the shared folder yesterday at 11:47 pm.":
                    "You have compared the files: four authors in every copy on the USB stick, and a change in the shared folder yesterday at 11:47 pm, made from Tomás's account.",
                # the card labels (B1.7, B1.8)
                "The file history: four authors in every backup":
                    "The file history: four authors in every backup, and the fifth name added from Tomás's account",
                "Tomás's word: he never wrote that message and made the slides himself":
                    "Tomás's confession: he added Duarte last night and wrote the message himself",
                # Rita, `pen`: Tomás's alibi falls here (B1.9)
                "\"The USB stick? It should be here somewhere, but I can't find it.\" She looks at the table. \"We stayed here late last night eating pizza, but with this mess, it could be anywhere.\"":
                    "\"The USB stick? It should be here somewhere, but I can't find it.\" She looks at the table. \"We stayed here late last night eating pizza. Tomás went off to the lab at half past eleven, on his own.\"",
                "Rita cannot find the USB stick. The group ate pizza here last night.":
                    "Rita cannot find the USB stick. The group ate pizza here last night; Tomás went to the lab alone at half past eleven.",
                # Tomás lies: `who` (the account and Rita's half past eleven say otherwise), `msg5` (the arrival line) and `slides` (B1.10 to B1.13)
                "\"Only a hood. Like the one Duarte wears. But nobody ever saw him arrive.\"":
                    "\"Only a hood. Like the one Duarte wears.\" He keeps his eyes on his screen. \"I was at computer 11 all night. I never went near computer 12.\"",
                "Tomás saw someone in a hood at computer 12 near midnight.":
                    "Tomás says he saw someone in a hood at computer 12 near midnight, and that he never went near it himself.",
                "\"'Duarte did the slides'? It is under my name, but I do not remember writing it. My phone buzzed with it last night, near midnight, as if it had been sent three weeks ago.\"":
                    "\"'Duarte did the slides'? I wrote that weeks ago. It is just true.\" He does not look at you.",
                "Tomás does not remember writing message 5; it reached his phone last night.":
                    "Tomás says he wrote the message with his name weeks ago.",
                "Ask about message 5, the one with his name":
                    "Ask about message 1, the one with his name",
                "Tomás keeps his eyes on the screen. \"The slides? I am finishing them. But the chat says Duarte did them, under my name. So maybe he did, and I only tidied up.\"":
                    "Tomás keeps his eyes on the screen. \"The slides? Duarte made them. I said so in the chat, three weeks ago.\"",
                "Tomás thinks Duarte may have made the slides, only because a chat message under his own name says so.":
                    "Tomás says Duarte made the slides, and that he wrote so in the chat three weeks ago.",
                # the reveals: Tomás confesses and still stands in the lab door; Leonor is shaken; Rita is a witness (B1.14 to B1.16)
                "Tomás reads the line under his name, then the small grey line beneath it. \"Arrived yesterday, 11:49 pm. At 11:49 I was sitting right here, one computer away from the one in the hood. I did not type a word.\" His voice drops. \"I never sent that. And the slides... I made the slides. All eleven. I was here until two on Tuesday.\" He turns his chair to face the glass wall. \"He walks the corridor, you know. Go back to the computer. If he comes, I will be standing in the door.\"":
                    "Tomás reads the small grey line under his message. \"Arrived yesterday, 11:49 pm.\" He closes his eyes. \"I wrote it last night. And I put his name on the cover at 11:47, from computer 12. I never made the slides. Duarte said he would make them if his name went on the report.\" He turns his chair to face the glass wall. \"He walks the corridor, you know. Go back to the computer. If he comes, I will be standing in the door. I owe you that.\"",
                "Tomás never wrote the message about the slides: he made them himself and will say so. He is watching the corridor for you.":
                    "Tomás confessed: he added Duarte last night, from computer 12, and wrote the message himself. He is watching the corridor for you.",
                "You tell her what Tomás said about the message with his name. Leonor stops with her thumb on the screen. \"He never wrote it?\" She scrolls back, slower this time. \"Then I do not know what I have been reading.\"":
                    "You tell her what Tomás told you. Leonor stops with her thumb on the screen. \"Tomás did this?\" She scrolls back, slower this time. \"Then I do not know what I have been reading.\"",
                "Leonor did not know that Tomás never wrote the message with his name. It shook her.":
                    "Leonor did not know that Tomás added Duarte. It shook her.",
                "Rita looks from your proof to her screen and back. \"So the photo did change.\" She laughs once, without any joy. \"I counted four. I said it out loud. I even wrote it in the chat: four of us, finally. That one is mine, I remember typing it.\" She closes the laptop. \"Tell the professor I counted. I will say it to his face.\"":
                    "Rita looks from your proof to her screen and back. \"So the photo did change.\" She laughs once, without any joy. \"I counted four. I said it out loud, on the day, to all of you.\" She closes the laptop. \"Tell the professor I counted. I will say it to his face.\"",
                "Rita counted four people on the day of the photo. The chat message that says four of them is hers. She will tell the professor.":
                    "Rita counted four people on the day of the photo. She will tell the professor.",
                # Leonor's own message is the one about the photo; Duarte names Tomás (B1.17, B1.18)
                "\"The one asking to book the study room. I wrote that at this table, three weeks ago.\" Leonor scrolls with one finger. \"The ones from the number I did not know all arrived within minutes of each other, last night.\"":
                    "\"The one about the cover photo. I wrote that the evening we took it.\" Leonor scrolls with one finger. \"The ones from the number I did not know all arrived within minutes of each other, last night.\"",
                "Leonor wrote the chat message about booking the study room herself.":
                    "Leonor wrote the chat message about the cover photo herself.",
                "\"The slides, of course. Ask anyone.\" He hesitates for a second.":
                    "\"The slides, of course. Ask Tomás, he will tell you.\" He hesitates for a second.",
                # the professor, when Tomás's confession answers the messages (B1.23)
                "\"Then the person whose name is on it never sent it. That answers this one.\"":
                    "\"Its author tells me he wrote it last night. A message written yesterday proves nothing about three weeks ago.\"",
                # the endings (B1.25 to B1.27); `fifth_element` keeps its text in every case
                "You show the history on the USB stick and the three messages you flagged: one from a number outside the group, one that counts five of you when there were four, and one that arrived last night, two minutes after the shared folder was changed. Leonor walks in with the original messages, and they match. The professor crosses the fifth name off the list and asks Duarte to explain. He has no answer. Tomorrow, the four of you present, with the case closed.":
                    "You show the history on the USB stick and the three messages you flagged: one from Duarte himself, weeks before anyone had heard of him; one from a number nobody knew, counting five of you; and one under Tomás's name that arrived last night, two minutes after his own account changed the shared folder. Leonor walks in with the original messages, and they match. Before the professor can ask, Tomás stands up and tells the room what he did: the name, the photo and the message, all for slides he never made. The professor crosses the fifth name off the list. Tomorrow, the four of you present, and Tomás presents the slides he finishes tonight.",
                "You show the history on the USB stick: four authors until last night. Leonor walks in and hands over the messages she kept: they were all sent on the same night, from a new number, with fake dates. The professor crosses the fifth name off the list. Duarte leaves the auditorium without a word. Tomorrow, the four of you present.":
                    "You show the history on the USB stick: four authors until last night, and the last change made from Tomás's account. Leonor walks in and hands over the messages she kept: they were all sent on the same night, with fake dates. The professor crosses the fifth name off the list. Duarte leaves the auditorium without a word, and Tomás does not look at any of you. Tomorrow, the four of you present.",
                "You show the history on the USB stick: the original work is recovered and had four authors until last night. But Duarte raises his phone: \"I have messages from everyone proving I took part.\" Without the original messages, you cannot prove they are fake. The professor sighs: \"Without proof that the messages are fake, the name stays.\" Tomorrow, the five of you present.":
                    "You show the history on the USB stick: the original work had four authors until last night. But Duarte raises his phone: \"I have messages from everyone proving I took part.\" Tomás nods along, a little too fast. Without the original messages, you cannot prove they are fake. The professor sighs: \"Without proof that the messages are fake, the name stays.\" Tomorrow, the five of you present.",
                # one sentence of the true ending: Rita stays last, right before her quote (B1.28)
                "Leonor comes in with her phone, Tomás with his slides, Rita counting under her breath.":
                    "Tomás comes in first, with the slides he finally finished tonight, and does not look at you; then Leonor with her phone, and Rita counting under her breath.",
            },
            "pt": {
                # the chat (story.py, group_chat): messages 1 to 4 (B1.1 to B1.4); message 5 does not change
                "Leonor, há 3 semanas, 21h05: \"Alguém pode reservar a sala de estudo para quinta-feira?\"":
                    "Rita, há 3 semanas, 21h05: \"Alguém pode reservar a sala de estudo para quinta-feira?\"",
                "Número desconhecido, há 3 semanas, 21h07: \"Já reservei. Também escrevi a conclusão, como sempre.\"":
                    "Duarte, há 3 semanas, 21h07: \"Já reservei. Também escrevi a conclusão, como sempre.\"",
                "Rita, há 2 semanas, 18h40: \"A fotografia para a capa está pronta. Os quatro, finalmente!\"":
                    "Leonor, há 2 semanas, 18h40: \"A fotografia para a capa está pronta. Os quatro, finalmente!\"",
                "Duarte, há 3 semanas, 22h10: \"Mal posso esperar para apresentarmos os cinco.\"":
                    "Número desconhecido, há 3 semanas, 22h10: \"Mal posso esperar para apresentarmos os cinco.\"",
                # the file history names the account (B1.5, B1.6)
                "Ligas a pen ao computador 12 e comparas. Nas cópias de segurança da pen, todas as versões têm quatro autores. Na pasta partilhada, a versão atual foi alterada ontem às 23h47, a partir deste mesmo computador: alguém acrescentou \"Duarte\" ao relatório e trocou a fotografia. Recuperas a versão original do trabalho.":
                    "Ligas a pen ao computador 12 e comparas. Nas cópias de segurança da pen, todas as versões têm quatro autores. Na pasta partilhada, a versão atual foi alterada ontem às 23h47, a partir deste mesmo computador, e a pasta diz de que conta: a do Tomás. Foi acrescentado \"Duarte\" ao relatório e trocada a fotografia. Recuperas a versão original do trabalho.",
                "Já comparaste os ficheiros: quatro autores em todas as cópias da pen, e uma alteração na pasta partilhada ontem às 23h47.":
                    "Já comparaste os ficheiros: quatro autores em todas as cópias da pen, e uma alteração na pasta partilhada ontem às 23h47, feita a partir da conta do Tomás.",
                # the card labels (B1.7, B1.8)
                "O histórico dos ficheiros: quatro autores em todas as cópias":
                    "O histórico dos ficheiros: quatro autores em todas as cópias, e o quinto nome acrescentado a partir da conta do Tomás",
                "A palavra do Tomás: nunca escreveu aquela mensagem e foi ele que fez os slides":
                    "A confissão do Tomás: acrescentou o Duarte ontem à noite e escreveu ele próprio a mensagem",
                # Rita, `pen`: Tomás's alibi falls here (B1.9)
                "\"A pen? Devia estar aqui, mas não a encontro.\" Olha para a mesa. \"Ontem ficámos aqui até tarde a comer pizza, mas com esta confusão, pode estar em qualquer lado.\"":
                    "\"A pen? Devia estar aqui, mas não a encontro.\" Olha para a mesa. \"Ontem ficámos aqui até tarde a comer pizza. O Tomás foi sozinho para a sala de informática às onze e meia.\"",
                "Rita: não encontra a pen. O grupo comeu pizza aqui ontem à noite.":
                    "Rita: não encontra a pen. O grupo comeu pizza aqui ontem à noite; o Tomás foi sozinho para a sala de informática às onze e meia.",
                # Tomás lies: `who` (the account and Rita's half past eleven say otherwise), `msg5` (the arrival line) and `slides` (B1.10 to B1.13)
                "\"Só vi um capuz. Como o que o Duarte usa. Mas ninguém o viu chegar.\"":
                    "\"Só vi um capuz. Como o que o Duarte usa.\" Não tira os olhos do ecrã. \"Estive no computador 11 a noite toda. Nunca me aproximei do 12.\"",
                "O Tomás viu alguém de capuz no computador 12 perto da meia-noite.":
                    "O Tomás diz que viu alguém de capuz no computador 12 perto da meia-noite e que ele próprio nunca se aproximou.",
                "\"'Os slides foram do Duarte'? Está com o meu nome, mas não me lembro de a ter escrito. O meu telemóvel apitou com ela ontem à noite, perto da meia-noite, como se tivesse sido enviada há três semanas.\"":
                    "\"'Os slides foram do Duarte'? Escrevi isso há semanas. É verdade e pronto.\" Não olha para ti.",
                "O Tomás não se lembra de ter escrito a mensagem 5; chegou-lhe ao telemóvel ontem à noite.":
                    "O Tomás diz que escreveu a mensagem com o nome dele há semanas.",
                "Perguntar pela mensagem 5, a que tem o nome dele":
                    "Perguntar pela mensagem 1, a que tem o nome dele",
                "O Tomás não tira os olhos do ecrã. \"Os slides? Estou a acabá-los. Mas o chat diz que foram do Duarte, com o meu nome. Se calhar foram mesmo, e eu só arrumei.\"":
                    "O Tomás não tira os olhos do ecrã. \"Os slides? Foi o Duarte que os fez. Eu disse-o no chat, há três semanas.\"",
                "O Tomás acha que os slides podem ter sido do Duarte, só porque uma mensagem do chat com o nome dele o diz.":
                    "O Tomás diz que foi o Duarte que fez os slides e que o escreveu no chat há três semanas.",
                # the reveals: Tomás confesses and still stands in the lab door; Leonor is shaken; Rita is a witness (B1.14 to B1.16)
                "O Tomás lê a linha por baixo do nome dele e depois a linha cinzenta mais pequena. \"Chegou ontem às 23h49. Às 23h49 eu estava aqui sentado, no computador ao lado do rapaz de capuz. Não escrevi uma palavra.\" Baixa a voz. \"Eu nunca enviei isto. E os slides... fui eu que fiz os slides. Os onze. Fiquei aqui até às duas na terça-feira.\" Roda a cadeira para a parede de vidro. \"Ele anda pelo corredor, sabes. Volta para o computador. Se ele vier, eu fico à porta.\"":
                    "O Tomás lê a linha cinzenta mais pequena por baixo da mensagem. \"Chegou ontem às 23h49.\" Fecha os olhos. \"Escrevi-a ontem à noite. E pus o nome dele na capa às 23h47, no computador 12. Nunca fiz os slides. O Duarte disse que os fazia se o nome dele fosse para o relatório.\" Roda a cadeira para a parede de vidro. \"Ele anda pelo corredor, sabes. Volta para o computador. Se ele vier, eu fico à porta. Devo-te isso.\"",
                "O Tomás nunca escreveu a mensagem sobre os slides: foi ele que os fez e vai dizê-lo. Fica a vigiar o corredor por ti.":
                    "O Tomás confessou: acrescentou o Duarte ontem à noite, no computador 12, e escreveu ele próprio a mensagem. Fica a vigiar o corredor por ti.",
                "Contas-lhe o que o Tomás disse sobre a mensagem com o nome dele. A Leonor fica com o polegar parado no ecrã. \"Ele nunca a escreveu?\" Volta atrás na conversa, mais devagar. \"Então já não sei o que é que andei a ler.\"":
                    "Contas-lhe o que o Tomás te disse. A Leonor fica com o polegar parado no ecrã. \"Foi o Tomás?\" Volta atrás na conversa, mais devagar. \"Então já não sei o que é que andei a ler.\"",
                "A Leonor não sabia que o Tomás nunca escreveu a mensagem com o nome dele. Ficou abalada.":
                    "A Leonor não sabia que tinha sido o Tomás a acrescentar o Duarte. Ficou abalada.",
                "A Rita olha da tua prova para o ecrã e outra vez para a prova. \"Então a fotografia mudou mesmo.\" Ri-se uma vez, sem alegria nenhuma. \"Eu contei quatro. Disse-o em voz alta. Até o escrevi no chat: os quatro, finalmente. Essa é minha, lembro-me de a escrever.\" Fecha o portátil. \"Diz ao professor que eu contei. Eu digo-lho na cara.\"":
                    "A Rita olha da tua prova para o ecrã e outra vez para a prova. \"Então a fotografia mudou mesmo.\" Ri-se uma vez, sem alegria nenhuma. \"Eu contei quatro. Disse-o em voz alta, nesse dia, a todos vocês.\" Fecha o portátil. \"Diz ao professor que eu contei. Eu digo-lho na cara.\"",
                "A Rita contou quatro pessoas no dia da fotografia. A mensagem do chat que fala nos quatro é dela. Vai dizê-lo ao professor.":
                    "A Rita contou quatro pessoas no dia da fotografia. Vai dizê-lo ao professor.",
                # Leonor's own message is the one about the photo; Duarte names Tomás (B1.17, B1.18)
                "\"A que pede para reservar a sala de estudo. Escrevi-a nesta mesa, há três semanas.\" A Leonor percorre o ecrã com um dedo. \"As do número que eu não conhecia chegaram todas com minutos de diferença, ontem à noite.\"":
                    "\"A da fotografia da capa. Escrevi-a na noite em que a tirámos.\" A Leonor percorre o ecrã com um dedo. \"As do número que eu não conhecia chegaram todas com minutos de diferença, ontem à noite.\"",
                "A Leonor escreveu ela própria a mensagem do chat sobre reservar a sala de estudo.":
                    "A Leonor escreveu ela própria a mensagem do chat sobre a fotografia da capa.",
                "\"Os slides, claro. Pergunta a qualquer um.\" Hesita por um segundo.":
                    "\"Os slides, claro. Pergunta ao Tomás, ele diz-te.\" Hesita por um segundo.",
                # the professor, when Tomás's confession answers the messages (B1.23)
                "\"Então quem a assina nunca a enviou. Essa fica respondida.\"":
                    "\"O autor diz-me que a escreveu ontem à noite. Uma mensagem escrita ontem não prova nada sobre há três semanas.\"",
                # the endings (B1.25 to B1.27); `fifth_element` keeps its text in every case
                "Mostras o histórico da pen e as três mensagens que marcaste: uma de um número fora do grupo, uma que fala em cinco quando eram quatro, e uma que chegou ontem à noite, dois minutos depois de a pasta partilhada ser alterada. A Leonor entra com as mensagens originais, e batem certo. O professor risca o quinto nome da lista e pede ao Duarte que se explique. Ele não tem resposta. Amanhã apresentam os quatro, com o caso encerrado.":
                    "Mostras o histórico da pen e as três mensagens que marcaste: uma do próprio Duarte, semanas antes de alguém ter ouvido falar dele; uma de um número que ninguém conhecia, a contar cinco; e uma com o nome do Tomás que chegou ontem à noite, dois minutos depois de a conta dele ter alterado a pasta partilhada. A Leonor entra com as mensagens originais, e batem certo. Antes de o professor perguntar, o Tomás levanta-se e conta o que fez: o nome, a fotografia e a mensagem, tudo por uns slides que nunca fez. O professor risca o quinto nome da lista. Amanhã apresentam os quatro, e o Tomás apresenta os slides que acaba esta noite.",
                "Mostras o histórico da pen: quatro autores até ontem à noite. A Leonor entra e entrega as mensagens que guardou: foram todas enviadas na mesma noite, de um número novo, com datas falsas. O professor risca o quinto nome da lista. O Duarte sai do auditório sem dizer nada. Amanhã apresentam os quatro.":
                    "Mostras o histórico da pen: quatro autores até ontem à noite, e a última alteração feita a partir da conta do Tomás. A Leonor entra e entrega as mensagens que guardou: foram todas enviadas na mesma noite, com datas falsas. O professor risca o quinto nome da lista. O Duarte sai do auditório sem dizer nada, e o Tomás não olha para nenhum de vocês. Amanhã apresentam os quatro.",
                "Mostras o histórico da pen: o trabalho original está recuperado e tinha quatro autores até ontem à noite. Mas o Duarte levanta o telemóvel: \"Tenho mensagens de todos a provar que participei.\" Sem as mensagens originais, não consegues provar que são falsas. O professor suspira: \"Sem provas de que as mensagens são falsas, o nome fica.\" Amanhã apresentam os cinco.":
                    "Mostras o histórico da pen: o trabalho original tinha quatro autores até ontem à noite. Mas o Duarte levanta o telemóvel: \"Tenho mensagens de todos a provar que participei.\" O Tomás acena que sim, depressa demais. Sem as mensagens originais, não consegues provar que são falsas. O professor suspira: \"Sem provas de que as mensagens são falsas, o nome fica.\" Amanhã apresentam os cinco.",
                # one sentence of the true ending: Rita stays last, right before her quote (B1.28)
                "A Leonor entra com o telemóvel, o Tomás com os slides, a Rita a contar baixinho.":
                    "O Tomás entra primeiro, com os slides que finalmente acabou esta noite, sem olhar para ti; depois a Leonor com o telemóvel, e a Rita a contar baixinho.",
            },
        },
    },
    # Rita let Duarte in (design-notes/texts-ideas.md, B2): he needed a group with a good grade and
    # she said yes without asking anyone. She says she went home early; the file history names her account.
    "rita": {
        "order": [2, 4, 3, 5, 1],
        "accepts": {"name": ["files", "rita_word"]},
        # The professor's line when the confession answers the claim "name" (point 5).
        "right": {"en": {"name": {"rita_word": "\"The person who put the name there has told me so herself. Go on.\""}},
                  "pt": {"name": {"rita_word": "\"Quem pôs lá o nome já mo disse ela própria. Continue.\""}}},
        "texts": {
            "en": {
                # the chat (story.py, group_chat): messages 1 and 3 (B2.1, B2.3); messages 2, 4 and 5 do not change
                "Leonor, 3 weeks ago, 9:05 pm: \"Can someone book the study room for Thursday?\"":
                    "Tomás, 3 weeks ago, 9:05 pm: \"Can someone book the study room for Thursday?\"",
                "Rita, 2 weeks ago, 6:40 pm: \"Photo for the cover is ready. Four of us, finally!\"":
                    "Leonor, 2 weeks ago, 6:40 pm: \"Photo for the cover is ready. Four of us, finally!\"",
                # the file history names the account (B2.5, B2.6)
                "You plug the USB stick into computer 12 and compare. In the backups on the USB stick, every version has four authors. In the shared folder, the current version was changed yesterday at 11:47 pm, from this same computer: someone added \"Duarte\" to the report and swapped the photo. You recover the original version of the work.":
                    "You plug the USB stick into computer 12 and compare. In the backups on the USB stick, every version has four authors. In the shared folder, the current version was changed yesterday at 11:47 pm, from this same computer, and the folder says from which account: Rita's. \"Duarte\" was added to the report and the photo was swapped. You recover the original version of the work.",
                "You have compared the files: four authors in every copy on the USB stick, and a change in the shared folder yesterday at 11:47 pm.":
                    "You have compared the files: four authors in every copy on the USB stick, and a change in the shared folder yesterday at 11:47 pm, made from Rita's account.",
                # the card labels (B2.7, B2.8)
                "The file history: four authors in every backup":
                    "The file history: four authors in every backup, and the fifth name added from Rita's account",
                "Rita's word: she counted four people on the day of the photo":
                    "Rita's confession: she added Duarte and swapped the photo last night",
                # Rita lies: `pen` (Tomás saw her, and the pizza receipt says four), `duarte`, `warned` (B2.9 to B2.11)
                "\"The USB stick? It should be here somewhere, but I can't find it.\" She looks at the table. \"We stayed here late last night eating pizza, but with this mess, it could be anywhere.\"":
                    "\"The USB stick? No idea.\" She looks at the table, then away. \"I went home early last night. The others stayed here eating pizza.\"",
                "Rita cannot find the USB stick. The group ate pizza here last night.":
                    "Rita says she went home early last night, while the others ate pizza here, and does not know where the USB stick is.",
                "\"Duarte... honestly, I cannot picture him. Every time I try, I only see the name on the cover.\"":
                    "\"Duarte? He is... fine. He did his part.\" She goes back to her laptop a little too quickly.",
                "Rita goes quiet. \"If that is true, somebody wanted us to doubt ourselves.\"":
                    "Rita goes very still. \"Last night? I was at home last night.\"",
                "Rita doubts the fifth name too.":
                    "Rita says she was at home last night.",
                # Tomás tells the truth, and it is the second sign (B2.12 to B2.15)
                "\"Only a hood. Like the one Duarte wears. But nobody ever saw him arrive.\"":
                    "\"Long hair and a pink jumper. I thought it was Rita, but she told us she was going home early.\"",
                "Tomás saw someone in a hood at computer 12 near midnight.":
                    "Tomás saw someone with long hair and a pink jumper at computer 12 near midnight. He thought it was Rita.",
                "Ask about message 5, the one with his name":
                    "Ask about message 4, the one with his name",
                "Tomás does not remember writing message 5; it reached his phone last night.":
                    "Tomás does not remember writing message 4; it reached his phone last night.",
                "Tomás reads the line under his name, then the small grey line beneath it. \"Arrived yesterday, 11:49 pm. At 11:49 I was sitting right here, one computer away from the one in the hood. I did not type a word.\" His voice drops. \"I never sent that. And the slides... I made the slides. All eleven. I was here until two on Tuesday.\" He turns his chair to face the glass wall. \"He walks the corridor, you know. Go back to the computer. If he comes, I will be standing in the door.\"":
                    "Tomás reads the line under his name, then the small grey line beneath it. \"Arrived yesterday, 11:49 pm. At 11:49 I was sitting right here, one computer away from whoever was at computer 12. I did not type a word.\" His voice drops. \"I never sent that. And the slides... I made the slides. All eleven. I was here until two on Tuesday.\" He turns his chair to face the glass wall. \"He walks the corridor, you know. Go back to the computer. If he comes, I will be standing in the door.\"",
                # Rita confesses (B2.16)
                "Rita looks from your proof to her screen and back. \"So the photo did change.\" She laughs once, without any joy. \"I counted four. I said it out loud. I even wrote it in the chat: four of us, finally. That one is mine, I remember typing it.\" She closes the laptop. \"Tell the professor I counted. I will say it to his face.\"":
                    "Rita looks from your proof to her screen and back, and the smile goes. \"I put him there.\" She says it very quietly. \"Last night, at computer 12. He needed a group with a good grade, and I said yes before I asked any of you.\" She closes the laptop. \"Tell the professor. I will say it to his face.\"",
                "Rita counted four people on the day of the photo. The chat message that says four of them is hers. She will tell the professor.":
                    "Rita confessed: she added Duarte and swapped the photo last night, from computer 12. She will tell the professor.",
                # Leonor's own message is the one about the photo; Duarte names Rita (B2.17, B2.18)
                "\"The one asking to book the study room. I wrote that at this table, three weeks ago.\" Leonor scrolls with one finger. \"The ones from the number I did not know all arrived within minutes of each other, last night.\"":
                    "\"The one about the cover photo. I wrote that the evening we took it.\" Leonor scrolls with one finger. \"The ones from the number I did not know all arrived within minutes of each other, last night.\"",
                "Leonor wrote the chat message about booking the study room herself.":
                    "Leonor wrote the chat message about the cover photo herself.",
                "\"The slides, of course. Ask anyone.\" He hesitates for a second.":
                    "\"The slides, of course. Ask Rita, she knows.\" He hesitates for a second.",
                # the professor, when Rita's confession answers the photo (B2.23)
                "\"A witness who counted. I will hear her tomorrow; tonight I believe her.\"":
                    "\"The one who swapped it tells me what was there before: four people. I will hear her tomorrow.\"",
                # the endings (B2.25 to B2.27)
                "You show the history on the USB stick and the three messages you flagged: one from a number outside the group, one that counts five of you when there were four, and one that arrived last night, two minutes after the shared folder was changed. Leonor walks in with the original messages, and they match. The professor crosses the fifth name off the list and asks Duarte to explain. He has no answer. Tomorrow, the four of you present, with the case closed.":
                    "You show the history on the USB stick and the three messages you flagged: one from a number nobody knew; one from Duarte, counting five of you when there were four; and one under Tomás's name that arrived last night, two minutes after Rita's account changed the shared folder. Leonor walks in with the original messages, and they match. Rita does not wait to be asked: she tells the professor that she added the name and swapped the photo, because Duarte needed a group. The professor crosses the fifth name off the list. Tomorrow, the four of you present, and Rita has a lot to explain on the way there.",
                "You show the history on the USB stick: four authors until last night. Leonor walks in and hands over the messages she kept: they were all sent on the same night, from a new number, with fake dates. The professor crosses the fifth name off the list. Duarte leaves the auditorium without a word. Tomorrow, the four of you present.":
                    "You show the history on the USB stick: four authors until last night, and the last change made from Rita's account. Leonor walks in and hands over the messages she kept: they were all sent on the same night, with fake dates. The professor crosses the fifth name off the list. Duarte leaves the auditorium without a word, and Rita stares at the floor. Tomorrow, the four of you present.",
                "You show the history on the USB stick: the original work is recovered and had four authors until last night. But Duarte raises his phone: \"I have messages from everyone proving I took part.\" Without the original messages, you cannot prove they are fake. The professor sighs: \"Without proof that the messages are fake, the name stays.\" Tomorrow, the five of you present.":
                    "You show the history on the USB stick: the original work had four authors until last night. But Duarte raises his phone: \"I have messages from everyone proving I took part.\" Rita looks down at her hands. Without the original messages, you cannot prove they are fake. The professor sighs: \"Without proof that the messages are fake, the name stays.\" Tomorrow, the five of you present.",
                # one sentence of the true ending: Rita stays last, right before her quote (B2.28)
                "Leonor comes in with her phone, Tomás with his slides, Rita counting under her breath.":
                    "Leonor comes in with her phone, Tomás with his slides, and Rita last of all, slowly, counting under her breath.",
            },
            "pt": {
                # the chat (story.py, group_chat): messages 1 and 3 (B2.1, B2.3); messages 2, 4 and 5 do not change
                "Leonor, há 3 semanas, 21h05: \"Alguém pode reservar a sala de estudo para quinta-feira?\"":
                    "Tomás, há 3 semanas, 21h05: \"Alguém pode reservar a sala de estudo para quinta-feira?\"",
                "Rita, há 2 semanas, 18h40: \"A fotografia para a capa está pronta. Os quatro, finalmente!\"":
                    "Leonor, há 2 semanas, 18h40: \"A fotografia para a capa está pronta. Os quatro, finalmente!\"",
                # the file history names the account (B2.5, B2.6)
                "Ligas a pen ao computador 12 e comparas. Nas cópias de segurança da pen, todas as versões têm quatro autores. Na pasta partilhada, a versão atual foi alterada ontem às 23h47, a partir deste mesmo computador: alguém acrescentou \"Duarte\" ao relatório e trocou a fotografia. Recuperas a versão original do trabalho.":
                    "Ligas a pen ao computador 12 e comparas. Nas cópias de segurança da pen, todas as versões têm quatro autores. Na pasta partilhada, a versão atual foi alterada ontem às 23h47, a partir deste mesmo computador, e a pasta diz de que conta: a da Rita. Foi acrescentado \"Duarte\" ao relatório e trocada a fotografia. Recuperas a versão original do trabalho.",
                "Já comparaste os ficheiros: quatro autores em todas as cópias da pen, e uma alteração na pasta partilhada ontem às 23h47.":
                    "Já comparaste os ficheiros: quatro autores em todas as cópias da pen, e uma alteração na pasta partilhada ontem às 23h47, feita a partir da conta da Rita.",
                # the card labels (B2.7, B2.8)
                "O histórico dos ficheiros: quatro autores em todas as cópias":
                    "O histórico dos ficheiros: quatro autores em todas as cópias, e o quinto nome acrescentado a partir da conta da Rita",
                "A palavra da Rita: contou quatro pessoas no dia da fotografia":
                    "A confissão da Rita: acrescentou o Duarte e trocou a fotografia ontem à noite",
                # Rita lies: `pen` (Tomás saw her, and the pizza receipt says four), `duarte`, `warned` (B2.9 to B2.11)
                "\"A pen? Devia estar aqui, mas não a encontro.\" Olha para a mesa. \"Ontem ficámos aqui até tarde a comer pizza, mas com esta confusão, pode estar em qualquer lado.\"":
                    "\"A pen? Não faço ideia.\" Olha para a mesa e depois desvia o olhar. \"Ontem fui cedo para casa. Os outros ficaram aqui a comer pizza.\"",
                "Rita: não encontra a pen. O grupo comeu pizza aqui ontem à noite.":
                    "A Rita diz que ontem foi cedo para casa, enquanto os outros comiam pizza aqui, e que não sabe onde está a pen.",
                "\"O Duarte... sinceramente, não o consigo imaginar. Sempre que tento, só vejo o nome na capa.\"":
                    "\"O Duarte? É... simpático. Fez a parte dele.\" Volta para o portátil um bocadinho depressa demais.",
                "A Rita fica calada. \"Se for verdade, alguém quis que duvidássemos de nós próprios.\"":
                    "A Rita fica muito quieta. \"Ontem à noite? Ontem à noite eu estava em casa.\"",
                "A Rita também desconfia do quinto nome.":
                    "A Rita diz que ontem à noite estava em casa.",
                # Tomás tells the truth, and it is the second sign (B2.12 to B2.15)
                "\"Só vi um capuz. Como o que o Duarte usa. Mas ninguém o viu chegar.\"":
                    "\"Cabelo comprido e uma camisola cor-de-rosa. Pensei que era a Rita, mas ela tinha dito que ia cedo para casa.\"",
                "O Tomás viu alguém de capuz no computador 12 perto da meia-noite.":
                    "O Tomás viu alguém de cabelo comprido e camisola cor-de-rosa no computador 12 perto da meia-noite. Pensou que era a Rita.",
                "Perguntar pela mensagem 5, a que tem o nome dele":
                    "Perguntar pela mensagem 4, a que tem o nome dele",
                "O Tomás não se lembra de ter escrito a mensagem 5; chegou-lhe ao telemóvel ontem à noite.":
                    "O Tomás não se lembra de ter escrito a mensagem 4; chegou-lhe ao telemóvel ontem à noite.",
                "O Tomás lê a linha por baixo do nome dele e depois a linha cinzenta mais pequena. \"Chegou ontem às 23h49. Às 23h49 eu estava aqui sentado, no computador ao lado do rapaz de capuz. Não escrevi uma palavra.\" Baixa a voz. \"Eu nunca enviei isto. E os slides... fui eu que fiz os slides. Os onze. Fiquei aqui até às duas na terça-feira.\" Roda a cadeira para a parede de vidro. \"Ele anda pelo corredor, sabes. Volta para o computador. Se ele vier, eu fico à porta.\"":
                    "O Tomás lê a linha por baixo do nome dele e depois a linha cinzenta mais pequena. \"Chegou ontem às 23h49. Às 23h49 eu estava aqui sentado, no computador ao lado de quem estava no computador 12. Não escrevi uma palavra.\" Baixa a voz. \"Eu nunca enviei isto. E os slides... fui eu que fiz os slides. Os onze. Fiquei aqui até às duas na terça-feira.\" Roda a cadeira para a parede de vidro. \"Ele anda pelo corredor, sabes. Volta para o computador. Se ele vier, eu fico à porta.\"",
                # Rita confesses (B2.16)
                "A Rita olha da tua prova para o ecrã e outra vez para a prova. \"Então a fotografia mudou mesmo.\" Ri-se uma vez, sem alegria nenhuma. \"Eu contei quatro. Disse-o em voz alta. Até o escrevi no chat: os quatro, finalmente. Essa é minha, lembro-me de a escrever.\" Fecha o portátil. \"Diz ao professor que eu contei. Eu digo-lho na cara.\"":
                    "A Rita olha da tua prova para o ecrã e outra vez para a prova, e o sorriso desaparece. \"Fui eu que o pus lá.\" Di-lo muito baixinho. \"Ontem à noite, no computador 12. Ele precisava de um grupo com boa nota, e eu disse que sim antes de perguntar a algum de vocês.\" Fecha o portátil. \"Diz ao professor. Eu digo-lho na cara.\"",
                "A Rita contou quatro pessoas no dia da fotografia. A mensagem do chat que fala nos quatro é dela. Vai dizê-lo ao professor.":
                    "A Rita confessou: acrescentou o Duarte e trocou a fotografia ontem à noite, no computador 12. Vai dizê-lo ao professor.",
                # Leonor's own message is the one about the photo; Duarte names Rita (B2.17, B2.18)
                "\"A que pede para reservar a sala de estudo. Escrevi-a nesta mesa, há três semanas.\" A Leonor percorre o ecrã com um dedo. \"As do número que eu não conhecia chegaram todas com minutos de diferença, ontem à noite.\"":
                    "\"A da fotografia da capa. Escrevi-a na noite em que a tirámos.\" A Leonor percorre o ecrã com um dedo. \"As do número que eu não conhecia chegaram todas com minutos de diferença, ontem à noite.\"",
                "A Leonor escreveu ela própria a mensagem do chat sobre reservar a sala de estudo.":
                    "A Leonor escreveu ela própria a mensagem do chat sobre a fotografia da capa.",
                "\"Os slides, claro. Pergunta a qualquer um.\" Hesita por um segundo.":
                    "\"Os slides, claro. Pergunta à Rita, ela sabe.\" Hesita por um segundo.",
                # the professor, when Rita's confession answers the photo (B2.23)
                "\"Uma testemunha que contou. Ouço-a amanhã; esta noite, acredito nela.\"":
                    "\"Quem a trocou diz-me o que lá estava antes: quatro pessoas. Ouço-a amanhã.\"",
                # the endings (B2.25 to B2.27)
                "Mostras o histórico da pen e as três mensagens que marcaste: uma de um número fora do grupo, uma que fala em cinco quando eram quatro, e uma que chegou ontem à noite, dois minutos depois de a pasta partilhada ser alterada. A Leonor entra com as mensagens originais, e batem certo. O professor risca o quinto nome da lista e pede ao Duarte que se explique. Ele não tem resposta. Amanhã apresentam os quatro, com o caso encerrado.":
                    "Mostras o histórico da pen e as três mensagens que marcaste: uma de um número que ninguém conhecia; uma do Duarte, a contar cinco quando eram quatro; e uma com o nome do Tomás que chegou ontem à noite, dois minutos depois de a conta da Rita ter alterado a pasta partilhada. A Leonor entra com as mensagens originais, e batem certo. A Rita não espera que lhe perguntem: conta ao professor que acrescentou o nome e trocou a fotografia, porque o Duarte precisava de um grupo. O professor risca o quinto nome da lista. Amanhã apresentam os quatro, e a Rita tem muito que explicar pelo caminho.",
                "Mostras o histórico da pen: quatro autores até ontem à noite. A Leonor entra e entrega as mensagens que guardou: foram todas enviadas na mesma noite, de um número novo, com datas falsas. O professor risca o quinto nome da lista. O Duarte sai do auditório sem dizer nada. Amanhã apresentam os quatro.":
                    "Mostras o histórico da pen: quatro autores até ontem à noite, e a última alteração feita a partir da conta da Rita. A Leonor entra e entrega as mensagens que guardou: foram todas enviadas na mesma noite, com datas falsas. O professor risca o quinto nome da lista. O Duarte sai do auditório sem dizer nada, e a Rita fica a olhar para o chão. Amanhã apresentam os quatro.",
                "Mostras o histórico da pen: o trabalho original está recuperado e tinha quatro autores até ontem à noite. Mas o Duarte levanta o telemóvel: \"Tenho mensagens de todos a provar que participei.\" Sem as mensagens originais, não consegues provar que são falsas. O professor suspira: \"Sem provas de que as mensagens são falsas, o nome fica.\" Amanhã apresentam os cinco.":
                    "Mostras o histórico da pen: o trabalho original tinha quatro autores até ontem à noite. Mas o Duarte levanta o telemóvel: \"Tenho mensagens de todos a provar que participei.\" A Rita olha para as mãos. Sem as mensagens originais, não consegues provar que são falsas. O professor suspira: \"Sem provas de que as mensagens são falsas, o nome fica.\" Amanhã apresentam os cinco.",
                # one sentence of the true ending: Rita stays last, right before her quote (B2.28)
                "A Leonor entra com o telemóvel, o Tomás com os slides, a Rita a contar baixinho.":
                    "A Leonor entra com o telemóvel, o Tomás com os slides e, por último, devagar, a Rita, a contar baixinho.",
            },
        },
    },
}
