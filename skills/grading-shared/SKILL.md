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

Every grading email body MUST include a disclaimer paragraph directly below the greeting. The wording depends on the class's address style (Formal/Informal) and the assessment type (Homework/Projects vs. Knowledge-Checks):

**Formal Address (Sie):**
- **Homework / Projects / General (Leistungsfeststellung):**
  `Im Folgenden finden Sie die automatische Beurteilung Ihrer Leistungsfeststellung. Bitte beachten Sie, dass diese Beurteilung Irrtümer enthalten kann.`
- **Knowledge-Checks / Mini-Exams (Knowledge-Check):**
  `Im Folgenden finden Sie die automatische Beurteilung Ihres Knowledge-Checks. Bitte beachten Sie, dass diese Beurteilung Irrtümer enthalten kann.`

**Informal Address (Du):**
- **Homework / Projects / General (Leistungsfeststellung):**
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

1. **Task instructions** — the homework description, exam questions, or project
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

## Homework Discovery Protocol

Shared homework source discovery for `repograde` and `projectgrade`.
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
For each matching directory, check for homework content in these files
(in order of preference):

1. `Hausübung.md` — dedicated homework file (legacy format)
2. `Angabe_HÜ.md` — detailed homework specification
3. `README.md` — lesson plan containing a homework section

When a file is found:
- Extract the date directly from the directory name (e.g., `2026-03-21_promises`
  → date `2026-03-21`). No German date parsing needed.
- Extract the topic from the directory name and/or the file content.
- For `README.md`, locate the homework section under one of these headings:
  `## 📝 Hausübung`, `## Hausübung`, or `## 📝 Hausübung`.
  If the section states "Keine Hausübung" (no homework), skip this lesson.
- Read the file content for assignment details.
- Add to the homework list: `(iso_date, topic, content)`.

#### 1c: Future Lesson Exclusion

Per-lesson directories with a date in the future represent prepared but
not-yet-held lessons. Their homework assignments MUST NOT be included in
the unified homework list.

1. Determine today's date: `date +%Y-%m-%d`
2. For each per-lesson directory, extract `<YYYY-MM-DD>` from the name.
3. If `lesson_date > today`, skip this directory entirely.
4. Do NOT include its homework, regardless of whether a homework section
   exists in the file.

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

1. **Read the ENTIRE file** — do not stop after the first homework entry.
2. **Extract ALL date references** from:
   - Headings: `## Hausübung vom 18. Februar`
   - Inline dates: `Abgabe bis 25. Februar`
   - Date ranges: `Zeitraum: 10.-18. März`
   - Relative dates: `nächste Woche`, `in 2 Wochen` (convert to absolute)
3. **Normalize ALL dates to ISO format** (YYYY-MM-DD).
4. **Build a homework list**: `[(iso_date, topic, content), ...]`.

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
contain homework content (same file search order as Source 1b: `Hausübung.md`,
`Angabe_HÜ.md`, `README.md`). Apply Future Lesson Exclusion (1c) identically.

### Merging All Sources

1. Collect homework entries from all sources into a single unified list.
2. If multiple sources contain an entry for the same date, prefer the per-lesson
   file over the legacy cumulative file. This is expected to be rare.
3. Sort the unified list by date.
4. If no source provides any homework entries, report this to the user and grade
   based on available work only.

## Deadline Calculation

### Determining the Deadline

Homework is due at 00:00 on the same weekday one week after the lesson.
Since all lessons in a given course fall on the same weekday, the deadline is
always:

```
deadline = lesson_date + 7 days, at 00:00:00
```

Subagents MUST use shell date arithmetic for reliable calculation:

```bash
DEADLINE=$(date -d "2026-02-23 +7 days" +%Y-%m-%dT00:00:00)
```

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
| > DEADLINE             | verspätet      | 0.75   | 25% penalty on achieved quality |
| No commits             | fehlend        | —      | 0 points for this homework |

### Deadline in Reports

Reports MUST mention the concrete deadline for each homework, including the
exact `YYYY-MM-DDT00:00:00` timestamp and whether the student's latest
relevant commit fell before or after it.

## Bulk Grading Protocol

Shared concurrency and directory handling for `repograde` bulk mode.

### Directory Exclusion

When enumerating student repositories, **exclude**:
- `_class` (homework symlink)
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

