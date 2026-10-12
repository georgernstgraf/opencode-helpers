---
name: grading-shared
description: Shared configuration and protocols for all grading workflows
license: MIT
compatibility: opencode
metadata:
  category: education
  output: configuration
---

# Grading Shared Configuration

## Purpose

This skill provides centralized configuration for all grading workflows,
ensuring consistent email formatting, address styles, second-person address
throughout all grading content, and database access across different
assessment types.

## Output Language: MANDATORY GERMAN

All student-facing content (grading reports, feedback, email bodies) MUST be 
written in natural German with proper UTF-8 umlauts (ä, ö, ü, ß). 
Never use English for content intended for students.

## Usage

Import this skill at the beginning of any grading-related skill or command.
Reference the sections below for consistent behavior.

## Class Configuration

### Address Style Mapping

Determine formal vs informal address based on class identifier:

| Class | Address Style |
|-------|---------------|
| `2ahwii` | Informal |
| `3ahwii` | Informal |
| `5ahwii` | Informal |
| `4ahwit` | Informal |
| `5ahwit` | Informal |
| `4aaif` | Informal |
| All others | Formal |

### Implementation

When processing student data:
1. Extract class identifier from filename, directory, or database.
2. Normalize to uppercase for comparison: `UPPER(klasse)`.
3. Check if class is in the informal list above.
4. Apply corresponding address style throughout all grading content.

### Name Parsing from Repository Basename (CRITICAL)

Repository directory names follow the convention `Lastname Firstname`. The **last
word** is always the first name; **everything before it** is the last name. This
applies to compound last names as well.

**Parsing rule:** Split the basename on spaces → `parts[0:-1]` = last name,
`parts[-1]` = first name.

| Repository Basename | Last Name | First Name |
|---------------------|-----------|------------|
| `Umlauf Ellen` | Umlauf | Ellen |
| `Quintero Castañeda Nicolas` | Quintero Castañeda | Nicolas |
| `Prodanovic Jovana` | Prodanovic | Jovana |
| `Wahringer Tobias` | Wahringer | Tobias |
| `Leeb Samuel` | Leeb | Samuel |
| `Zore Elsner Marija` | Zore Elsner | Marija |

**Wrong vs Correct — Formal salutation:**
```
❌ Sehr geehrte Frau Ellen,        ← used first name as last name
✅ Sehr geehrte Frau Umlauf,       ← correct last name

❌ Sehr geehrter Herr Nicolas,      ← used first name as last name
✅ Sehr geehrter Herr Quintero Castañeda,  ← correct compound last name

❌ Sehr geehrter Herr Tobias,       ← used first name as last name
✅ Sehr geehrter Herr Wahringer,    ← correct last name
```

**Wrong vs Correct — Informal salutation:**
```
❌ Liebe Umlauf,                    ← used last name as first name
✅ Liebe Ellen,                     ← correct first name

❌ Lieber Quintero Castañeda,       ← used last name as first name
✅ Lieber Nicolas,                  ← correct first name
```

## Email Generation Protocol

### Greeting Formulas

**Formal Address** (uses **last name** — see Name Parsing section above):
- Female: `Sehr geehrte Frau [Last Name],`
- Male: `Sehr geehrter Herr [Last Name],`
- Unknown gender: `Guten Tag [First Name] [Last Name],`

**Informal Address** (uses **first name** — the last word in the basename):
- Any gender: `Liebe [First Name],` or `Lieber [First Name],`
- Female preference: `Liebe [First Name],`
- Male preference: `Lieber [First Name],`
- Unknown gender: `Guten Tag [First Name] [Last Name],`

**Concrete examples:**

| Basename | Gender | Formal Greeting | Informal Greeting |
|----------|--------|-----------------|-------------------|
| `Umlauf Ellen` | F | `Sehr geehrte Frau Umlauf,` | `Liebe Ellen,` |
| `Quintero Castañeda Nicolas` | M | `Sehr geehrter Herr Quintero Castañeda,` | `Lieber Nicolas,` |
| `Wahringer Tobias` | M | `Sehr geehrter Herr Wahringer,` | `Lieber Tobias,` |

### Closing Formulas

**Formal Address:**
```
Mit freundlichen Grüßen,

   Georg Graf
```

**Informal Address:**
```
Lieben Gruß,

   Georg Graf
```

### Automatic Assessment Disclaimers

Every grading email body MUST include a disclaimer paragraph directly below the greeting. The wording depends on the class's address style (Formal/Informal) and the assessment type (Assignments/Projects vs. Knowledge-Checks):

**Formal Address (Sie):**
- **Assignments / Projects / General (Leistungsfeststellung):**
  `Im Folgenden finden Sie die automatische Beurteilung Ihrer Leistungsfeststellung. Bitte beachten Sie, dass diese Beurteilung Irrtümer enthalten kann.`
- **Knowledge-Checks / Mini-Exams (Knowledge-Check):**
  `Im Folgenden finden Sie die automatische Beurteilung Ihres Knowledge-Checks. Bitte beachten Sie, dass diese Beurteilung Irrtümer enthalten kann.`

**Informal Address (Du):**
- **Assignments / Projects / General (Leistungsfeststellung):**
  `Im Folgenden findest du die automatische Beurteilung deiner Leistungsfeststellung. Bitte beachte, dass diese Beurteilung Irrtümer enthalten kann.`
- **Knowledge-Checks / Mini-Exams (Knowledge-Check):**
  `Im Folgenden findest du die automatische Beurteilung deines Knowledge-Checks. Bitte beachte, dass diese Beurteilung Irrtümer enthalten kann.`

### Gender Determination

Gender is determined from the **first name** (the last word in the repository
basename). Do NOT use the full basename string for gender lookup.

