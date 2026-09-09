---
name: lehrplan
description: "Set up and maintain an Austrian HTL teaching repository around three main tasks: fetch the legal curriculum for an Ausbildungszweig (e.g. WII, WIT, KIF) from RIS including a yearly Novellen-Check, extract the Lehrplan for one concrete Gegenstand from that law (with per-Lernziel Erläuterungen explaining what each topic IS plus its practical applications), and draft semester plans interactively. Use when: user mentions 'lehrplan', asks to 'prepare a teaching repo', 'check the Lehrplan for new Novellen', 'RIS sync', 'Lehrplan extrahieren', 'Jahrespläne neu ziehen', 'Semesterplan erstellen/überarbeiten', 'Erläuterungen ergänzen', or mentions Unterrichtsvorbereitung on a repo following the lehrplan/ convention."
license: MIT
compatibility: opencode
metadata:
  category: education
  scope: ris-curriculum
  output: lehrplan-extracts
---

# Lehrplan Skill

Reverse-engineered from the GRG-PMM teaching repository (HTL Spengergasse).
This skill is **convention-based, not project-hardwired**: it works in any
teaching repo that follows the `lehrplan/` convention described below.

The skill has three main tasks plus an identification preamble:

| Task | Purpose |
|------|---------|
| **A** — Gegenstand & Ausbildungszweig identifizieren | Always-on preamble: read the repo, report legal basis, check conformity |
| **1** — Gesetzesmaterial beschaffen | Fetch the legal curriculum for an Ausbildungszweig from RIS, Novellen-Check |
| **2** — Fach-Extraktion | Extract one subject's Lehrplan from the law, with Erläuterungen |
| **3** — Semesterplan | Interactively draft a semester plan from the extracted Lehrpläne |

The signature extension of this skill is the **Erläuterungs-Ebene**: for every
Lernziel (and especially in semester plans), a substantive German explanation
of what the topic actually **is** — Begriffserklärung first, integrated
Anwendungs- und Berufsbezug second. See "Qualitätskriterien für
Erläuterungen" below.

## Output Language: MANDATORY GERMAN

All generated files (extracts, METADATA.md sections, semester plans, reports)
MUST be written in natural German with proper UTF-8 umlauts (ä, ö, ü, ß).
Never use English for file content. Legal quotations must be copied verbatim
from RIS content.

## Repo Conventions

> **⛔ VERBINDLICHES ZIEL-AYOUT — NICHT NUR EMPFEHLSAM.**
> Das oben gezeigte Standard-Layout ist der **verbindliche Zielzustand** jedes
> Teaching-Repos. Wann immer eine Session auf ein Repo trifft, das davon abweicht
> (z. B. Lehrplan-Dateien unter `docs/lehrplan/`, Klassenordner oder
> `kompetenzmodule/` im Repo-Root, `jgN-einheiten.md`-Sammeldateien), gilt:
> **migrieren, nicht dulden.** Der Konformitäts-Check (Task A) behandelt jede
> solche Abweichung als Befund mit Migrationspflicht; nur eine explizite,
> dokumentierte Nutzer-Entscheidung (DECISIONS-Eintrag) kann eine Ausnahme
> rechtfertigen. **Einzige erlaubte Abweichung** bleibt das dreischichtige
> `<gegenstand>-lehrplan-text.md` als *Dateiformat* (② Schuladaption und ③
> Didaktik mitlegen) — die **Ablage** unter `lehrplan/` ist davon nicht
> berührt und bleibt Pflicht.

A teaching repo following this convention looks like:

```
lehrplan/
  <KLASSE>/                      # generic class label, UPPERCASE (e.g. 4HWIT, 5HWIT)
    <KLASSE>.lehrplan.md         # class-relevant curriculum extract (year-wise)
    README.md                    # class folder overview
    semesterplan-ws.md           # winter semester plan (interactively drafted, Task 3)
    semesterplan-ss.md           # summer semester plan (interactively drafted, Task 3)
    NN-slug/                     # lesson folder during preparation
    YYYY-MM-DD_thema/            # lesson folder once the teaching date is fixed
    assets/                      # shared styles, images
  kompetenzmodule/               # didactic KM-Steckbriefe: km<N>.md + README.md
  METADATA.md                    # legal basis, RIS references, amendment history,
                                  # school-autonomy notes, class mapping, file inventory
  <gegenstand>-lehrplan-text.md  # COMPLETE curriculum extract, all Jahrgänge
  RIS/                           # law-text PDFs ONLY (Rechtsinformationssystem)
    YYYY-MM-DD_<name>.pdf        # RIS PDFs, ISO-date prefixed
AGENTS.md                        # repo-level agent guidelines
GLOSSAR.md                       # domain abbreviations and terms
```

