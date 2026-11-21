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

**Legenda:** *confiança* são os corações (0 a 3; com 0 a pessoa acaba a conversa). *Diário* é a nota que fica guardada no diário do telemóvel. "→ fim" acaba a conversa.

## Rita
Onde está: **Sala de estudo** (`study_room`).

### `start`
- 🇵🇹 A Rita levanta os olhos do portátil. "Estás com um ar péssimo. Dormiste alguma coisa?"  *(linha 164)*
- 🇬🇧 Rita looks up from her laptop. "You look awful. Did you sleep at all?"  *(linha 48)*
- Respostas:
  - "Perguntar pela fotografia do grupo" / "Ask about the group photo" → `photo`
  - "Perguntar o que ela se lembra do Duarte" / "Ask what she remembers about Duarte" → `duarte`
  - "Perguntar pelas mensagens do chat" / "Ask about the chat messages" → `chat` *(só aparece se `files_viewed` = `True`)*
  - "Até já." / "Goodbye." → fim

### `photo`
- 🇵🇹 "A fotografia? Tirámo-la depois da última reunião. Quatro pessoas, a Leonor ficou com o temporizador. Lembro-me de contar as cabeças."  *(linha 170)*
- 🇬🇧 "The photo? We took it after the last meeting. Four of us, Leonor held the timer. I remember counting heads."  *(linha 54)*
- 📓 Diário: A Rita lembra-se de quatro pessoas na fotografia do grupo. / Rita remembers four people in the group photo.
- Respostas:
  - "Até já." / "Goodbye." → fim

### `duarte`
- 🇵🇹 "O Duarte... sinceramente, não o consigo imaginar. Sempre que tento, só vejo o nome na capa."  *(linha 173)*
- 🇬🇧 "Duarte... honestly, I cannot picture him. Every time I try, I only see the name on the cover."  *(linha 57)*
- Respostas:
  - "Dizer que achas que o nome foi acrescentado ontem à noite" / "Say you think the name was added last night" → `warned`

### `warned`
- 🇵🇹 A Rita fica calada. "Se for verdade, alguém quis que duvidássemos de nós próprios."  *(linha 175)*
- 🇬🇧 Rita goes quiet. "If that is true, somebody wanted us to doubt ourselves."  *(linha 59)*
- 📓 Diário: A Rita também desconfia do quinto nome. / Rita doubts the fifth name too.
- Respostas:
  - "Até já." / "Goodbye." → fim

### `chat`
- 🇵🇹 "Repara na hora a que as mensagens chegam. Algumas dizem há três semanas, mas no meu telemóvel aparecem como novas, de ontem à noite. Mensagens antigas não funcionam assim."  *(linha 178)*
- 🇬🇧 "Look at when the messages arrive. Some say three weeks ago, but my phone shows them as new, last night. That is not how old messages work."  *(linha 62)*
- 📓 Diário: Rita: uma mensagem antiga não chega como nova. Compara as horas de chegada no chat do grupo. / Rita: an old message does not arrive as new. Compare the arrival times in the group chat.
- Respostas:
  - "Até já." / "Goodbye." → fim

### Ações feitas a falar com Rita (em `story.py`)
- **▶ Abrir a gaveta do grupo** / Open the group drawer (`open_drawer`)
  - Se resultar 🇵🇹: Encontras a pen onde o grupo guardava as cópias de segurança do projeto. Guardas a pen.
  - Se resultar 🇬🇧: You find the USB stick where the group kept the project backups. You take the USB stick.

## Amélia
Onde está: **Reprografia** (`print_shop`).

### `start`
- 🇵🇹 A funcionária ajeita os óculos. "Fechamos daqui a dez minutos. Do que precisas?"  *(linha 183)*
- 🇬🇧 The clerk adjusts her glasses. "We close in ten minutes. What do you need?"  *(linha 67)*
- Respostas:
  - "Perguntar pelo pedido da fotografia da capa" / "Ask about the cover photo order" → `order`
  - "Perguntar se mais alguém veio perguntar" / "Ask if anyone else came asking" → `visitor`
  - "Até já." / "Goodbye." → fim

### `order`
- 🇵🇹 "Na semana passada. Quatro pessoas na fotografia, lembro-me porque tive de cortar a impressão. O ficheiro original do pedido ainda está guardado."  *(linha 188)*
- 🇬🇧 "Last week. Four people in the photo, I remember because I had to crop the print. The original order file is still saved."  *(linha 72)*
- 📓 Diário: A reprografia ainda tem o ficheiro original do pedido. / The print shop still has the original order file.
- Respostas:
  - "Até já." / "Goodbye." → fim

