# Plano do projeto — Plot Twist (trabalho de grupo)

Documento de referência da equipa. Resume o que foi decidido até agora e o que falta fazer.
Última atualização: 13/11/2026.

## 1. O que o curso pede

Fonte: [site do curso](https://nova-sbe-introduction-to-programming.github.io/intro-to-programming-2026/) e [página de avaliação](https://nova-sbe-introduction-to-programming.github.io/intro-to-programming-2026/evaluation.html).
A página da semana 8 (regras detalhadas do trabalho de grupo) ainda não estava publicada a 10/11 — confirmar quando sair.

- **Calendário:** trabalho de grupo nas semanas 8–10; apresentações nas semanas 11–12 (metade dos grupos em cada semana).
- **Nota:** a apresentação vale **40%** da nota final. Nota de grupo, ajustada por pessoa conforme a explicação do código.
- **Formato da apresentação:**
  - **Demo ao vivo num link público** (app publicada). Não são slides nem vídeo.
  - **Explicação do código:** os professores abrem o repositório e fazem perguntas.
- **Critérios:** funciona · design · âmbito e ambição · verificação (testes) · explicação do código.
- ⚠️ **Cada membro é questionado sobre código que NÃO escreveu.** Todos têm de perceber o projeto inteiro.
- Nada se entrega no Moodle: o trabalho vive no GitHub.
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
| **B. Inventar a história** | Mistério, 5+ cenas, objetos, finais e personagens, tudo no papel | Grupo todo | 🔄 proposta escrita em [historia.md](historia.md), falta o grupo rever |
| **C. Versão base** | Jogo mínimo que cumpre o brief, com testes | Afonso + revisão | ⏳ |
| **D. Extras criativos** | Uma funcionalidade por pessoa | Os 4 | ⏳ |
| **E. Publicar e ensaiar** | Link público (semana 9, não no último dia) e ensaio de perguntas | Os 4 | ⏳ |

### Fase A — passos

1. ✅ Clonar o repositório com o GitHub Desktop.
2. ✅ Criar a estrutura do projeto no branch `project-setup`: `pyproject.toml`, `uv.lock`, `.gitignore`, `.python-version`, `app.py` provisório, `tests/conftest.py`, `AGENTS.md`, `README.md` e `docs/`.
3. ✅ Confirmar que corre (`uv run streamlit run app.py`). Commit, branch publicado e Pull Request #1 revisto pelo grupo e com merge feito (10/11/2026).
4. ✅ Proteger o `main` no GitHub: ruleset "Main Protection" ativo (exige PR e 1 aprovação).
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
