# História — O quinto elemento

O mapa da história **tal como está no jogo hoje**: quem é quem, onde está cada prova e como acaba a noite.
Os textos exatos estão no código: `story.py` (cenas e finais, nos dois jogos), `prototypes/campus-3d/campus_people.py`
(as conversas) e `prototypes/campus-3d/campus_case.py` (as provas e a audiência). As falas todas, em português e
inglês, estão em [guiao-conversas.md](guiao-conversas.md). Cada mudança tem a sua spec em `specs/` (ver
[specs/README.md](../specs/README.md)).

Os nomes em letra de código (por exemplo `study_room`) são os identificadores do código, por isso estão em inglês.
A tradução inglesa deste ficheiro é [story-en.md](story-en.md): se um mudar, o outro muda também.

## 1. Resumo

Na véspera da apresentação, aparece uma quinta pessoa na fotografia do teu grupo de quatro. O nome dela, Duarte,
está na capa do relatório, e o grupo recebeu mensagens que parecem provar que ele sempre participou. Tens a noite
(das 22:30 às 23:00, no jogo 3D) para juntar as provas e mostrá-las ao professor, no auditório, antes que ele feche
a lista de grupos.

## 2. Personagens

| Personagem | Onde está | Papel |
|---|---|---|
| **Tu** | — | O jogador, membro do grupo de quatro. |
| **Rita** | Sala de estudo | Colega de grupo. Ajuda a encontrar a pen e lembra-se de que o dia da fotografia foi um sábado. |
| **Funcionária** | Reprografia | Guarda o pedido original da fotografia; contigo, reconstrói a fotografia rasgada. |
| **Leonor** | Biblioteca | Colega de grupo. Se lhe mostrares a fotografia, ajuda-te; lembra-se do teste de Finanças. Sai às 22:45 se ainda não tiver aceitado ajudar. |
| **Tomás** | Sala de informática | Colega de grupo. Explica a regra do código do computador 12. |
| **José, o segurança** | Entrada | Tem as gravações das câmaras. Só as mostra depois de lhe explicares a situação e lhe mostrares uma prova. |
| **Duarte** | Auditório | O intruso. Não se fala com ele: só fala na audiência, quando entregas as provas. Faz rondas à sala de informática. |
| **Professor** | Auditório | Fecha a lista de grupos. É a ele que entregas as provas. |

Os nomes da Rita, da Leonor e do Tomás podem ser trocados pelos nomes dos teus amigos no início (specs/your-own-group.md).

## 3. Mapa

Todas as salas abrem para o corredor; o auditório está sempre aberto.

```
              Reprografia   Sala de estudo   Biblioteca
Entrada ───────────────────── corredor ─────────────────────
(segurança)         Sala de informática      Auditório
```

## 4. As quatro provas para o professor

| Prova | Como a consegues | Desfaz a afirmação do Duarte |
|---|---|---|
| **O histórico dos ficheiros** | Encontras a pen na mesa da sala de estudo; no computador 12 metes o código (o dia da fotografia, que o grupo ajuda a descobrir) e abres os ficheiros. | "O meu nome está na capa desde o primeiro rascunho." |
| **A fotografia original** | Na reprografia, reconstróis a fotografia rasgada com a funcionária. | "Cinco pessoas na fotografia, e eu sou o da direita." |
| **O backup das conversas** | No computador 12, depois de abrires os ficheiros, guardas o backup das conversas originais. | "Tenho semanas de mensagens no grupo." |
| **A gravação da câmara** | Com o José: explicas a situação, mostras-lhe a fotografia ou os ficheiros, ligas os cabos e guardas a imagem da sala de informática às 23:47. | "Nem cá estive ontem à noite." |

A pen sozinha não é uma prova: a prova é o histórico que está dentro dela, depois de o abrires.

## 5. O professor e o fim da noite

Na primeira fala, o professor oferece duas coisas:
- **"📁 Mostrar uma prova":** escolhes as provas que tens e entregas-lhas.
  - Se faltar alguma, ele diz só quantas faltam ("Falta-lhe uma das provas. Volte quando a tiver.") e a noite continua.
  - Com as quatro, o Duarte faz as suas afirmações, cada uma cai com a sua prova, e o caso fica encerrado.
- **"Perguntar quantos elementos tem o grupo":** "Cinco" → "Só somos quatro" → "Vou trazer provas", e a conversa acaba.

## 6. Finais

| Final | Quando |
|---|---|
| **Caso encerrado** (`full_case`) | Entregas as quatro provas ao professor. O quinto nome é riscado. |
| **A faculdade fechou** | Chegam as 23:00 sem teres entregado todas as provas: o quinto nome continua na capa. |
| **Créditos roubados** (`stolen_credits`) | No jogo simples (`app.py`), quando apresentas as provas com alguma em falta. |

Não há outros finais: acusar a Leonor, "O impostor" e o final secreto saíram (specs/three-proofs.md).

## 7. O que custa tempo

Encontrar uma pista não custa nada. Custam minutos as escolhas erradas: uma prova errada (2), um sítio errado na mesa (1),
um código errado (2), uma resposta agressiva (5) e ser apanhado pelo Duarte no computador 12 antes de guardares o backup (3).
O jogo simples (`app.py`) não tem relógio.

## 8. Imagens

Ilustrações em `assets/`, usadas pelo jogo simples (`app.py`).

| Imagem | Ficheiro |
|---|---|
| Capa (a fotografia de grupo com cinco pessoas) | `assets/cover.jpg` |
| Sala de estudo, reprografia, biblioteca, sala de informática, auditório | `assets/study_room.jpg`, `print_shop.jpg`, `library.jpg`, `computer_lab.jpg`, `auditorium.jpg` |
| Pen e fotografia original | `assets/usb_stick.jpg`, `assets/original_photo.jpg` |
| Final "Créditos roubados" | `assets/ending_stolen_credits.jpg` |

`assets/ending_impostor.jpg` é do final que saiu e já não é usada.