Folder naming rules:

- Class folders: `<Stufe><Postfix>` in **UPPERCASE** (e.g. `4HWIT`).
  Generic labels cover parallel classes (`4HWIT` covers 4AHWIT/4BHWIT).
- Lesson folders: `NN-slug/` during preparation, renamed to
  `YYYY-MM-DD_slug/` when the teaching date is fixed.
- RIS folder: `lehrplan/RIS/` — uppercase exception (abbreviation, like
  class labels); holds ONLY RIS law-text PDFs.
- PDFs: `RIS/YYYY-MM-DD_<name>.pdf` (ISO 8601 date prefix).
- Lowercase with hyphens for all multi-word file and folder names.

## Class Mapping (MANUALLY MAINTAINED)

The skill carries this subject → class-postfix table. **Never extend or
modify it on your own.** If a repo uses a subject that is missing here,
report it to the user and propose an entry — but let the user edit this
skill file themselves.

| Gegenstand | Klassen-Postfix(e) |
|------------|--------------------|
| PMM        | HWIT               |
| INFI       | HWII               |
| WMC        | AIF, KIF, CIF      |

How the mapping works:

- Class folders are `<Stufe><Postfix>` (e.g. `4HWIT`, `5HWIT`; for WMC e.g.
  `4KIF`, `5KIF`).
- The `Stufe` (digit) comes from the Jahrgang in which the subject is taught
  per the legal curriculum (see METADATA.md / Fachgegenstände table).
- **Identify class folders generically**: any directory under `lehrplan/`
  matching `<digit><known-postfix>` is a class folder. Do not rely on a
  hardcoded list of full class names.

## Spengergasse-Klassen-Decoder (Abendform, Berufstätige-Formen)

