Open tasks:

1. [ ] **think: `opencode.service` gefailt + Orphan-Daemon (2026-11-11).** Die
      Unit steht seit 2026-11-08 09:52 auf `failed (Result: oom-kill)`
      (Peak 23,5 G / 12,6 G Swap), bedient wird der Host aber weiter von einem
      Orphan `opencode serve --service` (PID 408868, PPID = systemd, aber
      Cgroup `app-org.gnome.Terminal.slice/vte-spawn-…`) auf `127.0.0.1:4096`.
      Symptom: Clients und `oc-tg-bot-home` laufen normal, nur
      `systemctl --user is-active` meldet `failed`; nach Logout/Reboot ist der
      Server weg. Fix (nur mit Rücksprache, beendet laufende Sessions):
      Orphan killen → `systemctl --user start opencode.service` → `opencode api
      get /api/info` + `cat /proc/<pid>/cgroup` prüfen. Ursache des OOM
      (23,5 G Peak bei 30 G RAM, chrome im gleichen Scope) mitdenken.

2. [ ] Quiz-Begründungen gegenlesen (#94): Die Sub-Agents haben in PMM/WMC/
      INFI/SWP pro Antwortoption `data-grund`-Begründungen verfasst (teils
      redaktionell neu formuliert, wo vorher nur eine pauschale Erklärung
      stand). Struktur ist verifiziert (122 Fragen/427 Optionen, richtige
      Option „Richtig", übrige „Falsch"); offen ist die inhaltliche
      Stichprobe, ob jede Begründung sachlich korrekt und textgedeckt ist.

3. [ ] Policy observation: the continuous issue-awareness workflow
      (`AGENTS.global.md` + proactive commit/push) shipped 2026-09-15.
      Watch daily practice; tune the green-commit gate and auto-close
      criteria if commits land broken or issues close prematurely.

4. [ ] writing-for-agents audit — **P4** (last phase): add Completion Criteria
      ("Done when …") to each skill's instruction body and split the
      frontmatter `description` into clear trigger branches.
      Scope: ~20 skills under `skills/*/SKILL.md`.
      Prior phases shipped: P1 (`c4cff84`), P2 SSOT (`dbc9bde`),
      P3a progressive disclosure (`070961a`).
      P3a established the sibling pattern (`[X.md](./X.md)`, guarded by
      `tests/test_skill_links.py`) — P4 must keep resolving links and must
      NOT re-duplicate moved reference material. Verify with
      `python3 -m unittest discover -s tests -v`.
      Nearby: #131 (Observed-Drift-Klausel in `knowledge-persistence`) ist
      Skill-Text derselben Familie — im selben Zug erledigen.

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

Last updated: 2026-11-11.

## Erledigt am 2026-11-11 (Flotten-Nachzug)

- deepseek-search-Rollout abgeschlossen (think/claw/elite/dell; Schul-Hosts
  gregor/kik bewusst keylos). Der claw-Nebenbefund (Orphan-Server seit
  2026-10-17) ist erledigt: `opencode.service` läuft dort als `Type=oneshot`
  unter systemd (PPID = systemd --user, Cgroup `app.slice/opencode.service`).
- dell ist jetzt auch per SSH von claw erreichbar: claw-Pubkey
  (`SHA256:k8wWQ66…17GQ`, `georg@claw.graf.priv.at`) dauerhaft in
  `dell:~georg/.ssh/authorized_keys` (über think eingetragen, Eintrag bleibt).
- dell nachgezogen: Repo `d93acb0` → `5627852` (die `lehrplan`-
  Fachgruppen-Variante steckt bereits in `main`), Unit `Type=oneshot`/2.2.6
  aktiv, `Linger=yes`, `agents`/`skills`/`commands`-Symlinks vorhanden,
  `mcp.deepseek`-Overlay gesetzt (#116, #111).
- STT quality-first flottenweit: `whisper-large-v3` in `oc-tg-bot` +
  `oc-tg-bot-zazentimer` (claw), `oc-tg-bot-home` (think), `oc-tg-bot-dell`
  (dell) — Bots neu gestartet; gregor war schon korrekt (#46).
