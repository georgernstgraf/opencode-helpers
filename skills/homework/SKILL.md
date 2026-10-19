---
name: homework
description: Generate per-lesson assignment files (Aufgabe.md) from recent class Git history and teaching material, and keep the canonical assignment list in the cohort README current
license: MIT
compatibility: opencode
metadata:
  category: education
  output: assignment-file
---

# Homework Skill (Aufgaben)

## Purpose

This skill generates a per-lesson `Aufgabe.md` assignment file inside the
current lesson directory of a class folder and keeps the **canonical
assignment list** in the cohort README current (retrofit). The user invokes it
from inside the class folder (e.g., `~/repos/2ahwii/`) at the end of a lesson.
No arguments are needed.

## Terminology (CRITICAL)

- The canonical term is **Aufgabe** (plural: Aufgaben). Files, sections, and
  user-visible text use "Aufgabe" — never "Hausübung", "HÜ", or "homework".
- **Übung** is NOT an Aufgabe: Übungen (e.g. "Jetzt du!") are in-class
  Mitarbeits-Elemente and are never written as assignments.
- `Hausübung.md` / `Hausübungen.md` are legacy artifacts from earlier school
  years. This skill never creates them; it recognizes and preserves them
  when encountered.

## Output Language: MANDATORY GERMAN

The generated content inside `Aufgabe.md` MUST be written in natural German
with proper UTF-8 umlauts (ä, ö, ü, ß). Never use English for the assignment
descriptions.

## Invocation Context

- The user sits inside a class folder that is part of a Git repository.
- The class folder contains lesson directories named `<ISO-date>_<topic>`
  (e.g., `2026-03-21_promises`, `2026-04-01_async-await`).
- The skill auto-detects the current lesson directory from recent Git activity.
- No slash command is required. The user tells the agent to "generate
  homework" / "Aufgabe generieren" or similar, and the agent loads this skill
  directly.

## Protocol

### 0. Kohorten-Auflösung (Multi-Kohorten-Modus)

Wird der Skill für mehrere Kohorten auf einmal gerufen, identifiziert der
User die Kohorten meist per **WebUntis-Lesson-ID** (Tool `wu`, Repo
`webuntis-cli`): `<KLASSE>/<FACH>` — z. B. `3AHWII/SWP1x`, `4AHWIT/PMMx`,
`3AHWII/INFIx`, `3AAIF/WMC_1`, `5AHWIT/PMM`. Auflösung in Repo +
Klassenordner (Stand 2026-10-12, vor Ausführung mit `wu klasse <ID> faecher`
verifizieren — Fächerkürzel ändern sich mit dem Schuljahr):

| WebUntis-ID | Fach-Repo (in `georgernstgraf/`) | Klassenordner |
|---|---|---|
| `3AHWII/SWP1x` | `GRG-SWP` | `3ahwii/` |
| `3AHWII/INFIx` | `GRG-INFI` | `3ahwii/` |
| `4AHWIT/PMMx` / `PMMy` | `GRG-PMM` | `4ahwit-x/` / `4ahwit-y/` |
| `5AHWIT/PMM` | `GRG-PMM` | `5ahwit/` |
| `3AAIF/WMC_1` / `3CAIF/WMC_1` | `GRG-WMC` | `3aaif/` / `3caif/` |

Regeln für den Multi-Kohorten-Lauf:
- Der Discovery-Zeitfenster-Check (24 h) gilt pro Kohorte **relativ**:
  liegen die letzten Stunden länger zurück, ist die **jüngste datierte
  Lesson** das Target; bei Mehrdeutigkeit den User fragen.
- Die Aufgabe liegt nicht immer im Kohortenordner: Tages-READMEs (`## HÜ`,
  `## Aufgabe`), Kohorten-README-Verlauf und Prepared Lessons
  (`unterricht/<PREFIX>-<NN>-<slug>/hausaufgabe.md`) sind gleichwertige
  Evidenzquellen. Existiert zur Lesson kein Datumsordner, entweder einen
  anlegen (nur bei klarer Evidenz) oder den README-Eintrag direkt auf die
  Prepared Lesson zeigen lassen (Vorbild: `GRG-WMC/3aaif/README.md`).
- Kein Duplizieren kanonischer Aufgabentexte: liegt die Aufgabe bereits
  kanonisch in `unterricht/`, genügt der Index-Eintrag mit Link.

### 1. Discover Current Lesson Directory

- Run `git log --since="24 hours ago" --name-only --diff-filter=A` and
  `git diff --name-only` to find recently created or modified directories.
- Look for directories matching the pattern `<YYYY-MM-DD>_<topic>`.
- Select the most recently created or modified matching directory.
- If no matching directory is found, check for uncommitted directories with
  the same pattern.
- If multiple candidates exist or none is found, list the candidates and ask
  the user which lesson directory to target.

### 2. Discover Sources

- Read all files inside the identified lesson directory: `README.md`, code
  examples, exercise sheets, and any other content files.
