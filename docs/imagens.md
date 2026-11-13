# Imagens — prompts para as ilustrações

Prompts para gerar as 10 ilustrações do jogo com uma ferramenta de imagens por IA. A lista de ficheiros está na secção 10 de [historia.md](historia.md).

**Estado: proposta, ainda não testada.** Estes prompts ainda não foram experimentados numa ferramenta de imagens. Contem com duas a quatro tentativas por imagem e ajustem o que for preciso.

Os prompts estão em inglês, porque as ferramentas de imagens respondem melhor em inglês. As explicações estão em português.

## 1. Como usar

1. Escolham **uma só ferramenta** para as dez imagens (por exemplo ChatGPT, Gemini ou Copilot). Misturar ferramentas dá estilos diferentes.
2. Em cada pedido, colem o **bloco de estilo** (secção 2) sem mudar uma palavra e, logo a seguir, o parágrafo da imagem (secção 3).
3. Comecem pela `study_room`. Quando gostarem do resultado, essa passa a ser a imagem de referência. Nos pedidos seguintes, fiquem na mesma conversa ou carreguem essa imagem, e acrescentem no fim:
   `Use exactly the same illustration style, line work and colour palette as the study-room image, but draw a completely new picture: copy only the style, not the room or its furniture.`
4. Sigam esta ordem: `study_room`, `print_shop`, `library`, `computer_lab`, `auditorium`, os dois finais, `cover`, `original_photo` e `usb_stick`.
5. Antes de aceitar uma imagem, verifiquem os pontos de "Confirmar" dessa imagem.
6. Guardem os ficheiros como está explicado na secção 5.

Mais duas regras:

- Não escrevam "Nova SBE" nem nomes de pessoas reais nos pedidos. O campus das imagens é inventado.
- Se o limite diário gratuito obrigar a dividir o trabalho, todos usam a mesma ferramenta e a mesma imagem de referência.

## 2. Bloco de estilo

Cola-se igual no início de todos os pedidos.

```text
Detailed digital illustration in a stylised painterly style, like a hand-painted background from a narrative mystery game. It is clearly an illustration, not a photograph and not photorealistic, with thin dark outlines around the main objects, broad flat brush shapes in two or three tones per surface, crisp readable shapes, and no film grain, noise or rough texture. Every image uses the same limited palette: deep navy and teal for shadows, soft off-white for paper, and warm amber for lamps and for the single clear focal point. Whenever a place is shown, it is a fictional modern university campus at night, built of glass, pale concrete and light wood. The mood is a quiet, curious mystery, calm and never frightening. Any people are anonymous, seen only from behind, in silhouette, cropped or small in the distance, with no facial features. The image contains no text of any kind: no letters, numbers, logos, signs, captions or watermarks anywhere, so pages, screens, book spines and walls carry no writing at all.
```

Se mudarem este bloco a meio, têm de gerar outra vez as imagens já feitas.

## 3. Prompts

As cenas mostram só o que é verdade durante o jogo todo. Por isso não aparece a Leonor na biblioteca (ela sai se for acusada), a gaveta está fechada e não há nenhuma pen ligada ao computador.

O intruso é sempre a mesma figura: um rapaz de cabelo curto com um casaco comprido. A Leonor é a figura do rabo de cavalo alto.

### 3.1 `study_room.jpg` — sala de estudo (larga, 16:9)

```text
Wide landscape image, 16:9 aspect ratio. A small glass-walled group study room at night, seen from just inside the doorway, with nobody in it. A light-wood table stands in the middle under a single low pendant lamp that casts a pool of warm amber light. In that light, as the clear focal point, lies a thick bound report whose front is plain and blank except for one small picture, too small to make out, and beside it a closed laptop and a phone lying face down. Built into the long front edge of the table, facing the viewer and catching the lamp light, is one wide drawer with a small metal handle, firmly and completely closed. Four chairs are pulled up to the table and a fifth chair stands slightly apart in the shadow near the glass wall. Beyond the glass, the dark campus courtyard is deep blue with a few distant warm windows.
```

**Confirmar:** a gaveta vê-se e está fechada. Não há pen, nem pessoas. O portátil está fechado e o telemóvel virado para baixo. A capa do relatório não tem letras. A quinta cadeira é um extra: aceitem a imagem mesmo que o número de cadeiras não esteja certo.

### 3.2 `print_shop.jpg` — reprografia (larga, 16:9)

```text
Wide landscape image, 16:9 aspect ratio. A small campus print shop at closing time, seen from the dim blue corridor outside, looking in through its wide service counter. Above the counter a metal roller shutter is already pulled about a quarter of the way down, drawn as a few broad plain bands. Inside, warm amber light falls on large copiers with closed lids, dark switched-off panels and empty output trays, and on shelves of neatly stacked blank paper. Behind the counter an employee, a woman in a cardigan with her hair in a low bun, stands with her back to us, tidying a stack of paper on a shelf. The counter top is clean and completely empty, and the warm bright opening framed by the dark corridor is the clear focal point. The walls, the shutter and the panel above the counter are plain, bare, unmarked surfaces.
```

