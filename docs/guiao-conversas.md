# Guião das conversas — O quinto elemento (jogo 3D)

Tudo o que as pessoas dizem no jogo 3D, em português e em inglês, tal como está no código.

> **Gerado em 21/11/2026 (atualizado à mão a 22/11/2026) a partir de `prototypes/campus-3d/campus_people.py`, `prototypes/campus-3d/campus_case.py` e `story.py`.** O código é que manda: se mudares uma fala no código, este guião fica desatualizado até ser gerado outra vez.

## Como alterar uma fala

1. **Conversas** (o que cada pessoa diz quando falas com ela): `prototypes/campus-3d/campus_people.py`, dentro de `PEOPLE`. Há um bloco `"en"` (inglês) e um bloco `"pt"` (português). Ao lado de cada fala deste guião está o número da linha.
2. **Respostas às ações** (o que acontece quando escolhes ▶ abrir a gaveta, pedir a cópia, etc.): `story.py`, em `result_text` (quando resulta) e `blocked_text` (quando ainda não podes).
3. **Provas, confrontos e audiência** (o que as pessoas respondem quando lhes mostras uma prova, e as três afirmações do Duarte): `prototypes/campus-3d/campus_case.py`. Só o servidor lê este ficheiro: nada do que lá está pode ir para `campus_text.py`.
4. **O que vai para o balão:** só o que está **entre aspas** (`\"...\"` no código) aparece no balão e é lido pela voz. O resto aparece como narração, em itálico, fora dos balões. Exemplo: `Rita looks up from her laptop. \"You don't look so good.\"`: "Rita looks up from her laptop." é narração, e "You don't look so good." vai para o balão.
5. **Regras para não estragar nada** (os testes verificam-nas):
   - Muda só o texto entre as aspas de `"text"`, `"label"` e `"note"`. Não mudes os identificadores (`"start"`, `"photo"`, `"next": ...`, `"if": ...`, `"trust"`).
   - Se mudares uma fala em português, muda também a inglesa (e vice-versa). As duas línguas têm de ter as mesmas falas, respostas e condições: só o texto muda.
   - Dentro do texto, as aspas da fala escrevem-se `\"` (barra e aspas).
   - As falas nunca podem dizer quais são as mensagens falsas ("message 2", "mensagem 4"…).
