# Guião das conversas — O quinto elemento (jogo 3D)

Tudo o que as pessoas dizem no jogo 3D, em português e em inglês, tal como está no código.

> **Gerado em 21/11/2026 (atualizado à mão a 23/11/2026, com os três casos do dia mais abaixo) a partir de `prototypes/campus-3d/campus_people.py`, `prototypes/campus-3d/campus_case.py` e `story.py`.** O código é que manda: se mudares uma fala no código, este guião fica desatualizado até ser gerado outra vez.

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

**Legenda:** ⏳ *custa N minutos* é uma resposta agressiva: tira esses minutos à contagem decrescente (para mudar, altera `"cost": 5` no código) e fica lembrada até ao fim da noite (ver "Quando foste rude", mais abaixo). 📁 *prova* é uma carta que podes mostrar numa conversa ("Mostrar uma prova"): a certa, na fala certa, faz a pessoa ceder; qualquer outra custa 2 minutos (com o Duarte, 1). *Confiança* (0 a 3) é o humor da pessoa: não aparece no jogo (não há corações), o jogador percebe-o pelo que ela diz; com 0 a pessoa acaba a conversa. *Diário* é a nota que fica guardada no diário do telemóvel. "→ fim" acaba a conversa: no jogo 3D estas respostas não aparecem (usa-se o botão "Terminar conversa"), mas têm de existir no código, porque cada fala precisa de pelo menos uma resposta. Uma pergunta já feita na mesma conversa não volta a aparecer. 🕙 *até às 22:25* / *até às 22:30* quer dizer que a pessoa se vai embora a essa hora do campus. ↺ *a partir da noite N* é uma resposta que só aparece a quem já acabou N−1 noites com esse nome (chave `"night"` no código). Só é oferecida junto com a primeira fala da conversa.

## Rita
Onde está: **Sala de estudo** (`study_room`).

### `start`
- 🇵🇹 A Rita levanta os olhos do portátil. "Estás com cara de quem não dormiu nada. Conseguiste descansar alguma coisa?"  *(linha 222)*
- 🇬🇧 Rita looks up from her laptop. "You don't look so good. Did you sleep at all?"  *(linha 68)*
- Respostas:
  - "Perguntar pela fotografia do grupo" / "Ask about the group photo" → `photo`
  - "Perguntar o que ela se lembra do Duarte" / "Ask what she remembers about Duarte" → `duarte`
  - "Perguntar onde está a pen" / "Ask where the USB stick is" → `pen`
  - "Perguntar pelas mensagens do chat" / "Ask about the chat messages" → `chat` *(só aparece se `files_viewed` = `True`)*
  - ↺ "Dizer-lhe que te lembras de ela contar as cabeças" / "Tell her you remember her counting heads" → `five` *(a partir da noite 3)*
  - "Até já." / "Goodbye." → fim

### `photo`
- 🇵🇹 "A fotografia? Tirámo-la depois da última reunião, nós os quatro."  *(linha 230)*
- 🇬🇧 "The photo? We took it after the last meeting, the four of us."  *(linha 77)*
- 📓 Diário: A Rita lembra-se de quatro pessoas na fotografia do grupo. / Rita remembers four people in the group photo.
- Respostas:
  - "Perguntar porque é que a fotografia da pasta mostra cinco" / "Ask why the photo in the folder shows five" → `five`
  - "Até já." / "Goodbye." → fim

### `five` — 📁 cede com `files` ou `original_photo`
- 🇵🇹 "Então contei mal." A Rita vira o portátil para ti: cinco pessoas. "Uma fotografia não muda. A minha memória muda. Ele devia estar mesmo ali."  *(linha 234)*
- 🇬🇧 "Then I counted wrong." Rita turns the laptop towards you: five people. "A photo cannot change. My memory can. He must have been standing right there."  *(linha 82)*
- Respostas:
  - "Até já." / "Goodbye." → fim

### `pen`
- 🇵🇹 "A pen? Devia estar aqui, mas não a encontro." Olha para a mesa. "Ontem ficámos aqui até tarde a comer pizza, mas com esta confusão, pode estar em qualquer lado."  *(linha 236)*
- 🇬🇧 "The USB stick? It should be here somewhere, but I can't find it." She looks at the table. "We stayed here late last night eating pizza, but with this mess, it could be anywhere."  *(linha 84)*
- 📓 Diário: Rita: não encontra a pen. O grupo comeu pizza aqui ontem à noite. / Rita cannot find the USB stick. The group ate pizza here last night.
- Respostas:
  - "Até já." / "Goodbye." → fim

### `duarte`
- 🇵🇹 "O Duarte... sinceramente, não o consigo imaginar. Sempre que tento, só vejo o nome na capa."  *(linha 238)*
- 🇬🇧 "Duarte... honestly, I cannot picture him. Every time I try, I only see the name on the cover."  *(linha 86)*
- Respostas:
  - "Dizer que achas que o nome foi acrescentado ontem à noite" / "Say you think the name was added last night" → `warned`

### `warned`
- 🇵🇹 A Rita fica calada. "Se for verdade, alguém quis que duvidássemos de nós próprios."  *(linha 240)*
- 🇬🇧 Rita goes quiet. "If that is true, somebody wanted us to doubt ourselves."  *(linha 88)*
- 📓 Diário: A Rita também desconfia do quinto nome. / Rita doubts the fifth name too.
- Respostas:
  - "Até já." / "Goodbye." → fim

### `chat`
- 🇵🇹 "Repara na hora a que as mensagens chegam. Algumas dizem há três semanas, mas no meu telemóvel aparecem como novas, de ontem à noite. Mensagens antigas não funcionam assim."  *(linha 243)*
- 🇬🇧 "Look at when the messages arrive. Some say three weeks ago, but my phone shows them as new, last night. That is not how old messages work."  *(linha 91)*
- 📓 Diário: Rita: uma mensagem antiga não chega como nova. Compara as horas de chegada no chat do grupo. / Rita: an old message does not arrive as new. Compare the arrival times in the group chat.
- Respostas:
  - "Até já." / "Goodbye." → fim

### Ações feitas nesta conversa (em `story.py`)
- **▶ Abrir a gaveta do grupo** / Open the group drawer (`open_drawer`)
  - Se resultar 🇵🇹: Encontras a pen onde o grupo guardava as cópias de segurança do projeto. Guardas a pen.
  - Se resultar 🇬🇧: You find the USB stick where the group kept the project backups. You take the USB stick.

## Funcionária
Onde está: **Reprografia** (`print_shop`).
🕙 Só até às 22:25. Depois, a sala continua aberta mas o balcão está vazio: "A grade está descida e o balcão às escuras. A funcionária foi para casa às 22:25. Há um papel colado na grade: fotografia da capa, pedido de 17 de outubro, levantar amanhã." / "The shutter is down and the counter is dark. The clerk went home at 22:25. A slip is taped to the shutter: cover photo, order of 17 October, collect tomorrow." (a frase está em `campus_clock.py`, não em `campus_text.py`)

### `start`
- 🇵🇹 A funcionária ajeita os óculos. "Fechamos daqui a dez minutos, do que precisas?"  *(linha 248)*
- 🇬🇧 The clerk adjusts her glasses. "Hello! We close in ten minutes. What do you need?"  *(linha 96)*
- Respostas:
  - "Perguntar pelo pedido da fotografia da capa" / "Ask about the cover photo order" → `order`
  - ↺ "Dizer a data antes dela" / "Say the date before she does" → `again` *(a partir da noite 2)*
  - "Até já." / "Goodbye." → fim

### `order`
- 🇵🇹 "A fotografia da capa? Tiraram-na e mandaram-na imprimir aqui no mesmo dia. Eram quatro pessoas, ainda me lembro, e acho que o ficheiro original do pedido ainda está guardado."  *(linha 253)*
- 🇬🇧 "The cover photo? You took it and had it printed here the same day. I remember there were four people in it, and I think the original order file is still saved."  *(linha 101)*
- 📓 Diário: A fotografia da capa foi impressa na reprografia no dia em que foi tirada. A reprografia ainda tem o ficheiro original do pedido. / The cover photo was printed at the print shop the day it was taken. The print shop still has the original order file.
- Respostas:
  - "Até já." / "Goodbye." → fim

### `again` — ↺ a partir da noite 2
- 🇵🇹 A funcionária fica com a mão parada na impressora. "Dezassete de outubro. Sim. Como é que tu...?" Olha para o relógio. "Há muito tempo que estou a fechar daqui a dez minutos." Franze a testa para o balcão. "Estranho. Não me lembro de te ver sair."  *(linha 256)*
- 🇬🇧 The clerk stops with her hand on the printer. "The seventeenth of October. Yes. How do you...?" She looks at the clock. "I have been closing in ten minutes for a very long time." She frowns at the counter. "Odd. I do not remember you leaving."  *(linha 105)*
- 📓 Diário: A funcionária confirmou a data antes de acabares de a dizer: a fotografia da capa foi impressa a 17 de outubro. / The clerk agreed with the date before you finished saying it: the cover photo was printed on 17 October.
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
- 🇵🇹 A Leonor fecha o livro devagar. "Vens por causa do Duarte. Eu sei."  *(linha 261)*
- 🇬🇧 Leonor closes her book slowly. "You are here about Duarte. I know."  *(linha 110)*
- Respostas:
  - "Perguntar se tem a certeza de que ele estava no grupo" / "Ask if she is sure he was in the group" → `sure`
  - "Dizer-lhe que tens dúvidas" / "Tell her you have doubts" → `soft`
  - "Perguntar que mensagem do chat é mesmo dela" / "Ask which chat message is really hers" → `mine` *(só aparece se `colleague_choice` = `help`)*
  - "Dizer que ela está a mentir" / "Say she is lying" → `harsh` ⏳ **custa 5 minutos**
  - ↺ "Dizer-lhe que sabias que ela ia dizer exatamente isso" / "Tell her you knew she would say exactly that" → `again` *(a partir da noite 3)*
  - "Até já." / "Goodbye." → fim

