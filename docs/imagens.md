# Imagens — prompts para as fotografias do jogo

Prompts para gerar as 12 imagens do jogo com uma ferramenta de imagens por IA, num estilo **fotorrealista e cinematográfico**: noite, luz quente âmbar dentro dos edifícios, azul frio lá fora. A spec é [specs/campus-visuals.md](../specs/campus-visuals.md) (secção 6).

**Estado: proposta, ainda não testada.** Contem com duas a quatro tentativas por imagem.

As 10 imagens que estão hoje em `assets/` são ilustrações (o estilo antigo). Misturar ilustrações com fotografias fica estranho, por isso o ideal é gerar as 12 de novo com este estilo. Enquanto não estiverem todas feitas, o jogo continua a funcionar: uma imagem que falta simplesmente não aparece.

Os prompts estão em inglês, porque as ferramentas respondem melhor em inglês. As explicações estão em português.

## 1. Como usar

1. Escolham **uma só ferramenta** para as 12 imagens. Misturar ferramentas dá estilos e caras diferentes.
2. Em cada pedido colem, por esta ordem e sem mudar uma palavra:
   1. o **bloco de estilo** (secção 2);
   2. a **ficha** de cada personagem que aparece nessa imagem (secção 3), se houver;
   3. o prompt da imagem (secção 4).
3. Comecem pelo `campus_exterior`. Quando gostarem, passa a ser a **imagem de referência do estilo**. Nos pedidos seguintes fiquem na mesma conversa ou carreguem-na, e acrescentem no fim:
   `Match exactly the photographic style, lighting, colour grade and lens of the reference image, but show a completely new place.`
4. Para as personagens, a primeira imagem onde cada uma aparece bem passa a ser a **referência dessa personagem**. Depois acrescentem:
   `The person described as <NAME> must look exactly like the person in the reference image: same face, hair and clothes.`
5. Ordem sugerida: `campus_exterior`, `entrance_hall`, `study_room`, `print_shop`, `library`, `computer_lab`, `auditorium`, os dois finais, `cover`, `original_photo` e `usb_stick`.
6. Antes de aceitar uma imagem, verifiquem os pontos de **Confirmar**.
7. Guardem os ficheiros como diz a secção 6.

Mais três regras:

- **Não escrevam "Nova SBE"** nem nomes de pessoas reais nos pedidos. O prompt descreve um campus parecido (edifícios brancos e baixos, vidro, junto à praia), mas inventado. Com o nome verdadeiro, as ferramentas tendem a inventar logótipos e letreiros, ou a recusar o pedido.
- **As pessoas são inventadas.** Se uma cara parecer alguém real (um colega, um professor, uma pessoa famosa), gerem outra vez.
- **Cada imagem só mostra o que é verdade durante o jogo todo.** Por isso a Leonor não aparece na biblioteca (ela sai se for acusada), a gaveta está fechada e não há nenhuma pen ligada ao computador.

## 2. Bloco de estilo

Cola-se igual no início de todos os pedidos. Se o mudarem a meio, têm de gerar outra vez as imagens já feitas.

```text
Photorealistic cinematic film still at night, as if shot on a 35 mm lens with a full-frame camera: realistic materials and proportions, shallow depth of field, very light film grain, gentle haze in the light. Lighting: warm amber tungsten light (about 2700 K) inside buildings, cool deep-blue night light (about 7000 K) outside, with a clear contrast between the two. Colour grade: deep navy and teal shadows, warm amber highlights, soft off-white for paper. Whenever a place is shown, it is a fictional modern university campus on the Atlantic coast: low white concrete buildings with long horizontal lines, large glass walls, light-wood interiors, a wide plaza, and the beach and the ocean right next to it. The mood is a quiet, curious mystery, calm and never frightening. It is not an illustration, not a cartoon and not a 3D render. The image contains no text of any kind: no letters, numbers, logos, signs, captions or watermarks anywhere, so screens, pages, book spines, walls and clothes carry no writing at all.
```

## 3. Fichas das personagens

