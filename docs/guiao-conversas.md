# Guião das conversas — O quinto elemento (jogo 3D)

Tudo o que as pessoas dizem no jogo 3D, em português e em inglês, tal como está no código.

> **Gerado em 21/11/2026 a partir de `prototypes/campus-3d/campus_people.py` e `story.py`.** O código é que manda: se mudares uma fala no código, este guião fica desatualizado até ser gerado outra vez.

## Como alterar uma fala

1. **Conversas** (o que cada pessoa diz quando falas com ela): `prototypes/campus-3d/campus_people.py`, dentro de `PEOPLE`. Há um bloco `"en"` (inglês) e um bloco `"pt"` (português). Ao lado de cada fala deste guião está o número da linha.
2. **Respostas às ações** (o que acontece quando escolhes ▶ abrir a gaveta, pedir a cópia, etc.): `story.py`, em `result_text` (quando resulta) e `blocked_text` (quando ainda não podes).
3. **O que vai para o balão:** só o que está **entre aspas** (`\"...\"` no código) aparece no balão e é lido pela voz. O resto aparece como narração, em itálico, fora dos balões. Exemplo: `Rita looks up from her laptop. \"You look awful.\"`: "Rita looks up from her laptop." é narração, e "You look awful." vai para o balão.
4. **Regras para não estragar nada** (os testes verificam-nas):
   - Muda só o texto entre as aspas de `"text"`, `"label"` e `"note"`. Não mudes os identificadores (`"start"`, `"photo"`, `"next": ...`, `"if": ...`, `"trust"`).
   - Se mudares uma fala em português, muda também a inglesa (e vice-versa). As duas línguas têm de ter as mesmas falas, respostas e condições: só o texto muda.
   - Dentro do texto, as aspas da fala escrevem-se `\"` (barra e aspas).
   - As falas nunca podem dizer quais são as mensagens falsas ("message 2", "mensagem 4"…).
