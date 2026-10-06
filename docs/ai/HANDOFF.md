Open tasks:

1. [ ] Quiz-Begründungen gegenlesen (#94): Die Sub-Agents haben in PMM/WMC/
      INFI/SWP pro Antwortoption `data-grund`-Begründungen verfasst (teils
      redaktionell neu formuliert, wo vorher nur eine pauschale Erklärung
      stand). Struktur ist verifiziert (122 Fragen/427 Optionen, richtige
      Option „Richtig", übrige „Falsch"); offen ist die inhaltliche
      Stichprobe, ob jede Begründung sachlich korrekt und textgedeckt ist.

2. [ ] Policy observation (new): the continuous issue-awareness workflow
      (`AGENTS.global.md` + proactive commit/push) shipped 2026-09-15.
      Watch daily practice; tune the green-commit gate and auto-close
      criteria if commits land broken or issues close prematurely.
      Note: one opencode session restart is needed for the global file to
      load on each host (think/dell symlink replication pending — see
      task 4 for dell).

3. [ ] writing-for-agents audit — **P4** (last phase): add Completion Criteria
      ("Done when …") to each skill's instruction body and split the
      frontmatter `description` into clear trigger branches.
      Scope: ~20 skills under `skills/*/SKILL.md`.
      Prior phases shipped: P1 (`c4cff84`), P2 SSOT (`dbc9bde`),
      P3a progressive disclosure (`070961a`).
      P3a established the sibling pattern (`[X.md](./X.md)`, guarded by
      `tests/test_skill_links.py`) — P4 must keep links resolving and must
      NOT re-duplicate moved reference material. Verify with
      `python3 -m unittest discover -s tests -v`.

4. [ ] dell-repo sync pending: dell's `~/repos/georgernstgraf/opencode-helpers`
      sits on `d14cc25` with an uncommitted local change to
      `skills/lehrplan/SKILL.md` — the **Fachgruppen-Variante** for
      multi-subject repos (43 insertions, 2 deletions; self-contained
      `<fach>-<zweig>/` folders, flat `jahr_<N>_semesterplan_{ws,ss}.md`,
      `Gesetzestexte/` exception). Next session: diff-review it, commit, then
      integrate with `ee3d02f` (think's Drei-Aufgaben-Struktur commit) and the
      newer main (P1/P2/P3a; text conflict in SKILL.md is likely — integrate
      both), push. Also replicate the `agents/` directory + the
      `~/.config/opencode/agents` symlink on dell. Also replicate the
      `mcp.searxng.environment` block (Gregor primary, chain `gregor`)
      into dell's `~/.config/opencode/opencode.json` — rollout step 2
      after think (#74, DECISIONS.md 2026-09-17).

5. [ ] Credentials im SVN (infra) — canonical task lives in
      `~/svn/georg/docs/ai/HANDOFF.md` **Task 5**
      (consolidate → `svn:ignore` → history rewrite → rotation of all leaked
      secrets incl. infra private keys). This repo only contributed the SearXNG
      access-control half (nginx Basic-Auth + `8888` on `127.0.0.1` + wrapper
      credential) — that part is done. Track the SVN/secret work over there.

6. [ ] PMM (`GRG-PMM`) bleibt kanonische create-lesson-Referenz, nutzt aber
      weiterhin `<klasse>/prepared-lessons/` und das alte Ablagemodell. Bei
      nächster Gelegenheit auf die #90-Regeln angleichen (KM-Anforderung,
      `unterricht/prepared-lessons/`, Beamer-Boxen) — erst nach Rücksprache.

7. [ ] #92 Folge-Migration (lehrplan): Andere Repos tragen noch die alte
      Zweig-Fach-Ebene `unterricht/<ZWEIG>-<FACH>/` und ggf. `kompetenzmodule/`
      im Zweig-Ordner. Betroffen u. a. GRG-INFI (`unterricht/HWII-INFI/`,
      `infi-hwii/kompetenzmodule/`), GRG-WMC (`unterricht/WMC/` — dokumentierte
      Ausnahme für form-übergreifende Planung), GRG-SWP. Pro Repo als Befund
      melden und (nach Rücksprache) auf Fach-/Zweig-Ebene umstellen. Prüfen, ob
      `kompetenzmodule/` je Fach ans `lehrplan/`-Root wandert.

Last updated: 2026-10-06.
