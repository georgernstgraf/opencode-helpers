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
ensuring consistent email formatting, address styles, and database access
across different assessment types.

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
2. Check if class is in the informal list above
3. Apply corresponding address style throughout

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
4. Flag case for manual review

## Database Access

### Databases

| Database | Path | Purpose |
|----------|------|---------|
| UploadThing | `/home/georg/OneDrive/uploadthing.db` | Repository grading |
| Vacuum | `vacuum.db` (current directory) | Knowledge-check grading |

### Schema

Table: `users`

| Column | Description |
|--------|-------------|
| `email` | Student email address |
| `name` | Full student name |
| `klasse` | Class identifier |

### Lookup Protocol

1. Match student by name (handle variations and partial matches)
2. Retrieve `email` and `klasse` columns
3. Use `klasse` to determine address style
4. If not found, set `mailto: null` and add `note` field for manual review

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
- Include full assessment content (long emails expected)
- Preserve paragraph spacing and readable newline structure
- Include greeting at start
- Include closing formula at end
- UTF-8 encoding with natural German umlauts (ä, ö, ü, ß)

## Constraints

- All grading content must be written in German
- Trailing comma required in all salutations
- Two newlines before signature line
- Three-space indentation before `Georg Graf`
- Never guess gender - use neutral fallback when uncertain
- Flag uncertain cases for manual review

## Output Expectations

This skill provides configuration only. Consuming skills produce:
- Individual assessment files
- EMAIL.json with personalized payloads
- Class-wide reports (anonymized)