5. Depois de mudar, corre `uv run pytest`. Se ficar verde, recarrega o jogo (http://localhost:8503).

**Legenda:** ⏳ *custa N minutos* é uma resposta agressiva: tira esses minutos à contagem decrescente (só no branch `harder-campus`; para mudar, altera `"cost": 5` no código). *Confiança* são os corações (0 a 3; com 0 a pessoa acaba a conversa). *Diário* é a nota que fica guardada no diário do telemóvel. "→ fim" acaba a conversa.

## Rita
Onde está: **Sala de estudo** (`study_room`).

### `start`
- 🇵🇹 A Rita levanta os olhos do portátil. "Estás com um ar péssimo. Dormiste alguma coisa?"  *(linha 172)*
- 🇬🇧 Rita looks up from her laptop. "You look awful. Did you sleep at all?"  *(linha 50)*
- Respostas:
  - "Perguntar pela fotografia do grupo" / "Ask about the group photo" → `photo`
  - "Perguntar o que ela se lembra do Duarte" / "Ask what she remembers about Duarte" → `duarte`
  - "Perguntar onde está a pen" / "Ask where the USB stick is" → `pen`
  - "Perguntar pelas mensagens do chat" / "Ask about the chat messages" → `chat` *(só aparece se `files_viewed` = `True`)*
  - "Até já." / "Goodbye." → fim

### `photo`
- 🇵🇹 "A fotografia? Tirámo-la depois da última reunião. Quatro pessoas, a Leonor ficou com o temporizador. Lembro-me de contar as cabeças."  *(linha 179)*
- 🇬🇧 "The photo? We took it after the last meeting. Four of us, Leonor held the timer. I remember counting heads."  *(linha 57)*
- 📓 Diário: A Rita lembra-se de quatro pessoas na fotografia do grupo. / Rita remembers four people in the group photo.
- Respostas:
  - "Até já." / "Goodbye." → fim

### `pen`
- 🇵🇹 "A pen? Devia estar na gaveta do grupo, mas não está." Olha para a mesa. "Ontem ficámos aqui até tarde a comer pizza. Com esta confusão, pode estar em qualquer lado."  *(linha 182)*
- 🇬🇧 "The USB stick? It should be in the group drawer, but it is not." She looks at the table. "We stayed here late last night eating pizza. With this mess, it could be anywhere."  *(linha 60)*
- 📓 Diário: Rita: a pen não está na gaveta. O grupo comeu pizza aqui ontem à noite. / Rita: the USB stick is not in the drawer. The group ate pizza here last night.
- Respostas:
  - "Até já." / "Goodbye." → fim

### `duarte`
- 🇵🇹 "O Duarte... sinceramente, não o consigo imaginar. Sempre que tento, só vejo o nome na capa."  *(linha 184)*
- 🇬🇧 "Duarte... honestly, I cannot picture him. Every time I try, I only see the name on the cover."  *(linha 62)*
- Respostas:
  - "Dizer que achas que o nome foi acrescentado ontem à noite" / "Say you think the name was added last night" → `warned`

### `warned`
- 🇵🇹 A Rita fica calada. "Se for verdade, alguém quis que duvidássemos de nós próprios."  *(linha 186)*
- 🇬🇧 Rita goes quiet. "If that is true, somebody wanted us to doubt ourselves."  *(linha 64)*
- 📓 Diário: A Rita também desconfia do quinto nome. / Rita doubts the fifth name too.
- Respostas:
  - "Até já." / "Goodbye." → fim

### `chat`
- 🇵🇹 "Repara na hora a que as mensagens chegam. Algumas dizem há três semanas, mas no meu telemóvel aparecem como novas, de ontem à noite. Mensagens antigas não funcionam assim."  *(linha 189)*
- 🇬🇧 "Look at when the messages arrive. Some say three weeks ago, but my phone shows them as new, last night. That is not how old messages work."  *(linha 67)*
- 📓 Diário: Rita: uma mensagem antiga não chega como nova. Compara as horas de chegada no chat do grupo. / Rita: an old message does not arrive as new. Compare the arrival times in the group chat.
- Respostas:
  - "Até já." / "Goodbye." → fim

### Ações feitas nesta conversa (em `story.py`)
- **▶ Abrir a gaveta do grupo** / Open the group drawer (`open_drawer`)
  - Se resultar 🇵🇹: Encontras a pen onde o grupo guardava as cópias de segurança do projeto. Guardas a pen.
  - Se resultar 🇬🇧: You find the USB stick where the group kept the project backups. You take the USB stick.

## Funcionária
Onde está: **Reprografia** (`print_shop`).

### `start`
- 🇵🇹 A funcionária ajeita os óculos. "Fechamos daqui a dez minutos. Do que precisas?"  *(linha 194)*
- 🇬🇧 The clerk adjusts her glasses. "We close in ten minutes. What do you need?"  *(linha 72)*
- Respostas:
  - "Perguntar pelo pedido da fotografia da capa" / "Ask about the cover photo order" → `order`
  - "Perguntar se mais alguém veio perguntar" / "Ask if anyone else came asking" → `visitor`
  - "Até já." / "Goodbye." → fim

### `order`
- 🇵🇹 "A 14 de novembro, na semana passada. Tiraram a fotografia e mandaram-na imprimir no mesmo dia. Quatro pessoas, lembro-me porque tive de cortar a impressão. O ficheiro original do pedido ainda está guardado."  *(linha 199)*
- 🇬🇧 "On 14 November, last week. You took the photo and had it printed the same day. Four people in it, I remember because I had to crop the print. The original order file is still saved."  *(linha 77)*
- 📓 Diário: A fotografia da capa foi tirada e impressa a 14 de novembro. A reprografia ainda tem o ficheiro original do pedido. / The cover photo was taken and printed on 14 November. The print shop still has the original order file.
- Respostas:
  - "Até já." / "Goodbye." → fim

### `visitor`
- 🇵🇹 "Ontem ao fim da tarde passou por aqui um rapaz de capuz. Pediu para reimprimir a capa com outra fotografia."  *(linha 202)*
- 🇬🇧 "A young man in a hood came by yesterday evening. He asked to reprint the cover with a different photo."  *(linha 80)*
- 📓 Diário: Um desconhecido de capuz pediu à reprografia para mudar a fotografia da capa. / A hooded stranger asked the print shop to change the cover photo.
- Respostas:
  - "Perguntar como era ele" / "Ask what he looked like" → `hood`

### `hood`
- 🇵🇹 "Um sorriso calmo. Não quis deixar o nome. Pensei que fosse do vosso grupo."  *(linha 205)*
- 🇬🇧 "A calm smile. He did not want to leave a name. I thought he was one of your group."  *(linha 83)*
- Respostas:
  - "Até já." / "Goodbye." → fim

### Ações feitas nesta conversa (em `story.py`)
- **▶ Pedir uma cópia do pedido original** / Ask for a copy of the original order (`request_copy`)
  - Se resultar 🇵🇹: A funcionária volta a imprimir o ficheiro que ficou guardado no pedido. Na fotografia original estão quatro pessoas. Guardas a fotografia.
  - Se resultar 🇬🇧: The clerk prints again the file that was saved with the order. The original photo shows four people. You take the photo.

## Leonor
Onde está: **Biblioteca** (`library`).

### `start` — confiança 2
- 🇵🇹 A Leonor fecha o livro devagar. "Vens por causa do Duarte. Eu sei."  *(linha 209)*
- 🇬🇧 Leonor closes her book slowly. "You are here about Duarte. I know."  *(linha 87)*
- Respostas:
  - "Perguntar se tem a certeza de que ele estava no grupo" / "Ask if she is sure he was in the group" → `sure`
  - "Dizer-lhe que tens dúvidas" / "Tell her you have doubts" → `soft`
  - "Dizer que ela está a mentir" / "Say she is lying" → `harsh` ⏳ **custa 5 minutos**
  - "Até já." / "Goodbye." → fim

### `sure` — confiança 2
- 🇵🇹 "Está em todas as mensagens há semanas. Tenho-as aqui." Toca no telemóvel.  *(linha 215)*
- 🇬🇧 "He has been in every message for weeks. I have them right here." She taps her phone.  *(linha 93)*
- Respostas:
  - "Pedir para ver as mensagens" / "Ask to see the messages" → `messages`

### `messages` — confiança 3
- 🇵🇹 "Olha. Todas de um número que eu não conhecia. Algumas têm data de há semanas, mas chegaram ontem à noite."  *(linha 217)*
- 🇬🇧 "Look. All from a number I did not know. Some are dated weeks ago, but they arrived last night."  *(linha 95)*
- 📓 Diário: A Leonor recebeu as mensagens do Duarte ontem à noite, de um número desconhecido. / Leonor received Duarte's messages last night, from an unknown number.
- Respostas:
  - "Até já." / "Goodbye." → fim

### `soft` — confiança 3
- 🇵🇹 "Eu queria acreditar em ti." Olha para o telemóvel. "Talvez devesse ver outra vez."  *(linha 220)*
- 🇬🇧 "I wanted to believe you." She looks at her phone. "Maybe I should look again."  *(linha 98)*
- Respostas:
  - "Pedir para ver as mensagens" / "Ask to see the messages" → `messages`

### `harsh` — confiança 1
- 🇵🇹 "Desculpa?" A voz dela endurece.  *(linha 222)*
- 🇬🇧 "Excuse me?" Her voice hardens.  *(linha 100)*
- Respostas:
  - "Pedir desculpa" / "Apologise" → `soft`
  - "Insistir" / "Insist" → `closed` ⏳ **custa 5 minutos**

### `closed` — confiança 0
- 🇵🇹 A Leonor levanta-se. "Volta com provas, não com acusações."  *(linha 225)*
- 🇬🇧 Leonor stands up. "Come back with proof, not accusations."  *(linha 103)*
- Respostas:
  - "Sair." / "Leave." → fim

### Ações feitas nesta conversa (em `story.py`)
- **▶ Mostrar a fotografia e pedir ajuda discretamente** / Show the photo and quietly ask for help (`ask_for_help`)
  - Se resultar 🇵🇹: A Leonor compara a fotografia com a do relatório e fica pálida. "Recebi estas mensagens todas ontem à noite, de um número que não conhecia. E algumas têm datas de há três semanas." Promete guardar as mensagens originais e ir ter contigo ao auditório.
  - Se resultar 🇬🇧: Leonor compares the photo with the one in the report and turns pale. "I got all these messages last night, from a number I did not know. And some of them are dated three weeks ago." She promises to keep the original messages and to meet you in the auditorium.
  - Se ainda não puderes 🇵🇹: A Leonor encolhe os ombros. "O Duarte esteve sempre no grupo, tenho aqui as mensagens. Tens alguma prova do contrário?"
  - Se ainda não puderes 🇬🇧: Leonor shrugs. "Duarte has always been in the group, I have the messages right here. Do you have any proof otherwise?"
- **▶ Mostrar a fotografia e acusá-la de ajudar o Duarte** / Show the photo and accuse her of helping Duarte (`accuse`)
  - Se resultar 🇵🇹: "Achas que eu fazia isso ao grupo?" A Leonor levanta-se, ofendida. "Então não preciso destas mensagens para nada." Apaga a conversa à tua frente e sai.
  - Se resultar 🇬🇧: "You think I would do that to the group?" Leonor stands up, offended. "Then you do not need these messages for anything." She deletes the conversation in front of you and leaves.
  - Se ainda não puderes 🇵🇹: A Leonor encolhe os ombros. "O Duarte esteve sempre no grupo, tenho aqui as mensagens. Tens alguma prova do contrário?"
  - Se ainda não puderes 🇬🇧: Leonor shrugs. "Duarte has always been in the group, I have the messages right here. Do you have any proof otherwise?"

## Tomás
Onde está: **Sala de informática** (`computer_lab`).

### `start` — confiança 2
- 🇵🇹 O Tomás está curvado sobre o computador 11, a evitar o teu olhar. "Ah. Olá. Já é tarde."  *(linha 228)*
- 🇬🇧 Tomás is hunched over computer 11, avoiding your eyes. "Oh. Hi. It is late."  *(linha 106)*
- Respostas:
  - "Perguntar com calma o que está ali a fazer" / "Ask kindly what he is doing here" → `kind`
  - "Exigir saber porque mentiu sobre o Duarte" / "Demand to know why he lied about Duarte" → `hard` ⏳ **custa 5 minutos**
  - "Mostrar-lhe a fotografia original" / "Show him the original photo" → `photo` *(só aparece se tens `original_photo`)*
  - "Até já." / "Goodbye." → fim

### `kind` — confiança 3
- 🇵🇹 "Não conseguia dormir. Vim acabar os slides. E... vi alguém no computador 12 ontem à noite, perto da meia-noite."  *(linha 234)*
- 🇬🇧 "Could not sleep. I came to finish the slides. And... I saw someone at computer 12 last night, near midnight."  *(linha 112)*
- Respostas:
  - "Perguntar quem era" / "Ask who it was" → `who`
  - "Perguntar a password do computador 12" / "Ask for the password of computer 12" → `password`
  - "Perguntar pela mensagem 5, a que tem o nome dele" / "Ask about message 5, the one with his name" → `msg5` *(só aparece se `files_viewed` = `True`)*

### `password` — confiança 3
- 🇵🇹 "A password do 12? É a do grupo: o dia e o mês em que tirámos a fotografia da capa. Quatro algarismos. Eu nunca me lembro da data."  *(linha 238)*
- 🇬🇧 "The password of computer 12? It is the group's: the day and the month we took the cover photo. Four digits. I can never remember the date."  *(linha 116)*
- 📓 Diário: Tomás: a password do computador 12 é o dia e o mês em que foi tirada a fotografia da capa (4 algarismos). / Tomás: the password of computer 12 is the day and month the cover photo was taken (4 digits).
- Respostas:
  - "Até já." / "Goodbye." → fim

### `who` — confiança 3
- 🇵🇹 "Só vi um capuz. Como o que o Duarte usa. Mas ninguém o viu chegar."  *(linha 240)*
- 🇬🇧 "Only a hood. Like the one Duarte wears. But nobody ever saw him arrive."  *(linha 118)*
- 📓 Diário: O Tomás viu alguém de capuz no computador 12 perto da meia-noite. / Tomás saw someone in a hood at computer 12 near midnight.
- Respostas:
  - "Até já." / "Goodbye." → fim

### `msg5` — confiança 3
- 🇵🇹 "'O Duarte fez os slides'? Eu nunca escrevi isso. O meu telemóvel apitou com ela à meia-noite, como se tivesse sido enviada há três semanas."  *(linha 243)*
- 🇬🇧 "'Duarte did the slides'? I never wrote that. My phone buzzed with it at midnight, as if it was sent three weeks ago."  *(linha 121)*
- 📓 Diário: O Tomás diz que nunca escreveu a mensagem 5; chegou ontem à noite. / Tomás says he never wrote message 5; it arrived last night.
- Respostas:
  - "Até já." / "Goodbye." → fim

### `hard` — confiança 1
- 🇵🇹 "Como? Eu não menti!" A voz dele treme.  *(linha 246)*
- 🇬🇧 "Excuse me? I did not lie!" His voice shakes.  *(linha 124)*
- Respostas:
  - "Pedir desculpa" / "Apologise" → `calm`
  - "Pressionar mais" / "Push harder" → `closed` ⏳ **custa 5 minutos**

### `calm` — confiança 2
- 🇵🇹 "Está bem. Foi uma noite longa. Pergunta com educação."  *(linha 249)*
- 🇬🇧 "Fine. It has been a long night. Ask properly."  *(linha 127)*
- Respostas:
  - "Perguntar com calma o que está ali a fazer" / "Ask kindly what he is doing here" → `kind`
  - "Até já." / "Goodbye." → fim

### `photo` — confiança 2
- 🇵🇹 O Tomás fica a olhar para a fotografia. "Quatro pessoas... nunca tinha reparado." Engole em seco.  *(linha 251)*
- 🇬🇧 Tomás stares at the photo. "Four people... I never noticed." He swallows.  *(linha 129)*
- Respostas:
  - "Pedir-lhe ajuda" / "Ask him to help you" → `help`

### `help` — confiança 3
- 🇵🇹 "Está bem. Vê o chat do grupo. Nem tudo o que lá está é meu."  *(linha 253)*
- 🇬🇧 "All right. Check the group chat. Not everything in there is mine."  *(linha 131)*
- 📓 Diário: O Tomás sugere que algumas mensagens do chat não são de quem diz. / Tomás hints that some chat messages are not from the people they name.
- Respostas:
  - "Até já." / "Goodbye." → fim

### `closed` — confiança 0
- 🇵🇹 O Tomás cruza os braços. "Ficamos por aqui."  *(linha 256)*
- 🇬🇧 Tomás crosses his arms. "We are done here."  *(linha 134)*
- Respostas:
  - "Sair." / "Leave." → fim

## Computador 12
Onde está: **Sala de informática** (`computer_lab`).

### `start`
- 🇵🇹 O computador 12 ainda está ligado, com a sessão do grupo aberta. Pede uma password de 4 algarismos.  *(linha 259)*
- 🇬🇧 Computer 12 is still on, with the group's session open. It asks for a 4-digit password.  *(linha 137)*
- Respostas:
  - "Afastar-me do computador." / "Step away from the computer." → fim

### Ações feitas nesta conversa (em `story.py`)
- **▶ Consultar os ficheiros antigos do projeto** / Look at the old project files (`view_files`)
  - Se resultar 🇵🇹: Ligas a pen ao computador 12 e comparas. Nas cópias de segurança da pen, todas as versões têm quatro autores. Na pasta partilhada, a versão atual foi alterada ontem às 23h47, a partir deste mesmo computador: alguém acrescentou "Duarte Sequeira" ao relatório e trocou a fotografia. Recuperas a versão original do trabalho.
  - Se resultar 🇬🇧: You plug the USB stick into computer 12 and compare. In the backups on the USB stick, every version has four authors. In the shared folder, the current version was changed yesterday at 11:47 pm, from this same computer: someone added "Duarte Sequeira" to the report and swapped the photo. You recover the original version of the work.
  - Se ainda não puderes 🇵🇹: A pasta partilhada só mostra a versão atual, já com cinco nomes. Precisas da cópia de segurança do grupo.
  - Se ainda não puderes 🇬🇧: The shared folder only shows the current version, already with five names. You need the group's backup copy.
- **▶ Abrir o chat do grupo no computador 12** / Open the group chat on computer 12 (`open_chat`)

## Professor
Onde está: **Auditório** (`auditorium`).

### `start`
- 🇵🇹 O professor levanta os olhos da lista de grupos. "É sobre as apresentações de amanhã?"  *(linha 262)*
- 🇬🇧 The professor looks up from the list of groups. "Is this about tomorrow's presentations?"  *(linha 140)*
- Respostas:
  - "Perguntar quantos elementos tem o teu grupo na lista" / "Ask how many members your group has on the list" → `list`
  - "Dizer que vais trazer provas" / "Say you will bring proof" → `proof`
  - "Até já." / "Goodbye." → fim

### `list`
- 🇵🇹 "Cinco, segundo a capa. Há algum problema?"  *(linha 267)*
- 🇬🇧 "Five, according to the cover. Is something wrong with that?"  *(linha 145)*
- Respostas:
  - "Dizer que vocês são só quatro" / "Say there are only four of you" → `evidence`

### `evidence`
- 🇵🇹 "Então preciso de provas, não de uma sensação. Traga-me o histórico do projeto."  *(linha 269)*
- 🇬🇧 "Then I need evidence, not a feeling. Bring me the history of the project."  *(linha 147)*
- 📓 Diário: O professor quer o histórico do projeto como prova. / The professor wants the project history as evidence.
- Respostas:
  - "Até já." / "Goodbye." → fim

### `proof`
- 🇵🇹 "Provas são bem-vindas. Apresente-as quando estiver pronto."  *(linha 272)*
- 🇬🇧 "Evidence is welcome. Present it when you are ready."  *(linha 150)*
- Respostas:
  - "Até já." / "Goodbye." → fim

### Ações feitas nesta conversa (em `story.py`)
- **▶ Apresentar as provas ao professor** / Present the evidence to the professor (`present_evidence`)
  - Acaba o jogo: o texto que aparece é o do final (em `story.py`, `endings`).

## Duarte
Onde está: **Auditório** (`auditorium`).

### `start` — confiança 3
- 🇵🇹 O Duarte sorri com calma. "Ah, o quarto elemento. Pronto para amanhã?"  *(linha 276)*
- 🇬🇧 Duarte smiles calmly. "Ah, the fourth wheel. Ready for tomorrow?"  *(linha 154)*
- Respostas:
  - "Perguntar que parte do projeto fez" / "Ask which part of the project he did" → `part`
  - "Dizer-lhe que sabes a verdade" / "Tell him you know the truth" → `know` ⏳ **custa 5 minutos**
  - "Até já." / "Goodbye." → fim

### `part` — confiança 3
- 🇵🇹 "Os slides, claro. Pergunta a qualquer um." Hesita por um segundo.  *(linha 281)*
- 🇬🇧 "The slides, of course. Ask anyone." He hesitates for a second.  *(linha 159)*
- Respostas:
  - "Perguntar que slide" / "Ask which slide" → `slide`

### `slide` — confiança 2
- 🇵🇹 "A... introdução. A bonita." O Duarte olha para a porta. "Porquê tantas perguntas?"  *(linha 283)*
- 🇬🇧 "The... intro. The nice one." Duarte glances at the door. "Why all these questions?"  *(linha 161)*
- 📓 Diário: O Duarte não soube dizer que slide fez. / Duarte could not say which slide he made.
- Respostas:
  - "Até já." / "Goodbye." → fim

### `know` — confiança 1
- 🇵🇹 "Que verdade? Cuidado com as acusações."  *(linha 286)*
- 🇬🇧 "Know what? Careful with accusations."  *(linha 164)*
- Respostas:
  - "Pressioná-lo" / "Press him" → `closed` ⏳ **custa 5 minutos**
  - "Recuar" / "Back off" → `start`

### `closed` — confiança 0
- 🇵🇹 O Duarte ri-se e vira-te as costas. A conversa acabou.  *(linha 289)*
- 🇬🇧 Duarte laughs and turns away. The conversation is over.  *(linha 167)*
- Respostas:
  - "Sair." / "Leave." → fim

## Procurar a pen e o código do computador 12 (em `prototypes/campus-3d/campus_search.py`)

No jogo 3D a pen já não se recebe da Rita: procura-se na sala de estudo, clicando nos objetos. O computador 12 pede um código antes de mostrar os ficheiros. As respostas estão em `campus_search.py`, que só o servidor lê (nunca vai para a página).

- **Onde está a pen:** `pizza` (Caixa de pizza).
- **Código do computador 12:** `1411`. As pistas estão nas falas `password` do Tomás e `order` da funcionária.
- 🇵🇹 Quando encontras a pen: Debaixo da última fatia de pizza fria está a pen do grupo, com as cópias de segurança do projeto. Guardas a pen.
- 🇬🇧 When you find it: Under the last cold slice of pizza lies the group's USB stick, with the project backups. You take the USB stick.
- O que há em cada sítio errado (cada clique errado custa 1 minuto):
  - **Gaveta do grupo** / Group drawer: A gaveta do grupo está vazia. Alguém tirou a pen daqui. / The group drawer is empty. Someone took the USB stick out of here.
  - **Casaco na cadeira** / Coat on the chair: Só um casaco esquecido. Os bolsos estão vazios. / Just a forgotten coat. The pockets are empty.
  - **Caneca** / Mug: Café frio. Nada lá dentro. / Cold coffee. Nothing inside.
  - **Mochila** / Backpack: Cadernos e um carregador de telemóvel. Nada de pen. / Notebooks and a phone charger. No USB stick.
  - **Pilha de livros** / Pile of books: Livros de finanças, cheios de páginas sublinhadas. / Finance books, full of underlined pages.
  - **Papéis espalhados** / Scattered papers: Rascunhos do relatório. Nada escondido entre eles. / Drafts of the report. Nothing hidden between them.
  - **Caixote do lixo** / Bin: Papéis amarrotados e uma lata vazia. / Crumpled paper and an empty can.
  - **Vaso** / Plant pot: Só terra e algumas folhas secas. / Only soil and a few dry leaves.

Nota: as ações "Abrir a gaveta do grupo" (Rita) e "Ver os ficheiros antigos" (computador 12) continuam em `story.py`, mas o jogo 3D não as mostra: usa a procura e o código.

