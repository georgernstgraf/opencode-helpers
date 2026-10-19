---
name: knowledge-exam
description: Generate German knowledge-check exams and solution files from the taught material (class Git history + WebUntis Lehrstoff)
license: MIT
compatibility: opencode
metadata:
  category: education
  output: exam
---

# Knowledge Exam Skill

## Purpose

This skill creates a German knowledge-check exam for a specific class folder
based on the taught material (class Git history, cohort directories and the
WebUntis Lehrstoff record). Use it when asked to generate a mini-exam from the
material covered in class.

## Output Language: MANDATORY GERMAN

The generated exam and solution files MUST be written in natural German with 
proper UTF-8 umlauts (ä, ö, ü, ß). 
Never use English for the exam questions or solutions.

## Target Repository: the private `-T` exam repo (MANDATORY)

Knowledge-check exam and solution files must be written into the teacher's
**private test/exam repository** — the sibling repo named `<subject>-T`
(e.g. `GRG-PMM-T` for `GRG-PMM`). **Never write them into the public
teaching repo.**

Before generating files:

1. Locate the `-T` repo on disk (typically `~/repos/<owner>/<subject>-T`);
   if it does not exist, stop and ask the user.
2. Verify it is up to date (`git fetch && git status -sb`).
3. Read the target repo's `AGENTS.md` — it defines repo-specific conventions:
   file naming (`knowledge_<klasse>_<date>.md` + `_solutions.md`), class
   folder layout (flat vs. dated subfolder, cohort suffixes like `4ahwit-x`),
   and the formelle Anrede rule (Du vs. Sie per class).

Additional rules (discovered in practice):

- **Prüfungs-Angaben gehören IMMER ins `-T`-Repo** — Knowledge-Checks, PLFs
  und sonstige Prüfungsangaben, niemals ins öffentliche Teaching-Repo.
  HÜ-/Aufgaben-Dateien (`Aufgabe.md` im Klassenordner) sind *keine*
  Prüfungs-Angaben: sie bleiben im Teaching-Repo, damit Schüler:innen sie
  per Clone erreichen (homework-Workflow).
- **Fehlender Kohorten-Ordner im `-T`-Repo ist normal** bei Semesterstart
  (neues SJ: alte `4aaif/`-artige Ordner liegen noch flach im Root, die
  neuen `3aaif/` etc. existieren noch nicht). In diesem Fall den Ordner
  nach den `-T`-AGENTS.md-Konventionen anlegen — nicht abbrechen.
- **Der Zug ist im Klassennamen kodiert** (`3aaif` vs. `3caif`, bzw.
  `3ahwii`-artige Kürzel) — keine künstlichen Zusatz-Suffixe erfinden
  (`-x`, `-a` o. ä.), außer das `-T`-AGENTS.md verlangt sie explizit
  (z. B. bei mehreren parallelen Gruppen derselben Klasse).

## Inputs

- `class`: target class folder name.
- `fach`: (optional) WebUntis-Fachkürzel für den Lehrstoff-Abgleich, z. B.
  `WMC_1`. Wird es weggelassen, über `wu klasse <KLASSE> --details` auflösen
  (Suche nach dem eigenen Fach); schlägt das fehl, ohne WebUntis weiterarbeiten.
- `weeks`: (optional) Begrenzung der Git-Historie des Kohorten-Ordners als
  Zeitanker (Schritt 3); der Prüf-Umfang kommt primär aus WebUntis-Lehrstoff
  und Kohorten-READMEs.
- `exam-date`: (mandatory) the planned exam date, must be either:
  - An ISO date (YYYY-MM-DD format).
  - The literal `today`.
  - The literal `tomorrow`.
- `mc-count`: (optional) number of multiple-choice questions, default 10.
- `free-count`: (optional) number of free-text questions, default 3.

## Protocol

### 1. Validate Inputs

- **Mandatory exam-date parameter**: If `exam-date` is not provided, abort
  immediately with an error message explaining that this parameter is required.
- Confirm that a folder matching `class` exists in the **target `-T`
  repository** (see "Target Repository" section above), not in the teaching
  repo. If the folder does not exist, it may need to be created there —
  check the repo's AGENTS.md conventions first.
- If the `-T` repo cannot be located, stop and ask the user. If only the
  **class folder** is missing, that is normal at semester start — create it
  (see "Target Repository" above), do not abort.
- **Resolve exam-date to ISO format**:
  - If `exam-date` is an ISO date (YYYY-MM-DD), use it as-is.
  - If `exam-date` is `today`, compute today's ISO date.
  - If `exam-date` is `tomorrow`, compute tomorrow's ISO date.
  - Store this resolved date as `<isodate>` for output filenames.

### 2. Resolve Question Counts

- Default values: 10 multiple-choice questions, 3 free-text questions.
- If `mc-count` is not provided, set `mc-count = 10`.
- If `free-count` is not provided, set `free-count = 3`.
- If neither `mc-count` nor `free-count` was provided by the user:
  - Before generating, ask the user: "Sollen 10 MC-Fragen und 3 Freitext-Fragen generiert werden? (j/n)"
  - If the user confirms, proceed with defaults.
  - If the user declines, ask for specific counts before continuing.
- Do NOT ask for confirmation when at least one count was explicitly provided.

### 3. Stoffbasis: Kohorten-Dir, Lessons & WebUntis-Abgleich

Der Prüf-Umfang ist definiert durch **was tatsächlich unterrichtet wurde** —
nicht durch den Semesterplan. Drei Quellen, in dieser Reihenfolge gewichtet:

