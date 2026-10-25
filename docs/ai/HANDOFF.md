Open tasks:

1. [ ] **`deepseek-search`-Rollout (neu 2026-10-25):** **think** ist umgestellt
      (Host-Overlay `mcp.deepseek.environment` mit `DEEPSEEK_SEARCH_API_KEY_FILE`,
      `mcp.searxng` dort entfernt, Key-Datei `~/.config/opencode/deepseek.key`
      mode 600). **claw** ebenfalls (Key aus der eigenen `auth.json`, lokale
      Instanz `http://127.0.0.1:8888`, `SEARXNG_CHAIN=default` inkl.
      `braveapi`, Server via `opencode reload` neu geladen, Config in SVN r7669
      von claw committet). **Schul-Hosts** (gregor/dell/kik) bleiben bewusst
      ohne Key auf `searxng_search` — gregor/kik geprüft, unverändert grün.
      Offen: **elite** (Key-Datei + Overlay, `mcp.searxng` raus,
      `opencode.service` restart, echte Suche + erzwungener 402;
      `deepseek.key` in `svn:ignore` von
      `EDV/Deployed/elite/home/georg/.config/opencode/` aufnehmen) und **dell**
      (Overlay prüfen).
      Nebenbefund claw: dort läuft der georg-Server (PID auf :62764) in einem
      verwaisten Session-Scope (seit 2026-10-17, keine systemd-Unit) — bei
      Gelegenheit die Unit-Vorlage aus `dotfiles/systemd/user/` installieren
      + `loginctl enable-linger georg` (wie think/kik), damit er Reboots
      übersteht. Außerdem läuft auf claw ein fremder `opencode serve` des Users
      `sami` auf :60490 (21 Tage alt) — nicht unserer.

2. [ ] Quiz-Begründungen gegenlesen (#94): Die Sub-Agents haben in PMM/WMC/
      INFI/SWP pro Antwortoption `data-grund`-Begründungen verfasst (teils
      redaktionell neu formuliert, wo vorher nur eine pauschale Erklärung
      stand). Struktur ist verifiziert (122 Fragen/427 Optionen, richtige
      Option „Richtig", übrige „Falsch"); offen ist die inhaltliche
      Stichprobe, ob jede Begründung sachlich korrekt und textgedeckt ist.

3. [ ] Policy observation (new): the continuous issue-awareness workflow
      (`AGENTS.global.md` + proactive commit/push) shipped 2026-09-15.
      Watch daily practice; tune the green-commit gate and auto-close
      criteria if commits land broken or issues close prematurely.
      Note: one opencode session restart is needed for the global file to
      load on each host (think/dell symlink replication pending — see
      task 4 for dell).

4. [ ] writing-for-agents audit — **P4** (last phase): add Completion Criteria
      ("Done when …") to each skill's instruction body and split the
      frontmatter `description` into clear trigger branches.
      Scope: ~20 skills under `skills/*/SKILL.md`.
      Prior phases shipped: P1 (`c4cff84`), P2 SSOT (`dbc9bde`),
      P3a progressive disclosure (`070961a`).
      P3a established the sibling pattern (`[X.md](./X.md)`, guarded by
      `tests/test_skill_links.py`) — P4 must keep links resolving and must
      NOT re-duplicate moved reference material. Verify with
      `python3 -m unittest discover -s tests -v`.

5. [ ] dell-repo sync pending: dell's `~/repos/georgernstgraf/opencode-helpers`
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

6. [ ] Credentials im SVN (infra) — canonical task lives in
      `~/svn/georg/docs/ai/HANDOFF.md` **Task 5**
      (consolidate → `svn:ignore` → history rewrite → rotation of all leaked
      secrets incl. infra private keys). This repo only contributed the SearXNG
      access-control half (nginx Basic-Auth + `8888` on `127.0.0.1` + wrapper
      credential) — that part is done. Track the SVN/secret work over there.

7. [ ] PMM (`GRG-PMM`) bleibt kanonische create-lesson-Referenz, nutzt aber
      weiterhin `<klasse>/prepared-lessons/` und das alte Ablagemodell. Bei
      nächster Gelegenheit auf die #90-Regeln angleichen (KM-Anforderung,
      `unterricht/prepared-lessons/`, Beamer-Boxen) — erst nach Rücksprache.

8. [ ] #92 Folge-Migration (lehrplan): Andere Repos tragen noch die alte
      Zweig-Fach-Ebene `unterricht/<ZWEIG>-<FACH>/` und ggf. `kompetenzmodule/`
      im Zweig-Ordner. Betroffen u. a. GRG-INFI (`unterricht/HWII-INFI/`,
      `infi-hwii/kompetenzmodule/`), GRG-WMC (`unterricht/WMC/` — dokumentierte
      Ausnahme für form-übergreifende Planung), GRG-SWP. Pro Repo als Befund
      melden und (nach Rücksprache) auf Fach-/Zweig-Ebene umstellen. Prüfen, ob
      `kompetenzmodule/` je Fach ans `lehrplan/`-Root wandert.

Last updated: 2026-10-17.

9. [ ] Host-Services nachziehen (#111): Die Unit-Vorlagen
      (`dotfiles/systemd/user/`) sind erst auf `kik` und `gregor` im Einsatz.
      Prüfen, ob `think`/`dell`/`claw` ebenfalls `opencode.service` +
      `oc-tg-bot-<host>.service` als **user** Units betreiben (inkl.
      `loginctl enable-linger`) und ob deren Bot-`.env` noch
      `STT_MODEL=whisper-large-v3-turbo` führt — der Wert gehört auf
      `whisper-large-v3` (DECISIONS.md 2026-10-17).