### `sure` — confiança 2 — 📁 cede com `tomas_word`
- 🇵🇹 "Está em todas as mensagens há semanas. Tenho-as aqui." Toca no telemóvel.  *(linha 269)*
- 🇬🇧 "He has been in every message for weeks. I have them right here." She taps her phone.  *(linha 119)*
- Respostas:
  - "Pedir para ver as mensagens" / "Ask to see the messages" → `messages`

### `messages` — confiança 3
- 🇵🇹 "Olha. Todas de um número que eu não conhecia. Algumas têm data de há semanas, mas chegaram ontem à noite."  *(linha 274)*
- 🇬🇧 "Look. All from a number I did not know. Some are dated weeks ago, but they arrived last night."  *(linha 125)*
- 📓 Diário: A Leonor recebeu as mensagens do Duarte ontem à noite, de um número desconhecido. / Leonor received Duarte's messages last night, from an unknown number.
- Respostas:
  - "Até já." / "Goodbye." → fim

### `mine` — confiança 3
- 🇵🇹 "A que pede para reservar a sala de estudo. Escrevi-a nesta mesa, há três semanas." A Leonor percorre o ecrã com um dedo. "As do número que eu não conhecia chegaram todas com minutos de diferença, ontem à noite."  *(linha 271)*
- 🇬🇧 "The one asking to book the study room. I wrote that at this table, three weeks ago." Leonor scrolls with one finger. "The ones from the number I did not know all arrived within minutes of each other, last night."  *(linha 122)*
- 📓 Diário: A Leonor escreveu ela própria a mensagem do chat sobre reservar a sala de estudo. / Leonor wrote the chat message about booking the study room herself.
- Respostas:
  - "Até já." / "Goodbye." → fim

### `soft` — confiança 3
- 🇵🇹 "Eu queria acreditar em ti." Olha para o telemóvel. "Talvez devesse ver outra vez."  *(linha 277)*
- 🇬🇧 "I wanted to believe you." She looks at her phone. "Maybe I should look again."  *(linha 128)*
- Respostas:
  - "Pedir para ver as mensagens" / "Ask to see the messages" → `messages`

### `harsh` — confiança 1
- 🇵🇹 "Desculpa?" A voz dela endurece.  *(linha 279)*
- 🇬🇧 "Excuse me?" Her voice hardens.  *(linha 130)*
- Respostas:
  - "Pedir desculpa" / "Apologise" → `soft`
  - "Insistir" / "Insist" → `closed` ⏳ **custa 5 minutos**

### `closed` — confiança 0
- 🇵🇹 A Leonor levanta-se. "Volta com provas, não com acusações."  *(linha 282)*
- 🇬🇧 Leonor stands up. "Come back with proof, not accusations."  *(linha 133)*
- Respostas:
  - "Sair." / "Leave." → fim

### `again` — confiança 3 — ↺ a partir da noite 3
- 🇵🇹 A mão da Leonor fica em cima do livro. "Palavra por palavra? Ninguém sabe o que eu vou dizer." Fica a olhar para o teu cachecol. "Já fizemos isto antes?"  *(linha 283)*
- 🇬🇧 Leonor's hand stays on the book. "Word for word? Nobody knows what I am going to say." She studies your scarf. "Have we done this before?"  *(linha 135)*
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
- 🇵🇹 O Tomás está curvado sobre o computador 11, a evitar o teu olhar. "Ah. Olá. Já é tarde."  *(linha 287)*
- 🇬🇧 Tomás is hunched over computer 11, avoiding your eyes. "Oh. Hi. It is late."  *(linha 139)*
- Respostas:
  - "Perguntar com calma o que está ali a fazer" / "Ask kindly what he is doing here" → `kind`
  - "Exigir saber porque mentiu sobre o Duarte" / "Demand to know why he lied about Duarte" → `hard` ⏳ **custa 5 minutos**
  - "Mostrar-lhe a fotografia original" / "Show him the original photo" → `photo` *(só aparece se tens `original_photo`)*
  - ↺ "Dizer-lhe que já sabes o que o chat diz sobre os slides" / "Tell him you know what the chat says about the slides" → `slides` *(a partir da noite 2)*
  - "Até já." / "Goodbye." → fim

### `kind` — confiança 3
- 🇵🇹 "Não conseguia dormir e vim acabar os slides. Ontem à noite, perto da meia-noite, vi alguém no computador 12."  *(linha 294)*
- 🇬🇧 "I could not sleep, I just came here to finish the slides. And... I saw someone at computer 12 last night, near midnight."  *(linha 148)*
- Respostas:
  - "Perguntar quem era" / "Ask who it was" → `who`
  - "Perguntar a password do computador 12" / "Ask for the password of computer 12" → `password`
  - "Perguntar pela mensagem 5, a que tem o nome dele" / "Ask about message 5, the one with his name" → `msg5` *(só aparece se `files_viewed` = `True`)*
  - "Perguntar quem fez os slides" / "Ask who made the slides" → `slides` *(só aparece se `files_viewed` = `True`)*

### `password` — confiança 3
- 🇵🇹 "A password do computador? É o dia e o mês em que tirámos a fotografia da capa. São só 4 números, mas nunca me lembro da data. Entre todos havemos de lá chegar."  *(linha 299)*
- 🇬🇧 "The password of computer 12? It is the group's: the day and the month we took the cover photo. Four digits. I can never remember the date, but between all of us we can work it out."  *(linha 153)*
- 📓 Diário: Tomás: a password do computador 12 é o dia e o mês em que foi tirada a fotografia da capa (4 algarismos). / Tomás: the password of computer 12 is the day and month the cover photo was taken (4 digits).
- Respostas:
  - "Até já." / "Goodbye." → fim

### `who` — confiança 3
- 🇵🇹 "Só vi um capuz. Como o que o Duarte usa. Mas ninguém o viu chegar."  *(linha 301)*
- 🇬🇧 "Only a hood. Like the one Duarte wears. But nobody ever saw him arrive."  *(linha 155)*
- 📓 Diário: O Tomás viu alguém de capuz no computador 12 perto da meia-noite. / Tomás saw someone in a hood at computer 12 near midnight.
- Respostas:
  - "Até já." / "Goodbye." → fim

### `msg5` — confiança 3
- 🇵🇹 "'Os slides foram do Duarte'? Está com o meu nome, mas não me lembro de a ter escrito. O meu telemóvel apitou com ela ontem à noite, perto da meia-noite, como se tivesse sido enviada há três semanas."  *(linha 304)*
- 🇬🇧 "'Duarte did the slides'? It is under my name, but I do not remember writing it. My phone buzzed with it last night, near midnight, as if it had been sent three weeks ago."  *(linha 159)*
- 📓 Diário: O Tomás não se lembra de ter escrito a mensagem 5; chegou-lhe ao telemóvel ontem à noite. / Tomás does not remember writing message 5; it reached his phone last night.
- Respostas:
  - "Até já." / "Goodbye." → fim

### `slides` — confiança 2 — 📁 cede com `msg_5`
- 🇵🇹 O Tomás não tira os olhos do ecrã. "Os slides? Estou a acabá-los. Mas o chat diz que foram do Duarte, com o meu nome. Se calhar foram mesmo, e eu só arrumei."  *(linha 307)*
- 🇬🇧 Tomás keeps his eyes on the screen. "The slides? I am finishing them. But the chat says Duarte did them, under my name. So maybe he did, and I only tidied up."  *(linha 163)*
- 📓 Diário: O Tomás acha que os slides podem ter sido do Duarte, só porque uma mensagem do chat com o nome dele o diz. / Tomás thinks Duarte may have made the slides, only because a chat message under his own name says so.
- Respostas:
  - "Até já." / "Goodbye." → fim

### `hard` — confiança 1
- 🇵🇹 "Como? Eu não menti!" A voz dele treme.  *(linha 310)*
- 🇬🇧 "Excuse me? I did not lie!" His voice shakes.  *(linha 166)*
- Respostas:
  - "Pedir desculpa" / "Apologise" → `calm`
  - "Pressionar mais" / "Push harder" → `closed` ⏳ **custa 5 minutos**

### `calm` — confiança 2
- 🇵🇹 "Está bem. Foi uma noite longa. Pergunta com educação."  *(linha 313)*
- 🇬🇧 "Fine. It has been a long night. Ask properly."  *(linha 169)*
- Respostas:
  - "Perguntar com calma o que está ali a fazer" / "Ask kindly what he is doing here" → `kind`
  - "Até já." / "Goodbye." → fim

