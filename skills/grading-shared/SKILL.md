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
6. If student not found, set `mailto: null` and add `note` field for manual review

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
- Trailing comma required in all salutations
- Two newlines before signature line
- Three-space indentation before `Georg Graf`
- Never guess gender - use neutral fallback when uncertain
- Flag uncertain cases for manual review

## Output Expectations

This skill provides configuration only. Consuming skills produce:
- Per-student `*_grading.md` files with individual feedback (second-person German)
- `EMAIL.json` with personalized payloads (second-person body)
- `GRADINGS.md` class-wide overview (where applicable)
- `CLASS.md` anonymized class patterns (where applicable)
