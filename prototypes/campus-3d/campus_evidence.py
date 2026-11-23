"""Evidence cards, confrontations and the hearing of the 3D game (specs/evidence-and-hearing.md).

The rules only: the data (which card breaks which claim, and every line) is in campus_case.py, and
both files are read by the server only. campus_game.py calls these functions.

What the player holds comes from two places:
- the saved game (db.py, table `games`): the item and the flags of the story;
- the night's notes (db.py, table `nights`): who was cracked tonight, the answers of the hearing,
  the campus minute, the rounds at which the player was caught (specs/night-schedule.md),
  whether tonight's row of `runs` is already written (`run`, specs/earlier-nights.md, point 2),
  how many rude answers each person got (`rude`, specs/trust-has-consequences.md, point 3) and
  which case is played tonight (`case`, specs/case-of-the-day.md, point 4).
The notes are read through read_night, which keeps only what it understands, so a damaged row can
neither raise an error nor help the player.

The case of the night (specs/culprit-of-the-night.md) is played with the story's own actions: the
functions of that section only renumber the chat and tell the texts of the case on the way out.
"""

from datetime import date

import db
import game
import logic
from campus_case import CASE_TEXT, CONFRONT, EVIDENCE, FACTS, HEARING
# The cases of the day (specs/case-of-the-day.md and specs/culprit-of-the-night.md): server only.
from campus_case import CASES
# The cost of a card is in the night's cost table (specs/night-schedule.md, point 2): the server adds
# it to the campus minute.
from campus_clock import COSTS, NIGHT_MINUTES, ROUNDS
# What the server remembers of earlier nights (specs/earlier-nights.md): the gate of the true ending
# and the row of tonight's ending.
from campus_memory import TRUE_ENDING, record, seen_all, true_ending
from campus_people import OBJECTS, PEOPLE, TEMPERS, talk
from campus_text import TEXT
from story import STORIES

# The ten cards, in the order the hand shows them (point 4): the ones the save gives, then the facts.
CARDS = list(EVIDENCE) + list(FACTS.values())
FINAL_ROOM = "auditorium"
# The doubts are never counted above three (point 10).
MAX_DOUBTS = 3
# The classic case: the one played by a game with no `case` note (specs/case-of-the-day.md, point 4).
CLASSIC = "outsider"


# ---------- the night's notes ----------

def valid_hearing(answers, state):
    """True when `answers` can be the saved answers of the hearing of this game (point 2).

    A list of at most three answers, each "concede" or a card id. Before the ending it counts only in
    the auditorium, and with fewer than three answers (the third answer ends the game); after the
    ending it must have all three.
    """
    if not isinstance(answers, list) or len(answers) > len(HEARING):
        return False
    if not all(isinstance(answer, str) and (answer == "concede" or answer in CARDS) for answer in answers):
        return False
    if state["ending"] != "none":
        return len(answers) == len(HEARING)
    return state["scene"] == FINAL_ROOM and len(answers) < len(HEARING)


def clean_minute(saved):
    """The campus minute of a saved night (specs/night-schedule.md, point 1).

    The column holds the whole minutes (db.load_night already turns anything that is not an int into
    0); it is brought back inside 0 to 30. The note `half` adds half a minute only when it is exactly
    true and the night is not over.
    """
    whole = min(max(saved["minute"], 0), NIGHT_MINUTES)
    if saved["notes"].get("half") is True and whole < NIGHT_MINUTES:
        return whole + 0.5
    return whole


def clean_rude(saved):
    """The note `rude`, cleaned (specs/trust-has-consequences.md, point 3): a dict whose keys are
    Leonor, Tomás or Duarte and whose values are the ints 1 or 2. Anything else is dropped, so a
    damaged note counts as calm. `type(...) is int`: True and 1.0 are not a count."""
    if not isinstance(saved, dict):
        return {}
    return {person: saved[person] for person in TEMPERS
            if type(saved.get(person)) is int and saved[person] in (1, 2)}


def clean_case(saved):
    """The note `case`, cleaned (specs/case-of-the-day.md, point 4): a dict with exactly `variant` (a
    case of CASES) and `date` ("" or a date written as 2026-11-22). Anything else is None, the
    classic case, so a damaged note can neither raise an error nor change the case."""
    if not isinstance(saved, dict) or set(saved) != {"variant", "date"}:
        return None
    variant, day = saved["variant"], saved["date"]
    if not isinstance(variant, str) or variant not in CASES or not isinstance(day, str):
        return None
    if day:
        try:
            date.fromisoformat(day)
        except ValueError:
            return None
    return {"variant": variant, "date": day}


