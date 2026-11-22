# Guião das conversas — O quinto elemento (jogo 3D)

Tudo o que as pessoas dizem no jogo 3D, em português e em inglês, tal como está no código.

> **Gerado em 22/11/2026 a partir de `prototypes/campus-3d/campus_people.py`, `prototypes/campus-3d/campus_case.py` e `story.py`.** O código é que manda: se mudares uma fala no código, este guião fica desatualizado até ser gerado outra vez.

## Como alterar uma fala

1. **Conversas** (o que cada pessoa diz quando falas com ela): `prototypes/campus-3d/campus_people.py`, dentro de `PEOPLE`. Há um bloco `"en"` (inglês) e um bloco `"pt"` (português). Ao lado de cada fala deste guião está o número da linha.
2. **Respostas às ações** (o que acontece quando escolhes ▶ abrir a gaveta, pedir a cópia, etc.): `story.py`, em `result_text` (quando resulta) e `blocked_text` (quando ainda não podes).
3. **Provas, confrontos e audiência** (o que as pessoas respondem quando lhes mostras uma prova, e as três afirmações do Duarte): `prototypes/campus-3d/campus_case.py`. Só o servidor lê este ficheiro: nada do que lá está pode ir para `campus_text.py`.
4. **O que vai para o balão:** só o que está **entre aspas** (`\"...\"` no código) aparece no balão e é lido pela voz. O resto aparece como narração, em itálico, fora dos balões. Exemplo: `Rita looks up from her laptop. \"You look awful.\"`: "Rita looks up from her laptop." é narração, e "You look awful." vai para o balão.
5. **Regras para não estragar nada** (os testes verificam-nas):
   - Muda só o texto entre as aspas de `"text"`, `"label"` e `"note"`. Não mudes os identificadores (`"start"`, `"photo"`, `"next": ...`, `"if": ...`, `"trust"`).
   - Se mudares uma fala em português, muda também a inglesa (e vice-versa). As duas línguas têm de ter as mesmas falas, respostas e condições: só o texto muda.
   - Dentro do texto, as aspas da fala escrevem-se `\"` (barra e aspas).
   - As falas nunca podem dizer quais são as mensagens falsas ("message 2", "mensagem 4"…).