When gender is not clear from the first name:
1. Use class records or submission wording as additional context.
2. If still uncertain, use neutral fallback: `Guten Tag [First Name] [Last Name],`
3. Keep class-based closing formula (formal or informal based on class).
4. Flag case for manual review in the output files.

## Second-Person Address in Grading Content

### Requirement

ALL grading content must address the student directly in the second person,
matching the email salutation style. This applies to:
- `*_grading.md` files (repograde, knowledge-assessment, projectgrade)
- Email body text in `EMAIL.json`

### Pronoun and Verb conjugation

| Style | Pronoun | Verb Conjugation | Example |
|-------|---------|-----------------|---------|
| Formal (Sie) | Sie | 3rd person plural formal | "Sie haben die Aufgabe gut gelöst" |
| Informal (Du) | Du | 2nd person informal | "Du hast die Aufgabe gut gelöst" |

### Grading Content Examples

**Formal Address (Sie) - Wrong ❌:**
```
Der Student hat die Aufgabe gut gelöst. Er hat sich bemüht.
```

**Formal Address (Sie) - Correct ✅:**
```
Sie haben die Aufgabe gut gelöst. Sie haben sich bemüht.
```

**Informal Address (Du) - Wrong ❌:**
```
Der Schüler hat die Aufgabe gut gelöst. Er hat sich bemüht.
```

**Informal Address (Du) - Correct ✅:**
```
Du hast die Aufgabe gut gelöst. Du hast dich bemüht.
```

### Gender-Neutral Handling for Unclear Cases

When student gender cannot be determined:
1. Use formal "Sie" (works as gender-neutral in written German).
2. Use gender-neutral adjective forms where possible.
3. Use neutral greeting fallback: `Guten Tag [First Name] [Last Name],`
4. Flag in output files for manual review.

### Consistency Checklist

Before finalizing any grading output, verify:
- [ ] Email greeting matches body address style (Sie or Du)
- [ ] All pronouns in body refer to student as "Sie" or "Du"
- [ ] No third-person references to the student ("der Schüler", "die Studentin")
- [ ] Verb conjugation matches address style
- [ ] Closing formula matches address style

## Grading Methodology (CRITICAL)

All grading workflows MUST evaluate student work through pure AI reasoning and
judgment. The following rules apply to every grading skill (`repograde`,
`knowledge-assessment`, `projectgrade`) and every subagent used within them.

### Pure AI Evaluation

- **Grading is performed through AI reasoning alone.** The agent must read,
  understand, and evaluate each student submission by directly comparing it
  against the task instructions and expected solutions. The evaluation must be
  a direct intellectual act by the AI, not a mechanical or automated process.
- **No scripts or programs for evaluation.** Under no circumstances may agents
  write, invoke, or rely on scripts, programs, test runners, linters, or
  automated checkers to assess student work. Grading must never be reduced to
  a mechanical operation.
- **Programmatic output formatting is allowed.** Using `json.dump()` or similar
  serializers to write `EMAIL.json` or `*_email.json` files is permitted. The
  prohibition applies only to the act of grading/assessing the student's work
  itself — not to output formatting helpers.

### Available Inputs Per Evaluation

For every student submission, the agent has access to the following inputs and
must base its evaluation exclusively on them:

1. **Task instructions** — the assignment description (Aufgabe), exam questions, or project
   requirements that define what was asked of the student.
2. **Expected solutions** — the reference solution or answer key against which
   student work is compared.
3. **Student submission** — the individual student's work (repository commits,
   answer file, code changes) to be evaluated.

### Handling Large Volumes

- **For bulk or multi-student grading, use sub-agents.** Each sub-agent
  evaluates one student or repository independently, using the same pure AI
  reasoning approach.
- Sub-agents MUST follow all rules defined in this skill, including the
  no-script grading requirement.
- The orchestrating agent delegates work to sub-agents but must never write
  evaluation scripts or batch-processing programs.

## Database Access

### Databases

| Database | Path | Purpose |
|----------|------|---------|
| UploadThing | `/home/georg/OneDrive/uploadthing.db` | Repository grading |
| Vacuum | `vacuum.db` (current directory) | Knowledge-check grading (must exist at start; error if missing) |

### Schema

Table: `users`

| Column | Description |
|--------|-------------|
| `email` | Student email address |
| `name` | Full student name |
| `klasse` | Class identifier |

### Lookup Protocol

1. Match student by name (handle variations and partial matches).
2. Normalize class comparison to uppercase: `WHERE UPPER(klasse) = UPPER(?)`.
3. Retrieve `email` and `klasse` columns.
4. Use `klasse` to determine address style.
5. If `vacuum.db` is missing at start, stop immediately with error.
6. Track all students with missing email addresses.

## Missing Email Address Handling (CRITICAL)

When generating `EMAIL.json`, if any student's email address cannot be found in
the database, the workflow MUST stop before generating the file.

### Protocol

1. **Collect all lookups**: Perform database lookup for all students first.
2. **Check for missing emails**: After all lookups, identify students without
   valid email addresses.
3. **If any are missing**:
   - STOP immediately.
   - Do NOT generate `EMAIL.json`.
   - Present ALL unresolved names to the user in a clear list:
     ```
     Die folgenden Schüler/innen konnten nicht in der Datenbank gefunden werden:
     - [Name 1]
     - [Name 2]
     - ...
     
     Bitte aktualisieren Sie die Datenbank und starten Sie den Vorgang erneut.
     ```
   - Wait for user to update the database.
   - User should confirm when database is updated.
   - Retry the entire grading process.
4. **Only proceed**: Generate `EMAIL.json` when ALL students have valid email
   addresses.

### Rationale

