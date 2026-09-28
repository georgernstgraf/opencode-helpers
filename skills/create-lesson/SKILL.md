---
name: create-lesson
description: "Richtet zu einem Kompetenzmodul (KM) oder Teilen davon — den geplanten Einheiten im unterricht/-Ordner — eine Lesson her (self-contained HTML: Erklärung, Quiz, Aufgabe) und legt sie als Prepared Lesson in unterricht/<PREFIX>-<NN>-<slug>/ ab. Use when the user says 'Lektion bauen/erstellen', 'Unterrichtseinheit ausarbeiten', 'Wiederholungs-Lektion', 'on demand eine Lektion einstreuen' oder eine Lesson-HTML für den Unterricht gebraucht wird."
license: MIT
compatibility: opencode
---

# Create-Lesson-Skill

Richtet zu einem **Kompetenzmodul (KM) oder Teilen eines KM** — den geplanten
Einheiten im `unterricht/`-Ordner — eine **Lesson** her: eine selbständige
HTML-Seite für Schüler:innen mit Erklärung, interaktivem Quiz und integrierter
**Aufgabe** am Lesson-Ende (Aufgabe = Mitarbeit). Der Skill arbeitet **in
`unterricht/`** und legt dort **Prepared Lessons** ab; die Übernahme in den
Klassenordner erfolgt per Hand. Konventionsbasiert, nicht auf ein Fach
verdrahtet (Vorbild: `lehrplan`- und `teach`-Skill).

Kanonische Referenz-Implementierung (zentrales `assets/`, Bootstrap/Badge,
`<PREFIX>-<NN>-<slug>/`, Beamer-taugliche Code-Boxen, Stil-Leitfaden):
`/home/georg/repos/georgernstgraf/GRG-PMM`.

## Abgrenzung zum Teach-Skill (wichtig, keine Duplikation)

- **`teach` = Selbstlernen** (die Lehrperson lernt: Lernpfade, Meisterschaft,
  Learning Records). Die HTML-Anatomie dort (self-contained, Assets,
  Quiz-Widget-Muster) wird hier **referenziert, nicht kopiert**.
- **`create-lesson` = Lehren** (Schüler-Material): KM-/einheitengebunden,
  lektüregebunden (Lizenzregeln!), per Code-Ausführung verifiziert, als
  **Prepared Lesson** in `unterricht/<PREFIX>-<NN>-<slug>/` abgelegt.
- Faustregel: Wer `MISSION.md`/`learning-records/` braucht → `teach`.
  Wer `KM + Ziel-UE` nennt → dieser Skill.

## Grundregeln (nicht verhandelbar)

1. **Anforderung ist das KM, nicht die Unterlage.** Was die Lesson lehren
   muss, ergibt sich aus dem KM/der Ziel-UE im `unterricht/`-Plan. Der
   vorhandene Bestand (`Unterlagen/`, frühere Lektionen) ist die *bisherige
   gelebte Praxis*: Der Skill prüft **kritisch, ob er das geforderte Material
   ausreichend abdeckt**, darf daraus borgen und kopieren — aber der Bestand
   ist **keine Obergrenze**. Deckt er nicht, ergänzt der Skill eigenständig.
2. **Nie nachfragen.** Fehlende Angaben werden autonom aufgelöst, in dieser
   Reihenfolge: (a) `unterricht/`-Plan + KM, (b) `Unterlagen/` und bestehende
   Lektionen, (c) PMM-Referenz. Einzige zulässige Rückfrage: fehlendes
   Bestellformat (KM/Ziel-UE/Thema).
3. **Arbeitsort `unterricht/`.** Prepared Lessons liegen **flach** unter
   `unterricht/` als `<PREFIX>-<NN>-<slug>/` (`KM<#>` = Kompetenzmodul,
   `SA` = schulautonom; `<NN>` läuft **pro KM**) und bestehen aus
   `praesentation.html` + `hausaufgabe.md` + `lesson.html`. Klassenordner
   werden **nicht** direkt beschrieben — die Lehrperson kopiert die Lesson per
   Hand in den Datums-Ordner der Klasse.
4. **Immer 90 Minuten.** Eine Lesson ist **immer** eine ganze Doppelstunde
   (~90 min) — auch eine Wiederholung. Mehrere Aufbauschritte, Beispiele,
   Übungen, Quiz; nie eine 15-Minuten-Zusammenfassung.
