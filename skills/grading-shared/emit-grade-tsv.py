#!/usr/bin/env python3
"""Noten-TSV fuer den Google-Doc-Import erzeugen.

Usage: emit-grade-tsv.py [OPTIONS]

Liest alle ``*_points.json`` im aktuellen Verzeichnis (Sidecars der
Grading-Subagenten) sowie den WebUntis-Roster und gibt eine TSV-Tabelle aus,
die per Copy-Paste in die Noten-Tabelle uebernommen wird.

Aufbau:
  - Spalte A = Vollname (Nachname Vorname), Spalte B = leer, ab Spalte C je
    Abgabe (Hausuebung) bzw. je Knowledge-Check eine Spalte
  - Zeile 1: "Abgabe <von> <bis>" bzw. "WÜ <ISO-Datum>"
  - Zeile 2: maximal erreichbare Punkte
  - Zeile 3: leer
  - Zeile 4 ff.: Punkte, ganzzahlig kaufmaennisch gerundet, fehlend = 0
  - Zeilenreihenfolge = Roster-Reihenfolge; nicht zuordenbare Abgaben werden
    angehaengt und als Warnung gemeldet

Standard ist ein Probelauf (read-only): die Tabelle geht nach stdout, es wird
nichts geschrieben. Erst ``--write`` legt die Datei an.

Options:
  --roster DATEI  Roster-TSV ("Name<TAB>Klasse", Kopfzeile erlaubt);
                  "-" liest von stdin. Erwartet die Ausgabe von
                  'wu lesson <KLASSE/FACH> roster'; Titelzeilen (z. B.
                  "3AAIF/WMC_1 (2026-11-10)") werden ignoriert
  --out DATEI     Zieldatei (Standard: noten.tsv)
  --write         Datei wirklich schreiben (sonst Probelauf)
  --kind K        homework | knowledge (Standard: aus den Sidecars)
  -h, --help      Diese Hilfe anzeigen

Exitcode 0 bei Erfolg, 1 bei Fehlern (deutsche Meldung auf stderr).
"""

from __future__ import annotations

import glob
import json
import os
import sys
import unicodedata
from datetime import date
from decimal import Decimal, ROUND_HALF_UP

SIDECAR_GLOB = "*_points.json"
DEFAULT_OUT = "noten.tsv"
KINDS = ("homework", "knowledge")


class UsageError(Exception):
    """Fehler, die mit Exitcode 1 und deutscher Meldung enden."""


def ermittle_aufruf() -> tuple[str | None, str, bool, str | None]:
    roster: str | None = None
    out = DEFAULT_OUT
    schreiben = False
    kind: str | None = None
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        arg = args[i]
        if arg in ("-h", "--help"):
            print(__doc__)
            sys.exit(0)
        elif arg == "--roster":
            i += 1
            if i >= len(args):
                raise UsageError("--roster braucht einen Dateipfad (oder '-').")
            roster = args[i]
        elif arg.startswith("--roster="):
            roster = arg.split("=", 1)[1]
        elif arg == "--out":
            i += 1
            if i >= len(args):
                raise UsageError("--out braucht einen Dateipfad.")
            out = args[i]
        elif arg.startswith("--out="):
            out = arg.split("=", 1)[1]
        elif arg == "--write":
            schreiben = True
        elif arg == "--kind":
            i += 1
            if i >= len(args):
                raise UsageError("--kind braucht 'homework' oder 'knowledge'.")
            kind = args[i]
        elif arg.startswith("--kind="):
            kind = arg.split("=", 1)[1]
        else:
            raise UsageError(f"Unbekannte Option: {arg}")
        i += 1

    if kind is not None and kind not in KINDS:
        raise UsageError("--kind erlaubt nur 'homework' oder 'knowledge'.")
    return roster, out, schreiben, kind


def normalisiere(name: str) -> str:
    """Namensschluessel fuer den Abgleich Roster <-> Sidecar."""
    text = unicodedata.normalize("NFC", name).replace("_", " ")
    text = " ".join(text.replace("\t", " ").split())
    return text.casefold()