Colem a ficha de cada personagem que aparece na imagem, logo a seguir ao bloco de estilo. As fichas descrevem sempre a mesma roupa, porque toda a história se passa na mesma noite.

```text
LEONOR: a 21-year-old university student, slim, with long straight dark-brown hair tied in a high ponytail, wearing a mustard-yellow knit sweater with a white shirt collar showing, dark jeans and white trainers, small gold hoop earrings.
```

```text
DUARTE: a 22-year-old young man, tall and lean, with short neat dark-blond hair, clean-shaven, wearing a long charcoal-grey wool overcoat over a black turtleneck, dark trousers and black leather shoes. Calm, confident, relaxed posture.
```

```text
THE PROFESSOR: a man in his late fifties with short grey hair and a short trimmed grey beard, thin rectangular glasses, a navy blazer over a light-blue shirt with no tie.
```

```text
THE CLERK: a woman in her mid-forties with dark hair in a low bun, a burgundy cardigan over a grey top, reading glasses hanging on a cord around her neck.
```

| Imagem | Personagens a colar |
|---|---|
| `print_shop` | THE CLERK |
| `auditorium` | THE PROFESSOR, DUARTE |
| `ending_impostor` | DUARTE, LEONOR |
| `ending_stolen_credits` | DUARTE, THE PROFESSOR |
| `cover` | LEONOR, DUARTE |
| `original_photo` | LEONOR |
| as outras | nenhuma |

## 4. Prompts

### 4.1 `campus_exterior.jpg` — o campus à noite, visto de fora (larga, 16:9)

Aparece no ecrã inicial.

```text
Wide landscape image, 16:9 aspect ratio. The campus seen from the wide open plaza in front of the main entrance, at night, at eye level. Low white concrete buildings with long horizontal lines and tall glass walls glow from inside with warm amber light; in the middle, a glass entrance with its doors lit from within is the clear focal point. To one side, beyond a low wall, the beach and the dark ocean stretch to the horizon under a deep-blue sky, with a faint line of white foam and a few distant lights along the coast. On the plaza, a few students walk in small groups, small in the distance, softly lit by the windows, some carrying bags and laptops. The ground is light paving, slightly damp, reflecting the warm windows. There are no signs, logos or lettering on the buildings.
```

**Confirmar:** vê-se o mar e a entrada iluminada. As pessoas são poucas, pequenas e não se destacam. Não há letras nem logótipos nos edifícios.

### 4.2 `entrance_hall.jpg` — o átrio, logo depois da porta (larga, 16:9)

Aparece no momento "a entrar no edifício", com o texto por cima, em baixo. Por isso a parte de baixo da imagem deve ser escura e calma.

```text
Wide landscape image, 16:9 aspect ratio. The entrance hall of the building at night, seen from just inside the glass doors, as if you had just stepped in. A tall, quiet hall with white concrete walls, a light-wood floor and a wide staircase rising toward an upper floor where one warm light is still on; that distant warm light is the clear focal point. Most of the hall is in soft blue shadow; a few low amber lights along the walls. Behind the viewer, reflected faintly in the glass on one side, the blue night and the sea. The hall is empty and silent. The lower third of the image is dark and simple, with no objects, so that text could be placed there.
```

**Confirmar:** não há pessoas. A parte de baixo é escura e lisa. Não há placas, setas nem letras.

### 4.3 `study_room.jpg` — sala de estudo (larga, 16:9)

```text
Wide landscape image, 16:9 aspect ratio. A small glass-walled group study room at night, seen from just inside the doorway, with nobody in it. A light-wood table stands in the middle under a single low pendant lamp that casts a pool of warm amber light. In that light, as the clear focal point, lies a thick bound report with a plain blank front except for one small printed photograph, too small to make out, and beside it a closed laptop and a phone lying face down. Built into the long front edge of the table, facing the viewer, is one wide drawer with a small metal handle, firmly and completely closed. Four chairs are pulled up to the table and a fifth chair stands slightly apart in the shadow near the glass wall. Beyond the glass, the dark campus and a glimpse of the blue night sea.
```

