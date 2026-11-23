"""Two answers on every line of Tomás (a right one and a wrong one), people give in through the right
answer of their claim line, and no "Show evidence" in conversations (specs/two-answers.md)."""
import importlib
import itertools
import sys
from pathlib import Path

import logic

FOLDER = Path(__file__).resolve().parents[1] / "prototypes" / "campus-3d"
sys.path.insert(0, str(FOLDER))
campus = importlib.import_module("campus_game")
people = importlib.import_module("campus_people")
PLAY = (FOLDER / "play.js").read_text(encoding="utf-8")
PLAYER = "two answers"


def call(operation="open", language="en", **extra):
    return campus.command(dict(operation=operation, language=language, player=PLAYER, **extra))


def shown(options):
    """The answers the page shows: not the goodbyes (the header ends a talk) and not a memory answer."""
    return [o for o in options if o["next"] is not None and "night" not in o]


def states():
    """Every mix of the things that open the answers: the photo held, the files seen."""
    for photo, files in itertools.product((False, True), repeat=2):
        yield {"inventory": ["original_photo"] if photo else [], "flags": {"files_viewed": files}}


def test_every_line_of_tomas_and_rita_offers_at_most_two_answers_whatever_is_held():
    for language in ("en", "pt"):
        for person in ("tomas", "rita"):
            for node, line in people.PEOPLE[language][person]["nodes"].items():
                for state in states():
                    open_now = [o for o in shown(line["options"]) if logic._condition_met(o.get("if", {}), state)]
                    assert len(open_now) <= 2, (language, person, node, state)


def test_rita_goes_from_the_usb_stick_to_the_photo_to_her_claim():
    for language in ("en", "pt"):
        nodes = people.PEOPLE[language]["rita"]["nodes"]
        right = lambda node: [o["next"] for o in shown(nodes[node]["options"])][0]
        assert (right("start"), right("pen"), right("photo")) == ("pen", "photo", "five"), language
        for node in ("start", "pen", "photo", "counted", "duarte", "warned", "sorry"):
            assert shown(nodes[node]["options"])[-1]["next"] == "upset", (language, node)
        assert [o["next"] for o in nodes["upset"]["options"]] == ["sorry", "closed"]
        assert not any("cost" in o for line in nodes.values() for o in line["options"])   # Rita has no rude answer


def test_the_order_is_kind_then_who_then_password():
    for language in ("en", "pt"):
        nodes = people.PEOPLE[language]["tomas"]["nodes"]
        right = lambda node: [o["next"] for o in shown(nodes[node]["options"])][0]
        assert (right("start"), right("kind"), right("who")) == ("kind", "who", "password"), language
        # Each wrong answer leads to his offended line, where an apology brings the questions back.
        for node in ("start", "kind", "who", "password", "photo"):
            assert shown(nodes[node]["options"])[-1]["next"] == "hard", (language, node)
        assert [o["next"] for o in nodes["calm"]["options"]][0] == "kind"


def test_the_right_answer_on_a_claim_line_names_the_card_that_breaks_it():
    case = importlib.import_module("campus_case")
    for language in ("en", "pt"):
        for person, claim in case.CONFRONT.items():
            cracks = [o for o in people.PEOPLE[language][person]["nodes"][claim["node"]]["options"] if "crack" in o]
            assert cracks and all(o["crack"] in claim["breaks"] for o in cracks), (language, person)
            assert people.offered(cracks[0])["crack"] == cracks[0]["crack"]


def test_tomas_gives_in_through_the_right_answer():
    call()
    for action in ("open_drawer", "go_computer_lab", "view_files"):
        call("play", action=action)
    slides = call("talk", npc="tomas", node="slides")
    right = next(o for o in slides["options"] if o.get("crack"))
    reply = call("confront", npc="tomas", node="slides", evidence=right["crack"])   # what the page sends
    assert reply["confront"]["cracked"] is True


def test_show_evidence_is_gone_only_in_the_print_shop_and_the_computer_lab():
    assert 'const NO_EVIDENCE = ["amelia", "tomas", "computer12"];' in PLAY
    assert "const showsEvidence = !NO_EVIDENCE.includes(line.npc)" in PLAY
    assert 'if (line.npc === "guard") { guardShown(card); return; }' in PLAY   # the guard is not touched
    assert "if (option.crack) {" in PLAY and "confrontWith(line, { id: option.crack, label: option.label }, true)" in PLAY
    assert 'const TWO_ANSWERS = new Set(["tomas", "rita"]);' in PLAY
