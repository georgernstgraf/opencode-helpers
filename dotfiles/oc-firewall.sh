#!/usr/bin/env bash
# opencode-helpers/dotfiles/oc-firewall.sh
# ---------------------------------------------------------------------------
# Firewall-Schutz für den lokalen opencode-Server-Port: erlaubt Loopback und
# das VPN (10.8.0.0/24), verwirft (REJECT) alles andere an diesem Port.
#
# Bewusst eine präzise INPUT-Regel: keine Default-Policy-Änderung, kein
# SSH-Lockout-Risiko, Docker-FORWARD-Ketten unangetastet (claw).
# Vorbild: swift, Firewall-Regel "OpenCode nur VPN" (Windows).
#
# Aufruf:  oc-firewall.sh apply|remove|status
# Port:    aus ~/.config/opencode/service.json gelesen (Default 49374 —
#          Linux-Default von OpenCode). Die Unit "oc-firewall.service"
#          (dotfiles/systemd/user/) ruft dieses Skript beim Boot auf.
# Rechte:  passwordless sudo für iptables nötig (auf kik/gregor/claw vorhanden).
#
# KEINE SECRETS in dieser Datei.
# ---------------------------------------------------------------------------

set -u
MODE="${1:-status}"
VPN_CIDR="${OC_FIREWALL_VPN_CIDR:-10.8.0.0/24}"
SERVICE_JSON="$HOME/.config/opencode/service.json"
PORT=49374
if command -v jq >/dev/null 2>&1 && [ -f "$SERVICE_JSON" ]; then
  PORT="$(jq -r '.port // 49374' "$SERVICE_JSON")"
fi

rule() {   # $1 = iptables-Operation (-C/-I/-D); Regeltext immer identisch halten
  local op="$1"
  sudo -n iptables "$op" INPUT -p tcp --dport "$PORT" ! -i lo ! -s "$VPN_CIDR" -j REJECT 2>/dev/null
}

case "$MODE" in
  apply)
    if rule -C; then
      echo "oc-firewall: Regel existiert bereits (Port $PORT)"
    else
      if rule -I; then
        echo "oc-firewall: Regel gesetzt (Port $PORT — Loopback+VPN $VPN_CIDR erlaubt, sonst REJECT)"
      else
        echo "oc-firewall: FEHLER — Regel nicht gesetzt (passwordless sudo für iptables nötig)" >&2
        exit 1
      fi
    fi
    ;;
  remove)
    if rule -D; then
      echo "oc-firewall: Regel entfernt (Port $PORT)"
    else
      echo "oc-firewall: keine Regel vorhanden (Port $PORT)"
    fi
    ;;
  status|*)
    echo "oc-firewall: Port $PORT, VPN $VPN_CIDR"
    if rule -C; then
      echo "oc-firewall: Regel AKTIV"
    else
      echo "oc-firewall: keine Regel"
    fi
    ;;
esac
