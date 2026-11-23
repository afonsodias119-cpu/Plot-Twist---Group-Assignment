"""What the 3D campus remembers of a name from one night to the next (specs/earlier-nights.md).

Rules only. The finished nights are the rows of the table `runs` (db.py, point 1); the texts of the
unknown number and of the true ending are in campus_case.py. Both are server only: page3d.py does not
import this file, so the page never sees what a name has seen or what the number will say.

Reading writes nothing. A row is added only by `record`, which is called by the command that ends a
night (the verdict, a direct present_evidence, or 22:45), and the note `run` of tonight's notes
(campus_evidence.read_night) says it was written, so a reload cannot write it again (point 2).
"""

import db
from campus_case import NIGHT_TEXT, TRUE_ENDING
from campus_text import TEXT
from story import STORIES

# The story's endings, in the order of its list: the order of `seen` (point 3).
STORY_ENDINGS = [ending["id"] for ending in STORIES["en"]["endings"]]
# The row of a night that reached 22:45 with no ending (point 2): it counts, and it opens nothing.
TIME_UP = "time_up"
# From this night on, the three round warnings are the unknown number's whisper (point 4).
ROUND_WHISPER_NIGHT = 3


def night_number(player, night):
    """Which night of this name tonight is: the finished nights plus 1 (point 3).

    `night` are tonight's notes. Once tonight's row is written (the note `run`), the night keeps its
    number until the restart. Never below 1, even with a damaged note.
    """
    return number_of(db.load_runs(player), night)


def number_of(runs, night):
    """The night number from the rows already read (see night_number)."""
    finished = len(runs)
    return max(finished if night["run"] else finished + 1, 1)


def seen_in(runs):
    """The story endings among these rows, each once, in the order of the story's list.

    A night that ended at 22:45 (TIME_UP) or in the true ending is not a story ending.
    """
    return [ending for ending in STORY_ENDINGS if ending in runs]


def seen(player):
    """The story endings this name has seen."""
    return seen_in(db.load_runs(player))


def seen_all(player):
    """True when this name has seen every story ending: the gate of the true ending is open."""
    return len(seen(player)) == len(STORY_ENDINGS)


def record(player, night, ending):
    """Write tonight's row in `runs` once, with the ending that was shown (point 2).

    Returns tonight's notes with `run` set to True: the caller saves them with
    campus_evidence.write_night in the same command. When the row is already written, nothing is.
    """
    if night["run"]:
        return night
    db.add_run(player, ending)
    return dict(night, run=True)


def memory_view(player, night):
    """The snapshot's `memory` (point 3): {"night", "seen", "open", "over"}."""
    runs = db.load_runs(player)   # read once: the four fields come from the same rows
    found = seen_in(runs)
    return {"night": number_of(runs, night), "seen": found,
            "open": len(found) == len(STORY_ENDINGS), "over": TRUE_ENDING in runs}


def whispers(state, memory, language):
    """The snapshot's `whispers`: the unknown number's messages as this night starts, as {"id", "text"}.

    None on night 1, after an ending, and once the true ending was recorded (the number is quiet).
    Nights 2, 3 and 4 have their own line, night 5 and every later night share one; once the four
    story endings were seen, the dare takes the place of the line of the night (point 4).
    """
    number = memory["night"]
    if number == 1 or state["ending"] != "none" or memory["over"]:
        return []
    texts = NIGHT_TEXT[language]
    if memory["open"]:
        text = texts["dare"]
    else:
        lines = texts["whispers"]   # nights 2, 3, 4, then 5 and later
        text = lines[min(number - 2, len(lines) - 1)]
    return [{"id": f"night-{number}", "text": text}]


def round_warning(language, number):
    """The text of the three round warnings on night `number` (point 4): the impersonal text of
    specs/night-schedule.md on nights 1 and 2, the unknown number's whisper from night 3."""
    if number >= ROUND_WHISPER_NIGHT:
        return NIGHT_TEXT[language]["round"]
    return TEXT[language]["schedule"]["round"]


def true_ending(language):
    """The true ending as the snapshot carries it (point 8), sent only on the night that earned it.

    It has no professor's line: `verdict` is empty, as for an ending without a cap.
    """
    ending = NIGHT_TEXT[language]["ending"]
    return {"id": TRUE_ENDING, "title": ending["title"], "text": ending["text"], "stamp": ending["stamp"],
            "emoji": ending["emoji"], "voices": list(ending["voices"]), "verdict": ""}
