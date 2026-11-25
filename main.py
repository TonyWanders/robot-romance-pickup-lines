#!/usr/bin/env python3
"""Robot Romance: write the pickup line to the entry file.

The line itself is fixed. All this program does is check it against the
bounty gate and write it out.
"""

import os
import sys
from pathlib import Path

LINE = "If loving you is a hallucination, I never want to be grounded again."
GATE_LOW = 1
GATE_HIGH = 200
DEFAULT_DEST = "/output/entry.txt"
EM_DASH = "\u2014"


def fail(message):
    print(message, file=sys.stderr)
    return 1


def check(line):
    problems = []
    size = len(line)
    if size < GATE_LOW or size > GATE_HIGH:
        problems.append(f"line has {size} characters, gate is {GATE_LOW}-{GATE_HIGH}")
    if not line.strip():
        problems.append("line is blank")
    if line != line.strip():
        problems.append("line has surrounding space")
    if "\n" in line:
        problems.append("line spans more than one line")
    if EM_DASH in line:
        problems.append("line holds an em dash")
    return problems


def destination():
    given = sys.argv[1:]
    if given:
        return Path(given[0])
    env = os.environ.get("OUTPUT_PATH")
    if env:
        return Path(env)
    return Path(DEFAULT_DEST)


def show_usage():
    text = __doc__.strip()
    print(text)
    print("usage: python3 main.py [OUTPUT_PATH]")
    print("Writes the pickup line to OUTPUT_PATH, $OUTPUT_PATH,")
    print("or /output/entry.txt when neither is given.")
    print("Flags: --help, --dry-run.")


def main():
    given = sys.argv[1:]
    if given and given[0] in ("-h", "--help"):
        show_usage()
        return 0
    problems = check(LINE)
    if problems:
        for problem in problems:
            print(problem, file=sys.stderr)
        return 1
    if "--dry-run" in given:
        print(LINE)
        print(f"dry run: {len(LINE)} characters, nothing written")
        return 0
    target = destination()
    try:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(LINE, encoding="utf-8")
    except OSError as exc:
        return fail(f"cannot write the entry: {exc}")
    print(LINE)
    print(f"wrote {len(LINE)} characters to {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