**Confirmar:** a gaveta vê-se e está fechada. Não há pen nem pessoas. O portátil está fechado e o telemóvel virado para baixo. A capa do relatório não tem letras.

### 4.4 `print_shop.jpg` — reprografia (larga, 16:9)

Colar antes: **THE CLERK**.

```text
Wide landscape image, 16:9 aspect ratio. A small campus print shop at closing time, seen from the dim blue corridor outside, looking in through its wide service counter. Above the counter a metal roller shutter is already pulled about a quarter of the way down. Inside, warm amber light falls on large copiers with closed lids and dark, switched-off panels, and on shelves of neatly stacked blank paper. Behind the counter stands THE CLERK, seen in three-quarter view from the side, tidying a stack of paper on a shelf, her face partly turned away. The counter top is clean and completely empty, and the warm bright opening framed by the dark corridor is the clear focal point. The walls, the shutter and the panel above the counter are plain and unmarked.
```

**Confirmar:** o balcão está vazio, sem fotografia. A funcionária tem o cabelo num carrapito baixo e o casaco cor de vinho (não é rabo de cavalo: esse é o sinal da Leonor). Não há letreiros nem tabelas de preços.

### 4.5 `library.jpg` — biblioteca (larga, 16:9)

```text
Wide landscape image, 16:9 aspect ratio. A quiet university library at night, looking down a long aisle between two tall rows of bookshelves toward the back of the room. At the far end, past the corner of the last bookshelf, only one bare corner of a study table and the warm amber glow of its reading lamp can be seen; the rest of the table and its chairs are hidden behind that bookshelf. That glow at the end of the aisle is the clear focal point, while the aisle lies in deep navy and teal shadow, with faint blue night light from tall windows on one side. The books have plain spines in muted colours, and the aisle is completely empty.
```

**Confirmar:** não se vê ninguém, nem uma sombra ou um braço. As lombadas dos livros não têm títulos.

### 4.6 `computer_lab.jpg` — sala de informática (larga, 16:9)

```text
Wide landscape image, 16:9 aspect ratio. An empty university computer room at night, seen from the doorway: neat rows of desks with identical dark monitors, all switched off, fading back into navy shadow. One single computer in the middle of the room is still on, and its screen is the clear focal point: a plain, even, warm cream glow with nothing on it, lighting the keyboard, the mouse and an empty office chair pulled slightly back from the desk, as if someone left not long ago. Nothing is plugged into the computer. The rest of the room is lit only by faint blue campus light through the window blinds.
```

**Confirmar:** só um ecrã está ligado e não tem nada escrito. Não há pen, nem números nas mesas, nem pessoas.

### 4.7 `auditorium.jpg` — auditório (larga, 16:9)

Colar antes: **THE PROFESSOR** e **DUARTE**.

```text
Wide landscape image, 16:9 aspect ratio. A modern university auditorium late at night, seen from the top of the centre aisle, looking down over rows of empty seats in navy shadow toward the front. Down at the front, a single desk lamp makes a pool of warm amber light on a desk where THE PROFESSOR, small in the distance, is bent over a sheet of paper, writing. In the front row, alone, sits DUARTE, seen from behind and slightly from the side, leaning back with one arm resting along the back of the next seat, completely at ease. The pool of light holding these two people is the clear focal point, and there is nobody else in the hall. The large projection screen above them is dark, and the walls and doors are plain and unmarked.
```

**Confirmar:** só há duas pessoas. O Duarte tem o casaco comprido cinzento-escuro e parece descontraído, não ameaçador. Não há sinais de saída com letras.

### 4.8 `ending_impostor.jpg` — final "O impostor" (larga, 16:9)

Colar antes: **DUARTE** e **LEONOR**. Gerar na mesma conversa do `auditorium`.