### `visitor`
- 🇵🇹 "Ontem ao fim da tarde passou por aqui um rapaz de capuz. Pediu para reimprimir a capa com outra fotografia."  *(linha 191)*
- 🇬🇧 "A young man in a hood came by yesterday evening. He asked to reprint the cover with a different photo."  *(linha 75)*
- 📓 Diário: Um desconhecido de capuz pediu à reprografia para mudar a fotografia da capa. / A hooded stranger asked the print shop to change the cover photo.
- Respostas:
  - "Perguntar como era ele" / "Ask what he looked like" → `hood`

### `hood`
- 🇵🇹 "Um sorriso calmo. Não quis deixar o nome. Pensei que fosse do vosso grupo."  *(linha 194)*
- 🇬🇧 "A calm smile. He did not want to leave a name. I thought he was one of your group."  *(linha 78)*
- Respostas:
  - "Até já." / "Goodbye." → fim

### Ações feitas a falar com Amélia (em `story.py`)
- **▶ Pedir uma cópia do pedido original** / Ask for a copy of the original order (`request_copy`)
  - Se resultar 🇵🇹: A funcionária volta a imprimir o ficheiro que ficou guardado no pedido. Na fotografia original estão quatro pessoas. Guardas a fotografia.
  - Se resultar 🇬🇧: The clerk prints again the file that was saved with the order. The original photo shows four people. You take the photo.

## Leonor
Onde está: **Biblioteca** (`library`).

### `start` — confiança 2
- 🇵🇹 A Leonor fecha o livro devagar. "Vens por causa do Duarte. Eu sei."  *(linha 198)*
- 🇬🇧 Leonor closes her book slowly. "You are here about Duarte. I know."  *(linha 82)*
- Respostas:
  - "Perguntar se tem a certeza de que ele estava no grupo" / "Ask if she is sure he was in the group" → `sure`
  - "Dizer-lhe que tens dúvidas" / "Tell her you have doubts" → `soft`
  - "Dizer que ela está a mentir" / "Say she is lying" → `harsh`
  - "Até já." / "Goodbye." → fim

### `sure` — confiança 2
- 🇵🇹 "Está em todas as mensagens há semanas. Tenho-as aqui." Toca no telemóvel.  *(linha 204)*
- 🇬🇧 "He has been in every message for weeks. I have them right here." She taps her phone.  *(linha 88)*
- Respostas:
  - "Pedir para ver as mensagens" / "Ask to see the messages" → `messages`

### `messages` — confiança 3
- 🇵🇹 "Olha. Todas de um número que eu não conhecia. Algumas têm data de há semanas, mas chegaram ontem à noite."  *(linha 206)*
- 🇬🇧 "Look. All from a number I did not know. Some are dated weeks ago, but they arrived last night."  *(linha 90)*
- 📓 Diário: A Leonor recebeu as mensagens do Duarte ontem à noite, de um número desconhecido. / Leonor received Duarte's messages last night, from an unknown number.
- Respostas:
  - "Até já." / "Goodbye." → fim

### `soft` — confiança 3
- 🇵🇹 "Eu queria acreditar em ti." Olha para o telemóvel. "Talvez devesse ver outra vez."  *(linha 209)*
- 🇬🇧 "I wanted to believe you." She looks at her phone. "Maybe I should look again."  *(linha 93)*
- Respostas:
  - "Pedir para ver as mensagens" / "Ask to see the messages" → `messages`

### `harsh` — confiança 1
- 🇵🇹 "Desculpa?" A voz dela endurece.  *(linha 211)*
- 🇬🇧 "Excuse me?" Her voice hardens.  *(linha 95)*
- Respostas:
  - "Pedir desculpa" / "Apologise" → `soft`
  - "Insistir" / "Insist" → `closed`

### `closed` — confiança 0
- 🇵🇹 A Leonor levanta-se. "Volta com provas, não com acusações."  *(linha 214)*
- 🇬🇧 Leonor stands up. "Come back with proof, not accusations."  *(linha 98)*
- Respostas:
  - "Sair." / "Leave." → fim

### Ações feitas a falar com Leonor (em `story.py`)
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
- 🇵🇹 O Tomás está curvado sobre o computador 11, a evitar o teu olhar. "Ah. Olá. Já é tarde."  *(linha 217)*
- 🇬🇧 Tomás is hunched over computer 11, avoiding your eyes. "Oh. Hi. It is late."  *(linha 101)*
- Respostas:
  - "Perguntar com calma o que está ali a fazer" / "Ask kindly what he is doing here" → `kind`
  - "Exigir saber porque mentiu sobre o Duarte" / "Demand to know why he lied about Duarte" → `hard`
  - "Mostrar-lhe a fotografia original" / "Show him the original photo" → `photo` *(só aparece se tens `original_photo`)*
  - "Até já." / "Goodbye." → fim

