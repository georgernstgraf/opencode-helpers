Open tasks:

1. [ ] **think: TUI-Disziplin beobachten (2026-11-11 erledigt).** Der
      Orphan-Daemon und die 1,5 Tage alte TUI (PID 614678, v2.2.5) sind weg;
      `opencode.service` läuft auf 2.2.7 unter systemd (PPID = systemd --user,
      Cgroup `app.slice/opencode.service`, `:4096`), Bot `active`. Offen ist
      nur die Ursache des vorangegangenen `oom-kill` (Peak 23,5 G / 12,6 G
      Swap bei 30 G RAM, brave + chrome im selben Scope) — bei erneutem
      Ausfall Speicherdruck prüfen, nicht die Unit.

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

4. [ ] Credentials im SVN (infra) — canonical task lives in
      `~/svn/georg/docs/ai/HANDOFF.md` **Task 5**
      (consolidate → `svn:ignore` → history rewrite → rotation of all leaked
      secrets incl. infra private keys). This repo only contributed the SearXNG
      access-control half (nginx Basic-Auth + `8888` on `127.0.0.1` + wrapper
      credential) — that part is done. Track the SVN/secret work over there.

5. [ ] PMM (`GRG-PMM`) bleibt kanonische create-lesson-Referenz, nutzt aber
      weiterhin `<klasse>/prepared-lessons/` und das alte Ablagemodell. Bei
      nächster Gelegenheit auf die #90-Regeln angleichen (KM-Anforderung,
      `unterricht/prepared-lessons/`, Beamer-Boxen) — erst nach Rücksprache.

6. [ ] #92 Folge-Migration (lehrplan): Andere Repos tragen noch die alte
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
- writing-for-agents-Audit abgeschlossen: P4 (`568215c`, #133) ergänzt
  `## Done when` + Trigger-Branches in 17 Skills, und #131 (`b32d0f2`) bringt
  die Observed-Drift-Klausel in `knowledge-persistence` + `AGENTS.global.md`.
  Dabei `codebase-audit` gequotet — sein `description` war ungültiges YAML
  (unquoted `": "`), was kein Test prüfte; der YAML-Sweep der Batch-Specs
  hat es aufgedeckt.
- Offen aus P4 (nicht im Scope, eigener Entscheid nötig): `handoff` und
  `wait-what` tragen Claude-Ära-Felder (`disable-model-invocation`,
  `argument-hint`), die opencode ignoriert — Umstellung auf
  `metadata.opencode/autoinvoke: false` + Aufnahme in `HIDDEN_SKILLS` wäre
  eine Sichtbarkeits-Änderung.