### `photo` — confiança 2
- 🇵🇹 O Tomás fica a olhar para a fotografia. "Quatro pessoas... nunca tinha reparado." Engole em seco.  *(linha 315)*
- 🇬🇧 Tomás stares at the photo. "Four people... I never noticed." He swallows.  *(linha 171)*
- Respostas:
  - "Pedir-lhe ajuda" / "Ask him to help you" → `help`

### `help` — confiança 3
- 🇵🇹 "Está bem. Vê o chat do grupo. Nem tudo o que lá está é meu."  *(linha 317)*
- 🇬🇧 "All right. Check the group chat. Not everything in there is mine."  *(linha 173)*
- 📓 Diário: O Tomás sugere que algumas mensagens do chat não são de quem diz. / Tomás hints that some chat messages are not from the people they name.
- Respostas:
  - "Até já." / "Goodbye." → fim

### `closed` — confiança 0
- 🇵🇹 O Tomás cruza os braços. "Ficamos por aqui."  *(linha 320)*
- 🇬🇧 Tomás crosses his arms. "We are done here."  *(linha 176)*
- Respostas:
  - "Sair." / "Leave." → fim

## Computador 12
Onde está: **Sala de informática** (`computer_lab`).

### `start`
- 🇵🇹 O computador 12 ainda está ligado, com a sessão do grupo aberta. Pede uma password de 4 algarismos.  *(linha 323)*
- 🇬🇧 Computer 12 is still on, with the group's session open. It asks for a 4-digit password.  *(linha 179)*
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
- 🇵🇹 O professor levanta os olhos da lista de grupos. "É sobre as apresentações de amanhã?"  *(linha 326)*
- 🇬🇧 The professor looks up from the list of groups. "Is this about tomorrow's presentations?"  *(linha 182)*
- Respostas:
  - "Perguntar quantos elementos tem o teu grupo na lista" / "Ask how many members your group has on the list" → `list`
  - "Dizer que vais trazer provas" / "Say you will bring proof" → `proof`
  - ↺ "Perguntar se já ouviu este caso" / "Ask if he has heard this case before" → `again` *(a partir da noite 4)*
  - "Até já." / "Goodbye." → fim

### `list`
- 🇵🇹 "Cinco, segundo a capa. Há algum problema?"  *(linha 332)*
- 🇬🇧 "Five, according to the cover. Is something wrong with that?"  *(linha 188)*
- Respostas:
  - "Dizer que vocês são só quatro" / "Say there are only four of you" → `evidence`

### `evidence`
- 🇵🇹 "Então preciso de provas, não de uma sensação. Traga-me o histórico do projeto."  *(linha 334)*
- 🇬🇧 "Then I need evidence, not a feeling. Bring me the history of the project."  *(linha 190)*
- 📓 Diário: O professor quer o histórico do projeto como prova. / The professor wants the project history as evidence.
- Respostas:
  - "Até já." / "Goodbye." → fim

### `proof`
- 🇵🇹 "Provas são bem-vindas. Apresente-as quando estiver pronto."  *(linha 337)*
- 🇬🇧 "Evidence is welcome. Present it when you are ready."  *(linha 193)*
- Respostas:
  - "Até já." / "Goodbye." → fim

### `again` — ↺ a partir da noite 4
- 🇵🇹 O professor vira uma página da lista e volta a virá-la. "Todos os anos me aparece um grupo com um nome a mais. Nunca é o mesmo grupo. É sempre o mesmo nome."  *(linha 339)*
- 🇬🇧 The professor turns a page of the list, then turns it back. "Every year a group comes to me with one name too many. Never the same group. Always the same name."  *(linha 196)*
- Respostas:
  - "Até já." / "Goodbye." → fim

### Ações feitas nesta conversa (em `story.py`)
- **▶ Apresentar as provas ao professor** / Present the evidence to the professor (`present_evidence`)
  - No jogo 3D este botão abre a audiência (as três afirmações do Duarte, em `campus_case.py`); só depois da terceira resposta o jogo acaba. O servidor continua a aceitar a ação direta.

## Duarte
Onde está: **Auditório** (`auditorium`).

### `start` — confiança 3
- 🇵🇹 O Duarte sorri com calma. "Ah, o quarto elemento. Pronto para amanhã?"  *(linha 343)*
- 🇬🇧 Duarte smiles calmly. "Ah, the fourth wheel. Ready for tomorrow?"  *(linha 200)*
- Respostas:
  - "Perguntar que parte do projeto fez" / "Ask which part of the project he did" → `part`
  - "Dizer-lhe que sabes a verdade" / "Tell him you know the truth" → `know` ⏳ **custa 5 minutos**
  - ↺ "Perguntar-lhe quantas noites já foram" / "Ask him how many nights this has been" → `again` *(a partir da noite 2)*
  - "Até já." / "Goodbye." → fim

### `part` — confiança 3
- 🇵🇹 "Os slides, claro. Pergunta a qualquer um." Hesita por um segundo.  *(linha 349)*
- 🇬🇧 "The slides, of course. Ask anyone." He hesitates for a second.  *(linha 206)*
- Respostas:
  - "Perguntar que slide" / "Ask which slide" → `slide`

### `slide` — confiança 2
- 🇵🇹 "A... introdução. A bonita." O Duarte olha para a porta. "Porquê tantas perguntas?"  *(linha 351)*
- 🇬🇧 "The... intro. The nice one." Duarte glances at the door. "Why all these questions?"  *(linha 208)*
- 📓 Diário: O Duarte não soube dizer que slide fez. / Duarte could not say which slide he made.
- Respostas:
  - "Até já." / "Goodbye." → fim

### `know` — confiança 1
- 🇵🇹 "Que verdade? Cuidado com as acusações."  *(linha 354)*
- 🇬🇧 "Know what? Careful with accusations."  *(linha 211)*
- Respostas:
  - "Pressioná-lo" / "Press him" → `closed` ⏳ **custa 5 minutos**
  - "Recuar" / "Back off" → `start`

### `closed` — confiança 0
- 🇵🇹 O Duarte ri-se e vira-te as costas. A conversa acabou.  *(linha 357)*
- 🇬🇧 Duarte laughs and turns away. The conversation is over.  *(linha 214)*
- Respostas:
  - "Sair." / "Leave." → fim

### `again` — confiança 2 — ↺ a partir da noite 2
- 🇵🇹 O sorriso do Duarte não se mexe. "Para ti? Já perdi a conta. Para mim só existe esta noite." Olha para o teu casaco como se fosse dele. "Outra vez tu. Já estava a gostar da companhia."  *(linha 358)*
- 🇬🇧 Duarte's smile does not move. "For you? I have lost count. For me there is only ever tonight." He looks at your coat as if it were his. "You again. I was starting to enjoy the company."  *(linha 216)*
- Respostas:
  - "Até já." / "Goodbye." → fim

## Quando foste rude (em `prototypes/campus-3d/campus_people.py`, fora de `PEOPLE`)

(specs/trust-has-consequences.md) Uma resposta ⏳ fica lembrada até ao fim da noite, nas notas da noite (nota `rude`); um "Novo jogo" esquece-a. A Leonor, o Tomás e o Duarte ficam com um feitio que nunca aparece no ecrã (nem número, nem corações): **calmo** (nenhuma resposta rude), **desconfiado** (uma), **hostil** (duas, por exemplo "Dizer que ela está a mentir" e depois "Insistir"). Pedir desculpa não desfaz. Quem cedeu com a prova certa fica calmo o resto da noite, diga-se o que se disser. A Rita, a funcionária e o professor estão sempre calmos.

Só muda o texto (e às vezes a nota) de uma fala: as respostas, as ações (a cópia, as decisões da Leonor, o computador 12, a audiência), as afirmações (`slides`, `five`, `sure`), os custos e o horário ficam iguais. Estes textos estão em tabelas próprias (`COLD`, `WITHHELD`, `LIES`, `WARNED`, `WARNS`), por isso `PEOPLE` não muda. Nenhum diz o culpado, uma data ou um código.

**Que texto ganha:** na fala `start`, o aviso (se quem avisa estiver hostil), senão a fala seca, senão a da história. Na fala `messages` da Leonor, a mentira se estiver hostil, senão a fala seca.

### Falas secas (`COLD`): desconfiado ou hostil; o diário guarda a nota de sempre
- **Tomás, `start`**
  - 🇵🇹 O Tomás nem levanta os olhos do computador 11. "O que foi agora?"  *(linha 372)*
  - 🇬🇧 Tomás does not look up from computer 11. "What now?"  *(linha 363)*
- **Tomás, `kind`**
  - 🇵🇹 "A acabar os slides." Continua a escrever. "Esteve alguém no computador 12 ontem à noite. É tudo o que sei."  *(linha 373)*
  - 🇬🇧 "Finishing the slides." He keeps typing. "Someone was at computer 12 last night. That is all I know."  *(linha 364)*
- **Tomás, `password`** (a regra do código não muda: só fica mais seca)
  - 🇵🇹 "O dia e o mês da fotografia da capa. Quatro algarismos." Nem levanta os olhos.  *(linha 374)*
  - 🇬🇧 "The day and month of the cover photo. Four digits." He does not look up.  *(linha 365)*
