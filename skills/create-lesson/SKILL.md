---
name: create-lesson
description: "Baut Klassen-Lektionen (self-contained HTML: Erklärung, Quiz, Hausaufgabe) aus Semesterplänen und Lehrplan-Extrakten — für Erstkontakt und Wiederholung aus früheren Jahrgängen. Use when the user says 'Lektion bauen/erstellen', 'Unterrichtseinheit ausarbeiten', 'Wiederholungs-Lektion', 'on demand eine Lektion einstreuen' oder a lesson HTML file is needed for classroom use."
license: MIT
compatibility: opencode
---

# Create-Lesson-Skill

Baut **Klassen-Lektionen**: selbständige HTML-Seiten für Schüler:innen mit
Erklärung, interaktivem Quiz und Hausaufgaben-Verweis — gegründet auf
Semesterplan (Ziel-UE) und Lehrplan-Extrakt (Quelle-KM). Funktioniert in
jedem Unterrichts-Repo, das der `lehrplan/`-Konvention folgt
(konventionsbasiert, nicht auf ein Fach verdrahtet — Vorbild: `lehrplan`-Skill).

## Abgrenzung zum Teach-Skill (wichtig, keine Duplikation)

- **`teach` = Selbstlernen** (die Lehrperson lernt: Lernpfade, Meisterschaft,
  Learning Records). Die HTML-Anatomie dort (self-contained, Assets,
  Quiz-Widget-Muster) wird hier **referenziert, nicht kopiert**.
- **`create-lesson` = Lehren** (Schüler-Material): lehrplangebunden
  (Quelle↔Ort), lektüregebunden (Lizenzregeln!), per Code-Ausführung
  verifiziert, in Klassenordnern abgelegt und ggf. über Kohorten gespiegelt.
- Faustregel: Wer `MISSION.md`/`learning-records/` braucht → `teach`.
  Wer `Thema + Ziel-UE` nennt → dieser Skill.

## Präludium: Repo-Stand lesen (vor jedem Bau)

1. **Lehrplan-Ebene:** `lehrplan/<zweig>/` vorhanden? KM-Steckbriefe
   (`kompetenzmodule/km*.md`), Ressourcen-Matrix, LEHRPLAN-Extrakt lesen.
2. **Unterrichtsebene:** `unterricht/<ZWEIG>-<FACH>/jgN-semesterplan-{ws,ss}.md`
   — die UE-Zeile zum Thema finden (Lektüre-Anker, R-Umsetzung/Werkzeug).
3. **Stil:** Repo-eigener Stil-Leitfaden (z. B. `docs/stil-leitfaden.md`)?
   Falls nein: Fallback-Dramaturgie aus § Bauablauf Schritt 4.
4. **Kohorten-Modell:** Klassenordner mit Master/Kopie-Regel aus README?
   Falls ja: Master bauen, Kopien spiegeln. Falls nein/unbekannt: erfragen.
5. **Daten:** Welche Datensätze nutzt die Zielklasse (Assets/CSV, Pakete)?
   Lesson-Code muss auf denselben Daten laufen wie der Unterricht.
6. **Tabellen-Stand:** Lessons-Tabelle im Klassen-README (Nr., Quiz-Richtige)?
   Nächste freie Nummer + nächste Quiz-Position daraus ablesen.

Nichts davon ohne ausdrückliche Anweisung neu anlegen oder migrieren —
Befunde melden, Bau fortsetzen soweit möglich.

## Bestellformat

`Thema + Ziel-UE [+ Quelle bei Wiederholung]`. Beispiele:

- „ANOVA-Varianzanalyse für 4AHWIT UE 8" (Erstkontakt: Quelle = Ziel-KM)
- „Wiederholung Verteilungen aus KM5 für 4AHWIT UE 4" (Quelle ≠ Ziel)

## Bauablauf (on-demand, 7 Schritte)

