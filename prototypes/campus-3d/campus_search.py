"""The answers of the two puzzles of the 3D game (specs/pen-and-code.md). Data only.

SERVER ONLY: this file is read by campus_game.py and is never put in the page (page3d.py does not
import it), so looking at the page cannot give the answers away. The labels of the spots, which the
page needs to draw the buttons, are in campus_text.py ("spots").

To change a puzzle, change it here (and, for the code, the hints of Tomás and the clerk in
campus_people.py, so the player can still work it out).
"""

# The places of the study room the player can search, in the order the text mode lists them.
SPOTS = ("drawer", "coat", "mug", "backpack", "books", "papers", "bin", "plant", "pizza")

# Where the USB stick is.
PEN_SPOT = "pizza"

# The password of computer 12: the day and month the cover photo was taken (14 November).
PC12_CODE = "1411"

# What the player finds in each spot. "nothing" is for the wrong spots; "found" is for PEN_SPOT.
SEARCH_TEXT = {
    "en": {
        "found": "Under the last cold slice of pizza lies the group's USB stick, with the project backups. You take the USB stick.",
        "nothing": {
            "drawer": "The group drawer is empty. Someone took the USB stick out of here.",
            "coat": "Just a forgotten coat. The pockets are empty.",
            "mug": "Cold coffee. Nothing inside.",
            "backpack": "Notebooks and a phone charger. No USB stick.",
            "books": "Finance books, full of underlined pages.",
            "papers": "Drafts of the report. Nothing hidden between them.",
            "bin": "Crumpled paper and an empty can.",
            "plant": "Only soil and a few dry leaves.",
        },
    },
    "pt": {
        "found": "Debaixo da última fatia de pizza fria está a pen do grupo, com as cópias de segurança do projeto. Guardas a pen.",
        "nothing": {
            "drawer": "A gaveta do grupo está vazia. Alguém tirou a pen daqui.",
            "coat": "Só um casaco esquecido. Os bolsos estão vazios.",
            "mug": "Café frio. Nada lá dentro.",
            "backpack": "Cadernos e um carregador de telemóvel. Nada de pen.",
            "books": "Livros de finanças, cheios de páginas sublinhadas.",
            "papers": "Rascunhos do relatório. Nada escondido entre eles.",
            "bin": "Papéis amarrotados e uma lata vazia.",
            "plant": "Só terra e algumas folhas secas.",
        },
    },
}
