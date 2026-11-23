# Plano do projeto — Plot Twist (trabalho de grupo)

Documento de referência da equipa. Resume o que foi decidido até agora e o que falta fazer.
Última atualização: 22/11/2026 (horário da noite no branch `night-schedule`, por cima das provas e audiência).

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
| **D. Extras criativos** | Uma funcionalidade por pessoa | Os 4 | ✅ 3D jogável no `main` (Maria + Afonso) e puzzle do chat de grupo (Guilherme). 🔄 Provas e audiência (`specs/evidence-and-hearing.md`, branch `evidence-and-hearing`): mostrar provas nas conversas, três pessoas que cedem e a audiência com as três afirmações do Duarte; código e testes feitos (299 testes a passar), falta a verificação no browser (3D e modo de texto, nas duas línguas), o Pull Request e a revisão. 🔄 Horário da noite (`specs/night-schedule.md`, branch `night-schedule`, por cima das provas): o servidor passa a saber o minuto do campus (operação `time`, tabela de custos em `campus_clock.py`), a funcionária sai às 22:25 e a Leonor às 22:30 (se estiver indecisa), uma pista perdida não fecha o auditório, o número desconhecido avisa das horas e das rondas, e o Duarte apanha quem estiver no chat às 22:27, 22:34 e 22:41. Na página: a hora do campus antes da contagem, a nota da grade (e no diário), "Tarde demais" nas pistas, a conversa que acaba quando a pessoa sai, o Duarte à porta da sala de informática no 3D. Código e testes feitos (347 testes a passar); verificado no browser com uma base de dados de rascunho (saída da funcionária, aviso, apanhado no computador 12, nota da grade, modo de texto); falta o Pull Request e a revisão. 🔄 Noites anteriores (`specs/earlier-nights.md`, branch `earlier-nights`, por cima do horário): o jogo lembra-se de cada noite acabada de um nome (tabela `runs` em `db.py`, regras em `campus_memory.py`). Na noite 2 o número desconhecido diz "Outra vez tu?" (e continua no telemóvel depois do "Novo jogo"); a partir da noite 3 os avisos das rondas são dele. Seis respostas ↺ só aparecem a partir de uma certa noite e só junto com a primeira fala da conversa (duas são atalhos para as afirmações do Tomás e da Rita). No ecrã inicial, a quinta figura da fotografia do caso muda de noite para noite (mais escura, o casaco, o cachecol e o chapéu do detetive, depois a tua inicial) e uma linha por baixo do nome diz que noite é. Com os quatro finais vistos em noites anteriores, uma audiência perfeita com a palavra do Tomás e a da Rita dá um final verdadeiro, que só o servidor conhece; depois dele a fotografia mostra quatro pessoas. Código e testes feitos (378 testes a passar, mais `tests/continuous-conversations.cjs`); falta o Pull Request e a revisão |
| **E. Publicar e ensaiar** | Link público (semana 9, não no último dia) e ensaio de perguntas | Os 4 | 🔄 publicado em https://plot-twist.streamlit.app/ (`app_3d.py`); falta ensaio e dados da equipa no README |

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

### O backup das conversas, sem chat nem quinto elemento — Maria (23/11/2026)

Alteração preparada em `computer-lab-backup` (nos dois jogos: mexe no `story.py`): depois de abrir os ficheiros, o computador 12 oferece "Guardar o backup das conversas originais", e o auditório passa a pedir os ficheiros e o backup. O chat do grupo e as mensagens para marcar deixam de existir, e o final secreto "O quinto elemento" também. Os três finais passam a depender da escolha da Leonor: ajuda → Caso encerrado; acusada → O impostor (texto novo); sem escolha → Créditos roubados. No 3D, o Tomás cede com o histórico dos ficheiros, o Duarte apanha quem está no computador 12 antes de guardar o backup, e o final verdadeiro abre depois dos três finais. Mudam testes revistos de toda a equipa, com aprovação (lista na spec). Ver `specs/computer-lab-backup.md`.

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