def case_of(night):
    """The case played tonight, as its data in CASES. A game with no `case` note (opened with `open`,
    or a damaged note) plays the classic case."""
    case = night.get("case")
    return CASES[case["variant"] if case else CLASSIC]


def read_night(player, state):
    """The night's notes of this player, cleaned: {"minute", "cracked", "hearing", "verdict", "caught", "run", "rude", "case"}.

    `cracked` keeps only people who have a confrontation; `hearing` is None when no hearing was
    started (or the saved one does not fit this game); `verdict` is kept only when the game has ended
    and the hearing could have produced it; `minute` is a whole number or a half from 0 to 30;
    `caught` keeps only the rounds of the schedule (specs/night-schedule.md, point 8); `run` is
    True only when the note is exactly true (specs/earlier-nights.md, point 2); `rude` is cleaned by
    clean_rude; `case` by clean_case (None: the classic case). Cleaning happens in memory: nothing is
    written here.
    """
    saved = db.load_night(player)
    notes = saved["notes"]
    cracked = notes.get("cracked")
    cracked = [person for person in CONFRONT if isinstance(cracked, list) and person in cracked]
    caught = notes.get("caught")
    caught = [mark for mark in ROUNDS if isinstance(caught, list) and mark in caught]
    answers = notes.get("hearing")
    night = {"minute": clean_minute(saved), "cracked": cracked,
             "hearing": answers if valid_hearing(answers, state) else None, "verdict": "", "caught": caught,
             "run": notes.get("run") is True, "rude": clean_rude(notes.get("rude")),
             "case": clean_case(notes.get("case"))}
    # The saved verdict is only a record of what was shown (point 10): the screen always works the
    # ending out again from the answers (shown_ending), so editing this note by hand changes nothing.
    if night["hearing"] is not None and state["ending"] != "none":
        shown, _line = verdict_of(state, night["hearing"], bool(caught), claims_of(night))
        if notes.get("verdict") == shown:
            night["verdict"] = shown
        # The true ending is believed only when tonight's game agrees with it (specs/earlier-nights.md, point 8).
        if notes.get("verdict") == TRUE_ENDING and perfect_night(state, night):
            night["verdict"] = TRUE_ENDING
    return night


def write_night(player, night):
    """Save the night's notes. A hearing that was never started is left out.

    The column `minute` is an INTEGER, so it gets the whole minutes and the half is the note `half`
    (specs/night-schedule.md, point 1).
    """
    minute = night["minute"]
    notes = {"cracked": night["cracked"], "verdict": night["verdict"], "caught": night["caught"],
             "half": minute != int(minute), "run": night["run"]}
    if night["hearing"] is not None:
        notes["hearing"] = night["hearing"]
    if night.get("rude"):   # only when someone got a rude answer (specs/trust-has-consequences.md, point 3)
        notes["rude"] = night["rude"]
    if night.get("case"):   # only a game begun with `begin` has one (specs/case-of-the-day.md, point 4)
        notes["case"] = night["case"]
    db.save_night(player, int(minute), notes)


# ---------- the case of the night (specs/culprit-of-the-night.md) ----------
# The story is always played with its own messages 1 to 5 (2, 4 and 5 are the fake ones). A case only
# shows them in another order and tells some texts differently, on the way out. The page only ever
# sees shown numbers: these functions turn one kind of number into the other (point 3).

# The cards of the flagged chat messages.
MESSAGE_CARDS = [f"msg_{n}" for n in range(1, 6)]


def story_number(shown, night):
    """The story's message number of the message shown at place `shown` tonight."""
    return case_of(night)["order"][shown - 1]


def shown_number(message, night):
    """The place where the story's message `message` is shown tonight."""
    return case_of(night)["order"].index(message) + 1


def story_card(card, night):
    """A card the page sent (msg_<shown>) as the story's card (msg_<message>). Other cards, and
    anything that is not a card, come back as they are: the usual checks refuse them later."""
    if card not in MESSAGE_CARDS:
        return card
    return f"msg_{story_number(int(card[len('msg_'):]), night)}"


def shown_card(card, night):
    """A story's card as the page sees it: msg_<message> becomes msg_<shown>."""
    if card not in MESSAGE_CARDS:
        return card
    return f"msg_{shown_number(int(card[len('msg_'):]), night)}"