```text
Wide landscape image, 16:9 aspect ratio. The same auditorium late at night, now seen from beside the professor's desk at the front, looking up the centre aisle. Warm amber light has spread to fill most of the hall, pushing the cold blue to the edges. In the foreground, on the desk under the lamp, lies a single sheet of paper showing only five identical plain grey bars stacked in a column; one bold dark stroke crosses out only the bottom bar, a pen rests beside it, and this crossed-out bar is the clear focal point. In the distance, at the top of the aisle, DUARTE, small and seen from behind, walks out through an open side door into a blue corridor. At the left edge stands LEONOR, seen from the side, watching him go, holding a phone with a plain glowing screen at her side. These are the only two people, and every seat is empty. The feeling is relief, calm and justice done.
```

**Confirmar:** a folha tem cinco barras lisas e só a última está riscada (se as barras parecerem letras, gerem outra vez). Só há duas pessoas. A imagem é claramente mais quente do que a do auditório.

### 4.9 `ending_stolen_credits.jpg` — final "Créditos roubados" (larga, 16:9)

Colar antes: **DUARTE** e **THE PROFESSOR**. Gerar na mesma conversa do `auditorium`.

```text
Wide landscape image, 16:9 aspect ratio. The same auditorium late at night, seen from the centre aisle a few rows behind the front row, looking toward the professor's desk. Cold navy and teal fill almost everything, and the warm amber light has shrunk to one small pool on the desk. In the foreground DUARTE stands in the front row, seen from behind from the waist up, calm and relaxed, holding a phone up beside his shoulder with its screen turned toward us: a plain, even blue-white glow with nothing on it, the clear focal point and the one cold light. Beyond him, small in the dim amber pool, THE PROFESSOR sits at the desk with lowered shoulders, head bowed over a sheet of paper. On the stage behind the desk, five empty chairs stand in a neat row. There is nobody else in the hall, and the feeling is quiet, bitter and unfair, but not threatening.
```

**Confirmar:** só há duas pessoas. A Leonor não aparece (neste final ela não está no auditório). O ecrã do telemóvel não tem texto.

### 4.10 `cover.jpg` — a fotografia de grupo com cinco pessoas (larga, 16:9)

Colar antes: **LEONOR** e **DUARTE**. Na pré-visualização esta imagem só aparece no ecrã inicial se não houver `campus_exterior.jpg`, mas é a base da `original_photo`.

```text
Wide landscape image, 16:9 aspect ratio. A single printed photograph with a thin white border lies flat and slightly tilted on a dark wooden desk at night, seen from directly above, lit by a warm lamp just out of frame. The photograph fills about two thirds of the image width. Inside it, exactly five students stand in one straight row, side by side, full height, with a small gap between each one, smiling naturally in front of a large glass wall of the campus in daylight. From left to right: first, a tall young man with short brown hair and a backpack on one shoulder; second, LEONOR; third, a young woman with short curly black hair holding a laptop under one arm; fourth, a young man in a grey hooded sweatshirt raising one hand in a small wave; fifth, at the far right, DUARTE, standing a wider step apart from the others, his edges very slightly sharper and brighter than the rest, as if he had been added to the photo afterwards. Exactly five people and no more. Nothing else lies on the desk.
```

**Confirmar:** contem as pessoas: exatamente cinco, pela ordem mochila, Leonor, portátil, mão levantada, Duarte. O Duarte está na ponta direita, um pouco afastado.

### 4.11 `original_photo.jpg` — fotografia original, quatro pessoas (quadrada, 1:1)

A forma mais segura é partir da `cover`, como diz a secção 5. Este prompt serve se a ferramenta não conseguir editar.

Colar antes: **LEONOR**.

```text
Square image, 1:1 aspect ratio. This is an item icon, not a scene: one single printed photograph with a thin white border, centred with a very slight tilt on a plain, empty, very dark navy background, filling most of the frame, with no hands, furniture or other objects. Inside the photograph, exactly four students stand in one straight row, smiling naturally in front of a large glass wall of the campus in daylight. From left to right: a tall young man with short brown hair and a backpack on one shoulder; LEONOR; a young woman with short curly black hair holding a laptop under one arm; a young man in a grey hooded sweatshirt raising one hand in a small wave. To the right of the fourth person there is only an empty stretch of the glass wall. Exactly four people and no more.
```

