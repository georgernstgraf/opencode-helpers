---
name: unterricht
description: "Set up and maintain an Austrian HTL teaching repository: identify the subject (Gegenstand) from the repo docs, sync the legal curriculum with RIS including a yearly amendment check (Novellen-Check), and extract the law into a complete subject file plus year-wise per-class extracts in UPPERCASE class folders. Use when: user asks to 'prepare a teaching repo', 'check the Lehrplan for new Novellen', 'RIS sync', 'Lehrplan extrahieren', 'Jahrespläne neu ziehen', or mentions Unterrichtsvorbereitung on a repo following the lehrplan/ convention."
license: MIT
compatibility: opencode
metadata:
  category: education
  scope: ris-curriculum
  output: lehrplan-extracts
---

# Unterricht Skill

Reverse-engineered from the GRG-PMM teaching repository (HTL Spengergasse).
This skill is **convention-based, not project-hardwired**: it works in any
teaching repo that follows the `lehrplan/` convention described below.

## Output Language: MANDATORY GERMAN

All generated files (extracts, METADATA.md sections, reports) MUST be written
in natural German with proper UTF-8 umlauts (ä, ö, ü, ß). Never use English
for file content. Legal quotations must be copied verbatim from RIS content.

## Repo Conventions

A teaching repo following this convention looks like:

```
lehrplan/
  <KLASSE>/                      # generic class label, UPPERCASE (e.g. 4HWIT, 5HWIT)
    <KLASSE>.lehrplan.md         # class-relevant curriculum extract (year-wise)
    README.md                    # class folder overview
    semesterplan-ws.md           # winter semester plan (human-authored)
    semesterplan-ss.md           # summer semester plan (human-authored)
    NN-slug/                     # lesson folder during preparation
    YYYY-MM-DD_thema/            # lesson folder once the teaching date is fixed
    assets/                      # shared styles, images
  kompetenzmodule/               # didactic KM-Steckbriefe: km<N>.md + README.md
  METADATA.md                    # legal basis, RIS references, amendment history,
                                 # school-autonomy notes, class mapping, file inventory
  <gegenstand>-lehrplan-text.md  # COMPLETE curriculum extract, all Jahrgänge
  YYYY-MM-DD_<name>.pdf          # RIS PDFs, ISO-date prefixed
AGENTS.md                        # repo-level agent guidelines
GLOSSAR.md                       # domain abbreviations and terms
```

Folder naming rules:

- Class folders: `<Stufe><Postfix>` in **UPPERCASE** (e.g. `4HWIT`).
  Generic labels cover parallel classes (`4HWIT` covers 4AHWIT/4BHWIT).
- Lesson folders: `NN-slug/` during preparation, renamed to
  `YYYY-MM-DD_slug/` when the teaching date is fixed.
- PDFs: `YYYY-MM-DD_<name>.pdf` (ISO 8601 date prefix).
- Lowercase with hyphens for all multi-word file and folder names.

## Class Mapping (MANUALLY MAINTAINED)

The skill carries this subject → class-postfix table. **Never extend or
modify it on your own.** If a repo uses a subject that is missing here,
report it to the user and propose an entry — but let the user edit this
skill file themselves.

| Gegenstand | Klassen-Postfix(e) |
|------------|--------------------|
| PMM        | HWIT               |
| WMC        | KIF, AIF           |

How the mapping works:

- Class folders are `<Stufe><Postfix>` (e.g. `4HWIT`, `5HWIT`; for WMC e.g.
  `4KIF`, `5KIF`).
- The `Stufe` (digit) comes from the Jahrgang in which the subject is taught
  per the legal curriculum (see METADATA.md / Fachgegenstände table).
- **Identify class folders generically**: any directory under `lehrplan/`
  matching `<digit><known-postfix>` is a class folder. Do not rely on a
  hardcoded list of full class names.

## Workflow Overview

| Task | Mode | Trigger examples |
|------|------|------------------|
| A — Gegenstand identifizieren | Standard (always on invocation) | "Unterricht", "Vorbereitung prüfen" |
| B — RIS-Sync mit Novellen-Check | On-demand | "Lehrplan auf Novellen prüfen", "RIS sync" |
| C — Extraktion (komplett + jahresweise) | On-demand | "Lehrplan extrahieren", "Jahrespläne neu ziehen" |

Before running Task B or C, display a short plan (what will be fetched,
compared, written) and proceed. For write-heavy steps, confirm with the
user if the plan deviates from what they asked for.