def claims_of(night):
    """Duarte's three claims tonight (point 5): HEARING itself in the classic case; in the other
    cases a claim also accepts the cards of the case's `accepts` (a confession of the teammate who
    added the name breaks "my name has been there since the first draft")."""
    accepts = case_of(night)["accepts"]
    if not accepts:
        return HEARING
    return [dict(claim, accepts=claim["accepts"] + accepts.get(claim["id"], [])) for claim in HEARING]


def swapped(value, texts, keys):
    """`value` with every key of `texts` replaced by its case text, in every string inside it.
    Dict keys (the ids) are never changed. `keys` are tried longest first, each once: no case text
    contains another key, so a text put in is never changed again."""
    if isinstance(value, str):
        for key in keys:
            if key in value:
                value = value.replace(key, texts[key])
        return value
    if isinstance(value, dict):
        return {name: swapped(inner, texts, keys) for name, inner in value.items()}
    if isinstance(value, list):
        return [swapped(inner, texts, keys) for inner in value]
    return value


def retell(reply, night, language):
    """A reply as tonight's case tells it (point 6): each classic text the case changes is replaced
    by the case's own. A case text reaches the page exactly when its classic text would have, so
    the secrets stay on the server. The classic case changes nothing. Reading writes nothing."""
    texts = case_of(night)["texts"][language]
    if not texts:
        return reply
    return swapped(reply, texts, sorted(texts, key=len, reverse=True))


# ---------- trust (specs/trust-has-consequences.md) ----------

def remember_rude(player, night, person):
    """A rude answer to `person`: one more in the note `rude`, never above 2 (point 2). Returns the
    night as it is now saved."""
    rude = dict(night["rude"])
    rude[person] = min(rude.get(person, 0) + 1, 2)
    night = dict(night, rude=rude)
    write_night(player, night)
    return night


def moods(night):
    """The temper of Leonor, Tomás and Duarte tonight (point 1): "calm" with no rude answer, "wary"
    with one, "hostile" with two. A person cracked tonight is calm whatever was said: the proof showed
    the player was right. Server only: the temper is never sent to the page."""
    names = ("calm", "wary", "hostile")
    return {person: "calm" if person in night["cracked"] else names[night["rude"].get(person, 0)]
            for person in TEMPERS}


# ---------- the cards ----------

def held(state, night):
    """The ids of the cards the player holds now, in the order of CARDS."""
    cards = [card for card, condition in EVIDENCE.items() if logic._condition_met(condition, state)]
    return cards + [fact for person, fact in FACTS.items() if person in night["cracked"]]


def chat_message(language, n):
    """The story's own text of chat message n (the first text of the chat is its introduction)."""
    texts = STORIES[language]["scenes"]["group_chat"]["texts"]
    return [entry["text"] for entry in texts if entry["when"] == {}][n]


def card_label(card, language):
    """What a card says. A flagged chat message is shown with the story's own text, not a copy."""
    if card.startswith("msg_"):
        return "🚩 " + chat_message(language, int(card[len("msg_"):]))
    return CASE_TEXT[language]["labels"][card]


def hand(state, night, language):
    """The cards for the snapshot: [{"id", "label"}], only the ones held now. A flagged message is
    msg_<shown> and the messages are listed in the order they are shown (specs/culprit-of-the-night.md,
    point 3): CARDS has msg_1 to msg_5 in order, so filtering it keeps that order."""
    shown = [shown_card(card, night) for card in held(state, night)]
    return [{"id": card, "label": card_label(story_card(card, night), language)} for card in CARDS if card in shown]


# ---------- confronting ----------

def hearing_open(state, night):
    """True from the start of the hearing until the ending (point 12)."""
    return night["hearing"] is not None and state["ending"] == "none"


def refuse_during_hearing(state, night, language):
    """`talk` and `confront` raise during the hearing: the player cannot walk out of their own case."""
    if hearing_open(state, night):
        raise ValueError(TEXT[language]["hearing_locked"])


def is_broken(night, person, node):
    """True when `node` is the claim line of a person who was already cracked tonight."""
    return person in night["cracked"] and CONFRONT[person]["node"] == node


def without_broken_claims(reply, night):
    """A `talk` reply with the answers that lead to a broken claim taken out (point 7).

    A broken claim line cannot be asked for any more, so asking for it raises, like any line `talk`
    would not give now.
    """
    if is_broken(night, reply["npc"], reply["node"]):
        raise ValueError("Unknown answer / Resposta desconhecida.")
    options = [option for option in reply["options"] if not is_broken(night, reply["npc"], option["next"])]
    return dict(reply, options=options)


