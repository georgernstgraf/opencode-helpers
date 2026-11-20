---
name: plf-bauen
description: Baut eine schriftliche Leistungsüberprüfung (PLF) in LaTeX aus dem
  Aufgabenpool eines Lehrplan-Repos zusammen — Stoffabgrenzung, Wahl freier
  Varianten, Gruppen A/B als Zwillinge derselben Variantenfamilie, Punktesatz,
  Lösungsschlüssel, Build und Prüfer. Use when the user says "PLF bauen",
  "Prüfung aus dem Aufgabenpool", "Schularbeit zusammenstellen", "Test mit
  Gruppen A/B", "Prüfung mit Fragmenten" or asks for a printed exam from the
  variant pool. Do not use for Markdown-Wissensüberprüfungen (knowledge-exam)
  or for assignments in the cohort folder (homework).
license: MIT
compatibility: opencode
metadata:
  category: education
  output: exam-latex
---

# PLF aus dem Aufgabenpool bauen

Eine PLF ist hier kein neu getippter Text, sondern eine **Auswahl**: jede
Aufgabe ist ein LaTeX-Fragment aus dem Pool (`docs/ai/aufgaben/**/varianten/`),
Angabe und Lösung als Paar. Du wählst, setzt die Punkte und baust die zwei
Gruppen — du schreibst keine Aufgabentexte um.

## Begriffe

- **Gruppe A / Gruppe B** — die beiden Prüfungsversionen derselben PLF.
  `-gruppe-a`/`-gruppe-b` im Dateinamen heißt genau das.
- **Variante** — eine konkrete Aufgabe im Pool.
- **Variantenfamilie** — Varianten desselben Typs mit **identischem
  Fragenskelett** (gleiche Teilfragen, gleiche Bearbeitungsform); nur die
  Instanz unterscheidet sie. Ein Typ-Ordner kann mehrere Familien enthalten.
- **Fragenskelett** — das, was innerhalb einer Familie konstant ist; es ist das
  Vergleichskriterium für ein A/B-Paar.

## Ablauf

### 1. Rahmen festlegen

Klasse, Datum, Fach und Umfang („von Anfang bis inklusive …“) klären. Anlegen
als Bereich, nicht als Aufgabenliste: `check_scope.py --new --bis <name>`.
`check_scope.py <stoff.md> --list` zeigt die Typen mit Punkten und die im
Schuljahr noch **freien** Varianten (einmal verwendet = für alle Klassen des
Schuljahrs verbrannt).

Fertig, wenn `<klasse>/<YYYY-MM-DD>__<thema>/` mit `<datum>_<klasse>.stoff.md`
existiert und `--list` genug freie Varianten zeigt. `⚠` in der Liste heißt
fehlender Content, nicht schlechte Auswahl.

### 2. Varianten wählen — A und B als Zwillinge

Je Position ein Typ; für Gruppe B eine **andere Variante derselben
Variantenfamilie**: gleiches Fragenskelett, gleiche Punkte, andere Instanz.

Gibt der freie Vorrat die Familie nicht doppelt her, legst du den Zwilling an
(`…-gruppe-b.tex` + `.loesung.tex` + Variantenseite mit `familie:`), statt auf
eine strukturell andere Variante desselben Typs auszuweichen. Zwei Familien
desselben Typs nebeneinander (etwa „Kantenliste zeichnen + Komplement“ neben
„abstrakt: wieviele Kanten?“) sind ein Fehler, auch wenn beide dasselbe Thema
prüfen.

Fertig, wenn jede Position zwei Varianten derselben Familie hat und
`make verfuegbarkeit` sie als verbraucht führt.

### 3. Angabe bauen

Instanz-Ordner, je Aufgabe `\def\fragpunkte{N}` und darunter
`\input{…/<TypID>-<slug>.tex}`. Die Punktzahl steht **nur** in der Prüfung,
nie im Fragment. Vor jeder Aufgabe mit TikZ-Graph ein Seitenumbruch
(`\vfill\begin{center}{\bf Bitte wenden!}\end{center}\pagebreak`).

Der **Titel** nennt Umfang und Thema, nicht das Ergebnis: „Ein Graph aus einer
Kantenliste“, nicht „K_4,6 aus einer Kantenliste“ (bipartit!) und nicht
„Windmühle“ (planar!). Der Graphename gehört in den Lösungsschlüssel und in
die Variantenseite.

### 4. Lösungsschlüssel bauen

`loesungen_<datum>_<klasse>.tex` im selben Ordner, dieselbe Auswahl als
`.loesung.tex`; je Aufgabe eine Überschrift mit Punktzahl und — erlaubt, weil
prüferseitig — dem Graphenamen.

### 5. Prüfen

```sh
make check            # docs, scope, fragmente, verfuegbarkeit, plf-check
make fragmente-pdf    # Kompilier-Gate aller Fragmente
cd <klasse>/<ordner> && pdflatex <angabe>.tex && pdflatex loesungen_<datum>_<klasse>.tex
pdftotext <angabe>.pdf - | grep 'Aufgabe [0-9]'   # Titel-Stichprobe
```

`plf-check` paart A und B über den Typ (die Reihenfolge darf abweichen) und
vergleicht Punkte, Familie und Skelett. Bereits gehaltene Prüfungen bleiben
unangetastet: ihre Abweichung wird in der `.tex` mit
`% plf-paar-ausnahme: <Begründung>` dokumentiert und erscheint als Warnung.

Fertig, wenn `make check` grün ist, beide PDFs bauen und die Titel Stichprobe
für Stichprobe nichts verraten.

### 6. Nach der Prüfung

`make verfuegbarkeit` nachziehen (neue Verbrannt-Liste), dann Prüfung und
Lösung veröffentlichen, sobald sie gehalten ist; der Rohbestand der Abgaben
bleibt im privaten `-T`-Repo.

## Ablage

- Fragmente und Variantenseiten: `docs/ai/aufgaben/<bereich>/<thema>/<typ>/varianten/`
- Prüfungen: `<klasse>/<YYYY-MM-DD>__<thema>/` (aktuelle), `SJ<YY><YY>/` (Archiv, nur PDF gepflegt)
- Repo-Konventionen: `docs/ai/CONVENTIONS.md` („Prüfung aus Fragmenten bauen“), Begriffe: `docs/ai/DOMAIN.md`

`CONVENTIONS.md` gewinnt bei Abweichungen; diese Skill beschreibt das
Verfahren, nicht die Dateipfade des einzelnen Repos.
