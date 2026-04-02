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
| `4aaif` | Informal |
| All others | Formal |

### Implementation

When processing student data:
1. Extract class identifier from filename, directory, or database
2. Normalize to uppercase for comparison: `UPPER(klasse)`
3. Check if class is in the informal list above
4. Apply corresponding address style throughout all grading content

## Email Generation Protocol

### Greeting Formulas

**Formal Address:**
- Female: `Sehr geehrte Frau [Last Name],`
- Male: `Sehr geehrter Herr [Last Name],`
- Unknown gender: `Guten Tag [First Name] [Last Name],`

**Informal Address:**
- Any gender: `Liebe [First Name],` or `Lieber [First Name],`
- Female preference: `Liebe [First Name],`
- Male preference: `Lieber [First Name],`
- Unknown gender: `Guten Tag [First Name] [Last Name],`

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

### Gender Determination

When gender is not clear from first name:
1. Use class records or submission wording as additional context
2. If still uncertain, use neutral fallback: `Guten Tag [First Name] [Last Name],`
3. Keep class-based closing formula (formal or informal based on class)
4. Flag case for manual review in the output files

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
1. Use formal "Sie" (works as gender-neutral in written German)
2. Use gender-neutral adjective forms where possible
3. Use neutral greeting fallback: `Guten Tag [First Name] [Last Name],`
4. Flag in output files for manual review

### Consistency Checklist

Before finalizing any grading output, verify:
- [ ] Email greeting matches body address style (Sie or Du)
- [ ] All pronouns in body refer to student as "Sie" or "Du"
- [ ] No third-person references to the student ("der Schüler", "die Studentin")
- [ ] Verb conjugation matches address style
- [ ] Closing formula matches address style

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

1. Match student by name (handle variations and partial matches)
2. Normalize class comparison to uppercase: `WHERE UPPER(klasse) = UPPER(?)`
3. Retrieve `email` and `klasse` columns
4. Use `klasse` to determine address style
5. If `vacuum.db` is missing at start, stop immediately with error
6. Track all students with missing email addresses

## Missing Email Address Handling (CRITICAL)

When generating `EMAIL.json`, if any student's email address cannot be found in
the database, the workflow MUST stop before generating the file.

### Protocol

1. **Collect all lookups**: Perform database lookup for all students first
2. **Check for missing emails**: After all lookups, identify students without
   valid email addresses
3. **If any are missing**:
   - STOP immediately
   - Do NOT generate `EMAIL.json`
   - Present ALL unresolved names to the user in a clear list:
     ```
     Die folgenden Schüler/innen konnten nicht in der Datenbank gefunden werden:
     - [Name 1]
     - [Name 2]
     - ...
     
     Bitte aktualisieren Sie die Datenbank und starten Sie den Vorgang erneut.
     ```
   - Wait for user to update the database
   - User should confirm when database is updated
   - Retry the entire grading process
4. **Only proceed**: Generate `EMAIL.json` when ALL students have valid email
   addresses

### Rationale

- Prevents incomplete or invalid email payloads
- Ensures all students receive their feedback
- Forces database maintenance rather than workarounds

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

## Constraints

- All grading content must be written in German
- All grading content must use second-person address (Sie or Du)
- Never use third-person to refer to the student being graded
- UTF-8 encoding with natural German umlauts (ä, ö, ü, ß); never replace with
  transliterations (ae, oe, ue) unless source material requires it
- Trailing comma required in all salutations
- Two newlines before signature line
- Three-space indentation before `Georg Graf`
- Never guess gender - use neutral fallback when uncertain
- Flag uncertain cases for manual review

## Repository Analysis Protocol

Shared pre-grading verification and analysis steps for all repository-based
grading skills (`repograde`, `repogradesince`, `projectgrade`).

### Pre-Grading Verification

Before inspecting repository content, verify repository state:

1. Navigate to the student repository directory
2. Run `git pull` to ensure latest version is checked out
3. Run `git status` to check for uncommitted changes
4. If uncommitted changes exist, STOP IMMEDIATELY and report to user
5. If pull fails or reports errors, STOP IMMEDIATELY and report to user

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

- substantive: meaningful implementation, debugging, refactoring, feature work
- superficial: formatting-only edits, whitespace changes, trivial renames,
  auto-generated files without meaningful modification

Consider common patterns across JavaScript, Java, C#, SQL, CSS, HTML, and
general programming constructs.

### Branch and Activity Analysis

- Focus primarily on `main`, but highlight significant non-main branch work.
- Count commits over time.
- Detect inactive gaps between first and last relevant commits.
- Use evidence-based diligence signals such as `high`, `medium`, or `low`.

## Homework Discovery Protocol

Shared homework source discovery for `repograde` and `repogradesince`.
Homework assignments may exist in multiple locations. The grading skill MUST
discover and merge all sources into a unified homework list before matching
against student commits.

### Source 1: `_class` Symlink (Preferred)

Check for a `_class` symlink in the CWD. If it exists, follow it and look for
homework inside the linked class folder.

#### 1a: Legacy Cumulative File

