#!/usr/bin/env python3
"""The Meeting That Should Have Been One Line.

Writes the single sentence that could have replaced an entire
pointless meeting to $MAKEFUN_OUTPUT_DIR/entry.txt (default
/output/entry.txt), then reads it back and verifies it against the
gate: UTF-8 text, 1-200 characters, not only whitespace, exactly
one line, exactly one sentence.
"""

import os
import sys

LINE = (
    "We all already agree, so I'm sending the email we were "
    "too polite to write, and this meeting is over."
)

MAX_CHARS = 200


def validate(text: str) -> None:
    """Raise ValueError if the text fails any gate rule."""
    if not text:
        raise ValueError("entry is empty")
    if not text.strip():
        raise ValueError("entry is only whitespace")
    if len(text) > MAX_CHARS:
        raise ValueError(
            f"entry is {len(text)} characters, over the {MAX_CHARS} limit"
        )
    if "\n" in text.strip():
        raise ValueError("entry must be a single line")
    if text != text.strip():
        raise ValueError("entry must not start or end with whitespace")
    if any(ord(ch) < 0x20 and ch not in "\t" for ch in text):
        raise ValueError("entry must not contain control characters")
    if "  " in text:
        raise ValueError("entry must not contain double spaces")
    if text.count(".") != 1 or not text.rstrip().endswith("."):
        raise ValueError("entry must be exactly one sentence")


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")

    validate(LINE)

    with open(path, "w", encoding="utf-8") as f:
        f.write(LINE + "\n")

    # Read it back and verify what actually landed on disk.
    with open(path, "r", encoding="utf-8") as f:
        written = f.read()
    validate(written.rstrip("\n"))
    if written.rstrip("\n") != LINE:
        raise ValueError("round-trip mismatch: file content differs from line")

    print(f"Wrote {len(LINE)}-character entry to {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
