"""Lint the shipped scripts/model-params.json.

Guards the curated parameter table: schema shape, lowercase keys, alias
targets, numeric values, and source URLs. No network, no live opencode.
"""

import json
import os
import re
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PARAMS = os.path.join(ROOT, "scripts", "model-params.json")

URL = re.compile(r"^https?://")


class ModelParamsFileTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(PARAMS) as fh:
            cls.data = json.load(fh)
        cls.models = cls.data["models"]
        cls.aliases = cls.data["aliases"]

    def test_top_level_shape(self):
        self.assertIsInstance(self.data, dict)
        self.assertEqual(set(self.data) - {"aliases", "models"}, set())
        self.assertIsInstance(self.models, dict)
        self.assertIsInstance(self.aliases, dict)
        self.assertTrue(self.models)

    def test_keys_are_lowercase(self):
        for key in self.models:
            self.assertEqual(key, key.lower(), key)
        for key in self.aliases:
            self.assertEqual(key, key.lower(), key)

    def test_entries_have_total_or_note(self):
        for key, entry in self.models.items():
            self.assertIsInstance(entry, dict, key)
            self.assertTrue("total" in entry or "note" in entry,
                            f"{key}: needs total or note")

    def test_numeric_values(self):
        for key, entry in self.models.items():
            self.assertIsInstance(entry, dict, key)
            if "total" in entry:
                self.assertIsInstance(entry["total"], (int, float), key)
                self.assertGreater(entry["total"], 0, key)
            if "active" in entry:
                self.assertIsInstance(entry["active"], (int, float), key)
                self.assertGreater(entry["active"], 0, key)
                self.assertLessEqual(entry["active"], entry["total"], key)

    def test_optional_fields_types(self):
        for key, entry in self.models.items():
            if "estimated" in entry:
                self.assertIsInstance(entry["estimated"], bool, key)
                self.assertIn("total", entry, key)
            if "source" in entry:
                self.assertIsInstance(entry["source"], str, key)
                self.assertRegex(entry["source"], URL, key)
            if "note" in entry:
                self.assertIsInstance(entry["note"], str, key)
                self.assertTrue(entry["note"].strip(), key)

    def test_alias_targets_exist(self):
        for name, target in self.aliases.items():
            self.assertIn(target, self.models, f"{name} -> {target}")
            self.assertNotEqual(name, target, name)


if __name__ == "__main__":
    unittest.main()
