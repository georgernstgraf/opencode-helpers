# Project State

Current status as of 2026-09-29.

## Current Focus

`create-lesson` (#94) hat das Quiz auf **Begründung pro Option** umgestellt:
kanonisches `data-grund`-Modell, Sofort-Feedback beim Radio-`change` ohne
Prüf-Button, `.feedback` zeigt die Begründung der gewählten Option. Die
Repo-Migration ist durch (PMM 9 Dateien/33 Fragen, WMC 10/47, INFI 6/36,
SWP 3/6; 122 Fragen/427 Optionen verifiziert). Offen: stichprobenartiges
Gegenlesen der redaktionell formulierten Begründungen.

`lehrplan` (#92) trennt Fach-Ebene und Zweig-Ebene sauber: `kompetenzmodule/`
+ KM-keyed Ressourcen am `lehrplan/`-Root (Fach), Extrakt/Klassen-Extrakte/
Planung in `lehrplan/<fach>-<zweig>/` (Zweig), `unterricht/` nur noch flache
`KM<#>/SA`-Einheiten. Die Zweig-Fach-Ebene `unterricht/<ZWEIG>-<FACH>/` entfällt;
`create-lesson` bezieht den Plan aus `lehrplan/<fach>-<zweig>/`.

`create-lesson` (#90) wurde umgebaut: KM-Anforderung statt Unterlagen-Obergrenze,
Arbeitsort `unterricht/` mit `prepared-lessons/NN-slug.html`, kein Nachfragen,
Doppelstunden-Umfang, KM-Vollständigkeit und Beamer-taugliche Code-Boxen.
Erste Anwendung: GRG-WMC auf zentrales `assets/` + selbst-geführte
prepared-lessons umstellen.

## Completed (this cycle)

- [x] #94 CLOSED 2026-09-29 — create-lesson: Quiz-Begründung pro Option
      (`data-grund`), Sofort-Feedback beim Radio-`change`, kein Prüf-Button;
      Skill-Schritt 6 + Verifikation 4; kanonische `assets/quiz.js` (byte-
      identisch) + Markup in PMM/WMC/INFI/SWP migriert; 122 Fragen/427
      Optionen semantisch geprüft (richtige Option „Richtig", übrige „Falsch")
- [x] #92 CLOSED 2026-09-29 — lehrplan: Fach-Ebene (`kompetenzmodule/` +
      KM-keyed Ressourcen am Root) vs. Zweig-Ebene (`<fach>-<zweig>/` mit
      Extrakt + Planung); `unterricht/` ohne Zweig-Fach-Ordner; Kollisions-
      Behauptung entfernt, Restfall-Regel für Mehr-Fächer-Repos
      (`kompetenzmodule/<fach>/`); WMC-Ausnahme um Planungsdateien erweitert;
      Retrofit-Klausel invertiert; `create-lesson`-Planquelle angepasst;
      Test-Suite grün (70)
- [x] #89 CLOSED 2026-09-28 — knowledge-persistence endet mit eigenem Commit + Push: Skill um
      Pflichtschritt „Commit and Push" + Constraint erweitert; `issue-workflow`
      (`commit`, `finish`, Continuous-Issue-Completion, Output Expectations)
      und `commands/knowledge-persist.md` angeglichen; `docs/ai/`-Doku
      aktualisiert; Test-Suite grün (70)
- [x] #90 CLOSED 2026-09-28 — create-lesson: Anforderung ist das
      **KM/Teil-KM**; `Unterlagen/` als kritisch geprüfte *gelebte Praxis*
      (borgen/kopieren erlaubt, keine Obergrenze); Arbeitsort **`unterricht/`**
      mit `prepared-lessons/NN-slug.html` + Tages-README-Vorlage; Klassenordner
      nur per Hand; **kein Nachfragen** (außer Bestellformat);
      Doppelstunden-Umfang, KM-Vollständigkeit und Beamer-taugliche helle
      Code-Boxen als Pflicht + Verifikationspunkte
- [x] create-lesson Aufgabe als erster `## Aufgabe`-Abschnitt (#84):
      Layout-Template, Verifikation, Nachziehen im Skill und die
      Classroom-Material-Konvention in `docs/ai/CONVENTIONS.md`
      angeglichen; Link-Test grün
- [x] Grading-Skill-Konfiguration (#85): `grading-shared` Adresstabelle
      um `4ahwit`/`5ahwit` (Informal) ergänzt; `knowledge-assessment`
      läuft nun auch in einem Git-Working-Tree, ohne Git-Operationen;
      `docs/ai/CONVENTIONS.md` (Grading-Kontext) gespalten
- [x] create-lesson Ablage/Aufgabe/Quiz (#83): Lektionen liegen **immer**
      im Datums-Ordner `<klasse>/YYYY-MM-DD__thema/` (`lesson.html` +
      Tages-README), kein `lessons/`-Ordner mehr; Aufgaben-Referenz im
      Tages-README ist Pflicht; Quiz 1–5 statt 3–5. `SKILL.md`,
      `docs/ai/CONVENTIONS.md` und `docs/ai/DECISIONS.md` angeglichen;
      Suite grün (42, inkl. `test_skill_links`)
- [x] `oc-models-report` Filter matcht „free"-Kosten (#82): `matches()`
      durchsucht zusätzlich den gerenderten Kostenwert (`fmt_cost`), damit
      `--provider groq free` die 0/0-Modelle findet; nur Kosten, keine
      Kontext-/Keyword-Erweiterung; 2 neue Tests, Suite grün (42)
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