### `kind` — confiança 3
- 🇵🇹 "Não conseguia dormir. Vim acabar os slides. E... vi alguém no computador 12 ontem à noite, perto da meia-noite."  *(linha 223)*
- 🇬🇧 "Could not sleep. I came to finish the slides. And... I saw someone at computer 12 last night, near midnight."  *(linha 107)*
- Respostas:
  - "Perguntar quem era" / "Ask who it was" → `who`
  - "Perguntar pela mensagem 5, a que tem o nome dele" / "Ask about message 5, the one with his name" → `msg5` *(só aparece se `files_viewed` = `True`)*

### `who` — confiança 3
- 🇵🇹 "Só vi um capuz. Como o que o Duarte usa. Mas ninguém o viu chegar."  *(linha 226)*
- 🇬🇧 "Only a hood. Like the one Duarte wears. But nobody ever saw him arrive."  *(linha 110)*
- 📓 Diário: O Tomás viu alguém de capuz no computador 12 perto da meia-noite. / Tomás saw someone in a hood at computer 12 near midnight.
- Respostas:
  - "Até já." / "Goodbye." → fim

### `msg5` — confiança 3
- 🇵🇹 "'O Duarte fez os slides'? Eu nunca escrevi isso. O meu telemóvel apitou com ela à meia-noite, como se tivesse sido enviada há três semanas."  *(linha 229)*
- 🇬🇧 "'Duarte did the slides'? I never wrote that. My phone buzzed with it at midnight, as if it was sent three weeks ago."  *(linha 113)*
- 📓 Diário: O Tomás diz que nunca escreveu a mensagem 5; chegou ontem à noite. / Tomás says he never wrote message 5; it arrived last night.
- Respostas:
  - "Até já." / "Goodbye." → fim

### `hard` — confiança 1
- 🇵🇹 "Como? Eu não menti!" A voz dele treme.  *(linha 232)*
- 🇬🇧 "Excuse me? I did not lie!" His voice shakes.  *(linha 116)*
- Respostas:
  - "Pedir desculpa" / "Apologise" → `calm`
  - "Pressionar mais" / "Push harder" → `closed`

### `calm` — confiança 2
- 🇵🇹 "Está bem. Foi uma noite longa. Pergunta com educação."  *(linha 235)*
- 🇬🇧 "Fine. It has been a long night. Ask properly."  *(linha 119)*
- Respostas:
  - "Perguntar com calma o que está ali a fazer" / "Ask kindly what he is doing here" → `kind`
  - "Até já." / "Goodbye." → fim

### `photo` — confiança 2
- 🇵🇹 O Tomás fica a olhar para a fotografia. "Quatro pessoas... nunca tinha reparado." Engole em seco.  *(linha 237)*
- 🇬🇧 Tomás stares at the photo. "Four people... I never noticed." He swallows.  *(linha 121)*
- Respostas:
  - "Pedir-lhe ajuda" / "Ask him to help you" → `help`

### `help` — confiança 3
- 🇵🇹 "Está bem. Vê o chat do grupo. Nem tudo o que lá está é meu."  *(linha 239)*
- 🇬🇧 "All right. Check the group chat. Not everything in there is mine."  *(linha 123)*
- 📓 Diário: O Tomás sugere que algumas mensagens do chat não são de quem diz. / Tomás hints that some chat messages are not from the people they name.
- Respostas:
  - "Até já." / "Goodbye." → fim

### `closed` — confiança 0
- 🇵🇹 O Tomás cruza os braços. "Ficamos por aqui."  *(linha 242)*
- 🇬🇧 Tomás crosses his arms. "We are done here."  *(linha 126)*
- Respostas:
  - "Sair." / "Leave." → fim

## Computador 12
Onde está: **Sala de informática** (`computer_lab`).

### `start`
- 🇵🇹 O computador 12 ainda está ligado, com a sessão do grupo aberta.  *(linha 245)*
- 🇬🇧 Computer 12 is still on, with the group's session open.  *(linha 129)*
- Respostas:
  - "Afastar-me do computador." / "Step away from the computer." → fim

