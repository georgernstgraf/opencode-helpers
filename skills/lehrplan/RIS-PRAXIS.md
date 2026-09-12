# RIS-Praxiswissen (projektübergreifend)

Generisches, gegenstandsunabhängiges Wissen zum Fetchen von
ris.bka.gv.at. Angereichert aus realen Aufgabe-1/2-Läufen.
**Persist-back-Regel: nach jedem Aufgabe-1/2-Lauf neu gelernte generische
RIS-Muster in diesen Abschnitt übernehmen** (Wissen auf Skill-Ebene —
dieses Wissen ist nicht projektspezifisch und darf nicht in den Docs
eines einzelnen Repos gefangen bleiben).

## Fetch-Strategien

- **Nie** `webfetch` auf die `GeltendeFassung.wxe`-Seite
  (Gesetzesnummer-URL) — bei Lehrplanpaketen liefert sie das *gesamte*
  Paket (alle Anlagen, oft > 5 MB) und überschreitet das webfetch-Limit.
  Stattdessen `curl` + lokales Parsen.
- **Autorisierender Ein-Zeilen-Novellen-Check:** `curl` auf das
  **NOR-Dokument der Anlage des Zweigs** (Link in METADATA.md gespeichert).
  Sein Kundmachungsorgan-Kopf liest sich z. B. „BGBl. II Nr. 262/2015
  zuletzt geändert durch BGBl. II Nr. 250/2021" — eine Zeile,
  Änderungsprüfung komplett. Mit
  `rg -o ".{200}zuletzt geändert.{200}"` extrahieren.
- **Novelle identifizieren:** die ELI-Seite
  `https://www.ris.bka.gv.at/eli/bgbl/II/<Jahr>/<Nr>` ist klein und liefert
  Kurztitel, Kundmachungsdatum, Typ, einbringende Stelle.
- **Novellen-Details:** signiertes PDF unter
  `https://www.ris.bka.gv.at/Dokumente/BgblAuth/BGBLA_<Jahr>_II_<Nr>/BGBLA_<Jahr>_II_<Nr>.pdf`,
  dann `pdftotext` + `rg`. Details:
  - Novellen-§§ sind fortlaufend **pro Novelle** nummeriert — nach
    `Anlage <N.N>` / Gegenstands-Schlüsselwörtern greppen, um die §§ zu
    finden, die die Anlage des Gegenstands berühren.
  - Inkrafttreten-Muster: „Die Abschnitte I und VII der Anlage <N.N> …
    treten hinsichtlich des I. Jahrganges mit 1. September <Jahr> und
    hinsichtlich der weiteren Jahrgänge jeweils mit 1. September der
    Folgejahre jahrgangsweise aufsteigend in Kraft."
  - Eine Novelle kann bloß allgemeinbildende Abschnitte berühren (z. B.
    Religion/Ethik 2021), während der Abschnitt des Gegenstands
    unverändert bleibt — in dem Fall bleiben die Extrakte gültig, keine
    Re-Extraktion.
- **ELI-Seite des Stammgesetzes** (`…/eli/bgbl/II/2015/262/20150917`)
  listet alle Anlagen und Kern-Metadaten — nützlich für Aufgabe A.

## PDF-Ablage

- RIS-PDFs nach `lehrplan/RIS/YYYY-MM-DD_<name>.pdf` mit dem
  **Kundmachungsdatum** (das Fetch-Datum ist irrelevant — das Präfix
  datiert den Gesetzestext). Novellen:
  `lehrplan/RIS/YYYY-MM-DD_BGBl-II-<Nr>_Novelle-<slug>.pdf`.
- Der `lehrplan/`-Root bleibt sauber: Gesetzestext-PDFs im
  `lehrplan/`-Root sind ein Konformitäts-Check-Befund mit
  Migrationspflicht.
- Andere (nicht-RIS-)Referenz-PDFs unterliegen **nicht** der
  Datumpräfix-Konvention und kommen nie in `lehrplan/RIS/`.

## Ausgabe in METADATA.md

- Jede RIS-Abfrage in METADATA.md dokumentieren: „RIS-Status abgefragt am
  YYYY-MM-DD: … zuletzt geändert durch …" als Belegzeile unter der
  Änderungshistorie.
- Niemals eine Änderung einer BGBl.-Nummer zuordnen, ohne sie gefetcht zu
  haben — plausibel aussehende Paare (Datum + Nummer) können falsch sein
  (z. B. BGBl. II Nr. 74/2017 = IngG-Fachrichtungsverordnung, hat mit dem
  HTL-Lehrplanpaket nichts zu tun).
