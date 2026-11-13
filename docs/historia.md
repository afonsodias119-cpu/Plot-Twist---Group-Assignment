# História — O quinto elemento

Mapa completo da história do jogo: cenas, objetos, decisões e finais.
**Estado: proposta, a rever pelo grupo.** Nada disto está ainda no código.

Os nomes em letra de código (por exemplo `study_room`) são os identificadores que vão para o código e para o ficheiro de dados, por isso estão em inglês. Os textos que o jogador lê estão em português.

## 1. Resumo

Na véspera da apresentação, aparece uma quinta pessoa na fotografia do teu grupo de quatro. O nome dela está no relatório e todos os colegas receberam mensagens que parecem provar que sempre participou. Só tu sabes que há alguma coisa errada.

- **Objetivo:** provar que o intruso está a tentar apropriar-se do trabalho.
- **Local:** Nova SBE, à noite.
- **Duração:** o brief pede cerca de 10 minutos. A versão base é mais curta: os caminhos mais curtos têm 6 e 12 ações (secção 8). Medimos o tempo quando o jogo estiver jogável; os extras da fase D (secção 12) servem para o alongar.

## 2. Personagens

| Personagem | Papel |
|---|---|
| **Tu** | O jogador. Membro do grupo de quatro. |
| **Leonor** | Colega de grupo. Recebeu as mensagens falsas. Pode ajudar-te ou virar-te as costas. |
| **Duarte Sequeira** | O intruso. Acrescentou o seu nome ao relatório e alterou a fotografia. |
| **O professor** | Está no auditório a fechar a lista de grupos para o dia seguinte. |
| **Funcionária da reprografia** | Guarda o pedido original de impressão da fotografia. |

Os nomes são inventados. Se houver alguém no curso com um destes nomes, trocamos.

## 3. Mapa

A sala de estudo é o centro. Todas as outras salas ligam à sala de estudo.

```
                 Biblioteca
                     |
Reprografia --- Sala de estudo --- Sala de informática
                     |
                 Auditório (bloqueado até veres os ficheiros antigos)
```

| Cena | Identificador | Liga a |
|---|---|---|
| Sala de estudo (início) | `study_room` | `print_shop`, `library`, `computer_lab`, `auditorium` |
| Reprografia | `print_shop` | `study_room` |
| Biblioteca | `library` | `study_room` |
| Sala de informática | `computer_lab` | `study_room` |
| Auditório | `auditorium` | `study_room` |

## 4. Objetos

| Objeto | Identificador | Onde se apanha | Para que serve |
|---|---|---|---|
| Pen com o histórico do projeto | `usb_stick` | Sala de estudo, na gaveta do grupo | Desbloqueia a consulta dos ficheiros antigos na sala de informática |
| Fotografia original impressa | `original_photo` | Reprografia | Convence a Leonor a ouvir-te na biblioteca |

Regras dos objetos (vêm do brief):

- Cada objeto apanha-se uma só vez por jogo.
- Usar um objeto não o gasta: fica no inventário até ao fim.

## 5. O que o jogo memoriza

Além da cena atual e do inventário, o jogo guarda três coisas:

| O quê | Identificador | Valores | Muda quando |
|---|---|---|---|
| A decisão com a Leonor | `colleague_choice` | `none`, `help`, `accused` | Escolhes pedir ajuda ou acusar. Só se escolhe uma vez. |
| Se já viste os ficheiros antigos | `files_viewed` | `false`, `true` | Consultas os ficheiros com a pen |
| O final atingido | `ending` | `none`, `impostor`, `stolen_credits` | Apresentas as provas no auditório |

## 6. Cenas

Há três regras que valem para todas as cenas:

- As ações "Ir para…" e "Voltar…" mudam de cena. O resultado visível é o texto da cena nova. As outras ações mantêm-te na mesma cena e mostram um texto de resultado.
- Uma ação bloqueada mostra a explicação e **não muda nada**: nem a cena, nem o inventário, nem o que está guardado.
- Uma ação que já foi feita (objeto apanhado, decisão tomada, ficheiros vistos) deixa de aparecer. Se mesmo assim for pedida às regras, é rejeitada e não muda nada.

Nas tabelas, o texto que o jogador lê está em itálico.

