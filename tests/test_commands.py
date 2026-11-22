"""Guards the command layer (`commands/`).

Commands are plain Markdown files that OpenCode discovers by name; the file body
is the prompt template and `description` lives in the frontmatter. Two failure
modes are pinned here:

1. A command file without frontmatter (or without a description) still loads,
   but shows up unnamed in command lists — and one without a body submits an
   empty prompt.
2. An inline `commands.<name>.template` in a checked-in `opencode.json` shadows
   nothing but silently duplicates a versioned file. That is exactly how
   `/tmpissue` kept running pre-#118 text after `commands/tmpissue.md` had moved
   on (#138): the repo file was dead weight and nobody noticed. Inline command
   definitions are therefore forbidden in this repository's configs.
"""

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMANDS = ROOT / "commands"

DESCRIPTION = re.compile(r"""^\s*description\s*:\s*(.+)$""", re.MULTILINE)


def split_frontmatter(text):
    """(frontmatter, body) of a command file; raises if the block is missing."""
    if not text.startswith("---"):
        raise AssertionError("no frontmatter")
    end = text.index("\n---", 3)
    return text[3:end], text[end + 4 :]


class CommandFileTest(unittest.TestCase):
    def test_every_command_has_a_description_and_a_body(self):
        offenders = []
        for path in sorted(COMMANDS.glob("*.md")):
            frontmatter, body = split_frontmatter(path.read_text(encoding="utf-8"))
            match = DESCRIPTION.search(frontmatter)
            if match is None or not match.group(1).strip():
                offenders.append("{}: no description".format(path.name))
            if not body.strip():
                offenders.append("{}: empty body".format(path.name))
        self.assertEqual(offenders, [], "; ".join(offenders))

    def test_no_inline_command_templates_in_config(self):
        config = ROOT / "opencode.json"
        offenders = []
        if config.exists():
            data = json.loads(config.read_text(encoding="utf-8"))
            offenders = sorted(data.get("commands", {}))
        self.assertEqual(
            offenders,
            [],
            "Commands are file-based in commands/<name>.md - an inline "
            "'commands' block in opencode.json drifts from it (#138): "
            + ", ".join(offenders),
        )


if __name__ == "__main__":
    unittest.main()
