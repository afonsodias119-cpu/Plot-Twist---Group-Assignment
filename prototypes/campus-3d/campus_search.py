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
         "sticky_notes", "pen", "highlighter", "headphones", "keys", "calculator", "usb_stick")

# Where the USB stick is: it is one of the objects of the table.
PEN_SPOT = "usb_stick"

# The password of computer 12: the day and month the cover photo was taken (14 November).
PC12_CODE = "1411"

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
        },
    },
}

# The torn photo of the print shop (specs/torn-photo.md). photo.js draws the 9 pieces; only here is it
# written which piece goes in each place of the frame (reading order: top row left to right, then the
# middle row, then the bottom row), all upright.
PHOTO_PIECES = ("k", "d", "q", "a", "n", "f", "w", "h", "s")
PHOTO_SOLUTION = ("q", "w", "a", "f", "k", "s", "d", "n", "h")

PHOTO_TEXT = {
    "en": "The last piece fits. In the original photo there are four of you, and in the corner the date stamp says 14.11. The clerk tapes the pieces together and hands you the photo.",
    "pt": "O último pedaço encaixa. Na fotografia original estão quatro pessoas, e no canto o carimbo da data diz 14.11. A funcionária cola os pedaços com fita-cola e dá-te a fotografia.",
}