### Structure for Homework Grading Emails

Used by `repograde` skill (single-repo and bulk mode). The email body follows
this exact paragraph order:

1. **Greeting** — per Greeting Formulas section above.

2. **Automatic assessment disclaimer** — per Automatic Assessment Disclaimers section above.

3. **Opening sentence** (address style dependent):
   - Formal: `Ich habe Ihre Hausübungen, welche im Zeitraum vom [Start-Datum] bis zum [End-Datum] aufgegeben waren, durchgesehen.`
   - Informal: `Ich habe deine Hausübungen, welche im Zeitraum vom [Start-Datum] bis zum [End-Datum] aufgegeben waren, durchgesehen.`
   - Dates in German long format (e.g., "18. Februar 2026", "4. März 2026").

3. **Commit summary** — Two to three sentences summarizing the commits
   discovered in the student's repository during the grading period.
   Mention overall activity, approximate number of substantive commits,
   and any notable patterns (gaps, bursts, consistent work).

4. **Homework overview** — A concise list of all homework assignments,
   each in one to two sentences. Format:

   ```
   HÜ1: [Topic/content summary in 1-2 sentences]
   HÜ2: [Topic/content summary in 1-2 sentences]
   ```

   Use "HÜ" as abbreviation for "Hausübung". Number sequentially.

5. **Per-homework evaluation** — For each homework assignment, provide
   a detailed discussion and evaluation on a 0–100% scale. Each evaluation
   is a separate paragraph covering:
   - What the student did well.
   - What was missing or could be improved.
   - Specific technical observations (with code snippets where helpful).
   - A percentage rating for that individual homework.

6. **Coverage / timeliness summary** — One short paragraph summarizing overall
   homework coverage and whether submissions were on time, late, partial, or
   missing where relevant.

7. **Recommendations and praise** — A warm, genuine paragraph with
   improvement suggestions and subtle praise. See Praise Guidelines below.

8. **Final score summary** — One short paragraph containing the final weighted
   result in the form `Endbewertung: XX/100 (XX%)`.

9. **Closing** — per Closing Formulas section above.

Keep email length reasonably consistent across students. Do not omit one of the
paragraph groups above simply because a repository is weaker or stronger; if
evidence is limited, say so briefly and continue with the same structure.

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

5. **Recommendations and praise** — Same guidelines as homework emails.

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

### Example: Formal Homework Email Body

```
Sehr geehrte Frau Huber,

im Folgenden finden Sie die automatische Beurteilung Ihrer Leistungsfeststellung. Bitte beachten Sie, dass diese Beurteilung Irrtümer enthalten kann.

Ich habe Ihre Hausübungen, welche im Zeitraum vom 4. März bis zum
18. März aufgegeben waren, durchgesehen.

In Ihrem Repository habe ich insgesamt 12 Commits in diesem Zeitraum
gefunden. Die Arbeit war regelmäßig verteilt, mit einem deutlichen
Schwerpunkt in der ersten Woche. Die meisten Änderungen betrafen
SQL-Skripte und Datenbank-Schema-Dateien.

HÜ1: Erstellung einer SQL-Datenbank mit CREATE TABLE und INSERT
statements für ein Bibliotheksverwaltungssystem.
HÜ2: Implementierung von JOIN-Operationen zwischen den Tabellen
der Bibliotheksdatenbank.

HÜ1 – Bibliotheksdatenbank:

Sie haben die Tabellenstruktur sauber entworfen und die
Fremdschlüsselbeziehungen korrekt definiert. Die INSERT-Statements
decken die wesentlichen Daten ab. Bei der Tabelle "Ausleihe" hätte
das Rückgabedatum als nullable Spalte definiert werden sollen, da
ein Buch zum Zeitpunkt der Ausleihe noch nicht zurückgegeben sein
muss. Bewertung: 80%.

HÜ2 – JOIN-Operationen:

```sql
SELECT b.Titel, a.Name
FROM Buecher b
JOIN BuchAutor ba ON b.BuchID = ba.BuchID
JOIN Autoren a ON ba.AutorID = a.AutorID;
```

Dieser Dreifach-Join ist korrekt umgesetzt. Die Alias-Namen sind
sinnvoll gewählt. Bei der LEFT JOIN-Aufgabe fehlt jedoch die
Berücksichtigung von Büchern ohne Ausleihe – hier wäre ein LEFT
JOIN statt des INNER JOIN nötig gewesen. Bewertung: 65%.

Insgesamt zeigen Ihre Abgaben ein solides Grundverständnis der
relationalen Datenbankkonzepte. Es empfiehlt sich, die
Unterschiede zwischen den JOIN-Typen (INNER, LEFT, RIGHT) noch
einmal anhand praktischer Beispiele nachzuvollziehen. Die
Tabellenstruktur der Bibliotheksdatenbank ist Ihnen gut gelungen.

Beide Hausübungen waren erkennbar abgegeben. Die erste Aufgabe war
weitgehend vollständig, bei der zweiten Aufgabe gab es inhaltliche
Lücken bei einzelnen JOIN-Varianten.

Insgesamt ist eine solide Grundlage erkennbar. Es lohnt sich, die
Behandlung unvollständiger Ergebniszeilen bei LEFT JOINs noch gezielt
zu üben.

Endbewertung: 73/100 (73%)

Mit freundlichen Grüßen,

   Georg Graf
```

