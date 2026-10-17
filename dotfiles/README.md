# dotfiles/

Gemeinsame, hostneutrale Dotfiles/Shell-Fragmente für **alle** Hosts.
Verteilt über den `opencode-helpers`-Clone (git), den jeder Host ohnehin
vorhält — so erreichen sie auch Hosts ohne SVN-Checkout (z. B. `kik`).

## `bash_functions.sh`

Einzige Quelle der gemeinsamen Shell-Funktionen und -Aliase:

- `oc` / `oc-new` / `oc-attach` / `oc-session` / `oc-sessions` /
  `oc-all-sessions` / `oc-restart` (OpenCode V2, Auto-Discovery über
  `~/.local/state/opencode/service.json`)
- `su-status` / `su-stop` / `su-start` / `su-restart` / `su-log` /
  `su-services` (systemd user services)
- `git-acp`

### Verwendung

In der jeweiligen `~/.bash_aliases` (interaktive Shells):

```sh
[ -f "$HOME/repos/georgernstgraf/opencode-helpers/dotfiles/bash_functions.sh" ] && \
  . "$HOME/repos/georgernstgraf/opencode-helpers/dotfiles/bash_functions.sh"
```

- Der Pfad nutzt `$HOME` (funktioniert für `georg` und `grafg`).
- Host-Spezifisches (lokale Aliase, abweichende Ports/Env) gehört in die
  lokale `~/.bash_aliases`, nicht hierher.
- **Keine Secrets** — Server-Passwörter kommen aus `service.json`/`pass`.
- Updates verteilen sich über `git pull` im Clone.

## `systemd/user/`

Vorlagen für die userbezogenen Units, die auf jedem Host laufen:
`opencode.service` (OpenCode-V2-Server, nur `127.0.0.1`, Passwort aus
`~/.config/opencode/service.json`) und `oc-tg-bot.service` (OpenCode-
Telegram-Bot, ein eigener Bot je Host). Kein Auto-Deploy: pro Host kopieren,
Platzhalter (`<HOST>`, `<NODE_BIN_DIR>`) ersetzen, `sudo loginctl
enable-linger "$USER"` setzen (sonst kein Start nach Reboot/ohne Login).
Details und Installationsablauf: [`systemd/user/README.md`](systemd/user/README.md).
Keine Secrets in den Units — Bot-Token und Server-Passwort liegen in der
lokalen `~/.config/oc-tg-bot-<host>/.env` (Mode 600).