### 6.1 Sala de estudo — `study_room` (cena inicial)

**Texto:**
> É noite, véspera da apresentação. Na pasta do grupo, a fotografia mostra cinco pessoas. Vocês são quatro. Na capa do relatório há um quinto nome: Duarte Sequeira. No chat, os teus colegas garantem que ele "esteve sempre connosco". Só tu sabes que isso é mentira.

**Texto extra depois de apanhares a pen:**
> A gaveta do grupo está vazia.

| Ação | Condição | Resultado |
|---|---|---|
| Abrir a gaveta do grupo | Ainda não tens a pen | Ganhas `usb_stick`. Texto: *Encontras a pen onde o grupo guardava as cópias de segurança do projeto. Guardas a pen.* Depois disto, a ação deixa de aparecer. |
| Ir para a reprografia | — | Vais para `print_shop` |
| Ir para a biblioteca | — | Vais para `library` |
| Ir para a sala de informática | — | Vais para `computer_lab` |
| Ir para o auditório | `files_viewed` é `true` | Vais para `auditorium` |

**Se o auditório estiver bloqueado:**
> Ainda não tens provas. O professor não te vai ouvir só com uma suspeita.

### 6.2 Reprografia — `print_shop`

**Texto:**
> A reprografia está quase a fechar. A funcionária lembra-se do vosso grupo: imprimiram aqui a fotografia para a capa do relatório na semana passada.

**Texto extra depois de apanhares a fotografia:**
> A funcionária já te deu a cópia do pedido original.

| Ação | Condição | Resultado |
|---|---|---|
| Pedir uma cópia do pedido original | Ainda não tens a fotografia | Ganhas `original_photo`. Texto: *A funcionária volta a imprimir o ficheiro que ficou guardado no pedido. Na fotografia original estão quatro pessoas. Guardas a fotografia.* Depois disto, a ação deixa de aparecer. |
| Voltar à sala de estudo | — | Vais para `study_room` |

### 6.3 Biblioteca — `library`

**Texto (antes da decisão):**
> A Leonor, a tua colega de grupo, está a estudar numa mesa ao fundo. Foi uma das pessoas que recebeu as mensagens do Duarte.

**Texto depois de pedires ajuda:**
> A Leonor está a guardar capturas de ecrã das mensagens. "Eu trato disto. Vemo-nos no auditório."

**Texto depois de a acusares:**
> A mesa da Leonor está vazia.

| Ação | Condição | Resultado |
|---|---|---|
| Mostrar a fotografia e pedir ajuda discretamente | Tens `original_photo` e ainda não decidiste | `colleague_choice` passa a `help`. Texto: *A Leonor compara a fotografia com a do relatório e fica pálida. "Recebi estas mensagens todas ontem à noite, de um número que não conhecia. E algumas têm datas de há três semanas." Promete guardar as mensagens originais e ir ter contigo ao auditório.* |
| Mostrar a fotografia e acusá-la de ajudar o Duarte | Tens `original_photo` e ainda não decidiste | `colleague_choice` passa a `accused`. Texto: *"Achas que eu fazia isso ao grupo?" A Leonor levanta-se, ofendida. "Então não preciso destas mensagens para nada." Apaga a conversa à tua frente e sai.* |
| Voltar à sala de estudo | — | Vais para `study_room` |

**Se tentares qualquer uma das duas ações sem a fotografia:**
> A Leonor encolhe os ombros. "O Duarte esteve sempre no grupo, tenho aqui as mensagens. Tens alguma prova do contrário?"

Depois de escolheres, as duas ações deixam de aparecer. A decisão não se pode mudar.

### 6.4 Sala de informática — `computer_lab`

**Texto:**
> A sala de informática está vazia. O computador 12 ainda está ligado: é o que o grupo usava para trabalhar no projeto.

**Texto extra depois de veres os ficheiros:**
> Já comparaste os ficheiros: quatro autores em todas as cópias da pen, e uma alteração na pasta partilhada ontem às 23h47.

