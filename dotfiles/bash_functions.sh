#!/usr/bin/env bash
# opencode-helpers/dotfiles/bash_functions.sh
# ---------------------------------------------------------------------------
# Gemeinsame, hostneutrale Shell-Funktionen und -Aliase für alle Hosts.
#
# Kanonische Quelle (git): georgernstgraf/opencode-helpers → dotfiles/bash_functions.sh
# Verteilung: opencode-helpers-Clone je Host (git pull), aus ~/.bash_aliases
#   mit Guard gesourct — Pfad nutzt $HOME, damit er für georg UND grafg passt:
#     [ -f "$HOME/repos/georgernstgraf/opencode-helpers/dotfiles/bash_functions.sh" ] && \
#       . "$HOME/repos/georgernstgraf/opencode-helpers/dotfiles/bash_functions.sh"
# Voraussetzungen:
#   * `opencode` (V2) im PATH  (Host-.bashrc setzt ~/.opencode/bin)
#   * `jq` für oc-all-sessions
#   * laufender V2-Background-Service (Auto-Discovery über
#     ~/.local/state/opencode/service.json) — kein --server/Passwort nötig.
#
# Host-Spezifisches (lokale Aliase, abweichende Server-Ports) gehört NICHT
# hierher, sondern in die jeweilige ~/.bash_aliases.
# KEINE SECRETS: Server-Passwörter kommen aus service.json/pass, nie im Klartext.
# ---------------------------------------------------------------------------

# === OpenCode V2 (Auto-Discovery des lokalen Background-Service) ===
alias oc='opencode'                                     # neue Session im aktuellen Verzeichnis
oc-new()       { opencode "$@"; }                       # neue Session
oc-attach()    { opencode --continue "$@"; }            # letzte Session des Projekts fortsetzen
oc-session()   { opencode --session "$1" "${@:2}"; }    # bestimmte Session fortsetzen/anlegen
oc-sessions()  { opencode session list --max-count "${1:-20}"; }   # Sessions des Projekts
oc-all-sessions() {   # ALLE Sessions des lokalen Servers (neueste zuerst), optional: Anzahl
  opencode api GET /api/session 2>/dev/null \
    | jq -r '(.data // .) | sort_by(-.time.updated) | .[] | "\(.id)\t\(.time.updated/1000|strftime("%Y-%m-%d %H:%M"))\t\(.title)"' \
    | column -t -s $'\t' | head -n "${1:-20}"
}
oc-restart()   { systemctl --user restart opencode.service && echo "opencode.service neu gestartet"; }

# === OpenCode an einen entfernten Server hängen (TUI via VPN) ===
# Muster: think -> swift (Windows-Flotten-Host, [hosts/swift]).
# Passwort zur Laufzeit aus pass — nie im Klartext hier (KEINE SECRETS).
# Port 28894 ist der Windows-Default (Linux wäre 49374) und steht in swift's
# service.json fest; Firewall/Client-URLs hängen daran.
# Hosts ohne VPN/pass (z. B. kik) scheitern bewusst mit Fehlermeldung.
oc-attach-swift() {   # TUI an den swift-Server (Windows, VPN 10.8.0.5:28894) hängen
  local pw
  pw="$(PASSWORD_STORE_DIR="$HOME/svn/georg/private/password-store" \
        pass show swift/opencode-server-password 2>/dev/null | head -1)"
  if [ -z "$pw" ]; then
    echo "oc-attach-swift: kein Passwort aus pass (Store/GPG-Key fehlt) oder Host ohne VPN-Zugang (z. B. kik)" >&2
    return 1
  fi
  OPENCODE_PASSWORD="$pw" opencode --continue --server http://10.8.0.5:28894 "$@"
}

# === systemd user services ===
su-status()    { systemctl --user status "$@"; }
su-stop()      { systemctl --user stop "$@"; }
su-start()     { systemctl --user start "$@"; }
su-restart()   { systemctl --user restart "$@"; }
su-log()       { journalctl --user -u "$1" --no-pager -n 50 -f; }
su-services()  { systemctl --user list-units --type=service --no-pager --no-legend "$@" | awk '{print $1}'; }

# === Git ===
alias git-acp='git add . && git commit -mACP && git push'
