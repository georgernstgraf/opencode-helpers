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
│   ├── save.md         # Persist session knowledge to _agents/
│   ├── knowledge.md    # Create mini-exams from git history
│   ├── knowledge-assess.md  # Assess student submissions
│   ├── issue-start.md  # Start working on a GitHub issue
│   ├── issue-commit.md # Save progress to an issue
│   ├── issue-finish.md # Complete task and close issue
│   ├── nextprompt.md   # Process next transcription
│   └── security.md     # Security audit report
├── skills/             # Reusable skill definitions
│   ├── knowledge-persistence/  # Persist agent knowledge across sessions
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
| `/knowledge <class> <weeks>` | Create mini-exam from recent git commits |
| `/knowledge-assess` | Assess student submissions against solutions |
| `/issue-start [issue\|#new]` | Start or continue working on a GitHub issue |
| `/issue-commit` | Save progress to an issue (keeps it open) |
| `/issue-finish` | Complete task, commit, push, and close issue |
| `/nextprompt` | Process oldest transcription via aitranscribe |
| `/security <output>` | Generate security audit report |

## Skills

### knowledge-persistence

Extracts accumulated understanding from a session and persists it to structured
knowledge files. Use at the end of productive sessions or when asked to "save context".

### orchestrator

Manages complex, multi-step tasks requiring architectural planning and systematic
execution. Use for features involving 3+ files or non-linear solutions.

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