- **Leonor, `start`**
  - 🇵🇹 Desta vez a Leonor não fecha o livro. "Sim?"  *(linha 375)*
  - 🇬🇧 Leonor does not close her book this time. "Yes?"  *(linha 366)*
- **Leonor, `messages`** (só desconfiada; hostil, mente: ver abaixo)
  - 🇵🇹 "De um número que eu não conhecia. Ontem à noite."  *(linha 376)*
  - 🇬🇧 "From a number I did not know. Last night."  *(linha 367)*
- **Duarte, `start`**
  - 🇵🇹 O Duarte nem se dá ao trabalho de sorrir. "Ainda por aqui?"  *(linha 377)*
  - 🇬🇧 Duarte does not bother to smile. "Still here?"  *(linha 368)*
- **Duarte, `part`**
  - 🇵🇹 "Os slides. Pergunta a qualquer um." Olha para além de ti.  *(linha 378)*
  - 🇬🇧 "The slides. Ask anyone." He looks past you.  *(linha 369)*

### Pistas que ficam por dar (`WITHHELD`): desconfiado ou hostil; sem nota no diário
São só pistas: tudo o que é preciso para um final tem outra fonte.
- **Tomás, `who`**
  - 🇵🇹 "Não vi nada. Posso trabalhar?"  *(linha 392)*
  - 🇬🇧 "I did not see anything. Can I work now?"  *(linha 386)*
- **Tomás, `help`**
  - 🇵🇹 O Tomás fica a olhar para a fotografia um segundo a mais. "Vê o que quiseres. Estou ocupado."  *(linha 393)*
  - 🇬🇧 Tomás looks at the photo a second too long. "Check what you like. I am busy."  *(linha 387)*
- **Leonor, `mine`**
  - 🇵🇹 "Descobre tu."  *(linha 394)*
  - 🇬🇧 "Work it out yourself."  *(linha 388)*
- **Duarte, `slide`**
  - 🇵🇹 "Porque é que te havia de dizer?" O Duarte olha para a porta.  *(linha 395)*
  - 🇬🇧 "Why would I tell you?" Duarte glances at the door.  *(linha 389)*

### Mentiras (`LIES`): só hostil; o diário guarda o que te disseram
Uma mentira não é uma afirmação: mostrar-lhe uma prova dá a resposta habitual da pessoa e custa os minutos de sempre. Vence-se não acreditando nela. O Duarte mente de qualquer maneira: hostil, não ganha uma mentira nova.
- **Tomás, `msg5`** (desmentem-no a linha de chegada da mensagem 5 no chat, "chegou ontem às 23h49", e a fala `chat` da Rita; quem acreditar nele não marca a mensagem e perde o `full_case`)
  - 🇵🇹 "A que tem o meu nome? Fui eu que a escrevi. Há três semanas, como lá diz." Encolhe os ombros sem olhar para ti.  *(linha 410)*
  - 🇬🇧 "The one with my name? I wrote it. Three weeks ago, like it says." He shrugs without looking at you.  *(linha 404)*
  - 📓 Diário: O Tomás diz que foi ele que escreveu a mensagem com o nome dele, há três semanas. / Tomás says he wrote the message with his name himself, three weeks ago.
- **Leonor, `messages`** (desmentem-na a mesma linha de chegada e a fala `chat` da Rita)
  - 🇵🇹 "Não têm nada de estranho. Chegaram nas datas que lá dizem, há semanas." Vira o telemóvel ao contrário.  *(linha 412)*
  - 🇬🇧 "Nothing strange about them. They came on the dates they say, weeks ago." She turns the phone face down.  *(linha 406)*
  - 📓 Diário: A Leonor diz que as mensagens chegaram nas datas delas, há semanas. / Leonor says the messages arrived on their dates, weeks ago.

### O aviso que passa (`WARNS` e `WARNED`): enquanto quem avisa estiver hostil e não tiver cedido
A cadeia é fixa: o Tomás avisa a Leonor, a Leonor avisa a Rita, o Duarte avisa o professor. Só muda a primeira fala (`start`) de quem foi avisado; as respostas, as ações e as decisões dessa pessoa ficam iguais.
- **Leonor** (avisada pelo Tomás)
  - 🇵🇹 A Leonor fecha o livro antes de chegares à mesa. "O Tomás mandou-me mensagem. Diz que andas por aí a chamar mentirosos às pessoas."  *(linha 425)*
  - 🇬🇧 Leonor closes her book before you reach the table. "Tomás texted me. He says you are going round calling people liars."  *(linha 422)*
- **Rita** (avisada pela Leonor)
  - 🇵🇹 A Rita levanta os olhos e não sorri. "A Leonor diz que lhe gritaste na biblioteca. É verdade?"  *(linha 426)*
  - 🇬🇧 Rita looks up and does not smile. "Leonor says you shouted at her in the library. Is that true?"  *(linha 423)*
- **Professor** (avisado pelo Duarte)
  - 🇵🇹 O professor levanta os olhos da lista e não sorri. "O Duarte diz-me que o ameaçou. Espero que amanhã me traga provas, e não isso."  *(linha 427)*
  - 🇬🇧 The professor looks up from the list and does not smile. "Duarte tells me you threatened him. I hope you bring evidence tomorrow, not that."  *(linha 424)*

## Procurar a pen e o código do computador 12 (em `prototypes/campus-3d/campus_search.py`)

No jogo 3D a pen já não se recebe da Rita: procura-se na sala de estudo, clicando nos objetos. O computador 12 pede um código antes de mostrar os ficheiros. As respostas estão em `campus_search.py`, que só o servidor lê (nunca vai para a página).

- **Onde está a pen:** `pizza` (Caixa de pizza).
- **Código do computador 12:** `1710` (sábado, 17 de outubro). O Tomás diz a regra (fala `password`) e o dia descobre-se a perguntar ao grupo no computador 12 e a ver a Meteorologia e o Calendário do telemóvel (ver abaixo). A funcionária já não diz a data; ela continua no carimbo da fotografia original ("17.10") e no papel da grade depois das 22:25.
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

### A conversa no computador 12 e as apps do telemóvel (em `prototypes/campus-3d/campus_text.py` e `play.js`, specs/calendar-code.md)
Quem te segue: a **Rita** depois de encontrares a pen, a **Leonor** depois de aceitar ajudar (`ask_for_help`). Esperam junto do computador 12. O **Tomás** já está na sala de informática. Na conversa com o computador 12 há uma pergunta nova; cada pessoa presente responde à vez:
- Pergunta: "Perguntar ao grupo o que se lembram do dia da fotografia" / "Ask the group what they remember about the day of the photo"
- **Tomás** 🇵🇹 Estava um sol incrível. Lembro-me da Rita a queixar-se de que não via nada no ecrã do telemóvel.
  - 🇬🇧 The sun was incredible. I remember Rita complaining she could not see anything on her phone screen.
- **Rita** 🇵🇹 E foi num sábado. A faculdade estava vazia e ninguém nos mandou sair da sala.
  - 🇬🇧 And it was a Saturday. The faculty was empty and nobody told us to leave the room.
- **Leonor** 🇵🇹 Foi depois do teste de Finanças, a 15 de outubro. Lembro-me porque já estávamos todos mais descansados.
  - 🇬🇧 It was after the Finance test, on 15 October. I remember because we were all more relaxed by then.
- Se faltar alguém: Falta aqui gente do grupo. Quem não veio contigo não se pode lembrar de nada. / Some of the group are missing. Whoever did not come with you cannot remember anything.
- No fim: O teu telemóvel guarda o mês de outubro inteiro: a Meteorologia e o Calendário. / Your phone keeps the whole of October: the Weather and Calendar apps.
- **Meteorologia** (telemóvel, outubro inteiro): sol a 1, 3, 6, 10, 12, 17, 18, 21, 26 e 29 (a tabela `WEATHER` está em `play.js`). Sábados de sol: 3, 10 e 17.
- **Calendário** (telemóvel, outubro de 2026): 6 — Reunião do grupo; 13 — Reunião do grupo; 15 — Teste de Finanças; 20 — Reunião do grupo; 22 — Teste de Microeconomia; 27 — Reunião do grupo; 30 — Entrega do relatório intermédio.
- Sol + sábado = dias 3, 10 e 17; depois do teste de Finanças (dia 15) = **dia 17**. Sem a Leonor ficam os três sábados.
- O código escreve-se no campo de 4 algarismos. Cada código errado custa 2 minutos. / Every wrong code costs 2 minutes. Depois de 3 códigos errados: Três códigos errados. A fotografia original tinha um carimbo com a data no canto… / Three wrong codes. The original photo had a date stamp in the corner…

Nota: as ações "Abrir a gaveta do grupo" (Rita) e "Ver os ficheiros antigos" (computador 12) continuam em `story.py`, mas o jogo 3D não as mostra: usa a procura e o código.

## Provas, confrontos e audiência (em `prototypes/campus-3d/campus_case.py`)

Só o servidor lê este ficheiro. A página recebe uma carta quando a tens, e uma fala quando a mereceste.

