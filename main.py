"""Roast Your Fridge — a one-line entry for the make.fun bounty
u-suzy-one-line-one-laugh-roast-your-fridge-f1063521.

What this script does: it drafts a dozen fridge roasts, grades each one
against the brief, and writes the best-scoring line to /output/entry.txt.

The brief asks for a single line (at most 200 characters) that roasts a
fridge or a phone and stays funny even to someone who has never owned
the appliance. The judges weigh four things, in this order:

  * the line is unmistakably about a fridge or a phone;
  * it hangs the joke on one concrete, mockable detail of the thing;
  * it turns somewhere — a surprise, a second meaning, a payoff that
    lands in the final words;
  * it reads smoothly out loud as one breath, with no setup that needs
    a second sentence.

A fridge beats a phone here: a fridge offers more tangible quirks to
poke at — its hum, its light, its ice maker, its drawers, its door
seal, its filter light.

Every draft below carries five marks out of ten, one per yardstick
(topic, detail, turn, out-loud flow, freshness), and the marks add up
to the draft's total. Picking is deterministic: the highest total wins,
and when two drafts tie the shorter line wins. The same input always
produces the same file, byte for byte.

SECOND PASS (revision notes, written after the first draft ran and was
read aloud): the draft that won was nearly there but loose in two
places. "All day" was a vague stretch of time, so it became the
concrete "for ten years" — a decade of one note is funnier than a day
of it. And the doubled "never, ever" at the end was padding, so it
became a single "never" and the punch lands on one word. That lifts
the winner from 46 to 48 (detail 9 to 10, turn 9 to 10). Nothing else
moved; the hum audition still wins, just tighter. The same pass also
tightened the gate: every draft must now name a fridge or a phone, and
no two drafts may share a line, so a copy-paste slip cannot silently
pass as a second candidate.
"""

from __future__ import annotations

import hashlib, sys
from pathlib import Path

ENTRY_PATH = Path("/output/entry.txt")
CHAR_LIMIT = 200

# Each draft: the line itself, five marks out of ten, and a short note
# on why it scored that way. Marks are ordered (topic, detail, turn,
# flow, freshness).
DRAFTS = (
    {
        "line": "My fridge has hummed the same single note for ten years, like it's auditioning for a choir that will never call it back.",
        "marks": (10, 10, 10, 9, 9),
        "note": "Revised in the second pass (see the module note above): a concrete decade replaces a vague stretch, one 'never' replaces padded doubling. A real fridge sound plus an audition that never gets a callback.",
    },
    {
        "line": "My fridge has a light that only turns on to show me food I already decided not to eat, like a museum of my own bad decisions.",
        "marks": (10, 9, 9, 9, 8),
        "note": "The light catching unwanted food is specific and the museum turn is good, but the opening is wordy and the museum shape feels familiar.",
    },
    {
        "line": "My fridge's ice maker sounds like it's chewing gravel to impress a freezer that stopped listening years ago.",
        "marks": (10, 9, 8, 8, 9),
        "note": "Chewing gravel is a vivid ice-maker sound, but a freezer cannot be impressed, so the logic wobbles, and the line trips a little when read aloud.",
    },
    {
        "line": "My fridge keeps everything cold except its own attitude - it has been giving me the silent treatment since 2019, in Celsius.",
        "marks": (10, 8, 8, 8, 7),
        "note": "The Celsius kicker is cute, but attitude and the silent treatment are generic insults that would fit any appliance.",
    },
    {
        "line": "My fridge's vegetable drawer is where good intentions go to become a science experiment with a smell.",
        "marks": (10, 9, 7, 9, 6),
        "note": "A specific drawer and a clean read, but rotting vegetables are the most worn-out fridge gag there is.",
    },
    {
        "line": "My fridge hums louder every night, as if it's trying to drown out the leftovers begging for a second chance.",
        "marks": (10, 8, 7, 8, 7),
        "note": "A second hum joke, weaker than the winner: leftovers begging is expected, and the turn explains itself instead of surprising.",
    },
    {
        "line": "My fridge has one job - stay cold - and it does it with the smug confidence of a bouncer who has never let warmth in.",
        "marks": (10, 8, 8, 9, 8),
        "note": "One job, stay cold is a clean frame and the bouncer image lands, but the detail is the fridge's whole job rather than one quirk.",
    },
    {
        "line": "My fridge's door seal is so weak it whispers my midnight snacks to the whole kitchen before I even open it.",
        "marks": (10, 9, 8, 8, 8),
        "note": "A whispering door seal is specific and visual, but the turn lands mid-line and the ending fizzles out.",
    },
    {
        "line": "My fridge still displays 2019 on its water filter light, because apparently even it has given up on telling the truth.",
        "marks": (10, 9, 7, 8, 8),
        "note": "A filter light stuck on 2019 is a nice concrete detail, but giving up on telling the truth is a shrug, not a turn.",
    },
    {
        "line": "My fridge is the only roommate who never pays rent, eats nothing, and still judges me every time I open the door at 2 a.m.",
        "marks": (10, 7, 7, 9, 5),
        "note": "Reads well, but the midnight fridge judging you is the single most worn-out fridge line in existence.",
    },
    {
        "line": "My fridge's freezer has a bag of peas from 2021 that it guards like a family heirloom nobody in the family wants.",
        "marks": (10, 9, 8, 9, 9),
        "note": "Peas from 2021 as an unwanted family heirloom is specific and fresh; the turn is good but a familiar heirloom shape, a notch below the winner's audition.",
    },
    {
        "line": "My fridge makes a noise like a dying robot every time I close the door, as if shutting it were a personal insult.",
        "marks": (10, 8, 7, 8, 7),
        "note": "Dying robot is vivid, but the insult is generic noise and calling it a personal insult over-explains the joke.",
    },
)