- Prevents incomplete or invalid email payloads.
- Ensures all students receive their feedback.
- Forces database maintenance rather than workarounds.

## Email JSON Structure

```json
[
  {
    "mailto": "student@example.com",
    "subject": "[Subject based on context]",
    "body": "[Full personalized assessment in German]"
  }
]
```

### Body Requirements

- Language: German
- Address student directly in second person (Sie or Du based on class)
- Include full assessment content (long emails expected)
- Preserve paragraph spacing and readable newline structure
- Include greeting at start
- Include closing formula at end
- UTF-8 encoding with natural German umlauts (ä, ö, ü, ß)

### JSON Escaping Rules (CRITICAL)

The `body` field often contains multi-paragraph German text with newlines, quotes,
and special characters. **Improper escaping is the most common cause of broken
email JSON files.** The following rules MUST be followed:

1. **All JSON string values must be valid JSON.** Newlines inside the `body`
   field must use the escaped sequence `\n` (two characters: backslash, `n`), NOT
   literal line breaks. Double quotes must be escaped as `\"`, backslashes as `\\`,
   and tabs as `\t`.

2. **No literal newlines inside JSON string values.** A file like this is INVALID:
   ```json
   "body": "Sehr geehrte Frau Huber,

   Sie haben die Aufgabe gut gelöst."
   ```
   The correct form is:
   ```json
   "body": "Sehr geehrte Frau Huber,\n\nSie haben die Aufgabe gut gelöst."
   ```

3. **Validate before writing.** Every `*_email.json` file must parse successfully
   with a standard JSON parser. After writing, verify with:
   ```bash
   python3 -c "import json; json.load(open('FILE_email.json'))"
   ```

4. **Detect double-escaped newlines.** After loading the JSON, check that the
   `body` field does not contain literal `\n` (backslash followed by n, which
   indicates the file had `\\n` — double-escaped newlines):
   ```bash
   python3 << 'PYEOF'
   import json
   d = json.load(open('FILE_email.json'))
   body = d[0]['body']
   assert '\\n' not in body, 'body contains literal backslash-n — double-escaped newlines'
   print('OK')
   PYEOF
   ```
   If validation fails, fix by reading the file with `json.load()`, replacing
   literal `\n` in the body with actual newlines, and re-writing with
   `json.dump(..., ensure_ascii=False)`.

5. **MUST use programmatic JSON writing.** You MUST use `json.dump()` or
   `json.dumps()` to write `*_email.json` or `EMAIL.json`. Never construct JSON
   via string interpolation, f-strings, or template languages. Always use
   `ensure_ascii=False` to preserve UTF-8 umlauts (ä, ö, ü, ß). This guarantees
   correct escaping of all special characters automatically.

## Constraints

- All grading content must be written in German.
- All grading content must use second-person address (Sie or Du).
- Never use third-person to refer to the student being graded.
- UTF-8 encoding with natural German umlauts (ä, ö, ü, ß); never replace with
  transliterations (ae, oe, ue) unless source material requires it.
- Trailing comma required in all salutations.
- Two newlines before signature line.
- Three-space indentation before `Georg Graf`.
- Never guess gender - use neutral fallback when uncertain.
- Flag uncertain cases for manual review.
- Grading must be performed through pure AI evaluation; never write scripts,
  programs, or automated checkers to assess student work. For bulk grading,
  use sub-agents instead (see `## Grading Methodology (CRITICAL)` above).

## Repository Analysis Protocol

Shared pre-grading verification and analysis steps for all repository-based
grading skills (`repograde`, `projectgrade`).

### Pre-Grading Verification

Before inspecting repository content, verify repository state:

1. Navigate to the student repository directory.
2. Run the Inner Git Repository Discovery to locate the actual Git working
   directory inside the student directory.
3. Run `git pull` inside the Git working directory to ensure latest version is
   checked out.
4. Run `git status` inside the Git working directory to check for uncommitted
   changes.
5. If uncommitted changes exist, STOP IMMEDIATELY and report to user.
6. If pull fails or reports errors, STOP IMMEDIATELY and report to user.

### Discovery

- Identify relevant branches.
- Enumerate commits while avoiding duplicate SHA processing.
- Collect commit metadata: SHA, author, date, branch context, and message.

### Per-Commit Inspection

For every relevant commit, inspect actual changes with commands equivalent to:

- `git show --stat --summary <sha>`
- `git show --format=fuller --unified=3 <sha>`

Use diff content, not filenames alone, to identify what the student worked on.

### Topic Detection

Detect technical topics from the diffs and distinguish substantive work from
superficial edits.

- substantive: meaningful implementation, debugging, refactoring, feature work.
- superficial: formatting-only edits, whitespace changes, trivial renames,
  auto-generated files without meaningful modification.

Consider common patterns across JavaScript, Java, C#, SQL, CSS, HTML, and
general programming constructs.

### Branch and Activity Analysis

- Focus primarily on `main`, but highlight significant non-main branch work.
- Count commits over time.
- Detect inactive gaps between first and last relevant commits.
- Use evidence-based diligence signals such as `high`, `medium`, or `low`.

## Repository Structure Discovery

Student repositories may use a two-level directory structure:

```
CWD/STUDENT_DIR/INNER_PROJECT/.git
```

The `.git` directory (or `.git` file) is one level deeper than the student
directory. This section defines how to locate the actual Git working directory
before running any git commands.

### Inner Git Repository Discovery

For each student repository, determine the correct Git working directory:

1. **Enter the student directory** (or follow the symlink to its target).
2. **Search for `.git`** inside the student directory up to 2 levels deep.
3. The parent directory of the found `.git` is the **Git working directory**.
4. All `git` commands (`pull`, `log`, `show`, `status`, `diff`) MUST be run
   inside the Git working directory.