1. **WebUntis (Authoritäts-Quelle):** `wu lesson <KLASSE>/<FACH> termine
   --mit-lehrstoff` (z. B. `wu lesson 3AAIF/WMC_1 termine --mit-lehrstoff`)
   liefert alle Termine mit eingetragenem Lehrstoff. Achtung: bei langen
   Listen großzügigen Timeout setzen. Der Lehrstoff **fence**t den Prüf-Umfang:
   Fragen dürfen nichts abdecken, was dort nie aufgetaucht ist (z. B. Formulare
   in 3caif ja, in 3aaif nein — Stoffstand strikt kohorenscharf).
2. **Kohorten-Dir im Teaching-Repo:** datierte Tagesordner
   (`YYYY-MM-DD[_]thema/`) mit READMEs, Lesson-Dateien, Demos und
   Aufgabe-Dateien. Die READMEs spiegeln den realen Stoffstand inkl.
   Abgaben und Ausnahmen.
3. **Referenzierte Materialien:** Prepared Lessons (`unterricht/<PREFIX>-NN-*`),
   Beispielprojekte und Unterlagen, soweit sie von den Kohorten-READMEs
   verlinkt sind — dort steht die Stofftiefe für Detailfragen.

Ergänzend: Git-Historie des Kohorten-Ordners als Zeitanker
(`git log --since=<start> -- <kohorte>`), um den unterrichteten Zeitraum
abzugrenzen. Minimal-Commits sind Stunden-Anker, keine vollständige Abdeckung.

- Taucht bei erledigten Terminen **kein Lehrstoff** auf (Status „offen"),
  dem User melden; `wu lesson … lehrstoff eintragen` nur auf expliziten
  Wunsch (Text via `--text-datei` wegen Umlauten, beide parallelen
  Termin-IDs je Datum beschreiben, vorher `--testlauf`).
- **Mehrere Kohorten gleichzeitig?** Pro Kohorte einen eigenen Subagenten
  mit identischem Format-Spec spawnen (parallel) und danach zentral
  gegenlesen.

### 4. Generate Exam Files

- Create `knowledge_<class>_<isodate>.md` inside the class folder.
- Include exactly `mc-count` multiple-choice questions.
- Each multiple-choice question must have exactly 4 answer options.
- Each multiple-choice question is worth 4 points total.
- Make the questions as unambiguous as possible, put enough context in.
- Score multiple-choice questions per option: award 1 point for each option that
  is handled correctly, whether it was correctly checked or correctly left
  blank.
- For every multiple-choice question, explicitly allow students to mark `-`
  and briefly explain why they consider the answer ambiguous or
  context-dependent.
- Include exactly `free-count` free-form questions.
- Each free-form question is worth 15 points.
- Put a friendly "Gutes Gelingen" footer at the bottom.

### 5. Generate Solution File

- Create `knowledge_<class>_<isodate>_solutions.md` in the same folder.
- Keep the student-facing exam and the solution file separate.
- Do not include the solutions in the student-facing exam file.
- Solution layout per MC question: which options are correct (z. B.
  „Richtig: a ☑, b ☑, c ☐, d ☑") **plus** ein Satz Begründung je Option —
  die Markierungen müssen mit den Erklärungen übereinstimmen (Abweichung
  zwischen Header-Zeile und ✔/✘-Erklärungen war schon ein echter Fehler).
- Solution layout per free-form question: Musterlösung + Wertungs-Skizze,
  deren Teilschritte **exakt** auf die Frage-Punkte (Standard 15 P) summieren.
- The solution file is teacher-facing: kein Schüler-Footer (Name/Datum-Felder,
  „Gutes Gelingen") am Ende.

### 6. Quality Gate (vor der Übergabe, Pflicht)

Vor der Ablieferung beide Dateien systematisch prüfen — jedes dieser
Kriterien ist in der Praxis schon verletzt worden:

- **Rater-Sicherheit:** Option a) darf nicht (fast) immer die richtige sein.
  Bei erkennbaren Mustern rotieren: wahre Option mit einer falschen Position
  tauschen (Text wandert, Lösungsmarkierung wandert mit). Faustregel: blindes
  Ankreuzen (z. B. „immer a+b+c") darf nicht mehr als ~70 % bringen.
  Falsche Optionen über die Positionen a–d verteilen, nicht geballt auf d).
  Die Anzahl korrekter Optionen je Frage mischen (nicht alle Fragen mit
  „3 richtige").
- **Wertung:** MC = 4 P; Summen der Freitext-Wertungs-Skizzen = Frage-Punkte;
  Gesamtpunkte in Header und Footer identisch.
- **Konsistenz Exam↔Solutions:** Fragennummerierung, Titel, Reihenfolge und
  Optionentexte deckungsgleich; Markierungen passend zur Option-Reihenfolge
  (skriptbasiert prüfbar).
- **Keine Duplikate:** derselbe Fakt (oder dieselbe Rechnung mit denselben
  Zahlen) nicht doppelt prüfen — weder MC↔MC noch MC↔Freitext.
- **Sprache:** durchgehend Du/Sie laut `-T`-AGENTS.md, echte Umlaute,
  kein Englisch in Fragen; Fachbegriffe nur, wenn sie unterrichtet wurden
  (z. B. einen unbehandelten Spec-Term vermeiden und das Verhalten stattdessen
  als beobachtbares Ergebnis abfragen).

### 7. Constraints

- Do not commit any generated files, EVER. The teacher will add them manually
  after the exam is over.
- Preserve existing files unless the task explicitly requires replacement.
- Write both generated Markdown files in German.
- UTF-8 is explicitly allowed and preferred in generated Markdown files.
- Do not replace German umlauts with transliterations such as `ae`, `oe`, or
  `ue` unless the surrounding source material explicitly requires that form.

## Output Expectations

- Student exam file in German with the required question counts and scoring.
- Separate teacher solution file in German.
- Filenames must include the class name and the exam date in ISO format
  (resolved from the mandatory `exam-date` parameter).
