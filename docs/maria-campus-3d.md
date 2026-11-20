# Contributo da Maria da Cunha — campus jogável

19 de novembro de 2026. Base: ramo `prototype-3d` do grupo.

## O que foi feito

O cenário do colega passa a ter um modo opcional que permite jogar o mistério
**O quinto elemento**, usando as regras e os textos que o grupo já escreveu.
A aplicação Streamlit e o passeio visual original continuam disponíveis.

- Painel com texto da cena, ações de investigação e botões para mudar de sala.
- Inventário com os dois objetos e explicação das ações bloqueadas.
- Caderno que reúne apenas as pistas já descobertas, sem revelar finais antecipadamente.
- Escolha com a Leonor recordada, dois finais existentes e paragem das ações ao terminar.
- Guardar e retomar pelo mesmo nome, incluindo idioma, sala, objetos e decisões.
- Confirmação antes de recomeçar, com opção de cancelar.
- Interface em português e inglês, foco de teclado e layout adaptável.
- Modo de texto automático quando o cenário 3D não carrega; também pode ser escolhido.
- Movimento 3D livre por todo o mapa. Ao atravessar a porta de uma sala, o ecrã pede ao servidor
  (`enter` em `campus_game.py`) para viajar com as ações do próprio jogo. Se a porta estiver
  bloqueada, aparece a explicação, nada muda e o boneco volta ao corredor. Investigar só funciona
  com o boneco dentro da sala da cena guardada.
- Um jogo novo começa no exterior, na praça, à frente de um letreiro **NOVA** grande, em 3D e
  iluminado (construído com formas simples em `game3d.html`). O boneco entra no edifício pelas
  portas de vidro. Um jogo retomado começa na sala guardada (`fresh` em `campus_game.py`).
- Menos lag no 3D: sem o passo de oclusão ambiente (o mais pesado), só as 10 luzes mais próximas do
  boneco ficam acesas (`updateLights`), resolução limitada a 1,25×, sombras mais leves e o mar a
  recalcular normais a cada 4 imagens. Num browser sem placa gráfica, o tempo por imagem desceu de
  cerca de 1040 ms para 465 ms. O boneco anda a 4,8 (antes 3,6).

## Como experimentar

Na raiz do projeto, neste ramo:

```sh
uv sync
uv run python prototypes/campus-3d/server3d.py
```

Abrir http://127.0.0.1:8765 e manter o terminal aberto.
O mesmo nome retoma a partida. Ctrl+C termina o servidor.
Este protótipo usa `data/campus3d.db`, separado do progresso da aplicação Streamlit.
É uma demonstração local, não uma versão publicada na Internet.

## Onde estão as alterações

| Ficheiro | Responsabilidade |
|---|---|
| `prototypes/campus-3d/campus_game.py:9` | Prepara a cena, ações, inventário e caderno a partir do jogo existente. |
| `prototypes/campus-3d/campus_game.py:55` | Valida os pedidos e chama abrir, jogar ou recomeçar. |
| `prototypes/campus-3d/server3d.py:18` | Recebe os pedidos do navegador no servidor local. |
| `prototypes/campus-3d/play.js` | Controlos, mensagens, confirmação e apresentação do estado. |
| `prototypes/campus-3d/play.css` | Apresentação do painel e modo de texto. |
| `prototypes/campus-3d/campus_text.py` | Rótulos da interface nos dois idiomas. |
| `prototypes/campus-3d/page3d.py:76` | Acrescenta o modo jogável sem retirar o passeio visual. |
| `prototypes/campus-3d/game3d.html` | Liga a sala/personagens ao progresso e deteta falhas WebGL. |
| `tests/test_campus_3d.py` | 21 verificações novas do adaptador e do servidor. |
| `specs/playable-campus-3d.md` | Âmbito desta melhoria. |
| `docs/plano-do-projeto.md` | Atualização do estado do projeto. |

`story.py`, `logic.py`, `db.py`, `game.py`, `app.py`, as imagens e os testes anteriores
não foram alterados. As alterações acrescentam uma interface ao trabalho existente;
não substituem a história, os finais ou as regras dos colegas.

## Validação realizada

- `uv run pytest -q`: **77 testes passaram** (56 existentes + 21 novos).
- Sintaxe JavaScript verificada com `node --check`.
- No navegador: recolha dos objetos, rota bloqueada, decisão de ajudar a Leonor,
  retoma após atualizar a página, cancelamento e confirmação de reinício e os dois finais.
- O navegador de teste não disponibiliza WebGL. Foi verificado o modo de texto
  automático, mas **o cenário 3D e a sua ligação visual ao progresso precisam de
  ser testados num navegador com WebGL**. O layout móvel também precisa de revisão visual.

## Próximos passos do grupo

1. Outro elemento revê este ramo e experimenta o modo jogável com WebGL.
2. Confirmar o aspeto em telemóvel e se a posição das personagens é adequada.
3. Decidir se o protótipo será integrado na entrega ou apresentado como extensão.
4. Rever e integrar primeiro o trabalho `prototype-3d`, respeitando as dependências.

As alterações foram preparadas com apoio de IA. A Maria e o grupo devem compreender
a ligação entre os botões, `campus_game.py` e as funções existentes antes da apresentação.