5. **Vollständigkeit des KM.** Alle Wege/Konzepte des KM kommen vor (Beispiel
   CSS-Einbindung: `style`-Attribut, `<style>`-Block im HTML, verlinktes
   Stylesheet — alle drei).
6. **Beamer-Tauglichkeit.** Code-Boxen sind **hell** (heller Grund, dunkle
   Schrift), kontrastreich, ausreichend groß und umbruchfreundlich; **keine
   schwarzen/dunklen Code-Boxen**. Erzeugen zentrale Assets die Boxen, wird
   das Asset an der zentralen Stelle korrigiert (nicht pro Lesson
   überschrieben).

## Präludium: Repo-Stand lesen (vor jedem Bau)

1. **Plan/KM:** `unterricht/` — die UE-Zeile zum Ziel-KM/Teil-KM
   finden (Lektüre-Anker, Ziel). `lehrplan/`-Ebene (KM-Steckbriefe) bei Bedarf
   gegenlesen.
2. **Unterlagen (Coverage-Check):** themenspezifische `Unterlagen/`
   (Folien-PDF/PPTX, `.md`, Demos) + bestehende Lektionen lesen. Notieren, was
   sie lehren — und **was zur KM-Anforderung fehlt** (wird ergänzt).
3. **Stil:** (a) bestehende Lektionen des Repos, (b) `docs/stil-leitfaden.md`,
   (c) PMMs `docs/stil-leitfaden.md`. Nie nachfragen.
4. **Layout:** Konvention des Repos/der Zielklasse übernehmen; kein fremdes
   Layout aufzwingen.
5. **Assets:** zentrales repo-weites `assets/` vorhanden? Den gemeinsamen
   Bootstrap (`assets/loader.js`), das Theme (`assets/theme.js` +
   `lesson.css`), das Quiz (`assets/quiz.js`) und den Badge wiederverwenden.
   Fehlt ein Baustein, einmal im zentralen `assets/` ergänzen — Reuse vor
   Duplikat.
6. **Tabellen-Stand:** Lessons-Tabelle im Klassen-README (Nr., Quiz-Richtige)?
   Nächste freie Nummer + Start-Rotation der Quiz-Positionen daraus ablesen.

Nichts ungefragt anlegen oder migrieren, außer es fehlt zum Bau (dann ergänzen,
Befund melden). **Kein Nachfragen** — Lücken autonom aus (a) `unterricht/`-Plan,
(b) bestehenden Lektionen, (c) PMM-Referenz schließen.

## Bestellformat

`KM/Teil-KM + Ziel-UE + Thema`. Beispiele:

- „KM3 Basis-Webtechniken, UE 3: CSS-Basics für 3AAIF/3CAIF"
- „Wiederholung Verteilungen aus KM5 für 4AHWIT UE 4"

Ohne Bestellformat wird nicht gebaut — das ist die einzige zulässige Rückfrage.

## Bauablauf (8 Schritte)

