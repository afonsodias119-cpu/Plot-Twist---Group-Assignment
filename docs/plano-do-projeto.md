# Plano do projeto — Plot Twist (trabalho de grupo)

Documento de referência da equipa. Resume o que foi decidido até agora e o que falta fazer.
Última atualização: 23/11/2026 (correções para a grelha de avaliação no branch `grading-fixes`: o nome pertence ao browser, dependências sem vulnerabilidades, o nome verificado no primeiro passo e o README).

## 1. O que o curso pede

Fonte: [site do curso](https://nova-sbe-introduction-to-programming.github.io/intro-to-programming-2026/) e [página de avaliação](https://nova-sbe-introduction-to-programming.github.io/intro-to-programming-2026/evaluation.html).
A página da semana 8 (regras detalhadas do trabalho de grupo) ainda não estava publicada a 10/11 — confirmar quando sair.

- **Calendário:** trabalho de grupo nas semanas 8–10; apresentações nas semanas 11–12 (metade dos grupos em cada semana).
- **Nota:** a apresentação vale **40%** da nota final. Todos os membros recebem a mesma nota (nota de grupo).
- **Formato da apresentação:**
  - **Demo ao vivo num link público** (app publicada). Não são slides nem vídeo.
  - **Explicação do código:** os professores abrem o repositório e fazem perguntas.
- **Critérios:** funciona · design · âmbito e ambição · verificação (testes) · explicação do código.
- ⚠️ **Cada membro é questionado sobre código que NÃO escreveu.** Todos têm de perceber o projeto inteiro.
- **Entrega:** um membro submete o link do repositório no Moodle até **23/11/2026, 23:59**. O repositório é público, o `main` tem a app publicada e o README tem o URL, os nomes e os números de aluno de todos.
- **Tecnologia:** Python, Streamlit, SQLite e pytest, tudo corrido com `uv`.

## 2. Decisões da equipa

- **Jogo escolhido:** Plot Twist (mistério / escape room).
- **História escolhida:** "O quinto elemento", passada na Nova SBE. Mapa completo em [historia.md](historia.md).
- **Começamos do zero**, sem partir de um projeto a solo.
- **Repositório:** https://github.com/afonsodias119-cpu/Plot-Twist---Group-Assignment
- **Regra de ouro:** o `main` só muda através de Pull Requests revistos por outro membro.

## 3. O que o jogo tem de cumprir (versão base)

Detalhes completos em [plot-twist-brd.md](plot-twist-brd.md). Em resumo:

- Pelo menos **5 cenas**, **2 objetos** e **2 finais** (um deles depende de uma escolha ou objeto anterior).
- Ações bloqueadas sem os requisitos (ex.: porta trancada sem chave). Uma ação bloqueada não muda nada.
- Os objetos apanham-se uma só vez, não se duplicam e não se gastam.
- Novo jogo e continuar jogo. Recomeçar pede confirmação.
- O progresso fica gravado em SQLite e sobrevive a fechar e abrir a app.
- **Fora do âmbito (não fazer):** diálogo com IA em direto, multijogador, combate, serviços pagos ou externos.

## 4. Plano por fases

| Fase | O quê | Quem | Estado |
|---|---|---|---|
| **A. Preparar** | Clonar o repositório, criar a estrutura e proteger o `main` | Afonso | 🔄 quase pronta (falta o passo 5: os colegas clonarem) |
| **B. Inventar a história** | Mistério, 5+ cenas, objetos, finais e personagens, tudo no papel | Grupo todo | ✅ história revista e integrada na main (#3, #4 e #6) |
| **C. Versão base** | Jogo mínimo que cumpre o brief, com testes | Afonso + revisão | ✅ implementada e no `main` (107 testes a passar) |
| **D. Extras criativos** | Uma funcionalidade por pessoa | Os 4 | ✅ 3D jogável no `main` (Maria + Afonso) e puzzle do chat de grupo (Guilherme). ✅ Provas e audiência (`specs/evidence-and-hearing.md`), integrada na main (#45): mostrar provas nas conversas, três pessoas que cedem e a audiência com as três afirmações do Duarte. ✅ Horário da noite (`specs/night-schedule.md`), integrado na main (#46): o servidor passa a saber o minuto do campus (operação `time`, tabela de custos em `campus_clock.py`), a funcionária sai às 22:25 e a Leonor às 22:30 (se estiver indecisa), uma pista perdida não fecha o auditório, o número desconhecido avisa das horas e das rondas, e o Duarte apanha quem estiver no chat às 22:27, 22:34 e 22:41. Na página: a hora do campus antes da contagem, a nota da grade (e no diário), "Tarde demais" nas pistas, a conversa que acaba quando a pessoa sai, o Duarte à porta da sala de informática no 3D. ✅ Noites anteriores (`specs/earlier-nights.md`), integradas na main (#49): o jogo lembra-se de cada noite acabada de um nome (tabela `runs` em `db.py`, regras em `campus_memory.py`). Na noite 2 o número desconhecido diz "Outra vez tu?" (e continua no telemóvel depois do "Novo jogo"); a partir da noite 3 os avisos das rondas são dele. Seis respostas ↺ só aparecem a partir de uma certa noite e só junto com a primeira fala da conversa (duas são atalhos para as afirmações do Tomás e da Rita). No ecrã inicial, a quinta figura da fotografia do caso muda de noite para noite (mais escura, o casaco, o cachecol e o chapéu do detetive, depois a tua inicial) e uma linha por baixo do nome diz que noite é. Com os quatro finais vistos em noites anteriores, uma audiência perfeita com a palavra do Tomás e a da Rita dá um final verdadeiro, que só o servidor conhece; depois dele a fotografia mostra quatro pessoas. ✅ Sete ideias novas (branch `more-ideas`), todas feitas: **sons que dizem coisas** (`specs/sounds-that-tell.md`): passos do Duarte que se aproximam e se afastam na sala de informática antes e depois de cada ronda, a grade da reprografia a descer às 22:25 (mais baixo nas outras salas), a cadeira e os passos da Leonor quando sai, e uma vibração por cada mensagem nova (no máximo três); tudo feito com Web Audio em `play.js`, nada toca com o Som desligado nem ao recarregar a página. **Mais para encontrar** (`specs/more-to-find.md`): três objetos novos na mesa da sala de estudo (cartão de estudante, calendário de exames, talão da pizza) e sete coisas para ver nas outras salas, com a operação nova `examine` (secção "Ver" no painel, tecla K no 3D); duas são pistas falsas: o livro de pedidos custa 2 minutos até teres a fotografia original, e o post-it do computador 7 (2311) nunca é o código. **Comandos no telemóvel**: a ideia já estava na main (`specs/touch-card-qr.md`, do Afonso: joystick escolhido no primeiro ecrã, cartão de detetive e código QR), por isso o nosso joystick, os seus textos e `specs/phone-joystick.md` saíram na junção e fica o dele. Das nossas coisas só fica que a nota "Clica na tecla K para ver…" das coisas para ver também se toca com o dedo, como a das pessoas. **Confiança com consequências** (`specs/trust-has-consequences.md`): uma resposta agressiva continua a custar 5 minutos (na página) e agora fica lembrada até ao fim da noite (operação nova `rude`, nota `rude` nas notas da noite; `talk` continua a não gravar nada). A Leonor, o Tomás e o Duarte ficam desconfiados (uma resposta rude: falas mais secas, e quatro pistas que ficam por dar) ou hostis (duas: o Tomás mente sobre a mensagem 5 e a Leonor sobre as mensagens, mentiras que o chat e a Rita desmentem; e a pessoa seguinte é avisada: o Tomás avisa a Leonor, a Leonor a Rita, o Duarte o professor). Quem cede com a prova certa fica calmo. O feitio nunca vai para a página (nem número, nem corações); as respostas, as ações, as afirmações, o código e o horário não mudam. Textos em `campus_people.py` (`COLD`, `WITHHELD`, `LIES`, `WARNED`, `WARNS`) e no guião das conversas. Código e testes feitos (428 testes a passar, mais `tests/continuous-conversations.cjs`); verificado no browser em inglês com uma base de dados de rascunho. **Caso do dia** (`specs/case-of-the-day.md`): a data (hora de Lisboa) escolhe o caso, o mesmo para toda a gente nesse dia; a barra de cima da ficha do caso mostra "Caso de 22 de novembro" ao lado do nome do jogo (no telemóvel o "Confidencial" e a hora dão-lhe lugar), a barra de cima do jogo também, e o cartão de partilha ganha a linha `📅 Caso de 22 de novembro` (sem nomes, sem código). A página começa com a operação nova `begin`; um jogo continuado fica com o seu caso, "Jogar outra vez" joga o caso de hoje, e `open` (todos os testes revistos) continua a jogar o caso clássico. **Culpado variável** (`specs/culprit-of-the-night.md`): três casos em `campus_case.py` (`CASES`): `outsider` (o clássico: o Duarte sozinho), `tomas` (o Tomás meteu o Duarte no grupo, por causa dos slides) e `rita` (a Rita disse que sim ao Duarte sem perguntar a ninguém). Cada caso tem a sua ordem do chat, as suas mensagens falsas como se veem, a conta no histórico dos ficheiros, quem mente e o que o desmente, uma confissão que também desfaz a afirmação "o meu nome está lá desde o primeiro rascunho", e os seus finais (o final verdadeiro também). Depois da junção com a main o computador 12 é igual em todos os casos: fotografia de sábado, 17 de outubro, código 1710, e nenhuma fala de um caso toca no que o grupo se lembra desse dia. A história joga-se sempre com as suas mensagens 1 a 5: o servidor só muda a ordem do chat e troca os textos à saída (`campus_evidence.retell`); a página só vê os números do chat como se veem. Os segredos (culpado, código, mensagens falsas, textos dos casos) nunca vão para a página. Código e testes feitos (452 testes a passar, mais `tests/continuous-conversations.cjs`); os três casos jogados até ao fim com uma base de dados de rascunho (pistas, quatro finais, audiência sem dúvidas e final verdadeiro), e verificados no browser em inglês e em português. **O teu grupo** (`specs/your-own-group.md`): no passo "O teu detetive" do ecrã inicial, debaixo do criador de personagem, uma secção fechada "O teu grupo (opcional)" com três campos: o amigo 1 fica no lugar da Leonor, o 2 no da Rita e o 3 no do Tomás (cada campo diz de quem é o lugar e se é "ela" ou "ele"; vazio fica o nome da história). As fichas de nomes do grupo (no aviso "A faculdade fecha às 22:45") mostram os nomes escritos. Os nomes vão com `begin` e o servidor limpa-os (`campus_people.clean_group`): só letras, espaços, apóstrofos e hífenes, até 14 caracteres, primeira letra maiúscula; um nome mau volta ao da história, e dois nomes iguais, "Duarte" ou o nome de outro lugar (a "Rita" no lugar da Leonor) devolvem o grupo todo da história. Ficam nas notas da noite (`names`), nunca na tabela `games`; um jogo continuado fica com o seu grupo e o "Novo jogo" mantém-no. No fim de cada resposta, `campus_evidence.retell` troca as palavras Leonor, Rita e Tomás de uma só vez (uma expressão regular), por isso um nome nunca é trocado duas vezes; chega às conversas, ao chat, às provas, às pistas, à audiência, aos finais (o verdadeiro também) e aos textos dos três casos, nas duas línguas. Os ids e as vozes não mudam; as placas com os nomes no 3D mostram o grupo (também quando a Rita e a Leonor te seguem), e no computador 12 as lembranças do grupo e os nomes de quem fala também usam os nomes dos amigos. Código e testes feitos (462 testes a passar, mais `tests/continuous-conversations.cjs`); verificado no browser em inglês e em português, com nomes com acento e apóstrofo, nomes vazios, um nome com HTML (recusado e mostrado como texto) e no telemóvel (375 × 812). **Junção com a main** (#50, #51 e #52) feita no branch: 486 testes a passar (os da Maria e do Afonso incluídos), mais `tests/continuous-conversations.cjs`; verificado no browser no computador e no telemóvel (375 × 812, tátil), em inglês e em português, com o caso do Tomás e o da Rita. Falta: o Pull Request e a revisão |
| **E. Publicar e ensaiar** | Link público (semana 9, não no último dia) e ensaio de perguntas | Os 4 | 🔄 publicado em https://plot-twist.streamlit.app/ (`app_3d.py`); falta ensaio e dados da equipa no README |

### Tomás termina depois da pista do computador — Maria (23/11/2026)

Alteração em `maria/tomas-password-end`: depois de explicar a palavra-passe, o Tomás deixa de oferecer respostas; a explicação fica visível até terminar a conversa. Ao voltar com o histórico dos ficheiros, fala dos slides. Ver `specs/tomas-password-end.md`.

### Conversas corridas — Maria (22/11/2026)

✅ Integrada na main (#37): depois de cada resposta, as outras perguntas disponíveis continuam no mesmo diálogo, sem terminar e voltar a falar. Mantém as pistas, as condições e as consequências. Ver `specs/continuous-conversations.md`.

### Ações da conversa só quando fazem sentido — Maria (22/11/2026)

✅ Integrada na main (#41): no jogo 3D, os dois botões amarelos da Leonor (pedir ajuda ou acusá-la) só aparecem quando já tens a fotografia original. Antes disso, a conversa mostra só as respostas normais; com a fotografia, mostra só as duas decisões. Na reprografia, "Pedir uma cópia do pedido original" só aparece depois de a funcionária falar do pedido. Nas conversas, as ações deixam de ser botões amarelos: parecem respostas normais e vêm depois das perguntas. O servidor e as regras não mudam. Ver `specs/actions-when-they-make-sense.md`.

### Interface mais limpa e intuitiva — Maria (22/11/2026)

✅ Integrada na main (#40), só no jogo 3D: a ficha do caso diz só "O teu grupo" e o Backspace mostra o texto todo de uma vez; a barra de cima deixa de ter emojis (fica "Telemóvel" e "Menu", com Como foi feito, vozes, lanterna e som por extenso); a lista de pistas do telemóvel já não diz onde está cada pista; e as conversas deixam de mostrar os corações de confiança. O servidor e as regras não mudam. Ver `specs/cleaner-interface.md`.

### Sem contagem de finais no ecrã inicial — Maria (22/11/2026)

Alteração preparada em `no-endings-on-start`: o ecrã inicial do jogo 3D deixa de mostrar "Finais descobertos: 0/4", para o jogador não saber quantos finais há antes de jogar. O ecrã do fim continua a mostrar os finais descobertos. Ver `specs/no-endings-on-start.md`.

### A pen escondida na mesa — Maria (22/11/2026)

Alteração preparada em `hidden-object-table`: na sala de estudo só a mesa, cheia de tralha, se pode revistar. Clicar nela (ou em "Ver a mesa") abre um grande plano visto de cima, com dezenas de objetos; cada objeto errado custa 1 minuto; os objetos podem ser arrastados (sem custo) e há uma lupa desenhada no canto que se arrasta pela mesa. Nenhum texto diz onde está a pen, e o chão da sala ficou livre. O servidor mantém a operação `search`; só mudou a lista de objetos em `campus_search.py`. Ver `specs/hidden-object-table.md`. No mesmo ramo: as placas das portas deixam de aparecer por cima da mesa, e entrar no auditório sem provas vindo de outra sala já não leva a personagem para a sala de estudo (`specs/auditorium-door-keeps-room.md`).

### A fotografia triturada — Maria (22/11/2026)

Alteração preparada em `torn-photo` (depende de `hidden-object-table`): na reprografia, ao pedir a cópia, a funcionária descobre que alguém triturou a fotografia original. O jogador junta 9 pedaços rasgados numa moldura (arrastar para encaixar, tocar para rodar). Só o servidor sabe a solução (operação `assemble`); com a fotografia certa vê-se o grupo de quatro e o carimbo da data (agora 17.10). Ver `specs/torn-photo.md`.

### Ecrã inicial em passos e painel que diz onde estás — Maria (22/11/2026)

Alteração preparada em `start-screen-steps`, só no jogo 3D: a ficha do caso perde a legenda "PROVA 01" e o "Caso #005" (fica o nome do jogo) e pede só o nome; "Seguinte" abre um passo novo, "O teu detetive", com o personalizador; no primeiro jogo de cada nome aparece ainda um aviso ("A faculdade fecha às 22:45", 30 minutos) com a missão e o grupo. Fora da sala guardada, o painel lateral diz onde a personagem está (Corredor, Exterior ou a porta de outra sala). Ver `specs/creator-after-name.md`.

### O código do computador 12 com a ajuda do grupo — Maria (22/11/2026)

Alteração preparada em `computer-12-with-the-group` (depende de `start-screen-steps`): a funcionária já não diz a data da fotografia. A Rita (depois da pen) e a Leonor (depois de aceitar ajudar) seguem o jogador e esperam junto do computador 12. Aí o jogador pergunta ao grupo o que se lembram do dia da fotografia e cada um responde à vez (Tomás: estava sol; Rita: foi num sábado; Leonor: depois do teste de Finanças, a 15 de outubro). O telemóvel ganha as apps Meteorologia e Calendário de outubro, que transformam essas lembranças num só dia. A fotografia passa a ser de sábado, 17 de outubro (código `1710`). O código escreve-se no campo de 4 algarismos; cada código errado custa 2 minutos e, ao fim de 3, aparece a dica do carimbo da fotografia. O servidor só ganha o campo `followers` no estado. Mudam testes revistos, com aprovação da equipa: a fala da funcionária e, só na data, o código, o carimbo da fotografia, o papel da grade e a fala de memória da funcionária (lista na spec). Ver `specs/calendar-code.md`.

### Junção das sete ideias com a main — 23/11/2026

O branch `more-ideas` recebeu as três alterações novas da main (comandos no telemóvel, ecrã inicial em passos e computador 12 com o grupo). Decisões: fica o joystick do Afonso (o nosso saiu, com `specs/phone-joystick.md` e o seu teste); o enigma do computador 12 da Maria é igual em todos os casos do dia (17 de outubro, código `1710`), e cada caso só muda as mensagens falsas, a conta no histórico, quem mente, as confissões, a audiência e os finais; o "Caso de …" fica na barra de cima da ficha do caso e "O teu grupo (opcional)" no passo "O teu detetive"; as lembranças do grupo no computador 12 usam os nomes dos amigos. O post-it 2311 do computador 7 continua a ser um código errado (custa 2 minutos, como qualquer código errado). Mudaram só os nossos testes novos (`tests/test_culprit_of_the_night.py`, `tests/test_case_of_the_day.py`, `tests/test_more_to_find.py`, `tests/test_your_own_group.py`); nenhum teste revisto mudou.

### Correções para a grelha de avaliação — 23/11/2026

Branch `grading-fixes`, feito depois de comparar o projeto com a grelha da página do trabalho de grupo (funciona 20, interface 20, âmbito 20, verificação 10, segurança 10, explicação do repositório 20):

- **Segurança — o nome pertence ao browser** (`specs/name-belongs-to-browser.md`): antes, quem escrevesse o nome de outra pessoa continuava, mudava ou recomeçava o jogo dela. Agora o browser cria uma chave secreta para cada nome antes do primeiro pedido; o servidor guarda só o hash dessa chave (tabela nova `keys` em `db.py`, regra em `game.claim_name`) e recusa o nome a quem não tiver a chave, com a mensagem por baixo do campo do nome. `campus_game.command` e os testes revistos não mudam (`keyed_command` tira a chave antes). Limite: o nome só continua no mesmo browser.
- **Segurança — dependências** (`specs/safe-dependencies.md`): o `uv audit` encontrava 62 vulnerabilidades conhecidas no Pillow 12.3.0 (vem com o Streamlit). Passámos para Streamlit 1.67.0 e Pillow 13; o `uv audit` já não encontra nenhuma. O `pytest` passou para o grupo `dev`. O Three.js e a biblioteca do código QR têm agora hashes de integridade (o browser recusa um ficheiro alterado).
- **Interface — o nome é verificado onde se escreve** (`specs/name-check-first-step.md`): um nome inválido já não passa dois passos à frente; o erro aparece logo por baixo do campo. E o fim do texto da ficha já não tira o foco do campo a meio de escrever o nome.
- **Explicação do repositório:** o README explica como o projeto está construído, onde ficam os dados, a segurança, o que os testes cobrem e não cobrem, os limites e como podia mudar. O AGENTS.md ganhou as regras dos segredos e das dependências.

Verificado: todos os testes a passar com o Streamlit 1.67, mais `tests/continuous-conversations.cjs`; o jogo jogado no browser (inglês e português, computador e telemóvel): nome inválido, nome de outro browser recusado, o dono continua, 3D e código QR carregados com os hashes. Nota: o primeiro pedido depois de o servidor arrancar demora 8 a 15 segundos (já acontecia na main) — abrir o jogo e começar uma vez antes da apresentação.

### Pronto para a demo — 23/11/2026

Branch `demo-ready`:

- **O primeiro clique já não falha** (`specs/warm-start.md`): o Python responde em menos de 0,1 s, mas a primeira ida e volta pelo Streamlit depois de o servidor arrancar demorava cerca de 2 s, e enquanto o 3D carrega a página responde tarde (medido: 8,5 a 14,7 s no primeiro "Começar"; a ponte desistia aos 20 s). Agora a ponte acorda o servidor logo que a página abre (`{"warmup": true}`, respondido por `campus_game.keyed_command` sem nome, sem chave e sem gravar nada) e espera até 60 s. Medido depois: com o servidor acabado de arrancar, "Começar" respondeu em 0,4 s.
- **Testes no GitHub** (`specs/tests-on-github.md`): `.github/workflows/tests.yml` corre o pytest e as verificações do JavaScript em cada push e pull request; o README mostra o selo "Tests" da `main`.
- **README:** um diagrama de um clique, da página à base de dados e de volta.

### O backup das conversas, sem chat nem quinto elemento — Maria (23/11/2026)

Alteração preparada em `computer-lab-backup` (nos dois jogos: mexe no `story.py`): depois de abrir os ficheiros, o computador 12 oferece "Guardar o backup das conversas originais", e o auditório passa a pedir os ficheiros e o backup. O chat do grupo e as mensagens para marcar deixam de existir, e o final secreto "O quinto elemento" também. Os três finais passam a depender da escolha da Leonor: ajuda → Caso encerrado; acusada → O impostor (texto novo); sem escolha → Créditos roubados. No 3D, o Tomás cede com o histórico dos ficheiros, o Duarte apanha quem está no computador 12 antes de guardar o backup, e o final verdadeiro abre depois dos três finais. Depois de juntar a main (#53 a #56), combinado com o Afonso: as provas para o professor passam a ser a pen, a fotografia e o backup (a câmara de segurança entra como quarta prova, feita pelo Afonso); os casos do culpado saem e o culpado é sempre o Duarte; os nomes dos amigos continuam. Mudam testes revistos de toda a equipa, com aprovação (lista na spec). Ver `specs/computer-lab-backup.md`.

### Duas respostas nas conversas do Tomás e da Rita — Maria (23/11/2026)

Alteração preparada em `two-answers`: o botão "Mostrar prova" sai das conversas da reprografia e da sala de informática (fica nas outras, incluindo o segurança). Cada fala do Tomás tem só duas respostas, uma certa e uma errada, pela ordem perguntar com calma → quem era → a password → (depois dos ficheiros) quem fez os slides; a resposta certa nos slides fá-lo ceder, como a prova fazia. A Rita passa a ter também só duas respostas em cada fala (a pen → a fotografia → "porque mostra cinco" → o Duarte → o nome acrescentado → as mensagens), e cede na fala "Então contei mal"; uma resposta errada deixa-a chateada e "Pedir desculpa" volta ao início. A pergunta sobre a mensagem 5 saiu, e com ela a mentira do Tomás hostil. Ver `specs/two-answers.md`.

### "Mostrar prova" quando o segurança a pede, e a fotografia da Rita depois da pen — Maria (23/11/2026)

Alteração preparada em `evidence-after-monitors`: com o segurança, "Mostrar uma prova" só aparece depois de "Explicar a situação", quando ele pede uma prova; com a Rita deixa de aparecer. Depois de a Rita dizer que a pen pode estar em qualquer lado da mesa, já não aparece a pergunta da fotografia: vais procurar a pen, e quando a tens a primeira pergunta à Rita passa a ser a fotografia do grupo. Ver `specs/evidence-after-monitors.md`.

### Três provas decidem o final; sem acusar a Leonor e sem final secreto — Maria (23/11/2026)

Alteração preparada no mesmo branch, `evidence-after-monitors` (nos dois jogos: mexe no `story.py`). Só há três maneiras de a noite acabar: chegas ao professor com as três provas (a pen, a fotografia original e o backup) e respondes certo às três afirmações do Duarte → Caso encerrado; falta-te uma prova ou erras uma resposta → Crédito roubado (fala nova do professor, `missing`); ou o tempo acaba às 22:45. A ação "acusar a Leonor" e o final "O impostor" saem. A Leonor fica, porque ajuda no computador 12, mas deixa de ser uma pista do telemóvel. O auditório está sempre aberto (o mapa já não tem cadeado). O final verdadeiro ("22:46") e o desafio do número desconhecido também saem. Mudam testes revistos de toda a equipa; precisam de aprovação na revisão do PR (lista na spec). Ver `specs/three-proofs.md`.

### O professor numa só linha de raciocínio — Maria (23/11/2026)

Alteração preparada no mesmo branch: a conversa com o professor segue uma ordem só (quantos elementos tem o grupo → "cinco" → "só somos quatro" → ele pede provas → "vou trazer provas" → "apresente-as quando estiver pronto"), e só no fim aparece o botão para apresentar as provas. Na audiência, uma linha explica o que fazer quando o Duarte fala: responder com a prova que mostra que a afirmação é falsa. Ver `specs/professor-line-of-thought.md`.

### A câmara de segurança é a quarta prova — Maria (23/11/2026)

Alteração preparada no mesmo branch: a fase 2 da secretária do segurança (o José, os cabos e as gravações, feitos pelo Afonso). Ao guardar a imagem das 23:47 da sala de informática, o servidor regista-a (pedido `footage`) e ela passa a ser uma prova na mão. O Duarte ganha uma quarta afirmação ("Nem cá estive ontem à noite"), que só a gravação desfaz: sem ela não há "Caso encerrado". A noite continua com 30 minutos; os limites dos testes de equilíbrio foram medidos de novo (uma noite cuidadosa cabe até ~37 s por clique). Muda um teste revisto do Afonso (`test_security_desk.py`) e outros da audiência e do horário; precisam de aprovação (lista na spec). Ver `specs/camera-proof.md`.

### Na audiência, "Mostrar uma prova"; o Duarte só fala na audiência — Maria (23/11/2026)

Na audiência, cada afirmação do Duarte responde-se com "📁 Mostrar uma prova" (abre as provas que tens, ou diz que ainda não tens nenhuma) ou "Não dizer nada" (`specs/hearing-show-evidence.md`). O jogador já não fala com o Duarte: ele só aparece a fazer as afirmações ao professor. O K deixa de o escolher, e o corredor entre as cadeiras do auditório ficou mais largo para chegares ao professor (`specs/duarte-only-in-the-hearing.md`).

### As pistas dizem o que encontrar, não onde — Maria (23/11/2026)

O cartão do início e o telemóvel mostram só quatro pistas, sem a sala e sem dicas de onde ou com quem: a pen do grupo, a fotografia original, as imagens da câmara da sala de informática e o histórico dos ficheiros. Ver `specs/clues-without-answers.md`.

### O professor: apresentar as provas ou perguntar — Maria (23/11/2026)

Na primeira fala, o professor oferece duas coisas: apresentar as provas ou perguntar quantos elementos tem o grupo (essa conversa acaba em "vou trazer provas"). Apresentar entrega de uma vez todas as provas que tens; se faltar alguma, o final diz quais. Ver `specs/hand-over-the-proofs.md`.

### Sem contagem de finais — Maria (23/11/2026)

O ecrã do final, o texto de partilha e o cartão deixam de mostrar "Finais descobertos: 1/2". Ver `specs/no-endings-count.md`.

### Fase A — passos

1. ✅ Clonar o repositório com o GitHub Desktop.
2. ✅ Criar a estrutura do projeto no branch `project-setup`: `pyproject.toml`, `uv.lock`, `.gitignore`, `.python-version`, `app.py` provisório, `tests/conftest.py`, `AGENTS.md`, `README.md` e `docs/`.
3. ✅ Confirmar que corre (`uv run streamlit run app.py`). Commit, branch publicado e Pull Request #1 revisto pelo grupo e com merge feito (10/11/2026).
4. ✅ Proteger o `main` no GitHub: ruleset "Main Protection" ativo (exige PR; as aprovações estão a 0 por decisão da equipa).
5. ⏳ Cada colega: clonar no GitHub Desktop, correr `uv sync`, depois `uv run pytest` e por fim `uv run streamlit run app.py`.

### Como trabalhamos (todas as funcionalidades)

1. Criar uma **Issue** no GitHub com a funcionalidade.
2. Escrever a **spec** em `specs/` (planeamento, regras, "Done when").
3. Criar um **branch** com o nome da tarefa.
4. Escrever o código e os **testes**.
5. Abrir um **Pull Request**.
6. **Outro membro revê e aprova.**
7. Fazer **merge**.

A revisão serve de preparação para a pergunta "explica código que não escreveste".

## 5. Ideias criativas (fase D)

| Ideia | Como funciona |
|---|---|
| 📚 **Vários mistérios** | O jogador escolhe entre 2 ou 3 histórias (ex.: "Assalto à Nova SBE", "O professor desaparecido", "Noite na biblioteca"). Sugerido no brief. |
| ✏️ **Editor de histórias** | Ecrã para criar cenas, escolhas e objetos sem mexer no código. É o mais ambicioso e também vem sugerido no brief. |
| 🗺️ **Mapa do campus** | Mostra as salas visitadas e onde o jogador está. |
| 🔐 **Puzzles com código** | O cacifo só abre com um código de 4 dígitos escondido nas pistas. |
| 🗣️ **Personagens e interrogatórios** | Falar com suspeitos. As respostas mudam conforme as pistas encontradas. |
| 🕵️ **Caderno do detetive** | As pistas ficam guardadas num caderno. No fim acusa-se um suspeito, e o final depende de acertar e de ter provas. |
| ⏳ **Limite de ações** | 15 ações antes de a segurança fechar o edifício. Dá tensão e um final extra. |
| 🏆 **Conquistas e finais secretos** | Galeria de finais descobertos (ex.: "2 de 4") e medalhas ("Speedrun", "Todas as pistas"). |
| 📊 **Estatísticas** | Jogos feitos, final mais comum, jogo mais rápido. |
| 🎨 **Ambiente** | Imagem por cena, cores de mistério, efeito de máquina de escrever e sons opcionais. Conta para o design. |

### Divisão sugerida (a decidir em grupo)

1. **Vários mistérios e escolha no início**, com as histórias em ficheiros de dados.
2. **Puzzles com código e interrogatórios.**
3. **Caderno do detetive e acusação final**, com finais múltiplos.
4. **Conquistas, estatísticas e design** (mapa, imagens e cores).

## 6. Notas para mais tarde

- **Publicação:** o Streamlit Community Cloud é gratuito e liga-se ao GitHub, mas lá o SQLite pode ser apagado quando a app reinicia. Resolver isto na fase E.
- A base de dados (`data/*.db`) não vai para o GitHub: cada pessoa tem o seu progresso local.
