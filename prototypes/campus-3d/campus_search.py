"""The answers of the two puzzles of the 3D game (specs/pen-and-code.md). Data only.

SERVER ONLY: this file is read by campus_game.py and is never put in the page (page3d.py does not
import it), so looking at the page cannot give the answers away. The labels of the objects, which the
page shows next to ✗ after a wrong click, are in campus_text.py ("spots"); table.js draws them.

To change a puzzle, change it here (and, for the code, the hints of Tomás and the clerk in
campus_people.py, so the player can still work it out).
"""

# The kinds of objects on the table of the study room (specs/hidden-object-table.md). Every one can be
# clicked in the close-up of the table; table.js draws them.
SPOTS = ("papers", "notebook", "pizza_box", "pizza_slice", "napkin", "can", "mug", "crisps", "cable",
         "sticky_notes", "pen", "highlighter", "headphones", "keys", "calculator",
         # student life on the table (specs/more-to-find.md, point 1): like every object, a wrong one costs 1 minute
         "student_card", "timetable", "receipt",
         "usb_stick")

# Where the USB stick is: it is one of the objects of the table.
PEN_SPOT = "usb_stick"

# The password of computer 12: the day and month the cover photo was taken (Saturday 17 October,
# specs/calendar-code.md).
PC12_CODE = "1710"

# What the player finds in each spot. "nothing" is for the wrong spots; "found" is for PEN_SPOT.
SEARCH_TEXT = {
    "en": {
        "found": "There, half under a greasy napkin, between pizza crusts: the group's USB stick, with the project backups. You take the USB stick.",
        "nothing": {
            "papers": "Drafts of the report, full of crossed-out lines.",
            "notebook": "Someone's notebook. Lecture notes and doodles.",
            "pizza_box": "An empty pizza box with grease at the bottom.",
            "pizza_slice": "A cold slice of pizza, already hard.",
            "napkin": "A crumpled napkin stained with tomato sauce.",
            "can": "An empty can of soda.",
            "mug": "Cold coffee. Nothing inside.",
            "crisps": "An empty bag of crisps. Only crumbs.",
            "cable": "A tangled phone charger cable.",
            "sticky_notes": "Sticky notes with ideas for the slides.",
            "pen": "A pen without its cap.",
            "highlighter": "A yellow highlighter, almost dry.",
            "headphones": "Someone's headphones, still warm.",
            "keys": "A set of keys on a university key ring.",
            "calculator": "A finance calculator. The screen says 0.",
            "student_card": "Someone's student card. The photo is from first year, and nobody would recognise the face now.",
            "timetable": "The exam timetable. Corporate Finance is circled three times in red, with a small skull next to it.",
            "receipt": "Last night's pizza receipt: four margheritas, the bill split four ways.",
        },
    },
    "pt": {
        "found": "Ali, meio tapada por um guardanapo engordurado, entre côdeas de pizza: a pen do grupo, com as cópias de segurança do projeto. Guardas a pen.",
        "nothing": {
            "papers": "Rascunhos do relatório, cheios de riscos.",
            "notebook": "O caderno de alguém. Apontamentos das aulas e rabiscos.",
            "pizza_box": "Uma caixa de pizza vazia, com gordura no fundo.",
            "pizza_slice": "Uma fatia de pizza fria, já dura.",
            "napkin": "Um guardanapo amarrotado, sujo de molho de tomate.",
            "can": "Uma lata de refrigerante vazia.",
            "mug": "Café frio. Nada lá dentro.",
            "crisps": "Um pacote de batatas fritas vazio. Só migalhas.",
            "cable": "Um cabo de carregador todo enrolado.",
            "sticky_notes": "Post-its com ideias para os slides.",
            "pen": "Uma caneta sem tampa.",
            "highlighter": "Um marcador amarelo, quase seco.",
            "headphones": "Os auscultadores de alguém, ainda quentes.",
            "keys": "Um molho de chaves com um porta-chaves da universidade.",
            "calculator": "Uma calculadora financeira. O ecrã diz 0.",
            "student_card": "O cartão de estudante de alguém. A fotografia é do primeiro ano, e hoje ninguém reconheceria aquela cara.",
            "timetable": "O calendário de exames. Finanças Empresariais está rodeado três vezes a vermelho, com uma caveira pequenina ao lado.",
            "receipt": "O talão da pizza de ontem à noite: quatro pizzas margherita, a conta dividida por quatro.",
        },
    },
}

# ---------- things to look at in the other rooms (specs/more-to-find.md, points 2 to 4) ----------
# Server only, like the rest of this file: the page gets only the id and the name of the things of the
# saved room (`finds` in the snapshot), and a text only when the player looks.
FINDS = {"print_shop": ("price_list", "order_book"), "library": ("noticeboard", "returns_trolley"),
         "computer_lab": ("lab_whiteboard", "computer7"), "auditorium": ("podium",)}
