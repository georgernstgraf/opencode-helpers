# Repograde Report Format

Mandatory structure and section-content requirements for `<basename>_grading.md`
reports, plus the standardization rules for subagents.

## Reporting Expectations

Reports MUST follow `grading-shared` Reporting Protocol (in German) and additionally include:

- If date-filtered: clear indication of the cutoff date.
- **Hausübungs-Abdeckung section**: Complete list of all assigned homeworks
  with completion status and Abdeckungsquote percentage.
- **Weighted final evaluation**: Base score x completion ratio.
- Final evaluation with `Endbewertung: XX/100` (the weighted score, not base).

### Mandatory `*_grading.md` Structure (EXACT ORDER)

Every repository grading report MUST use exactly the following top-level
sections in exactly this order:

```markdown
# Bewertung: [Repository Basename]

## Rahmen

## Commit-Überblick

## Pünktlichkeit der Abgaben

## Hausübungs-Abdeckung

## Codequalität

## Konkrete technische Beobachtungen

## Stärken

## Verbesserungspotenzial

## Endbewertung
```

Do NOT rename, merge, omit, or reorder these sections.

### Section Content Requirements

#### `## Rahmen`

This section MUST state:

- whether all commits or only commits from a cutoff date onwards were graded,
- the grading period in plain German,
- the number of relevant homework assignments in the grading period,
- whether the repository contained enough evidence for a confident assessment.

Target length: 2-4 sentences.

#### `## Commit-Überblick`

This section MUST state, when determinable:

- total number of relevant commits,
- approximate number of substantive commits,
- approximate number of superficial commits,
- activity pattern (`regelmäßig`, `phasenhaft`, `stark gebündelt`, etc.),
- notable inactive gaps or bursts.

Target length: 2-3 sentences.

If exact substantive/superficial counts cannot be determined confidently, say
so explicitly and provide the best evidence-based approximation.

#### `## Pünktlichkeit der Abgaben`

This section MUST cover every homework assignment in the grading period.
For each homework, state the concrete deadline date (calculated per
`grading-shared` Deadline Calculation) and classify as one of:

- `pünktlich` — latest relevant commit ≤ deadline (YYYY-MM-DDT00:00:00)
- `verspätet` — latest relevant commit > deadline
- `nicht erkennbar abgegeben` — no relevant commits found

Use one bullet per homework. Include the deadline timestamp and the date of
the latest relevant commit as evidence. Keep each bullet to 1-2 sentences.

Example: `HÜ1 (23.2.): pünktlich — letzter Commit am 1.3. ≤ Deadline 2.3. 00:00`

#### `## Hausübungs-Abdeckung`

This section MUST list all relevant homework assignments and state for each
whether the work was completed, partially completed, or missing.

For each homework, include:

- short homework label/topic,
- status (`erfüllt`, `teilweise erfüllt`, `fehlend`),
- one short evidence-based explanation.

This section MUST end with:

- `Abdeckungsquote: XX%`
- `Abgedeckte Hausübungen: X von Y`

#### `## Codequalität`

This section MUST discuss the quality of the visible work under these lenses:

- correctness,
- structure/organization,
- readability,
- technical understanding.

Target length: 3-5 sentences.

Avoid vague praise. Use concrete observations tied to repository evidence.

#### `## Konkrete technische Beobachtungen`

This section MUST contain exactly 2-4 bullet points.

Each bullet MUST describe a concrete technical observation from the repository,
for example:

- a correct implementation decision,
- a recurring bug pattern,
- an incomplete feature,
- a meaningful refactoring,
- a SQL / HTML / CSS / JS / Java / C# detail visible in the diffs.

Each bullet should be one concise evidence-based sentence. Do not repeat the
same point in multiple bullets.

#### `## Stärken`

This section MUST contain exactly 2 bullet points.

Each bullet should describe a genuine strength visible in the student's work.
Keep the tone understated and factual.

#### `## Verbesserungspotenzial`

This section MUST contain exactly 2 bullet points.

Each bullet should describe a concrete improvement target that follows directly
from the observed repository evidence.

#### `## Endbewertung`

This section MUST contain the Scoring Table as defined in Per-Homework
Scoring (see above), followed by:

```
Erreichte Punkte: [sum] / [N × 100]
Endbewertung: [XX]/100 ([XX]%)
```

The scoring table MUST list ALL homework assignments in the grading period
with their individual Quality, Factor, and Effective score. Use `—` for
missing homeworks (Quality and Effective = 0%).

The Endbewertung is calculated as `round(sum(effective_scores) / (N × 100) × 100)`.

This section MUST also include one short concluding paragraph that explains
why the final result is appropriate.

### Standardization Rules for Subagents

In bulk mode, every subagent MUST follow these normalization rules:

1. Use the exact top-level headings above.
2. Keep section lengths within the target ranges.
3. Include all required metrics even when the values are low.
4. If evidence is missing, write that explicitly; do not skip the section.
5. Do not add extra top-level sections.
6. Do not switch to essay style or dramatically longer prose for some students.
7. Base all statements on repository evidence, not on speculation.
