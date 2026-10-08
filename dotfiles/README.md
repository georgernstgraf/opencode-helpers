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
