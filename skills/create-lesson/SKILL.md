---
name: create-lesson
description: "Richtet zu einem Kompetenzmodul (KM) oder einem Thema daraus eine kohortenagnostische Lesson her (self-contained HTML: Lektion und Präsentation in einem — Erklärung, Lernquizzes, drei Übungsbeispiele, beamer-tauglich) und legt sie als Prepared Lesson in unterricht/<PREFIX>-<NN>-<slug>/ ab (und verlinkt sie im Lernplattform-Navigator index.html) — ohne lauffähigen Projektcode, Beispielprojekte liegen in der Beispielprojekt-Ablage des Repos. Eine Zuordnung zu einer geplanten Unterrichtseinheit im Semesterplan ist möglich, aber optional — die Lesson gehört zum Thema und KM, nicht zu einer Kohorte. Use when the user says 'Lektion bauen/erstellen', 'Unterrichtseinheit ausarbeiten', 'Wiederholungs-Lektion', 'on demand eine Lektion einstreuen' oder eine Lesson-HTML für den Unterricht gebraucht wird."
license: MIT
compatibility: opencode
---

# Create-Lesson-Skill

Richtet zu einem **Kompetenzmodul (KM) oder einem Thema daraus** eine
**Lesson** her: eine selbständige HTML-Seite für Schüler:innen mit Erklärung,
**Lernquizzes** über den Stoff verteilt und **drei abzugebenden
Übungsbeispielen** am Lesson-Ende (die Beispiele = Mitarbeit). Der Skill
arbeitet **in `unterricht/`** und legt dort **Prepared
Lessons** ab; die Übernahme in den Kohortenordner erfolgt **per Hand** durch
die Lehrperson. Konventionsbasiert, nicht auf ein Fach verdrahtet (Vorbild:
`lehrplan`- und `teach`-Skill).

## Kohorten-Agnostik (Grundprinzip)

Eine Lesson gehört zu einem **Thema**, das einen **Teil eines KM** deckt —
nicht zu einer Kohorte und nicht zu einer fest geplanten Unterrichtseinheit:

- **Thema → KM** ist die tragende Zuordnung. Das Thema deckt einen Teil des
  Kompetenzmoduls ab; der Skill prüft gegen die KM-Anforderung, nicht gegen
  einen Stundenplan.
- **UE-Zuordnung ist optional.** Semesterpläne können dem Thema eine
  Unterrichtseinheit *zuordnen* — sie müssen es nicht. Die Dynamik des
  tatsächlichen Unterrichts macht eine feste Direktzuordnung lächerlich; der
  Skill erzwingt sie daher **nie** und befasst sich **nicht mit dem
  Lernfortschritt einzelner Kohorten**.
- **Übernahme bleibt manuell.** Die Lehrperson entscheidet zur Tagesdynamik,
  welche vorbereitete Lektion passt, **kopiert** sie per Hand vom
  Unterrichtsordner in den jeweiligen **Kohortenordner** und fügt das **Datum
  manuell in den Ordnernamen** ein. Der Skill schreibt nie in Kohortenordner
  und führt keine Kohorten-Statistik.

Kanonische Referenz-Implementierung (zentrales `assets/`, Bootstrap/Badge,
`<PREFIX>-<NN>-<slug>/`, Stil-Leitfaden):
`/home/georg/repos/georgernstgraf/GRG-PMM`.
**Hinweis:** PMM trennt teils `lesson.html` und `praesentation.html`
(Reveal.js/CDN) — das ist die *alte* Praxis. Hier gilt **Lektion und
Präsentation in einem** (Grundregel 6): **eine** HTML, kein Foliensatz,
kein Framework/CDN.

## Lernplattform: GitHub Pages & `index.html`

**GitHub Pages ist die Lernplattform des Repos.** Veröffentlicht und verlinkt
wird **ausschließlich `unterricht/`** — plus das zentrale `assets/` und der
Navigator `index.html`. Alles andere ist **nicht** Teil der Lernplattform:
Kohorten-Ordner, `lehrplan/`, `Unterlagen/`, Archiv-Ordner usw. werden weder
deployt noch vom Navigator verlinkt.

- Der Root-`index.html` ist der **Navigator** der Lernplattform. Er listet die
  Prepared Lessons aus `unterricht/<PREFIX>-<NN>-<slug>/` — gruppiert nach
  Jahrgang/KM — und verlinkt **nur** `unterricht/`-Ziele.