**Confirmar:** exatamente quatro pessoas, as mesmas da capa e pela mesma ordem. Não há casaco comprido.

### 4.12 `usb_stick.jpg` — pen (quadrada, 1:1)

```text
Square image, 1:1 aspect ratio. This is an item icon, not a scene: one single USB flash drive, centred on a plain, empty, very dark navy background, filling about two thirds of the frame, with no hands, cables or other objects. A product-style photograph in a three-quarter view from slightly above: a smooth amber-orange plastic body, a brushed silver metal connector and a small metal key ring at the other end. A soft warm rim light runs around its outline, with a faint shadow beneath it. The body is completely plain, with no brand, symbol or marking.
```

**Confirmar:** um só objeto, em fundo liso e escuro. A pen não tem marca, símbolo nem números.

## 5. Problemas comuns

**A personagem não ficou igual à anterior.** Carreguem a imagem de referência dessa personagem e usem a frase do passo 4 da secção 1. Se continuar diferente, peçam na mesma conversa: `Keep this image exactly the same, but make <NAME> look exactly like in the reference image.`

**O número de pessoas está errado** (capa e fotografia original). Contem sempre, incluindo reflexos no vidro. Pedidos de correção:

- Capa só com quatro pessoas: `Keep this image exactly the same, but add DUARTE at the far right of the row, a wider step apart from the others.`
- Pessoas a mais: `Keep this image exactly the same, but remove the extra person, so that exactly five remain, from left to right: backpack, LEONOR, laptop, raised hand, DUARTE.`

**A capa e a fotografia original têm de condizer.** Façam primeiro a capa. Quando tiver exatamente cinco pessoas, peçam na mesma conversa:

`Keep this photograph exactly the same, but remove DUARTE on the far right and fill the gap with the glass wall. Change nothing else.`

e depois:

`Now show only this same four-person photograph, complete with its thin white border, centred with a very slight tilt on a plain, empty, very dark navy background, as a square 1:1 image.`

**A ferramenta inventou texto.** Vejam as folhas, os ecrãs, as lombadas, as paredes, por cima das portas, as roupas e os cantos. Letras ilegíveis também contam. Peçam: `Remove all letters, numbers and logos and replace them with plain blank surfaces. Change nothing else.` Evitem as palavras "cover", "title" e "poster" nas vossas mensagens.

**Parece uma ilustração ou um render 3D.** Acrescentem: `Make it look like a real photograph taken with a camera: natural skin, real fabric and concrete, imperfect light.`

**Ficou demasiado escuro no jogo.** As imagens aparecem com uma moldura escura por cima (a vinheta do `style.css`). Se o ponto principal desaparecer, peçam: `Same image, but one stop brighter in the focal point.`

**O formato saiu errado.** Aceitem o formato mais largo que houver e recortem em cima e em baixo sem perder o ponto principal. Na `entrance_hall`, guardem a parte de baixo escura.

## 6. Guardar os ficheiros

- **Imagens largas** (exterior, átrio, cenas, finais e capa): recortar para 16:9 e redimensionar para **1280 × 720** píxeis.
- **Ícones** (pen e fotografia original): recortar em quadrado e redimensionar para **512 × 512** píxeis.
- Guardar em **JPG** com qualidade à volta de 80. Cada ficheiro abaixo de **300 KB**; se ficar maior, qualidade 70. A `entrance_hall` vai dentro da página, por isso convém mesmo que fique leve.
- Nomes exatamente como nos títulos da secção 4, na pasta `assets/` (ao lado de `app.py`). Substituir um ficheiro antigo com o mesmo nome é tudo o que é preciso: o código não muda.

Antes de aceitar, vejam a imagem no tamanho do jogo: cerca de 700 píxeis de largura nas cenas e cerca de 300 nas miniaturas do corredor. Se o ponto principal não se perceber nas miniaturas, gerem outra vez.
