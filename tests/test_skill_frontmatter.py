"""Guards the skill visibility rules of the shared skill source.

Two things are pinned here, both host-independent:

1. Skills that must NOT be advertised to the model carry the V2 switch
   `metadata.opencode/autoinvoke: false`. The older `slash: true` field looks
   like it does this but is inert in OpenCode 2 (unknown frontmatter is
   ignored), so its presence anywhere is a bug.
2. Exactly one search skill is advertised (the provider-neutral entry point);
   the SearXNG backend manual stays loadable by ID but out of the model's list.
"""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"

# Skills that are loaded on demand only (explicit ID / @mention).
HIDDEN_SKILLS = {
    "codebase-audit",
    "grill-me",
    "grill-with-docs",
    "searxng",
    "teach",
}

# The two search skills; exactly one of them may be advertised.
SEARCH_SKILLS = {"deepseek-search", "searxng"}

AUTOINVOKE_FALSE = re.compile(r"""["']?opencode/autoinvoke["']?\s*:\s*false""")
SLASH_FIELD = re.compile(r"^\s*slash\s*:", re.MULTILINE)


def frontmatter(skill_dir):
    """The raw YAML frontmatter block of a skill (no delimiters)."""
    text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    if not text.startswith("---"):
        raise AssertionError("{}: SKILL.md has no frontmatter".format(skill_dir.name))
    end = text.index("\n---", 3)
    return text[3:end]


class SkillVisibilityTest(unittest.TestCase):
    def test_hidden_skills_supply_autoinvoke_false(self):
        missing = []
        for name in sorted(HIDDEN_SKILLS):
            skill_dir = SKILLS / name
            self.assertTrue((skill_dir / "SKILL.md").exists(), name)
            if not AUTOINVOKE_FALSE.search(frontmatter(skill_dir)):
                missing.append(name)
        self.assertEqual(
            missing,
            [],
            "Hidden skills without metadata.opencode/autoinvoke: false: "
            + ", ".join(missing),
        )

    def test_no_inert_slash_field(self):
        offenders = sorted(
            skill.parent.name
            for skill in SKILLS.glob("*/SKILL.md")
            if SLASH_FIELD.search(frontmatter(skill.parent))
        )
        self.assertEqual(
            offenders,
            [],
            "`slash: true` is ignored by OpenCode 2 - use "
            "metadata.opencode/autoinvoke: false instead: " + ", ".join(offenders),
        )

    def test_exactly_one_advertised_search_skill(self):
        advertised = {
            name
            for name in SEARCH_SKILLS
            if not AUTOINVOKE_FALSE.search(frontmatter(SKILLS / name))
        }
        self.assertEqual(
            advertised,
            {"deepseek-search"},
            "Exactly one search skill may be advertised to the model",
        )


if __name__ == "__main__":
    unittest.main()
