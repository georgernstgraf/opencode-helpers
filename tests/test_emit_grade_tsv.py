"""Tests fuer skills/grading-shared/emit-grade-tsv.py (Noten-TSV).

Hermetisch: legt Roster und Punkte-Sidecars in einem temporaeren Verzeichnis
an und ruft das Skript als Subprozess auf. Kein Netz, keine echten Lauf-Daten.
"""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKRIPT = ROOT / "skills" / "grading-shared" / "emit-grade-tsv.py"

ROSTER = "Name\tKlasse\nAbazi Hamza\t3AAIF\nAhmad Ali\t3AAIF\nZorn Eva\t3AAIF\n"


def sidecar(name, **felder):
    eintrag = {"name": name}
    eintrag.update(felder)
    return {f"{name}_points.json": json.dumps([eintrag], ensure_ascii=False)}


def homework(name, werte):
    """werte: Liste von (from, to, max, points)."""
    return sidecar(
        name,
        kind="homework",
        assignments=[
            {"from": von, "to": bis, "max": maximum, "points": punkte}
            for von, bis, maximum, punkte in werte
        ],
    )


class EmitGradeTsvTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name)
        (self.dir / "roster.tsv").write_text(ROSTER, encoding="utf-8")

    def tearDown(self):
        self._tmp.cleanup()

    def schreibe(self, dateien):
        for name, inhalt in dateien.items():
            (self.dir / name).write_text(inhalt, encoding="utf-8")

    def lauf(self, *args, stdin=None):
        return subprocess.run(
            [sys.executable, str(SKRIPT), *args],
            cwd=self.dir,
            capture_output=True,
            text=True,
            input=stdin,
            check=False,
        )

    def test_hausuebung_tsv_layout_rundung_und_nullen(self):
        self.schreibe(
            {
                **homework(
                    "Abazi Hamza",
                    [
                        ("2026-10-06", "2026-10-13", 100, 80),
                        ("2026-10-13", "2026-10-20", 100, 52.5),
                    ],
                ),
                **homework(
                    "Ahmad Ali",
                    [
                        ("2026-10-06", "2026-10-13", 100, 0),
                        ("2026-10-13", "2026-10-20", 100, 0),
                    ],
                ),
            }
        )

        ergebnis = self.lauf("--roster", "roster.tsv")

        self.assertEqual(ergebnis.returncode, 0, ergebnis.stderr)
        self.assertEqual(
            ergebnis.stdout,
            "\t\tAbgabe 06.10.–13.10.2026\tAbgabe 13.10.–20.10.2026\n"
            "\t\t100\t100\n"
            "\t\t\t\n"
            "Abazi Hamza\t\t80\t53\n"
            "Ahmad Ali\t\t0\t0\n"
            "Zorn Eva\t\t0\t0\n",
        )
        self.assertIn("Probelauf", ergebnis.stderr)

    def test_knowledge_check(self):
        self.schreibe(
            {
                **sidecar(
                    "Abazi Hamza",
                    kind="knowledge",
                    exam="2026-10-20",
                    max=145,
                    points=88,
                ),
                **sidecar(
                    "Ahmad Ali",
                    kind="knowledge",
                    exam="2026-10-20",
                    max=145,
                    points=0,
                ),
            }
        )

        ergebnis = self.lauf("--roster", "roster.tsv")

        self.assertEqual(ergebnis.returncode, 0, ergebnis.stderr)
        self.assertEqual(
            ergebnis.stdout,
            "\t\tWÜ 2026-10-20\n"
            "\t\t145\n"
            "\t\t\n"
            "Abazi Hamza\t\t88\n"
            "Ahmad Ali\t\t0\n"
            "Zorn Eva\t\t0\n",
        )

    def test_zeitraum_ueber_jahreswechsel(self):
        self.schreibe(
            homework(
                "Abazi Hamza",
                [("2026-12-22", "2027-01-12", 100, 70)],
            )
        )

        ergebnis = self.lauf("--roster", "roster.tsv")

        self.assertEqual(ergebnis.returncode, 0, ergebnis.stderr)
        self.assertIn("Abgabe 22.12.2026–12.01.2027", ergebnis.stdout)

    def test_probelauf_schreibt_nichts_und_write_schreibt_datei(self):
        self.schreibe(
            homework("Abazi Hamza", [("2026-10-06", "2026-10-13", 100, 80)])
        )

        probelauf = self.lauf("--roster", "roster.tsv")
        self.assertEqual(probelauf.returncode, 0, probelauf.stderr)
        self.assertFalse((self.dir / "noten.tsv").exists())

        schreiben = self.lauf("--roster", "roster.tsv", "--write")
        self.assertEqual(schreiben.returncode, 0, schreiben.stderr)
        self.assertEqual(schreiben.stdout, "")
        self.assertEqual(
            (self.dir / "noten.tsv").read_text(encoding="utf-8"), probelauf.stdout
        )

    def test_abgabe_ohne_roster_eintrag_wird_angehaengt_und_gemeldet(self):
        self.schreibe(
            homework("Neuling Nora", [("2026-10-06", "2026-10-13", 100, 60)])
        )

        ergebnis = self.lauf("--roster", "roster.tsv")

        self.assertEqual(ergebnis.returncode, 0, ergebnis.stderr)
        self.assertIn("ohne Roster-Eintrag", ergebnis.stderr)
        self.assertTrue(ergebnis.stdout.rstrip("\n").endswith("Neuling Nora\t\t60"))

    def test_roster_ueber_stdin(self):
        self.schreibe(
            homework("Abazi Hamza", [("2026-10-06", "2026-10-13", 100, 80)])
        )

        ergebnis = self.lauf("--roster", "-", stdin="Name\tKlasse\nAbazi Hamza\t3AAIF\n")

        self.assertEqual(ergebnis.returncode, 0, ergebnis.stderr)
        self.assertIn("Abazi Hamza\t\t80", ergebnis.stdout)

    def test_titelzeile_und_kopfzeile_des_rosters_werden_ignoriert(self):
        (self.dir / "roster.tsv").write_text(
            "3AAIF/WMC_1 (2026-11-10)\nName\tKlasse\nAbazi Hamza\t3AAIF\n",
            encoding="utf-8",
        )
        self.schreibe(
            homework("Abazi Hamza", [("2026-10-06", "2026-10-13", 100, 80)])
        )

        ergebnis = self.lauf("--roster", "roster.tsv")

        self.assertEqual(ergebnis.returncode, 0, ergebnis.stderr)
        self.assertEqual(
            ergebnis.stdout,
            "\t\tAbgabe 06.10.–13.10.2026\n"
            "\t\t100\n"
            "\t\t\n"
            "Abazi Hamza\t\t80\n",
        )

    def test_widerspruechliche_maximalpunkte_brechen_ab(self):
        self.schreibe(
            {
                **homework("Abazi Hamza", [("2026-10-06", "2026-10-13", 100, 80)]),
                **homework("Ahmad Ali", [("2026-10-06", "2026-10-13", 120, 80)]),
            }
        )

        ergebnis = self.lauf("--roster", "roster.tsv")

        self.assertEqual(ergebnis.returncode, 1)
        self.assertIn("Maximalpunkte", ergebnis.stderr)

    def test_gemischte_arten_brechen_ab(self):
        self.schreibe(
            {
                **homework("Abazi Hamza", [("2026-10-06", "2026-10-13", 100, 80)]),
                **sidecar(
                    "Ahmad Ali",
                    kind="knowledge",
                    exam="2026-10-20",
                    max=145,
                    points=88,
                ),
            }
        )

        ergebnis = self.lauf("--roster", "roster.tsv")

        self.assertEqual(ergebnis.returncode, 1)
        self.assertIn("mischen", ergebnis.stderr)

    def test_ohne_sidecars_und_ohne_roster_klare_fehler(self):
        ohne_sidecars = self.lauf("--roster", "roster.tsv")
        self.assertEqual(ohne_sidecars.returncode, 1)
        self.assertIn("Keine *_points.json", ohne_sidecars.stderr)

        self.schreibe(
            homework("Abazi Hamza", [("2026-10-06", "2026-10-13", 100, 80)])
        )
        ohne_roster = self.lauf()
        self.assertEqual(ohne_roster.returncode, 1)
        self.assertIn("Kein Roster", ohne_roster.stderr)


if __name__ == "__main__":
    unittest.main()
