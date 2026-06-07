#!/usr/bin/env python3
"""Aggregate per-student *email.json files into a single EMAIL.json.

Usage: aggregate-emails.py [OPTIONS]

Reads all *_email.json files from the current working directory,
fixes double-escaped newlines in body fields, and writes EMAIL.json.

Options:
  --help  Show this message and exit.

Exit code 0 on success, 1 on failure.
"""

import glob
import json
import os
import sys


def main() -> int:
    cwd = os.getcwd()
    files = sorted(glob.glob(os.path.join(cwd, "*_email.json")))

    # Exclude EMAIL.json itself and backup files
    files = [
        f
        for f in files
        if os.path.basename(f) != "EMAIL.json" and "-backup-" not in os.path.basename(f)
    ]

    if not files:
        print("ERROR: No *_email.json files found", file=sys.stderr)
        return 1

    entries = []
    repaired = 0

    for path in files:
        try:
            with open(path, encoding="utf-8") as fh:
                data = json.load(fh)
        except json.JSONDecodeError as e:
            print(f"ERROR: Failed to parse {os.path.basename(path)}: {e}", file=sys.stderr)
            return 1
        except OSError as e:
            print(f"ERROR: Cannot read {os.path.basename(path)}: {e}", file=sys.stderr)
            return 1

        if not isinstance(data, list) or len(data) == 0:
            print(f"ERROR: {os.path.basename(path)}: expected non-empty array", file=sys.stderr)
            return 1

        entry = data[0]
        body = entry.get("body", "")
        if "\\n" in body:
            body = body.replace("\\n", "\n")
            entry["body"] = body
            repaired += 1
        entries.append(entry)

    outpath = os.path.join(cwd, "EMAIL.json")
    try:
        with open(outpath, "w", encoding="utf-8") as fh:
            json.dump(entries, fh, ensure_ascii=False, indent=2)
    except OSError as e:
        print(f"ERROR: Cannot write {outpath}: {e}", file=sys.stderr)
        return 1

    # Validate by re-reading
    try:
        with open(outpath, encoding="utf-8") as fh:
            validated = json.load(fh)
    except json.JSONDecodeError as e:
        print(f"ERROR: Written EMAIL.json is invalid: {e}", file=sys.stderr)
        return 1

    # Verify no double-escaped newlines remain
    for v in validated:
        if "\\n" in v.get("body", ""):
            print("ERROR: Double-escaped newlines remain in output", file=sys.stderr)
            return 1

    print(f"OK: {len(entries)} entries from {len(files)} files, {repaired} body/bodies repaired")
    return 0


if __name__ == "__main__":
    if "--help" in sys.argv or "-h" in sys.argv:
        print(__doc__)
        sys.exit(0)
    sys.exit(main())