### As provas (cartas)
| id | quando a tens | 🇵🇹 | 🇬🇧 |
|---|---|---|---|
| `original_photo` | tens o objeto `original_photo` (a fotografia triturada, reconstruída na reprografia) | A fotografia original, colada com fita-cola: quatro pessoas | The original photo, taped back together: four people |
| `files` | `files_viewed` = `True` | O histórico dos ficheiros: quatro autores em todas as cópias | The file history: four authors in every backup |
| `leonor_messages` | `colleague_choice` = `help` | As capturas de ecrã da Leonor: chegaram todas ontem à noite | Leonor's screenshots: every message arrived last night |
| `msg_1` … `msg_5` | `flagged_n` = `True` (na página, `n` é o número que o jogador vê no chat; o servidor converte-o) | 🚩 e o texto dessa mensagem do chat, lido de `story.py` | 🚩 and the text of that chat message, read from `story.py` |
| `tomas_word` | o Tomás cedeu esta noite (notas da noite) | A palavra do Tomás: nunca escreveu aquela mensagem e foi ele que fez os slides | Tomás's word: he never wrote that message and made the slides himself |
| `rita_word` | a Rita cedeu esta noite (notas da noite) | A palavra da Rita: contou quatro pessoas no dia da fotografia | Rita's word: she counted four people on the day of the photo |

### Quem cede, e com que prova
| pessoa | fala | provas que a fazem ceder | carta que ganhas |
|---|---|---|---|
| Tomás | `slides` | `msg_5` (a mensagem 5 da história, a que tem o nome dele e chegou ontem: na página é a `msg_1` no caso `tomas` e a `msg_4` no caso `rita`) | `tomas_word` |
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

**1. `name`** (fala o Duarte) — desfaz-se com `files` (e, no caso `tomas`, com `tomas_word`; no caso `rita`, com `rita_word`)
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

## Os três casos do dia (em `prototypes/campus-3d/campus_case.py`, `CASES`)

(specs/case-of-the-day.md e specs/culprit-of-the-night.md) Cada dia tem um caso, o mesmo para toda a gente nesse dia (hora de Lisboa). O jogo começa com a operação `begin` (o ecrã inicial mostra "Caso de 22 de novembro"); um jogo continuado fica com o seu caso, e "Jogar outra vez" joga o caso do dia de hoje. A operação `open` (todos os testes revistos) joga sempre o caso clássico. Os dias seguem a ordem `outsider`, `tomas`, `rita`: 22 de novembro de 2026 é `tomas`, 23 é `rita`, 24 é `outsider`.

O dia aparece no ecrã inicial, na barra de cima e no cartão de partilha (`📅 Caso de 22 de novembro`), com os textos de `campus_text.py`: `case_of_day` 🇵🇹 Caso de {d} de {month} / 🇬🇧 Case of {d} {month}, e `months` (janeiro … dezembro / January … December). Nunca diz o caso, o culpado nem o código.

A história joga-se sempre com as suas mensagens 1 a 5 (falsas: 2, 4 e 5). Um caso só muda a ordem em que o chat as mostra e alguns textos, à saída do servidor (`campus_evidence.retell`): a chave é o texto clássico exato e o valor é o que o caso diz em vez dele. A página só vê os números mostrados: as cartas `msg_n`, as ações `flag_n` e os títulos do diário usam o número do chat que o jogador vê. Se mudares uma fala clássica, a fala do caso deixa de ser usada (um teste falha): muda as duas.

| | `outsider` (clássico) | `tomas` | `rita` |
|---|---|---|---|
| chat como se vê (lugar → mensagem da história) | 1 2 3 4 5 | 5 1 2 3 4 | 2 4 3 5 1 |
| falsas, como se veem | 2, 4, 5 | 1, 3, 5 | 1, 2, 4 |
| o histórico dos ficheiros diz a conta | não | do Tomás | da Rita |
| quem mente | ninguém de propósito | Tomás (`who`, `msg5`, `slides`) | Rita (`pen`, `duarte`, `warned`) |
| data da fotografia, código | 14.11, `1411` | 10.11, `1011` | 13.11, `1311` |
| afirmação `name` desfaz-se com | `files` | `files`, `tomas_word` | `files`, `rita_word` |
| o colega que cede | testemunha / nunca escreveu | o Tomás confessa | a Rita confessa |

Os sinais contra quem mente, em cada caso: `tomas` — a conta do Tomás no histórico, e a Rita (`pen`) diz que ele foi sozinho para a sala de informática às onze e meia, quando ele (`who`) diz que nunca se aproximou do 12; `rita` — a conta da Rita, e o Tomás (`who`) viu uma camisola cor-de-rosa e cabelo comprido, quando ela (`pen`) diz que foi cedo para casa. O `fifth_element` tem o mesmo texto em todos os casos. Uma fala de "Quando foste rude" ganha sempre à do caso.

### Caso `tomas`: o Tomás deixou entrar o Duarte
- **Chat, mensagem 1 da história**
  - 🇵🇹 Rita, há 3 semanas, 21h05: "Alguém pode reservar a sala de estudo para quinta-feira?"  *(linha 322)*
  - 🇬🇧 Rita, 3 weeks ago, 9:05 pm: "Can someone book the study room for Thursday?"  *(linha 235)*
- **Chat, mensagem 2 da história**
  - 🇵🇹 Duarte, há 3 semanas, 21h07: "Já reservei. Também escrevi a conclusão, como sempre."  *(linha 324)*
  - 🇬🇧 Duarte, 3 weeks ago, 9:07 pm: "Booked it. I wrote the conclusion too, like always."  *(linha 237)*
- **Chat, mensagem 3 da história**
  - 🇵🇹 Leonor, há 2 semanas, 18h40: "A fotografia para a capa está pronta. Os quatro, finalmente!"  *(linha 326)*
  - 🇬🇧 Leonor, 2 weeks ago, 6:40 pm: "Photo for the cover is ready. Four of us, finally!"  *(linha 239)*
- **Chat, mensagem 4 da história**
  - 🇵🇹 Número desconhecido, há 3 semanas, 22h10: "Mal posso esperar para apresentarmos os cinco."  *(linha 328)*
  - 🇬🇧 Unknown number, 3 weeks ago, 10:10 pm: "Can't wait for the five of us to present."  *(linha 241)*
- **Computador 12, o código certo (comparar os ficheiros)**
  - 🇵🇹 Ligas a pen ao computador 12 e comparas. Nas cópias de segurança da pen, todas as versões têm quatro autores. Na pasta partilhada, a versão atual foi alterada ontem às 23h47, a partir deste mesmo computador, e a pasta diz de que conta: a do Tomás. Foi acrescentado "Duarte" ao relatório e trocada a fotografia. Recuperas a versão original do trabalho.  *(linha 331)*
  - 🇬🇧 You plug the USB stick into computer 12 and compare. In the backups on the USB stick, every version has four authors. In the shared folder, the current version was changed yesterday at 11:47 pm, from this same computer, and the folder says from which account: Tomás's. "Duarte" was added to the report and the photo was swapped. You recover the original version of the work.  *(linha 244)*
- **Sala de informática, depois de comparares os ficheiros**
  - 🇵🇹 Já comparaste os ficheiros: quatro autores em todas as cópias da pen, e uma alteração na pasta partilhada ontem às 23h47, feita a partir da conta do Tomás.  *(linha 333)*
  - 🇬🇧 You have compared the files: four authors in every copy on the USB stick, and a change in the shared folder yesterday at 11:47 pm, made from Tomás's account.  *(linha 246)*
- **Carta `files`**
  - 🇵🇹 O histórico dos ficheiros: quatro autores em todas as cópias, e o quinto nome acrescentado a partir da conta do Tomás  *(linha 336)*
  - 🇬🇧 The file history: four authors in every backup, and the fifth name added from Tomás's account  *(linha 249)*
- **Carta `tomas_word`**
  - 🇵🇹 A confissão do Tomás: acrescentou o Duarte ontem à noite e escreveu ele próprio a mensagem  *(linha 338)*
  - 🇬🇧 Tomás's confession: he added Duarte last night and wrote the message himself  *(linha 251)*
- **Rita, `pen`**
  - 🇵🇹 "A pen? Devia estar aqui, mas não a encontro." Olha para a mesa. "Ontem ficámos aqui até tarde a comer pizza. O Tomás foi sozinho para a sala de informática às onze e meia."  *(linha 341)*
  - 🇬🇧 "The USB stick? It should be here somewhere, but I can't find it." She looks at the table. "We stayed here late last night eating pizza. Tomás went off to the lab at half past eleven, on his own."  *(linha 254)*
  - 📓 Diário 🇵🇹 Rita: não encontra a pen. O grupo comeu pizza aqui ontem à noite; o Tomás foi sozinho para a sala de informática às onze e meia.  *(linha 343)*
  - 📓 Diário 🇬🇧 Rita cannot find the USB stick. The group ate pizza here last night; Tomás went to the lab alone at half past eleven.  *(linha 256)*
- **Tomás, `who`**
  - 🇵🇹 "Só vi um capuz. Como o que o Duarte usa." Não tira os olhos do ecrã. "Estive no computador 11 a noite toda. Nunca me aproximei do 12."  *(linha 346)*
  - 🇬🇧 "Only a hood. Like the one Duarte wears." He keeps his eyes on his screen. "I was at computer 11 all night. I never went near computer 12."  *(linha 259)*
  - 📓 Diário 🇵🇹 O Tomás diz que viu alguém de capuz no computador 12 perto da meia-noite e que ele próprio nunca se aproximou.  *(linha 348)*
  - 📓 Diário 🇬🇧 Tomás says he saw someone in a hood at computer 12 near midnight, and that he never went near it himself.  *(linha 261)*