Verifiziertes Wissen zu den Klassenkürzeln der HTL Spengergasse (Erwachsenenbildung,
stand 2026-09-06, Quelle: Schul-Website „Informatik – Abendform" + Lehrer-Angabe):

**Code-Schema:** `<Semester><Form-Serie>IF` — die Ziffer ist das Semester,
**ungerade = WS, gerade = SS** (z. B. `3AIF` WS → `4AIF` SS; `5KIF` WS → `6KIF` SS).

| Form-Serie | Form | Dauer | Einstieg | Abschluss |
|------------|------|-------|----------|-----------|
| `AIF` | Aufbaulehrgang | 7 Semester | ohne Reifeprüfung (Vorbereitungslehrgang, Fachschule, facheinschlägiger Lehrabschluss) | **Reife- und Diplomprüfung** (Diplom + Matura) |
| `KIF` | Kolleg | 6 Semester | Reifeprüfung / Berufsreifeprüfung / Studienberechtigungsprüfung → Matura bereits vorhanden | **Diplomprüfung** (nur Diplom) |
| `CIF` | zweite Kolleg-Variante | 6 Semester | Matura bereits vorhanden | Diplomprüfung (nur Diplom); **C = Zweig, dessen Unterricht erst ab 17:10 beginnt** |

- Praxiscodes der Kohorten tragen ein **Zug-Präfix** (A/B/C) auf dem Form-Code:
  `4AAIF` (Zug A, AIF), `4AKIF` (Zug A, KIF), `4BKIF` (Zug B, KIF), `4CAIF` (CIF).
- Ein Schuljahrgang kann mehrere Form-Serien parallel bedienen (z. B. Jahr 1 in
  `34AIF` + `34KIF` + `34CIF`); die Klassenordner sind dann **Block-Ordner** für
  semestrierte Berufstätigen-Formen: `<Sem3Sem4><Form>` (`34AIF`, `34KIF`,
  `34CIF`, `56KIF`) statt Stufen-Notation — die PMM-Stufen-Notation (`4HWIT`)
  bleibt für Tagesschul-Formen das Gegenmodell.
- WMC/Informatik-Sonderformen: Rechtsgrundlage BGBl. II Nr. 368/2022
  (Anlagen 1 + 1.9, Varianten I.3/I.4); Referenz-Raster Anlage 1.10
  (262/2015 idF 383/2021). **Achtung:** der signed 383/2021-PDF enthält nur den
  VO-Text — der Anlagen-Wortlaut steht im BgblAuth-**COO-HTML** (konsolidierte
  Einzel-Anlage, fetchbar).
- Erlaubte Konventions-Abweichung: ein **dreischichtiges `LEHRPLAN.md`** statt
  `<gegenstand>-lehrplan-text.md`, wenn ② Schuladaption und ③ Didaktik mitlegen.
- Schul-Websites schreiben pauschal „Abschluss: Diplomprüfung" — die
  Matura-Logik der Formen steht in der **Einstiegsvarianten-Tabelle**, nicht in
  der Abschlusszeile.

## Ausbildungszweig-Konzept

Task 1 operates at the **Ausbildungszweig** level (e.g. WII, WIT, KIF), not at
the subject level. The legal hierarchy is:

```
Ausbildungszweig (z. B. WII, WIT, KIF)
  → Rechtsgrundlage: BGBl.-Verordnung mit Anlagen (z. B. BGBl. II Nr. 262/2015)
    → Anlage(n): das Gesetz publiziert die Unterrichtsfächer eines
      Ausbildungszweigs MEIST GEMEINSAM in EINEM Dokument (e.g. Anlage 1.28
      covers ALL subjects of the WIT Zweig)
    → Variiert: manche Zweige/Fächer haben eigene Anlagen (e.g. WMC:
      Anlage 1.9 aus BGBl. II Nr. 368/2022 statt der WIT-Sammelanlage)
      → einzelne Fächer (Abschnitte der Anlage)
```

Consequences for the skill:

- **Task 1 (Beschaffung)** targets the Zweig's document(s). Expect one shared
  Anlage per Zweig as the normal case; detect and report separate Anlagen
  when they exist. The METADATA.md of a repo stores which Anlage covers the
  repo's subject.
- **Task 2 (Extraktion)** always extracts ONE subject (one Abschnitt) from
  the Zweig document — never the whole Zweig.
- The fetch strategy remains Anlage-based (NOR document per Anlage, see
  RIS-Praxiswissen) — a Zweig document is fetched once and serves all its
  subjects.

## Workflow Overview

| Task | Mode | Trigger examples |
|------|------|------------------|
| A — Gegenstand & Ausbildungszweig identifizieren | Standard (always on invocation) | "Unterricht", "Vorbereitung prüfen" |
| 1 — Gesetzesmaterial beschaffen (Zweig) | On-demand | "Lehrplan auf Novellen prüfen", "RIS sync", "Gesetzesmaterial holen" |
| 2 — Fach-Extraktion mit Erläuterungen | On-demand | "Lehrplan extrahieren", "Jahrespläne neu ziehen", "Erläuterungen ergänzen" |
| 3 — Semesterplan (interaktiv) | On-demand | "Semesterplan erstellen", "Semesterplan überarbeiten" |

Before running Task 1, 2 or 3, display a short plan (what will be fetched,
compared, written) and proceed. For write-heavy steps, confirm with the
user if the plan deviates from what they asked for.

## Task A — Gegenstand & Ausbildungszweig identifizieren

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
- **Ausbildungszweig**: which Zweig the repo's subject belongs to (e.g.
  WIT for PMM), and which Anlage covers it — shared with other subjects
  or its own (see Ausbildungszweig-Konzept).
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
| RIS-Verzeichnis | All law-text PDFs stored under `lehrplan/RIS/` — PDFs in the `lehrplan/` root are a migration finding |
| Erläuterungen | KM-Überblicke and Lernziel-Erläuterungen present in all extracts (see Task 2) |
| Semesterpläne | `semesterplan-ws.md`/`semesterplan-ss.md` present for every active class, covering the current KMs |