def confront(player, state, night, language, person, node, card, gone=(), number=1):
    """The player shows `card` to `person` on the line `node` (point 6).

    The right card on the claim line cracks the person: they are added to `cracked` (the only
    write here) and their fact, if they have one, is a card from now on. Anything else writes nothing
    here. `minutes` is what the card costs (specs/night-schedule.md, point 2): campus_game.py adds it
    to the campus minute. `gone` are the people who have left by the schedule; `number` is which
    night of this name tonight is (campus_memory.night_number), so a memory answer counts as in `talk`.
    The reply never says which card would have been right.
    """
    refuse_during_hearing(state, night, language)
    if not isinstance(card, str) or card not in CARDS:
        raise ValueError("Unknown evidence / Prova desconhecida.")
    talk(state, language, person, node, gone, number)   # the same checks as a conversation: the person is here, the line can be reached
    if person in OBJECTS:
        raise ValueError("Unknown person / Pessoa desconhecida.")
    if is_broken(night, person, node):
        raise ValueError("Unknown answer / Resposta desconhecida.")
    if card not in held(state, night):
        raise ValueError("You do not have that / Não tens isso.")

    text = CASE_TEXT[language]
    reply = {"npc": person, "name": PEOPLE[language][person]["name"], "cracked": False,
             "text": text["rebuffs"][person], "trust": None, "note": "", "minutes": COSTS["card_wrong"]}
    if person == "duarte":   # one line for any card, on any of his lines
        return dict(reply, minutes=COSTS["card_duarte"])
    claim = CONFRONT.get(person)
    if claim and node == claim["node"] and card in claim["breaks"]:
        write_night(player, dict(night, cracked=night["cracked"] + [person]))
        reveal = text["reveals"][person]
        return dict(reply, cracked=True, text=reveal["text"], trust=reveal["trust"], note=reveal["note"],
                    minutes=COSTS["card_right"])
    return reply


# ---------- the hearing ----------

def doubts(answers, caught=False, claims=HEARING):
    """How many answers did not break their claim. "concede" is always a doubt.

    A player who was caught at computer 12 tonight has one more doubt, however many times it happened
    (specs/night-schedule.md, point 8). Never more than three. `claims` are tonight's (claims_of).
    """
    count = sum(1 for claim, answer in zip(claims, answers) if answer not in claim["accepts"])
    return min(count + (1 if caught else 0), MAX_DOUBTS)


def verdict_of(state, answers, caught=False, claims=HEARING):
    """The ending shown after the hearing and the key of the professor's verdict line ("" for none).

    The story decides the best the player earned (state["ending"]); the hearing can only lose it
    (point 10 and design-notes, B6). `caught`: the player was caught at a round tonight.
    """
    story_ending = state["ending"]
    count = doubts(answers, caught, claims)
    if count >= MAX_DOUBTS:
        return "stolen_credits", "three_help" if state["flags"]["colleague_choice"] == "help" else "three"
    if count == 2 and story_ending == "full_case":
        return "impostor", "two"
    if story_ending == "stolen_credits" and answers[-1] == "tomas_word":
        # Not a cap: it only keeps the hearing and the text of "Stolen credit" from contradicting each other.
        return story_ending, "no_originals"
    return story_ending, ""


def perfect_night(state, night):
    """True when tonight could give the true ending (specs/earlier-nights.md, point 8): the story's
    `full_case`, a hearing of three answers with no doubt (a catch is a doubt) and the words of
    Tomás and Rita both won tonight. The four endings of earlier nights are checked by the caller."""
    answers = night["hearing"]
    return (state["ending"] == "full_case" and answers is not None and len(answers) == len(HEARING)
            and doubts(answers, bool(night["caught"]), claims_of(night)) == 0
            and all(person in night["cracked"] for person in FACTS))