- **Tomás, `msg5`**
  - 🇵🇹 "'Os slides foram do Duarte'? Escrevi isso há semanas. É verdade e pronto." Não olha para ti.  *(linha 350)*
  - 🇬🇧 "'Duarte did the slides'? I wrote that weeks ago. It is just true." He does not look at you.  *(linha 263)*
  - 📓 Diário 🇵🇹 O Tomás diz que escreveu a mensagem com o nome dele há semanas.  *(linha 352)*
  - 📓 Diário 🇬🇧 Tomás says he wrote the message with his name weeks ago.  *(linha 265)*
- **Tomás, `kind`: a resposta que leva a `msg5`**
  - 🇵🇹 Perguntar pela mensagem 1, a que tem o nome dele  *(linha 354)*
  - 🇬🇧 Ask about message 1, the one with his name  *(linha 267)*
- **Tomás, `slides`**
  - 🇵🇹 O Tomás não tira os olhos do ecrã. "Os slides? Foi o Duarte que os fez. Eu disse-o no chat, há três semanas."  *(linha 356)*
  - 🇬🇧 Tomás keeps his eyes on the screen. "The slides? Duarte made them. I said so in the chat, three weeks ago."  *(linha 269)*
  - 📓 Diário 🇵🇹 O Tomás diz que foi o Duarte que fez os slides e que o escreveu no chat há três semanas.  *(linha 358)*
  - 📓 Diário 🇬🇧 Tomás says Duarte made the slides, and that he wrote so in the chat three weeks ago.  *(linha 271)*
- **Quando cede: Tomás**
  - 🇵🇹 O Tomás lê a linha cinzenta mais pequena por baixo da mensagem. "Chegou ontem às 23h49." Fecha os olhos. "Escrevi-a ontem à noite. E pus o nome dele na capa às 23h47, no computador 12. Nunca fiz os slides. O Duarte disse que os fazia se o nome dele fosse para o relatório." Roda a cadeira para a parede de vidro. "Ele anda pelo corredor, sabes. Volta para o computador. Se ele vier, eu fico à porta. Devo-te isso."  *(linha 361)*
  - 🇬🇧 Tomás reads the small grey line under his message. "Arrived yesterday, 11:49 pm." He closes his eyes. "I wrote it last night. And I put his name on the cover at 11:47, from computer 12. I never made the slides. Duarte said he would make them if his name went on the report." He turns his chair to face the glass wall. "He walks the corridor, you know. Go back to the computer. If he comes, I will be standing in the door. I owe you that."  *(linha 274)*
  - 📓 Diário 🇵🇹 O Tomás confessou: acrescentou o Duarte ontem à noite, no computador 12, e escreveu ele próprio a mensagem. Fica a vigiar o corredor por ti.  *(linha 363)*
  - 📓 Diário 🇬🇧 Tomás confessed: he added Duarte last night, from computer 12, and wrote the message himself. He is watching the corridor for you.  *(linha 276)*
- **Quando cede: Leonor**
  - 🇵🇹 Contas-lhe o que o Tomás te disse. A Leonor fica com o polegar parado no ecrã. "Foi o Tomás?" Volta atrás na conversa, mais devagar. "Então já não sei o que é que andei a ler."  *(linha 365)*
  - 🇬🇧 You tell her what Tomás told you. Leonor stops with her thumb on the screen. "Tomás did this?" She scrolls back, slower this time. "Then I do not know what I have been reading."  *(linha 278)*
  - 📓 Diário 🇵🇹 A Leonor não sabia que tinha sido o Tomás a acrescentar o Duarte. Ficou abalada.  *(linha 367)*
  - 📓 Diário 🇬🇧 Leonor did not know that Tomás added Duarte. It shook her.  *(linha 280)*
- **Quando cede: Rita**
  - 🇵🇹 A Rita olha da tua prova para o ecrã e outra vez para a prova. "Então a fotografia mudou mesmo." Ri-se uma vez, sem alegria nenhuma. "Eu contei quatro. Disse-o em voz alta, nesse dia, a todos vocês." Fecha o portátil. "Diz ao professor que eu contei. Eu digo-lho na cara."  *(linha 369)*
  - 🇬🇧 Rita looks from your proof to her screen and back. "So the photo did change." She laughs once, without any joy. "I counted four. I said it out loud, on the day, to all of you." She closes the laptop. "Tell the professor I counted. I will say it to his face."  *(linha 282)*
  - 📓 Diário 🇵🇹 A Rita contou quatro pessoas no dia da fotografia. Vai dizê-lo ao professor.  *(linha 371)*
  - 📓 Diário 🇬🇧 Rita counted four people on the day of the photo. She will tell the professor.  *(linha 284)*
- **Leonor, `mine`**
  - 🇵🇹 "A da fotografia da capa. Escrevi-a na noite em que a tirámos." A Leonor percorre o ecrã com um dedo. "As do número que eu não conhecia chegaram todas com minutos de diferença, ontem à noite."  *(linha 374)*
  - 🇬🇧 "The one about the cover photo. I wrote that the evening we took it." Leonor scrolls with one finger. "The ones from the number I did not know all arrived within minutes of each other, last night."  *(linha 287)*
  - 📓 Diário 🇵🇹 A Leonor escreveu ela própria a mensagem do chat sobre a fotografia da capa.  *(linha 376)*
  - 📓 Diário 🇬🇧 Leonor wrote the chat message about the cover photo herself.  *(linha 289)*
- **Duarte, `part`**
  - 🇵🇹 "Os slides, claro. Pergunta ao Tomás, ele diz-te." Hesita por um segundo.  *(linha 378)*
  - 🇬🇧 "The slides, of course. Ask Tomás, he will tell you." He hesitates for a second.  *(linha 291)*
- **Funcionária, `order`**
  - 🇵🇹 "A 10 de novembro, tiraram a fotografia e mandaram-na imprimir no mesmo dia. Eram quatro pessoas, ainda me lembro, e acho que o ficheiro original do pedido ainda está guardado."  *(linha 381)*
  - 🇬🇧 "On 10 November, you took the photo and had it printed the same day. I remember there were four people in it, and I think the original order file is still saved."  *(linha 294)*
  - 📓 Diário 🇵🇹 A fotografia da capa foi tirada e impressa a 10 de novembro. A reprografia ainda tem o ficheiro original do pedido.  *(linha 383)*
  - 📓 Diário 🇬🇧 The cover photo was taken and printed on 10 November. The print shop still has the original order file.  *(linha 296)*
- **Funcionária, `again`**
  - 🇵🇹 A funcionária fica com a mão parada na impressora. "Dez de novembro. Sim. Como é que tu...?" Olha para o relógio. "Há muito tempo que estou a fechar daqui a dez minutos." Franze a testa para o balcão. "Estranho. Não me lembro de te ver sair."  *(linha 385)*
  - 🇬🇧 The clerk stops with her hand on the printer. "The tenth of November. Yes. How do you...?" She looks at the clock. "I have been closing in ten minutes for a very long time." She frowns at the counter. "Odd. I do not remember you leaving."  *(linha 298)*
  - 📓 Diário 🇵🇹 A funcionária confirmou a data antes de acabares de a dizer: a fotografia da capa foi impressa a 10 de novembro.  *(linha 387)*
  - 📓 Diário 🇬🇧 The clerk agreed with the date before you finished saying it: the cover photo was printed on 10 November.  *(linha 300)*
- **Papel na grade da reprografia, depois das 22:25 (`SHUTTER`)**
  - 🇵🇹 A grade está descida e o balcão às escuras. A funcionária foi para casa às 22:25. Há um papel colado na grade: fotografia da capa, pedido de 10 de novembro, levantar amanhã.  *(linha 389)*
  - 🇬🇧 The shutter is down and the counter is dark. The clerk went home at 22:25. A slip is taped to the shutter: cover photo, order of 10 November, collect tomorrow.  *(linha 302)*
- **Fotografia colada (`PHOTO_TEXT`)**
  - 🇵🇹 O último pedaço encaixa. Na fotografia original estão quatro pessoas, e no canto o carimbo da data diz 10.11. A funcionária cola os pedaços com fita-cola e dá-te a fotografia.  *(linha 391)*
  - 🇬🇧 The last piece fits. In the original photo there are four of you, and in the corner the date stamp says 10.11. The clerk tapes the pieces together and hands you the photo.  *(linha 304)*
- **Audiência, afirmação 3. `messages`, certa com `tomas_word` (professor)**
  - 🇵🇹 "O autor diz-me que a escreveu ontem à noite. Uma mensagem escrita ontem não prova nada sobre há três semanas."  *(linha 394)*
  - 🇬🇧 "Its author tells me he wrote it last night. A message written yesterday proves nothing about three weeks ago."  *(linha 307)*