# The campus minutes a look costs. Only the order book: the red herring that wastes time on purpose.
# (campus_clock.COSTS is not used: its keys are pinned by a reviewed test.)
FIND_MINUTES = {"order_book": 2}
# When the two red herrings read differently (checked with logic._condition_met, like the cards):
# the order book once the original photo is held (and then it costs nothing), computer 7 once the files are viewed.
FIND_LATER = {"order_book": {"has": ["original_photo"]}, "computer7": {"flags": {"files_viewed": True}}}

# The texts (design-notes/texts-ideas.md, part E2). The red herrings name no person, no date of the
# photo and no code that works, so they fit every case and every group.
FIND_TEXT = {
    "en": {
        "price_list": {"name": "Price list", "text": "A laminated price list. Black and white, 5 cents. Colour, 25 cents. Thesis binding: ask nicely. Thesis binding after midnight: ask even more nicely."},
        "order_book": {"name": "Order book",
                       "text": "You leaf back through a year of orders until you find your group's: cover photo, 5 prints. Five.",
                       "later": "Your group's order again: cover photo, 5 prints. In the margin, in the clerk's handwriting: one for each of you and one for the professor's file. Five prints, not five people."},
        "noticeboard": {"name": "Noticeboard", "text": "The library noticeboard. Silence, please. Lost: a grey umbrella. Lost: the will to live, last seen in week 7 of Corporate Finance."},
        "returns_trolley": {"name": "Returns trolley", "text": "A trolley of returned books. On top, 'Excel for People Who Hate Excel', with a sticky note inside the cover: it did not help."},
        "lab_whiteboard": {"name": "Whiteboard", "text": "A perfect supply and demand graph, drawn with care. Underneath, in smaller letters: help."},
        "computer7": {"name": "Computer 7",
                      "text": "Computer 7 is locked too. A sticky note on its screen: pw 2311, presentation day!!",
                      "later": "The sticky note on computer 7 again: 2311, the day of the presentation. Someone's own computer, someone's own password. It has nothing to do with computer 12."},
        "podium": {"name": "Podium", "text": "A note taped to the podium: maximum 10 minutes per group. No exceptions. Yes, you."},
    },
    "pt": {
        "price_list": {"name": "Tabela de preços", "text": "Uma tabela de preços plastificada. Preto e branco, 5 cêntimos. Cores, 25 cêntimos. Encadernação de tese: pedir com jeitinho. Encadernação de tese depois da meia-noite: pedir com ainda mais jeitinho."},
        "order_book": {"name": "Livro de pedidos",
                       "text": "Folheias um ano inteiro de pedidos até encontrares o do vosso grupo: fotografia da capa, 5 impressões. Cinco.",
                       "later": "Outra vez o pedido do vosso grupo: fotografia da capa, 5 impressões. Na margem, com a letra da funcionária: uma para cada um e uma para o processo do professor. Cinco impressões, não cinco pessoas."},
        "noticeboard": {"name": "Quadro de avisos", "text": "O quadro de avisos da biblioteca. Silêncio, por favor. Perdido: um guarda-chuva cinzento. Perdida: a vontade de viver, vista pela última vez na semana 7 de Finanças Empresariais."},
        "returns_trolley": {"name": "Carrinho das devoluções", "text": "Um carrinho de livros devolvidos. Em cima, 'Excel para Quem Odeia Excel', com um post-it dentro da capa: não ajudou."},
        "lab_whiteboard": {"name": "Quadro branco", "text": "Um gráfico de oferta e procura perfeito, desenhado com cuidado. Por baixo, em letra mais pequena: socorro."},
        "computer7": {"name": "Computador 7",
                      "text": "O computador 7 também está bloqueado. Um post-it no ecrã: pw 2311, dia da apresentação!!",
                      "later": "Outra vez o post-it do computador 7: 2311, o dia da apresentação. O computador de alguém, a password de alguém. Não tem nada a ver com o computador 12."},
        "podium": {"name": "Púlpito", "text": "Um papel colado no púlpito: máximo de 10 minutos por grupo. Sem exceções. Sim, tu."},
    },
}

# The torn photo of the print shop (specs/torn-photo.md). photo.js draws the 9 pieces; only here is it
# written which piece goes in each place of the frame (reading order: top row left to right, then the
# middle row, then the bottom row), all upright.
PHOTO_PIECES = ("k", "d", "q", "a", "n", "f", "w", "h", "s")
PHOTO_SOLUTION = ("q", "w", "a", "f", "k", "s", "d", "n", "h")

PHOTO_TEXT = {
    "en": "The last piece fits. In the original photo there are four of you, and in the corner the date stamp says 17.10. The clerk tapes the pieces together and hands you the photo.",
    "pt": "O último pedaço encaixa. Na fotografia original estão quatro pessoas, e no canto o carimbo da data diz 17.10. A funcionária cola os pedaços com fita-cola e dá-te a fotografia.",
}