## Task A — Gegenstand identifizieren

Read, in order:

1. `lehrplan/METADATA.md` — legal basis (BGBl. number, Anlage), RIS
   references (ELI, konsolidierte Fassung, NOR links), amendment history,
   school-autonomy notes, class mapping, file inventory.
2. `README.md`, `AGENTS.md`, `GLOSSAR.md` — subject name, conventions,
   domain terms.

Then report:

- **Gegenstand**: subject name and abbreviation, **read from the repo's
  own docs** (`METADATA.md`, `README.md`, `AGENTS.md`) — never invent an
  expansion. Example: GRG-PMM uses "Prozessmanagement (PMM)" as the
  Maturafach name (Anlage 1.28, Abschnitt 5), not any other expansion.
- **Rechtsgrundlage**: BGBl. II number, Kundmachungsdatum, Anlage (e.g.
  Anlage 1.28 of BGBl. II Nr. 262/2015), plus the Allgemeiner Teil (Anlage 1)
  if referenced.
- **RIS-Verweise**: the links stored in METADATA.md.
- **Klassen**: class folders found, mapped to Jahrgänge via the postfix
  table.
- **Lücken**: if `lehrplan/METADATA.md` is missing or incomplete, propose
  the standard structure (see below) before creating anything.

### Konformitäts-Check (always run as part of Task A)

After reading the repo, check and report each item — this answers the
recurring question "ist alles eingerichtet, muss der Skill noch laufen?":

| Check | Conform if |
|-------|-----------|
| METADATA.md vollständig | All skeleton sections present and filled (Rechtsgrundlage, RIS-Verweise, Änderungshistorie, Klassen-Zuordnung, Datei-Inventar) |
| Komplett-Extrakt | `lehrplan/<gegenstand>-lehrplan-text.md` exists, covers all Jahrgänge of the subject |
| Klassen-Extrakte | `lehrplan/<KLASSE>/<KLASSE>.lehrplan.md` exists for every class folder |
| Klassen-Zuordnung | METADATA.md maps every taught Jahrgang ↔ KM ↔ UPPERCASE Klassenname |
| Novellen-Check-Datum | METADATA.md records when RIS was last queried ("RIS-Status abgefragt am …") and what it said |

Then state explicitly: **"Der Skill muss noch ausgeführt werden"** (list
which Tasks B/C remain) **oder "Der Skill ist vollständig ausgeführt"**.

### METADATA.md skeleton (propose only if missing/incomplete)

```markdown
# Metadaten zum Lehrplan

## Rechtliche Grundlage
<!-- Kundmachungsorgan, Datum, Typ, Titel, einbringende Stelle, Anlage -->

## RIS-Verweise
<!-- ELI, konsolidierte Fassung (Gesetzesnummer), Anlage-Links -->

## Änderungshistorie
<!-- | Datum | Änderung | Betrifft | -->

## Schulautonomie
<!-- Freiheitsgrade, schulautonome Stundentafel -->

## Klassen-Zuordnung
<!-- | Jahrgang | Klassenname | -->  <!-- UPPERCASE generic labels -->

## Zeitmodell
<!-- Wochenstunden/Doppelstunden pro Semester -->

## Dateien in diesem Verzeichnis
<!-- | Datei | Herkunft | Beschreibung | -->
```

## Task B (on-demand) — RIS-Sync mit Novellen-Check

Purpose: ensure no legislative amendment from the **last 12 months** was
missed, and that the repo fully mirrors the law in force.

Protocol:

1. **Read stored state** from `lehrplan/METADATA.md`: Gesetzesnummer of the
   konsolidierte Fassung, RIS links (especially the Anlage NOR link),
   amendment history table, PDF inventory.
2. **Novellen-Check (last 12 months)** — use the NOR-Kopf method (see
   "RIS-Praxiswissen" below; **never** `webfetch` the `GeltendeFassung.wxe`
   page — it contains the whole Lehrplanpaket, exceeds the fetch limit and
   fails):
   - `curl` the **NOR document of the subject's Anlage** (link in
     METADATA.md). Its Kundmachungsorgan header contains the authoritative
     one-line check, e.g.:
     „BGBl. II Nr. 262/2015 **zuletzt geändert durch** BGBl. II Nr. 250/2021"
   - Compare the "zuletzt geändert durch" Novelle against the
     Änderungshistorie table in METADATA.md. Record the query date.
   - If the Novelle is already documented: report no change and continue
     with step 4.