| Ação | Condição | Resultado |
|---|---|---|
| Consultar os ficheiros antigos do projeto | Tens `usb_stick` e ainda não os viste | `files_viewed` passa a `true`. Texto: *Ligas a pen ao computador 12 e comparas. Nas cópias de segurança da pen, todas as versões têm quatro autores. Na pasta partilhada, a versão atual foi alterada ontem às 23h47, a partir deste mesmo computador: alguém acrescentou "Duarte Sequeira" ao relatório e trocou a fotografia. Recuperas a versão original do trabalho.* A pen fica no inventário. Depois disto, a ação deixa de aparecer. |
| Voltar à sala de estudo | — | Vais para `study_room` |

**Se tentares consultar sem a pen:**
> A pasta partilhada só mostra a versão atual, já com cinco nomes. Precisas da cópia de segurança do grupo.

### 6.5 Auditório — `auditorium`

**Texto:**
> O professor está no auditório a fechar a lista de grupos para amanhã. O Duarte está sentado na primeira fila, com um sorriso calmo.

| Ação | Condição | Resultado |
|---|---|---|
| Apresentar as provas ao professor | — | O jogo termina. O final depende de `colleague_choice` (ver secção 7). |
| Voltar à sala de estudo | — | Vais para `study_room` |

## 7. Finais

Depois de um final, as ações da história param. O jogador pode rever o resultado ou começar um jogo novo.

### Final 1 — "O impostor" (`impostor`)

**Condição:** apresentas as provas com `colleague_choice` igual a `help`.

> Mostras o histórico da pen: quatro autores até ontem à noite. A Leonor entra e entrega as mensagens que guardou: foram todas enviadas na mesma noite, de um número novo, com datas falsas. O professor risca o quinto nome da lista. O Duarte sai do auditório sem dizer nada. Amanhã apresentam os quatro.

### Final 2 — "Créditos roubados" (`stolen_credits`)

**Condição:** apresentas as provas com `colleague_choice` igual a `accused` ou `none`.

> Mostras o histórico da pen: o trabalho original está recuperado e tinha quatro autores até ontem à noite. Mas o Duarte levanta o telemóvel: "Tenho mensagens de todos a provar que participei." Sem as mensagens originais, não consegues provar que são falsas. O professor suspira: "Sem provas de que as mensagens são falsas, o nome fica." Amanhã apresentam os cinco.

## 8. Todas as combinações

| Viste os ficheiros? | Decisão com a Leonor | O que acontece |
|---|---|---|
| Não | Qualquer uma | O auditório está bloqueado. O jogo continua. |
| Sim | Pediste ajuda | Final 1 — "O impostor" |
| Sim | Acusaste-a | Final 2 — "Créditos roubados" |
| Sim | Nunca falaste com ela | Final 2 — "Créditos roubados" |

Não há becos sem saída: a pen e a fotografia estão sempre disponíveis até serem apanhadas, por isso qualquer jogo consegue chegar a um final. A única coisa que não se pode desfazer é a decisão com a Leonor.

**Caminho mais curto para cada final:**

- **Final 1 (12 ações):** abrir a gaveta → reprografia → pedir a cópia → sala de estudo → biblioteca → pedir ajuda → sala de estudo → sala de informática → consultar os ficheiros → sala de estudo → auditório → apresentar as provas.
- **Final 2 (6 ações):** abrir a gaveta → sala de informática → consultar os ficheiros → sala de estudo → auditório → apresentar as provas.

## 9. Como a história cumpre o brief

Requisitos de conteúdo de [plot-twist-brd.md](plot-twist-brd.md):

| O brief pede | Na nossa história |
|---|---|
| Pelo menos 5 cenas | 5: sala de estudo, reprografia, biblioteca, sala de informática, auditório |
| Pelo menos 2 objetos | 2: pen e fotografia original |
| Um objeto desbloqueia uma ação | A pen desbloqueia a consulta dos ficheiros. A fotografia desbloqueia a conversa com a Leonor. |
| 2 finais, um depende de uma escolha anterior | "O impostor" e "Créditos roubados". Dependem da decisão com a Leonor. |
| Uma decisão memorizada afeta uma ação ou um final mais tarde | `colleague_choice` decide o final. `files_viewed` abre o auditório. |

Cenários de aceitação (vão ser os testes):