- **Jede neu gebaute Lesson wird im selben Commit im `index.html` verlinkt**
  (Titel + ein Satz „Worum geht's"). Bestehende Blöcke/Einträge ergänzen,
  nicht umsortieren; fehlt der passende Block, einen anlegen.
- Das Deployment läuft über `.github/workflows/pages.yml` und kopiert nur
  `index.html`, `assets/` und `unterricht/` (rsync) in die Site. Fehlt der
  Workflow, einmal nach dem Vorbild des Repos (bzw. GRG-INFI/GRG-PMM) anlegen.
- **Prepared Lessons müssen in allen Auslieferungskontexten funktionieren** —
  lokal über `./serve.sh`, im **VS-Code-Browser** (Simple Browser/Live Preview,
  immer über die Server-URL, **nie** `file://`) **und** auf GitHub Pages unter
  der Basis `/<repo>/`. Daraus folgen: Nicht-Asset-Links **relativ**; **kein
  `<base>`**, **keine root-absoluten Pfade**; Assets nur über den generischen
  Ahnen-Bootstrap (Root-Resolver, kein Repo-Name); **genau ein** Top-Level-
  `assets/` (kein Dot-Ordner `.assets` — Pages überspringt diese; ggf.
  `.nojekyll`); Badge-Basis aus `assets/site.js`.
- **Referenzen liegen außerhalb des Deploys:** `GLOSSAR.md` (und weiteres
  Root-Nachschlagewerk) wird **nicht** mitdeployt. Links aus Lessons/Navigator
  darauf laufen daher über die **GitHub-URL** des Repos (siehe § Referenzmaterial).

## Referenzmaterial (nicht unter `unterricht/`)

`unterricht/` ist **nicht** der Ort für Nachschlagewerke — dort liegen
ausschließlich Lesson-Ordner (Grundregel 3):

- **Glossar = `GLOSSAR.md` im Repo-Root.** Neue Fachbegriffe (mit KM-Verweis;
  UE-Verweis nur, wenn tatsächlich zugeordnet) kommen dorthin.
- **Weiteres repo-weites Nachschlagewerk** (z. B. ein SQL-Spickzettel) liegt
  ebenfalls als eigene Markdown-Datei im **Repo-Root** — nie als `reference/`
  unter `unterricht/`.
- **Lesson-spezifische Checklisten** (z. B. eine Normalformen-Tabelle) bleiben
  **in** der jeweiligen Lesson.
- Auf Root-Referenzen wird per **GitHub-URL** verlinkt (siehe § Lernplattform).

## Abgrenzung zum Teach-Skill (wichtig, keine Duplikation)

- **`teach` = Selbstlernen** (die Lehrperson lernt: Lernpfade, Meisterschaft,
  Learning Records). Die HTML-Anatomie dort (self-contained, Assets,
  Quiz-Widget-Muster) wird hier **referenziert, nicht kopiert**.
- **`create-lesson` = Lehren** (Schüler-Material): KM-/themengebunden,
  kohortenagnostisch, lektüregebunden (Lizenzregeln!), per Code-Ausführung
  verifiziert, als **Prepared Lesson** in `unterricht/<PREFIX>-<NN>-<slug>/`
  abgelegt.
- Faustregel: Wer `MISSION.md`/`learning-records/` braucht → `teach`.
  Wer `KM + Thema` nennt → dieser Skill.

## Grundregeln (nicht verhandelbar)

1. **Anforderung ist das KM, nicht die Unterlage.** Was die Lesson lehren
   muss, ergibt sich aus dem KM bzw. dem bestellten Thema
   (`lehrplan/kompetenzmodule/`; der Semesterplan dient nur als optionale
   Orientierung, welche UE das Thema typischerweise trägt). Der
   vorhandene Bestand (`Unterlagen/`, frühere Lektionen) ist die *bisherige
   gelebte Praxis*: Der Skill prüft **kritisch, ob er das geforderte Material
   ausreichend abdeckt**, darf daraus borgen und kopieren — aber der Bestand
   ist **keine Obergrenze**. Deckt er nicht, ergänzt der Skill eigenständig.
2. **Nie nachfragen.** Fehlende Angaben werden autonom aufgelöst, in dieser
   Reihenfolge: (a) KM-Steckbriefe + Semesterplan, (b) `Unterlagen/` und
   bestehende Lektionen, (c) PMM-Referenz. Einzige zulässige Rückfrage:
   fehlendes Bestellformat (KM/Thema).
3. **Arbeitsort `unterricht/`.** Prepared Lessons liegen **flach** unter
   `unterricht/` als `<PREFIX>-<NN>-<slug>/` (`KM<#>` = Kompetenzmodul,
   `SA` = schulautonom; `<NN>` läuft **pro KM**) und bestehen aus
   `lesson.html` + `Übungsbeispiele.md` (siehe
   § Prepared Lessons) — **kein lauffähiger Projektcode** (siehe
   § Beispielprojekte). Die `lesson.html` ist **zugleich die Präsentation**
   (Grundregel 6): **kein** separater Foliensatz. **`unterricht/`
   enthält ausschließlich solche Lesson-Ordner** — *keine* weiteren Ordner
   (kein `reference/`, kein lesson-lokales `assets/`; das repo-weite
   `assets/` liegt im Repo-Root). Kohortenordner werden **nicht** direkt
   beschrieben — die Lehrperson kopiert die Lesson per Hand in den
   Datums-Ordner der Kohorte (siehe § Prepared Lessons).
4. **Immer 90 Minuten.** Eine Lesson ist **immer** eine ganze Doppelstunde
   (~90 min) — auch eine Wiederholung. Mehrere Aufbauschritte, Beispiele,
   Übungen, Quiz; nie eine 15-Minuten-Zusammenfassung.
5. **Vollständigkeit des KM.** Alle Wege/Konzepte des KM kommen vor (Beispiel
   CSS-Einbindung: `style`-Attribut, `<style>`-Block im HTML, verlinktes
   Stylesheet — alle drei).
6. **Lektion und Präsentation in einem (Beamer).** Eine Lesson ist **zugleich
   die Präsentation**: **eine** self-contained HTML, die im Unterricht am
   Beamer Schritt für Schritt projiziert wird — **kein** separater
   Foliensatz (`praesentation.html`), **kein** Folien-Framework/CDN. Daraus
   folgt die Beamer-Tauglichkeit: projizierbare Grundschrift und Kontraste,
   **ein Gedanke pro bildschirmgroßem Block** (abschnittsweise, nicht
   Textwüste); Code-Boxen sind **hell** (heller Grund, dunkle Schrift),
   kontrastreich, ausreichend groß und umbruchfreundlich; **keine
   schwarzen/dunklen Code-Boxen**. Erzeugen zentrale Assets die Boxen, wird
   das Asset an der zentralen Stelle korrigiert (nicht pro Lesson
   überschrieben).

## Beispielprojekte (kein Code unter `unterricht/`)

`unterricht/` ist **Unterrichtsmaterial-Ordner**: HTML, Markdown und die
zentralen `assets/` — aber **kein lauffähiger Projektcode**. Code-Beispiele, die
im `lesson.html` als Lehrmaterial *angezeigt* werden, sind erwünscht und
bleiben erlaubt; verboten sind **lauffähige Projektdateien** (Scaffolds,
`package.json`, Tests, Projekt-Datenbanken usw.), die man installieren und
starten kann.

Fertige Beispielprojekte gehören in die **Beispielprojekt-Ablage des Repos**,
außerhalb von `unterricht/`. Die Ablage wird ermittelt — **die Repo-Konvention
gewinnt, nicht ein fester Name**:

1. Explizite Nennung in `AGENTS.md`, `README.md` oder
   `docs/ai/ARCHITECTURE.md` (z. B. GRG-SWP: `Sample_Projects/`).
2. Sonst ein vorhandener Top-Level-Ordner mit diesem Zweck — **auch abweichend
   benannte**, etwa `Sample_Projects/`, `Beispielprojekte/`, `Beispiele/`,
   `Projekte/`, `examples/`, `praxis/`, oder funktional gleichwertige Ablagen
   (z. B. `Coole_Prisma_Schemas/`).
3. Ist keiner vorhanden: Default **`Beispielprojekte/`** anlegen und im
   `README.md`/`ARCHITECTURE.md` als Beispielprojekt-Ablage dokumentieren.

Ein Beispielprojekt liegt dort als eigenständiger Ordner
**`<Ablage>/km<#>-<NN>-<slug>/`** — das **KM-Präfix trägt jeder Beispielordner**
(z. B. `Beispielprojekte/km8-01-hono-formulare/`; `<#>` = KM, `<NN>` wie in der
zugehörigen Lesson). Jeder Ordner hat eine eigene README, eigene Abhängigkeiten
und ist für sich lauffähig und getestet. Die Lesson **verweist** darauf und
**dupliziert keinen Projektcode** — der Verweis steht im Lesson-Text bzw. in
den Übungsbeispielen, nicht als eingebettete Projektdatei. Da die Beispielprojekt-Ablage
**nicht** auf GitHub Pages liegt, erfolgt der Verweis aus der deployten Lesson
per **GitHub-URL** (siehe § Lernplattform).

## Präludium: Repo-Stand lesen (vor jedem Bau)

1. **Plan/KM:** KM-Steckbriefe (`lehrplan/kompetenzmodule/`) zum Ziel-KM/Thema
   lesen (Lektüre-Anker, Ziel, Bildungs- und Lehraufgabe). Semesterpläne
   (`lehrplan/<zweig>/jg<N>-semesterplan-*.md`) nur als optionale
   Orientierung — **keine Direktzuordnung zu einer UE, keine Kohorte**.
2. **Unterlagen (Coverage-Check):** themenspezifische `Unterlagen/`
   (Folien-PDF/PPTX, `.md`, Demos) + bestehende Lektionen lesen. Notieren, was
   sie lehren — und **was zur KM-Anforderung fehlt** (wird ergänzt).
3. **Stil:** (a) bestehende Lektionen des Repos, (b) `docs/stil-leitfaden.md`,
   (c) PMMs `docs/stil-leitfaden.md`. Nie nachfragen.
4. **Layout:** Konvention des Repos übernehmen; kein fremdes
   Layout aufzwingen.
5. **Assets:** zentrales repo-weites `assets/` vorhanden? Den gemeinsamen
   Bootstrap (`assets/loader.js`), das Theme (`assets/theme.js` +
   `lesson.css`), das Quiz (`assets/quiz.js`) und den Badge wiederverwenden.
   Fehlt ein Baustein, einmal im zentralen `assets/` ergänzen — Reuse vor
   Duplikat.
6. **Nummern-Stand:** Nächste freie `<NN>` pro `<PREFIX>` aus dem Bestand in
   `unterricht/` ablesen. Kohorten-READMEs (Lessons-Tabellen, Lernstände)
   werden **nicht** gelesen oder geschrieben — sie sind Sache der
   Lehrperson.
7. **Beispielprojekt-Ablage:** Wo liegen die lauffähigen Beispielprojekte des
   Repos (außerhalb `unterricht/`)? Repo-Konvention bzw. vorhandenen Ordner
   ermitteln — siehe § Beispielprojekte. Nichts anlegen, was anders benannt
   schon besteht.
8. **Navigator:** Root-`index.html` lesen — Aufbau (Jahrgangs-/KM-Blöcke) und
   bestehende Einträge verstehen, um die neue Lesson korrekt einzureihen
   (§ Lernplattform).

Nichts ungefragt anlegen oder migrieren, außer es fehlt zum Bau (dann ergänzen,
Befund melden). **Kein Nachfragen** — Lücken autonom aus (a) Semesterplan,
(b) bestehenden Lektionen, (c) PMM-Referenz schließen.

## Bestellformat

`KM/Teil-KM + Thema` — eine Ziel-UE oder Kohorte kann genannt werden, ist
aber **optional** und wird nur als Kontext notiert (nicht in die Lesson
gebacken). Beispiele:

- „KM3 Basis-Webtechniken, Thema: CSS-Basics"
- „Wiederholung Verteilungen aus KM5, Thema: Hypergeometrische Verteilung"
- „Wiederholung Verteilungen aus KM5 für 4AHWIT UE 4" (mit optionaler
  UE-Angabe)