5. Derive output filenames (`<basename>_grading.md`, `<basename>_email.json`)
   from the **student directory basename** (the top-level name or the symlink
   name), NOT from the inner project folder name.

### Example

```
2ahwii-swp/alw240094/SWP-2025-26/.git
            ^^^^^^^^^ student dir basename (used for output filenames)
                       ^^^^^^^^^^ Git working directory (where git commands run)
```

## Assignment Discovery Protocol (Aufgaben-Discovery)

Shared assignment source discovery for `repograde` and `projectgrade`.
Assignments (Aufgaben) may exist in multiple locations. The grading skill MUST
discover and merge all sources into a unified assignment list before matching
against student commits.

### Terminology (CRITICAL)

- The canonical term is **Aufgabe** (plural: **Aufgaben**). All user-visible
  content uses "Aufgabe 1", "Aufgabe 2", … spelled out — never "Hausübung",
  "HÜ", or "homework".
- **Übung** is NOT an Aufgabe. Übungen (e.g. "Jetzt du!") are in-class
  Mitarbeits-Elemente and MUST never appear in the assignment list.
- The word **Hausübung** is legacy vocabulary. It is recognized only inside
  legacy sources (see below) and never used in new output.

### Source 1: Cohort README (via `_class` Symlink, Preferred)

Check for a `_class` symlink in the CWD. If it exists, follow it and read the
cohort README (`README.md`) inside the linked class folder.

#### 1a: Canonical Assignment List

Look for a `## Aufgaben` section near the top of the cohort README. It is a
spare bullet-list index with one line per assignment:

```markdown
## Aufgaben

- 2026-09-29: Seite dekorieren (CSS) → [2026-10_XX_css-basics/](./2026-10_XX_css-basics/)
```

Parse each bullet as `(iso_date, short_description, optional_relative_link)`:

- Resolve relative links against the cohort README directory; the link target
  is a lesson folder (Tagesordner) whose assignment content is read from there
  (see Source 2). The list is an INDEX only — the task text lives in the
  lesson folder, never in the list itself.
- Entries without a link are matched by date/topic against the other sources.
- Grading is read-only: if the canonical list is missing, do NOT create it.
  Report its absence as a note.

#### 1b: Dated Sections in the Cohort README

Sections with `## YYYY-MM-DD` headings may contain assignment text directly.
Extract the date from the heading and the assignment content from the section
body. Relative deadlines ("bis nächste Woche 00:00") are resolved via the wu
termine (see Deadline Calculation).

### Source 2: Per-Lesson Folders inside `_class`

Scan `_class/` for subdirectories matching `<YYYY-MM-DD>_<topic>`,
`<YYYY-MM-DD>__<topic>` (create-lesson convention, double underscore), or an
ambiguous `<YYYY-MM>_<X>_<topic>` form (e.g. `2026-10_XX_css-basics`) whose
date is resolved via Git (see Git Folder Provenance Resolution below).

For each matching directory, check for assignment content in this order:

1. `Aufgabe.md` — dedicated assignment file (canonical)
2. `README.md` — Tages-README with an assignment section under the heading
   `## Aufgabe` or `## 📝 Aufgabe`
3. Legacy files (data from earlier school years only): `Hausübung.md`,
   `Angabe_HÜ.md`, or a README section under `## Hausübung` / `## 📝 Hausübung`.
   If the legacy section states "Keine Hausübung", skip this lesson.

When a file is found:
- Extract the date from the directory name — a full `YYYY-MM-DD` is the
  CANDIDATE assignment date, subject to the Git Folder Provenance check below
  (a renamed folder keeps the date of its OLDEST name).
- Extract the topic from the directory name and/or the file content.
- Read the file content for assignment details.
- Add to the assignment list: `(iso_date, topic, content)`.

#### Reference Pattern (Indirection to a Prepared Lesson)

The `## Aufgabe` section of a Tages-README may be a REFERENCE rather than task
text, for example: "Wir haben Lesson `KM3-03-css-basics` gemacht, die Aufgabe
ist die Aufgabe von dort." Detection: a lesson reference matching
`<PREFIX>-<NN>-<slug>` and/or a relative link into `unterricht/`.

Resolution:

1. Resolve the lesson folder relative to the teaching-repo root:
   `<repo-root>/unterricht/<PREFIX>-<NN>-<slug>/` (from a cohort folder one
   level below the repo root this is `../unterricht/…`, from two levels
   `../../unterricht/…`).
2. Read the assignment content from that folder in this order: `aufgabe.md`,
   `hausaufgabe.md` (legacy), the Tages-README template
   (`<PREFIX>-<NN>-<slug>.md`), or the `## Aufgabe` section of the lesson.
3. Assignment date and deadline stay cohort-side (folder name / Git / wu);
   only the CONTENT is resolved remotely. An explicit deadline found in the
   referenced content still wins (see Deadline Calculation).

### Source 3: Legacy Cumulative File

Check for a `Hausübungen.md` file directly in the CWD or inside `_class/`
(may be a symbolic link; follow symlinks when reading). This is the legacy
single-file approach from earlier school years. If found, parse it using the
Semantic Date Extraction rules below.

#### Semantic Date Extraction

**You MUST perform a thorough semantic analysis of the entire file.**

Many agents fail at this step because they:
- Only read the first entry
- Miss dates embedded in the text (not just headings)
- Fail to convert German date formats to ISO
- Skip entries that don't match a naive pattern match

Required steps:

1. **Read the ENTIRE file** — do not stop after the first assignment entry.
2. **Extract ALL date references** from:
   - Headings: `## Hausübung vom 18. Februar`
   - Inline dates: `Abgabe bis 25. Februar`
   - Date ranges: `Zeitraum: 10.-18. März`
   - Relative dates: `nächste Woche`, `in 2 Wochen` (convert to absolute)