Check for `Hausübungen.md` inside `_class/` (may also be a symbolic link;
follow symlinks when reading).

If found, parse it using the Semantic Date Extraction rules below.

#### 1b: Per-Lesson Files inside `_class`

Scan `_class/` for subdirectories matching the pattern `<YYYY-MM-DD>_<topic>`.
For each matching directory, check if `Hausübung.md` exists inside it.

If found:
- Extract the date directly from the directory name (e.g., `2026-03-21_promises`
  → date `2026-03-21`). No German date parsing needed.
- Extract the topic from the directory name and/or the file content.
- Read the file content for assignment details.
- Add to the homework list: `(iso_date, topic, content)`.

### Source 2: Legacy File in CWD

Check for a `Hausübungen.md` file directly in the CWD (may be a symbolic link;
follow symlinks when reading). This is the old symlink-to-single-file approach.
If found, parse it using the Semantic Date Extraction rules below.

#### Semantic Date Extraction

**You MUST perform a thorough semantic analysis of the entire file.**

Many agents fail at this step because they:
- Only read the first entry
- Miss dates embedded in the text (not just headings)
- Fail to convert German date formats to ISO
- Skip entries that don't match a naive pattern match

Required steps:

1. **Read the ENTIRE file** — do not stop after the first homework entry
2. **Extract ALL date references** from:
   - Headings: `## Hausübung vom 18. Februar`
   - Inline dates: `Abgabe bis 25. Februar`
   - Date ranges: `Zeitraum: 10.-18. März`
   - Relative dates: `nächste Woche`, `in 2 Wochen` (convert to absolute)
3. **Normalize ALL dates to ISO format** (YYYY-MM-DD)
4. **Build a homework list**: `[(iso_date, topic, content), ...]`

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
         requested date is 2026-02-10, conclude "no matching homework"
✅ CORRECT: Parse ALL entries, find "vom 10. Februar" (matches),
            "vom 18. Februar" (after cutoff), "vom 25. Februar" (after cutoff)
```

### Source 3: Per-Lesson Files in CWD

Scan the CWD itself for subdirectories matching `<YYYY-MM-DD>_<topic>` that
contain `Hausübung.md`. This covers per-lesson homework without a `_class`
symlink.

### Merging All Sources

1. Collect homework entries from all sources into a single unified list.
2. If multiple sources contain an entry for the same date, prefer the per-lesson
   file over the legacy cumulative file. This is expected to be rare.
3. Sort the unified list by date.
4. If no source provides any homework entries, report this to the user and grade
   based on available work only.

## Bulk Grading Protocol

Shared concurrency and directory handling for `repograde` and `repogradesince`
bulk modes.

### Directory Exclusion

When enumerating student repositories, **exclude**:
- `_class` (homework symlink)
- Any directory starting with `_` (underscore prefix)
- Any directory starting with `.` (dot prefix)

These excluded directories are NOT student repositories and must never be graded.

### Concurrency

- Default maximum: 5 repositories in progress at once.
- When one grading run completes, start the next after an approximately
  3-second delay.
- Each subagent must derive its output stem from the repository basename and
  write only `<basename>_grading.md` plus `<basename>_email.json`.
- Subagents must never write shared `EMAIL.json`.

### Aggregation

After all subagents finish, the master workflow must:
1. Read the generated `*_email.json` files.
2. Create shared `EMAIL.json` following the Email JSON Structure rules above.

## Reporting Protocol

All grading content must be written in German and address the student directly
in the second person (Sie or Du based on class). See the Second-Person Address
section above for pronoun usage and examples.

Reports should include, where applicable:

- repository overview
- homework-by-homework summary
- topic coverage
- per-commit technical analysis
- non-main branch activity
- activity over time
- inactive gaps
- diligence assessment
- final evaluation with `Endbewertung: XX/100`

### Second-Person Tone Examples

**Informal (2ahwii, 3ahwii, 5ahwii, 4aaif):**

```
## Repository-Übersicht

Du hast in diesem Semester durchweg solide Arbeit geleistet. Dein
Repository zeigt eine klare Struktur und regelmäßige Commits.

## Hausübungen

### HU1: SQL-Grundlagen
Du hast die JOIN-Operationen korrekt implementiert. Besonders positiv
ist, dass du die Fremdschlüssel-Beziehung sauber modelliert hast.
```

**Formal (all other classes):**

```
## Repository-Übersicht

Sie haben in diesem Semester durchweg solide Arbeit geleistet. Ihr
Repository zeigt eine klare Struktur und regelmäßige Commits.

## Hausübungen

### HU1: SQL-Grundlagen
Sie haben die JOIN-Operationen korrekt implementiert. Besonders positiv
ist, dass Sie die Fremdschlüssel-Beziehung sauber modelliert haben.
```

## Output Expectations

This skill provides configuration and shared protocols. Consuming skills
produce:
- Per-student `*_grading.md` files with individual feedback (second-person German)
- `EMAIL.json` with personalized payloads (second-person body)
- `GRADINGS.md` class-wide overview (where applicable)
- `CLASS.md` anonymized class patterns (where applicable)
