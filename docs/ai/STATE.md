# Project State

Current status as of 2026-09-06.

## Current Focus

Single-source search stack: the SearXNG skill owns the MCP server and uses
the public service URL as primary instance on every host.

## Completed (this cycle)

- [x] Consolidated the searxng MCP server: `skills/searxng/scripts/opencode-searxng`
      (stdlib-only) is the single implementation; legacy `scripts/opencode-searxng`
      moved to `scripts/archive/`. MCP config (`opencode.json`, repo + live) points
      to the skill path; `SEARX_URL` env dropped. Verified live after an opencode
      restart: tool appears as `searxng_search` with the full 7-parameter schema
- [x] Ported the richer tool schema into the stdlib server (`category`, `engines`,
      `time_range`, `safesearch` alongside `query`/`language`/`pageno`) and extended
      `searxng-search.sh` accordingly (URL-encoded params, honest empty results,
      `img_src`/`thumbnail`/`publishedDate` in output)
- [x] Primary search instance switched to `https://searxng.claw.graf.priv.at` —
      no localhost entry, because the skill runs on multiple hosts (verified:
      script and live tool report the public instance)
- [x] `~/bin` on claw now symlinks to the SVN toolset (`~/svn/georg/EDV/Toolset`,
      r7386); opencode/telegram-bot restart scripts live there
- [x] `searxng` is THE single search skill — no other search skill exists in
      `skills/`, upstream (mattpocock) has none, duplicate names are checked by
      `sync-upstream-skills`

## Pending

None

## Blockers

None

## Next Session Suggestion

None — consolidation and public-URL switch verified live in a fresh session
on 2026-09-06.