**Confirmar:** o balcão está vazio, sem fotografia e sem nada a ser entregue. A cara da funcionária não se vê e o cabelo dela não está em rabo de cavalo (esse é o sinal da Leonor). Não há letreiros, cartazes nem tabelas de preços.

### 3.3 `library.jpg` — biblioteca (larga, 16:9)

```text
Wide landscape image, 16:9 aspect ratio. A quiet university library at night, looking down a long aisle between two tall rows of bookshelves toward the back of the room. At the far end, past the corner of the last bookshelf, only one bare corner of a study table and the warm amber glow of its reading lamp can be seen; the rest of the table and its chairs are hidden from view behind that bookshelf. That glow at the end of the aisle is the clear focal point, while the aisle in front of it lies in deep navy and teal shadow, with faint blue night light from tall windows on one side. The books are simple bands of muted colour with plain spines, and the aisle and the floor are completely empty.
```

**Confirmar:** não se vê ninguém, nem sequer uma sombra ou um braço. Só se vê um canto da mesa, sem livros, portátil nem outros objetos em cima. Se o candeeiro se vir, não faz mal. As lombadas dos livros não têm títulos.

### 3.4 `computer_lab.jpg` — sala de informática (larga, 16:9)

```text
Wide landscape image, 16:9 aspect ratio. An empty university computer room at night, seen from the doorway: neat rows of desks with identical dark monitors, all switched off, fading back into navy shadow. One single computer in the middle of the room is still on, and its screen is the clear focal point: a plain, even, warm cream-amber glow with nothing on it, lighting the keyboard, the mouse and the empty chair pulled slightly back from the desk, as if someone left not long ago. The desk holds only the keyboard and the mouse, and nothing is plugged into the computer. The rest of the room is lit only by faint distant campus lights through the window blinds.
```

**Confirmar:** só um ecrã está ligado. Não há nada ligado ao computador nem nenhuma pen na mesa. Não há números nos ecrãs, nas mesas ou nas paredes. Não há pessoas.

### 3.5 `auditorium.jpg` — auditório (larga, 16:9)

```text
Wide landscape image, 16:9 aspect ratio. A modern university auditorium late at night, seen from the top of the centre aisle at the back, looking down over rows of empty seats in navy shadow toward the front. Down at the front, a single lamp makes a pool of warm amber light on a desk where a professor, a small distant figure bent over a sheet of paper so that no face can be seen, is writing. In the front row, alone, sits a young man with short hair in a long dark coat, seen only from behind as a dark shape against the warm light, leaning back comfortably with one arm resting along the back of the next seat, completely at ease. The pool of light holding these two figures is the clear focal point, and there are no other people in the hall. The large projection screen above them is dark, and the doors and walls are plain and unmarked.
```

**Confirmar:** só há duas pessoas, o professor ao fundo e uma figura de costas na primeira fila. Não se veem caras. A figura sentada parece descontraída, não ameaçadora. Não há sinais de saída com letras.

### 3.6 `ending_impostor.jpg` — final "O impostor" (larga, 16:9)

```text
Wide landscape image, 16:9 aspect ratio. A modern university auditorium late at night, seen from beside the professor's desk at the front, looking across the desk and up the centre aisle between rows of seats. In this image the warm amber light has spread to fill most of the hall, pushing the cold blue out to the edges. In the foreground, on the desk under a lamp, lies a single sheet of paper showing nothing but five identical plain solid grey bars stacked in a column; one bold dark stroke crosses out only the bottom bar, a pen rests beside it, and this crossed-out bar is the clear focal point. In the distance, at the top of the aisle, a young man with short hair in a long dark coat, small and seen from behind, walks out through an open side door with a plain frame into a blue corridor. At the left edge, seen from behind, a student with a high ponytail stands watching him go, holding a softly glowing phone at her side, its screen plain and blank. These two are the only people in the image, and all the seats, including the front row, are empty. The feeling is relief, calm and justice done.
```

**Confirmar:** a folha tem cinco barras lisas e só a última está riscada. Se as barras saírem como letras falsas, gerem outra vez. Há só duas pessoas, as duas de costas: a figura do casaco comprido, pequena, a sair pela porta, e a figura do rabo de cavalo, com o telemóvel na mão. Não há ninguém sentado na primeira fila. A imagem é claramente mais quente do que a do auditório.

### 3.7 `ending_stolen_credits.jpg` — final "Créditos roubados" (larga, 16:9)

