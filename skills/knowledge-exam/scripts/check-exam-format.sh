#!/usr/bin/env bash
# Format-Lint für Knowledge-Check-Angaben (knowledge-exam).
#
# Prüft die Schülerversion einer Angabe auf das `[ ]`-Format:
#   * jede MC-Frage hat genau vier Zeilen `[ ] <Aussage>`
#   * die vier Zeilen stehen zusammenhängend direkt unter dem Fragetext
#   * keine Buchstaben-Labels (a)), keine Task-Listen (- [ ]), keine
#     Umbruchzeilen, keine vorab gesetzten Marken ([x], [-])
#   * der Hinweisblock erklärt `[x]` und `[-]`
#
# Bewertet nichts — reiner Format-Lint (siehe #52: keine Bewertungsskripte).
#
# Aufruf:  check-exam-format.sh <exam.md> [<exam.md> ...]
# Exit:    0 = ok, 1 = Formatfehler, 2 = Aufruffehler
set -u

if [ "$#" -eq 0 ]; then
	echo "Aufruf: $(basename "$0") <exam.md> [<exam.md> ...]" >&2
	exit 2
fi

status=0

for datei in "$@"; do
	if [ ! -f "$datei" ]; then
		echo "$datei: Datei nicht gefunden" >&2
		exit 2
	fi
	awk -v datei="$datei" '
	{
		sub(/\r$/, "")
		zeile[NR] = $0
		if ($0 ~ /^```/) { im_code = !im_code; code[NR] = 1; next }
		if (im_code) { code[NR] = 1; next }
		if ($0 ~ /^### /) { fragen[++nf] = NR }
	}
	END {
		fehler = 0

		if (nf == 0) {
			printf "%s: keine Fragen vom Typ `### N.` gefunden\n", datei > "/dev/stderr"
			exit 2
		}

		# --- globale Prüfungen -------------------------------------------
		hx = 0; hm = 0
		for (i = 1; i <= NR; i++) {
			if (code[i]) continue
			z = zeile[i]

			if (z ~ /^\[/ && z !~ /^\[ \] [^ ]/) {
				printf "%s:%d: Option muss die Form `[ ] <Aussage>` haben (Leerzeichen zwischen den Klammern, Text dahinter): %s\n", datei, i, z > "/dev/stderr"
				fehler++
			}
			if (z ~ /^[a-dA-D]\)/) {
				printf "%s:%d: Buchstaben-Label statt `[ ]`-Zeile: %s\n", datei, i, z > "/dev/stderr"
				fehler++
			}
			if (z ~ /^[-*][ \t]+\[[ xX-]\]/) {
				printf "%s:%d: Task-Listen-Form `- [ ]` statt `[ ]` am Zeilenanfang: %s\n", datei, i, z > "/dev/stderr"
				fehler++
			}
			if (z ~ /^\[[xX-]\]/) {
				printf "%s:%d: vorab gesetzte Marke in der Angabe (Schülerversion muss leer sein): %s\n", datei, i, z > "/dev/stderr"
				fehler++
			}
			if (index(z, "[x]")) hx = 1
			if (index(z, "[-]")) hm = 1
		}
		if (!hx || !hm) {
			printf "%s: Hinweisblock fehlt — die Erklärung zu [x] und [-] wurde nicht gefunden\n", datei > "/dev/stderr"
			fehler++
		}

		# --- Prüfungen je Frage ------------------------------------------
		for (b = 1; b <= nf; b++) {
			s = fragen[b]
			e = (b < nf ? fragen[b + 1] - 1 : NR)

			n = 0
			for (i = s + 1; i <= e; i++) {
				if (code[i]) continue
				if (zeile[i] ~ /^\[ \] /) { n++; opt[n] = i }
			}
			if (n == 0) continue	# Freitextfrage

			if (n != 4) {
				printf "%s:%d: MC-Frage mit %d statt 4 `[ ]`-Zeilen: %s\n", datei, s, n, zeile[s] > "/dev/stderr"
				fehler++
			}
			for (i = 1; i < n; i++) {
				if (opt[i + 1] != opt[i] + 1) {
					printf "%s:%d: Optionen sind nicht zusammenhängend (Leerzeile oder Umbruch dazwischen): %s\n", datei, opt[i + 1], zeile[opt[i + 1]] > "/dev/stderr"
					fehler++
				}
			}
			if (n > 0) {
				j = opt[n] + 1
				if (j <= e && zeile[j] !~ /^[ \t]*$/ && zeile[j] !~ /^#/ && zeile[j] !~ /^---/) {
					printf "%s:%d: Text direkt nach der letzten Option (umgebrochene Aussage?): %s\n", datei, j, zeile[j] > "/dev/stderr"
					fehler++
				}
			}
		}

		exit (fehler > 0 ? 1 : 0)
	}' "$datei"
	rc=$?
	[ "$rc" -eq 2 ] && exit 2
	[ "$rc" -ne 0 ] && status=1
done

exit "$status"