1. **Quelle grounden:** Matrix-Key des Quell-KMs, KM-Steckbrief
   (Wissen/Verstehen/Können), Lektüre-Anker. **Lizenzregel:** Lektüre immer
   per URL/Kapitel zuweisen, nie Text übernehmen („link, don't copy";
   besonders CC BY-NC-ND-Werke: Didaktik übernehmen, Wortlaut nie).
   Nur verlinken, was verifiziert existiert (keine erfundenen Deep-Links —
   im Zweifel Buch-Root + Kapitelnummer).
2. **Tiefe wählen:** Erstkontakt = Grundbegriffe aufbauen. Wiederholung =
   reaktivieren + eine Stufe höher (keine Grundbegriffe neu einführen),
   Anschluss an das Vorwissen der Zielklasse explizit benennen.
3. **Kopf (themenfokussiert):** Zeile 1 = `Lektion NN · Thema`
   (zweistellig, pro Schuljahr pro Klasse — max. ~40 Wochen). Zeile 2 klein =
   `UE n · Klasse Semester [· Wiederholung aus KMx]`. Thema zuerst,
   Provenienz zweitrangig aber auffindbar.
4. **Dramaturgie (6 Bausteine):** Einstiegsfrage (reale Frage mit Datenbezug)
   → Ziel-Artefakt (fertiger Plot/Tabelle als Sehnsuchtsbild) →
   inkrementeller Aufbau (ein Konzept pro Schritt, ein Datensatz durchgehend)
   → „Jetzt du!" (3 Aufgaben: Vorhersage zuerst, dann ausführen; Interleaving
   früherer Lessons) → Typische Fehler (je mit Anti-Beispiel-Code) →
   Zusammenfassung (Tabelle) + Ausblick (Folge-UE im **Ziel**-Semesterplan).
   Dazu Lektüre-Box mit Pflicht-Charakter am Anfang.
5. **Quiz:** genau 1 Frage pro Lesson; Richtige-Position aus der
   Klassen-Tabelle rotieren (A/B/C/D); Antwortoptionen gleiche Wortzahl
   (möglichst Zeichenzahl) — keine Format-Hinweise.
6. **Hausaufgabe:** Auf bestehenden HÜ-Master verlinken. Existiert keiner,
   wird die Lücke als Folge-Item (Datei + Issue) festgehalten — keine
   HÜ ad hoc in die Lesson schreiben.
7. **Code-Stil:** Projekt-Konvention (z. B. `<-`, Snake_case, natives Pipe);
   Output als Kommentar, Erklärung als Kommentar; Zeilen kurz halten.

## Dateinamen

`NN-thema-slug.html` (zweistellig, kleingeschrieben, Bindestriche),
z. B. `04-anova-varianzanalyse.html`. Ablage: Lessons-Ordner des
Klassenverzeichnisses (Konvention des Repos, z. B. `<klasse>/lessons/`
oder `<klasse>/teach/lessons/`).

## Verifikation (vor Abgabe, Pflicht)

1. Jeder Code-Block läuft wie abgedruckt (per Ausführung gegen die echten
   Daten prüfen; behauptete Zahlen = berechnete Zahlen).
2. Alle relativen Links auflösbar (Assets, Nachbar-Lessons, HÜ, Semesterplan).
3. Kein CDN / keine externen Abhängigkeiten (Offline-Lesbarkeit), außer
   verlinkter Lektüre.
4. Quiz klickbar, genau eine Richtige, Rotation eingehalten.

## Nachziehen (gleicher Commit)

- Lessons-Tabelle im Klassen-README (Nr. · Ziel-UE vollqualifiziert ·
  Thema · Quelle · Typ · Quiz-Richtige · Status).
- Kohorten-Spiegel nach Master-Regel des Repos.
- Neue Fachbegriffe ins Glossar (mit vollqualifiziertem UE-Verweis).
- Commit-Message nach Repo-Konvention (mit Issue-Nummer, falls verlangt).

## Was dieser Skill NICHT tut

- Keine Semesterpläne entwerfen (lehrplan-Skill, Aufgabe 3).
- Keine Folien/Hausaufgaben-Master anlegen (Folge-Items statt Ad-hoc-Bau).
- Keine Selbstlern-Pfade (teach-Skill).
