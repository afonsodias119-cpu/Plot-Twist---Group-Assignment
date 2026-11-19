"""PROTOTYPE ONLY — builds the 3D page with the real texts from story.py, in both languages.

Run from the project folder:
    uv run python prototypes/campus-3d/page3d.py
It writes campus3d.html next to this file; open it in the browser (needs internet for Three.js).
campus3d.html is generated, so it is not in git (see .gitignore in this folder).
"""

import base64
import json
import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[2]  # the project folder, two levels up
sys.path.insert(0, str(PROJECT))
from story import STORIES, UI_TEXTS  # noqa: E402

HERE = Path(__file__).parent
SCENES = ["print_shop", "study_room", "library", "computer_lab", "auditorium"]

# Texts that only the prototype needs (in the real game they would go to story.py).
EXTRA = {
    "pt": {
        "case": "Caso #005",
        "stamp": "Confidencial",
        "case_label": "O caso",
        "evidence": "PROVA 01 · Fotografia do grupo",
        "mission_label": "A tua missão",
        "mission": "Descobre a verdade sobre o quinto nome antes de a apresentação começar.",
        "button": "Aceitar o caso →",
        "back": "← Língua",
        "skip": "Clica no texto para ler tudo",
        "help": "⬆️⬇️⬅️➡️ ou WASD para andar",
        "corridor": "Corredor",
        "outside_title": "Entrada do campus",
        "outside_text": "É noite. Ouve-se o mar a bater na praia, mesmo ao lado do campus. Quase todas as luzes estão apagadas, mas a porta de vidro da entrada ainda abre. Alguém ficou a trabalhar até tarde.",
    },
    "en": {
        "case": "Case #005",
        "stamp": "Confidential",
        "case_label": "The case",
        "evidence": "EVIDENCE 01 · Group photo",
        "mission_label": "Your mission",
        "mission": "Uncover the truth about the fifth name before the presentation begins.",
        "button": "Accept the case →",
        "back": "← Language",
        "skip": "Click the text to read it all",
        "help": "⬆️⬇️⬅️➡️ or WASD to move",
        "corridor": "Corridor",
        "outside_title": "Campus entrance",
        "outside_text": "It is night. You can hear the sea on the beach, right next to the campus. Almost every light is off, but the glass entrance door still opens. Someone stayed late.",
    },
}


def picture(name):
    path = PROJECT / "assets" / f"{name}.jpg"
    if not path.exists():
        return None
    return "data:image/jpeg;base64," + base64.b64encode(path.read_bytes()).decode()


def language_data(language):
    story, ui, extra = STORIES[language], UI_TEXTS[language], EXTRA[language]
    scenes = {s: {"title": story["scenes"][s]["title"], "text": story["scenes"][s]["texts"][0]["text"]} for s in SCENES}
    scenes["outside"] = {"title": extra["outside_title"], "text": extra["outside_text"]}
    return {
        "scenes": scenes,
        "intro": dict(extra, title=ui["title"], premise=ui["premise"]),
        "ui": {"help": extra["help"], "corridor": extra["corridor"]},
    }


def build_page():
    images = {s: picture(s) for s in SCENES}
    images["outside"] = images["cover"] = picture("cover")
    data = {"pt": language_data("pt"), "en": language_data("en"), "images": images}
    return (HERE / "game3d.html").read_text().replace("__DATA__", json.dumps(data))


if __name__ == "__main__":
    out = HERE / "campus3d.html"
    out.write_text(build_page())
    print(out)