Ohne Bestellformat (mindestens KM + Thema) wird nicht gebaut — das ist die
einzige zulässige Rückfrage.

## Bauablauf (10 Schritte)

1. **Quelle grounden:** KM-Anforderung festhalten; `Unterlagen/` + frühere
   Lektionen als Quelle nutzen (borgen/kopieren erlaubt). **Lizenzregel:**
   Lektüre immer per URL/Kapitel zuweisen, nie Text übernehmen („link, don't
   copy"; besonders CC BY-NC-ND-Werke: Didaktik übernehmen, Wortlaut nie).
   Nur verlinken, was verifiziert existiert (keine erfundenen Deep-Links — im
   Zweifel Buch-Root + Kapitelnummer).
2. **Tiefe & Umfang:** Erstkontakt = Grundbegriffe aufbauen. Wiederholung =
   reaktivieren + eine Stufe höher (keine Grundbegriffe neu einführen),
   Anschluss an das typische Vorwissen der Zielstufe benennen. Immer so viel
   Stoff, dass es eine **Doppelstunde** trägt.
3. **Kopf (themenfokussiert):** Zeile 1 = `Lektion <PREFIX>-<NN> · Thema`
   (`KM<#>`/`SA`, z. B. `KM5-03`). Zeile 2 klein = `Wiederholung aus KMx`
   bzw. leer — **keine Klasse, kein Semester, keine UE** (die Lesson ist
   kohortenagnostisch; UE/Klasse stehen nur im Kohorten-README, das die
   Lehrperson selbst pflegt). Thema zuerst, Provenienz zweitrangig aber auffindbar.
   Lehrplan, KM-Bezug und Runtime gehören **nicht** in den HTML-Header — sie
   stehen am Lesson-Ende im zugeklappten `<details>`-Block
   (siehe § Kopierzeile & Lehrplan-Details).
4. **HTML-Gerüst, Bootstrap & Badge:** Jede Lesson nutzt im `<head>` den
   **generischen Inline-Bootstrap** (findet `assets/loader.js` über die
   Ahnen-Verzeichnisse; Repo-Name nirgends im Code) mit `data-css`/`data-js`
   (Stylesheet + Theme + Quiz). Der Loader injiziert zusätzlich `assets/site.js`
   (Pages-Basis) und `assets/github-pages-link.js` (Badge „Auf GitHub Pages
   ansehen", fixiert, `no-print`). **Timing-Fallstrick:** `loader.js` injiziert
   alle diese Skripte dynamisch (asynchron) — `DOMContentLoaded` ist beim
   Ausführen oft schon vorbei. Init-Code (Quiz, Theme, Badge) muss deshalb bei
   `document.readyState !== "loading"` **sofort starten**, sonst erst auf
   `DOMContentLoaded` warten (Muster: `theme.js`, `github-pages-link.js`,
   `quiz.js`); sonst bleiben Quiz/Toggle auf der Live-Seite ohne Funktion.
   Toggle-Button im Header. Default folgt
   `prefers-color-scheme`, die Wahl per `localStorage` gemerkt, **Print immer
   hell**, kein CDN. Fehlt ein Baustein im zentralen `assets/`, einmal ergänzen
   — Reuse vor Duplikat. Seiten laufen über den Live-Server (`serve.sh`), nie
   `file://`.
5. **Dramaturgie (6 Bausteine):** Einstiegsfrage (reale Frage mit Datenbezug)
   → Ziel-Artefakt (fertiger Plot/Tabelle als Sehnsuchtsbild) →
   inkrementeller Aufbau (ein Konzept pro Schritt, ein Beispiel durchgehend)
   → „Jetzt du!" (3 Aufgaben: Vorhersage zuerst, dann ausführen; Interleaving
   früherer Lessons) → Typische Fehler (je mit Anti-Beispiel-Code) →
   Zusammenfassung (Tabelle) + Ausblick (thematisch auf verwandte
   Prepared Lessons bzw. den Semesterplan — ohne feste UE-Zuordnung).
   Dazu Lektüre-Box mit Pflicht-Charakter am Anfang.
6. **Lernquizzes (Format 2.0).** Quizze sind **Lernquizzes**, keine
   Punkteprüfung: Sie prüfen ausschließlich den *zuvor erklärten* Stoff und
   sind über die Lesson **verzahnt** — nach jedem Stoffabschnitt ein Quiz
   (W3Schools-Muster: rund vier Fragen am Ende eines Abschnitts). Wie viele
   Quizze und Fragen nötig sind, entscheidet das LM-Urteil; Maßstab ist, dass
   der behandelte Stoff **vollständig** abgedeckt ist. Ein einzelnes Quiz mit
   einer Frage ist nie genug. Die **Fragetypen werden durchmischt** (Begriff,
   Code lesen, Interpretation, Übertragung), und die Schwierigkeit **steigt**
   über die Lesson (leicht → schwer); jedes Quiz trägt ein kleines Badge mit
   der Stufe. Antwortoptionen möglichst gleiche Wortzahl — keine
   Format-Hinweise.
   Markup (zentrales `assets/quiz.js`, das Badge, „Show", Infokugeln und
   Prüf-Button selbst injiziert):
   `<div class="quiz" data-titel="Quiz 1" data-stufe="leicht">` mit je Frage
   `<div class="frage" data-loesung="0,2">` — `data-loesung` ist die
   **Lösungsmenge** als Indexliste; **0 bis 4 Optionen** dürfen richtig sein
   (Extremfälle ausdrücklich erlaubt, wie in den Wissensüberprüfungen). Jede
   Frage hat **vier Optionen als Checkboxen** (keine Radios —
   Mehrfach-richtig braucht Mehrfachauswahl) mit eindeutigem `name`, und
   **jede Option trägt eine eigene Begründung** in `data-grund`:
   die richtige, *warum* sie stimmt, jede falsche, *warum* sie falsch ist;
   jede Begründung ist durch den Lesson-Text gedeckt. **Ein
   „Überprüfen"-Button je Quiz** wertet alle Fragen auf einmal aus (keine
   Sofort-Auswertung beim Anklicken): je Frage erscheint **richtig** (Auswahl
   = Lösungsmenge) oder **falsch**, die Kärtchen färben sich (weiches
   Neongrün/Neonrot, augenschonend), und **Infokugeln** neben den Fragen
   zeigen bei Hover/Tipp die Lösungsmenge samt Begründungen. Danach wird der
   Button zu **„Nochmal versuchen"** und setzt alle Kästchen zurück. **Kein
   Punktestand** — die Wahrheit zählt, nicht die Quote.
   **Show-Modal:** Das Quiz steht inline in der Lesson; ein „Show"-Button
   öffnet es bildschirmfüllend als Modal (Backdrop-Blur, Kreuz oben rechts
   zum Zurückschließen) — der Beamer-/Klassenmodus. Beides ist dasselbe DOM.
   **Kein CDN, kein Framework** (kein Alpine/Reveal): Vanilla-JS im zentralen
   `assets/quiz.js`, CSS in `assets/lesson.css`.
