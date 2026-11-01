#!/usr/bin/env bash
# Liest die Anrede einer Kohorte aus <subject>-T/<kohorte>/anrede.txt.
#
# Die Datei ist die EINZIGE Autoritaet fuer die Anrede (Du/Sie) in allen
# Grading-Skills. Sie enthaelt genau ein Wort: "Sie" oder "Du".
#
# Ausgabe: "Du" oder "Sie" auf stdout (Exit 0).
# Exit 1 mit deutscher Meldung auf stderr, wenn die Datei fehlt, leer ist oder
# etwas anderes als "Sie"/"Du" enthaelt. Exit 2 bei falschem Aufruf.
#
# Verwendung:
#   ANREDE=$(read-anrede.sh "$T_REPO/$KOHORTE/anrede.txt") || exit 1
set -euo pipefail

if [ "$#" -ne 1 ]; then
    echo "Aufruf: read-anrede.sh <pfad/zu/anrede.txt>" >&2
    exit 2
fi

datei="$1"

if [ ! -f "$datei" ]; then
    echo "FEHLT: $datei" >&2
    echo "Bitte die Datei anlegen und genau 'Sie' oder 'Du' hineinschreiben." >&2
    exit 1
fi

# BOM, CR, Whitespace und Satzzeichen ignorieren, Gross-/Kleinschreibung egal.
wert="$(
    tr -d '\357\273\277' < "$datei" \
        | tr -d '\r' \
        | tr -d '[:space:]' \
        | tr -d '[:punct:]' \
        | tr '[:upper:]' '[:lower:]'
)"

case "$wert" in
    du)
        echo "Du"
        ;;
    sie)
        echo "Sie"
        ;;
    "")
        echo "LEER: $datei" >&2
        echo "Bitte genau 'Sie' oder 'Du' eintragen." >&2
        exit 1
        ;;
    *)
        echo "UNGÜLTIG: $datei enthält '$wert'" >&2
        echo "Erlaubt ist nur 'Sie' oder 'Du'." >&2
        exit 1
        ;;
esac