### Example: Informal Homework Email Body

```
Lieber Thomas,

im Folgenden findest du die automatische Beurteilung deiner Leistungsfeststellung. Bitte beachte, dass diese Beurteilung Irrtümer enthalten kann.

Ich habe deine Hausübungen, welche im Zeitraum vom 4. März bis zum
18. März aufgegeben waren, durchgesehen.

In deinem Repository habe ich 8 Commits gefunden, die meisten davon
in der zweiten Woche. Du hast dich intensiv mit den SQL-Themen
auseinandergesetzt.

HÜ1: Erstellung einer SQL-Datenbank mit CREATE TABLE und INSERT
statements für ein Bibliotheksverwaltungssystem.
HÜ2: Implementierung von JOIN-Operationen zwischen den Tabellen
der Bibliotheksdatenbank.

HÜ1 – Bibliotheksdatenbank:

Du hast die Tabellen korrekt erstellt und die Beziehungen sauber
modelliert. Die Datentypen sind durchgehend passend gewählt.
Die Index-Definitionen fehlen allerdings vollständig – bei einer
Bibliotheksdatenbank mit Suchanfragen auf Titel und Autor wären
Indizes sinnvoll. Bewertung: 75%.

HÜ2 – JOIN-Operationen:

Die einfachen JOINs hast du zuverlässig implementiert. Bei den
komplexeren Abfragen mit Unterabfragen gibt es noch Unsicherheiten.
Die Lösung für "Alle Autoren mit mehr als 3 Büchern" verwendet
einen korrekten Ansatz, die Gruppierung ist aber nicht ganz
vollständig. Bewertung: 60%.

Insgesamt eine ordentliche Leistung. Es wäre hilfreich, wenn du
die JOIN-Typen noch einmal wiederholst – besonders die Fälle,
in denen ein LEFT JOIN nötig ist. Die Grundlagen sitzen, und mit
etwas mehr Übung bei den komplexeren Abfragen wirst du noch
sicherer.

Beide Hausübungen sind erkennbar bearbeitet. Bei der zweiten Aufgabe
zeigen sich aber noch Lücken bei den komplexeren Abfragen.

Insgesamt ist das eine brauchbare Arbeitsgrundlage. Wenn du die
Unterschiede der JOIN-Typen noch sicherer anwenden kannst, wird die
Qualität der Lösungen deutlich steigen.

Endbewertung: 68/100 (68%)

Lieben Gruß,

   Georg Graf
```

## Reporting Protocol

All grading content must be written in German and address the student directly
in the second person (Sie or Du based on class). See the Second-Person Address
section above for pronoun usage and examples.

The `*_grading.md` files may use full Markdown formatting (headers, bold,
tables, lists). Only the email body in `*_email.json` is restricted to plain
text per the Email Body Format section above.

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

## Output Expectations

This skill provides configuration and shared protocols. Consuming skills
produce:
- Per-student `*_grading.md` files with individual feedback (second-person German).
- `EMAIL.json` with personalized payloads (second-person body).
- `GRADINGS.md` class-wide overview (where applicable).
- `CLASS.md` anonymized class patterns (where applicable).
