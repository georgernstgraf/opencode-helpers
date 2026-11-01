"""Tests fuer skills/grading-shared/read-anrede.sh (hartes Anrede-Gate).

Hermetisch: legt die Anrede-Datei in einem temporaeren Verzeichnis an.
"""

import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKRIPT = ROOT / "skills" / "grading-shared" / "read-anrede.sh"


class ReadAnredeTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def lauf(self, inhalt=None, dateiname="anrede.txt"):
        pfad = self.dir / dateiname
        if inhalt is not None:
            pfad.write_text(inhalt, encoding="utf-8")
        return subprocess.run(
            ["bash", str(SKRIPT), str(pfad)],
            capture_output=True,
            text=True,
            check=False,
        )

    def test_formelle_anrede(self):
        ergebnis = self.lauf("Sie\n")
        self.assertEqual(ergebnis.returncode, 0, ergebnis.stderr)
        self.assertEqual(ergebnis.stdout.strip(), "Sie")

    def test_informelle_anrede_kleingeschrieben(self):
        ergebnis = self.lauf("  du\n")
        self.assertEqual(ergebnis.returncode, 0, ergebnis.stderr)
        self.assertEqual(ergebnis.stdout.strip(), "Du")

    def test_bom_und_crlf(self):
        ergebnis = self.lauf("\ufeffSie\r\n")
        self.assertEqual(ergebnis.returncode, 0, ergebnis.stderr)
        self.assertEqual(ergebnis.stdout.strip(), "Sie")

    def test_fehlende_datei_stoppt(self):
        ergebnis = self.lauf()
        self.assertEqual(ergebnis.returncode, 1)
        self.assertIn("FEHLT", ergebnis.stderr)
        self.assertIn("anrede.txt", ergebnis.stderr)

    def test_leere_datei_stoppt(self):
        ergebnis = self.lauf("\n \n")
        self.assertEqual(ergebnis.returncode, 1)
        self.assertIn("LEER", ergebnis.stderr)

    def test_ungueltiger_inhalt_stoppt(self):
        ergebnis = self.lauf("beide\n")
        self.assertEqual(ergebnis.returncode, 1)
        self.assertIn("UNGÜLTIG", ergebnis.stderr)

    def test_falscher_aufruf(self):
        ergebnis = subprocess.run(
            ["bash", str(SKRIPT)], capture_output=True, text=True, check=False
        )
        self.assertEqual(ergebnis.returncode, 2)
        self.assertIn("Aufruf", ergebnis.stderr)


if __name__ == "__main__":
    unittest.main()
