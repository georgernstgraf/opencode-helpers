# opencode-helpers

Reusable AI agent configuration templates for [opencode](https://opencode.ai) projects.

## Purpose

This repository provides standardized commands, skills, and knowledge persistence
patterns for AI-assisted development workflows. Copy the files you need into your
project to supercharge your opencode sessions.

## Structure

```
opencode-helpers/
├── commands/           # Slash commands for opencode
│   ├── save.md         # Persist session knowledge to docs/ai/
│   ├── knowledge.md    # Thin wrapper for exam-generation skill
│   ├── knowledge-assess.md  # Thin wrapper for assessment skill
│   ├── issue-start.md  # Start working on a GitHub issue
│   ├── issue-commit.md # Save progress to an issue
│   ├── issue-finish.md # Complete task and close issue
│   ├── nextprompt.md   # Process next transcription
│   └── security.md     # Security audit report
├── skills/             # Reusable skill definitions
│   ├── knowledge-persistence/  # Persist agent knowledge across sessions
│   ├── knowledge-exam/ # Generate exams from git history
│   ├── knowledge-assessment/   # Assess student submissions
│   └── orchestrator/   # Manage complex multi-step tasks
├── docs/ai/            # Knowledge persistence templates
│   ├── HANDOFF.md      # Pending tasks for next session
│   ├── CONVENTIONS.md  # Coding conventions
│   ├── DECISIONS.md    # Architectural decisions
│   ├── PITFALLS.md     # Things that don't work
│   ├── DOMAIN.md       # Business/domain knowledge
│   └── STATE.md        # Current project state
└── AGENTS.md           # Bootstrap config for AI agents
```

## Quick Start

1. Copy `AGENTS.md` to your project root
2. Copy any commands you need to `commands/` in your project
3. Copy any skills you need to `skills/` in your project
4. Copy `docs/ai/` directory to persist knowledge across sessions
5. Customize the files for your project

## Commands

| Command | Description |
|---------|-------------|
| `/save` | Persist session knowledge to `docs/ai/` files |
| `/knowledge <class> <weeks>` | Run the exam-generation skill for a class |
| `/knowledge-assess` | Run the assessment skill for student submissions |
| `/issue-start [issue\|#new]` | Start or continue working on a GitHub issue |
| `/issue-commit` | Save progress to an issue (keeps it open) |
| `/issue-finish` | Complete task, commit, push, and close issue |
| `/nextprompt` | Process oldest transcription via aitranscribe |
| `/security <output>` | Generate security audit report |

## Skills

### knowledge-persistence

Extracts accumulated understanding from a session and persists it to structured
knowledge files. Use at the end of productive sessions or when asked to "save context".

The intended persisted output is the `docs/ai/` knowledge set:

- `HANDOFF.md` for open tasks and next-session context
- `CONVENTIONS.md` for ongoing rules and working patterns
- `DECISIONS.md` for durable choices with rationale
- `PITFALLS.md` for hard-won constraints and non-obvious failures
- `DOMAIN.md` for business or domain rules when relevant
- `STATE.md` for the current focus, completed work, pending work, and blockers

The `/save` command is the entrypoint for this workflow. In this template repo,
the command and skill document the intended behavior clearly so projects can
adopt or implement the persistence flow consistently.

### knowledge-exam

Generates German mini-exams and separate solution files from recent Git history
for a given class folder. The workflow uses 10 multiple-choice questions with 4
answer options each and 3 free-text questions. Multiple-choice questions are
scored per option, and free-text questions are worth 15 points each.

### knowledge-assessment

Grades student knowledge-check submissions, writes German reports, and produces
bulk email JSON payloads. The assessment uses the same point-based model as the
exam skill instead of an Austrian school grading scheme.

### orchestrator

Manages complex, multi-step tasks requiring architectural planning and systematic
execution. Use for features involving 3+ files or non-linear solutions.

## Command vs Skill

- Use a command when the main value is a short, ergonomic entrypoint with a few
  arguments.
- Promote the workflow into a skill when the instructions grow into a reusable
  protocol with multiple steps, constraints, outputs, or decision rules.
- Prefer thin commands that pass context into a dedicated skill rather than
  embedding long operational procedures directly in the command file.

## Knowledge Files (`docs/ai/`)

The `docs/ai/` directory maintains context across AI sessions:

- **HANDOFF.md** - Pending tasks for the next session
- **CONVENTIONS.md** - Coding patterns and style rules to follow
- **DECISIONS.md** - Architectural decisions with rationale
- **PITFALLS.md** - Hard-won knowledge about what doesn't work
- **DOMAIN.md** - Business logic not obvious from code
- **STATE.md** - Current project status and focus

## Use Cases

This template is particularly useful for:

- **Educational projects** - Create exams from git history, assess submissions
- **GitHub-integrated workflows** - Issue tracking with AI assistance
- **Knowledge persistence** - Maintain context across AI sessions
- **Security audits** - Structured security analysis

## License

MIT

## Contributing

Issues and PRs welcome at [github.com/georgernstgraf/opencode-helpers](https://github.com/georgernstgraf/opencode-helpers)