Then state explicitly: **"Der Skill muss noch ausgeführt werden"** (list
which Tasks 1/2/3 remain) **oder "Der Skill ist vollständig ausgeführt"**.

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
<!-- | Datei (RIS-PDFs als `RIS/<name>.pdf`) | Herkunft | Beschreibung | -->
```

## Task 1 (on-demand) — Gesetzesmaterial beschaffen (Ausbildungszweig)

Purpose: ensure the repo fully mirrors the law in force for the subject's
Ausbildungszweig, and that no legislative amendment from the **last 12
months** was missed.

Protocol:

1. **Read stored state** from `lehrplan/METADATA.md`: Gesetzesnummer of the
   konsolidierte Fassung, RIS links (especially the Anlage NOR link),
   amendment history table, PDF inventory.
2. **Novellen-Check (last 12 months)** — use the NOR-Kopf method (see
   "RIS-Praxiswissen" below; **never** `webfetch` the `GeltendeFassung.wxe`
   page — it contains the whole Lehrplanpaket, exceeds the fetch limit and
   fails):
   - `curl` the **NOR document of the Zweig's Anlage** (link in
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
     of the Zweig are affected, whether the subject's Lehrstoff (the
     Anlage's subject Abschnitt) is touched.
   - Store the PDF into `lehrplan/RIS/` as
     `YYYY-MM-DD_BGBl-II-<Nr>_Novelle-<slug>.pdf` (Kundmachungsdatum).
   - Update METADATA.md: RIS-Verweise (Novelle ELI link), Änderungshistorie
     (append a row: Kundmachungsdatum, Novelle + Inkrafttreten, Betrifft),
     file inventory, plus the evidence line "RIS-Status abgefragt am …".
   - Flag Task 2 (re-extraction) as required **only if the subject's
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

## Task 2 (on-demand) — Fach-Extraktion mit Erläuterungen

Purpose: turn the legal text into human-readable Markdown layers — the
verbatim law plus the Erläuterungs-Ebene (what each topic actually is).

1. **Source**: extract the text from the RIS HTML of the Zweig's Anlage
   (preferred: current konsolidierte Fassung link in METADATA.md) or from
   the stored PDF. Quote only fetched content — never reconstruct legal
   text from memory.
2. **Complete extract** — `lehrplan/<gegenstand>-lehrplan-text.md`:
   - All Jahrgänge of the subject, in order (I.–V. Jahrgang).
   - Structure: `## <Jahrgang>` → `### <Semester> — Kompetenzmodul <N>`
     → `#### Bildungs- und Lehraufgabe` → `#### Lehrstoff`.
   - **Erläuterungs-Ebene (mandatory)**, see "Qualitätskriterien für
     Erläuterungen":
     - **KM-Überblick**: directly under each `### <Semester> — Kompetenzmodul
       <N>` heading, a short introductory description as annotation
       (`> **Überblick:** …`) — worum geht es in diesem Kompetenzmodul
       insgesamt.
     - **Lernziel-Erläuterungen**: directly under **each Lernziel bullet**
       of the Bildungs- und Lehraufgabe, an inline annotation
       (`> **Erläuterung:** …`) explaining what the topic IS.
     - **Lehrstoff-Erläuterungen**: one annotation (`> **Erläuterung:** …`)
       per Lehrstoff-Bereich (Lehrstoff is compressed prose — one
       Erläuterung per Bereich, not per fragment).
   - Annotate milestones (e.g. "III. Jahrgang — Statistik beginnt hier")
     if present in the source, marked clearly as annotations.
   - Reference header: legal basis, RIS link, extraction date.