6. Depois de mudar, corre `uv run pytest`. Se ficar verde, recarrega o jogo (no endereço que o Streamlit mostra ao arrancar; por omissão http://localhost:8501).

**Legenda:** ⏳ *custa N minutos* é uma resposta agressiva: tira esses minutos à contagem decrescente (para mudar, altera `"cost": 5` no código). 📁 *prova* é uma carta que podes mostrar numa conversa ("Mostrar uma prova"): a certa, na fala certa, faz a pessoa ceder; qualquer outra custa 2 minutos (com o Duarte, 1). *Confiança* (0 a 3) é o humor da pessoa: não aparece no jogo (não há corações), o jogador percebe-o pelo que ela diz; com 0 a pessoa acaba a conversa. *Diário* é a nota que fica guardada no diário do telemóvel. "→ fim" acaba a conversa: no jogo 3D estas respostas não aparecem (usa-se o botão "Terminar conversa"), mas têm de existir no código, porque cada fala precisa de pelo menos uma resposta. Uma pergunta já feita na mesma conversa não volta a aparecer. 🕙 *até às 22:25* / *até às 22:30* quer dizer que a pessoa se vai embora a essa hora do campus. ↺ *a partir da noite N* é uma resposta que só aparece a quem já acabou N−1 noites com esse nome (chave `"night"` no código). Só é oferecida junto com a primeira fala da conversa.

## Rita
Onde está: **Sala de estudo** (`study_room`).

### `start`
- 🇵🇹 A Rita levanta os olhos do portátil. "Estás com cara de quem não dormiu nada. Conseguiste descansar alguma coisa?"  *(linha 207)*
- 🇬🇧 Rita looks up from her laptop. "You don't look so good. Did you sleep at all?"  *(linha 53)*
- Respostas:
  - "Perguntar pela fotografia do grupo" / "Ask about the group photo" → `photo`
  - "Perguntar o que ela se lembra do Duarte" / "Ask what she remembers about Duarte" → `duarte`
  - "Perguntar onde está a pen" / "Ask where the USB stick is" → `pen`
  - "Perguntar pelas mensagens do chat" / "Ask about the chat messages" → `chat` *(só aparece se `files_viewed` = `True`)*
  - ↺ "Dizer-lhe que te lembras de ela contar as cabeças" / "Tell her you remember her counting heads" → `five` *(a partir da noite 3)*
  - "Até já." / "Goodbye." → fim

### `photo`
- 🇵🇹 "A fotografia? Tirámo-la depois da última reunião, nós os quatro."  *(linha 215)*
- 🇬🇧 "The photo? We took it after the last meeting, the four of us."  *(linha 62)*
- 📓 Diário: A Rita lembra-se de quatro pessoas na fotografia do grupo. / Rita remembers four people in the group photo.
- Respostas:
  - "Perguntar porque é que a fotografia da pasta mostra cinco" / "Ask why the photo in the folder shows five" → `five`
  - "Até já." / "Goodbye." → fim

### `five` — 📁 cede com `files` ou `original_photo`
- 🇵🇹 "Então contei mal." A Rita vira o portátil para ti: cinco pessoas. "Uma fotografia não muda. A minha memória muda. Ele devia estar mesmo ali."  *(linha 219)*
- 🇬🇧 "Then I counted wrong." Rita turns the laptop towards you: five people. "A photo cannot change. My memory can. He must have been standing right there."  *(linha 67)*
- Respostas:
  - "Até já." / "Goodbye." → fim

### `pen`
- 🇵🇹 "A pen? Devia estar aqui, mas não a encontro." Olha para a mesa. "Ontem ficámos aqui até tarde a comer pizza, mas com esta confusão, pode estar em qualquer lado."  *(linha 221)*
- 🇬🇧 "The USB stick? It should be here somewhere, but I can't find it." She looks at the table. "We stayed here late last night eating pizza, but with this mess, it could be anywhere."  *(linha 69)*
- 📓 Diário: Rita: não encontra a pen. O grupo comeu pizza aqui ontem à noite. / Rita cannot find the USB stick. The group ate pizza here last night.
- Respostas:
  - "Até já." / "Goodbye." → fim

### `duarte`
- 🇵🇹 "O Duarte... sinceramente, não o consigo imaginar. Sempre que tento, só vejo o nome na capa."  *(linha 223)*
- 🇬🇧 "Duarte... honestly, I cannot picture him. Every time I try, I only see the name on the cover."  *(linha 71)*
- Respostas:
  - "Dizer que achas que o nome foi acrescentado ontem à noite" / "Say you think the name was added last night" → `warned`

### `warned`
- 🇵🇹 A Rita fica calada. "Se for verdade, alguém quis que duvidássemos de nós próprios."  *(linha 225)*
- 🇬🇧 Rita goes quiet. "If that is true, somebody wanted us to doubt ourselves."  *(linha 73)*
- 📓 Diário: A Rita também desconfia do quinto nome. / Rita doubts the fifth name too.
- Respostas:
  - "Até já." / "Goodbye." → fim

### `chat`
- 🇵🇹 "Repara na hora a que as mensagens chegam. Algumas dizem há três semanas, mas no meu telemóvel aparecem como novas, de ontem à noite. Mensagens antigas não funcionam assim."  *(linha 228)*
- 🇬🇧 "Look at when the messages arrive. Some say three weeks ago, but my phone shows them as new, last night. That is not how old messages work."  *(linha 76)*
- 📓 Diário: Rita: uma mensagem antiga não chega como nova. Compara as horas de chegada no chat do grupo. / Rita: an old message does not arrive as new. Compare the arrival times in the group chat.
- Respostas:
  - "Até já." / "Goodbye." → fim

### Ações feitas nesta conversa (em `story.py`)
- **▶ Abrir a gaveta do grupo** / Open the group drawer (`open_drawer`)
  - Se resultar 🇵🇹: Encontras a pen onde o grupo guardava as cópias de segurança do projeto. Guardas a pen.
  - Se resultar 🇬🇧: You find the USB stick where the group kept the project backups. You take the USB stick.

## Funcionária
Onde está: **Reprografia** (`print_shop`).
🕙 Só até às 22:25. Depois, a sala continua aberta mas o balcão está vazio: "A grade está descida e o balcão às escuras. A funcionária foi para casa às 22:25. Há um papel colado na grade: fotografia da capa, pedido de 14 de novembro, levantar amanhã." / "The shutter is down and the counter is dark. The clerk went home at 22:25. A slip is taped to the shutter: cover photo, order of 14 November, collect tomorrow." (a frase está em `campus_clock.py`, não em `campus_text.py`)

### `start`
- 🇵🇹 A funcionária ajeita os óculos. "Fechamos daqui a dez minutos, do que precisas?"  *(linha 233)*
- 🇬🇧 The clerk adjusts her glasses. "Hello! We close in ten minutes. What do you need?"  *(linha 81)*
- Respostas:
  - "Perguntar pelo pedido da fotografia da capa" / "Ask about the cover photo order" → `order`
  - ↺ "Dizer a data antes dela" / "Say the date before she does" → `again` *(a partir da noite 2)*
  - "Até já." / "Goodbye." → fim

### `order`
- 🇵🇹 "A 14 de novembro, tiraram a fotografia e mandaram-na imprimir no mesmo dia. Eram quatro pessoas, ainda me lembro, e acho que o ficheiro original do pedido ainda está guardado."  *(linha 238)*
- 🇬🇧 "On 14 November, you took the photo and had it printed the same day. I remember there were four people in it, and I think the original order file is still saved."  *(linha 86)*
- 📓 Diário: A fotografia da capa foi tirada e impressa a 14 de novembro. A reprografia ainda tem o ficheiro original do pedido. / The cover photo was taken and printed on 14 November. The print shop still has the original order file.
- Respostas:
  - "Até já." / "Goodbye." → fim

### `again` — ↺ a partir da noite 2
- 🇵🇹 A funcionária fica com a mão parada na impressora. "Catorze de novembro. Sim. Como é que tu...?" Olha para o relógio. "Há muito tempo que estou a fechar daqui a dez minutos." Franze a testa para o balcão. "Estranho. Não me lembro de te ver sair."  *(linha 241)*
- 🇬🇧 The clerk stops with her hand on the printer. "The fourteenth of November. Yes. How do you...?" She looks at the clock. "I have been closing in ten minutes for a very long time." She frowns at the counter. "Odd. I do not remember you leaving."  *(linha 90)*
- 📓 Diário: A funcionária confirmou a data antes de acabares de a dizer: a fotografia da capa foi impressa a 14 de novembro. / The clerk agreed with the date before you finished saying it: the cover photo was printed on 14 November.
- Respostas:
  - "Até já." / "Goodbye." → fim

### Ações feitas nesta conversa (em `story.py`)
- **▶ Pedir uma cópia do pedido original** / Ask for a copy of the original order (`request_copy`)
  - Se resultar 🇵🇹: A funcionária volta a imprimir o ficheiro que ficou guardado no pedido. Na fotografia original estão quatro pessoas. Guardas a fotografia.
  - Se resultar 🇬🇧: The clerk prints again the file that was saved with the order. The original photo shows four people. You take the photo.

## Leonor
Onde está: **Biblioteca** (`library`).
🕙 Só até às 22:30 enquanto estiver indecisa; se já estiver a ajudar, fica. Depois: "A cadeira da Leonor está vazia. O livro ficou aberto na mesma página." / "Leonor's chair is empty. Her book is still open at the same page."

### `start` — confiança 2
- 🇵🇹 A Leonor fecha o livro devagar. "Vens por causa do Duarte. Eu sei."  *(linha 246)*
- 🇬🇧 Leonor closes her book slowly. "You are here about Duarte. I know."  *(linha 95)*
- Respostas:
  - "Perguntar se tem a certeza de que ele estava no grupo" / "Ask if she is sure he was in the group" → `sure`
  - "Dizer-lhe que tens dúvidas" / "Tell her you have doubts" → `soft`
  - "Perguntar que mensagem do chat é mesmo dela" / "Ask which chat message is really hers" → `mine` *(só aparece se `colleague_choice` = `help`)*
  - "Dizer que ela está a mentir" / "Say she is lying" → `harsh` ⏳ **custa 5 minutos**
  - ↺ "Dizer-lhe que sabias que ela ia dizer exatamente isso" / "Tell her you knew she would say exactly that" → `again` *(a partir da noite 3)*
  - "Até já." / "Goodbye." → fim

### `sure` — confiança 2 — 📁 cede com `tomas_word`
- 🇵🇹 "Está em todas as mensagens há semanas. Tenho-as aqui." Toca no telemóvel.  *(linha 254)*
- 🇬🇧 "He has been in every message for weeks. I have them right here." She taps her phone.  *(linha 104)*
- Respostas:
  - "Pedir para ver as mensagens" / "Ask to see the messages" → `messages`

### `messages` — confiança 3
- 🇵🇹 "Olha. Todas de um número que eu não conhecia. Algumas têm data de há semanas, mas chegaram ontem à noite."  *(linha 259)*
- 🇬🇧 "Look. All from a number I did not know. Some are dated weeks ago, but they arrived last night."  *(linha 110)*
- 📓 Diário: A Leonor recebeu as mensagens do Duarte ontem à noite, de um número desconhecido. / Leonor received Duarte's messages last night, from an unknown number.
- Respostas:
  - "Até já." / "Goodbye." → fim

### `mine` — confiança 3
- 🇵🇹 "A que pede para reservar a sala de estudo. Escrevi-a nesta mesa, há três semanas." A Leonor percorre o ecrã com um dedo. "As do número que eu não conhecia chegaram todas com minutos de diferença, ontem à noite."  *(linha 256)*
- 🇬🇧 "The one asking to book the study room. I wrote that at this table, three weeks ago." Leonor scrolls with one finger. "The ones from the number I did not know all arrived within minutes of each other, last night."  *(linha 107)*
- 📓 Diário: A Leonor escreveu ela própria a mensagem do chat sobre reservar a sala de estudo. / Leonor wrote the chat message about booking the study room herself.
- Respostas:
  - "Até já." / "Goodbye." → fim

### `soft` — confiança 3
- 🇵🇹 "Eu queria acreditar em ti." Olha para o telemóvel. "Talvez devesse ver outra vez."  *(linha 262)*
- 🇬🇧 "I wanted to believe you." She looks at her phone. "Maybe I should look again."  *(linha 113)*
- Respostas:
  - "Pedir para ver as mensagens" / "Ask to see the messages" → `messages`

### `harsh` — confiança 1
- 🇵🇹 "Desculpa?" A voz dela endurece.  *(linha 264)*
- 🇬🇧 "Excuse me?" Her voice hardens.  *(linha 115)*
- Respostas:
  - "Pedir desculpa" / "Apologise" → `soft`
  - "Insistir" / "Insist" → `closed` ⏳ **custa 5 minutos**

### `closed` — confiança 0
- 🇵🇹 A Leonor levanta-se. "Volta com provas, não com acusações."  *(linha 267)*
- 🇬🇧 Leonor stands up. "Come back with proof, not accusations."  *(linha 118)*
- Respostas:
  - "Sair." / "Leave." → fim

### `again` — confiança 3 — ↺ a partir da noite 3
- 🇵🇹 A mão da Leonor fica em cima do livro. "Palavra por palavra? Ninguém sabe o que eu vou dizer." Fica a olhar para o teu cachecol. "Já fizemos isto antes?"  *(linha 268)*
- 🇬🇧 Leonor's hand stays on the book. "Word for word? Nobody knows what I am going to say." She studies your scarf. "Have we done this before?"  *(linha 120)*
- Respostas:
  - "Até já." / "Goodbye." → fim

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
- 🇵🇹 O Tomás está curvado sobre o computador 11, a evitar o teu olhar. "Ah. Olá. Já é tarde."  *(linha 272)*
- 🇬🇧 Tomás is hunched over computer 11, avoiding your eyes. "Oh. Hi. It is late."  *(linha 124)*
- Respostas:
  - "Perguntar com calma o que está ali a fazer" / "Ask kindly what he is doing here" → `kind`
  - "Exigir saber porque mentiu sobre o Duarte" / "Demand to know why he lied about Duarte" → `hard` ⏳ **custa 5 minutos**
  - "Mostrar-lhe a fotografia original" / "Show him the original photo" → `photo` *(só aparece se tens `original_photo`)*
  - ↺ "Dizer-lhe que já sabes o que o chat diz sobre os slides" / "Tell him you know what the chat says about the slides" → `slides` *(a partir da noite 2)*
  - "Até já." / "Goodbye." → fim

### `kind` — confiança 3
- 🇵🇹 "Não conseguia dormir e vim acabar os slides. Ontem à noite, perto da meia-noite, vi alguém no computador 12."  *(linha 279)*
- 🇬🇧 "I could not sleep, I just came here to finish the slides. And... I saw someone at computer 12 last night, near midnight."  *(linha 133)*
- Respostas:
  - "Perguntar quem era" / "Ask who it was" → `who`
  - "Perguntar a password do computador 12" / "Ask for the password of computer 12" → `password`
  - "Perguntar pela mensagem 5, a que tem o nome dele" / "Ask about message 5, the one with his name" → `msg5` *(só aparece se `files_viewed` = `True`)*
  - "Perguntar quem fez os slides" / "Ask who made the slides" → `slides` *(só aparece se `files_viewed` = `True`)*

### `password` — confiança 3
- 🇵🇹 "A password do computador? É o dia e o mês em que tirámos a fotografia da capa. São só 4 números mas nunca me lembro da data."  *(linha 284)*
- 🇬🇧 "The password of computer 12? It is the group's: the day and the month we took the cover photo. Four digits. I can never remember the date."  *(linha 138)*
- 📓 Diário: Tomás: a password do computador 12 é o dia e o mês em que foi tirada a fotografia da capa (4 algarismos). / Tomás: the password of computer 12 is the day and month the cover photo was taken (4 digits).
- Respostas:
  - "Até já." / "Goodbye." → fim

### `who` — confiança 3
- 🇵🇹 "Só vi um capuz. Como o que o Duarte usa. Mas ninguém o viu chegar."  *(linha 286)*
- 🇬🇧 "Only a hood. Like the one Duarte wears. But nobody ever saw him arrive."  *(linha 140)*
- 📓 Diário: O Tomás viu alguém de capuz no computador 12 perto da meia-noite. / Tomás saw someone in a hood at computer 12 near midnight.
- Respostas:
  - "Até já." / "Goodbye." → fim

### `msg5` — confiança 3
- 🇵🇹 "'Os slides foram do Duarte'? Está com o meu nome, mas não me lembro de a ter escrito. O meu telemóvel apitou com ela ontem à noite, perto da meia-noite, como se tivesse sido enviada há três semanas."  *(linha 289)*
- 🇬🇧 "'Duarte did the slides'? It is under my name, but I do not remember writing it. My phone buzzed with it last night, near midnight, as if it had been sent three weeks ago."  *(linha 144)*
- 📓 Diário: O Tomás não se lembra de ter escrito a mensagem 5; chegou-lhe ao telemóvel ontem à noite. / Tomás does not remember writing message 5; it reached his phone last night.
- Respostas:
  - "Até já." / "Goodbye." → fim

### `slides` — confiança 2 — 📁 cede com `msg_5`
- 🇵🇹 O Tomás não tira os olhos do ecrã. "Os slides? Estou a acabá-los. Mas o chat diz que foram do Duarte, com o meu nome. Se calhar foram mesmo, e eu só arrumei."  *(linha 292)*
- 🇬🇧 Tomás keeps his eyes on the screen. "The slides? I am finishing them. But the chat says Duarte did them, under my name. So maybe he did, and I only tidied up."  *(linha 148)*
- 📓 Diário: O Tomás acha que os slides podem ter sido do Duarte, só porque uma mensagem do chat com o nome dele o diz. / Tomás thinks Duarte may have made the slides, only because a chat message under his own name says so.
- Respostas:
  - "Até já." / "Goodbye." → fim

### `hard` — confiança 1
- 🇵🇹 "Como? Eu não menti!" A voz dele treme.  *(linha 295)*
- 🇬🇧 "Excuse me? I did not lie!" His voice shakes.  *(linha 151)*
- Respostas:
  - "Pedir desculpa" / "Apologise" → `calm`
  - "Pressionar mais" / "Push harder" → `closed` ⏳ **custa 5 minutos**

### `calm` — confiança 2
- 🇵🇹 "Está bem. Foi uma noite longa. Pergunta com educação."  *(linha 298)*
- 🇬🇧 "Fine. It has been a long night. Ask properly."  *(linha 154)*
- Respostas:
  - "Perguntar com calma o que está ali a fazer" / "Ask kindly what he is doing here" → `kind`
  - "Até já." / "Goodbye." → fim

### `photo` — confiança 2
- 🇵🇹 O Tomás fica a olhar para a fotografia. "Quatro pessoas... nunca tinha reparado." Engole em seco.  *(linha 300)*
- 🇬🇧 Tomás stares at the photo. "Four people... I never noticed." He swallows.  *(linha 156)*
- Respostas:
  - "Pedir-lhe ajuda" / "Ask him to help you" → `help`

### `help` — confiança 3
- 🇵🇹 "Está bem. Vê o chat do grupo. Nem tudo o que lá está é meu."  *(linha 302)*
- 🇬🇧 "All right. Check the group chat. Not everything in there is mine."  *(linha 158)*
- 📓 Diário: O Tomás sugere que algumas mensagens do chat não são de quem diz. / Tomás hints that some chat messages are not from the people they name.
- Respostas:
  - "Até já." / "Goodbye." → fim

### `closed` — confiança 0
- 🇵🇹 O Tomás cruza os braços. "Ficamos por aqui."  *(linha 305)*
- 🇬🇧 Tomás crosses his arms. "We are done here."  *(linha 161)*
- Respostas:
  - "Sair." / "Leave." → fim

## Computador 12
Onde está: **Sala de informática** (`computer_lab`).

### `start`
- 🇵🇹 O computador 12 ainda está ligado, com a sessão do grupo aberta. Pede uma password de 4 algarismos.  *(linha 308)*
- 🇬🇧 Computer 12 is still on, with the group's session open. It asks for a 4-digit password.  *(linha 164)*
- Respostas:
  - "Afastar-me do computador." / "Step away from the computer." → fim

### Ações feitas nesta conversa (em `story.py`)
- **▶ Consultar os ficheiros antigos do projeto** / Look at the old project files (`view_files`)
  - Se resultar 🇵🇹: Ligas a pen ao computador 12 e comparas. Nas cópias de segurança da pen, todas as versões têm quatro autores. Na pasta partilhada, a versão atual foi alterada ontem às 23h47, a partir deste mesmo computador: alguém acrescentou "Duarte" ao relatório e trocou a fotografia. Recuperas a versão original do trabalho.
  - Se resultar 🇬🇧: You plug the USB stick into computer 12 and compare. In the backups on the USB stick, every version has four authors. In the shared folder, the current version was changed yesterday at 11:47 pm, from this same computer: someone added "Duarte" to the report and swapped the photo. You recover the original version of the work.
  - Se ainda não puderes 🇵🇹: A pasta partilhada só mostra a versão atual, já com cinco nomes. Precisas da cópia de segurança do grupo.
  - Se ainda não puderes 🇬🇧: The shared folder only shows the current version, already with five names. You need the group's backup copy.
- **▶ Abrir o chat do grupo no computador 12** / Open the group chat on computer 12 (`open_chat`)

## Professor
Onde está: **Auditório** (`auditorium`).

### `start`
- 🇵🇹 O professor levanta os olhos da lista de grupos. "É sobre as apresentações de amanhã?"  *(linha 311)*
- 🇬🇧 The professor looks up from the list of groups. "Is this about tomorrow's presentations?"  *(linha 167)*
- Respostas:
  - "Perguntar quantos elementos tem o teu grupo na lista" / "Ask how many members your group has on the list" → `list`
  - "Dizer que vais trazer provas" / "Say you will bring proof" → `proof`
  - ↺ "Perguntar se já ouviu este caso" / "Ask if he has heard this case before" → `again` *(a partir da noite 4)*
  - "Até já." / "Goodbye." → fim

### `list`
- 🇵🇹 "Cinco, segundo a capa. Há algum problema?"  *(linha 317)*
- 🇬🇧 "Five, according to the cover. Is something wrong with that?"  *(linha 173)*
- Respostas:
  - "Dizer que vocês são só quatro" / "Say there are only four of you" → `evidence`

### `evidence`
- 🇵🇹 "Então preciso de provas, não de uma sensação. Traga-me o histórico do projeto."  *(linha 319)*
- 🇬🇧 "Then I need evidence, not a feeling. Bring me the history of the project."  *(linha 175)*
- 📓 Diário: O professor quer o histórico do projeto como prova. / The professor wants the project history as evidence.
- Respostas:
  - "Até já." / "Goodbye." → fim

### `proof`
- 🇵🇹 "Provas são bem-vindas. Apresente-as quando estiver pronto."  *(linha 322)*
- 🇬🇧 "Evidence is welcome. Present it when you are ready."  *(linha 178)*
- Respostas:
  - "Até já." / "Goodbye." → fim

### `again` — ↺ a partir da noite 4
- 🇵🇹 O professor vira uma página da lista e volta a virá-la. "Todos os anos me aparece um grupo com um nome a mais. Nunca é o mesmo grupo. É sempre o mesmo nome."  *(linha 324)*
- 🇬🇧 The professor turns a page of the list, then turns it back. "Every year a group comes to me with one name too many. Never the same group. Always the same name."  *(linha 181)*
- Respostas:
  - "Até já." / "Goodbye." → fim

### Ações feitas nesta conversa (em `story.py`)
- **▶ Apresentar as provas ao professor** / Present the evidence to the professor (`present_evidence`)
  - No jogo 3D este botão abre a audiência (as três afirmações do Duarte, em `campus_case.py`); só depois da terceira resposta o jogo acaba. O servidor continua a aceitar a ação direta.

## Duarte
Onde está: **Auditório** (`auditorium`).

### `start` — confiança 3
- 🇵🇹 O Duarte sorri com calma. "Ah, o quarto elemento. Pronto para amanhã?"  *(linha 328)*
- 🇬🇧 Duarte smiles calmly. "Ah, the fourth wheel. Ready for tomorrow?"  *(linha 185)*
- Respostas:
  - "Perguntar que parte do projeto fez" / "Ask which part of the project he did" → `part`
  - "Dizer-lhe que sabes a verdade" / "Tell him you know the truth" → `know` ⏳ **custa 5 minutos**
  - ↺ "Perguntar-lhe quantas noites já foram" / "Ask him how many nights this has been" → `again` *(a partir da noite 2)*
  - "Até já." / "Goodbye." → fim

### `part` — confiança 3
- 🇵🇹 "Os slides, claro. Pergunta a qualquer um." Hesita por um segundo.  *(linha 334)*
- 🇬🇧 "The slides, of course. Ask anyone." He hesitates for a second.  *(linha 191)*
- Respostas:
  - "Perguntar que slide" / "Ask which slide" → `slide`

### `slide` — confiança 2
- 🇵🇹 "A... introdução. A bonita." O Duarte olha para a porta. "Porquê tantas perguntas?"  *(linha 336)*
- 🇬🇧 "The... intro. The nice one." Duarte glances at the door. "Why all these questions?"  *(linha 193)*
- 📓 Diário: O Duarte não soube dizer que slide fez. / Duarte could not say which slide he made.
- Respostas:
  - "Até já." / "Goodbye." → fim

### `know` — confiança 1
- 🇵🇹 "Que verdade? Cuidado com as acusações."  *(linha 339)*
- 🇬🇧 "Know what? Careful with accusations."  *(linha 196)*
- Respostas:
  - "Pressioná-lo" / "Press him" → `closed` ⏳ **custa 5 minutos**
  - "Recuar" / "Back off" → `start`

### `closed` — confiança 0
- 🇵🇹 O Duarte ri-se e vira-te as costas. A conversa acabou.  *(linha 342)*
- 🇬🇧 Duarte laughs and turns away. The conversation is over.  *(linha 199)*
- Respostas:
  - "Sair." / "Leave." → fim

### `again` — confiança 2 — ↺ a partir da noite 2
- 🇵🇹 O sorriso do Duarte não se mexe. "Para ti? Já perdi a conta. Para mim só existe esta noite." Olha para o teu casaco como se fosse dele. "Outra vez tu. Já estava a gostar da companhia."  *(linha 343)*
- 🇬🇧 Duarte's smile does not move. "For you? I have lost count. For me there is only ever tonight." He looks at your coat as if it were his. "You again. I was starting to enjoy the company."  *(linha 201)*
- Respostas:
  - "Até já." / "Goodbye." → fim

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
| `original_photo` | tens o objeto `original_photo` (a fotografia triturada, reconstruída na reprografia) | A fotografia original, colada com fita-cola: quatro pessoas | The original photo, taped back together: four people |
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

**Rita** — sem confiança (a Rita não tem nível de confiança)
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
Uma resposta por afirmação, sem segunda tentativa. Uma prova que não a desfaz, ou "Não dizer nada", é uma dúvida: a confiança do professor em ti desce um ponto (aparece por extenso por baixo do número da afirmação, por exemplo "Confiança do professor em ti: 2/3"; não há corações).

**1. `name`** (fala o Duarte) — desfaz-se com `files`
- 🇵🇹 O Duarte levanta-se sem pressa. "Professor, abra o relatório. O meu nome está na capa. Está lá desde o primeiro rascunho."
- 🇬🇧 Duarte stands up without hurry. "Professor, open the report. My name is on the cover. It has been there since the first draft."
- Certa, `files` (professor): 🇵🇹 "Quatro autores em todas as cópias, e um quinto nome acrescentado ontem às 23h47. Continue." / 🇬🇧 "Four authors in every backup, and a fifth name added last night at 11:47 pm. Go on."
- Errada, qualquer outra (professor): 🇵🇹 "Isso não me diz quem escreveu um relatório." Faz um pequeno sinal na lista. / 🇬🇧 "That does not tell me who wrote a report." He makes a small mark on the list.

**2. `photo`** (fala o Duarte) — desfaz-se com `original_photo` ou `rita_word`
- 🇵🇹 "Então olhe para a fotografia. Cinco pessoas, e eu sou o da direita, de casaco comprido. Uma máquina fotográfica não acrescenta ninguém."
- 🇬🇧 "Then look at the photograph. Five people, and I am the one on the right, in the long coat. A camera does not add anyone."
- Certa, `original_photo` (professor): 🇵🇹 O professor põe a fotografia colada ao lado da capa. "A impressão da própria reprografia, com o carimbo da data. Quatro pessoas, antes de alguém acrescentar um quinto." / 🇬🇧 The professor holds the taped photo next to the cover. "The print shop's own print, with its date stamp. Four people, before anyone added a fifth."
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

### O número desconhecido nas noites seguintes
Uma mensagem quando a noite começa (id `night-<n>`), em `NIGHT_TEXT` de `campus_case.py`. Uma noite conta quando acaba (um final, ou as 22:45 sem final), nunca com um "Novo jogo" simples.

| quando | 🇵🇹 | 🇬🇧 |
|---|---|---|
| noite 1 | (nenhuma) | (none) |
| noite 2 | Outra vez tu? | You again? |
| noite 3 | Outra vez tu. O mesmo casaco, o mesmo cachecol. | You again. Same coat, same scarf. |
| noite 4 | Eu já deixei de contar as noites. Tu não. | I have stopped counting the nights. You have not. |
| noite 5 e seguintes | Olha para a fotografia do teu caso. Depois diz-me qual de nós é o quinto. | Look at the photo on your case file. Then tell me which of us is the fifth. |
| qualquer noite depois de vistos os quatro finais da história (em vez da mensagem dessa noite) | Quatro finais, e continuas aqui. Nunca vais conseguir que os três fiquem do teu lado. Não em trinta minutos. | Four endings, and still here. You will never get all three of them to stand with you. Not in thirty minutes. |
| depois do final verdadeiro | (nenhuma: o número fica calado) | (none) |

A partir da noite 3, os três avisos das rondas (`round-12`, `round-19`, `round-26`) passam a ser do número desconhecido: 🇵🇹 Fecha o computador. Ele vem aí. / 🇬🇧 Close the computer. He is walking. Nas noites 1 e 2 ficam com o texto de sempre.

### O final verdadeiro
- **id:** `night_over` (nunca vai para a página). **Título:** 22:46 (nas duas línguas). **Carimbo:** 🇵🇹 A NOITE ACABOU / 🇬🇧 THE NIGHT IS OVER. **Emoji:** 🌅.
- **Quando:** Os quatro finais da história já vistos em noites anteriores; nesta noite, o final "Caso encerrado", a audiência sem nenhuma dúvida, e a palavra do Tomás e a da Rita conquistadas.
- **Vozes**, pela ordem das falas entre aspas: `rita`, `duarte`, `duarte`, `professor`.
- 🇵🇹 Não esperas que o Duarte acabe as frases; já as ouviste antes. Três afirmações, três respostas, cada uma em cima da mesa antes de ele se calar, e o professor não tira os olhos de ti uma única vez. Depois a porta abre-se e já ninguém está sozinho. A Leonor entra com o telemóvel, o Tomás com os slides, a Rita a contar baixinho. «Quatro. Eu contei.» O Duarte olha para os quatro, juntos, e pela primeira vez o sorriso dele não tem para onde ir. «Outra vez tu.» Não é uma pergunta. «Só precisava que um de vocês duvidasse dos outros três.» Puxa o capuz para trás. Por baixo não há nenhum desconhecido: só um chapéu, um cachecol e um casaco comprido, e são os teus. O professor risca o quinto nome. Quando voltas a olhar para a primeira fila, a cadeira está vazia; em cima dela ficou um telemóvel com todas as mensagens que recebeste do número desconhecido, escritas e nunca enviadas. O teu telemóvel vibra uma última vez. O remetente já não é desconhecido: o nome no ecrã é o teu. O relógio da parede marca 22:46. Ninguém apagou as luzes. «Amanhã apresentam os quatro.» Na fotografia da capa estão quatro pessoas, e tu conheces todas.
- 🇬🇧 You do not wait for Duarte to finish his sentences; you have heard them before. Three claims, three answers, each one on the table before he stops speaking, and the professor never once looks away from you. Then the door opens and nobody is alone any more. Leonor comes in with her phone, Tomás with his slides, Rita counting under her breath. "Four. I counted." Duarte looks at the four of you standing together, and for the first time his smile has nowhere to go. "You again." It is not a question. "I only ever needed one of you to doubt the other three." He pushes back his hood. There is no stranger under it: only a hat, a scarf and a long coat, and they are yours. The professor crosses out the fifth name. When you look back at the front row the seat is empty; on it lies a phone with every message you ever received from the unknown number, written and never sent. Your own phone buzzes one last time. The sender is no longer unknown: the name on the screen is your own. The clock on the wall reads 22:46. Nobody has switched off the lights. "Tomorrow, the four of you present." In the photo on the cover there are four people, and you know every one of them.

## O horário da noite (em `prototypes/campus-3d/campus_clock.py` e `campus_text.py`)

A noite começa às 22:15 e a faculdade fecha às 22:45 (30 minutos do campus). O servidor guarda o minuto; a página desenha a contagem decrescente e diz ao servidor o seu próprio minuto. Nenhum texto lista os custos: o jogador aprende-os pelas notas e pelo relógio.

### O que custa minutos
| O quê | Minutos do campus | O que o jogador vê |
|---|---|---|
| Pedir a cópia | 0,5 (meio minuto) | `−0,5 min` (`−0.5 min` em inglês) |
| A decisão sobre a Leonor; o código certo (comparar os ficheiros) | 1 cada | `−1 min` |
| A prova certa | 0 | nada |
| Uma prova errada, ou numa fala errada | 2 | `−2 minutos: isso não provou nada.` |
| Qualquer prova mostrada ao Duarte | 1 | `−1 minuto: ele nem olhou.` |
| Apanhado no computador 12 | 3 | a fala `caught` e `−3 min` (na primeira ronda os 3 minutos acabam às 22:30, quando uma Leonor indecisa se vai embora) |
| Uma resposta agressiva | 5 | `−5 minutos: a conversa correu mal.` (igual) |
| Um sítio errado; um código errado | 1 | igual |
| Andar, falar, o sítio certo, abrir e fechar o chat, marcar, responder a uma afirmação | 0 | nada |

### As duas saídas
- **Funcionária:** sai às 22:25 (minuto 10). A frase da grade está acima, na secção da Funcionária.
- **Leonor:** sai às 22:30 (minuto 15), só se ainda estiver indecisa. A ajudar, fica; acusada, a mesa já ficou vazia pela história e às 22:30 nada muda.
- Depois de a pessoa sair, a sala continua aberta, mas a pessoa já não aparece, não se pode falar com ela nem mostrar-lhe provas, e a ação dela (a cópia; as duas decisões da Leonor) é recusada com a frase do horário. Uma conversa aberta quando a pessoa sai acaba com essa frase.

Depois das 22:25 a data do código lê-se no papel colado na grade da reprografia: no modo de texto é o primeiro parágrafo da sala; em 3D aparece como nota ao entrar e fica no diário.

Uma pista que já não se pode obter fica "perdida" e conta como feita para a porta do auditório: a noite acaba sempre.

### As rondas do Duarte: 22:27, 22:34 e 22:41
Se nesse minuto estiveres no chat do grupo do computador 12 e o Tomás ainda não tiver cedido, és apanhado: o chat fecha (as mensagens já marcadas ficam), custa 3 minutos e começas a audiência com uma dúvida.
- `caught` 🇵🇹 A porta da sala abre-se atrás de ti. "A trabalhar até tarde?" O Duarte estica o braço por cima do teu ombro e fecha o chat. "Essas mensagens não são para ti." / 🇬🇧 The lab door opens behind you. "Working late?" Duarte reaches past your shoulder and closes the chat. "Those messages are not for you."
- `door` (o Tomás já cedeu e vigia a porta: a ronda passa e não custa nada) 🇵🇹 O Tomás põe-se à porta. O Duarte segue caminho. / 🇬🇧 Tomás stands in the doorway. Duarte walks on.

### As mensagens do número desconhecido
| id | quando chega | 🇵🇹 | 🇬🇧 |
|---|---|---|---|
| `shop` | do minuto 5 ao 9, sem a fotografia original | A reprografia fecha às 22:25. E tu ainda na conversa. | The print shop closes at 22:25. You are still talking. |
| `leonor` | do minuto 10 ao 14, a Leonor indecisa e a pista dela não perdida | A Leonor arruma a mochila às dez e meia. Faz sempre isso. | Leonor packs her bag at half past ten. She always does. |
| `lost` | quando uma pista se perde | Para isso, hoje já é tarde. Amanhã deixo-te a luz acesa. | Too late for that tonight. I will keep the light on for you tomorrow. |
| `round-12`, `round-19`, `round-26` | no minuto antes de cada ronda (11, 18, 25), se o Tomás ainda não cedeu | Anda alguém no corredor. Não estejas no computador 12 quando ele passar. | Someone is walking the corridor. Do not be at computer 12 when he passes. |