6. Depois de mudar, corre `uv run pytest`. Se ficar verde, recarrega o jogo (no endereço que o Streamlit mostra ao arrancar; por omissão http://localhost:8501).

**Legenda:** ⏳ *custa N minutos* é uma resposta agressiva: tira esses minutos à contagem decrescente (para mudar, altera `"cost": 5` no código). 📁 *prova* é uma carta que podes mostrar numa conversa ("Mostrar uma prova"): a certa, na fala certa, faz a pessoa ceder; qualquer outra custa 2 minutos (com o Duarte, 1). *Confiança* são os corações (0 a 3; com 0 a pessoa acaba a conversa). *Diário* é a nota que fica guardada no diário do telemóvel. "→ fim" acaba a conversa: no jogo 3D estas respostas não aparecem (usa-se o botão "Terminar conversa"), mas têm de existir no código, porque cada fala precisa de pelo menos uma resposta. Uma pergunta já feita na mesma conversa não volta a aparecer.

## Rita
Onde está: **Sala de estudo** (`study_room`).

### `start`
- 🇵🇹 A Rita levanta os olhos do portátil. "Estás com um ar péssimo. Dormiste alguma coisa?"  *(linha 188)*
- 🇬🇧 Rita looks up from her laptop. "You look awful. Did you sleep at all?"  *(linha 50)*
- Respostas:
  - "Perguntar pela fotografia do grupo" / "Ask about the group photo" → `photo`
  - "Perguntar o que ela se lembra do Duarte" / "Ask what she remembers about Duarte" → `duarte`
  - "Perguntar onde está a pen" / "Ask where the USB stick is" → `pen`
  - "Perguntar pelas mensagens do chat" / "Ask about the chat messages" → `chat` *(só aparece se `files_viewed` = `True`)*
  - "Até já." / "Goodbye." → fim

### `photo`
- 🇵🇹 "A fotografia? Tirámo-la depois da última reunião. Quatro pessoas, a Leonor ficou com o temporizador. Lembro-me de contar as cabeças."  *(linha 195)*
- 🇬🇧 "The photo? We took it after the last meeting. Four of us, Leonor held the timer. I remember counting heads."  *(linha 57)*
- 📓 Diário: A Rita lembra-se de quatro pessoas na fotografia do grupo. / Rita remembers four people in the group photo.
- Respostas:
  - "Perguntar porque é que a fotografia da pasta mostra cinco" / "Ask why the photo in the folder shows five" → `five`
  - "Até já." / "Goodbye." → fim

### `five` — 📁 cede com `files` ou `original_photo`
- 🇵🇹 "Então contei mal." A Rita vira o portátil para ti: cinco pessoas. "Uma fotografia não muda. A minha memória muda. Ele devia estar mesmo ali."  *(linha 199)*
- 🇬🇧 "Then I counted wrong." Rita turns the laptop towards you: five people. "A photo cannot change. My memory can. He must have been standing right there."  *(linha 62)*
- Respostas:
  - "Até já." / "Goodbye." → fim

### `pen`
- 🇵🇹 "A pen? Devia estar na gaveta do grupo, mas não está." Olha para a mesa. "Ontem ficámos aqui até tarde a comer pizza. Com esta confusão, pode estar em qualquer lado."  *(linha 201)*
- 🇬🇧 "The USB stick? It should be in the group drawer, but it is not." She looks at the table. "We stayed here late last night eating pizza. With this mess, it could be anywhere."  *(linha 64)*
- 📓 Diário: Rita: a pen não está na gaveta. O grupo comeu pizza aqui ontem à noite. / Rita: the USB stick is not in the drawer. The group ate pizza here last night.
- Respostas:
  - "Até já." / "Goodbye." → fim

### `duarte`
- 🇵🇹 "O Duarte... sinceramente, não o consigo imaginar. Sempre que tento, só vejo o nome na capa."  *(linha 203)*
- 🇬🇧 "Duarte... honestly, I cannot picture him. Every time I try, I only see the name on the cover."  *(linha 66)*
- Respostas:
  - "Dizer que achas que o nome foi acrescentado ontem à noite" / "Say you think the name was added last night" → `warned`

### `warned`
- 🇵🇹 A Rita fica calada. "Se for verdade, alguém quis que duvidássemos de nós próprios."  *(linha 205)*
- 🇬🇧 Rita goes quiet. "If that is true, somebody wanted us to doubt ourselves."  *(linha 68)*
- 📓 Diário: A Rita também desconfia do quinto nome. / Rita doubts the fifth name too.
- Respostas:
  - "Até já." / "Goodbye." → fim

### `chat`
- 🇵🇹 "Repara na hora a que as mensagens chegam. Algumas dizem há três semanas, mas no meu telemóvel aparecem como novas, de ontem à noite. Mensagens antigas não funcionam assim."  *(linha 208)*
- 🇬🇧 "Look at when the messages arrive. Some say three weeks ago, but my phone shows them as new, last night. That is not how old messages work."  *(linha 71)*
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
- 🇵🇹 A funcionária ajeita os óculos. "Fechamos daqui a dez minutos. Do que precisas?"  *(linha 213)*
- 🇬🇧 The clerk adjusts her glasses. "We close in ten minutes. What do you need?"  *(linha 76)*
- Respostas:
  - "Perguntar pelo pedido da fotografia da capa" / "Ask about the cover photo order" → `order`
  - "Perguntar se mais alguém veio perguntar" / "Ask if anyone else came asking" → `visitor`
  - "Até já." / "Goodbye." → fim

### `order`
- 🇵🇹 "A 14 de novembro, na semana passada. Tiraram a fotografia e mandaram-na imprimir no mesmo dia. Quatro pessoas, lembro-me porque tive de cortar a impressão. O ficheiro original do pedido ainda está guardado."  *(linha 218)*
- 🇬🇧 "On 14 November, last week. You took the photo and had it printed the same day. Four people in it, I remember because I had to crop the print. The original order file is still saved."  *(linha 81)*
- 📓 Diário: A fotografia da capa foi tirada e impressa a 14 de novembro. A reprografia ainda tem o ficheiro original do pedido. / The cover photo was taken and printed on 14 November. The print shop still has the original order file.
- Respostas:
  - "Até já." / "Goodbye." → fim

### `visitor`
- 🇵🇹 "Ontem ao fim da tarde passou por aqui um rapaz de capuz. Pediu para reimprimir a capa com outra fotografia."  *(linha 221)*
- 🇬🇧 "A young man in a hood came by yesterday evening. He asked to reprint the cover with a different photo."  *(linha 84)*
- 📓 Diário: Um desconhecido de capuz pediu à reprografia para mudar a fotografia da capa. / A hooded stranger asked the print shop to change the cover photo.
- Respostas:
  - "Perguntar como era ele" / "Ask what he looked like" → `hood`

### `hood`
- 🇵🇹 "Um sorriso calmo. Não quis deixar o nome. Pensei que fosse do vosso grupo."  *(linha 224)*
- 🇬🇧 "A calm smile. He did not want to leave a name. I thought he was one of your group."  *(linha 87)*
- Respostas:
  - "Até já." / "Goodbye." → fim

### Ações feitas nesta conversa (em `story.py`)
- **▶ Pedir uma cópia do pedido original** / Ask for a copy of the original order (`request_copy`)
  - Se resultar 🇵🇹: A funcionária volta a imprimir o ficheiro que ficou guardado no pedido. Na fotografia original estão quatro pessoas. Guardas a fotografia.
  - Se resultar 🇬🇧: The clerk prints again the file that was saved with the order. The original photo shows four people. You take the photo.

## Leonor
Onde está: **Biblioteca** (`library`).

### `start` — confiança 2
- 🇵🇹 A Leonor fecha o livro devagar. "Vens por causa do Duarte. Eu sei."  *(linha 228)*
- 🇬🇧 Leonor closes her book slowly. "You are here about Duarte. I know."  *(linha 91)*
- Respostas:
  - "Perguntar se tem a certeza de que ele estava no grupo" / "Ask if she is sure he was in the group" → `sure`
  - "Dizer-lhe que tens dúvidas" / "Tell her you have doubts" → `soft`
  - "Perguntar que mensagem do chat é mesmo dela" / "Ask which chat message is really hers" → `mine` *(só aparece se `colleague_choice` = `help`)*
  - "Dizer que ela está a mentir" / "Say she is lying" → `harsh` ⏳ **custa 5 minutos**
  - "Até já." / "Goodbye." → fim

### `sure` — confiança 2 — 📁 cede com `tomas_word`
- 🇵🇹 "Está em todas as mensagens há semanas. Tenho-as aqui." Toca no telemóvel.  *(linha 235)*
- 🇬🇧 "He has been in every message for weeks. I have them right here." She taps her phone.  *(linha 99)*
- Respostas:
  - "Pedir para ver as mensagens" / "Ask to see the messages" → `messages`

### `messages` — confiança 3
- 🇵🇹 "Olha. Todas de um número que eu não conhecia. Algumas têm data de há semanas, mas chegaram ontem à noite."  *(linha 240)*
- 🇬🇧 "Look. All from a number I did not know. Some are dated weeks ago, but they arrived last night."  *(linha 105)*
- 📓 Diário: A Leonor recebeu as mensagens do Duarte ontem à noite, de um número desconhecido. / Leonor received Duarte's messages last night, from an unknown number.
- Respostas:
  - "Até já." / "Goodbye." → fim

### `mine` — confiança 3
- 🇵🇹 "A que pede para reservar a sala de estudo. Escrevi-a nesta mesa, há três semanas." A Leonor percorre o ecrã com um dedo. "As do número que eu não conhecia chegaram todas com minutos de diferença, ontem à noite."  *(linha 237)*
- 🇬🇧 "The one asking to book the study room. I wrote that at this table, three weeks ago." Leonor scrolls with one finger. "The ones from the number I did not know all arrived within minutes of each other, last night."  *(linha 102)*
- 📓 Diário: A Leonor escreveu ela própria a mensagem do chat sobre reservar a sala de estudo. / Leonor wrote the chat message about booking the study room herself.
- Respostas:
  - "Até já." / "Goodbye." → fim

### `soft` — confiança 3
- 🇵🇹 "Eu queria acreditar em ti." Olha para o telemóvel. "Talvez devesse ver outra vez."  *(linha 243)*
- 🇬🇧 "I wanted to believe you." She looks at her phone. "Maybe I should look again."  *(linha 108)*
- Respostas:
  - "Pedir para ver as mensagens" / "Ask to see the messages" → `messages`

### `harsh` — confiança 1
- 🇵🇹 "Desculpa?" A voz dela endurece.  *(linha 245)*
- 🇬🇧 "Excuse me?" Her voice hardens.  *(linha 110)*
- Respostas:
  - "Pedir desculpa" / "Apologise" → `soft`
  - "Insistir" / "Insist" → `closed` ⏳ **custa 5 minutos**

### `closed` — confiança 0
- 🇵🇹 A Leonor levanta-se. "Volta com provas, não com acusações."  *(linha 248)*
- 🇬🇧 Leonor stands up. "Come back with proof, not accusations."  *(linha 113)*
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
- 🇵🇹 O Tomás está curvado sobre o computador 11, a evitar o teu olhar. "Ah. Olá. Já é tarde."  *(linha 251)*
- 🇬🇧 Tomás is hunched over computer 11, avoiding your eyes. "Oh. Hi. It is late."  *(linha 116)*
- Respostas:
  - "Perguntar com calma o que está ali a fazer" / "Ask kindly what he is doing here" → `kind`
  - "Exigir saber porque mentiu sobre o Duarte" / "Demand to know why he lied about Duarte" → `hard` ⏳ **custa 5 minutos**
  - "Mostrar-lhe a fotografia original" / "Show him the original photo" → `photo` *(só aparece se tens `original_photo`)*
  - "Até já." / "Goodbye." → fim

### `kind` — confiança 3
- 🇵🇹 "Não conseguia dormir. Vim acabar os slides. E... vi alguém no computador 12 ontem à noite, perto da meia-noite."  *(linha 257)*
- 🇬🇧 "Could not sleep. I came to finish the slides. And... I saw someone at computer 12 last night, near midnight."  *(linha 122)*
- Respostas:
  - "Perguntar quem era" / "Ask who it was" → `who`
  - "Perguntar a password do computador 12" / "Ask for the password of computer 12" → `password`
  - "Perguntar pela mensagem 5, a que tem o nome dele" / "Ask about message 5, the one with his name" → `msg5` *(só aparece se `files_viewed` = `True`)*
  - "Perguntar quem fez os slides" / "Ask who made the slides" → `slides` *(só aparece se `files_viewed` = `True`)*

### `password` — confiança 3
- 🇵🇹 "A password do 12? É a do grupo: o dia e o mês em que tirámos a fotografia da capa. Quatro algarismos. Eu nunca me lembro da data."  *(linha 262)*
- 🇬🇧 "The password of computer 12? It is the group's: the day and the month we took the cover photo. Four digits. I can never remember the date."  *(linha 127)*
- 📓 Diário: Tomás: a password do computador 12 é o dia e o mês em que foi tirada a fotografia da capa (4 algarismos). / Tomás: the password of computer 12 is the day and month the cover photo was taken (4 digits).
- Respostas:
  - "Até já." / "Goodbye." → fim

### `who` — confiança 3
- 🇵🇹 "Só vi um capuz. Como o que o Duarte usa. Mas ninguém o viu chegar."  *(linha 264)*
- 🇬🇧 "Only a hood. Like the one Duarte wears. But nobody ever saw him arrive."  *(linha 129)*
- 📓 Diário: O Tomás viu alguém de capuz no computador 12 perto da meia-noite. / Tomás saw someone in a hood at computer 12 near midnight.
- Respostas:
  - "Até já." / "Goodbye." → fim

### `msg5` — confiança 3
- 🇵🇹 "'Os slides foram do Duarte'? Está com o meu nome, mas não me lembro de a ter escrito. O meu telemóvel apitou com ela ontem à noite, perto da meia-noite, como se tivesse sido enviada há três semanas."  *(linha 267)*
- 🇬🇧 "'Duarte did the slides'? It is under my name, but I do not remember writing it. My phone buzzed with it last night, near midnight, as if it had been sent three weeks ago."  *(linha 133)*
- 📓 Diário: O Tomás não se lembra de ter escrito a mensagem 5; chegou-lhe ao telemóvel ontem à noite. / Tomás does not remember writing message 5; it reached his phone last night.
- Respostas:
  - "Até já." / "Goodbye." → fim

### `slides` — confiança 2 — 📁 cede com `msg_5`
- 🇵🇹 O Tomás não tira os olhos do ecrã. "Os slides? Estou a acabá-los. Mas o chat diz que foram do Duarte, com o meu nome. Se calhar foram mesmo, e eu só arrumei."  *(linha 270)*
- 🇬🇧 Tomás keeps his eyes on the screen. "The slides? I am finishing them. But the chat says Duarte did them, under my name. So maybe he did, and I only tidied up."  *(linha 137)*
- 📓 Diário: O Tomás acha que os slides podem ter sido do Duarte, só porque uma mensagem do chat com o nome dele o diz. / Tomás thinks Duarte may have made the slides, only because a chat message under his own name says so.
- Respostas:
  - "Até já." / "Goodbye." → fim

### `hard` — confiança 1
- 🇵🇹 "Como? Eu não menti!" A voz dele treme.  *(linha 273)*
- 🇬🇧 "Excuse me? I did not lie!" His voice shakes.  *(linha 140)*
- Respostas:
  - "Pedir desculpa" / "Apologise" → `calm`
  - "Pressionar mais" / "Push harder" → `closed` ⏳ **custa 5 minutos**

### `calm` — confiança 2
- 🇵🇹 "Está bem. Foi uma noite longa. Pergunta com educação."  *(linha 276)*
- 🇬🇧 "Fine. It has been a long night. Ask properly."  *(linha 143)*
- Respostas:
  - "Perguntar com calma o que está ali a fazer" / "Ask kindly what he is doing here" → `kind`
  - "Até já." / "Goodbye." → fim

### `photo` — confiança 2
- 🇵🇹 O Tomás fica a olhar para a fotografia. "Quatro pessoas... nunca tinha reparado." Engole em seco.  *(linha 278)*
- 🇬🇧 Tomás stares at the photo. "Four people... I never noticed." He swallows.  *(linha 145)*
- Respostas:
  - "Pedir-lhe ajuda" / "Ask him to help you" → `help`

### `help` — confiança 3
- 🇵🇹 "Está bem. Vê o chat do grupo. Nem tudo o que lá está é meu."  *(linha 280)*
- 🇬🇧 "All right. Check the group chat. Not everything in there is mine."  *(linha 147)*
- 📓 Diário: O Tomás sugere que algumas mensagens do chat não são de quem diz. / Tomás hints that some chat messages are not from the people they name.
- Respostas:
  - "Até já." / "Goodbye." → fim

### `closed` — confiança 0
- 🇵🇹 O Tomás cruza os braços. "Ficamos por aqui."  *(linha 283)*
- 🇬🇧 Tomás crosses his arms. "We are done here."  *(linha 150)*
- Respostas:
  - "Sair." / "Leave." → fim

## Computador 12
Onde está: **Sala de informática** (`computer_lab`).

### `start`
- 🇵🇹 O computador 12 ainda está ligado, com a sessão do grupo aberta. Pede uma password de 4 algarismos.  *(linha 286)*
- 🇬🇧 Computer 12 is still on, with the group's session open. It asks for a 4-digit password.  *(linha 153)*
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
- 🇵🇹 O professor levanta os olhos da lista de grupos. "É sobre as apresentações de amanhã?"  *(linha 289)*
- 🇬🇧 The professor looks up from the list of groups. "Is this about tomorrow's presentations?"  *(linha 156)*
- Respostas:
  - "Perguntar quantos elementos tem o teu grupo na lista" / "Ask how many members your group has on the list" → `list`
  - "Dizer que vais trazer provas" / "Say you will bring proof" → `proof`
  - "Até já." / "Goodbye." → fim

### `list`
- 🇵🇹 "Cinco, segundo a capa. Há algum problema?"  *(linha 294)*
- 🇬🇧 "Five, according to the cover. Is something wrong with that?"  *(linha 161)*
- Respostas:
  - "Dizer que vocês são só quatro" / "Say there are only four of you" → `evidence`

### `evidence`
- 🇵🇹 "Então preciso de provas, não de uma sensação. Traga-me o histórico do projeto."  *(linha 296)*
- 🇬🇧 "Then I need evidence, not a feeling. Bring me the history of the project."  *(linha 163)*
- 📓 Diário: O professor quer o histórico do projeto como prova. / The professor wants the project history as evidence.
- Respostas:
  - "Até já." / "Goodbye." → fim

### `proof`
- 🇵🇹 "Provas são bem-vindas. Apresente-as quando estiver pronto."  *(linha 299)*
- 🇬🇧 "Evidence is welcome. Present it when you are ready."  *(linha 166)*
- Respostas:
  - "Até já." / "Goodbye." → fim

### Ações feitas nesta conversa (em `story.py`)
- **▶ Apresentar as provas ao professor** / Present the evidence to the professor (`present_evidence`)
  - No jogo 3D este botão abre a audiência (as três afirmações do Duarte, em `campus_case.py`); só depois da terceira resposta o jogo acaba. O servidor continua a aceitar a ação direta.

## Duarte
Onde está: **Auditório** (`auditorium`).

### `start` — confiança 3
- 🇵🇹 O Duarte sorri com calma. "Ah, o quarto elemento. Pronto para amanhã?"  *(linha 303)*
- 🇬🇧 Duarte smiles calmly. "Ah, the fourth wheel. Ready for tomorrow?"  *(linha 170)*
- Respostas:
  - "Perguntar que parte do projeto fez" / "Ask which part of the project he did" → `part`
  - "Dizer-lhe que sabes a verdade" / "Tell him you know the truth" → `know` ⏳ **custa 5 minutos**
  - "Até já." / "Goodbye." → fim

### `part` — confiança 3
- 🇵🇹 "Os slides, claro. Pergunta a qualquer um." Hesita por um segundo.  *(linha 308)*
- 🇬🇧 "The slides, of course. Ask anyone." He hesitates for a second.  *(linha 175)*
- Respostas:
  - "Perguntar que slide" / "Ask which slide" → `slide`

### `slide` — confiança 2
- 🇵🇹 "A... introdução. A bonita." O Duarte olha para a porta. "Porquê tantas perguntas?"  *(linha 310)*
- 🇬🇧 "The... intro. The nice one." Duarte glances at the door. "Why all these questions?"  *(linha 177)*
- 📓 Diário: O Duarte não soube dizer que slide fez. / Duarte could not say which slide he made.
- Respostas:
  - "Até já." / "Goodbye." → fim

### `know` — confiança 1
- 🇵🇹 "Que verdade? Cuidado com as acusações."  *(linha 313)*
- 🇬🇧 "Know what? Careful with accusations."  *(linha 180)*
- Respostas:
  - "Pressioná-lo" / "Press him" → `closed` ⏳ **custa 5 minutos**
  - "Recuar" / "Back off" → `start`

### `closed` — confiança 0
- 🇵🇹 O Duarte ri-se e vira-te as costas. A conversa acabou.  *(linha 316)*
- 🇬🇧 Duarte laughs and turns away. The conversation is over.  *(linha 183)*
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

## Provas, confrontos e audiência (em `prototypes/campus-3d/campus_case.py`)

Só o servidor lê este ficheiro. A página recebe uma carta quando a tens, e uma fala quando a mereceste.

### As provas (cartas)
| id | quando a tens | 🇵🇹 | 🇬🇧 |
|---|---|---|---|
| `original_photo` | tens o objeto `original_photo` | O pedido original da fotografia: quatro pessoas | The original photo order: four people |
| `files` | `files_viewed` = `True` | O histórico dos ficheiros: quatro autores em todas as cópias | The file history: four authors in every backup |
| `leonor_messages` | `colleague_choice` = `help` | As capturas de ecrã da Leonor: chegaram todas ontem à noite | Leonor's screenshots: every message arrived last night |
| `msg_1` … `msg_5` | `flagged_n` = `True` | 🚩 e o texto dessa mensagem do chat, lido de `story.py` | 🚩 and the text of that chat message, read from `story.py` |
| `tomas_word` | o Tomás cedeu esta noite (notas da noite) | A palavra do Tomás: nunca escreveu aquela mensagem e foi ele que fez os slides | Tomás's word: he never wrote that message and made the slides himself |
| `rita_word` | a Rita cedeu esta noite (notas da noite) | A palavra da Rita: contou quatro pessoas no dia da fotografia | Rita's word: she counted four people on the day of the photo |

### Quem cede, e com que prova
| pessoa | fala | provas que a fazem ceder | carta que ganhas |
|---|---|---|---|
| Tomás | `slides` | `msg_5` | `tomas_word` |
| Rita | `five` | `files`, `original_photo` | `rita_word` |
| Leonor | `sure` | `tomas_word` | nenhuma |

### Quando cedem (a prova certa na fala certa)
**Tomás** — confiança 3
- 🇵🇹 O Tomás lê a linha por baixo do nome dele e depois a linha cinzenta mais pequena. "Chegou ontem às 23h49. Às 23h49 eu estava aqui sentado, no computador ao lado do rapaz de capuz. Não escrevi uma palavra." Baixa a voz. "Eu nunca enviei isto. E os slides... fui eu que fiz os slides. Os onze. Fiquei aqui até às duas na terça-feira." Roda a cadeira para a parede de vidro. "Ele anda pelo corredor, sabes. Volta para o computador. Se ele vier, eu fico à porta."
- 🇬🇧 Tomás reads the line under his name, then the small grey line beneath it. "Arrived yesterday, 11:49 pm. At 11:49 I was sitting right here, one computer away from the one in the hood. I did not type a word." His voice drops. "I never sent that. And the slides... I made the slides. All eleven. I was here until two on Tuesday." He turns his chair to face the glass wall. "He walks the corridor, you know. Go back to the computer. If he comes, I will be standing in the door."
- 📓 Diário: O Tomás nunca escreveu a mensagem sobre os slides: foi ele que os fez e vai dizê-lo. Fica a vigiar o corredor por ti. / Tomás never wrote the message about the slides: he made them himself and will say so. He is watching the corridor for you.

**Rita** — sem confiança (não tem corações)
- 🇵🇹 A Rita olha da tua prova para o ecrã e outra vez para a prova. "Então a fotografia mudou mesmo." Ri-se uma vez, sem alegria nenhuma. "Eu contei quatro. Disse-o em voz alta. Até o escrevi no chat: os quatro, finalmente. Essa é minha, lembro-me de a escrever." Fecha o portátil. "Diz ao professor que eu contei. Eu digo-lho na cara."
- 🇬🇧 Rita looks from your proof to her screen and back. "So the photo did change." She laughs once, without any joy. "I counted four. I said it out loud. I even wrote it in the chat: four of us, finally. That one is mine, I remember typing it." She closes the laptop. "Tell the professor I counted. I will say it to his face."
- 📓 Diário: A Rita contou quatro pessoas no dia da fotografia. A mensagem do chat que fala nos quatro é dela. Vai dizê-lo ao professor. / Rita counted four people on the day of the photo. The chat message that says four of them is hers. She will tell the professor.

**Leonor** — confiança 3, sem carta
- 🇵🇹 Contas-lhe o que o Tomás disse sobre a mensagem com o nome dele. A Leonor fica com o polegar parado no ecrã. "Ele nunca a escreveu?" Volta atrás na conversa, mais devagar. "Então já não sei o que é que andei a ler."
- 🇬🇧 You tell her what Tomás said about the message with his name. Leonor stops with her thumb on the screen. "He never wrote it?" She scrolls back, slower this time. "Then I do not know what I have been reading."
- 📓 Diário: A Leonor não sabia que o Tomás nunca escreveu a mensagem com o nome dele. Ficou abalada. / Leonor did not know that Tomás never wrote the message with his name. It shook her.

### Qualquer outra prova, ou outra fala (custa 2 minutos; com o Duarte, 1)
- **Tomás** 🇵🇹 O Tomás olha de relance e volta ao ecrã. "E o que é que isso tem a ver com o que eu acabei de dizer?" / 🇬🇧 Tomás glances at it and back at his screen. "And what does that have to do with what I just said?"
- **Rita** 🇵🇹 A Rita olha para aquilo e volta ao portátil. "E então? Não vejo o que é que isso muda." / 🇬🇧 Rita looks at it, then back at her laptop. "And? I do not see what that changes."
- **Leonor** 🇵🇹 A Leonor olha para o que tens na mão e depois para ti. "Se me queres mostrar alguma coisa, diz o que queres de mim." / 🇬🇧 Leonor looks at what you are holding, then at you. "If you want to show me something, say what you want from me."
- **Funcionária** 🇵🇹 A funcionária olha por cima dos óculos. "Eu imprimo coisas. Não as julgo. Precisas de alguma coisa impressa?" / 🇬🇧 The clerk looks over her glasses. "I print things. I do not judge them. Is there anything you need printed?"
- **Professor** 🇵🇹 O professor não lhe pega. "Assim não. Apresente as provas como deve ser, quando estiver pronto." / 🇬🇧 The professor does not take it. "Not like this. Present your evidence properly, when you are ready."
- **Duarte** (qualquer prova, em qualquer fala; 1 minuto) 🇵🇹 O Duarte nem olha. "Guarda isso para o professor. Eu vou estar na primeira fila." / 🇬🇧 Duarte does not look at it. "Keep it for the professor. I will be sitting in the front row."

### A audiência: as três afirmações do Duarte
Uma resposta por afirmação, sem segunda tentativa. Uma prova que não a desfaz, ou "Não dizer nada", é uma dúvida (um coração a menos na confiança do professor).

**1. `name`** (fala o Duarte) — desfaz-se com `files`
- 🇵🇹 O Duarte levanta-se sem pressa. "Professor, abra o relatório. O meu nome está na capa. Está lá desde o primeiro rascunho."
- 🇬🇧 Duarte stands up without hurry. "Professor, open the report. My name is on the cover. It has been there since the first draft."
- Certa, `files` (professor): 🇵🇹 "Quatro autores em todas as cópias, e um quinto nome acrescentado ontem às 23h47. Continue." / 🇬🇧 "Four authors in every backup, and a fifth name added last night at 11:47 pm. Go on."
- Errada, qualquer outra (professor): 🇵🇹 "Isso não me diz quem escreveu um relatório." Faz um pequeno sinal na lista. / 🇬🇧 "That does not tell me who wrote a report." He makes a small mark on the list.

**2. `photo`** (fala o Duarte) — desfaz-se com `original_photo` ou `rita_word`
- 🇵🇹 "Então olhe para a fotografia. Cinco pessoas, e eu sou o da direita, de casaco comprido. Uma máquina fotográfica não acrescenta ninguém."
- 🇬🇧 "Then look at the photograph. Five people, and I am the one on the right, in the long coat. A camera does not add anyone."
- Certa, `original_photo` (professor): 🇵🇹 O professor põe as duas impressões lado a lado. "O ficheiro da própria reprografia. Quatro pessoas, uma semana antes das suas cinco." / 🇬🇧 The professor holds the two prints side by side. "The print shop's own file. Four people, a week before your five."
- Certa, `rita_word` (professor): 🇵🇹 "Uma testemunha que contou. Ouço-a amanhã; esta noite, acredito nela." / 🇬🇧 "A witness who counted. I will hear her tomorrow; tonight I believe her."
- Errada, `files` (professor): 🇵🇹 "O histórico diz que uma fotografia foi trocada. Não me mostra a que lá estava antes." / 🇬🇧 "The history says a photo was swapped. It does not show me the one that was there before."
- Errada, qualquer outra (professor): 🇵🇹 "Isso não me diz nada sobre quem está numa fotografia." Faz um sinal na lista. / 🇬🇧 "That tells me nothing about who is in a photograph." He makes a mark on the list.

**3. `messages`** (fala o Duarte) — desfaz-se com `leonor_messages` ou `tomas_word`
- 🇵🇹 O Duarte levanta o telemóvel. "E as mensagens? Semanas delas. O próprio Tomás escreveu: 'Os slides foram do Duarte, claro.' O Tomás também é mentiroso?"
- 🇬🇧 Duarte raises his phone. "And the messages? Weeks of them. Tomás wrote it himself: 'Duarte did the slides, obviously.' Is Tomás a liar too?"
- Certa, `leonor_messages` (professor): 🇵🇹 "Todas entregues na mesma noite, de um número que ninguém conhecia. Uma data escreve-se. A hora de chegada, não." / 🇬🇧 "Every one delivered on the same night, from a number nobody knew. A date can be typed. An arrival time cannot."
- Certa, `tomas_word` (professor): 🇵🇹 "Então quem a assina nunca a enviou. Essa fica respondida." / 🇬🇧 "Then the person whose name is on it never sent it. That answers this one."
- Errada, uma mensagem marcada `msg_1` … `msg_5` (professor): 🇵🇹 "Marcou-a. Essa é a sua opinião sobre ela. Quem me vem aqui dizer que nunca a escreveu?" / 🇬🇧 "You flagged it. That is your opinion of it. Who will stand here and tell me they never wrote it?"
- Errada, qualquer outra (professor): 🇵🇹 "Isso não me diz quem enviou uma mensagem." Faz um sinal na lista. / 🇬🇧 "That does not tell me who sent a message." He makes a mark on the list.

**"Não dizer nada"** / "Say nothing" (`concede`, em qualquer afirmação; fala o Duarte; é sempre uma dúvida)
- 🇵🇹 O professor espera. O Duarte sorri. "Nada?"
- 🇬🇧 The professor waits. Duarte smiles. "Nothing?"

A resposta à terceira afirmação aparece no cartão do final, por cima do veredicto.

### O veredicto do professor (por cima do texto do final)
| chave | quando | 🇵🇹 | 🇬🇧 |
|---|---|---|---|
| `three` | 3 dúvidas, sem a Leonor a ajudar (mostra `stolen_credits`) | "Três vezes esta noite me deu razões para duvidar de si. Não risco um nome por um palpite." | "Three times tonight you gave me a reason to doubt you. I cannot cross out a name on a guess." |
| `three_help` | 3 dúvidas com `colleague_choice` = `help` (mostra `stolen_credits`) | O professor fecha a lista antes de a Leonor chegar à porta. "Já ouvi palpites que cheguem por uma noite." | The professor closes the list before Leonor reaches the door. "I have heard enough guesses for one night." |
| `two` | 2 dúvidas e o final da história é `full_case` (mostra `impostor`) | "Acho que tem razão sobre ele. Mas fez-me duvidar duas vezes esta noite, e eu só escrevo aquilo de que tenho a certeza." | "You are right about him, I think. But you made me doubt you twice tonight, and I write down only what I am sure of." |
| `no_originals` | sem limite, o final é `stolen_credits` e a afirmação 3 foi desfeita com `tomas_word` | O professor fica muito tempo a olhar para o telemóvel do Duarte. "Uma mensagem está respondida. Ele tem um telemóvel cheio delas, e ninguém aqui guardou as originais." | The professor looks at Duarte's phone for a long moment. "One message is answered. He has a phone full of them, and nobody here kept the originals." |