- **Final `full_case`**
  - 🇵🇹 Mostras o histórico da pen e as três mensagens que marcaste: uma do próprio Duarte, semanas antes de alguém ter ouvido falar dele; uma de um número que ninguém conhecia, a contar cinco; e uma com o nome do Tomás que chegou ontem à noite, dois minutos depois de a conta dele ter alterado a pasta partilhada. A Leonor entra com as mensagens originais, e batem certo. Antes de o professor perguntar, o Tomás levanta-se e conta o que fez: o nome, a fotografia e a mensagem, tudo por uns slides que nunca fez. O professor risca o quinto nome da lista. Amanhã apresentam os quatro, e o Tomás apresenta os slides que acaba esta noite.  *(linha 397)*
  - 🇬🇧 You show the history on the USB stick and the three messages you flagged: one from Duarte himself, weeks before anyone had heard of him; one from a number nobody knew, counting five of you; and one under Tomás's name that arrived last night, two minutes after his own account changed the shared folder. Leonor walks in with the original messages, and they match. Before the professor can ask, Tomás stands up and tells the room what he did: the name, the photo and the message, all for slides he never made. The professor crosses the fifth name off the list. Tomorrow, the four of you present, and Tomás presents the slides he finishes tonight.  *(linha 310)*
- **Final `impostor`**
  - 🇵🇹 Mostras o histórico da pen: quatro autores até ontem à noite, e a última alteração feita a partir da conta do Tomás. A Leonor entra e entrega as mensagens que guardou: foram todas enviadas na mesma noite, com datas falsas. O professor risca o quinto nome da lista. O Duarte sai do auditório sem dizer nada, e o Tomás não olha para nenhum de vocês. Amanhã apresentam os quatro.  *(linha 399)*
  - 🇬🇧 You show the history on the USB stick: four authors until last night, and the last change made from Tomás's account. Leonor walks in and hands over the messages she kept: they were all sent on the same night, with fake dates. The professor crosses the fifth name off the list. Duarte leaves the auditorium without a word, and Tomás does not look at any of you. Tomorrow, the four of you present.  *(linha 312)*
- **Final `stolen_credits`**
  - 🇵🇹 Mostras o histórico da pen: o trabalho original tinha quatro autores até ontem à noite. Mas o Duarte levanta o telemóvel: "Tenho mensagens de todos a provar que participei." O Tomás acena que sim, depressa demais. Sem as mensagens originais, não consegues provar que são falsas. O professor suspira: "Sem provas de que as mensagens são falsas, o nome fica." Amanhã apresentam os cinco.  *(linha 401)*
  - 🇬🇧 You show the history on the USB stick: the original work had four authors until last night. But Duarte raises his phone: "I have messages from everyone proving I took part." Tomás nods along, a little too fast. Without the original messages, you cannot prove they are fake. The professor sighs: "Without proof that the messages are fake, the name stays." Tomorrow, the five of you present.  *(linha 314)*
- **Final verdadeiro, a frase de quem entra (o resto do texto não muda)**
  - 🇵🇹 O Tomás entra primeiro, com os slides que finalmente acabou esta noite, sem olhar para ti; depois a Leonor com o telemóvel, e a Rita a contar baixinho.  *(linha 404)*
  - 🇬🇧 Tomás comes in first, with the slides he finally finished tonight, and does not look at you; then Leonor with her phone, and Rita counting under her breath.  *(linha 317)*
- **Audiência, afirmação 1. `name`, certa com `tomas_word` (professor; fala nova, só neste caso)**
  - 🇵🇹 "Quem pôs lá o nome já mo disse ele próprio. Lá se vai o 'desde o primeiro rascunho'."  *(linha 230)*
  - 🇬🇧 "The person who put the name there has told me so himself. So much for 'since the first draft'."  *(linha 229)*

### Caso `rita`: a Rita deixou entrar o Duarte
- **Chat, mensagem 1 da história**
  - 🇵🇹 Tomás, há 3 semanas, 21h05: "Alguém pode reservar a sala de estudo para quinta-feira?"  *(linha 497)*
  - 🇬🇧 Tomás, 3 weeks ago, 9:05 pm: "Can someone book the study room for Thursday?"  *(linha 420)*
- **Chat, mensagem 3 da história**
  - 🇵🇹 Leonor, há 2 semanas, 18h40: "A fotografia para a capa está pronta. Os quatro, finalmente!"  *(linha 326)*
  - 🇬🇧 Leonor, 2 weeks ago, 6:40 pm: "Photo for the cover is ready. Four of us, finally!"  *(linha 239)*
- **Computador 12, o código certo (comparar os ficheiros)**
  - 🇵🇹 Ligas a pen ao computador 12 e comparas. Nas cópias de segurança da pen, todas as versões têm quatro autores. Na pasta partilhada, a versão atual foi alterada ontem às 23h47, a partir deste mesmo computador, e a pasta diz de que conta: a da Rita. Foi acrescentado "Duarte" ao relatório e trocada a fotografia. Recuperas a versão original do trabalho.  *(linha 502)*
  - 🇬🇧 You plug the USB stick into computer 12 and compare. In the backups on the USB stick, every version has four authors. In the shared folder, the current version was changed yesterday at 11:47 pm, from this same computer, and the folder says from which account: Rita's. "Duarte" was added to the report and the photo was swapped. You recover the original version of the work.  *(linha 425)*
- **Sala de informática, depois de comparares os ficheiros**
  - 🇵🇹 Já comparaste os ficheiros: quatro autores em todas as cópias da pen, e uma alteração na pasta partilhada ontem às 23h47, feita a partir da conta da Rita.  *(linha 504)*
  - 🇬🇧 You have compared the files: four authors in every copy on the USB stick, and a change in the shared folder yesterday at 11:47 pm, made from Rita's account.  *(linha 427)*
- **Carta `files`**
  - 🇵🇹 O histórico dos ficheiros: quatro autores em todas as cópias, e o quinto nome acrescentado a partir da conta da Rita  *(linha 507)*
  - 🇬🇧 The file history: four authors in every backup, and the fifth name added from Rita's account  *(linha 430)*
- **Carta `rita_word`**
  - 🇵🇹 A confissão da Rita: acrescentou o Duarte e trocou a fotografia ontem à noite  *(linha 509)*
  - 🇬🇧 Rita's confession: she added Duarte and swapped the photo last night  *(linha 432)*
- **Rita, `pen`**
  - 🇵🇹 "A pen? Não faço ideia." Olha para a mesa e depois desvia o olhar. "Ontem fui cedo para casa. Os outros ficaram aqui a comer pizza."  *(linha 512)*
  - 🇬🇧 "The USB stick? No idea." She looks at the table, then away. "I went home early last night. The others stayed here eating pizza."  *(linha 435)*
  - 📓 Diário 🇵🇹 A Rita diz que ontem foi cedo para casa, enquanto os outros comiam pizza aqui, e que não sabe onde está a pen.  *(linha 514)*
  - 📓 Diário 🇬🇧 Rita says she went home early last night, while the others ate pizza here, and does not know where the USB stick is.  *(linha 437)*
- **Rita, `duarte`**
  - 🇵🇹 "O Duarte? É... simpático. Fez a parte dele." Volta para o portátil um bocadinho depressa demais.  *(linha 516)*
  - 🇬🇧 "Duarte? He is... fine. He did his part." She goes back to her laptop a little too quickly.  *(linha 439)*
- **Rita, `warned`**
  - 🇵🇹 A Rita fica muito quieta. "Ontem à noite? Ontem à noite eu estava em casa."  *(linha 518)*
  - 🇬🇧 Rita goes very still. "Last night? I was at home last night."  *(linha 441)*
  - 📓 Diário 🇵🇹 A Rita diz que ontem à noite estava em casa.  *(linha 520)*
  - 📓 Diário 🇬🇧 Rita says she was at home last night.  *(linha 443)*
- **Tomás, `who`**
  - 🇵🇹 "Cabelo comprido e uma camisola cor-de-rosa. Pensei que era a Rita, mas ela tinha dito que ia cedo para casa."  *(linha 523)*
  - 🇬🇧 "Long hair and a pink jumper. I thought it was Rita, but she told us she was going home early."  *(linha 446)*
  - 📓 Diário 🇵🇹 O Tomás viu alguém de cabelo comprido e camisola cor-de-rosa no computador 12 perto da meia-noite. Pensou que era a Rita.  *(linha 525)*
  - 📓 Diário 🇬🇧 Tomás saw someone with long hair and a pink jumper at computer 12 near midnight. He thought it was Rita.  *(linha 448)*
- **Tomás, `kind`: a resposta que leva a `msg5`**
  - 🇵🇹 Perguntar pela mensagem 4, a que tem o nome dele  *(linha 527)*
  - 🇬🇧 Ask about message 4, the one with his name  *(linha 450)*
- **Tomás, `msg5`**
  - 📓 Diário 🇵🇹 O Tomás não se lembra de ter escrito a mensagem 4; chegou-lhe ao telemóvel ontem à noite.  *(linha 529)*
  - 📓 Diário 🇬🇧 Tomás does not remember writing message 4; it reached his phone last night.  *(linha 452)*
