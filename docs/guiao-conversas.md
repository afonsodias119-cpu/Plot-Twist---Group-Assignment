# Guião das conversas — O quinto elemento (jogo 3D)

Tudo o que as pessoas dizem no jogo 3D, em português e em inglês, tal como está no código.

> **Gerado em 21/11/2026 (atualizado à mão a 23/11/2026, com os três casos do dia mais abaixo; depois da junção com o computador 12 resolvido com o grupo, o código e a data da fotografia são os mesmos em todos os casos e os números de linha foram refeitos) a partir de `prototypes/campus-3d/campus_people.py`, `prototypes/campus-3d/campus_case.py` e `story.py`.** O código é que manda: se mudares uma fala no código, este guião fica desatualizado até ser gerado outra vez.

## Como alterar uma fala

1. **Conversas** (o que cada pessoa diz quando falas com ela): `prototypes/campus-3d/campus_people.py`, dentro de `PEOPLE`. Há um bloco `"en"` (inglês) e um bloco `"pt"` (português). Ao lado de cada fala deste guião está o número da linha.
2. **Respostas às ações** (o que acontece quando escolhes ▶ abrir a gaveta, pedir a cópia, etc.): `story.py`, em `result_text` (quando resulta) e `blocked_text` (quando ainda não podes).
3. **Provas, confrontos e audiência** (o que as pessoas respondem quando lhes mostras uma prova, e as quatro afirmações do Duarte): `prototypes/campus-3d/campus_case.py`. Só o servidor lê este ficheiro: nada do que lá está pode ir para `campus_text.py`.
4. **O que vai para o balão:** só o que está **entre aspas** (`\"...\"` no código) aparece no balão e é lido pela voz. O resto aparece como narração, em itálico, fora dos balões. Exemplo: `Rita looks up from her laptop. \"You don't look so good.\"`: "Rita looks up from her laptop." é narração, e "You don't look so good." vai para o balão.
5. **Regras para não estragar nada** (os testes verificam-nas):
   - Muda só o texto entre as aspas de `"text"`, `"label"` e `"note"`. Não mudes os identificadores (`"start"`, `"photo"`, `"next": ...`, `"if": ...`, `"trust"`).
   - Se mudares uma fala em português, muda também a inglesa (e vice-versa). As duas línguas têm de ter as mesmas falas, respostas e condições: só o texto muda.
   - Dentro do texto, as aspas da fala escrevem-se `\"` (barra e aspas).
   - As falas nunca podem dizer quais são as mensagens falsas ("message 2", "mensagem 4"…).