```text
Wide landscape image, 16:9 aspect ratio. A modern university auditorium late at night, seen from the centre aisle a few rows behind the front row, looking toward the professor's desk. In this image cold navy and teal fill almost everything, and the warm amber light has shrunk to one small pool on the desk at the front. In the foreground a young man with short hair in a long dark coat stands in the front row, seen from behind from the waist up as a calm, relaxed dark shape, holding a phone up beside his shoulder with its screen turned toward us. In this image the phone screen is the clear focal point and the one cold light: a plain, even blue-white glow with nothing on it. Beyond him, small in the dim amber pool, the professor sits at the desk with lowered shoulders and head bowed over a sheet of paper, so that no face can be seen. On the stage behind the desk, five empty chairs stand in a neat row, waiting for tomorrow. There are no other people in the hall, and the feeling is quiet, bitter and unfair, but not threatening.
```

**Confirmar:** só há duas pessoas, o intruso e o professor. Não aparece a figura do rabo de cavalo: neste final a Leonor não está no auditório, porque saiu ofendida ou porque nunca falaste com ela. O ecrã do telemóvel não tem texto. As cinco cadeiras são um extra: se o número sair errado várias vezes, apaguem a frase que começa por "On the stage behind the desk".

### 3.8 `cover.jpg` — capa (larga, 16:9)

```text
Wide landscape image, 16:9 aspect ratio. A single printed photograph with a thin white border lies flat and slightly tilted on a dark wooden desk at night, seen from directly above. The photograph fills about two thirds of the image width, with dark desk visible all around it, and a warm amber lamp just out of frame lights it. Inside the photograph, exactly five students stand in one straight row, side by side and full height, with a small clear gap between each one. They are backlit dark navy silhouettes with no facial features, standing in front of one large, evenly lit glass wall that glows pale amber from edge to edge, with nothing else behind them. From left to right they are: first, a tall figure with short hair and a backpack hanging from one shoulder; second, a shorter figure with a high ponytail; third, a figure with curly hair holding a laptop under one arm; fourth, a figure in a hooded sweatshirt raising one hand in a small wave; and fifth, at the far right, a young man with short hair in a long coat with both hands in the pockets. The first four stand evenly spaced, while the fifth stands a wider step apart from them and has a thin pale outline, as if he had been added to the picture afterwards. There are five figures in total and no more: nobody stands behind the row, and there are no reflections or distant shapes that look like extra people. Nothing else lies on the desk.
```

**Confirmar:** contem as figuras, têm de ser exatamente cinco. Da esquerda para a direita: mochila, rabo de cavalo, portátil, mão levantada e casaco comprido. A figura do casaco comprido está na ponta direita, um pouco afastada. Não há caras nem letras.

### 3.9 `original_photo.jpg` — fotografia original (quadrada, 1:1)

A forma mais segura de a fazer é a partir da capa, como está explicado na secção 4. Este prompt serve se a ferramenta não conseguir editar a capa.

```text
Square image, 1:1 aspect ratio. This is an item icon, not a scene: one single printed photograph with a thin white border, centred and lying flat with a very slight tilt on a plain, empty, very dark navy background, large enough to fill most of the frame, with no room, furniture, hands or other objects. Inside the photograph, exactly four students stand in one straight row, side by side and full height, with a small clear gap between each one. They are backlit dark navy silhouettes with no facial features, standing in front of one large, evenly lit glass wall that glows pale amber from edge to edge, with nothing else behind them. From left to right they are: first, a tall figure with short hair and a backpack hanging from one shoulder; second, a shorter figure with a high ponytail; third, a figure with curly hair holding a laptop under one arm; and fourth, a figure in a hooded sweatshirt raising one hand in a small wave. To the right of the fourth figure the photograph shows only an empty stretch of the glowing wall. There are four figures in total and no more: nobody stands behind the row, and there are no reflections or distant shapes that look like extra people.
```

**Confirmar:** são exatamente quatro figuras, as mesmas da capa e pela mesma ordem: mochila, rabo de cavalo, portátil e mão levantada. Não há casaco comprido. Se continuar a aparecer uma quinta figura, apaguem a frase que começa por "To the right of the fourth figure" e tentem outra vez.

### 3.10 `usb_stick.jpg` — pen (quadrada, 1:1)

```text
Square image, 1:1 aspect ratio. This is an item icon, not a scene: one single USB flash drive, centred on a plain, empty, very dark navy background and large enough to fill about two thirds of the frame, with no room, furniture, hands, cables or other objects. It is seen in a three-quarter view from slightly above, with a smooth warm amber-orange plastic body, a silver metal connector and a small metal key-ring loop at the other end. A soft warm light runs all around its outline, so that it stands out clearly from the background, with a faint simple shadow beneath it. The body is completely plain, with no brand, symbol, marking or engraving.
```

**Confirmar:** só há um objeto, num fundo liso e escuro, sem mão nem computador. A pen não tem marca, símbolo nem números.

