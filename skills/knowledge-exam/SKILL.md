# Knowledge Exam Skill

## Purpose

This skill creates a German knowledge-check exam for a specific class folder
based on recent Git history. Use it when asked to generate a mini-exam from the
material covered in class.

## Inputs

- `class`: target class folder name
- `weeks`: number of weeks of Git history to analyze

## Protocol

### 1. Validate Inputs

- Confirm that a folder matching `class` exists in the current working tree.
- If the folder does not exist, stop immediately and report that the class name
  appears to be invalid.
- Compute today's ISO date for the output filenames.

### 2. Inspect Source Material

- Analyze Git commits from the last `weeks` weeks that changed files inside the
  class folder.
- Treat minimal commits as lecture anchors rather than complete coverage; infer
  the broader classroom context from the changed material in those commits.
- Review the changed files as needed to understand the topics that were likely
  taught.

### 3. Generate Exam Files

- Create `knowledge_<class>_<isodate>.md` inside the class folder.
- Write the exam in German.
- Include exactly 12 multiple-choice questions.
- Each multiple-choice question must have 1 to 4 correct answers.
- Each multiple-choice question is worth 2 points.
- For every multiple-choice question, explicitly allow students to mark `-`
  and briefly explain why they consider the answer ambiguous or
  context-dependent.
- Include exactly 3 free-form questions.
- Each free-form question is worth 8 points.

### 4. Generate Solution File

- Create `knowledge_<class>_<isodate>_solutions.md` in the same folder.
- Write the teacher solutions in German.
- Keep the student-facing exam and the solution file separate.
- Do not include the solutions in the student-facing exam file.

### 5. Constraints

- Do not commit any generated files.
- Preserve existing files unless the task explicitly requires replacement.
- Follow the repository convention that `**/*_solutions.md` stays git-ignored.

## Output Expectations

- Student exam file in German with the required question counts and scoring.
- Separate teacher solution file in German.
- Filenames must include the class name and today's ISO date.
