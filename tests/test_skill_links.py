import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
LINK = re.compile(r"\]\((\./[^)\s]+)\)")


class SkillLinkTest(unittest.TestCase):
    def test_relative_links_resolve(self):
        missing = []
        for skill in sorted(SKILLS.glob("*/SKILL.md")):
            text = skill.read_text(encoding="utf-8")
            for target in LINK.findall(text):
                path = target.split("#", 1)[0]
                resolved = (skill.parent / path).resolve()
                if not resolved.exists():
                    missing.append(f"{skill.relative_to(ROOT)} -> {target}")
        self.assertEqual(
            missing,
            [],
            "Unresolved skill-relative links:\n" + "\n".join(missing),
        )


if __name__ == "__main__":
    unittest.main()