- **Quando cede: Tomás**
  - 🇵🇹 O Tomás lê a linha por baixo do nome dele e depois a linha cinzenta mais pequena. "Chegou ontem às 23h49. Às 23h49 eu estava aqui sentado, no computador ao lado de quem estava no computador 12. Não escrevi uma palavra." Baixa a voz. "Eu nunca enviei isto. E os slides... fui eu que fiz os slides. Os onze. Fiquei aqui até às duas na terça-feira." Roda a cadeira para a parede de vidro. "Ele anda pelo corredor, sabes. Volta para o computador. Se ele vier, eu fico à porta."  *(linha 531)*
  - 🇬🇧 Tomás reads the line under his name, then the small grey line beneath it. "Arrived yesterday, 11:49 pm. At 11:49 I was sitting right here, one computer away from whoever was at computer 12. I did not type a word." His voice drops. "I never sent that. And the slides... I made the slides. All eleven. I was here until two on Tuesday." He turns his chair to face the glass wall. "He walks the corridor, you know. Go back to the computer. If he comes, I will be standing in the door."  *(linha 454)*
- **Quando cede: Rita**
  - 🇵🇹 A Rita olha da tua prova para o ecrã e outra vez para a prova, e o sorriso desaparece. "Fui eu que o pus lá." Di-lo muito baixinho. "Ontem à noite, no computador 12. Ele precisava de um grupo com boa nota, e eu disse que sim antes de perguntar a algum de vocês." Fecha o portátil. "Diz ao professor. Eu digo-lho na cara."  *(linha 534)*
  - 🇬🇧 Rita looks from your proof to her screen and back, and the smile goes. "I put him there." She says it very quietly. "Last night, at computer 12. He needed a group with a good grade, and I said yes before I asked any of you." She closes the laptop. "Tell the professor. I will say it to his face."  *(linha 457)*
  - 📓 Diário 🇵🇹 A Rita confessou: acrescentou o Duarte e trocou a fotografia ontem à noite, no computador 12. Vai dizê-lo ao professor.  *(linha 536)*
  - 📓 Diário 🇬🇧 Rita confessed: she added Duarte and swapped the photo last night, from computer 12. She will tell the professor.  *(linha 459)*
- **Leonor, `mine`**
  - 🇵🇹 "A da fotografia da capa. Escrevi-a na noite em que a tirámos." A Leonor percorre o ecrã com um dedo. "As do número que eu não conhecia chegaram todas com minutos de diferença, ontem à noite."  *(linha 374)*
  - 🇬🇧 "The one about the cover photo. I wrote that the evening we took it." Leonor scrolls with one finger. "The ones from the number I did not know all arrived within minutes of each other, last night."  *(linha 287)*
  - 📓 Diário 🇵🇹 A Leonor escreveu ela própria a mensagem do chat sobre a fotografia da capa.  *(linha 376)*
  - 📓 Diário 🇬🇧 Leonor wrote the chat message about the cover photo herself.  *(linha 289)*
- **Duarte, `part`**
  - 🇵🇹 "Os slides, claro. Pergunta à Rita, ela sabe." Hesita por um segundo.  *(linha 543)*
  - 🇬🇧 "The slides, of course. Ask Rita, she knows." He hesitates for a second.  *(linha 466)*
- **Funcionária, `order`**
  - 🇵🇹 "A 13 de novembro, tiraram a fotografia e mandaram-na imprimir no mesmo dia. Eram quatro pessoas, ainda me lembro, e acho que o ficheiro original do pedido ainda está guardado."  *(linha 546)*
  - 🇬🇧 "On 13 November, you took the photo and had it printed the same day. I remember there were four people in it, and I think the original order file is still saved."  *(linha 469)*
  - 📓 Diário 🇵🇹 A fotografia da capa foi tirada e impressa a 13 de novembro. A reprografia ainda tem o ficheiro original do pedido.  *(linha 548)*
  - 📓 Diário 🇬🇧 The cover photo was taken and printed on 13 November. The print shop still has the original order file.  *(linha 471)*
- **Funcionária, `again`**
  - 🇵🇹 A funcionária fica com a mão parada na impressora. "Treze de novembro. Sim. Como é que tu...?" Olha para o relógio. "Há muito tempo que estou a fechar daqui a dez minutos." Franze a testa para o balcão. "Estranho. Não me lembro de te ver sair."  *(linha 550)*
  - 🇬🇧 The clerk stops with her hand on the printer. "The thirteenth of November. Yes. How do you...?" She looks at the clock. "I have been closing in ten minutes for a very long time." She frowns at the counter. "Odd. I do not remember you leaving."  *(linha 473)*
  - 📓 Diário 🇵🇹 A funcionária confirmou a data antes de acabares de a dizer: a fotografia da capa foi impressa a 13 de novembro.  *(linha 552)*
  - 📓 Diário 🇬🇧 The clerk agreed with the date before you finished saying it: the cover photo was printed on 13 November.  *(linha 475)*
- **Papel na grade da reprografia, depois das 22:25 (`SHUTTER`)**
  - 🇵🇹 A grade está descida e o balcão às escuras. A funcionária foi para casa às 22:25. Há um papel colado na grade: fotografia da capa, pedido de 13 de novembro, levantar amanhã.  *(linha 554)*
  - 🇬🇧 The shutter is down and the counter is dark. The clerk went home at 22:25. A slip is taped to the shutter: cover photo, order of 13 November, collect tomorrow.  *(linha 477)*
- **Fotografia colada (`PHOTO_TEXT`)**
  - 🇵🇹 O último pedaço encaixa. Na fotografia original estão quatro pessoas, e no canto o carimbo da data diz 13.11. A funcionária cola os pedaços com fita-cola e dá-te a fotografia.  *(linha 556)*
  - 🇬🇧 The last piece fits. In the original photo there are four of you, and in the corner the date stamp says 13.11. The clerk tapes the pieces together and hands you the photo.  *(linha 479)*
- **Audiência, afirmação 2. `photo`, certa com `rita_word` (professor)**
  - 🇵🇹 "Quem a trocou diz-me o que lá estava antes: quatro pessoas. Ouço-a amanhã."  *(linha 559)*
  - 🇬🇧 "The one who swapped it tells me what was there before: four people. I will hear her tomorrow."  *(linha 482)*
- **Final `full_case`**
  - 🇵🇹 Mostras o histórico da pen e as três mensagens que marcaste: uma de um número que ninguém conhecia; uma do Duarte, a contar cinco quando eram quatro; e uma com o nome do Tomás que chegou ontem à noite, dois minutos depois de a conta da Rita ter alterado a pasta partilhada. A Leonor entra com as mensagens originais, e batem certo. A Rita não espera que lhe perguntem: conta ao professor que acrescentou o nome e trocou a fotografia, porque o Duarte precisava de um grupo. O professor risca o quinto nome da lista. Amanhã apresentam os quatro, e a Rita tem muito que explicar pelo caminho.  *(linha 562)*
  - 🇬🇧 You show the history on the USB stick and the three messages you flagged: one from a number nobody knew; one from Duarte, counting five of you when there were four; and one under Tomás's name that arrived last night, two minutes after Rita's account changed the shared folder. Leonor walks in with the original messages, and they match. Rita does not wait to be asked: she tells the professor that she added the name and swapped the photo, because Duarte needed a group. The professor crosses the fifth name off the list. Tomorrow, the four of you present, and Rita has a lot to explain on the way there.  *(linha 485)*
- **Final `impostor`**
  - 🇵🇹 Mostras o histórico da pen: quatro autores até ontem à noite, e a última alteração feita a partir da conta da Rita. A Leonor entra e entrega as mensagens que guardou: foram todas enviadas na mesma noite, com datas falsas. O professor risca o quinto nome da lista. O Duarte sai do auditório sem dizer nada, e a Rita fica a olhar para o chão. Amanhã apresentam os quatro.  *(linha 564)*
  - 🇬🇧 You show the history on the USB stick: four authors until last night, and the last change made from Rita's account. Leonor walks in and hands over the messages she kept: they were all sent on the same night, with fake dates. The professor crosses the fifth name off the list. Duarte leaves the auditorium without a word, and Rita stares at the floor. Tomorrow, the four of you present.  *(linha 487)*
- **Final `stolen_credits`**
  - 🇵🇹 Mostras o histórico da pen: o trabalho original tinha quatro autores até ontem à noite. Mas o Duarte levanta o telemóvel: "Tenho mensagens de todos a provar que participei." A Rita olha para as mãos. Sem as mensagens originais, não consegues provar que são falsas. O professor suspira: "Sem provas de que as mensagens são falsas, o nome fica." Amanhã apresentam os cinco.  *(linha 566)*
  - 🇬🇧 You show the history on the USB stick: the original work had four authors until last night. But Duarte raises his phone: "I have messages from everyone proving I took part." Rita looks down at her hands. Without the original messages, you cannot prove they are fake. The professor sighs: "Without proof that the messages are fake, the name stays." Tomorrow, the five of you present.  *(linha 489)*
- **Final verdadeiro, a frase de quem entra (o resto do texto não muda)**
  - 🇵🇹 A Leonor entra com o telemóvel, o Tomás com os slides e, por último, devagar, a Rita, a contar baixinho.  *(linha 569)*
  - 🇬🇧 Leonor comes in with her phone, Tomás with his slides, and Rita last of all, slowly, counting under her breath.  *(linha 492)*
- **Audiência, afirmação 1. `name`, certa com `rita_word` (professor; fala nova, só neste caso)**
  - 🇵🇹 "Quem pôs lá o nome já mo disse ela própria. Continue."  *(linha 415)*
  - 🇬🇧 "The person who put the name there has told me so herself. Go on."  *(linha 414)*

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
