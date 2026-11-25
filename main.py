# Roast Your Fridge — make.fun bounty
# u-suzy-one-line-one-laugh-roast-your-fridge-f1063521
#
# The program writes one funny one-line roast of a fridge to
# /output/entry.txt. Candidates were drafted against the judge's brief,
# in order of weight:
#   1. roasts a fridge (or a phone) in a single line
#   2. lands a laugh on a specific, recognisable detail of the appliance
#   3. turns on a twist, a surprise or a double meaning that pays off
#      in the last few words
#   4. reads cleanly aloud as one line, no setup needing a second sentence
#   5. feels fresh rather than a joke every fridge owner has worn out
# Each candidate carries a hand-scored craft score (0-10 per criterion,
# summed below); selection is deterministic: highest score wins, ties go
# to the shorter text. The output is byte-identical on every run.
# Fridge was chosen over phone: a fridge has more concrete, mockable
# details (hum, light, ice maker, drawers, door seal, filter light).
#
# REVISION (second pass, after the first draft ran clean): the winning
# line's weakness was vagueness — "all day" says nothing concrete and
# "never, ever" pads the ending instead of sharpening it. Revised to
# "has hummed ... for ten years" (a concrete duration that makes the
# single note funnier) and a single "never" (the punch lands harder
# without the doubled adverb). Score rises 46 -> 48: detail 9 -> 10,
# twist 9 -> 10. No other candidate changed; the winner is still the
# hum audition, now tighter.

CANDIDATES = [
    # score: fridge 10, detail 10, twist 10, aloud 9, fresh 9 = 48.
    # REVISED (see header): "for ten years" replaces vague "all day",
    # one "never" replaces padded "never, ever". The hum is a real,
    # specific fridge sound; the turn is the audition for a choir
    # that will never call it back, landing on the last words.
    ("My fridge has hummed the same single note for ten years, like "
     "it's auditioning for a choir that will never call it back.",
     48),
    # score: fridge 10, detail 9, twist 9, aloud 9, fresh 8 = 45.
    # The light showing unwanted food is specific; "museum of my own
    # bad decisions" is a good twist, but the setup is wordy and the
    # museum gag is a familiar shape.
    ("My fridge has a light that only turns on to show me food I "
     "already decided not to eat, like a museum of my own bad "
     "decisions.",
     45),
    # score: fridge 10, detail 9, twist 8, aloud 8, fresh 9 = 44.
    # Chewing gravel is a vivid ice-maker sound, but "to impress a
    # freezer" is odd logic — a freezer cannot be impressed — and the
    # line stumbles a little read aloud.
    ("My fridge's ice maker sounds like it's chewing gravel to "
     "impress a freezer that stopped listening years ago.",
     44),
    # score: fridge 10, detail 8, twist 8, aloud 8, fresh 7 = 41.
    # The Celsius kicker is cute, but "attitude / silent treatment"
    # is a generic insult that could fit any appliance.
    ("My fridge keeps everything cold except its own attitude - it "
     "has been giving me the silent treatment since 2019, in Celsius.",
     41),
    # score: fridge 10, detail 9, twist 7, aloud 9, fresh 6 = 41.
    # Specific drawer, clean read, but the rotting-veg joke is the
    # most worn-out fridge gag there is.
    ("My fridge's vegetable drawer is where good intentions go to "
     "become a science experiment with a smell.",
     41),
    # score: fridge 10, detail 8, twist 7, aloud 8, fresh 7 = 40.
    # A second hum joke, weaker than the winner: the leftovers
    # "begging" is expected, and the twist explains itself.
    ("My fridge hums louder every night, as if it's trying to drown "
     "out the leftovers begging for a second chance.",
     40),
    # score: fridge 10, detail 8, twist 8, aloud 9, fresh 8 = 43.
    # "One job - stay cold" is a clean frame and the bouncer image
    # lands, but the detail is the fridge's whole job, not one
    # specific quirk.
    ("My fridge has one job - stay cold - and it does it with the "
     "smug confidence of a bouncer who has never let warmth in.",
     43),
    # score: fridge 10, detail 9, twist 8, aloud 8, fresh 8 = 43.
    # A weak door seal whispering snacks is specific and visual, but
    # the twist lands mid-line and the ending fizzles.
    ("My fridge's door seal is so weak it whispers my midnight "
     "snacks to the whole kitchen before I even open it.",
     43),
    # score: fridge 10, detail 9, twist 7, aloud 8, fresh 8 = 42.
    # The filter light stuck on 2019 is a nice specific detail, but
    # "given up on telling the truth" is a shrug, not a twist.
    ("My fridge still displays 2019 on its water filter light, "
     "because apparently even it has given up on telling the truth.",
     42),
    # score: fridge 10, detail 7, twist 7, aloud 9, fresh 5 = 38.
    # Reads well, but the midnight-fridge-judging-you joke is the
    # single most worn-out fridge line in existence.
    ("My fridge is the only roommate who never pays rent, eats "
     "nothing, and still judges me every time I open the door at "
     "2 a.m.",
     38),
    # score: fridge 10, detail 9, twist 8, aloud 9, fresh 9 = 45.
    # The 2021 peas as an unwanted family heirloom is specific and
    # fresh; the twist is good but a familiar "heirloom nobody
    # wants" shape, a notch below the winner's audition turn.
    ("My fridge's freezer has a bag of peas from 2021 that it guards "
     "like a family heirloom nobody in the family wants.",
     45),
    # score: fridge 10, detail 8, twist 7, aloud 8, fresh 7 = 40.
    # "Dying robot" is vivid, but the insult is generic noise and
    # "personal insult" over-explains the joke.
    ("My fridge makes a noise like a dying robot every time I close "
     "the door, as if shutting it were a personal insult.",
     40),
]

# The gate requires 1-200 characters of non-whitespace UTF-8 text.
MAX_CHARS = 200


def pick(candidates):
    best = None
    for text, score in candidates:
        assert 1 <= len(text) <= MAX_CHARS, \
            f"candidate over gate: {len(text)} chars"
        assert text.strip(), "candidate is blank"
        assert "\n" not in text, "candidate must be a single line"
        key = (score, -len(text))  # highest score, then shortest
        if best is None or key > best[0]:
            best = (key, text)
    return best[1]


def main():
    import hashlib
    import os
    import sys

    roast = pick(CANDIDATES)
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(roast)
    os.chmod("/output/entry.txt", 0o644)
    # Verify the written output: read it back byte-for-byte, re-check
    # the gate (1-200 characters, single line, non-blank) and print a
    # SHA-256 digest so any truncation or alteration is visible. A
    # file that does not match the selected roast must fail loudly
    # instead of shipping a bad entry.
    with open("/output/entry.txt", "rb") as f:
        raw = f.read()
    written = raw.decode("utf-8")
    digest = hashlib.sha256(raw).hexdigest()
    if written != roast:
        print("error: /output/entry.txt does not match selected roast",
              file=sys.stderr)
        sys.exit(1)
    if not (1 <= len(written) <= MAX_CHARS and written.strip()
            and "\n" not in written):
        print("error: /output/entry.txt fails gate: "
              f"{len(written)} chars", file=sys.stderr)
        sys.exit(1)
    print(roast)
    print(f"chars={len(written)} sha256={digest}")


if __name__ == "__main__":
    main()
