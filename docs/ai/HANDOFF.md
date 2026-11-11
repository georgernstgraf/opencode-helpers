Open tasks:

1. [ ] Policy observation: the continuous issue-awareness workflow
      (`AGENTS.global.md` + proactive commit/push) shipped 2026-09-15.
      Watch daily practice; tune the green-commit gate and auto-close
      criteria if commits land broken or issues close prematurely.

2. [ ] Credentials im SVN (infra) — canonical task lives in
      `~/svn/georg/docs/ai/HANDOFF.md` **Task 5**
      (consolidate → `svn:ignore` → history rewrite → rotation of all leaked
      secrets incl. infra private keys). This repo only contributed the SearXNG
      access-control half (nginx Basic-Auth + `8888` on `127.0.0.1` + wrapper
      credential) — that part is done. Track the SVN/secret work over there.

3. [ ] PMM (`GRG-PMM`) bleibt kanonische create-lesson-Referenz, nutzt aber
      weiterhin `<klasse>/prepared-lessons/` und das alte Ablagemodell. Bei
      nächster Gelegenheit auf die #90-Regeln angleichen (KM-Anforderung,
      `unterricht/prepared-lessons/`, Beamer-Boxen) — erst nach Rücksprache.

4. [ ] #92 Folge-Migration (lehrplan): Andere Repos tragen noch die alte
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
- Claude-Ära-Frontmatter repariert (`47fd1f9`): `disable-model-invocation` in
  `handoff`, `wait-what`, `protokoll` und `to-questionnaire` auf
  `metadata.opencode/autoinvoke: false` umgestellt (die Skills waren trotz
  user-invoked-Absicht dem Modell angeboten), `argument-hint` entfernt,
  `HIDDEN_SKILLS` erweitert und ein Guard
  (`test_no_claude_era_inert_fields`) gegen den Rückfall ergänzt.
- think: Orphan/TUI bereinigt (`ff710e4`), OOM-Ursache vom 2026-11-08 bleibt
  bewusst unverfolgt (Entscheid des Nutzers 2026-11-11).
- Quiz-Begründungen inhaltlich gegengelesen (2026-11-11, Folgearbeit zu #94):
  53 Dateien, 1784 Optionen in vier Repos. 55 Begründungen korrigiert
  (falsche Zahlen, vertauschte Zeilen, Begründungen zu Nachbaroptionen,
  erfundene Mechanismen), 21 ASCII-Anführungszeichen in `data-grund`-Werten
  repariert (Attribut endete vorzeitig) und eine „Richtig"-Option ohne
  `data-richtig` ergänzt. Commits: GRG-PMM `6c233ee` (#48), GRG-WMC `a1da493`
  (#12), GRG-INFI `5274752` (#21), GRG-SWP `5e3e274` (#15) — alle vier Issues
  mit Befund-Kommentar geschlossen. Offen bleibt **GRG-PMM#49**: vermutlich
  falscher Antwortschlüssel `KM7-03/q10` (`power.t.test` läuft fehlerfrei, weil
  genau `n` fehlt), drei Fragen mit „wähle die wahre Aussage" ohne richtige
  Option (Legend ergänzen oder fünfte Option) und zwei Prosa-Widersprüche
  (`KM7-02` Yates vs. Freiheitsgrade, `KM7-01` 37+39−2 statt 37+40−2).
