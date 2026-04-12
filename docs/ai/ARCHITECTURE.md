# Architecture

Living structural map of the system as of 2026-04-13.
Overwritten when structural changes occur during a session.

## Overview

opencode-helpers is a template repository providing standardized skills,
agents, scripts, and knowledge persistence patterns for AI-assisted development 
workflows in opencode. Skills in `skills/` contain all workflow logic; the thin
command layer in `commands/` delegates to skills. Custom agents are managed in
`agents/`, and utility scripts are in `scripts/`. Session context is
persisted to a structured set of knowledge files in `docs/ai/`.

## Commands (`commands/`)

| Command | Purpose | Delegates to |
|---------|---------|-------------|
| `/improve` | Planning-only analysis of commands/skills for inconsistencies | none |
| `/issue-start` | Start or continue working on a task | `issue-workflow` |
| `/issue-commit` | Save work-in-progress progress to a GitHub issue | `issue-workflow` |
| `/issue-finish` | Complete a task: commit, push, close issue | `issue-workflow` |
| `/knowledge-assess` | Assess student knowledge-check submissions | `knowledge-assessment` |
| `/knowledge-exam` | Generate a German mini-exam from Git history | `knowledge-exam` |
| `/knowledge-persist` | Persist session context into docs/ai/ files | `knowledge-persistence` |
| `/nextprompt` | Run `aitranscribe -q` and treat output as next instruction | none (external tool) |
| `/security` | Generate a project security review report | none |
| `/tmpissue` | Create a GitHub issue from /tmp/issue.md, then delete it | none (`gh` CLI) |

## Agents (`agents/`)

| Agent | Purpose | Varity |
|-------|---------|--------|
| `chat` | General-purpose assistant with SearXNG web search; bypasses project context and plan-mode restrictions | Global primary |
| `build` | Standard build agent with integrated SearXNG web search | Global primary |
| `plan` | Standard plan agent (read-only) with integrated SearXNG web search | Global primary |

## Scripts (`scripts/`)

| Script | Purpose |
|--------|---------|
| `opencode-searxng.py` | MCP server providing `searxng_search` tool for web research |

## Skills (`skills/`)

| Skill | Purpose | Invocation |
|-------|---------|------------|
| `grading-shared` | Shared protocols: address style, email formulas, DB lookup, homework discovery, bulk concurrency, German/UTF-8 rules, email body format, praise guidelines, reporting | Referenced by `repograde`, `knowledge-assessment`, `projectgrade` |
| `homework` | Generate per-lesson Hausuebung.md files from Git history | Direct invocation from class folder |
| `issue-workflow` | Issue lifecycle management (start, checkpoint, finish) with mandatory issue-linked commits | `/issue-start`, `/issue-commit`, `/issue-finish` |
| `knowledge-assessment` | Assess German knowledge-check submissions, produce grading reports and email payloads | `/knowledge-assess` |
| `knowledge-exam` | Generate German knowledge-check exams and solution files | `/knowledge-exam` |
| `knowledge-persistence` | Persist session context into structured docs/ai/ knowledge files | `/knowledge-persist` |
| `projectgrade` | Grade student project repositories holistically based on Git commits, GitHub Issues, Pull Requests, and further measurable contributions | Direct skill invocation |
| `repograde` | Grade student repositories (full or date-filtered) in single-repo or bulk mode with plan presentation | Direct skill invocation |

## Knowledge Files (`docs/ai/`)

| File | Purpose | Update mode |
|------|---------|------------|
| HANDOFF.md | Open tasks and next-session context | Overwrite |
| DECISIONS.md | Chronological record of architectural and technical choices | Append |
| ARCHITECTURE.md | Living structural map of the current system | Overwrite |
| CONVENTIONS.md | Ongoing coding rules, patterns, and style agreements | Append |
| PITFALLS.md | Hard-won failure knowledge and non-obvious constraints | Append |
| DOMAIN.md | Business/teaching-domain rules | Append |
| STATE.md | Current project status snapshot | Overwrite |

## Data Flows

- `commands/*.md` → `skills/<name>/SKILL.md`: Commands pass user arguments and constraints into skills for execution
- `grading-shared` → `repograde`/`knowledge-assessment`/`projectgrade`: Shared protocols injected via skill reference at runtime
- `skills/*` → `docs/ai/*`: Knowledge-persistence skill writes session context into knowledge files
- `docs/ai/*` → agent bootstrap: AGENTS.md instructs agents to read knowledge files before starting any task
- `repograde` bulk mode: fan-out to concurrent subagents → per-repo artifact files → fan-in aggregation into shared EMAIL.json
- `opencode-searxng.py` (MCP) → OpenCode: Provides `searxng_searxng_search` tool to all agents via JSON-RPC
