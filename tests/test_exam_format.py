"""Tests fuer skills/knowledge-exam/scripts/check-exam-format.sh.

Hermetisch: schreibt Angaben in ein temporaeres Verzeichnis und prueft nur den
Exitcode und die Fehlermeldungen des Format-Lints.
"""

import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKRIPT = ROOT / "skills" / "knowledge-exam" / "scripts" / "check-exam-format.sh"

HINWEISE = """## Hinweise

- Bei jeder Aussage steht eine leere Klammer `[ ]`. Ersetze sie durch `[x]`,
  wenn die Aussage zutrifft. Lass sie leer, wenn sie nicht zutrifft.
- Hältst du eine Aussage für mehrdeutig, schreibe `[-]` und begründe das in
  einem Satz unter der Frage.
- Erlaubte Hilfsmittel: keine.
"""


def frage(nummer, optionen, titel="Thema"):
    """Baut eine MC-Frage; optionen ist eine Liste von Aussage-Zeilen."""
    zeilen = ["### {}. {}".format(nummer, titel), "", "Welche Aussagen sind richtig?", ""]
    zeilen.extend(optionen)
    zeilen.extend(["", "---", ""])
    return "\n".join(zeilen)


def angabe(optionen, hinweise=HINWEISE):
    return "# Knowledge-Check: Test\n\n" + hinweise + "\n---\n\n" + frage(1, optionen)


VIER = ["[ ] Aussage eins.", "[ ] Aussage zwei.", "[ ] Aussage drei.", "[ ] Aussage vier."]


class ExamFormatTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def datei(self, inhalt, name="knowledge_3ahwii_2026-11-09.md"):
        pfad = self.dir / name
        pfad.write_text(inhalt, encoding="utf-8")
        return pfad

    def lauf(self, *pfade):
        return subprocess.run(
            ["bash", str(SKRIPT)] + [str(p) for p in pfade],
            capture_output=True,
            text=True,
            check=False,
        )

    def test_gueltige_angabe(self):
        ergebnis = self.lauf(self.datei(angabe(VIER)))
        self.assertEqual(ergebnis.returncode, 0, ergebnis.stderr)

    def test_freitextfrage_wird_uebersprungen(self):
        text = angabe(VIER) + "### 2. Freitext\n\nBeschreibe dein Vorgehen.\n\n---\n\n---\n"
        ergebnis = self.lauf(self.datei(text))
        self.assertEqual(ergebnis.returncode, 0, ergebnis.stderr)

    def test_alte_buchstaben_form(self):
        optionen = ["a) Aussage eins.", "b) Aussage zwei.", "c) Aussage drei.", "d) Aussage vier."]
        ergebnis = self.lauf(self.datei(angabe(optionen)))
        self.assertEqual(ergebnis.returncode, 1)
        self.assertIn("Buchstaben-Label", ergebnis.stderr)

    def test_umgebrochene_aussage(self):
        optionen = [
            "[ ] Aussage eins.",
            "[ ] Aussage zwei.",
            "[ ] Aussage drei.",
            "[ ] Aussage vier, die leider über zwei",
            "    Zeilen umgebrochen wurde.",
        ]
        ergebnis = self.lauf(self.datei(angabe(optionen)))
        self.assertEqual(ergebnis.returncode, 1)
        self.assertIn("umgebrochene Aussage", ergebnis.stderr)

    def test_zu_wenige_optionen(self):
        ergebnis = self.lauf(self.datei(angabe(VIER[:3])))
        self.assertEqual(ergebnis.returncode, 1)
        self.assertIn("3 statt 4", ergebnis.stderr)

    def test_leerzeile_zwischen_optionen(self):
        optionen = [VIER[0], VIER[1], "", VIER[2], VIER[3]]
        ergebnis = self.lauf(self.datei(angabe(optionen)))
        self.assertEqual(ergebnis.returncode, 1)
        self.assertIn("nicht zusammenhängend", ergebnis.stderr)

    def test_task_listen_form(self):
        optionen = ["- " + o for o in VIER]
        ergebnis = self.lauf(self.datei(angabe(optionen)))
        self.assertEqual(ergebnis.returncode, 1)
        self.assertIn("Task-Listen-Form", ergebnis.stderr)

    def test_klammer_ohne_leerzeichen(self):
        optionen = ["[]Aussage eins."] + VIER[1:]
        ergebnis = self.lauf(self.datei(angabe(optionen)))
        self.assertEqual(ergebnis.returncode, 1)
        self.assertIn("[ ] <Aussage>", ergebnis.stderr)

    def test_vorab_gesetzte_marke(self):
        optionen = ["[x] Aussage eins."] + VIER[1:]
        ergebnis = self.lauf(self.datei(angabe(optionen)))
        self.assertEqual(ergebnis.returncode, 1)
        self.assertIn("vorab gesetzte Marke", ergebnis.stderr)

    def test_fehlender_hinweisblock(self):
        ergebnis = self.lauf(self.datei(angabe(VIER, hinweise="")))
        self.assertEqual(ergebnis.returncode, 1)
        self.assertIn("Hinweisblock fehlt", ergebnis.stderr)

    def test_ohne_fragen_ist_aufruffehler(self):
        ergebnis = self.lauf(self.datei("# Nur Prosa\n\nKein Prüfungstext.\n"))
        self.assertEqual(ergebnis.returncode, 2)

    def test_fehlende_datei_ist_aufruffehler(self):
        ergebnis = self.lauf(self.dir / "gibt-es-nicht.md")
        self.assertEqual(ergebnis.returncode, 2)

    def test_mehrere_dateien_eine_kaputt(self):
        gute = self.datei(angabe(VIER), name="gut.md")
        kaputte = self.datei(angabe(VIER[:2]), name="kaputt.md")
        ergebnis = self.lauf(gute, kaputte)
        self.assertEqual(ergebnis.returncode, 1)
        self.assertIn("kaputt.md", ergebnis.stderr)


if __name__ == "__main__":
    unittest.main()