3. **Class-wise extracts** — one per class folder:
   - Target: `lehrplan/<KLASSE>/<KLASSE>.lehrplan.md` (e.g.
     `lehrplan/4HWIT/4HWIT.lehrplan.md`).
   - Content: **only** the class-relevant Jahrgang (e.g. IV. Jahrgang =
     KM 7+KM 8 for a 4th-year class), i.e. Bildungs- und Lehraufgabe +
     Lehrstoff of its Kompetenzmodule — **including the full
     Erläuterungs-Ebene** (KM-Überblicke, Lernziel- und Lehrstoff-
     Erläuterungen).
   - Header: class name ↔ Jahrgang ↔ Kompetenzmodule mapping, legal basis,
     extraction date.
   - The Jahrgang ↔ KM mapping comes from METADATA.md.
4. **Klassennamen in den Lehrplan aufnehmen:** ensure the Klassen-Zuordnung
   table in METADATA.md maps every Jahrgang taught to its UPPERCASE class
   name(s). Add missing rows; never remove rows without user confirmation.
5. **Preserve manual annotations:** if an extract file already exists, read
   it first. Re-extraction must not silently drop human annotations
   (highlights, cross-references) **or existing Erläuterungen**. Rebuild
   the legal text, then re-apply, regenerate or flag affected annotations
   and Erläuterungen — never silently delete a human-authored Erläuterung;
   when in doubt, keep it and flag it for review.
6. Report: files written, Jahrgänge covered, any annotations or
   Erläuterungen that need manual re-check.

## Task 3 (on-demand) — Semesterplan (interaktives Protokoll)

Purpose: turn the extracted Lehrpläne into a concrete semester plan
(`semesterplan-ws.md` / `semesterplan-ss.md`). This is an **interactive
protocol**: the skill drafts, the user decides. Never write a final
semester plan without the user review step.

Protocol:

1. **Input-Check** (all must exist; if not, point to the missing Task 1/2
   outputs and stop):
   - Class extract `lehrplan/<KLASSE>/<KLASSE>.lehrplan.md` with
     Erläuterungs-Ebene (the content backbone).
   - KM-Steckbriefe `lehrplan/kompetenzmodule/km<N>.md` (read for context).
   - Zeitmodell from `lehrplan/METADATA.md` (Wochenstunden/Doppelstunden
     pro Semester — determines the number of UE).
   - Ressourcen-Matrix (e.g. `lehrplan/ressourcen-matrix.md`), if present —
     for Lektüre-Anker.
2. **UE-Grid-Entwurf**: map the KM content (Lernziele + Lehrstoff) onto UE
   blocks according to the Zeitmodell (real UE + reserved DS for tests/
   admin). Present the draft as a compact table (UE | Thema |
   KM/Lernziel-Bezug | geplante Lektüre-Anker). State assumptions
   explicitly (Vorwissen from earlier KMs, sequencing choices).
3. **User-Review (Pflictschritt)**: present the draft and ask for
   confirmation/adjustments — sequencing, Schwerpunkte, reserved slots.
   Do not proceed before the user has reviewed the grid.
4. **Ausarbeitung**: write `lehrplan/<KLASSE>/semesterplan-ws.md` or
   `semesterplan-ss.md`, following the repo's existing semester plan
   format (UE tables grouped by thematic blocks, header with Zeitmodell,
   Werkzeug, KM-Steckbrief and Ressourcen-Anker references, reserved DS
   and Schwerpunkte summary at the end).
   - **Per UE-Themenblock: eine inhaltliche Beschreibung** — a short
     Erläuterung paragraph (or annotated table rows) per thematic block /
     UE: what the topic IS, with integrated Anwendungs- und Berufsbezug
     (see "Qualitätskriterien für Erläuterungen"). Especially here the
     Erläuterungen must be substantial — this is the layer teachers
     actually teach from.
5. **Preserve manual content**: if a semester plan already exists, read it
   first. Reworking must not silently drop existing content (UE folders,
   annotations, didactic notes). Show a diff-like summary of what changed.
6. **Iteration**: offer follow-up adjustments (resequencing, swapping
   Lektüre-Anker, adding reserve UE). The user decides when the plan is
   final.

## Qualitätskriterien für Erläuterungen

Shared rules for every Erläuterung (Task 2 extracts and Task 3 semester
plans). An Erläuterung answers first and foremost: **"Was ist das
eigentlich? Worum geht es?"**

