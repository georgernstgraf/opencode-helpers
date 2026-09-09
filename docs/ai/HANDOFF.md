Open tasks:

1. [ ] dell-repo sync pending: dell's `~/repos/georgernstgraf/opencode-helpers`
      sits on `d14cc25` with an uncommitted local change to
      `skills/lehrplan/SKILL.md` — the **Fachgruppen-Variante** for
      multi-subject repos (43 insertions, 2 deletions; self-contained
      `<fach>-<zweig>/` folders, flat `jahr_<N>_semesterplan_{ws,ss}.md`,
      `Gesetzestexte/` exception). Next session: diff-review it, commit, then
      merge with `ee3d02f` (think's Drei-Aufgaben-Struktur commit — text
      conflict in SKILL.md is likely, integrate both), push.

Done (2026-09-09):

- SearXNG on dell: already configured correctly (mcp points to
  `skills/searxng/scripts/opencode-searxng`, public URL
  `https://searxng.claw.graf.priv.at` answers 200). Former handoff task
  closed once dell's repo is pulled (see open task 1).
- Dell opencode server replicated from think: opencode 1.18.30, user unit
  `opencode.service` (127.0.0.1:4096, own basic-auth credentials in dell's
  `~/.bashrc` exports and the unit file), linger enabled, shell helpers
  `oc-attach`/`oc-restart`/`oc-sessions` in `~/.bash_aliases` (old
  62764-block and `oc-home-attach` removed, backup at
  `~/.bash_aliases.bak.20260909`).
- Telegram bot moved from claw to dell without a cloned repo: claw's
  `oc-tg-bot-experimental` (@schurlixclaw_bot, was crash-looping with
  WorkingDirectory in the openclaw checkout) fully removed (unit + config);
  token reused on dell in `oc-tg-bot-dell.service` (npx
  @grinev/opencode-telegram-bot, `.env` in `~/.config/oc-tg-bot-dell/`,
  OPENCODE_API_URL=http://127.0.0.1:4096). Note: dell's npx lives in
  /snap/bin, not /usr/bin. TTS credential
  `~/schurlis-tts-8d8da980c9de.json` copied from claw to dell.

Last updated: 2026-09-09.