| Cenário | Como se testa nesta história |
|---|---|
| **A1** Caminho bloqueado | Jogo novo, tentar ir para o auditório: é rejeitado, continuas na sala de estudo e o inventário não muda. Com a pen mas sem ter visto os ficheiros, ir para o auditório também é rejeitado. Na sala de informática, tentar consultar os ficheiros sem a pen: é rejeitado, continuas na sala de informática, o inventário não muda e `files_viewed` continua `false`. |
| **A2** Caminho desbloqueado | Com a pen, na sala de informática, consultar os ficheiros é aceite e `files_viewed` passa a `true`. De volta à sala de estudo, ir para o auditório é aceite: a cena passa a `auditorium` e a pen continua no inventário. |
| **A3** Sem duplicados | Depois de apanhar a pen, pedir outra vez a ação de abrir a gaveta (no ecrã já não aparece, mas o teste pede-a diretamente às regras): é rejeitada e continuas com uma só pen. |
| **A4** Continuar jogo | Apanhar a pen, consultar os ficheiros, apanhar a fotografia e pedir ajuda à Leonor. Fechar e abrir a app (no teste: gravar e voltar a carregar o jogo da base de dados): a cena (`library`), os dois objetos, a decisão (`help`) e `files_viewed` (`true`) voltam iguais. De volta à sala de estudo, ir para o auditório continua a ser aceite. Reabrir a app depois de um final: o jogo continua terminado. |
| **A5** Dois finais | Os dois caminhos da secção 8 chegam a finais diferentes. Depois de um final, as ações da história são rejeitadas. |
| **A6** Recomeçar em segurança | Cancelar mantém o progresso (o jogo gravado fica igual). Confirmar volta à sala de estudo, com o inventário vazio, `colleague_choice` em `none`, `files_viewed` em `false` e `ending` em `none`. Testar também a partir de um jogo já terminado: depois de confirmar, as ações voltam a ser aceites. |

## 10. Imagens

Ilustrações detalhadas, todas no mesmo estilo, feitas antes e guardadas em `assets/`. São 10:

| Imagem | Ficheiro sugerido |
|---|---|
| Capa do jogo (a fotografia de grupo com cinco pessoas) | `assets/cover.png` |
| Sala de estudo | `assets/study_room.png` |
| Reprografia | `assets/print_shop.png` |
| Biblioteca | `assets/library.png` |
| Sala de informática | `assets/computer_lab.png` |
| Auditório | `assets/auditorium.png` |
| Pen | `assets/usb_stick.png` |
| Fotografia original | `assets/original_photo.png` |
| Final "O impostor" | `assets/ending_impostor.png` |
| Final "Créditos roubados" | `assets/ending_stolen_credits.png` |

**Estilo comum (a confirmar):** ilustração digital detalhada, ambiente de mistério, campus universitário moderno à noite, luz fria azulada com pontos de luz quente, sem texto na imagem. As pessoas aparecem de costas ou em silhueta, para não parecerem ninguém real.

## 11. Em aberto — para o grupo decidir

1. **Nomes.** "Leonor" e "Duarte Sequeira" servem?
2. **Língua do jogo.** Os textos estão em português. Se a apresentação for em inglês, traduzimos os textos (o código não muda, porque a história é um ficheiro de dados).
3. **Ações bloqueadas.** A proposta é mostrar a ação e explicar porque está bloqueada. A alternativa é esconder a ação até ser possível. O brief aceita as duas.
4. **Pen e auditório.** No brief, o exemplo é "chave abre porta". Aqui são dois passos: a pen abre os ficheiros, e ver os ficheiros abre o auditório. Fica mais interessante, mas temos de saber explicar isto na apresentação. A alternativa simples é o auditório exigir a pen diretamente.
5. **Atalhos entre salas.** Agora tudo passa pela sala de estudo. Podemos ligar salas entre si (por exemplo biblioteca e reprografia) para o jogador andar menos.

## 12. Onde encaixam os extras (fase D)

- **Puzzle com código:** o computador 12 pede uma palavra-passe de 4 dígitos, escondida nas pistas.
- **Caderno do detetive e acusação:** as pistas ficam num caderno e, no auditório, o jogador escolhe quem acusar.
- **Limite de ações:** "o edifício fecha às 23h" dá um terceiro final.
- **Vários mistérios:** esta história fica num ficheiro de dados, e um segundo mistério na Nova SBE é outro ficheiro.