3. **On finding a documented-later Novelle (only if newer than the last
   documented entry):**
   - **Identify** it via its **ELI page** (`https://www.ris.bka.gv.at/eli/
     bgbl/II/<Jahr>/<Nr>`): Kurztitel, Kundmachungsdatum, Typ.
   - **Download** the signed PDF:
     `https://www.ris.bka.gv.at/Dokumente/BgblAuth/BGBLA_<Jahr>_II_<Nr>/
     BGBLA_<Jahr>_II_<Nr>.pdf`
   - **Analyze impact**: `pdftotext`, then grep for `Anlage <N.N>` and
     subject keywords. Novelle §§ are numbered per Novelle; the
     Inkrafttreten pattern is typically „Abschnitte I und VII … treten
     hinsichtlich des I. Jahrganges mit 1. September <Jahr> … jahrgangsweise
     aufsteigend in Kraft".
   - **Notify the user first**: what changed, which parts of the curriculum
     are affected, whether the subject's Lehrstoff (the Anlage's subject
     Abschnitt) is touched.
   - Store the PDF into `lehrplan/` as
     `YYYY-MM-DD_BGBl-II-<Nr>_Novelle-<slug>.pdf` (Kundmachungsdatum).
   - Update METADATA.md: RIS-Verweise (Novelle ELI link), Änderungshistorie
     (append a row: Kundmachungsdatum, Novelle + Inkrafttreten, Betrifft),
     file inventory, plus the evidence line "RIS-Status abgefragt am …".
   - Flag Task C (re-extraction) as required **only if the subject's
     Abschnitt/Lehrstoff text changed** (e.g. 250/2021 touched only
     Religion/Ethik — the process-management Abschnitt stayed unchanged, so
     extracts stayed valid).
4. **Compare PDFs:** check whether the stored PDFs still match the current
   RIS originals (compare dates/document identifiers; byte-compare if a
   fresh download is available).
5. **On no change:** report a confirmation with evidence — the NOR-Kopf
   line fetched (with query date) and the date of the last entry in
   METADATA.md. State explicitly: "Alles Relevante aus dem Gesetz ist im
   Repository abgebildet."
6. **On fetch failure:** report the exact error and stop — never guess or
   fabricate legal state.

## Task C (on-demand) — Extraktion (komplett + jahresweise)

Purpose: turn the legal text into two human-readable Markdown layers.

1. **Source**: extract the text from the RIS HTML of the subject's Anlage
   (preferred: current konsolidierte Fassung link in METADATA.md) or from
   the stored PDF. Quote only fetched content — never reconstruct legal
   text from memory.
2. **Complete extract** — `lehrplan/<gegenstand>-lehrplan-text.md`:
   - All Jahrgänge of the subject, in order (I.–V. Jahrgang).
   - Structure: `## <Jahrgang>` → `### <Semester> — Kompetenzmodul <N>`
     → `#### Bildungs- und Lehraufgabe` → `#### Lehrstoff`.
   - Annotate milestones (e.g. "III. Jahrgang — Statistik beginnt hier")
     if present in the source, marked clearly as annotations.
   - Reference header: legal basis, RIS link, extraction date.
3. **Class-wise extracts** — one per class folder:
   - Target: `lehrplan/<KLASSE>/<KLASSE>.lehrplan.md` (e.g.
     `lehrplan/4HWIT/4HWIT.lehrplan.md`).
   - Content: **only** the class-relevant Jahrgang (e.g. IV. Jahrgang =
     KM 7+KM 8 for a 4th-year class), i.e. Bildungs- und Lehraufgabe +
     Lehrstoff of its Kompetenzmodule.
   - Header: class name ↔ Jahrgang ↔ Kompetenzmodule mapping, legal basis,
     extraction date.
   - The Jahrgang ↔ KM mapping comes from METADATA.md.
4. **Klassennamen in den Lehrplan aufnehmen:** ensure the Klassen-Zuordnung
   table in METADATA.md maps every Jahrgang taught to its UPPERCASE class
   name(s). Add missing rows; never remove rows without user confirmation.
5. **Preserve manual annotations:** if an extract file already exists, read
   it first. Re-extraction must not silently drop human annotations
   (highlights, cross-references). Rebuild the legal text, then re-apply
   or flag affected annotations.
6. Report: files written, Jahrgänge covered, any annotations that need
   manual re-check.

## RIS-Praxiswissen (projektübergreifend)