### Ações feitas a falar com Computador 12 (em `story.py`)
- **▶ Consultar os ficheiros antigos do projeto** / Look at the old project files (`view_files`)
  - Se resultar 🇵🇹: Ligas a pen ao computador 12 e comparas. Nas cópias de segurança da pen, todas as versões têm quatro autores. Na pasta partilhada, a versão atual foi alterada ontem às 23h47, a partir deste mesmo computador: alguém acrescentou "Duarte Sequeira" ao relatório e trocou a fotografia. Recuperas a versão original do trabalho.
  - Se resultar 🇬🇧: You plug the USB stick into computer 12 and compare. In the backups on the USB stick, every version has four authors. In the shared folder, the current version was changed yesterday at 11:47 pm, from this same computer: someone added "Duarte Sequeira" to the report and swapped the photo. You recover the original version of the work.
  - Se ainda não puderes 🇵🇹: A pasta partilhada só mostra a versão atual, já com cinco nomes. Precisas da cópia de segurança do grupo.
  - Se ainda não puderes 🇬🇧: The shared folder only shows the current version, already with five names. You need the group's backup copy.
- **▶ Abrir o chat do grupo no computador 12** / Open the group chat on computer 12 (`open_chat`)

## Professor
Onde está: **Auditório** (`auditorium`).

### `start`
- 🇵🇹 O professor levanta os olhos da lista de grupos. "É sobre as apresentações de amanhã?"  *(linha 248)*
- 🇬🇧 The professor looks up from the list of groups. "Is this about tomorrow's presentations?"  *(linha 132)*
- Respostas:
  - "Perguntar quantos elementos tem o teu grupo na lista" / "Ask how many members your group has on the list" → `list`
  - "Dizer que vais trazer provas" / "Say you will bring proof" → `proof`
  - "Até já." / "Goodbye." → fim

### `list`
- 🇵🇹 "Cinco, segundo a capa. Há algum problema?"  *(linha 253)*
- 🇬🇧 "Five, according to the cover. Is something wrong with that?"  *(linha 137)*
- Respostas:
  - "Dizer que vocês são só quatro" / "Say there are only four of you" → `evidence`

### `evidence`
- 🇵🇹 "Então preciso de provas, não de uma sensação. Traga-me o histórico do projeto."  *(linha 255)*
- 🇬🇧 "Then I need evidence, not a feeling. Bring me the history of the project."  *(linha 139)*
- 📓 Diário: O professor quer o histórico do projeto como prova. / The professor wants the project history as evidence.
- Respostas:
  - "Até já." / "Goodbye." → fim

### `proof`
- 🇵🇹 "Provas são bem-vindas. Apresente-as quando estiver pronto."  *(linha 258)*
- 🇬🇧 "Evidence is welcome. Present it when you are ready."  *(linha 142)*
- Respostas:
  - "Até já." / "Goodbye." → fim

### Ações feitas a falar com Professor (em `story.py`)
- **▶ Apresentar as provas ao professor** / Present the evidence to the professor (`present_evidence`)
  - Acaba o jogo: o texto que aparece é o do final (em `story.py`, `endings`).

## Duarte
Onde está: **Auditório** (`auditorium`).

### `start` — confiança 3
- 🇵🇹 O Duarte sorri com calma. "Ah, o quarto elemento. Pronto para amanhã?"  *(linha 262)*
- 🇬🇧 Duarte smiles calmly. "Ah, the fourth wheel. Ready for tomorrow?"  *(linha 146)*
- Respostas:
  - "Perguntar que parte do projeto fez" / "Ask which part of the project he did" → `part`
  - "Dizer-lhe que sabes a verdade" / "Tell him you know the truth" → `know`
  - "Até já." / "Goodbye." → fim

### `part` — confiança 3
- 🇵🇹 "Os slides, claro. Pergunta a qualquer um." Hesita por um segundo.  *(linha 267)*
- 🇬🇧 "The slides, of course. Ask anyone." He hesitates for a second.  *(linha 151)*
- Respostas:
  - "Perguntar que slide" / "Ask which slide" → `slide`

### `slide` — confiança 2
- 🇵🇹 "A... introdução. A bonita." O Duarte olha para a porta. "Porquê tantas perguntas?"  *(linha 269)*
- 🇬🇧 "The... intro. The nice one." Duarte glances at the door. "Why all these questions?"  *(linha 153)*
- 📓 Diário: O Duarte não soube dizer que slide fez. / Duarte could not say which slide he made.
- Respostas:
  - "Até já." / "Goodbye." → fim

### `know` — confiança 1
- 🇵🇹 "Que verdade? Cuidado com as acusações."  *(linha 272)*
- 🇬🇧 "Know what? Careful with accusations."  *(linha 156)*
- Respostas:
  - "Pressioná-lo" / "Press him" → `closed`
  - "Recuar" / "Back off" → `start`

### `closed` — confiança 0
- 🇵🇹 O Duarte ri-se e vira-te as costas. A conversa acabou.  *(linha 275)*
- 🇬🇧 Duarte laughs and turns away. The conversation is over.  *(linha 159)*
- Respostas:
  - "Sair." / "Leave." → fim

