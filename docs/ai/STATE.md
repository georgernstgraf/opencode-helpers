# Project State

Current status as of 2026-09-06.

## Current Focus

Single-source search stack: the SearXNG skill owns the MCP server, the legacy
requests-based copy is retired.

## Completed (this cycle)

- [x] Consolidated the searxng MCP server: `skills/searxng/scripts/opencode-searxng`
      (stdlib-only) is the single implementation; legacy `scripts/opencode-searxng`
      moved to `scripts/archive/`. MCP config (`opencode.json`, repo + live) points
      to the skill path; `SEARX_URL` env dropped
- [x] Ported the richer tool schema into the stdlib server (`category`, `engines`,
      `time_range`, `safesearch` alongside `query`/`language`/`pageno`) and extended
      `searxng-search.sh` accordingly (URL-encoded params, honest empty results,
      `img_src`/`thumbnail`/`publishedDate` in output, `localhost:8888` first)
- [x] `searxng` is THE single search skill — no other search skill exists in
      `skills/`, upstream (mattpocock) has none, duplicate names are checked by
      `sync-upstream-skills`
- [x] Added `skills/telegram-send/SKILL.md` — sends documents/photos to the user's
      private Telegram chat via the Bot API, reusing the local bot's credentials
      (`~/.config/oc-tg-bot*/.env`); available in all sessions via the
      `~/.config/opencode/skills` symlink → this repo's `skills/` (verified 2026-09-01)
- [x] Documented bot topology (4 systemd user services `oc-tg-bot*`, all attached to
      `opencode.service` on 127.0.0.1:62764) and secret-handling rules in the skill

## Pending

None

## Blockers

None

## Next Session Suggestion

Verify the upgraded `searxng_search` tool (7 params, incl. `category`/
`time_range`/`engines`/`safesearch`) and `telegram-send` appear after the next
opencode restart and work end-to-end from a fresh session.
