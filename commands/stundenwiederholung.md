---
description: Turn the audio transcript /tmp/issue.md into a README.md recap in today's lesson folder
---
Recap a lesson that was just held into the day folder's `README.md`, based on
the raw audio transcript in `/tmp/issue.md`. Run this right after a lesson,
from inside the teaching repo.

## 1. Pre-flight (stop on any failure, leave /tmp/issue.md in place)

1. **Transcript present** — `/tmp/issue.md` must exist and be non-empty. If
   not, stop with a clear error.
2. **Inside a Git work tree** — run `git rev-parse --is-inside-work-tree`. If
   it fails or returns nothing, stop with an error.
3. **Find the day folder** —
   `find . -type d -name "$(date +%F)*" -not -path './.git/*'`
   - The optional argument `$1` (ISO date `YYYY-MM-DD`) overrides "today".
   - **No match** → stop and tell the user to create the folder first
     (`<klasse>/YYYY-MM-DD__thema/`).
   - **More than one match** → list the candidates and ask the user which one
     belongs to this lesson. Never guess.

## 2. Reconstruct the lesson from the transcript

The transcript is garbled and full of interjections, side conversations and
technical fumbling. Extract only what the class actually covered:

- the **topics and concepts** taught, with the exact terminology used
- the **key definitions, formulas and worked examples**
- the **R functions / commands** mentioned and what they do
- the **homework** the teacher announced; if none was clearly announced,
  propose one and mark it explicitly as *Vorschlag*
- where the class **struggled or something was left open**

Mark anything uncertain as `(unklar)`. **Never invent content** the transcript
does not support.

Cross-check terminology and links against the day folder's `lesson.html`, the
matching `lehrplan/kompetenzmodule/km*.md`, and
`lehrplan/pmm-hwit/jg*-semesterplan-*.md`, so the recap matches the material.
Only link files/targets that actually exist (verify with `ls` / glob).

## 3. Merge into README.md (never clobber existing notes)

If `<Tagesordner>/README.md` already exists (the teacher writes notes live
during class), **preserve every existing line**. Integrate the generated
sections; do not delete or rewrite the teacher's text, and do not duplicate
sections that already exist. Otherwise create the file.

Keep it a *sensitive middle ground*, roughly 50–100 lines — a recap, not a
full lesson. Write in **German**, with **relative** links only (no `<base>`,
no root-absolute paths). Target structure:

1. `# <Thema> (<Datum>)` — reuse an existing title if one is present
2. `## Das war die Stunde` — the contents as short bullets
3. `## Erklärungen & Nachlesen` — relative links: `lesson.html` in the same
   folder, the relevant KM file, the semester plan, R4DS chapters, and
   optionally short explainer videos (only verified links)
4. `## Aufgabe bis zum nächsten Mal` — the announced homework; if none was
   announced, a clearly marked *Vorschlag*
5. `## Housekeeping` — KM reference, semester-plan link, runtime
   (R / RStudio, tidyverse)

## 4. Archive the transcript

Move `/tmp/issue.md` to `<Tagesordner>/transcript.md` (raw transcript, for the
record). The teaching repo is public, so the transcript — which contains
students' voices and names — must **not** be committed. Ensure `transcript.md`
(and R artifacts `RData`/`Rhistory` patterns) are listed in the repo's
`.gitignore`; append the missing lines if needed.

## 5. Issue + commit

The teaching repo requires an issue number on every commit:

1. Use the `issue-workflow` skill to create a new GitHub issue — title like
   `Stundenwiederholung <Datum>: <Thema>`, body = a short summary of what the
   transcript contained.
2. Commit the new/changed `README.md` (and `.gitignore` if it changed) with the
   issue reference, preserving the repo's commit style.
3. Push to the trunk line. Do **not** commit `transcript.md` or R artifacts.

## 6. Report

State at the end: the day folder, whether the README was created or merged,
the archived transcript location, the issue number, and the commit hash.