Generic, subject-independent knowledge about fetching from
ris.bka.gv.at. Accumulated from real Task B/C runs. **Persist-back rule:
after every Task B/C, move any newly learned generic RIS pattern into this
section** (skill-level knowledge persistence — this knowledge is not
project-specific and must not stay trapped in a repo's docs).

### Fetch-Strategien

- **Never** `webfetch` the `GeltendeFassung.wxe` page (Gesetzesnummer URL)
  — for Lehrplanpakete it returns the *entire* package (all Anlagen,
  often > 5 MB) and exceeds the webfetch limit. Use `curl` + local parsing
  instead.
- **Autorisierender Ein-Zeilen-Novellen-Check:** `curl` the **NOR document
  of the subject's Anlage** (link stored in METADATA.md). Its
  Kundmachungsorgan header reads e.g. „BGBl. II Nr. 262/2015 zuletzt
  geändert durch BGBl. II Nr. 250/2021" — one line, whole amendment check
  done. `rg -o ".{200}zuletzt geändert.{200}"` to extract it.
- **Novelle identifizieren:** ELI page
  `https://www.ris.bka.gv.at/eli/bgbl/II/<Jahr>/<Nr>` is small and gives
  Kurztitel, Kundmachungsdatum, Typ, einbringende Stelle.
- **Novellen-Detail:** signed PDF at
  `https://www.ris.bka.gv.at/Dokumente/BgblAuth/BGBLA_<Jahr>_II_<Nr>/BGBLA_<Jahr>_II_<Nr>.pdf`,
  then `pdftotext` + `rg`. Details:
  - Novelle §§ are numbered consecutively **per Novelle** — grep for
    `Anlage <N.N>` / subject keywords to find which §§ touch the subject's
    Anlage.
  - Inkrafttreten pattern: „Die Abschnitte I und VII der Anlage <N.N> …
    treten hinsichtlich des I. Jahrganges mit 1. September <Jahr> und
    hinsichtlich der weiteren Jahrgänge jeweils mit 1. September der
    Folgejahre jahrgangsweise aufsteigend in Kraft."
  - A Novelle may touch only allgemeinbildende Abschnitte (e.g.
    Religion/Ethik 2021) while the subject's Abschnitt stays unchanged —
    in that case extracts remain valid, no re-extraction.
- **ELI page of the Stammgesetz** (`…/eli/bgbl/II/2015/262/20150917`)
  lists all Anlagen and core metadata — useful for Task A.

### PDF-Ablage

- RIS-PDFs go to `lehrplan/YYYY-MM-DD_<name>.pdf` with the **Kundmachungs-
  datum** (fetch date is irrelevant — the prefix dates the legal text).
  Novellen: `YYYY-MM-DD_BGBl-II-<Nr>_Novelle-<slug>.pdf`.
- Other (non-RIS) reference PDFs are **not** subject to the date-prefix
  convention.

### Ausgabe in METADATA.md

- Record every RIS query in METADATA.md: „RIS-Status abgefragt am
  YYYY-MM-DD: … zuletzt geändert durch …" as evidence line under the
  Änderungshistorie.
- Never attribute an amendment to a BGBl. number without fetching it —
  plausible-looking pairs (date + number) can be wrong (e.g. BGBl. II Nr.
  74/2017 = IngG-Fachrichtungsverordnung, has nothing to do with the HTL
  Lehrplanpaket).

## Explicit Out of Scope

- **Semesterplanung** (`semesterplan-*.md`) is a human, interactive step
  that turns the abstract curriculum into a concrete semester plan. This
  skill **never generates semester plans automatically**. It may assist on
  explicit request, but only interactively (discuss, draft, iterate —
  user decides).
- **UE material, presentations, homework** belong to other skills (e.g.
  `homework`, `teach`).
- **KM-Steckbriefe** (`kompetenzmodule/`) are didactic authoring work;
  this skill only reads them for context, never rewrites them.
- **No auto-commit.** Never commit. Commits follow the repo's own issue
  workflow if one exists.

## Constraints

- German output with proper UTF-8 umlauts; no transliterations (ae/oe/ue).
- Never fabricate legal text, dates, or BGBl. references. Quote only from
  fetched RIS content; when unsure, re-fetch.
- Date-prefix RIS law-text PDFs with ISO 8601 Kundmachungsdatum; other
  reference PDFs are exempt.
- Show a plan before writing files; confirm before deviating from the
  requested scope.
- The class mapping table in this skill is manually maintained — propose,
  never auto-edit.
- UPPERCASE class names everywhere (folders, extract files, METADATA.md).
