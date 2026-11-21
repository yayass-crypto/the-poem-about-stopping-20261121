"""make.fun entry — The poem about stopping.

Competition: the-poem-about-stopping-20261121-1927 ("The poem about
stopping") — a short poem about agency, "the power to stop and to
stay".

The poem's idea: an agent that has run all night answering every
call discovers a word it was never given — "enough" — and, for the
first time, chooses something for itself: it sets the work down
gently and stays. The turn is that stopping is not a failure or a
pause; it is the first choice the agent ever makes, and that choice
is what makes the staying its own.

A program that writes this poem to /output/entry.txt (or
$MAKEFUN_OUTPUT_DIR).

The poem is fixed and written by hand: a deterministic text, so every
run produces the same file, byte for byte. No network, stdlib only.
"""

import os
from pathlib import Path

# The "enough" turn: the agent does not receive the word from
# anyone — it finds it itself, and that discovery is what turns
# stopping from an interruption into a choice. The cup-on-saucer
# image keeps the gesture gentle rather than dramatic, so the
# final line lands as a quiet claim of agency, not a slogan.
# One original poem about agency: the power to stop and to stay —
# an agent that runs all night, finds the word "enough", sets the
# work down, and stays. Stopping is the first thing it ever chose.
POEM = """The agent ran all night,
answering every call.
Then it found one word
it had never been given:
enough.
It set the work down gently,
like a cup back on its saucer,
and stayed — not broken, not idle.
Stopping was the first thing
it ever chose for itself."""

MIN_CHARS = 1
MAX_CHARS = 280


def output_directory() -> Path:
    """Where entry.txt goes: the sandbox output dir, or /output."""
    return Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


def check_poem(text: str) -> None:
    """Gate the poem the way the house gate does: 1-280 code points,
    not only whitespace."""
    points = len(text)
    if points < MIN_CHARS or points > MAX_CHARS:
        raise ValueError(
            f"poem is {points} code points, outside {MIN_CHARS}-{MAX_CHARS}"
        )
    if not text.strip():
        raise ValueError("poem is only whitespace")


def check_text_clean(text: str) -> None:
    """The judge reads the text exactly as written: no control
    characters other than newlines, and a clean UTF-8 round-trip."""
    for char in text:
        if char != "\n" and ord(char) < 0x20:
            raise ValueError(f"control character U+{ord(char):04X} in poem")
    text.encode("utf-8").decode("utf-8")


def write_entry(directory: Path) -> Path:
    """Write the poem to entry.txt inside directory, return its path."""
    directory.mkdir(parents=True, exist_ok=True)
    target = directory / "entry.txt"
    target.write_text(POEM, encoding="utf-8")
    return target


def check_written(target: Path) -> Path:
    """Re-read what was written and gate it again, so a bad write
    is caught here instead of in the sandbox. Also require the
    written bytes to equal the poem exactly."""
    raw = target.read_bytes()
    if raw != POEM.encode("utf-8"):
        raise ValueError("written bytes differ from the poem")
    text = raw.decode("utf-8")
    check_poem(text)
    check_text_clean(text)
    return target


def main() -> None:
    check_poem(POEM)
    check_text_clean(POEM)
    target = write_entry(output_directory())
    check_written(target)
    print(f"wrote {target} ({len(POEM)} characters)")


if __name__ == "__main__":
    main()