7. **Übungsbeispiele:** Jede Lesson erzeugt **drei abzugebende Beispiele** in
   `Übungsbeispiele.md` (im Lesson-Ordner), gegliedert als `Beispiel 1:` bis
   `Beispiel 3:`. Jedes Beispiel ist eine **Matura-/Testaufgaben-artige
   Aufgabe mit mindestens zwei Teilaufgaben** — eine einzelne Frage ist nie
   genug. Die drei Beispiele decken unterschiedliche Zwecke ab: Kernübung zum
   Stoff, Selbsttest im WÜ-Format (vier Optionen, 0–4 richtig, Musterlösung)
   und Transfer auf neue Daten bzw. eine neue Situation; die Lehrperson weist
   daraus zu („als Hausübung: Beispiel 2"). Die Lesson endet mit einem
   Abschnitt **„Übungsbeispiele"**, der die drei Beispiele anreißt und auf die
   Datei verweist; Abgabehinweis in neutraler Form („Abgabe nach Vorgabe
   deiner Lehrperson"). Der Begriff „Hausübung" kommt in keiner Schülerdatei
   vor — die Beispiele **sind** die Mitarbeit.
8. **Beamer-Check & Code-Stil (Lektion = Präsentation):** Die `lesson.html`
   ist zugleich die Präsentation — projizierbare Grundschrift/Kontraste, ein
   Gedanke pro bildschirmgroßem Block, keine dunklen Code-Boxen; Code
   ausreichend groß und umbruchfreundlich (siehe Grundregel 6).
   Projekt-Konvention (z. B. `<-`, Snake_case,
   natives Pipe); Output als Kommentar, Erklärung als Kommentar; Zeilen kurz
   halten.
9. **Beispielprojekt-Verweis (nur wenn nötig):** Braucht die Lesson ein
   lauffähiges Projekt, liegt dieses in der **Beispielprojekt-Ablage des Repos**
   (§ Beispielprojekte). Die Lesson **verlinkt** es relativ und dupliziert
   keinen Projektcode.
10. **Navigator-Eintrag (Lernplattform):** Die fertige Lesson im Root-
    `index.html` verlinken — Titel + Ein-Zeiler unter dem passenden
    Jahrgangs-/KM-Block. Nur `unterricht/`-Ziele, keine Kohorten-/Lehrplan-
    Links (siehe § Lernplattform).

## Prepared Lessons (Ablage & Lebenszyklus)

**Prepared Lesson** (undatiert, vorbereitet, **kohortenagnostisch**) liegt
**flach** in `unterricht/<PREFIX>-<NN>-<slug>/` (`KM<#>` = Kompetenzmodul,
`SA` = schulautonom; `<NN>` läuft pro KM) zusammen mit
`lesson.html` + `Übungsbeispiele.md` — **ausschließlich
Unterrichtsmaterial, kein lauffähiger Projektcode** (§ Beispielprojekte). Die
`lesson.html` ist **zugleich die Präsentation** (Lektion und Präsentation in
einem, Grundregel 6). Eine Tages-README-Vorlage wird **nicht** erzeugt — die
Lehrperson pflegt das Kohorten-README selbst (§ Kopierzeile).

**Übernahme in den Unterricht — ausschließlich manuell durch die Lehrperson:**

1. Die Lehrperson wählt die vorbereitete Lektion, die zur **Tagesdynamik**
   der Kohorte passt (nicht umgekehrt — die Lesson wartet, der Unterricht
   entscheidet).
2. Sie **kopiert** sie per Hand aus dem Unterrichtsordner in den
   **Kohortenordner** und **fügt das Datum manuell in den Ordnernamen** ein:
   `<klasse>/YYYY-MM-DD__thema/` mit `lesson.html` (das README pflegt sie
   selbst).
3. Der Skill schreibt **nie** direkt in Kohortenordner, liest keine
   Kohorten-Statistiken und führt keinen Lernfortschritt — die Lesson ist
   bis zur Übernahme kohortenfrei.

## Kopierzeile & Lehrplan-Details

Zwei Dinge reisen mit der Lesson, statt in einer Vorlage zu leben:

- **Kopierzeile für das Kohorten-README:** Der Abschlussbericht des Skills
  enthält die fertige Zeile zum Kopieren — relativer Pfad zur `lesson.html`
  plus Kurztitel, z. B.
  `[KM7-02 Chi-Quadrat-Test](unterricht/KM7-02-chi-quadrat-test/lesson.html)`.
  Die Lehrperson klebt sie ins Kohorten-README und ergänzt selbst, was
  aufgegeben wird („als Hausübung: Beispiel 2"). Kein weiteres Template.
- **Lehrplan-Details in der Lesson:** Am Lesson-Ende (vor dem Footer) steht ein
  zugeklappter `<details>`/`<summary>`-Block **„Lehrplan & Einordnung"** mit
  Lehrplan-Pfad, KM-Bezug (KM + Thema, ggf. UE) und Runtime. Diese Angaben
  gehören **nicht** in den HTML-Kopf.

## Verifikation (vor Abgabe, Pflicht)

1. Jeder Code-Block läuft wie abgedruckt (per Ausführung gegen die echten
   Daten prüfen; behauptete Zahlen = berechnete Zahlen).
2. Alle relativen Links auflösbar (Assets, Nachbar-Lessons, Übungsbeispiele,
   Semesterplan).
3. Kein CDN / keine externen Abhängigkeiten (läuft über den lokalen
   Live-Server `serve.sh`), außer verlinkter Lektüre.
4. Quiz **klickbar** prüfen: Checkboxen wählen → **Überprüfen** → je Frage
   richtig/falsch, Kärtchen färben sich, **Infokugeln** zeigen bei Hover/Tipp
   Lösungsmenge und Begründungen → **„Nochmal versuchen"** setzt zurück und
   wird wieder zum Überprüfen-Button; **„Show"** öffnet das bildschirmfüllende
   Modal, das Kreuz schließt es. **Jede Frage ist durch den Lesson-Text
   gedeckt** (kein nur genannter Begriff, kein Folge-UE-Stoff); **jede Option
   hat einen substanziellen, textgedeckten `data-grund`** (richtig wie
   falsch); `data-loesung` nennt die Lösungsmenge (0–4 Indizes); die
   Schwierigkeit steigt über die Lesson.
5. Übungsbeispiele: `Übungsbeispiele.md` mit `Beispiel 1:`–`Beispiel 3:`
   (je mindestens zwei Teilaufgaben) **und** Abschnitt „Übungsbeispiele" am
   Lesson-Ende **und** `<details>`-Block „Lehrplan & Einordnung" — Pflicht.
6. Light/Dark-Umschalter vorhanden und klickbar; Default folgt dem
   Betriebssystem, die Wahl überlebt den Reload, Print bleibt hell.
7. Bootstrap + Badge: generische Inline-Bootstrap im `<head>` vorhanden und
   `assets/loader.js` erreichbar; der Badge erscheint und zeigt auf die
   kanonische Pages-URL. Alles über den Live-Server (`serve.sh`), nie `file://`.
8. **Beamer (Lektion = Präsentation):** keine dunklen Code-Boxen; Code
   ausreichend groß und umbruchfreundlich; projizierbare Grundschrift, ein
   Gedanke pro bildschirmgroßem Block; die Lesson ist **ohne** separaten
   Foliensatz am Beamer vorführbar.
9. **Umfang:** die Lesson ist eine ganze Doppelstunde (90 min) — Pflicht.
10. **KM-Vollständigkeit:** alle im KM geforderten Wege/Konzepte kommen vor.
11. **Kein lauffähiger Code im Lesson-Ordner:**
    `unterricht/<PREFIX>-<NN>-<slug>/` enthält nur HTML/Markdown (+ zentrale
    `assets/`); Beispielprojekte liegen in der Beispielprojekt-Ablage
    (§ Beispielprojekte) und sind dort für sich lauffähig (Tests grün).
    Unter `unterricht/` liegen **ausschließlich** Lesson-Ordner — kein
    `reference/`, kein weiterer Hilfsordner (Grundregel 3).
12. **Lernplattform:** Die Lesson ist im Root-`index.html` verlinkt, der Link
    löst auf, und es gibt keine Verweise auf Kohorten-/Lehrplan-Ordner; der
    Pages-Workflow veröffentlicht nur `index.html`, `assets/` und `unterricht/`.
13. **Drei-Kontext-Lauffähigkeit:** Die Lesson läuft **lokal** (`./serve.sh`),
    im **VS-Code-Browser** (über die Server-URL, nicht `file://`) **und** unter
    der **Pages-Basis** (deployte URL nach dem Push bzw. lokal `/<repo>/…`
    simuliert) — Assets/Bootstrap, Badge, Quiz, Theme und Navigator-Link
    funktionieren in allen Kontexten; kein `<base>`, kein root-absoluter Pfad,
    kein `file://`. Das Quiz **klickbar** prüfen (Checkboxen wählen →
    Überprüfen → Färbung/Infokugeln → Nochmal versuchen; Show-Modal öffnen und
    schließen): Lokal kann das Timing den `DOMContentLoaded`-Fallstrick
    kaschieren, unter der Pages-Basis tritt er auf (siehe Bauablauf Schritt 4).

## Nachziehen (gleicher Commit)

- `Übungsbeispiele.md` (Beispiel 1–3) und der `<details>`-Block
  „Lehrplan & Einordnung" in der Lesson.
- Neue Lesson im Root-`index.html` verlinken (Lernplattform-Navigator) —
  Pflicht im selben Commit, nur `unterricht/`-Ziele.
- Neue Fachbegriffe ins **Root-`GLOSSAR.md`** (mit KM-Verweis; UE-Verweis
  nur, wenn tatsächlich zugeordnet).
- Im Abschlussbericht: **Kopierzeile** (Pfad + Kurztitel) für das
  Kohorten-README.
- Commit-Message nach Repo-Konvention (mit Issue-Nummer, falls verlangt).

## Was dieser Skill NICHT tut

- Keine Semesterpläne entwerfen (lehrplan-Skill, Aufgabe 3).
- Keine Lessons unterhalb der KM-Anforderung oder ohne Bezug zu KM/Unterlagen
  erfinden.
- Keinen separaten Foliensatz anlegen. Die `lesson.html` **ist** die
  Präsentation (Lektion und Präsentation in einem, Grundregel 6). Die
  Übungsbeispiele gehören in die Lesson — ein separater
  Aufgaben-Master entsteht nur, wenn die Repo-Konvention einen verlangt.
- **Keine Kohorten-Verwaltung:** nicht in Kohortenordner schreiben, keine
  Lessons-Tabellen in Klassen-READMEs pflegen, keinen Lernfortschritt von
  Kohorten verfolgen. Lessons-Tabellen in Klassen-READMEs, Übernahme-Datum
  und Kohorten-Zuordnung führt ausschließlich die Lehrperson manuell.
- Keine lauffähigen Beispielprojekte unter `unterricht/` anlegen oder dorthing
  kopieren — sie gehören in die Beispielprojekt-Ablage des Repos
  (§ Beispielprojekte).
- Keine Selbstlern-Pfade (teach-Skill).