3. **Normalize ALL dates to ISO format** (YYYY-MM-DD).
4. **Build an assignment list**: `[(iso_date, topic, content), ...]`.

Date patterns to recognize:

| Pattern | Example | Extraction |
|---------|---------|------------|
| `vom DD. Monat` | `vom 18. Februar` | 2026-02-18 (infer year) |
| `vom DD. Monat YYYY` | `vom 18. Februar 2026` | 2026-02-18 |
| `DD.MM.YYYY` | `18.02.2026` | 2026-02-18 |
| `bis DD. Monat` | `Abgabe bis 25. Februar` | 2026-02-25 (deadline) |
| `Zeitraum: DD.-DD. Monat` | `Zeitraum: 10.-18. März` | 2026-03-10 to 2026-03-18 |

Month name mapping:

```
Januar = 01    Juli = 07
Februar = 02   August = 08
März = 03      September = 09
April = 04     Oktober = 10
Mai = 05       November = 11
Juni = 06      Dezember = 12
```

When year is not explicit, infer from the grading context or cross-reference
with commit dates.

**Common Failure Pattern (AVOID THIS):**
```
❌ WRONG: Read Hausübungen.md, see first entry is "vom 18. Februar",
         requested date is 2026-02-10, conclude "no matching assignment"
✅ CORRECT: Parse ALL entries, find "vom 10. Februar" (matches),
            "vom 18. Februar" (after cutoff), "vom 25. Februar" (after cutoff)
```

### Source 4: Per-Lesson Files in CWD

Scan the CWD itself for subdirectories matching `<YYYY-MM-DD>_<topic>` that
contain assignment content (same file search order as Source 2, including the
Reference Pattern). Apply Future Lesson Exclusion identically.

### Git Folder Provenance Resolution

A lesson folder's NAME is not a reliable assignment date: folders may be
RENAMED forward (e.g. a folder created as `2026-09-22_html-basics` renamed to
`2026-09-29_html-basics` when the next UE approached). The assignment date
MUST therefore be resolved from the folder's Git provenance.

**Pitfall (CRITICAL):** Never trust `git log --diff-filter=A` on the current
path alone — renamed files register as `A` at the new path. Always use rename
detection (`-M` / `--follow`).

Resolution (first match wins):

1. **Reconstruct the name history** (run inside the `_class` target repo):
   ```bash
   git log -M --name-status --date=iso --format='%h %ad' --diff-filter=AR \
       -- <klasse>/<current-folder>*
   ```
2. **Rename found**: the name history is `oldest-name → … → current-name`.
   The assignment date is the date encoded in the OLDEST name of that chain
   (e.g. `2026-09-22_html-basics` → assignment date 2026-09-22). The rename
   commit date itself is NEVER the assignment date.
3. **No rename, full `YYYY-MM-DD` in the current name**: that date is the
   assignment date.
4. **No rename, ambiguous name** (e.g. `2026-10_XX_css-basics`): the
   assignment date is the DATE PART of the oldest commit that added files in
   the folder.
5. **wu validation (all cases)**: the resolved date must be a real lesson
   date from the wu termine; snap if needed (latest lesson date ≤ resolved
   date). If both the current name date and the provenance date are real
   lesson dates, the provenance date (oldest name) wins.
6. **README cross-check**: a lesson date declared in the Tages-README (e.g.
   "HTML-Grundlagen (2026-09-22)") is a cross-check signal. On conflict, the
   provenance/wu date wins and the conflict MUST be reported to the user —
   never silently resolved.
7. **Same-day renames (preparation case)**: when the folder was renamed on
   the SAME day it was created (e.g. created as `2026-09-29_css-basics` and
   renamed in the same commit to `2026-10_XX_css-basics`), the folder was
   prepared during that UE for a LATER UE — the oldest-name date is the
   preparation date, NOT the assignment date. In that case the assignment
   date comes from a dated cohort README section documenting the UE (e.g.
   `## 2026-10-06__css`) or from the wu termine, and the ambiguity MUST be
   reported. Note: lesson material may be DELETED after being moved into
   `unterricht/` — the cohort README reference section remains the
   assignment source (Reference Pattern applies).

### wu Termine Integration (MANDATORY)

Derive the lesson address from the `_class` symlink target
`…/GRG-<FACH>/<klasse>/` as `wu lesson <klasse>/<fach>` (e.g.
`_class -> GRG-WMC/3aaif` → `wu lesson 3aaif/wmc`). Query the termine:

```bash
wu lesson 3aaif/wmc termine --json
```

The termine list is used to:

1. **Snap dates**: map git commit dates to real lesson dates (latest lesson
   date ≤ commit date).
2. **Compute deadlines**: deadline = next DISTINCT lesson date strictly after
   the assignment date, at 00:00 (duplicate slots on one date count once;
   holidays are respected automatically).
3. **Resolve relative deadlines** ("bis nächste Woche", "bis zur nächsten UE").