def hearing(player, state, night, language, answer):
    """One answer of the hearing (point 10). Returns (accepted, message, heard).

    Each accepted answer is saved in the notes at once, so closing the card or reloading cannot
    take a doubt back. After the third answer the story's own present_evidence is played, the
    night ends and its row is written with the ending shown (specs/earlier-nights.md, point 2).
    """
    if not isinstance(answer, str) or not (answer in ("start", "concede") or answer in CARDS):
        raise ValueError("Invalid answer / Resposta inválida.")
    if answer in CARDS and answer not in held(state, night):
        raise ValueError("You do not have that / Não tens isso.")
    messages = STORIES[language]["messages"]
    if state["ending"] != "none":
        return False, messages["game_over"], False
    if state["scene"] != FINAL_ROOM:
        return False, messages["not_here"], False
    if night["hearing"] is None:
        if answer != "start":
            return False, messages["not_here"], False
        write_night(player, dict(night, hearing=[]))
        return True, "", True
    if answer == "start":
        return False, TEXT[language]["hearing_locked"], False

    night = dict(night, hearing=night["hearing"] + [answer])
    if len(night["hearing"]) == len(HEARING):
        # The saved ending is still "the first ending whose condition is true"; the verdict caps what is shown.
        game.play(player, "present_evidence", language)
        state = game.load(player)
        night["verdict"], _line = verdict_of(state, night["hearing"], bool(night["caught"]), claims_of(night))
        # The true ending: the four story endings seen on earlier nights (tonight's row is not written
        # yet) and a perfect night. The save keeps the story's full_case (point 8).
        if seen_all(player) and perfect_night(state, night):
            night["verdict"] = TRUE_ENDING
        night = record(player, night, night["verdict"])
    write_night(player, night)
    return True, "", True


def entry(who, text, language):
    """One entry of the hearing's log: who speaks, their name and what they say."""
    return {"who": who, "name": PEOPLE[language][who]["name"], "text": text}


def right_line(claim, answer, language, night):
    """The professor's line for a card that breaks the claim: the case file's own, or, for a pair
    only tonight's case has, the line of that case (specs/culprit-of-the-night.md, point 5)."""
    lines = CASE_TEXT[language]["right"][claim["id"]]
    if answer in lines:
        return lines[answer]
    return case_of(night)["right"][language][claim["id"]][answer]


def answer_reply(claim, answer, language, night):
    """What is said right after the player's answer to a claim: Duarte after "concede", otherwise the professor."""
    text = CASE_TEXT[language]
    if answer == "concede":
        return entry("duarte", text["concede"], language)
    if answer in claim["accepts"]:
        return entry("professor", right_line(claim, answer, language, night), language)
    return entry("professor", text["wrong"][claim["wrong"].get(answer, claim["id"])], language)


def hearing_view(state, night, language):
    """The hearing for the snapshot: {step, doubts, said}, rebuilt from the saved answers, or None.

    `said` ends with the claim that waits for an answer; after the third answer it ends with the
    reply to that answer, and `step` stays 3. A player who was caught at computer 12 hears first why
    the professor already doubts them (specs/night-schedule.md, point 8).
    """
    answers = night["hearing"]
    if answers is None:
        return None
    claims = CASE_TEXT[language]["claims"]
    tonight = claims_of(night)
    said = [entry("professor", CASE_TEXT[language]["caught"], language)] if night["caught"] else []
    said.append(entry("duarte", claims[HEARING[0]["id"]], language))
    for number, answer in enumerate(answers):
        mine = TEXT[language]["hearing_concede"] if answer == "concede" else "📁 " + card_label(answer, language)
        said.append({"who": "you", "name": "", "text": mine})
        said.append(answer_reply(tonight[number], answer, language, night))
        if number + 1 < len(HEARING):
            said.append(entry("duarte", claims[HEARING[number + 1]["id"]], language))
    return {"step": min(len(answers) + 1, len(HEARING)), "doubts": doubts(answers, bool(night["caught"]), tonight),
            "said": said}


def shown_ending(state, night, language):
    """The ending on the screen (point 11): the verdict's ending, with the professor's line in
    `verdict` (empty when no line applies). None while the game goes on.

    An ending reached without a hearing (present_evidence played directly) is the story's own. The
    true ending is shown only when read_night believed its verdict (specs/earlier-nights.md, point 8).
    """
    if state["ending"] == "none":
        return None
    if night["verdict"] == TRUE_ENDING:
        return true_ending(language)
    shown, line = state["ending"], ""
    if night["hearing"] is not None:
        shown, line = verdict_of(state, night["hearing"], bool(night["caught"]), claims_of(night))
    ending = next(e for e in STORIES[language]["endings"] if e["id"] == shown)
    verdict = CASE_TEXT[language]["verdicts"][line] if line else ""
    return {"id": ending["id"], "title": ending["title"], "text": ending["text"], "verdict": verdict}