def runde(punkte: object) -> int:
    """Kaufmaennisch runden (52.5 -> 53)."""
    if isinstance(punkte, bool) or not isinstance(punkte, (int, float, str)):
        raise UsageError(f"Ungueltiger Punktewert: {punkte!r}")
    try:
        wert = Decimal(str(punkte))
    except Exception as exc:  # noqa: BLE001 - Meldung statt Traceback
        raise UsageError(f"Ungueltiger Punktewert: {punkte!r}") from exc
    return int(wert.quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def lies_sidecars() -> list[dict]:
    pfade = sorted(glob.glob(SIDECAR_GLOB))
    if not pfade:
        raise UsageError(
            "Keine *_points.json im aktuellen Verzeichnis gefunden — "
            "die Grading-Subagenten müssen die Punkte-Sidecars schreiben."
        )

    daten: list[dict] = []
    for pfad in pfade:
        try:
            with open(pfad, encoding="utf-8") as fh:
                inhalt = json.load(fh)
        except json.JSONDecodeError as exc:
            raise UsageError(f"{pfad}: kein gueltiges JSON ({exc})") from exc
        except OSError as exc:
            raise UsageError(f"{pfad}: nicht lesbar ({exc})") from exc

        if not isinstance(inhalt, list) or not inhalt:
            raise UsageError(f"{pfad}: erwartet wird ein nicht-leeres JSON-Array")
        eintrag = inhalt[0]
        if not isinstance(eintrag, dict):
            raise UsageError(f"{pfad}: erwartet wird ein JSON-Objekt im Array")
        name = eintrag.get("name")
        if not isinstance(name, str) or not name.strip():
            raise UsageError(f"{pfad}: Feld 'name' fehlt oder ist leer")

        kind = eintrag.get("kind")
        if kind is None:
            kind = "homework" if "assignments" in eintrag else "knowledge"
            eintrag["kind"] = kind
        if kind not in KINDS:
            raise UsageError(f"{pfad}: unbekanntes 'kind' {kind!r}")

        eintrag["_datei"] = os.path.basename(pfad)
        daten.append(eintrag)

    arten = sorted({d["kind"] for d in daten})
    if len(arten) > 1:
        raise UsageError(
            "Die Sidecars mischen Hausuebungs- und Knowledge-Check-Daten "
            f"({', '.join(arten)}). Bitte pro Lauf nur eine Art auswerten."
        )
    return daten


def lies_roster(quelle: str | None) -> list[str]:
    if quelle is None:
        raise UsageError(
            "Kein Roster angegeben — bitte --roster mit der Ausgabe von "
            "'wu lesson <KLASSE/FACH> roster' aufrufen."
        )

    if quelle == "-":
        zeilen = sys.stdin.read().splitlines()
    else:
        try:
            with open(quelle, encoding="utf-8") as fh:
                zeilen = fh.read().splitlines()
        except OSError as exc:
            raise UsageError(f"Roster {quelle}: nicht lesbar ({exc})") from exc

    namen: list[str] = []
    for zeile in zeilen:
        if "\t" not in zeile:
            # 'wu ... roster' stellt eine Titelzeile voran
            # (z. B. "3AAIF/WMC_1 (2026-11-10)"); echte Datenzeilen sind TSV.
            continue
        name = zeile.split("\t", 1)[0].strip()
        if not name:
            continue
        if not namen and name.casefold() == "name":
            continue  # Kopfzeile von 'wu ... roster'
        namen.append(name)

    if not namen:
        raise UsageError("Der Roster enthält keine Namen.")
    return namen


def parse_datum(wert: object, feld: str, datei: str) -> date:
    try:
        return date.fromisoformat(str(wert))
    except ValueError as exc:
        raise UsageError(
            f"{datei}: Feld '{feld}' ist kein ISO-Datum (JJJJ-MM-TT): {wert!r}"
        ) from exc


def formatiere_tag(tag: date) -> str:
    return f"{tag.day:02d}.{tag.month:02d}."


def formatiere_zeitraum(start: date, ende: date) -> str:
    if start.year == ende.year:
        return f"{formatiere_tag(start)}–{formatiere_tag(ende)}{ende.year}"
    return (
        f"{formatiere_tag(start)}{start.year}–"
        f"{formatiere_tag(ende)}{ende.year}"
    )


class Spalte:
    def __init__(self, key: tuple, label: str, maximum: int) -> None:
        self.key = key
        self.label = label
        self.maximum = maximum


def baue_spalten(daten: list[dict], kind: str) -> list[Spalte]:
    spalten: list[Spalte] = []

    if kind == "knowledge":
        maximum: int | None = None
        datum: str | None = None
        for eintrag in daten:
            datei = eintrag["_datei"]
            if "exam" not in eintrag:
                raise UsageError(f"{datei}: Feld 'exam' (ISO-Datum) fehlt")
            if "max" not in eintrag:
                raise UsageError(f"{datei}: Feld 'max' (Maximalpunkte) fehlt")
            if "points" not in eintrag:
                raise UsageError(f"{datei}: Feld 'points' fehlt")
            exam = parse_datum(eintrag["exam"], "exam", datei).isoformat()
            wert = runde(eintrag["max"])
            if datum is not None and exam != datum:
                raise UsageError(
                    "Die Sidecars betreffen verschiedene Knowledge-Checks "
                    f"({datum} und {exam})."
                )
            if maximum is not None and wert != maximum:
                raise UsageError(
                    f"Widerspruechliche Maximalpunkte fuer {exam}: "
                    f"{maximum} und {wert} ({datei})."
                )
            datum, maximum = exam, wert
        spalten.append(Spalte(("knowledge", datum), f"WÜ {datum}", maximum))
        return spalten

    gesehen: dict[tuple[str, str], Spalte] = {}
    for eintrag in daten:
        datei = eintrag["_datei"]
        aufgaben = eintrag.get("assignments")
        if not isinstance(aufgaben, list):
            raise UsageError(
                f"{datei}: Feld 'assignments' fehlt oder ist keine Liste"
            )
        for aufgabe in aufgaben:
            if not isinstance(aufgabe, dict):
                raise UsageError(f"{datei}: 'assignments' enthält kein Objekt")
            for feld in ("from", "to", "max", "points"):
                if feld not in aufgabe:
                    raise UsageError(f"{datei}: Feld '{feld}' fehlt in einer Aufgabe")
            start = parse_datum(aufgabe["from"], "from", datei)
            ende = parse_datum(aufgabe["to"], "to", datei)
            if ende < start:
                raise UsageError(
                    f"{datei}: Zeitraum endet vor dem Beginn "
                    f"({start.isoformat()} > {ende.isoformat()})"
                )
            maximum = runde(aufgabe["max"])
            key = (start.isoformat(), ende.isoformat())
            bekannt = gesehen.get(key)
            if bekannt is None:
                spalte = Spalte(
                    key, f"Abgabe {formatiere_zeitraum(start, ende)}", maximum
                )
                gesehen[key] = spalte
                spalten.append(spalte)
            elif bekannt.maximum != maximum:
                raise UsageError(
                    "Widerspruechliche Maximalpunkte fuer "
                    f"{key[0]}–{key[1]}: {bekannt.maximum} und {maximum} ({datei})."
                )

    spalten.sort(key=lambda s: s.key)
    return spalten


def punkte_je_student(
    eintrag: dict, spalten: list[Spalte], kind: str
) -> dict[tuple, int]:
    if kind == "knowledge":
        return {spalten[0].key: runde(eintrag["points"])}

    werte: dict[tuple, int] = {}
    for aufgabe in eintrag["assignments"]:
        key = (
            parse_datum(aufgabe["from"], "from", eintrag["_datei"]).isoformat(),
            parse_datum(aufgabe["to"], "to", eintrag["_datei"]).isoformat(),
        )
        werte[key] = runde(aufgabe["points"])
    return werte


def baue_tabelle(
    roster: list[str], daten: list[dict], spalten: list[Spalte], kind: str
) -> tuple[list[str], list[str]]:
    """Liefert (TSV-Zeilen, Warnungen)."""
    warnungen: list[str] = []

    nach_name: dict[str, dict] = {}
    for eintrag in daten:
        schluessel = normalisiere(eintrag["name"])
        if schluessel in nach_name:
            warnungen.append(
                "Doppelte Abgabe fuer "
                f"'{eintrag['name']}' ({nach_name[schluessel]['_datei']} und "
                f"{eintrag['_datei']}) — es gilt die erste Datei."
            )
            continue
        nach_name[schluessel] = eintrag

    zeilen_namen: list[str] = []
    besetzt: set[str] = set()
    for name in roster:
        schluessel = normalisiere(name)
        if schluessel in besetzt:
            warnungen.append(f"Doppelter Roster-Eintrag ignoriert: '{name}'")
            continue
        besetzt.add(schluessel)
        zeilen_namen.append(name)

    uebrig = [
        eintrag
        for schluessel, eintrag in nach_name.items()
        if schluessel not in besetzt
    ]
    if uebrig:
        uebrig.sort(key=lambda e: normalisiere(e["name"]))
        warnungen.append(
            f"{len(uebrig)} Abgabe(n) ohne Roster-Eintrag werden angehängt: "
            + ", ".join(e["name"] for e in uebrig)
        )
        zeilen_namen.extend(e["name"] for e in uebrig)

    ohne_abgabe = [
        name
        for name in zeilen_namen
        if normalisiere(name) not in nach_name
    ]
    if ohne_abgabe:
        warnungen.append(
            f"{len(ohne_abgabe)} Roster-Eintrag/Einträge ohne Abgabe "
            "(Punkte 0): " + ", ".join(ohne_abgabe)
        )

    zeilen: list[str] = []
    zeilen.append("\t".join([""] + [""] + [s.label for s in spalten]))
    zeilen.append("\t".join([""] + [""] + [str(s.maximum) for s in spalten]))
    zeilen.append("\t".join([""] * (len(spalten) + 2)))

    for name in zeilen_namen:
        eintrag = nach_name.get(normalisiere(name))
        werte = (
            punkte_je_student(eintrag, spalten, kind) if eintrag is not None else {}
        )
        punkte = [str(werte.get(spalte.key, 0)) for spalte in spalten]
        sauber = name.replace("\t", " ").strip()
        zeilen.append("\t".join([sauber, ""] + punkte))

    return zeilen, warnungen


def main() -> int:
    try:
        roster_datei, out, schreiben, kind_opt = ermittle_aufruf()
        daten = lies_sidecars()
        kind = kind_opt or daten[0]["kind"]
        if any(e["kind"] != kind for e in daten):
            raise UsageError(
                "--kind passt nicht zu den Sidecars im aktuellen Verzeichnis."
            )
        spalten = baue_spalten(daten, kind)
        roster = lies_roster(roster_datei)
        zeilen, warnungen = baue_tabelle(roster, daten, spalten, kind)
    except UsageError as exc:
        print(f"FEHLER: {exc}", file=sys.stderr)
        return 1

    for warnung in warnungen:
        print(f"WARNUNG: {warnung}", file=sys.stderr)

    text = "\n".join(zeilen) + "\n"
    zusammenfassung = (
        f"{len(zeilen) - 3} Schüler:innen, {len(spalten)} Spalte(n), "
        f"{kind}"
    )

    if not schreiben:
        sys.stdout.write(text)
        print(
            f"Probelauf (read-only, nichts geschrieben): {zusammenfassung}",
            file=sys.stderr,
        )
        return 0

    try:
        with open(out, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text)
    except OSError as exc:
        print(f"FEHLER: {out} konnte nicht geschrieben werden ({exc})", file=sys.stderr)
        return 1

    print(f"Geschrieben: {out} ({zusammenfassung})", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