1. **Begriffserklärung (Kern, Hauptanteil):** Was ist das Thema inhaltlich?
   Grundidee, zentrale Konzepte, Methoden — verständlich auf Deutsch
   beschrieben. Not a mere restatement of the legal text: unpack the
   terminology.
2. **Anwendungs- und Berufsbezug (integrierter Bestandteil):** konkrete
   Einsatzmöglichkeiten im Beruf (real, specific — e.g. „Annahmeprüfung →
   Wareneingangskontrolle nach ISO 2859 in der Fertigung"). Integrated
   into the explanation, not a bolted-on list.
3. **Alltagsbezug und Querverweise (optional, wenn sinnvoll):** wo das
   Thema im Alltag begegnet; Anknüpfungspunkte zu anderen Kompetenzmodulen,
   Fächern oder späteren Jahrgängen.

Rules:

- **Länge:** 3–7 Sätze sind die Norm; bei bedürftigem Thema darf es gern
  mehr sein — lieber ausführlich als knapp. No rigid 2–4-sentence template.
- **German, substantive:** keine generischen Floskeln („wichtiges Thema",
  „in vielen Bereichen relevant"). Every sentence must carry content.
- **Never mix with legal text:** Erläuterungen are ALWAYS clearly marked as
  annotations (Blockquote with `**Überblick:**` / `**Erläuterung:**`).
  The verbatim law stays untouched and unmarked.
- **Human-authored Erläuterungen outrank generated ones:** on re-runs,
  preserve them (see Task 2, step 5).

## RIS-Praxiswissen (projektübergreifend)

Generic, subject-independent knowledge about fetching from
ris.bka.gv.at. Accumulated from real Task 1/2 runs. **Persist-back rule:
after every Task 1/2, move any newly learned generic RIS pattern into this
section** (skill-level knowledge persistence — this knowledge is not
project-specific and must not stay trapped in a repo's docs).

### Fetch-Strategien

- **Never** `webfetch` the `GeltendeFassung.wxe` page (Gesetzesnummer URL)
  — for Lehrplanpakete it returns the *entire* package (all Anlagen,
  often > 5 MB) and exceeds the webfetch limit. Use `curl` + local parsing
  instead.
- **Autorisierender Ein-Zeilen-Novellen-Check:** `curl` the **NOR document
  of the Zweig's Anlage** (link stored in METADATA.md). Its
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
    `Anlage <N.N>` / subject keywords to find which §§ touch the
    subject's Anlage.
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

- RIS-PDFs go to `lehrplan/RIS/YYYY-MM-DD_<name>.pdf` with the
  **Kundmachungsdatum** (fetch date is irrelevant — the prefix dates the
  legal text). Novellen: `lehrplan/RIS/YYYY-MM-DD_BGBl-II-<Nr>_Novelle-<slug>.pdf`.
- The `lehrplan/` root stays clean: law-text PDFs in the `lehrplan/` root
  are a Konformitäts-Check finding with migration duty.
- Other (non-RIS) reference PDFs are **not** subject to the date-prefix
  convention and never go into `lehrplan/RIS/`.

### Ausgabe in METADATA.md

- Record every RIS query in METADATA.md: „RIS-Status abgefragt am
  YYYY-MM-DD: … zuletzt geändert durch …" as evidence line under the
  Änderungshistorie.
- Never attribute an amendment to a BGBl. number without fetching it —
  plausible-looking pairs (date + number) can be wrong (e.g. BGBl. II Nr.
  74/2017 = IngG-Fachrichtungsverordnung, has nothing to do with the HTL
  Lehrplanpaket).

## Explicit Out of Scope

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
- **Erläuterungen are always clearly marked as annotations** (Blockquote
  with `**Überblick:**` / `**Erläuterung:**`) — legal text and didactic
  explanation must never visually merge.
- Date-prefix RIS law-text PDFs with ISO 8601 Kundmachungsdatum; other
  reference PDFs are exempt.
- Show a plan before writing files; confirm before deviating from the
  requested scope.
- Task 3 never writes a final semester plan without the user review step
  (Pflictschritt).
- The class mapping table in this skill is manually maintained — propose,
  never auto-edit.
- UPPERCASE class names everywhere (folders, extract files, METADATA.md).