- **Reference pattern**: if the lesson `README.md` contains an `## Aufgabe`
  section that is a REFERENCE to a prepared lesson (a lesson id matching
  `<PREFIX>-<NN>-<slug>` and/or a link into `unterricht/`), resolve it:
  read the prepared lesson folder
  `<repo-root>/unterricht/<PREFIX>-<NN>-<slug>/` (`aufgabe.md`, legacy
  `hausaufgabe.md`, Tages-README template, or the lesson's `## Aufgabe`
  section) and use that content as the task text.
- Scan all source files for web URLs. Fetch and read each URL to extract
  relevant topic content.
- Include uncommitted changes — the teacher may have just created or edited
  files during class.
- Also check for files in the class folder root (e.g., a shared `README.md`)
  if they provide context for the lesson topic.
- Look for typical file patterns: `README.md`, `*.md`, `*.js`, `*.java`,
  `*.html`, `*.css`, `*.sql`, and any files with "übung" or "aufgabe" in
  the name.

### 3. State Plan

Before writing, display the following to the user:

- **Lesson directory**: the path identified (e.g., `2026-03-21_promises/`)
- **Sources found**: list of files read, commits analyzed, and URLs fetched.
- **Topics deduced**: the teaching topics logically inferred from the sources,
  with a brief explanation of how each topic was derived.
- **Target file**: the full path of the `Aufgabe.md` to be created or updated.

Then proceed immediately without waiting for confirmation.

### 4. Generate or Update Assignment File

- Create `<lesson-dir>/Aufgabe.md` if it does not exist.
- If an existing `Aufgabe.md` (or legacy `Hausübung.md`) is present, read it
  and enrich rather than overwriting. Never rename or delete legacy files.
- Write 2-4 focused, practical exercises that reinforce the key concepts
  covered in the lesson.
- Each exercise should be specific enough that a student can complete it
  independently, referencing the lesson material where appropriate.
- Format as clean Markdown with a topic heading and numbered exercises.
- Write in natural German with proper UTF-8 umlauts.

### 5. Retrofit the Canonical Assignment List (MANDATORY)

After writing `Aufgabe.md`, keep the cohort README's canonical assignment
list current:

1. Locate the cohort README (`README.md` in the class folder root).
2. Look for a `## Aufgaben` section near the top. If it is missing, create it
   as the FIRST section (before all other content) — heading and entries only,
   **no lead-in line**: the list starts directly with the newest entry.
   If an existing section carries a lead-in line (e.g. "Kanonische Liste aller
   Aufgaben …"), remove it and keep the entries.
3. Check whether an entry for this lesson already exists (same ISO date).
4. If missing, ADD one spare bullet line — one sentence or a few words, plus
   a relative link to the lesson directory (a Markdown link whose target is
   the lesson directory path relative to the cohort README):

   ```markdown
   - 2026-10-13: Kurzbeschreibung der Aufgabe → `2026-10-13_thema/`
   ```

5. Insert the entry at the **top** of the list: the list runs **newest first**
   (descending ISO date). Never reword or delete existing entries. A list that
   still runs oldest-first gets flipped once, whole, in the same pass.
6. The list is an INDEX only — never copy the full task text into the cohort
   README.

### 6. Confirm

- Show the user what was created or updated.
- Report the file path, the number of exercises added or changed, and whether
  the canonical list entry was added or already existed.

## Assignment Evidence

Only create assignment entries when repository evidence supports that an
assignment is appropriate. Concrete examples of valid evidence:

- The lesson README or notes mention "Aufgabe", "Aufgaben", or a prepared
  lesson reference (Legacy sources may say "Hausübung" or "Übung" — treat
  "Aufgabe"/explicit assignment instructions as authoritative).
- Exercise files with starter code, TODO comments, or incomplete
  implementations were created during the lesson.
- The teacher's notes or commit messages reference an assignment.
- The lesson material covers a topic with clear practice exercises that
  naturally follow from what was taught.

If the source material reveals the lesson topic but nothing suggests an
assignment was intended, omit the assignment entry and report this to the
user.

## Constraints

- Never create, update, or reference `Hausübungen.md` (plural/cumulative).
  This skill only produces per-lesson `Aufgabe.md` files.
- Never commit generated changes. Leave files on disk for the user to review.
- Preserve existing assignment entries when enriching an existing file.
- The canonical list retrofit writes ONLY to the cohort README's
  `## Aufgaben` section (create if missing) — never touch other README
  content.
- Write natural German. Do not replace umlauts with transliterations (`ae`,
  `oe`, `ue`) unless the source material explicitly requires that form.
- Group commits from the same teaching session into one assignment entry.
- Do not fabricate dates, details, or exercises not supported by the source
  material.

## Output Expectations

- A created or updated `Aufgabe.md` inside the target lesson directory.
- A current canonical `## Aufgaben` list entry in the cohort README.
- 2-4 exercises written in German.
- A plan summary displayed to the user showing sources, deduced topics, and
  target file.
- Confirmation of what was written.