## 4. Problemas comuns

**O número de pessoas está errado.** Contem sempre as figuras antes de aceitar a capa e a fotografia original, incluindo reflexos e formas ao fundo. Se estiver errado, gerem outra vez duas ou três vezes com o mesmo prompt. Se continuar errado, peçam uma correção pequena na mesma conversa:

- Fotografia original com uma figura a mais: `Keep this image exactly the same, but remove the person at the far right.` Se a figura a mais não for a da direita, descrevam-na em vez de "at the far right".
- Capa só com quatro figuras: `Keep this image exactly the same, but add one more backlit silhouette at the far right of the row, a wider step apart from the others: a young man with short hair in a long coat.`
- Capa com figuras a mais: `Keep this image exactly the same, but remove the extra person, so that exactly five remain, from left to right: backpack, high ponytail, laptop, raised hand, long coat.`

Depois da correção, voltem a verificar os pontos de "Confirmar".

**A capa e a fotografia original têm de condizer.** Façam primeiro a capa. Quando tiver exatamente cinco figuras, peçam na mesma conversa:

`Keep this photograph exactly the same, but remove the fifth figure on the far right and fill the gap with the glowing glass wall. Change nothing else.`

A fotografia ocupa cerca de dois terços da largura da capa, por isso não cabe inteira num recorte quadrado. Peçam ainda, na mesma conversa:

`Now show only this same four-person photograph, complete with its thin white border, centred with a very slight tilt on a plain, empty, very dark navy background, as a square 1:1 image. Keep the four figures and the glowing wall exactly as they are.`

Voltem a contar as figuras: têm de ser quatro, pela mesma ordem. Essa imagem é o ícone `original_photo.jpg`.

Se a ferramenta não editar bem, usem o prompt 3.9. Em último caso, sem IA, recortem a capa em quadrado de forma a ficarem só as quatro primeiras figuras (a fotografia fica cortada à direita). Isto funciona porque a quinta figura está afastada, na ponta direita.

**A ferramenta inventou texto.** Olhem com atenção para as folhas, os ecrãs, as lombadas dos livros, as paredes da reprografia, por cima das portas, o corpo da pen e os cantos da imagem. Letras falsas ou ilegíveis também contam como texto. Peçam:

`Remove all letters, numbers and logos and replace them with plain blank shapes. Change nothing else.`

Se não resultar, gerem outra vez. Uma marca pequena num canto pode simplesmente ser recortada. Nas vossas mensagens, evitem as palavras "cover", "title" e "poster", porque levam a ferramenta a escrever um título.

**Vê-se uma cara.** Peçam: `Turn this person so we only see them from behind, with no face visible.`

**Os finais não parecem a mesma sala do auditório.** Gerem os dois finais na mesma conversa da imagem `auditorium` (ou carreguem essa imagem) e acrescentem no fim do pedido:

`This is the same auditorium as in the auditorium image seen from the back of the hall: the same seats, desk and lamp, now from a different camera position.`

**O formato saiu errado.** Algumas ferramentas gratuitas não fazem 16:9 e devolvem uma imagem um pouco mais alta. Aceitem o formato mais largo que houver e recortem em cima e em baixo, escolhendo o corte de forma a não perder o ponto principal. Na maior parte das imagens ele está perto do centro. No final "O impostor" a folha está em baixo e a figura que sai está em cima: vejam bem onde cortam. Se um ícone sair largo em vez de quadrado, peçam: `Make this a square 1:1 image, with the object centred and smaller and more empty background around it.`

## 5. Guardar os ficheiros

- **Imagens largas** (capa, cenas e finais): recortar para 16:9 e redimensionar para **1280 × 720** píxeis.
- **Ícones** (pen e fotografia original): recortar em quadrado e redimensionar para **512 × 512** píxeis.
- Guardar em **JPG**, com qualidade à volta de 80. Cada ficheiro deve ficar abaixo de 300 KB. Se ficar maior, baixem a qualidade para 70.
- Usar os nomes da secção 10 de [historia.md](historia.md) e guardar tudo na pasta `assets/`, na raiz do projeto (ao lado de `app.py`, não dentro de `docs/`). A pasta ainda não existe: criem-na quando guardarem a primeira imagem.

A app Fotografias do Windows 11 faz os três passos: recorta com proporções predefinidas, redimensiona em píxeis e guarda em JPG com a qualidade que escolherem. O Paint também recorta e redimensiona, mas não deixa escolher a qualidade do JPG: se o usarem, guardem em JPG e confirmem só que o ficheiro fica abaixo de 300 KB.

Antes de aceitar cada imagem, vejam-na no tamanho em que vai aparecer no jogo: cerca de 700 píxeis de largura para as imagens largas e cerca de 100 para os ícones. Se o ponto principal não se perceber nesse tamanho, gerem outra vez.
