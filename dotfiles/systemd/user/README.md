# dotfiles/systemd/user/

Kanonische **Vorlagen** für die userbezogenen systemd-Units, die auf jedem
OpenCode-Host laufen. Kein Auto-Deploy — jede Unit wird bewusst pro Host
kopiert und angepasst (Node-Pfade und Bot-Namen sind hostspezifisch).

| Vorlage | Zweck |
|---------|-------|
| `opencode.service` | OpenCode-V2-Background-Service (`opencode serve --service`), lauscht nur auf `127.0.0.1`; Passwortschutz über `~/.config/opencode/service.json` |
| `oc-tg-bot.service` | OpenCode-Telegram-Bot (`@grinev/opencode-telegram-bot` via `npx`), ein eigener Telegram-Bot je Host |

## Installation (Kurzfassung)

```sh
# 1. Server
cp dotfiles/systemd/user/opencode.service ~/.config/systemd/user/
# 2. Bot (Platzhalter <HOST>/<NODE_BIN_DIR> vorher ersetzen)
cp dotfiles/systemd/user/oc-tg-bot.service ~/.config/systemd/user/oc-tg-bot-<HOST>.service
# 3. Pflicht auf jedem Host
sudo loginctl enable-linger "$USER"
# 4. Aktivieren
systemctl --user daemon-reload
systemctl --user enable --now opencode.service oc-tg-bot-<HOST>.service
```

- **`enable-linger` ist Pflicht**: ohne Lingering startet der User-Manager die
  Units weder nach einem Reboot noch, wenn kein Login offen ist.
- **PATH**: Units (und `systemd-run`-Hilfsskripte) erben den interaktiven
  Shell-PATH **nicht** — `~/.opencode/bin` kommt aus `~/.bashrc`, nicht aus dem
  User-Manager. `opencode`, `npx`, `journalctl` … gehören in Unit-Skripten
  absolut aufgerufen, sonst `command not found` (real passiert 2026-10-17 bei
  der Übergabe des kik-Servers an die Unit).
- **Port**: ohne Pin nutzt V2 den Default `127.0.0.1:49374`; ein Pin geschieht
  host-lokal über `opencode service set hostname|port` (nicht in der Unit).
- **Passwort**: `opencode service get password`. Basic-Auth-Nutzername ist
  `opencode`. Der Wert gehört in die Bot-`.env`, **nie** ins Repo.
- **Reihenfolge bei der Erstinstallation auf einem Host, auf dem schon ein
  ad-hoc-Server läuft**: erst prüfen, wer `127.0.0.1:<port>` hält
  (`ss -ltnp`), dann den ad-hoc-Prozess stoppen und die Unit starten —
  sonst kämpfen beide um den Port. Achtung: Ein ad-hoc-Server bedient ggf. die
  laufende TUI-Session; deren Übergabe bricht diese Session ab.
- `%h` (systemd-Specifier, Home des Users) hält die Server-Vorlage für `georg`
  und `grafg` identisch.
- Verifikation: `systemctl --user is-enabled --is-active opencode.service`,
  `opencode service status`, Journal: `journalctl --user -u oc-tg-bot-<HOST> -f`.

## Bezug zur Shell

`dotfiles/bash_functions.sh` erwartet genau diese Unit-Namen:
`oc-restart` → `systemctl --user restart opencode.service`, `su-*` für die
allgemeine Unit-Steuerung.
