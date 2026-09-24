# Project State

Current status as of 2026-09-24.

## Current Focus

Continuous issue-awareness workflow: `AGENTS.global.md` + symlink and the
`issue-workflow` rewrite (proactive commit/push, auto-close criteria) just
shipped; observe daily practice and tune thresholds if needed.

## Completed (this cycle)

- [x] issue-workflow Auto-Close (#81): erledigte Issues werden autonom
      geschlossen, sobald die vier Sicherheitskriterien erfüllt sind (kein
      Nachfragen mehr); der Vollzug samt Issue-Nummer muss in der finalen
      Nachricht genannt werden; `AGENTS.global.md`, Skill (Purpose, Issue
      Completion, Output Expectations) und README angeglichen
- [x] `oc-models-report --provider <ID>` (#80): exakter, case-insensitive
      providerID-Filter, kombinierbar mit Substring-Filtern
      (`--provider openrouter opus`), provider-only listet alle Modelle des
      Providers; unbekannter Provider → stderr + exit 2; ohne Filter und ohne
      `--provider` → argparse-Fehler; 8 neue hermetic Tests, Suite grün
- [x] create-lesson Quiz-Regel (#78, `6049e7f`): 3–5 Fragen je Lesson
      passungsabhängig, Richtige-Positionen rotieren, je Frage genau eine
      Richtige; Präludium/Verifikation/Nachziehen angeglichen; Tests grün
- [x] create-lesson output rules (#77, `3183819`): shared light/dark toggle
      asset, `## Housekeeping` (Lehrplan · KM-Bezug · Runtime) at the bottom of
      the Tages-README, student-facing "Aufgabe" (= Mitarbeit) instead of
      "Hausübung"; tests green
- [x] `oc-models-report` in-repo (#79): `scripts/oc-models-report` caches the
      verbose model dump under `~/.local/share/oc-models-report/` with 12 h
      auto-refresh (`--refresh`, `--file`); table output byte-identical to
      the old script; hermetic tests added; `~/bin` copy replaced by a repo
      symlink (SVN)
- [x] SearXNG-MCP auf Think mit Gregor als Primary, Claw als Fallback (#74):
      `mcp.searxng.environment` im Repo-Template (`opencode.json`, secret-frei)
      und in der Think-Live-Config; `env.sample`-Primary auf `http://10.8.0.16`
      korrigiert; End-to-End verifiziert (`instance: http://10.8.0.16`).
      Gregor als agentische Schul-Suchinstanz festgehalten (DECISIONS.md
      2026-09-17: think → dell → Schüler-Agents)
- [x] Continuous issue-awareness workflow: `AGENTS.global.md` linked as
      `~/.config/opencode/AGENTS.md`; `issue-workflow` rewritten to proactive
      issue-linked commit/push (green commits only) with modes as manual
      overrides; `orchestration`, `AGENTS.md`, `AGENTS.template.md`,
      README and knowledge files aligned
- [x] P1 fixes: `orchestration` slimmed to a scope-gated policy (367→63
      lines), `telegram-send` skill removed, `projectgrade` follows the
      `grading-shared` missing-email protocol, `AGENTS.md` bootstrap list
      adds `HISTORY.md` (`c4cff84`)
- [x] P2 SSOT consolidation: shared German blocks reference `grading-shared`,
      address table removed from `projectgrade`, class list from
      `knowledge-exam`, point totals only in `knowledge-exam`, `searxng`
      duplicate API table removed (`dbc9bde`)
- [x] P3a progressive disclosure: 8 sibling reference files extracted;
      normative rules stayed inline; `tests/test_skill_links.py` link guard
      added (`070961a`)
- [x] Upstream-skill sync check: no content changes on the 6 transplanted
      skills
- [x] Repo-managed `agents/` directory with `lehrplan-annotator`, symlinked
      via `~/.config/opencode/agents` (prior cycle; still current)
- [x] SearXNG engine chain rework: `brave → google → mwmbl,searchmysite →
      braveapi` (token-gated `< 3` free hits); new envelope fields, per-engine
      mock, rewritten tests
- [x] SearXNG access control: nginx Basic-Auth (shared secret) for UI+API,
      `8888` bound to `127.0.0.1`, `limit_req`; wrapper authenticates from
      `~/.config/opencode/searxng.cred`; local perms locked
- [x] SearXNG skill doc clarified: `brave` is the only default result engine;
      `google` (and the free tier / `braveapi`) are fallback-only; the `< 3`
      gate protects the Brave API token (`039e96d`, `a8dae74`, `f44b905`)
- [x] SearXNG vhost: per-vhost logging (`searxng.access.log`/`.error.log`,
      custom `searxng` format with `rt=`); public `robots.txt` (`Disallow: /`)
      with server-level `X-Robots-Tag` and `proxy_hide_header` to avoid the
      duplicate
- [x] Corrected a misdiagnosis: `systemctl reload nginx` works here; the
      earlier "no effect" observation was a draining old worker answering the
      test request
- [x] SVN `EDV/Deployed` searxng nginx config synced 1:1 incl. backfill
      (`r7424`); `conf.d/{searxng-limits,searxng-logformat}.conf` added
- [ ] **Open**: SVN deployment mirror leaks secrets incl. infra private keys
      (CA/host/SSH/VPN keys, bot `.env`, `EDV/api-keys.txt`); history purge on
      `murl` pending decision (`~/svn/georg/docs/ai/HANDOFF.md` Task 5)

## Pending

- [ ] P4 of the audit: Completion Criteria ("Done when …") + frontmatter
      description trigger branches across `skills/*`
- [ ] dell replication: repo sync, `agents/` directory + `~/.config/opencode/agents`
      symlink, plus `mcp.searxng.environment` (Gregor primary, chain `gregor`)
      — rollout step 2 after think (see HANDOFF.md task 3)

## Blockers

None

## Next Session Suggestion

Start with P4: for each skill, add a short "Done when" completion criterion and
split the frontmatter `description` into clear trigger branches, without
re-introducing moved reference material. Keep the link guard green
(`python3 -m unittest discover -s tests -v`).
