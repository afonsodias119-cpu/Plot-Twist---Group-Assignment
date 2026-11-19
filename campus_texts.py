"""Plot Twist — the extra texts of the campus visuals preview (data only).

Used only by app_campus.py (see specs/campus-visuals.md). In phase 2 of that spec these
texts move into story.py. Both languages have exactly the same keys.

- TEASERS: one short line per scene, shown on its door card in the hallway. A teaser must
  stay true for the whole game, so it never mentions people who may have left.
- CAMPUS_UI: the new screen texts.
"""

TEASERS = {
    "en": {
        "study_room": "Where it all began: your group's table.",
        "print_shop": "About to close. The clerk remembers every order.",
        "library": "Silent rows of books, one lamp still on at the back.",
        "computer_lab": "Empty, except for one screen still glowing.",
        "auditorium": "The professor is closing tomorrow's list.",
    },
    "pt": {
        "study_room": "Onde tudo começou: a mesa do teu grupo.",
        "print_shop": "Está quase a fechar. A funcionária lembra-se de todos os pedidos.",
        "library": "Filas de livros em silêncio e um candeeiro aceso ao fundo.",
        "computer_lab": "Vazia, a não ser um ecrã ainda aceso.",
        "auditorium": "O professor está a fechar a lista de amanhã.",
    },
}

CAMPUS_UI = {
    "en": {
        "hallway": "The hallway",
        "entering": "You push the glass door. Behind you, the sound of the sea. Ahead, the hall is silent.",
    },
    "pt": {
        "hallway": "O corredor",
        "entering": "Empurras a porta de vidro. Atrás de ti, o som do mar. À frente, o átrio está em silêncio.",
    },
}
