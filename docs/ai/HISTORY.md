# History

Chronological archive of superseded decisions and pruned entries.
Entries here are no longer active truth. Never delete from this file.

## 2026-09-06 (SUPERSEDED 2026-04-01, origin: DECISIONS.md, reason: unified homework decision): Add homework-improve as a standalone education skill
- **Choice**: Implement `/homework-improve` as a thin command wrapper around a dedicated `homework-improve` skill that writes `Hausübungen.md`
- **Reason**: The workflow needs reusable rules for class-folder history analysis, German homework expansion, newest-first ordering, and re-entrant updates
- **Considered**: Embedding the workflow directly into the command file, or overloading `knowledge-exam` with homework behavior
- **Tradeoff**: One more standalone skill to maintain, but the homework workflow stays explicit and reusable
- **Superseded by**: 2026-04-01 unified homework decision
- **Origin**: docs/ai/DECISIONS.md
- **Reason**: Pruned — carried a "Superseded by: 2026-04-01 unified homework decision" marker; superseded entries do not stay in active files.

## 2026-09-06 (SUPERSEDED 2026-04-01, origin: DECISIONS.md, reason: unified homework decision): Add /homework command as read-only homework suggestion generator
- **Choice**: Implement `/homework` as a thin command wrapper around a dedicated `homework` skill that outputs suggestions without modifying files
- **Reason**: Teachers need quick homework ideas from recent lesson commits; unlike `/homework-improve`, this should be read-only for easy copy-paste
- **Considered**: Combining with `/homework-improve`, or extending `/knowledge-exam`
- **Tradeoff**: Another standalone skill, but keeps the read-only output pattern explicit and separate from file-modifying workflows
- **Superseded by**: 2026-04-01 unified homework decision
- **Origin**: docs/ai/DECISIONS.md
- **Reason**: Pruned — carried a "Superseded by: 2026-04-01 unified homework decision" marker; superseded entries do not stay in active files.

## 2026-09-06 (SUPERSEDED 2026-09-06, origin: DECISIONS.md, reason: chat/build/plan agents no longer exist; SearXNG part covered by the 2026-09-06 single-source decision): Use dedicated chat agent and SearXNG MCP server
- **Choice**: Implement a dedicated `chat` agent and a Python-based SearXNG MCP server
- **Reason**: Users often ask non-project related questions; a dedicated agent avoids "context watering" from plan-mode restrictions. SearXNG provides up-to-date web research capabilities.
- **Considered**: Using the plan agent for chat, using built-in websearch tools
- **Tradeoff**: Requires a local SearXNG instance and a custom MCP wrapper, but provides superior search quality and privacy.
- **Origin**: docs/ai/DECISIONS.md
- **Reason**: The chat agent (and the `agents/` management it depended on) no longer exists; the still-valid SearXNG MCP server part is recorded in the 2026-09-06 "Single-source SearXNG stack" decision.

## 2026-09-06 (SUPERSEDED 2026-09-06, origin: DECISIONS.md, reason: no `agents/` directory and no `~/.config/opencode/agents` links remain): Manage global OpenCode agents via repository symlinks
- **Choice**: Store global agent definitions in `agents/` and link them to `~/.config/opencode/agents/`
- **Reason**: Centralizes configuration in the `opencode-helpers` repository for version control and easy updates across environments.
- **Considered**: Copying files manually, using a specialized configuration manager
- **Tradeoff**: Requires manual setup of symlinks (documented in README), but ensures single source of truth.
- **Origin**: docs/ai/DECISIONS.md
- **Reason**: The `agents/` directory was removed from the repo (verified 2026-09-06); global agents are no longer repo-managed.

## 2026-09-06 (SUPERSEDED 2026-09-06, origin: CONVENTIONS.md, reason: MCP servers now live inside their skill directory; ~/bin is the SVN toolset symlink): Custom MCP servers in scripts/ + ~/bin symlink
- Custom MCP servers are stored in `scripts/` and symlinked to `~/bin/`.
- **Origin**: docs/ai/CONVENTIONS.md (File Layout)
- **Reason**: The searxng MCP server lives in `skills/searxng/scripts/` and is referenced by absolute path in `opencode.json`; `~/bin` on every host is a symlink to the personal SVN toolset (`~/svn/georg/EDV/Toolset`), not a repo-script target.

## 2026-09-06 (SUPERSEDED 2026-09-06, origin: STATE.md, reason: skill runs on multiple hosts; public URL is primary): localhost:8888 as first SearXNG instance
- STATE.md bullet claimed `localhost:8888` first in the `searxng-search.sh` instance chain.
- **Origin**: docs/ai/STATE.md (2026-09-06 snapshot, same day)
- **Reason**: `localhost:8888` only resolves on the SearXNG host; the chain is now `https://searxng.claw.graf.priv.at` → `etsi.me` → `baresearch.org`.