6. Depois de mudar, corre `uv run pytest`. Se ficar verde, recarrega o jogo (no endereço que o Streamlit mostra ao arrancar; por omissão http://localhost:8501).

**Legenda:** ⏳ *custa N minutos* é uma resposta agressiva: tira esses minutos à contagem decrescente (para mudar, altera `"cost": 5` no código) e fica lembrada até ao fim da noite (ver "Quando foste rude", mais abaixo). 📁 *prova* é uma carta que podes mostrar numa conversa ("Mostrar uma prova"), exceto com a funcionária, o Tomás, o computador 12 e a Rita, e com o segurança só depois de ele pedir uma prova ("Explicar a situação") (specs/two-answers.md, specs/evidence-after-monitors.md); qualquer prova errada custa 2 minutos (com o Duarte, 1). 📁 *cede com a resposta certa*: na fala em que a pessoa diz uma coisa falsa, a resposta ✓ lembra-lhe uma prova e fá-la ceder. ✓ é a resposta certa e ✗ a errada (o Tomás e a Rita têm sempre só estas duas). *Confiança* (0 a 3) é o humor da pessoa: não aparece no jogo (não há corações), o jogador percebe-o pelo que ela diz; com 0 a pessoa acaba a conversa. *Diário* é a nota que fica guardada no diário do telemóvel. "→ fim" acaba a conversa: no jogo 3D estas respostas não aparecem (usa-se o botão "Terminar conversa"), mas têm de existir no código, porque cada fala precisa de pelo menos uma resposta. Uma pergunta já feita na mesma conversa não volta a aparecer. 🕙 *até às 22:25* / *até às 22:30* quer dizer que a pessoa se vai embora a essa hora do campus. ↺ *a partir da noite N* é uma resposta que só aparece a quem já acabou N−1 noites com esse nome (chave `"night"` no código). Só é oferecida junto com a primeira fala da conversa.

## Rita
Onde está: **Sala de estudo** (`study_room`).

### `start`
- 🇵🇹 A Rita levanta os olhos do portátil. "Estás com cara de quem não dormiu nada. Conseguiste descansar alguma coisa?"  *(linha 275)*
- 🇬🇧 Rita looks up from her laptop. "You don't look so good. Did you sleep at all?"  *(linha 76)*
- Respostas:
  - ✓ "Perguntar onde está a pen" / "Ask where the USB stick is" → `pen` *(só aparece se não tens `usb_stick`)*
  - ✗ "Dizer-lhe que foi ela que perdeu a pen" / "Tell her she is the one who lost the USB stick" → `upset` *(só aparece se não tens `usb_stick`)*
  - ✓ "Perguntar pela fotografia do grupo" / "Ask about the group photo" → `photo` *(só aparece se tens `usb_stick`)*
  - ✗ "Dizer-lhe que a pen estava debaixo da pizza dela" / "Tell her the USB stick was under her own pizza" → `upset` *(só aparece se tens `usb_stick`)*
  - ✓ ↺ "Dizer-lhe que te lembras de ela contar as cabeças" / "Tell her you remember her counting heads" → `five` *(a partir da noite 3)*
  - "Até já." / "Goodbye." → fim

### `pen`
- 🇵🇹 "A pen? Devia estar aqui, mas não a encontro." Olha para a mesa. "Ontem ficámos aqui até tarde a comer pizza, mas com esta confusão, pode estar em qualquer lado da mesa."  *(linha 285)*
- 🇬🇧 "The USB stick? It should be here somewhere, but I can't find it." She looks at the table. "We stayed here late last night eating pizza, but with this mess, it could be anywhere on the table."  *(linha 86)*
- 📓 Diário: Rita: não encontra a pen. Pode estar em qualquer lado da mesa da sala de estudo. O grupo comeu pizza aqui ontem à noite. / Rita cannot find the USB stick. It could be anywhere on the study room table. The group ate pizza here last night.
- Respostas:
  - "Até já." / "Goodbye." → fim

### `photo`
- 🇵🇹 "A fotografia? Tirámo-la depois da última reunião, nós os quatro."  *(linha 289)*
- 🇬🇧 "The photo? We took it after the last meeting, the four of us."  *(linha 90)*
- 📓 Diário: A Rita lembra-se de quatro pessoas na fotografia do grupo. / Rita remembers four people in the group photo.
- Respostas:
  - ✓ "Perguntar porque é que a fotografia da pasta mostra cinco" / "Ask why the photo in the folder shows five" → `five`
  - ✗ "Dizer-lhe que a memória dela não conta" / "Tell her that her memory does not count" → `upset`

### `five` — 📁 cede com a resposta certa
- 🇵🇹 "Então contei mal." A Rita vira o portátil para ti: cinco pessoas. "Uma fotografia não muda. A minha memória muda. Ele devia estar mesmo ali."  *(linha 296)*
- 🇬🇧 "Then I counted wrong." Rita turns the laptop towards you: five people. "A photo cannot change. My memory can. He must have been standing right there."  *(linha 97)*
- Respostas:
  - ✓ "Lembrar-lhe a fotografia original da reprografia: quatro pessoas" / "Remind her of the print shop's original photo: four people" → cede (mostra `original_photo`) *(só aparece se tens `original_photo`)*
  - ✓ "Lembrar-lhe que o histórico dos ficheiros tem quatro autores em todas as cópias" / "Remind her the file history has four authors in every copy" → cede (mostra `files`) *(só aparece se não tens `original_photo` e `files_viewed` = `True`)*
  - ✓ "Perguntar o que ela se lembra do Duarte" / "Ask what she remembers about Duarte" → `duarte` *(só aparece se não tens `original_photo` e `files_viewed` = `False`)*
  - ✗ "Concordar que ela deve ter contado mal" / "Agree that she must have counted wrong" → `counted`

### `counted`
- 🇵🇹 A Rita acena devagar. "Pois. Uma fotografia não mente." Vira o portátil outra vez.  *(linha 302)*
- 🇬🇧 Rita nods slowly. "Yes. A photo does not lie." She turns the laptop back.  *(linha 103)*
- Respostas:
  - ✓ "Perguntar o que ela se lembra do Duarte" / "Ask what she remembers about Duarte" → `duarte`
  - ✗ "Dizer-lhe que então o Duarte fica no grupo" / "Tell her that then Duarte stays in the group" → `upset`

### `duarte`
- 🇵🇹 "O Duarte... sinceramente, não o consigo imaginar. Sempre que tento, só vejo o nome na capa."  *(linha 306)*
- 🇬🇧 "Duarte... honestly, I cannot picture him. Every time I try, I only see the name on the cover."  *(linha 107)*
- Respostas:
  - ✓ "Dizer que achas que o nome foi acrescentado ontem à noite" / "Say you think the name was added last night" → `warned`
  - ✗ "Dizer que então ele faz mesmo parte do grupo" / "Say that then he must really be part of the group" → `upset`

### `warned`
- 🇵🇹 A Rita fica calada. "Se for verdade, alguém quis que duvidássemos de nós próprios."  *(linha 310)*
- 🇬🇧 Rita goes quiet. "If that is true, somebody wanted us to doubt ourselves."  *(linha 111)*
- 📓 Diário: A Rita também desconfia do quinto nome. / Rita doubts the fifth name too.
- Respostas:
  - ✓ "Perguntar pelas mensagens do chat" / "Ask about the chat messages" → `chat` *(só aparece se `files_viewed` = `True`)*
  - ✓ "Dizer-lhe que vais procurar provas" / "Tell her you will go and find proof" → `promise` *(só aparece se `files_viewed` = `False`)*
  - ✗ "Dizer-lhe que é tudo imaginação dela" / "Tell her it is all in her head" → `upset`

### `promise`
- 🇵🇹 "Vai. Eu fico aqui." A Rita volta a abrir o portátil.  *(linha 315)*
- 🇬🇧 "Go. I will stay here." Rita opens her laptop again.  *(linha 116)*
- Respostas:
  - "Até já." / "Goodbye." → fim

### `chat`
- 🇵🇹 "Repara na hora a que as mensagens chegam. Algumas dizem há três semanas, mas no meu telemóvel aparecem como novas, de ontem à noite. Mensagens antigas não funcionam assim."  *(linha 318)*
- 🇬🇧 "Look at when the messages arrive. Some say three weeks ago, but my phone shows them as new, last night. That is not how old messages work."  *(linha 119)*
- 📓 Diário: Rita: uma mensagem antiga não chega como nova. As mensagens sobre o Duarte chegaram ontem à noite. / Rita: an old message does not arrive as new. The messages about Duarte arrived last night.
- Respostas:
  - "Até já." / "Goodbye." → fim

### `upset`
- 🇵🇹 A Rita fecha o portátil devagar. "Não precisas de falar assim comigo. Estamos todos cansados."  *(linha 321)*
- 🇬🇧 Rita closes her laptop slowly. "You do not have to talk to me like that. We are all tired."  *(linha 122)*
- Respostas:
  - ✓ "Pedir desculpa" / "Apologise" → `sorry`
  - ✗ "Dizer que só estás a ser sincero" / "Say you are only being honest" → `closed`

### `sorry`
- 🇵🇹 "Está bem. Pergunta lá."  *(linha 325)*
- 🇬🇧 "Fine. Go on, ask."  *(linha 126)*
- Respostas:
  - ✓ "Perguntar onde está a pen" / "Ask where the USB stick is" → `pen` *(só aparece se não tens `usb_stick`)*
  - ✗ "Dizer-lhe que foi ela que perdeu a pen" / "Tell her she is the one who lost the USB stick" → `upset` *(só aparece se não tens `usb_stick`)*
  - ✓ "Perguntar pela fotografia do grupo" / "Ask about the group photo" → `photo` *(só aparece se tens `usb_stick`)*
  - ✗ "Dizer-lhe que a pen estava debaixo da pizza dela" / "Tell her the USB stick was under her own pizza" → `upset` *(só aparece se tens `usb_stick`)*

### `closed`
- 🇵🇹 A Rita põe os auscultadores. Já não te está a ouvir.  *(linha 332)*
- 🇬🇧 Rita puts her headphones on. She is not listening any more.  *(linha 133)*
- Respostas:
  - "Sair." / "Leave." → fim
### Ações feitas nesta conversa (em `story.py`)
- **▶ Abrir a gaveta do grupo** / Open the group drawer (`open_drawer`)
  - Se resultar 🇵🇹: Encontras a pen onde o grupo guardava as cópias de segurança do projeto. Guardas a pen.
  - Se resultar 🇬🇧: You find the USB stick where the group kept the project backups. You take the USB stick.

## Funcionária
Onde está: **Reprografia** (`print_shop`).
🕙 Só até às 22:25. Depois, a sala continua aberta mas o balcão está vazio: "A grade está descida e o balcão às escuras. A funcionária foi para casa às 22:25. Há um papel colado na grade: fotografia da capa, pedido de 17 de outubro, levantar amanhã." / "The shutter is down and the counter is dark. The clerk went home at 22:25. A slip is taped to the shutter: cover photo, order of 17 October, collect tomorrow." (a frase está em `campus_clock.py`, não em `campus_text.py`)

### `start`
- 🇵🇹 A funcionária ajeita os óculos. "Fechamos daqui a dez minutos, do que precisas?"  *(linha 337)*
- 🇬🇧 The clerk adjusts her glasses. "Hello! We close in ten minutes. What do you need?"  *(linha 138)*
- Respostas:
  - "Perguntar pelo pedido da fotografia da capa" / "Ask about the cover photo order" → `order`
  - ↺ "Dizer a data antes dela" / "Say the date before she does" → `again` *(a partir da noite 2)*
  - "Até já." / "Goodbye." → fim

### `order`
- 🇵🇹 "A fotografia da capa? Tiraram-na e mandaram-na imprimir aqui no mesmo dia. Eram quatro pessoas, ainda me lembro, e acho que o ficheiro original do pedido ainda está guardado."  *(linha 342)*
- 🇬🇧 "The cover photo? You took it and had it printed here the same day. I remember there were four people in it, and I think the original order file is still saved."  *(linha 143)*
- 📓 Diário: A fotografia da capa foi impressa na reprografia no dia em que foi tirada. A reprografia ainda tem o ficheiro original do pedido. / The cover photo was printed at the print shop the day it was taken. The print shop still has the original order file.
- Respostas:
  - "Até já." / "Goodbye." → fim

### `again` — ↺ a partir da noite 2
- 🇵🇹 A funcionária fica com a mão parada na impressora. "Dezassete de outubro. Sim. Como é que tu...?" Olha para o relógio. "Há muito tempo que estou a fechar daqui a dez minutos." Franze a testa para o balcão. "Estranho. Não me lembro de te ver sair."  *(linha 345)*
- 🇬🇧 The clerk stops with her hand on the printer. "The seventeenth of October. Yes. How do you...?" She looks at the clock. "I have been closing in ten minutes for a very long time." She frowns at the counter. "Odd. I do not remember you leaving."  *(linha 147)*
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
- 🇵🇹 A Leonor fecha o livro devagar. "Vens por causa do Duarte. Eu sei."  *(linha 350)*
- 🇬🇧 Leonor closes her book slowly. "You are here about Duarte. I know."  *(linha 152)*
- Respostas:
  - "Perguntar se tem a certeza de que ele estava no grupo" / "Ask if she is sure he was in the group" → `sure`
  - "Dizer-lhe que tens dúvidas" / "Tell her you have doubts" → `soft`
  - "Perguntar que mensagem do chat é mesmo dela" / "Ask which chat message is really hers" → `mine` *(só aparece se `colleague_choice` = `help`)*
  - "Dizer que ela está a mentir" / "Say she is lying" → `harsh` ⏳ **custa 5 minutos**
  - ↺ "Dizer-lhe que sabias que ela ia dizer exatamente isso" / "Tell her you knew she would say exactly that" → `again` *(a partir da noite 3)*
  - "Até já." / "Goodbye." → fim

### `sure` — confiança 2
- 🇵🇹 "Está em todas as mensagens há semanas. Tenho-as aqui." Toca no telemóvel.  *(linha 358)*
- 🇬🇧 "He has been in every message for weeks. I have them right here." She taps her phone.  *(linha 161)*
- Respostas:
  - "Pedir para ver as mensagens" / "Ask to see the messages" → `messages`

### `messages` — confiança 3
- 🇵🇹 "Olha. Todas de um número que eu não conhecia. Algumas têm data de há semanas, mas chegaram ontem à noite."  *(linha 363)*
- 🇬🇧 "Look. All from a number I did not know. Some are dated weeks ago, but they arrived last night."  *(linha 167)*
- 📓 Diário: A Leonor recebeu as mensagens do Duarte ontem à noite, de um número desconhecido. / Leonor received Duarte's messages last night, from an unknown number.
- Respostas:
  - "Até já." / "Goodbye." → fim

### `mine` — confiança 3
- 🇵🇹 "A que pede para reservar a sala de estudo. Escrevi-a nesta mesa, há três semanas." A Leonor percorre o ecrã com um dedo. "As do número que eu não conhecia chegaram todas com minutos de diferença, ontem à noite."  *(linha 360)*
- 🇬🇧 "The one asking to book the study room. I wrote that at this table, three weeks ago." Leonor scrolls with one finger. "The ones from the number I did not know all arrived within minutes of each other, last night."  *(linha 164)*
- 📓 Diário: A Leonor escreveu ela própria a mensagem do chat sobre reservar a sala de estudo. / Leonor wrote the chat message about booking the study room herself.
- Respostas:
  - "Até já." / "Goodbye." → fim

### `soft` — confiança 3
- 🇵🇹 "Eu queria acreditar em ti." Olha para o telemóvel. "Talvez devesse ver outra vez."  *(linha 366)*
- 🇬🇧 "I wanted to believe you." She looks at her phone. "Maybe I should look again."  *(linha 170)*
- Respostas:
  - "Pedir para ver as mensagens" / "Ask to see the messages" → `messages`

### `harsh` — confiança 1
- 🇵🇹 "Desculpa?" A voz dela endurece.  *(linha 368)*
- 🇬🇧 "Excuse me?" Her voice hardens.  *(linha 172)*
- Respostas:
  - "Pedir desculpa" / "Apologise" → `soft`
  - "Insistir" / "Insist" → `closed` ⏳ **custa 5 minutos**

### `closed` — confiança 0
- 🇵🇹 A Leonor levanta-se. "Volta com provas, não com acusações."  *(linha 371)*
- 🇬🇧 Leonor stands up. "Come back with proof, not accusations."  *(linha 175)*
- Respostas:
  - "Sair." / "Leave." → fim

### `again` — confiança 3 — ↺ a partir da noite 3
- 🇵🇹 A mão da Leonor fica em cima do livro. "Palavra por palavra? Ninguém sabe o que eu vou dizer." Fica a olhar para o teu cachecol. "Já fizemos isto antes?"  *(linha 372)*
- 🇬🇧 Leonor's hand stays on the book. "Word for word? Nobody knows what I am going to say." She studies your scarf. "Have we done this before?"  *(linha 177)*
- Respostas:
  - "Até já." / "Goodbye." → fim

### Ações feitas nesta conversa (em `story.py`)
- **▶ Mostrar a fotografia e pedir ajuda discretamente** / Show the photo and quietly ask for help (`ask_for_help`)
  - Se resultar 🇵🇹: A Leonor compara a fotografia com a do relatório e fica pálida. "Recebi estas mensagens todas ontem à noite, de um número que não conhecia. E algumas têm datas de há três semanas." Promete guardar as mensagens originais e ir ter contigo ao auditório.
  - Se resultar 🇬🇧: Leonor compares the photo with the one in the report and turns pale. "I got all these messages last night, from a number I did not know. And some of them are dated three weeks ago." She promises to keep the original messages and to meet you in the auditorium.
  - Se ainda não puderes 🇵🇹: A Leonor encolhe os ombros. "O Duarte esteve sempre no grupo, tenho aqui as mensagens. Tens alguma prova do contrário?"
  - Se ainda não puderes 🇬🇧: Leonor shrugs. "Duarte has always been in the group, I have the messages right here. Do you have any proof otherwise?"
A Leonor já não pode ser acusada (specs/three-proofs.md): a única decisão é pedir-lhe ajuda.

## Tomás
Onde está: **Sala de informática** (`computer_lab`).

### `start` — confiança 2
- 🇵🇹 O Tomás está curvado sobre o computador 11, a evitar o teu olhar. "Ah. Olá. Já é tarde."  *(linha 376)*
- 🇬🇧 Tomás is hunched over computer 11, avoiding your eyes. "Oh. Hi. It is late."  *(linha 181)*
- Respostas:
  - ✓ "Perguntar com calma o que está ali a fazer" / "Ask kindly what he is doing here" → `kind`
  - ✗ "Exigir saber porque mentiu sobre o Duarte" / "Demand to know why he lied about Duarte" → `hard` ⏳ **custa 5 minutos**
  - ✓ ↺ "Dizer-lhe que já sabes o que o chat diz sobre os slides" / "Tell him you know what the chat says about the slides" → `slides` *(a partir da noite 2)*
  - "Até já." / "Goodbye." → fim

### `kind` — confiança 3
- 🇵🇹 "Não conseguia dormir e vim acabar os slides. Ontem à noite, perto da meia-noite, vi alguém no computador 12."  *(linha 382)*
- 🇬🇧 "I could not sleep, I just came here to finish the slides. And... I saw someone at computer 12 last night, near midnight."  *(linha 189)*
- Respostas:
  - ✓ "Perguntar quem era" / "Ask who it was" → `who`
  - ✗ "Dizer-lhe que isso parece uma desculpa" / "Tell him that sounds like an excuse" → `hard`

### `password` — confiança 3
- 🇵🇹 "A password do computador? É o dia e o mês em que tirámos a fotografia da capa. São só 4 números, mas nunca me lembro da data. Entre todos havemos de lá chegar."  *(linha 385)*
- 🇬🇧 "The password of computer 12? It is the group's: the day and the month we took the cover photo. Four digits. I can never remember the date, but between all of us we can work it out."  *(linha 192)*
- 📓 Diário: Tomás: a password do computador 12 é o dia e o mês em que foi tirada a fotografia da capa (4 algarismos). / Tomás: the password of computer 12 is the day and month the cover photo was taken (4 digits).
- Respostas:
  - ✓ "Perguntar quem fez os slides" / "Ask who made the slides" → `slides` *(só aparece se `files_viewed` = `True`)*
  - ✓ "Mostrar-lhe a fotografia original" / "Show him the original photo" → `photo` *(só aparece se tens `original_photo` e `files_viewed` = `False`)*
  - ✗ "Dizer-lhe que devia saber a data de cor" / "Tell him he should know the date by heart" → `hard`

### `who` — confiança 3
- 🇵🇹 "Só vi um capuz. Como o que o Duarte usa. Mas ninguém o viu chegar."  *(linha 391)*
- 🇬🇧 "Only a hood. Like the one Duarte wears. But nobody ever saw him arrive."  *(linha 200)*
- 📓 Diário: O Tomás viu alguém de capuz no computador 12 perto da meia-noite. / Tomás saw someone in a hood at computer 12 near midnight.
- Respostas:
  - ✓ "Perguntar a password do computador 12" / "Ask for the password of computer 12" → `password`
  - ✗ "Perguntar se o do capuz era ele" / "Ask if the one in the hood was him" → `hard`

### `slides` — confiança 2 — 📁 cede com a resposta certa
- 🇵🇹 O Tomás não tira os olhos do ecrã. "Os slides? Estou a acabá-los. Mas o chat diz que foram do Duarte, com o meu nome. Se calhar foram mesmo, e eu só arrumei."  *(linha 395)*
- 🇬🇧 Tomás keeps his eyes on the screen. "The slides? I am finishing them. But the chat says Duarte did them, under my name. So maybe he did, and I only tidied up."  *(linha 207)*
- 📓 Diário: O Tomás acha que os slides podem ter sido do Duarte, só porque uma mensagem do chat com o nome dele o diz. / Tomás thinks Duarte may have made the slides, only because a chat message under his own name says so.
- Respostas:
  - ✓ "Lembrar-lhe que o histórico dos ficheiros tem o nome dele em todas as versões dos slides" / "Remind him the file history has his name on every version of the slides" → cede (mostra `files`) *(só aparece se `files_viewed` = `True`)*
  - ✗ "Dizer-lhe que então o crédito é do Duarte" / "Tell him that then the credit is Duarte's" → `convinced`

### `convinced` — confiança 2
- 🇵🇹 O Tomás acena sem levantar os olhos. "Pois. Se calhar é mais justo. Ele fez mais do que eu penso."  *(linha 400)*
- 🇬🇧 Tomás nods without looking up. "Yeah. Maybe that is fairer. He did more than I think."  *(linha 212)*
- Respostas:
  - "Até já." / "Goodbye." → fim

### `hard` — confiança 1
- 🇵🇹 "Como? Eu não menti!" A voz dele treme.  *(linha 402)*
- 🇬🇧 "Excuse me? I did not lie!" His voice shakes.  *(linha 214)*
- Respostas:
  - ✓ "Pedir desculpa" / "Apologise" → `calm`
  - ✗ "Pressionar mais" / "Push harder" → `closed` ⏳ **custa 5 minutos**

### `calm` — confiança 2
- 🇵🇹 "Está bem. Foi uma noite longa. Pergunta com educação."  *(linha 405)*
- 🇬🇧 "Fine. It has been a long night. Ask properly."  *(linha 217)*
- Respostas:
  - ✓ "Perguntar com calma o que está ali a fazer" / "Ask kindly what he is doing here" → `kind`
  - ✗ "Insistir que ele mentiu" / "Insist that he lied" → `closed`

### `photo` — confiança 2
- 🇵🇹 O Tomás fica a olhar para a fotografia. "Quatro pessoas... nunca tinha reparado." Engole em seco.  *(linha 408)*
- 🇬🇧 Tomás stares at the photo. "Four people... I never noticed." He swallows.  *(linha 220)*
- Respostas:
  - ✓ "Pedir-lhe ajuda" / "Ask him to help you" → `help`
  - ✗ "Dizer-lhe que a culpa é dele" / "Tell him it is his fault" → `hard`

### `help` — confiança 3
- 🇵🇹 "Está bem. Guarda as conversas do grupo antes que alguém as apague. Nem tudo o que está no meu telemóvel é meu."  *(linha 411)*
- 🇬🇧 "All right. Save the group's conversations before someone deletes them. Not everything on my phone is mine."  *(linha 223)*
- 📓 Diário: O Tomás sugere que algumas mensagens do chat não são de quem diz. / Tomás hints that some chat messages are not from the people they name.
- Respostas:
  - "Até já." / "Goodbye." → fim

### `closed` — confiança 0
- 🇵🇹 O Tomás cruza os braços. "Ficamos por aqui."  *(linha 414)*
- 🇬🇧 Tomás crosses his arms. "We are done here."  *(linha 226)*
- Respostas:
  - "Sair." / "Leave." → fim
## Computador 12
Onde está: **Sala de informática** (`computer_lab`).

### `start`
- 🇵🇹 O computador 12 ainda está ligado, com a sessão do grupo aberta. Pede uma password de 4 algarismos.  *(linha 417)*
- 🇬🇧 Computer 12 is still on, with the group's session open. It asks for a 4-digit password.  *(linha 229)*
- Respostas:
  - "Afastar-me do computador." / "Step away from the computer." → fim

### Ações feitas nesta conversa (em `story.py`)
- **▶ Consultar os ficheiros antigos do projeto** / Look at the old project files (`view_files`)
  - Se resultar 🇵🇹: Ligas a pen ao computador 12 e comparas. Nas cópias de segurança da pen, todas as versões têm quatro autores. Na pasta partilhada, a versão atual foi alterada ontem às 23h47, a partir deste mesmo computador: alguém acrescentou "Duarte" ao relatório e trocou a fotografia. Recuperas a versão original do trabalho.
  - Se resultar 🇬🇧: You plug the USB stick into computer 12 and compare. In the backups on the USB stick, every version has four authors. In the shared folder, the current version was changed yesterday at 11:47 pm, from this same computer: someone added "Duarte" to the report and swapped the photo. You recover the original version of the work.
  - Se ainda não puderes 🇵🇹: A pasta partilhada só mostra a versão atual, já com cinco nomes. Precisas da cópia de segurança do grupo.
  - Se ainda não puderes 🇬🇧: The shared folder only shows the current version, already with five names. You need the group's backup copy.
- **▶ Guardar o backup das conversas originais** / Save a backup of the original conversations (`save_backup`, specs/computer-lab-backup.md: substitui o chat do grupo)
  - Se resultar 🇵🇹: O computador 12 ainda tem a conta do grupo aberta. Copias todo o histórico das conversas do grupo para a pen, tal como estava antes de ontem à noite: quatro pessoas, e nem uma mensagem do Duarte. Agora o professor pode ver as conversas originais.
  - Se resultar 🇬🇧: Computer 12 still has the group's account open. You copy the whole history of the group's conversations onto the USB stick, as it was before last night: four people, and not one message from Duarte. Now the professor can see the original conversations.

## Professor
Onde está: **Auditório** (`auditorium`). Uma só linha de raciocínio (specs/professor-line-of-thought.md): quantos elementos → cinco → só quatro → trazer provas → apresentar as provas.

### `start`
- 🇵🇹 O professor levanta os olhos da lista de grupos. "É sobre as apresentações de amanhã?"
- 🇬🇧 The professor looks up from the list of groups. "Is this about tomorrow's presentations?"
- Respostas:
  - "Perguntar quantos elementos tem o teu grupo na lista" / "Ask how many members your group has on the list" → `list`
  - ↺ "Perguntar se já ouviu este caso" / "Ask if he has heard this case before" → `again` *(a partir da noite 4)*
  - "Até já." / "Goodbye." → fim

### `list`
- 🇵🇹 "Cinco, segundo a capa. Há algum problema?"
- 🇬🇧 "Five, according to the cover. Is something wrong with that?"
- Respostas:
  - "Dizer que vocês são só quatro" / "Say there are only four of you" → `evidence`

### `evidence`
- 🇵🇹 "Então preciso de provas, não de uma sensação: quem fez o trabalho, quem está na fotografia, quem escreveu no grupo, e quem esteve no edifício ontem à noite."
- 🇬🇧 "Then I need evidence, not a feeling: who did the work, who is in the photo, who wrote in the group, and who was in the building last night."
- 📓 Diário: O professor quer provas de quem fez o trabalho, de quem está na fotografia, de quem escreveu no grupo e de quem esteve no edifício ontem à noite. / The professor wants proof of who did the work, who is in the photo, who wrote in the group and who was in the building last night.
- Respostas:
  - "Dizer que vais trazer provas" / "Say you will bring proof" → `proof`

### `proof`
- 🇵🇹 "Provas são bem-vindas. Apresente-as quando estiver pronto."
- 🇬🇧 "Evidence is welcome. Present it when you are ready."
- Só nesta fala aparece "▶ Apresentar as provas ao professor" (a audiência).
- Respostas:
  - "Até já." / "Goodbye." → fim

### `again` — ↺ a partir da noite 4
- 🇵🇹 O professor vira uma página da lista e volta a virá-la. "Todos os anos me aparece um grupo com um nome a mais. Nunca é o mesmo grupo. É sempre o mesmo nome."  *(linha 433)*
- 🇬🇧 The professor turns a page of the list, then turns it back. "Every year a group comes to me with one name too many. Never the same group. Always the same name."  *(linha 246)*
- Respostas:
  - "Até já." / "Goodbye." → fim

### Ações feitas nesta conversa (em `story.py`)
- **▶ Apresentar as provas ao professor** / Present the evidence to the professor (`present_evidence`)
  - No jogo 3D este botão abre a audiência (as quatro afirmações do Duarte, em `campus_case.py`); só depois da quarta resposta o jogo acaba. O servidor continua a aceitar a ação direta.

## Duarte
> **O jogador já não fala com o Duarte** (specs/duarte-only-in-the-hearing.md): ele só fala na audiência, com as afirmações ao professor. As falas abaixo continuam no servidor, mas a página nunca as mostra.
Onde está: **Auditório** (`auditorium`).

### `start` — confiança 3
- 🇵🇹 O Duarte sorri com calma. "Ah, o quarto elemento. Pronto para amanhã?"  *(linha 437)*
- 🇬🇧 Duarte smiles calmly. "Ah, the fourth wheel. Ready for tomorrow?"  *(linha 250)*
- Respostas:
  - "Perguntar que parte do projeto fez" / "Ask which part of the project he did" → `part`
  - "Dizer-lhe que sabes a verdade" / "Tell him you know the truth" → `know` ⏳ **custa 5 minutos**
  - ↺ "Perguntar-lhe quantas noites já foram" / "Ask him how many nights this has been" → `again` *(a partir da noite 2)*
  - "Até já." / "Goodbye." → fim

### `part` — confiança 3
- 🇵🇹 "Os slides, claro. Pergunta a qualquer um." Hesita por um segundo.  *(linha 443)*
- 🇬🇧 "The slides, of course. Ask anyone." He hesitates for a second.  *(linha 256)*
- Respostas:
  - "Perguntar que slide" / "Ask which slide" → `slide`

### `slide` — confiança 2
- 🇵🇹 "A... introdução. A bonita." O Duarte olha para a porta. "Porquê tantas perguntas?"  *(linha 445)*
- 🇬🇧 "The... intro. The nice one." Duarte glances at the door. "Why all these questions?"  *(linha 258)*
- 📓 Diário: O Duarte não soube dizer que slide fez. / Duarte could not say which slide he made.
- Respostas:
  - "Até já." / "Goodbye." → fim

### `know` — confiança 1
- 🇵🇹 "Que verdade? Cuidado com as acusações."  *(linha 448)*
- 🇬🇧 "Know what? Careful with accusations."  *(linha 261)*
- Respostas:
  - "Pressioná-lo" / "Press him" → `closed` ⏳ **custa 5 minutos**
  - "Recuar" / "Back off" → `start`

### `closed` — confiança 0
- 🇵🇹 O Duarte ri-se e vira-te as costas. A conversa acabou.  *(linha 451)*
- 🇬🇧 Duarte laughs and turns away. The conversation is over.  *(linha 264)*
- Respostas:
  - "Sair." / "Leave." → fim

### `again` — confiança 2 — ↺ a partir da noite 2
- 🇵🇹 O sorriso do Duarte não se mexe. "Para ti? Já perdi a conta. Para mim só existe esta noite." Olha para o teu casaco como se fosse dele. "Outra vez tu. Já estava a gostar da companhia."  *(linha 452)*
- 🇬🇧 Duarte's smile does not move. "For you? I have lost count. For me there is only ever tonight." He looks at your coat as if it were his. "You again. I was starting to enjoy the company."  *(linha 266)*
- Respostas:
  - "Até já." / "Goodbye." → fim

## Quando foste rude (em `prototypes/campus-3d/campus_people.py`, fora de `PEOPLE`)

(specs/trust-has-consequences.md) Uma resposta ⏳ fica lembrada até ao fim da noite, nas notas da noite (nota `rude`); um "Novo jogo" esquece-a. A Leonor, o Tomás e o Duarte ficam com um feitio que nunca aparece no ecrã (nem número, nem corações): **calmo** (nenhuma resposta rude), **desconfiado** (uma), **hostil** (duas, por exemplo "Dizer que ela está a mentir" e depois "Insistir"). Pedir desculpa não desfaz. Quem cedeu com a prova certa fica calmo o resto da noite, diga-se o que se disser. A Rita, a funcionária e o professor estão sempre calmos.

Só muda o texto (e às vezes a nota) de uma fala: as respostas, as ações (a cópia, as decisões da Leonor, o computador 12, a audiência), as afirmações (`slides`, `five`, `sure`), os custos e o horário ficam iguais. Estes textos estão em tabelas próprias (`COLD`, `WITHHELD`, `LIES`, `WARNED`, `WARNS`), por isso `PEOPLE` não muda. Nenhum diz o culpado, uma data ou um código.

**Que texto ganha:** na fala `start`, o aviso (se quem avisa estiver hostil), senão a fala seca, senão a da história. Na fala `messages` da Leonor, a mentira se estiver hostil, senão a fala seca.

### Falas secas (`COLD`): desconfiado ou hostil; o diário guarda a nota de sempre
- **Tomás, `start`**
  - 🇵🇹 O Tomás nem levanta os olhos do computador 11. "O que foi agora?"  *(linha 480)*
  - 🇬🇧 Tomás does not look up from computer 11. "What now?"  *(linha 381)*
- **Tomás, `kind`**
  - 🇵🇹 "A acabar os slides." Continua a escrever. "Esteve alguém no computador 12 ontem à noite. É tudo o que sei."  *(linha 481)*
  - 🇬🇧 "Finishing the slides." He keeps typing. "Someone was at computer 12 last night. That is all I know."  *(linha 382)*
- **Tomás, `password`** (a regra do código não muda: só fica mais seca)
  - 🇵🇹 "O dia e o mês da fotografia da capa. Quatro algarismos." Nem levanta os olhos.  *(linha 482)*
  - 🇬🇧 "The day and month of the cover photo. Four digits." He does not look up.  *(linha 383)*
- **Tomás, `who`** (a nota de sempre fica, por isso o diário guarda o que o caso diz)
  - 🇵🇹 "Alguém de capuz, no computador 12." Continua a escrever.  *(linha 483)*
  - 🇬🇧 "Someone in a hood, at computer 12." He keeps typing.  *(linha 384)*
- **Leonor, `start`**
  - 🇵🇹 Desta vez a Leonor não fecha o livro. "Sim?"  *(linha 484)*
  - 🇬🇧 Leonor does not close her book this time. "Yes?"  *(linha 385)*
- **Leonor, `messages`** (só desconfiada; hostil, mente: ver abaixo)
  - 🇵🇹 "De um número que eu não conhecia. Ontem à noite."  *(linha 485)*
  - 🇬🇧 "From a number I did not know. Last night."  *(linha 386)*
- **Duarte, `start`**
  - 🇵🇹 O Duarte nem se dá ao trabalho de sorrir. "Ainda por aqui?"  *(linha 486)*
  - 🇬🇧 Duarte does not bother to smile. "Still here?"  *(linha 387)*
- **Duarte, `part`**
  - 🇵🇹 "Os slides. Pergunta a qualquer um." Olha para além de ti.  *(linha 487)*
  - 🇬🇧 "The slides. Ask anyone." He looks past you.  *(linha 388)*

### Pistas que ficam por dar (`WITHHELD`): desconfiado ou hostil; sem nota no diário
São só pistas: tudo o que é preciso para um final tem outra fonte.
- **Tomás, `help`**
  - 🇵🇹 O Tomás fica a olhar para a fotografia um segundo a mais. "Vê o que quiseres. Estou ocupado."  *(linha 500)*
  - 🇬🇧 Tomás looks at the photo a second too long. "Check what you like. I am busy."  *(linha 406)*
- **Leonor, `mine`**
  - 🇵🇹 "Descobre tu."  *(linha 501)*
  - 🇬🇧 "Work it out yourself."  *(linha 407)*
- **Duarte, `slide`**
  - 🇵🇹 "Porque é que te havia de dizer?" O Duarte olha para a porta.  *(linha 502)*
  - 🇬🇧 "Why would I tell you?" Duarte glances at the door.  *(linha 408)*

### Mentiras (`LIES`): só hostil; o diário guarda o que te disseram
Uma mentira não é uma afirmação: mostrar-lhe uma prova dá a resposta habitual da pessoa e custa os minutos de sempre. Vence-se não acreditando nela. O Duarte mente de qualquer maneira: hostil, não ganha uma mentira nova.
- **Tomás**: já não mente (a fala da mensagem 5 saiu com o chat, specs/two-answers.md).
- **Leonor, `messages`** (desmentem-na o mesmo backup e a fala `chat` da Rita)
  - 🇵🇹 "Não têm nada de estranho. Chegaram nas datas que lá dizem, há semanas." Vira o telemóvel ao contrário.  *(linha 516)*
  - 🇬🇧 "Nothing strange about them. They came on the dates they say, weeks ago." She turns the phone face down.  *(linha 424)*
  - 📓 Diário: A Leonor diz que as mensagens chegaram nas datas delas, há semanas. / Leonor says the messages arrived on their dates, weeks ago.

### O aviso que passa (`WARNS` e `WARNED`): enquanto quem avisa estiver hostil e não tiver cedido
A cadeia é fixa: o Tomás avisa a Leonor, a Leonor avisa a Rita, o Duarte avisa o professor. Só muda a primeira fala (`start`) de quem foi avisado; as respostas, as ações e as decisões dessa pessoa ficam iguais.
- **Leonor** (avisada pelo Tomás)
  - 🇵🇹 A Leonor fecha o livro antes de chegares à mesa. "O Tomás mandou-me mensagem. Diz que andas por aí a chamar mentirosos às pessoas."  *(linha 529)*
  - 🇬🇧 Leonor closes her book before you reach the table. "Tomás texted me. He says you are going round calling people liars."  *(linha 440)*
- **Rita** (avisada pela Leonor)
  - 🇵🇹 A Rita levanta os olhos e não sorri. "A Leonor diz que lhe gritaste na biblioteca. É verdade?"  *(linha 530)*
  - 🇬🇧 Rita looks up and does not smile. "Leonor says you shouted at her in the library. Is that true?"  *(linha 441)*
- **Professor** (avisado pelo Duarte)
  - 🇵🇹 O professor levanta os olhos da lista e não sorri. "O Duarte diz-me que o ameaçou. Espero que amanhã me traga provas, e não isso."  *(linha 531)*
  - 🇬🇧 The professor looks up from the list and does not smile. "Duarte tells me you threatened him. I hope you bring evidence tomorrow, not that."  *(linha 442)*

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

Só o servidor lê este ficheiro. A página recebe uma carta quando a tens, e uma fala quando a mereceste. As provas para o professor são a pen (o histórico), a fotografia e o backup das conversas (specs/computer-lab-backup.md); a câmara de segurança será a quarta (specs/security-desk.md, fase 2).

### As provas (cartas)
| id | quando a tens | 🇵🇹 | 🇬🇧 |
|---|---|---|---|
| `original_photo` | tens o objeto `original_photo` (a fotografia triturada, reconstruída na reprografia) | A fotografia original, colada com fita-cola: quatro pessoas | The original photo, taped back together: four people |
| `files` | `files_viewed` = `True` | O histórico dos ficheiros: quatro autores em todas as cópias | The file history: four authors in every backup |
| `backup` | `backup_saved` = `True` (guardado no computador 12) | O backup das conversas originais: quatro pessoas, nem uma mensagem do Duarte | The backup of the original conversations: four people, not one message from Duarte |
| `footage` | a imagem das 23:47 da câmara da sala de informática guardada na secretária do segurança (nota `footage` da noite, specs/camera-proof.md) | A gravação da câmara: uma figura de capuz no computador 12 às 23h47 | The security recording: a hooded figure at computer 12 at 23:47 |

Ceder a Rita ou o Tomás já não dá uma carta: fica nas notas da noite (o Tomás fica a vigiar a porta). A Leonor já não cede com uma prova.

### Quem cede, e com que prova (pela resposta certa da fala, specs/two-answers.md)
| pessoa | fala | provas que a fazem ceder |
|---|---|---|
| Tomás | `slides` | `files` |
| Rita | `five` | `files`, `original_photo` |

### Quando cedem (a prova certa na fala certa)
**Tomás** — confiança 3
- 🇵🇹 O Tomás lê o histórico dos slides: todas as versões guardadas com o nome dele, a última na terça-feira às duas da manhã. "Então a mensagem diz que foi o Duarte. Os ficheiros dizem que fui eu." Baixa a voz. "Eu nunca enviei aquela mensagem. E os slides... fui eu que fiz os slides. Os onze. Fiquei aqui até às duas na terça-feira." Roda a cadeira para a parede de vidro. "Ele anda pelo corredor, sabes. Volta para o computador. Se ele vier, eu fico à porta."
- 🇬🇧 Tomás reads the history of the slides: every version saved under his name, the last one on Tuesday at two in the morning. "So the message says Duarte did them. The files say I did." His voice drops. "I never sent that message. And the slides... I made the slides. All eleven. I was here until two on Tuesday." He turns his chair to face the glass wall. "He walks the corridor, you know. Go back to the computer. If he comes, I will be standing in the door."
- 📓 Diário: O Tomás nunca escreveu a mensagem sobre os slides: foi ele que os fez e vai dizê-lo. Fica a vigiar o corredor por ti. / Tomás never wrote the message about the slides: he made them himself and will say so. He is watching the corridor for you.

**Rita** — sem confiança (a Rita não tem nível de confiança)
- 🇵🇹 A Rita olha da tua prova para o ecrã e outra vez para a prova. "Então a fotografia mudou mesmo." Ri-se uma vez, sem alegria nenhuma. "Eu contei quatro. Disse-o em voz alta. Até o escrevi no chat: os quatro, finalmente. Essa é minha, lembro-me de a escrever." Fecha o portátil. "Diz ao professor que eu contei. Eu digo-lho na cara."
- 🇬🇧 Rita looks from your proof to her screen and back. "So the photo did change." She laughs once, without any joy. "I counted four. I said it out loud. I even wrote it in the chat: four of us, finally. That one is mine, I remember typing it." She closes the laptop. "Tell the professor I counted. I will say it to his face."
- 📓 Diário: A Rita contou quatro pessoas no dia da fotografia. A mensagem do chat que fala nos quatro é dela. Vai dizê-lo ao professor. / Rita counted four people on the day of the photo. The chat message that says four of them is hers. She will tell the professor.

### Qualquer outra prova, ou outra fala (custa 2 minutos; com o Duarte, 1)
- **Tomás** 🇵🇹 O Tomás olha de relance e volta ao ecrã. "E o que é que isso tem a ver com o que eu acabei de dizer?" / 🇬🇧 Tomás glances at it and back at his screen. "And what does that have to do with what I just said?"
- **Rita** 🇵🇹 A Rita olha para aquilo e volta ao portátil. "E então? Não vejo o que é que isso muda." / 🇬🇧 Rita looks at it, then back at her laptop. "And? I do not see what that changes."
- **Leonor** 🇵🇹 A Leonor olha para o que tens na mão e depois para ti. "Se me queres mostrar alguma coisa, diz o que queres de mim." / 🇬🇧 Leonor looks at what you are holding, then at you. "If you want to show me something, say what you want from me."
- **Funcionária** 🇵🇹 A funcionária olha por cima dos óculos. "Eu imprimo coisas. Não as julgo. Precisas de alguma coisa impressa?" / 🇬🇧 The clerk looks over her glasses. "I print things. I do not judge them. Is there anything you need printed?"
- **Professor** 🇵🇹 O professor não lhe pega. "Assim não. Apresente as provas como deve ser, quando estiver pronto." / 🇬🇧 The professor does not take it. "Not like this. Present your evidence properly, when you are ready."
- **Duarte (qualquer prova, em qualquer fala; 1 minuto)** 🇵🇹 O Duarte nem olha. "Guarda isso para o professor. Eu vou estar na primeira fila." / 🇬🇧 Duarte does not look at it. "Keep it for the professor. I will be sitting in the front row."

### A audiência: as quatro afirmações do Duarte
No cartão aparece a linha 🇵🇹 "O Duarte faz uma afirmação. Responde com a prova que mostra que é falsa, ou não digas nada." / 🇬🇧 "Duarte makes a claim. Answer with the proof that shows it is false, or say nothing." Uma resposta por afirmação, sem segunda tentativa. Uma prova que não a desfaz, ou "Não dizer nada", é uma dúvida. A quarta afirmação desfaz-se com a gravação da câmara (specs/camera-proof.md).

**1. `name`** (fala o Duarte) — desfaz-se com `files`
- 🇵🇹 O Duarte levanta-se sem pressa. "Professor, abra o relatório. O meu nome está na capa. Está lá desde o primeiro rascunho."
- 🇬🇧 Duarte stands up without hurry. "Professor, open the report. My name is on the cover. It has been there since the first draft."
- Certa, `files` (professor): 🇵🇹 "Quatro autores em todas as cópias, e um quinto nome acrescentado ontem às 23h47. Continue." / 🇬🇧 "Four authors in every backup, and a fifth name added last night at 11:47 pm. Go on."
- Errada, qualquer outra (professor): 🇵🇹 "Isso não me diz quem escreveu um relatório." Faz um pequeno sinal na lista. / 🇬🇧 "That does not tell me who wrote a report." He makes a small mark on the list.

**2. `photo`** (fala o Duarte) — desfaz-se com `original_photo`
- 🇵🇹 "Então olhe para a fotografia. Cinco pessoas, e eu sou o da direita, de casaco comprido. Uma máquina fotográfica não acrescenta ninguém."
- 🇬🇧 "Then look at the photograph. Five people, and I am the one on the right, in the long coat. A camera does not add anyone."
- Certa, `original_photo` (professor): 🇵🇹 O professor põe a fotografia colada ao lado da capa. "A impressão da própria reprografia, com o carimbo da data. Quatro pessoas, antes de alguém acrescentar um quinto." / 🇬🇧 The professor holds the taped photo next to the cover. "The print shop's own print, with its date stamp. Four people, before anyone added a fifth."
- Errada, `files` (professor): 🇵🇹 "O histórico diz que uma fotografia foi trocada. Não me mostra a que lá estava antes." / 🇬🇧 "The history says a photo was swapped. It does not show me the one that was there before."
- Errada, qualquer outra (professor): 🇵🇹 "Isso não me diz nada sobre quem está numa fotografia." Faz um sinal na lista. / 🇬🇧 "That tells me nothing about who is in a photograph." He makes a mark on the list.

**3. `messages`** (fala o Duarte) — desfaz-se com `backup`
- 🇵🇹 O Duarte levanta o telemóvel. "E as mensagens? Semanas delas. O próprio Tomás escreveu: 'Os slides foram do Duarte, claro.' O Tomás também é mentiroso?"
- 🇬🇧 Duarte raises his phone. "And the messages? Weeks of them. Tomás wrote it himself: 'Duarte did the slides, obviously.' Is Tomás a liar too?"
- Certa, `backup` (professor): 🇵🇹 O professor percorre o backup. "As conversas do próprio grupo, tal como estavam antes de ontem à noite: quatro pessoas, e nem uma mensagem dele. Uma data escreve-se. Um backup de semanas, não." / 🇬🇧 The professor scrolls through the backup. "The group's own conversations, as they were before last night: four people, and not one message from him. A date can be typed. A backup of weeks cannot."
- Errada, qualquer outra (professor): 🇵🇹 "Isso não me diz quem enviou uma mensagem." Faz um sinal na lista. / 🇬🇧 "That does not tell me who sent a message." He makes a mark on the list.

**4. `here`** (fala o Duarte) — desfaz-se com `footage`
- 🇵🇹 O Duarte encosta-se e cruza os braços. "E quem mudou a pasta às 23h47? Eu não. Nem cá estive ontem à noite."
- 🇬🇧 Duarte leans back and folds his arms. "And who changed the folder at 23:47? Not me. I was not even here last night."
- Certa, `footage` (professor): 🇵🇹 O professor fica muito tempo a olhar para a imagem. "Computador 12, ontem às 23h47, o minuto em que o quinto nome foi acrescentado. Um capuz, um casaco comprido. E a câmara da entrada viu o mesmo casaco entrar às 23h38." Levanta os olhos. "Esteve cá, Duarte." / 🇬🇧 The professor looks at the picture for a long time. "Computer 12, last night at 23:47, the minute the fifth name was added. A hood, a long coat. And the entrance camera saw the same coat come in at 23:38." He looks up. "You were here, Duarte."
- Errada, qualquer outra (professor): 🇵🇹 "Isso não me diz quem estava no edifício ontem à noite." Faz um sinal na lista. / 🇬🇧 "That does not tell me who was in the building last night." He makes a mark on the list.

**"Não dizer nada"** / "Say nothing" (`concede`, em qualquer afirmação; fala o Duarte; é sempre uma dúvida)
- 🇵🇹 O professor espera. O Duarte sorri. "Nada?"
- 🇬🇧 The professor waits. Duarte smiles. "Nothing?"

A resposta à quarta afirmação aparece no cartão do final, por cima do veredicto.

### O veredicto do professor (por cima do texto do final)
Basta uma afirmação sem prova certa (uma prova errada ou "Não dizer nada") para o final ser "Crédito roubado", com esta fala (specs/three-proofs.md). Com as três respostas certas não há veredicto.

| chave | quando | 🇵🇹 | 🇬🇧 |
|---|---|---|---|
| `missing` | pelo menos uma afirmação sem a prova certa (mostra `stolen_credits`) | O professor olha para os sinais na lista. "Acho que tem razão sobre ele. Mas uma das afirmações dele ficou sem prova, e eu só escrevo aquilo de que tenho a certeza." | The professor looks at the marks on his list. "You are right about him, I think. But one of his claims has no proof against it, and I write down only what I am sure of." |

### Os finais (em `story.py`, nos dois jogos)
Só há três maneiras de a noite acabar (specs/three-proofs.md): chegas ao professor com as provas e respondes certo às afirmações do Duarte (três provas no jogo simples; quatro no 3D, com a gravação da câmara), ou falta-te alguma coisa, ou o tempo acaba às 22:45. O auditório está sempre aberto.

| id | quando | 🇵🇹 | 🇬🇧 |
|---|---|---|---|
| `full_case` — Caso encerrado | tens a fotografia original, viste os ficheiros e guardaste o backup (e, em 3D, a gravação da câmara e as quatro respostas certas) | Pões as tuas provas na mesa do professor… O professor risca o quinto nome da lista. Amanhã apresentam os quatro, com o caso encerrado. | You put your proofs on the professor's desk… The professor crosses the fifth name off the list. Tomorrow, the four of you present, with the case closed. |
| `stolen_credits` — Crédito roubado | falta uma prova (ou, em 3D, uma resposta errada) | Não tens todas as provas de que o professor precisa… "Não risco um nome por um palpite." Amanhã apresentam os cinco. | You do not have every proof the professor needs… "I cannot cross out a name on a hunch." Tomorrow, the five of you present. |

O texto completo de cada final está em `story.py`. O final "O impostor" (acusar a Leonor) e o final verdadeiro ("22:46") já não existem.

### O número desconhecido nas noites seguintes
Uma mensagem quando a noite começa (id `night-<n>`), em `NIGHT_TEXT` de `campus_case.py`. Uma noite conta quando acaba (um final, ou as 22:45 sem final), nunca com um "Novo jogo" simples.

| quando | 🇵🇹 | 🇬🇧 |
|---|---|---|
| noite 1 | (nenhuma) | (none) |
| noite 2 | Outra vez tu? | You again? |
| noite 3 | Outra vez tu. O mesmo casaco, o mesmo cachecol. | You again. Same coat, same scarf. |
| noite 4 | Eu já deixei de contar as noites. Tu não. | I have stopped counting the nights. You have not. |
| noite 5 e seguintes | Olha para a fotografia do teu caso. Depois diz-me qual de nós é o quinto. | Look at the photo on your case file. Then tell me which of us is the fifth. |

A partir da noite 3, os três avisos das rondas (`round-12`, `round-19`, `round-26`) passam a ser do número desconhecido: 🇵🇹 Fecha o computador. Ele vem aí. / 🇬🇧 Close the computer. He is walking. Nas noites 1 e 2 ficam com o texto de sempre.

## O caso do dia (em `prototypes/campus-3d/campus_case.py`, `CASES`)

(specs/case-of-the-day.md) O jogo começa com a operação `begin` e o ecrã inicial mostra a data do caso. Só existe o caso clássico (`outsider`): o culpado é sempre o Duarte. Os casos `tomas` e `rita` (specs/culprit-of-the-night.md) mudavam as mensagens falsas do chat e saíram com ele (specs/computer-lab-backup.md).

O dia aparece no ecrã inicial, na barra de cima e no cartão de partilha (`📅 Caso de 22 de novembro`), com os textos de `campus_text.py`: `case_of_day` 🇵🇹 Caso de {d} de {month} / 🇬🇧 Case of {d} {month}, e `months` (janeiro … dezembro / January … December). Nunca diz o caso, o culpado nem o código.

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
| Andar, falar, o sítio certo, guardar o backup, responder a uma afirmação | 0 | nada |

### As duas saídas
- **Funcionária:** sai às 22:25 (minuto 10). A frase da grade está acima, na secção da Funcionária.
- **Leonor:** sai às 22:30 (minuto 15), só se ainda não tiver aceitado ajudar. A ajudar, fica. Não é uma pista do telemóvel: quando sai, nenhuma pista se perde, mas deixa de estar no computador 12 para lembrar o dia do teste de Finanças.
- Depois de a pessoa sair, a sala continua aberta, mas a pessoa já não aparece, não se pode falar com ela nem mostrar-lhe provas, e a ação dela (a cópia; o pedido de ajuda à Leonor) é recusada com a frase do horário. Uma conversa aberta quando a pessoa sai acaba com essa frase.

Depois das 22:25 a data do código lê-se no papel colado na grade da reprografia: no modo de texto é o primeiro parágrafo da sala; em 3D aparece como nota ao entrar e fica no diário.

Uma pista que já não se pode obter (só a fotografia, depois das 22:25) fica "perdida" no telemóvel. O auditório está sempre aberto: sem essa prova, o final é "Crédito roubado".

### As rondas do Duarte: 22:27, 22:34 e 22:41
Se nesse minuto estiveres no computador 12 com os ficheiros abertos e o backup ainda por guardar, e o Tomás ainda não tiver cedido, és apanhado: custa 3 minutos e começas a audiência com uma dúvida (specs/computer-lab-backup.md).
- `caught` 🇵🇹 A porta da sala abre-se atrás de ti. "A trabalhar até tarde?" O Duarte estica o braço por cima do teu ombro e fecha a janela. "Essas conversas não são para ti." / 🇬🇧 The lab door opens behind you. "Working late?" Duarte reaches past your shoulder and closes the window. "Those conversations are not for you."
- `door` (o Tomás já cedeu e vigia a porta: a ronda passa e não custa nada) 🇵🇹 O Tomás põe-se à porta. O Duarte segue caminho. / 🇬🇧 Tomás stands in the doorway. Duarte walks on.

### As mensagens do número desconhecido
| id | quando chega | 🇵🇹 | 🇬🇧 |
|---|---|---|---|
| `shop` | do minuto 5 ao 9, sem a fotografia original | A reprografia fecha às 22:25. E tu ainda na conversa. | The print shop closes at 22:25. You are still talking. |
| `leonor` | do minuto 10 ao 14, a Leonor indecisa e a fotografia não perdida | A Leonor arruma a mochila às dez e meia. Faz sempre isso. | Leonor packs her bag at half past ten. She always does. |
| `lost` | quando a fotografia se perde | Para isso, hoje já é tarde. Amanhã deixo-te a luz acesa. | Too late for that tonight. I will keep the light on for you tomorrow. |
| `round-12`, `round-19`, `round-26` | no minuto antes de cada ronda (11, 18, 25), se o Tomás ainda não cedeu | Anda alguém no corredor. Não estejas no computador 12 quando ele passar. | Someone is walking the corridor. Do not be at computer 12 when he passes. |