1. **Quelle grounden:** KM-Anforderung festhalten; `Unterlagen/` + frühere
   Lektionen als Quelle nutzen (borgen/kopieren erlaubt). **Lizenzregel:**
   Lektüre immer per URL/Kapitel zuweisen, nie Text übernehmen („link, don't
   copy"; besonders CC BY-NC-ND-Werke: Didaktik übernehmen, Wortlaut nie).
   Nur verlinken, was verifiziert existiert (keine erfundenen Deep-Links — im
   Zweifel Buch-Root + Kapitelnummer).
2. **Tiefe & Umfang:** Erstkontakt = Grundbegriffe aufbauen. Wiederholung =
   reaktivieren + eine Stufe höher (keine Grundbegriffe neu einführen),
   Anschluss an das Vorwissen der Zielklasse explizit benennen. Immer so viel
   Stoff, dass es eine **Doppelstunde** trägt.
3. **Kopf (themenfokussiert):** Zeile 1 = `Lektion <PREFIX>-<NN> · Thema`
   (`KM<#>`/`SA`, z. B. `KM5-01`). Zeile 2 klein = `UE n · Klasse Semester [·
   Wiederholung aus KMx]`. Thema zuerst, Provenienz zweitrangig aber
   auffindbar. Lehrplan, KM-Bezug und Runtime gehören **nicht** in den
   HTML-Header — sie stehen unten im Tages-README (siehe § Tages-README).
4. **HTML-Gerüst, Bootstrap & Badge:** Jede Lesson nutzt im `<head>` den
   **generischen Inline-Bootstrap** (findet `assets/loader.js` über die
   Ahnen-Verzeichnisse; Repo-Name nirgends im Code) mit `data-css`/`data-js`
   (Stylesheet + Theme + Quiz). Der Loader injiziert zusätzlich `assets/site.js`
   (Pages-Basis) und `assets/github-pages-link.js` (Badge „Auf GitHub Pages
   ansehen", fixiert, `no-print`). Toggle-Button im Header. Default folgt
   `prefers-color-scheme`, die Wahl per `localStorage` gemerkt, **Print immer
   hell**, kein CDN. Fehlt ein Baustein im zentralen `assets/`, einmal ergänzen
   — Reuse vor Duplikat. Seiten laufen über den Live-Server (`serve.sh`), nie
   `file://`.
5. **Dramaturgie (6 Bausteine):** Einstiegsfrage (reale Frage mit Datenbezug)
   → Ziel-Artefakt (fertiger Plot/Tabelle als Sehnsuchtsbild) →
   inkrementeller Aufbau (ein Konzept pro Schritt, ein Beispiel durchgehend)
   → „Jetzt du!" (3 Aufgaben: Vorhersage zuerst, dann ausführen; Interleaving
   früherer Lessons) → Typische Fehler (je mit Anti-Beispiel-Code) →
   Zusammenfassung (Tabelle) + Ausblick (Folge-UE im **Ziel**-Semesterplan).
   Dazu Lektüre-Box mit Pflicht-Charakter am Anfang.
6. **Quiz:** so viele Fragen, wie der Stoff braucht — **keine harte
   Obergrenze** (auch 10+ sind in Ordnung). Die Richtige-Positionen über die
   tatsächliche Fragenzahl ausgewogen rotieren, je Frage genau eine Richtige;
   Antwortoptionen gleiche Wortzahl (möglichst Zeichenzahl) — keine
   Format-Hinweise. Fragen decken **ausschließlich** Stoff, der in der Lesson
   tatsächlich eingeführt wurde — kein Vorgriff auf Folge-UE, keine nur
   beiläufig genannten Begriffe. Markup:
   `<div class="quiz" data-loesung="N">` (zentrales `assets/quiz.js`).
7. **Aufgabe:** Abschnitt **„Aufgabe"** direkt am Lesson-Ende anhängen
   (nach Zusammenfassung/Ausblick): stufenweise aus dem Lesson-Stoff gestuft,
   Vorhersage-Aufgabe zuerst, plus Abgabehinweis (Konvention der Klasse, z. B.
   Commit im Schüler-Repo). Der schülerseitige Begriff ist immer **Aufgabe**,
   nie „Hausübung" — die Aufgabe **ist** die Mitarbeit. Die Tages-README-
   Vorlage verweist darauf (z. B. „Aufgabe: Abschnitt am Lesson-Ende").
   Existiert ein Aufgaben-Master im Repo, auf ihn verlinken statt duplizieren.
8. **Beamer-Check & Code-Stil:** Code-Boxen hell und groß genug für den
   Projektor (siehe Grundregel 6). Projekt-Konvention (z. B. `<-`, Snake_case,
   natives Pipe); Output als Kommentar, Erklärung als Kommentar; Zeilen kurz
   halten.

## Prepared Lessons (Ablage & Lebenszyklus)

**Prepared Lesson** (undatiert, vorbereitet) liegt **flach** in
`unterricht/<PREFIX>-<NN>-<slug>/` (`KM<#>` = Kompetenzmodul, `SA` =
schulautonom; `<NN>` läuft pro KM) zusammen mit `praesentation.html` +
`hausaufgabe.md` + `lesson.html`. Dazu gehört eine **Tages-README-Vorlage**
`<PREFIX>-<NN>-<slug>.md` (Inhalt + `## Aufgabe` + `## Housekeeping`, siehe
§ Tages-README).

**Übernahme in den Unterricht:** Die Lehrperson kopiert die Prepared Lesson
per Hand in den Datums-Ordner der laufenden Klasse `<klasse>/YYYY-MM-DD__thema/`
als `lesson.html` plus `README.md` (aus der Vorlage). Der Skill schreibt **nie**
direkt in Klassenordner; Kohorten-`prepared-lessons/` gibt es nicht mehr.

## Tages-README (Layout, Pflicht bei der Übernahme)

Zu einer Lesson gehört ein Tages-README **im selben Datums-Ordner**
`<klasse>/YYYY-MM-DD__thema/README.md` (aus der Vorlage `<PREFIX>-<NN>-<slug>.md`). Oben
steht der Inhalt: Lektions-Link plus ein bis zwei Zeilen, was die Lesson lehrt
(Liste mit Demo/Quiz/…). Die Aufgabe ist **Pflicht** und steht als **erster
eigener `## Aufgabe`-Abschnitt (H2)** — nicht als Listenpunkt. Die
**Housekeeping-Infos** (Lehrplan · KM-Bezug · Runtime) stehen als
**letzter Abschnitt** — nie im Kopf, nie im HTML-Header:

```
# <Thema> (<Datum>)

Lesson: `lesson.html` im selben Ordner — <ein Satz, was sie lehrt>.
- Demo/Quiz/… (Inhalt, soweit vorhanden)

## Aufgabe
<Kurzbeschreibung> — Abgabe <Konvention>

## Housekeeping
- Lehrplan: <Pfad/Link>
- KM-Bezug: <KM + UE + Anschluss>
- Runtime: <z. B. Deno, R/tidyverse>
```

## Verifikation (vor Abgabe, Pflicht)

1. Jeder Code-Block läuft wie abgedruckt (per Ausführung gegen die echten
   Daten prüfen; behauptete Zahlen = berechnete Zahlen).
2. Alle relativen Links auflösbar (Assets, Nachbar-Lessons, Aufgabe,
   Semesterplan).
3. Kein CDN / keine externen Abhängigkeiten (läuft über den lokalen
   Live-Server `serve.sh`), außer verlinkter Lektüre.
4. Quiz klickbar, je Frage genau eine Richtige, Rotation über die
   tatsächliche Fragenzahl eingehalten; **jede Frage ist durch den
   Lesson-Text gedeckt** (kein nur genannter Begriff, kein Folge-UE-Stoff).
5. Aufgabe: Abschnitt am Lesson-Ende vorhanden (oder Aufgaben-Master-Link)
   **und** Tages-README-Vorlage mit erstem eigenem `## Aufgabe`-Abschnitt (H2)
   und `## Housekeeping` zuletzt — Pflicht.
6. Light/Dark-Umschalter vorhanden und klickbar; Default folgt dem
   Betriebssystem, die Wahl überlebt den Reload, Print bleibt hell.
7. Bootstrap + Badge: generische Inline-Bootstrap im `<head>` vorhanden und
   `assets/loader.js` erreichbar; der Badge erscheint und zeigt auf die
   kanonische Pages-URL. Alles über den Live-Server (`serve.sh`), nie `file://`.
8. **Beamer:** keine dunklen Code-Boxen; Code ausreichend groß und
   umbruchfreundlich.
9. **Umfang:** die Lesson ist eine ganze Doppelstunde (90 min) — Pflicht.
10. **KM-Vollständigkeit:** alle im KM geforderten Wege/Konzepte kommen vor.

## Nachziehen (gleicher Commit)

- Lessons-Tabelle im Klassen-README (Nr. · Ziel-UE vollqualifiziert ·
  Thema · Quelle · Typ · Quiz-Richtige · Status); Aufgaben-Spalte statt „HÜ",
  Quiz-Richtige als Sequenz (z. B. `B·A·C·D·B`).
- Tages-README-Vorlage nach § Tages-README (Aufgabe als erster
  `## Aufgabe`-Abschnitt (H2), Housekeeping-Block zuletzt).
- Neue Fachbegriffe ins Glossar (mit vollqualifiziertem UE-Verweis).
- Commit-Message nach Repo-Konvention (mit Issue-Nummer, falls verlangt).

## Was dieser Skill NICHT tut

- Keine Semesterpläne entwerfen (lehrplan-Skill, Aufgabe 3).
- Keine Lessons unterhalb der KM-Anforderung oder ohne Bezug zu KM/Unterlagen
  erfinden.
- Keine Folien anlegen. Die Aufgabe gehört in die Lesson — ein separater
  Aufgaben-Master entsteht nur, wenn die Repo-Konvention einen verlangt.
- Nicht direkt in Klassenordnern schreiben (Übernahme per Hand).
- Keine Selbstlern-Pfade (teach-Skill).