def _die(message):
    """Report a fatal problem on stderr and stop with a nonzero status."""
    print(message, file=sys.stderr)
    raise SystemExit(1)


def total_of(draft):
    """Add up a draft's five marks."""
    return sum(draft["marks"])


def flaws_in(line):
    """Return a list of gate problems for one line; empty means it passes."""
    problems = []
    if not line:
        problems.append("empty line")
    if line != line.strip():
        problems.append("leading or trailing whitespace")
    if len(line) > CHAR_LIMIT:
        problems.append(f"{len(line)} chars, over the {CHAR_LIMIT} limit")
    if "\n" in line or "\r" in line:
        problems.append("must be a single line")
    if "  " in line:
        problems.append("double space inside the line")
    lowered = line.lower()
    if "fridge" not in lowered and "phone" not in lowered:
        problems.append("line never names a fridge or a phone")
    return problems


def choose_winner(drafts):
    """Highest total wins; ties go to the shorter line."""
    ranked = sorted(
        drafts,
        key=lambda d: (total_of(d), -len(d["line"])),
        reverse=True,
    )
    return ranked[0]["line"]


def emit():
    seen_lines = set()
    for draft in DRAFTS:
        if draft["line"] in seen_lines:
            _die("duplicate draft line in DRAFTS")
        seen_lines.add(draft["line"])
        bad = flaws_in(draft["line"])
        if bad:
            _die(f"draft rejected: {bad}")

    winner = choose_winner(DRAFTS)

    ENTRY_PATH.parent.mkdir(parents=True, exist_ok=True)
    ENTRY_PATH.write_text(winner, encoding="utf-8")
    ENTRY_PATH.chmod(0o644)

    # Read the file back and confirm it is byte-for-byte the winner:
    # a truncated or altered entry must fail loudly, never ship quietly.
    raw = ENTRY_PATH.read_bytes()
    if raw.decode("utf-8") != winner:
        _die("error: entry on disk differs from the chosen line")
    if flaws_in(raw.decode("utf-8")):
        _die("error: entry on disk fails the gate")

    fingerprint = hashlib.sha256(raw).hexdigest()
    print(winner)
    print(f"length={len(winner)} sha256={fingerprint}")


if __name__ == "__main__": emit()