**Failure rule (CRITICAL):** If `wu` is not installed, fails, or returns no
termine, STOP IMMEDIATELY with a German error message (e.g. "wu liefert keine
Termine — Aufgabendaten und Deadlines können nicht aufgelöst werden."). Never
guess dates or deadlines.

### Future Lesson Exclusion

Per-lesson directories with a date in the future represent prepared but
not-yet-held lessons. Their assignments MUST NOT be included in the unified
assignment list.

1. Determine today's date: `date +%Y-%m-%d`
2. For each per-lesson directory, resolve the assignment date via Git Folder
   Provenance Resolution.
3. If `lesson_date > today`, skip this directory entirely.
4. Do NOT include its assignment, regardless of whether an assignment section
   exists in the file.

### Merging All Sources

1. Collect assignment entries from all sources into a single unified list.
2. If multiple sources describe the same assignment, prefer the per-lesson
   file content over the canonical list index and over the legacy cumulative
   file.
3. Sort the unified list by date.
4. If no source provides any assignment entries, report this to the user and
   grade based on available work only.

## Aufgaben-Ablage-Ordnung (Order to Keep When Giving Assignments)

This section documents the expected repository layout. Keep to it when
creating or preparing assignments:

1. **Kohorten-README** (`<klasse>/README.md`): carry a spare canonical
   `## Aufgaben` bullet list near the top — one line per assignment with ISO
   date, a few words, and a relative link to the Tagesordner. The list is an
   index only; the task text lives in the lesson folder.
2. **Tagesordner** (`<klasse>/YYYY-MM-DD_<topic>/`; the create-lesson double
   underscore `YYYY-MM-DD__<topic>` is also accepted): contains `Aufgabe.md`
   or a `README.md` with an `## Aufgabe` section — full task text or a
   reference to a Prepared Lesson (`unterricht/<PREFIX>-<NN>-<slug>/`).
3. Ambiguous folder names like `YYYY-MM_XX_<topic>` are allowed; the date is
   resolved via the teaching repo's Git history and snapped to a wu lesson
   date. Renaming a lesson folder forward is also fine — the discovery
   attributes the date of the OLDEST name in the folder's Git history and
   reports the rename.
4. **Deadline**: state a concrete date ("Abgabe per Push bis 2026-10-13
   00:00") or "bis zur nächsten UE" (resolved via wu). Vague formulations
   that wu cannot resolve are not acceptable.
5. Prepared but not-yet-held lessons (future dates) may already exist; they
   are excluded automatically until the date arrives.
6. Assignments NEVER go into a student repository.
7. The word "Übung" marks in-class exercises, never assignments. Do not use
   "Hausübung" for new content.

## Deadline Calculation

### Determining the Assignment Date

1. Full `YYYY-MM-DD` in the lesson folder name → that date is the assignment
   date.
2. Ambiguous or renamed folder name (e.g. `2026-10_XX_css-basics`,
   `2026-09-29_html-basics` renamed from `2026-09-22_html-basics`) → Git
   Folder Provenance Resolution, snapped via wu to a real lesson date.
3. Cohort README dated section → the heading date.

The assignment date MUST correspond to an actual lesson date from
`wu lesson <klasse>/<fach> termine --json`.

### Determining the Deadline

Precedence:

1. **Explicit deadline in the assignment text** (e.g. "Abgabe per Push bis
   2026-09-29 00:00") ALWAYS wins. Parse ISO (`YYYY-MM-DD`) and German dates.
2. **Otherwise**: deadline = next DISTINCT lesson date strictly after the
   assignment date, at 00:00:00, taken from the wu termine. Duplicate slots
   on the same date count once; this automatically respects holidays
   (e.g. assignment 2026-10-13 → deadline 2026-10-20T00:00:00 when 10-13 is
   followed by 10-20).
3. **Relative deadlines** ("bis nächste Woche", "bis zur nächsten UE") are
   resolved to the next lesson date at 00:00 via the wu termine.

Subagents MUST take the deadline from the wu output (or an explicit deadline
in the assignment text) and MUST use shell date arithmetic only for
formatting, never for guessing:

```bash
wu lesson 3aaif/wmc termine --json
```

**Failure rule:** If wu is unavailable or returns no termine, STOP IMMEDIATELY
with a German error message. Never fall back to a fixed "+7 days" guess.

### Commit Filtering by Deadline

```bash
# On-time commits (assignment ≤ commit ≤ deadline):
git log --after="2026-02-10" --before="$DEADLINE" --oneline

# Late commits (commit after deadline):
git log --after="$DEADLINE" --oneline
```

### Punctuality Classification

| Latest relevant commit | Classification | Factor | Meaning |
|------------------------|----------------|--------|---------|
| ≤ DEADLINE             | pünktlich      | 1.0    | Full points possible |
| > DEADLINE             | verspätet      | 0.75   | 25% penalty on achieved quality, regardless of how late |
| No commits             | fehlend        | —      | 0 points for this assignment |

### Deadline in Reports

Reports MUST mention the concrete deadline for each assignment, including the
exact `YYYY-MM-DDT00:00:00` timestamp and whether the student's latest
relevant commit fell before or after it.

## Bulk Grading Protocol

Shared concurrency and directory handling for `repograde` bulk mode.

### Directory Exclusion

When enumerating student repositories, **exclude**:
- `_class` (assignment symlink)
- Any directory starting with `_` (underscore prefix)
- Any directory starting with `.` (dot prefix)
- Any regular files (not directories and not symlinks)

These excluded entries are NOT student repositories and must never be graded.

### Symlink Handling

Student repositories may be accompanied by name-based symlinks:

```
Alwazeh Sami -> alw240094
```

These symlinks are aliases to student directories. They serve for name
resolution (see `Student Name Resolution via Symlinks`) but are NOT
separate repositories. Only the target directories are graded.

When enumerating:
1. If a symlink points to another directory inside the CWD, skip it as a
   candidate for grading — only the target directory is graded.
2. Use the symlink's name for student identification.
3. Follow the symlink to find the actual repository for git operations.
4. If the symlink is BROKEN (target does not exist), it is NOT skipped and
   NOT an error — see Broken Name-Symlinks (Missing Repository) below.

### Concurrency

- Default maximum: 5 repositories in progress at once.
- When one grading run completes, start the next after an approximately
  3-second delay.
- Each subagent must derive its output stem from the repository basename and
  write only `<basename>_grading.md` plus `<basename>_email.json`.
- Subagents must never write shared `EMAIL.json`.

### Aggregation

After all subagents finish, the master workflow aggregates per-student
`*_email.json` files into a single `EMAIL.json`.

**Stop condition:** Verify the aggregation script exists:
```bash
SCRIPT=~/.opencode/skills/grading-shared/aggregate-emails.py
if [ ! -f "$SCRIPT" ]; then
    echo "ERROR: $SCRIPT not found" >&2
    exit 1
fi
```
If the script is missing, **STOP**, report the path to the user, and wait
for resolution before continuing.

**Execution:** Run the script from the current working directory:
```bash
~/.opencode/skills/grading-shared/aggregate-emails.py
```
If the script exits with a non-zero status or reports errors on stderr,
**STOP**, display its output to the user, and do not proceed.

## Email Body Format (CRITICAL)

All grading email bodies MUST be clear ASCII text. This section defines the
exact structure and formatting rules for every email body generated by any
grading skill.

### Plain-Text Rule

Email bodies are plain ASCII text with **one exception**: code blocks with
backtick fences (e.g., ```sql ... ```) for short source-code snippets that
help illustrate a grading point.

**Forbidden in email bodies:**
- Markdown headers (`##`, `###`, etc.)
- Bold text (`**...**`)
- Italic text (`*...*`)
- Markdown tables
- Markdown bullet lists (`- item` or `* item`)
- Horizontal rules (`---`)
- Any other Markdown formatting

**Allowed in email bodies:**
- Plain text paragraphs separated by blank lines.
- Code blocks with backtick fences for short source-code snippets.
- Natural German text with UTF-8 umlauts (ä, ö, ü, ß).

### Structure for Assignment Grading Emails

Used by `repograde` skill (single-repo and bulk mode). The email body follows
this exact paragraph order:

1. **Greeting** — per Greeting Formulas section above.

2. **Automatic assessment disclaimer** — per Automatic Assessment Disclaimers section above.

3. **Opening sentence** (address style dependent):
   - Formal: `Ich habe Ihre Aufgaben, welche im Zeitraum vom [Start-Datum] bis zum [End-Datum] aufgegeben waren, durchgesehen.`
   - Informal: `Ich habe deine Aufgaben, welche im Zeitraum vom [Start-Datum] bis zum [End-Datum] aufgegeben waren, durchgesehen.`
   - Dates in German long format (e.g., "18. Februar 2026", "4. März 2026").

3. **Commit summary** — Two to three sentences summarizing the commits
   discovered in the student's repository during the grading period.
   Mention overall activity, approximate number of substantive commits,
   and any notable patterns (gaps, bursts, consistent work).

4. **Assignment overview** — A concise list of all assignments,
   each in one to two sentences. Format:

   ```
   Aufgabe 1: [Topic/content summary in 1-2 sentences]
   Aufgabe 2: [Topic/content summary in 1-2 sentences]
   ```

   Use "Aufgabe" spelled out with a sequential number. Never abbreviate
   (no "HÜ", no "A1").

5. **Per-assignment evaluation** — For each assignment, provide
   a detailed discussion and evaluation on a 0–100% scale. Each evaluation
   is a separate paragraph covering:
   - What the student did well.
   - What was missing or could be improved.
   - Specific technical observations (with code snippets where helpful).
   - A percentage rating for that individual assignment.

6. **Coverage / timeliness summary** — One short paragraph summarizing overall
   assignment coverage and whether submissions were on time, late, partial, or
   missing where relevant.

7. **Recommendations and praise** — A warm, genuine paragraph with
   improvement suggestions and subtle praise. See Praise Guidelines below.

8. **Final score summary** — One short paragraph containing the final weighted
   result in the form `Endbewertung: XX/100 (XX%)`.

9. **Closing** — per Closing Formulas section above.

Keep email length reasonably consistent across students. Do not omit one of the
paragraph groups above simply because a repository is weaker or stronger; if
evidence is limited, say so briefly and continue with the same structure.

For students WITHOUT a repository (broken name-symlink), see the
Missing Repository Emphasis below — that variant replaces paragraph groups
3-6.

### Missing Repository Emphasis (No-Repo Cases)

For a student whose repository is missing (broken name-symlink — see Broken
Name-Symlinks), the email body consists of: greeting, automatic assessment
disclaimer, then the emphasis paragraph as the FIRST content paragraph
(adapted to the address style), a short consequences paragraph, and the
closing. The emphasis paragraph wording:

- Informal: `Zu deinem Aufgaben-Repository liegt mir bislang kein Link vor. Das ist der mit Abstand wichtigste offene Punkt: Ohne die Bekanntgabe deines Repositories ist keine positive Beurteilung möglich. Sende mir bitte UMGEHEND den URL deines GitHub-Repositories an grafg@spengergasse.at — genau so haben wir es in der ersten UE vereinbart. Sobald das Repository verfügbar ist, werde ich alle Aufgaben nachbewerten.`
- Formal: `Zu Ihrem Aufgaben-Repository liegt mir bislang kein Link vor. Das ist der mit Abstand wichtigste offene Punkt: Ohne die Bekanntgabe Ihres Repositories ist keine positive Beurteilung möglich. Senden Sie mir bitte UMGEHEND den URL Ihres GitHub-Repositories an grafg@spengergasse.at — genau so haben wir es in der ersten UE vereinbart. Sobald das Repository verfügbar ist, werde ich alle Aufgaben nachbewerten.`

Follow with one short paragraph stating that all assignments in the grading
period currently count 0% and that the final result is
`Endbewertung: 0/100 (0%)`.

### Structure for Knowledge-Check Emails

Used by `knowledge-assessment` skill. Same plain-text rule applies.

1. **Greeting** — per Greeting Formulas section above.

2. **Automatic assessment disclaimer** — per Automatic Assessment Disclaimers section above.

3. **Opening sentence** (address style dependent):
   - Formal: `Ich habe Ihre Wissensüberprüfung vom [Datum] durchgesehen.`
   - Informal: `Ich habe deine Wissensüberprüfung vom [Datum] durchgesehen.`

4. **Score summary** — Total points achieved out of total possible points.

4. **Question-by-question analysis** — Plain text paragraphs discussing
   strengths and weaknesses in specific questions.

5. **Recommendations and praise** — Same guidelines as assignment emails.

6. **Solutions note** — `Ich habe die Datei mit den korrekten Lösungen in das Git-Repository hochgeladen.`

7. **Closing** — per Closing Formulas section above.

### Praise Guidelines

Praise must be **subtle and understated**. Never effusive, never over the top.

**Good praise examples:**
- "Die JOIN-Operationen haben Sie sauber umgesetzt."
- "Hier ist Ihnen eine klare Struktur gelungen."
- "Das zeigt ein gutes Verständnis der Konzepte."
- "An dieser Stelle war Ihre Lösung besonders durchdacht."

**Bad praise examples (DO NOT USE):**
- "Hervorragende Arbeit! Brillant gelöst!"
- "Sie sind ein wahrer Meister der Programmierung!"
- "Phantastisch! Weiter so!"
- "Ich bin beeindruckt von Ihrer überragenden Leistung!"

The tone should feel like a calm, observant teacher noting genuine strengths
without exaggeration. Let the facts speak for themselves. When a student did
something well, state it matter-of-factly.

### Examples

Worked formal and informal assignment email bodies are in
[EMAIL-EXAMPLES.md](./EMAIL-EXAMPLES.md). Use them as shape references, not as
text to copy verbatim.

## Reporting Protocol

All grading content must be written in German and address the student directly
in the second person (Sie or Du based on class). See the Second-Person Address
section above for pronoun usage and examples.

The `*_grading.md` files may use full Markdown formatting (headers, bold,
tables, lists). Only the email body in `*_email.json` is restricted to plain
text per the Email Body Format section above.

Reports should include, where applicable:

- repository overview
- assignment-by-assignment summary
- topic coverage
- per-commit technical analysis
- non-main branch activity
- activity over time
- inactive gaps
- diligence assessment
- final evaluation with `Endbewertung: XX/100`

When a consuming skill defines an exact mandatory report template, that template
overrides any looser interpretation of this Reporting Protocol. In such cases,
agents and subagents MUST follow the exact heading names, order, and section
scope defined by the consuming skill and MUST NOT improvise alternative report
structures.

## Student Name Resolution via Symlinks

When the CWD contains name-based symlinks (`Lastname Firstname -> STUDENT_ID`),
use the symlink name to identify the student.

### Resolution Protocol

1. **Detect symlinks**: For each entry in the CWD, check if it is a symlink
   (`[ -L "$entry" ]`) and if it points to another student directory within
   the CWD.
2. **Parse the symlink name**: Apply the standard Name Parsing from Repository
   Basename rule (last word = first name, everything before = last name).
3. **Resolve student identity**:
   - For grading reports and `GRADINGS.md`: use the symlink name
     (e.g., "Alwazeh Sami").
   - For database lookup (email): use the symlink name.
   - For git operations: follow the symlink to the target directory, then
     apply Inner Git Repository Discovery.
   - For output filenames: derive from the symlink basename (e.g.,
     `Alwazeh Sami_grading.md`).

### When Symlinks Are Missing

If no name-based symlinks exist in the CWD, use the student directory name
directly as the identifier. Apply the standard Name Parsing from Repository
Basename rule to extract first and last name.

## Broken Name-Symlinks (Missing Repository)

A name-based symlink whose target does NOT exist (broken symlink, detected
with `[ -L "$entry" ] && [ ! -e "$entry" ]`) means: **the student has not yet
submitted the URL of their assignment repository.** (The conventional
placeholder target name is `KEIN-GITHUB-REPO`, but ANY missing target
qualifies — not just that exact name.)

### Protocol

1. **Do NOT stop and do NOT skip.** A broken name-symlink is a valid grading
   case, not an error. Bulk grading continues; the student is graded as a
   no-repository case.
2. **Evaluation**: no repository → no evidence → ALL assignments are rated
   0% (Quality `—`, Factor `—`, Effective 0%) and the final result is
   `Endbewertung: 0/100`.
3. **Outputs (bulk mode)**: the student receives a normal `<name>_grading.md`
   (mandatory structure per the consuming skill's report format, every
   section explicitly stating that no repository exists and no evidence is
   available) and a `<name>_email.json`. They appear in `GRADINGS.md` with
   0/100 and in the aggregated `EMAIL.json`.
4. **Email lookup**: proceed with the normal database lookup (by name). The
   standard Missing Email Address Handling applies unchanged.
5. **Email emphasis (MANDATORY)**: the email body MUST prominently state that
   submitting the repository URL is REQUIRED for a positive assessment — see
   Missing Repository Emphasis under Email Body Format.
6. **Single-repo mode**: when the explicitly provided repository path is a
   broken symlink, apply the same treatment (no-repo grading report +
   emphasis email) instead of stopping.
7. **No git commands** are run for these students (nothing to pull or
   inspect); the Pre-Grading Verification is skipped for them.

## Output Expectations

This skill provides configuration and shared protocols. Consuming skills
produce:
- Per-student `*_grading.md` files with individual feedback (second-person German).
- `EMAIL.json` with personalized payloads (second-person body).
- `GRADINGS.md` class-wide overview (where applicable).
- `CLASS.md` anonymized class patterns (where applicable).
