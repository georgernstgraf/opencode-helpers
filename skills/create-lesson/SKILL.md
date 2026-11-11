---
name: create-lesson
description: "Richtet zu einem Kompetenzmodul (KM) oder einem Thema daraus eine
  kohortenagnostische Lesson her (self-contained HTML: Lektion und Präsentation
  in einem — Erklärung, Lernquizzes, drei Aufgaben, beamer-tauglich) und legt
  sie als Prepared Lesson in unterricht/<PREFIX>-<NN>-<slug>/ ab (und verlinkt
  sie im Lernplattform-Navigator index.html) — ohne lauffähigen Projektcode,
  Beispielprojekte liegen in der Beispielprojekt-Ablage des Repos. Eine
  Zuordnung zu einer geplanten Unterrichtseinheit im Semesterplan ist möglich,
  aber optional — die Lesson gehört zum Thema und KM, nicht zu einer Kohorte.
  Use when the user says 'Lektion bauen/erstellen', 'Unterrichtseinheit
  ausarbeiten', 'Wiederholungs-Lektion', 'eine Lektion für den Unterricht
  bauen', 'on demand eine Lektion einstreuen' oder eine Lesson-HTML für den
  Unterricht gebraucht wird. Do not use for Selbstlern-Pfade (teach),
  Semesterpläne (lehrplan) oder das Nachtragen von Aufgaben im Kohortenordner
  (homework)."
license: MIT
compatibility: opencode
---

# Create-Lesson-Skill

Richtet zu einem **Kompetenzmodul (KM) oder einem Thema daraus** eine
**Lesson** her: eine selbständige HTML-Seite für Schüler:innen mit Erklärung,
**Lernquizzes** über den Stoff verteilt und **drei abzugebenden
Aufgaben** am Lesson-Ende (die Beispiele = Mitarbeit). Der Skill
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
- **Keine Zuordnung, auch nicht im Bericht.** Der Skill ordnet eine Lesson
  **nie** einer Kohorte zu — nicht im Ordnernamen, nicht in Kopf oder Text,
  nicht im Abschlussbericht und nicht in den Wissensdateien
  (`HANDOFF.md`, `STATE.md`, `HISTORY.md`). Formulierungen wie „noch keiner
  Kohorte zugeordnet“ machen aus einer bewussten Eigenschaft eine offene
  Aufgabe und sind zu vermeiden.

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
   `lesson.html` + `aufgabe.md` (siehe
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
der Aufgabe, nicht als eingebettete Projektdatei. Da die Beispielprojekt-Ablage
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

`KM/Teil-KM + Thema` — eine Ziel-UE oder Kohorte kann in der Bestellung
genannt werden, ist aber **optional**. Sie ist reine Kontextinformation für
die Lehrperson: Sie wird weder in die Lesson geschrieben noch als Zuordnung
dokumentiert — nicht im Abschlussbericht, nicht in `HANDOFF.md`/`STATE.md`.
Beispiele:

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
   Dazu Lektüre-Box mit Pflicht-Charakter am Anfang. In allen Schritten gilt
   die **Schülerperspektive** (§ Schülerperspektive).
6. **Lernquizzes (Format 2.1).** Quizze sind **Lernquizzes**, keine
   Punkteprüfung: Sie prüfen ausschließlich den *zuvor erklärten* Stoff und
   sind über die Lesson **verzahnt** — nach jedem Stoffabschnitt ein Quiz
   (W3Schools-Muster: rund vier Fragen am Ende eines Abschnitts). Wie viele
   Quizze und Fragen nötig sind, entscheidet das LM-Urteil; Maßstab ist, dass
   der behandelte Stoff **vollständig** abgedeckt ist. Ein einzelnes Quiz mit
   einer Frage ist nie genug. Die **Fragetypen werden durchmischt** (Begriff,
   Code lesen, Interpretation, Übertragung); die Progression (später im Stoff
   anspruchsvoller) bleibt eine unsichtbare Designregel. Antwortoptionen
   möglichst gleiche Wortzahl — keine Format-Hinweise. **Keine
   Schwierigkeitsstufen:** weder `data-stufe` noch „leicht/mittel/schwer"
   noch ★-Niveaus, weder im Markup noch in der Anzeige.
   Markup (zentrales `assets/quiz.js` injiziert Badge, Infokugeln und
   Prüf-Button):
   `<div class="quiz" data-titel="Quiz: <thema-slug>">` mit je Frage
   `<fieldset class="frage">`; die Frage steht im
   `<legend class="frage-text">`, die Optionen in `<div class="optionen">`.
   Die **Lösungsmenge steht an den Optionen selbst**: jede richtige Option
   trägt `data-richtig` am Input (Attribut vorhanden = richtig); **0 bis 4
   Optionen** dürfen richtig sein (Extremfälle ausdrücklich erlaubt, wie in
   den Wissensüberprüfungen) — bei 0-richtig trägt **keine** Option das
   Attribut. **Kein `data-loesung`, keine Positions- oder
   Buchstabenkodierung:** `quiz.js` mischt die Optionen beim Laden
   (Fisher-Yates), die Markup-Reihenfolge ist bedeutungslos — deshalb gibt
   es auch keine Rotationsprüfung mehr. Jede Frage hat **vier Optionen als
   Checkboxen** (keine Radios — Mehrfach-richtig braucht Mehrfachauswahl)
   mit lesson-präfixiertem, eindeutigem `name`, und
   **jede Option trägt eine eigene Begründung** in `data-grund`: die
   richtige, *warum* sie stimmt, jede falsche, *warum* sie falsch ist; jede
   Begründung ist durch den Lesson-Text gedeckt. **Ein
   „Überprüfen"-Button je Frage** wertet alle Optionen dieser Frage auf
   einmal aus (keine Sofort-Auswertung beim Anklicken): jede Option färbt
   sich danach, ob ihr Häkchen richtig gesetzt war (weiches
   Neongrün/Neonrot, augenschonend), und **eine Infokugel je Option** zeigt
   bei Hover/Fokus/Tipp genau diese Option samt ihrer Begründung; die Kugeln
   bleiben bis zum ersten Prüfen verborgen. Danach wird der Button zu
   **„Nochmal versuchen"** und setzt die Frage zurück. Eine versteckte
   `aria-live`-Statuszeile meldet das Ergebnis für Screenreader. **Kein
   Punktestand** — die Wahrheit zählt, nicht die Quote.
   **Kein Show-Modal** und kein Vollbild-Modus: Das Quiz steht inline in der
   Lesson und wird dort projiziert. **Kein CDN, kein Framework** (kein
   Alpine/Reveal): Vanilla-JS im zentralen `assets/quiz.js`, CSS in
   `assets/lesson.css`.
7. **Aufgabe:** Jede Lesson erzeugt **drei abzugebende Beispiele** in
   `aufgabe.md` (im Lesson-Ordner), gegliedert als `Beispiel 1:` bis
   `Beispiel 3:`. Jedes Beispiel ist eine **Matura-/Testaufgaben-artige
   Aufgabe mit mindestens zwei Teilaufgaben** — eine einzelne Frage ist nie
   genug. Die drei Beispiele decken unterschiedliche Zwecke ab: Kernübung zum
   Stoff, Selbsttest im WÜ-Format (vier Optionen, 0–4 richtig, Musterlösung)
   und Transfer auf neue Daten bzw. eine neue Situation; die Lehrperson weist
   daraus zu („als Hausübung: Beispiel 2"). Die Lesson endet mit einem
   Abschnitt **„Aufgabe"**, der die drei Beispiele anreißt und auf die Datei
   verweist; Abgabehinweis in neutraler Form („Abgabe nach Vorgabe deiner
   Lehrperson"). Der Begriff „Hausübung" kommt in keiner Schülerdatei vor —
   die Beispiele **sind** die Mitarbeit.
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

## Schülerperspektive (Erklärungsempathie)

Eine Lesson liest jemand, der den Stoff zum ersten Mal sieht. Beim Bauen und
Nachziehen immer aus dieser Perspektive prüfen:

- **Sparsam mit Abkürzungen und Fachjargon.** Symbole wie `df`, `p`, H₀, χ²,
  `NA`, Spaltenkürzel — beim ersten Auftreten einführen, dann wiederverwenden;
  die Langform bevorzugen, wenn der Kontext sie nicht trägt.
- **Nichts Unerklärtes in den Text werfen.** Jede Zahl, jedes Symbol, jeder
  Begriff, den der Schüler nachvollziehen soll, muss herleitbar sein:
  Rechenschritte, wo der Zwischenschritt nicht trivial ist; Werte nicht vom
  Himmel fallen lassen; eine Eigenschaft, die später Konsequenzen hat
  (z. B. eine Formeleigenschaft, aus der eine R-Warning folgt), nicht
  unverbunden stehen lassen.
- **Warnings und überraschender Output werden erklärt** — nicht als
  isolierter „Was tun"-Absatz, sondern als Konsequenz von etwas, das die
  Lesson bereits eingeführt hat.
- **Empathie vor Knappheit.** Der Skill neigt dazu, Dinge kurz und wenig
  erklärt hinzuschreiben. Korrekturrichtung: lieber ein Zwischenschritt
  mehr als einer zu wenig — der Leser darf nirgends abgehängt werden.

Beispielhaft (aus einer χ²-Überarbeitung): Beitrags-Tabelle statt nur
Gesamtsumme, Frei/Fest-Gitter statt nur df-Formel, Kontrollsumme der
Randsummen nach der Umrechnung.

## Fragenqualität (jedes Quiz-Item)

Eine Frage ist erst fertig, wenn sie vier Prüfungen besteht:

- **Nur mit dem Stoff lösbar** — nicht mit Allgemeinwissen, nicht mit
  Testtaktik („längste Option", „immer/nie", Ausschlussverfahren).
- **Jede Option hat einen Verteidigungsgrund** — die richtige, *warum* sie
  aus dem Text folgt; jede falsche, *welche Fehlvorstellung* sie bedient.
  Distraktoren stammen aus den „typischen Fehlern", aus `PITFALLS.md` und
  aus realen Verwechslungen — nie aus Fantasie.
- **Die Lösungsmenge ist nicht verhandelbar** — keine Option, über die man
  mit gutem Argument streiten könnte; Mehrfachlösungen sind unabhängig
  voneinander wahr/falsch, nicht „teilweise richtig".
- **Diskrimination statt Abruf** — mindestens ein Item je Block hält zwei
  ähnliche Begriffe auseinander (z. B. Fehler 1./2. Art, `sd` vs.
  Standardfehler, IQR-Zaun vs. Toleranzgrenze); mindestens eines ist
  Transfer auf neue Zahlen oder eine neue Situation; wo Code der Stoff ist,
  wird Code gelesen (Ausgabe vorhersagen, Fehler diagnostizieren), nicht
  Syntax abgefragt.

**Abdeckungsmatrix:** Vor dem Schreiben je Lesson eine Zeile pro
`<h2>`-Sektion und pro KM-Punkt anlegen („Sektion → Items"). Abnahme: jede
Sektion mindestens ein Item, jeder KM-Punkt mindestens eines, jede
„typischer Fehler"-Zeile mindestens ein Distraktor. Die Kurzfassung
(Sektionen × Items, KM-Punkte) gehört in die Commit-Message.

**Blindprobe und Gegenlesung:** Die Fragen nur mit dem Lesson-Text lösen —
wo man stockt, ist der Text oder die Frage defekt. Danach ein unabhängiger
Durchgang mit frischem Kontext (Subagent), der nur Lesson und Fragen sieht
und Mehrdeutigkeiten, ungedeckte Optionen, verräterische Wortlängen sowie
ohne den Abschnitt lösbare Fragen sucht.

**Zahlen und Positionen:** Jede behauptete Zahl und jede R-Ausgabe wird per
Ausführung gegen die echten Daten geprüft; Grenzfälle (Toleranzgrenze,
n/N = 5 %) werden wirklich durchgerechnet. Antwortpositionen rotieren,
Lösungsmengen variieren über die Lesson (0/1/2/3/4 richtig), ohne dass ein
Muster erkennbar wird.

## Markup & Lesbarkeit

- **Seitengerüst:** `lang="de"`, ein `h1`, `h2` → `h3` ohne Sprünge; das
  Quiz-Badge wird als `h3` injiziert und erscheint damit in der
  Dokumentgliederung.
- **Quiz-Vertrag** (siehe Bauablauf Schritt 6): `fieldset.frage` +
  `legend.frage-text`, `div.optionen` mit vier Checkbox-Labels,
  `data-grund` je Option, `name` lesson-präfixiert, `data-richtig` an
  jeder richtigen Option (kein `data-loesung`; Reihenfolge egal —
  `quiz.js` mischt).
- **Keine Inline-Styles**, keine Kohorten-, UE- oder Semesterangaben im
  Header oder Text (nur Provenienz wie „Wiederholung aus KM5"); Lehrplan
  ausschließlich im `<details>`-Block am Ende.
- **Prosa:** ein Gedanke pro bildschirmgroßem Block; Absätze 2–4 Sätze;
  Sätze im Schnitt höchstens ~18 Wörter, keiner über ~28; Aktiv und direkte
  Anrede; jeder Abschnitt beantwortet „warum", nennt die Grenze und ein
  Gegenbeispiel. Fachbegriffe bei Erstverwendung erklären, danach dieselbe
  Bezeichnung wie im `GLOSSAR.md`.
- **Callouts** einheitlich: `Lektüre`, `Merke`, `Achtung`, `Antwort auf die
  Einstiegsfrage` — höchstens einer pro Bildschirm.
- **Code:** heller Grund, dunkle Schrift; der Kommentar erklärt *warum* und
  nennt die Ausgabe; Zeilen höchstens ~80 Zeichen; deutsch.
- **Beamer & Print:** projizierbare Grundschrift und Kontraste, keine
  dunklen Code-Boxen, `break-inside: avoid` für Quiz und Code,
  Bedienelemente im Druck aus.

## Prepared Lessons (Ablage & Lebenszyklus)

**Prepared Lesson** (undatiert, vorbereitet, **kohortenagnostisch**) liegt
**flach** in `unterricht/<PREFIX>-<NN>-<slug>/` (`KM<#>` = Kompetenzmodul,
`SA` = schulautonom; `<NN>` läuft pro KM) zusammen mit
`lesson.html` + `aufgabe.md` — **ausschließlich
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
  Die Kopierzeile ist ein **Angebot an die Lehrperson**: Der Skill trägt sie
  nirgends ein und wertet sie nicht als Zuordnung. Die Lehrperson klebt sie ins
  Kohorten-README und ergänzt selbst, was aufgegeben wird („als Hausübung:
  Beispiel 2"). Kein weiteres Template.
- **Lehrplan-Details in der Lesson:** Am Lesson-Ende (vor dem Footer) steht ein
  zugeklappter `<details>`/`<summary>`-Block **„Lehrplan & Einordnung"** mit
  Lehrplan-Pfad, KM-Bezug (KM + Thema, ggf. UE) und Runtime. Diese Angaben
  gehören **nicht** in den HTML-Kopf.

## Verifikation (vor Abgabe, Pflicht)

1. Jeder Code-Block läuft wie abgedruckt (per Ausführung gegen die echten
   Daten prüfen; behauptete Zahlen = berechnete Zahlen).
2. Alle relativen Links auflösbar (Assets, Nachbar-Lessons, Aufgabe,
   Semesterplan).
3. Kein CDN / keine externen Abhängigkeiten (läuft über den lokalen
   Live-Server `serve.sh`), außer verlinkter Lektüre.
4. Quiz **klickbar** prüfen: Checkboxen wählen → **Überprüfen** → jede
   Option färbt sich nach ihrer Entscheidung, **Infokugeln** zeigen bei
   Hover/Fokus/Tipp genau diese Option samt Begründung → **„Nochmal
   versuchen"** setzt zurück und wird wieder zum Überprüfen-Button. **Jede
   Frage ist durch den Lesson-Text gedeckt** (kein nur genannter Begriff,
   kein Folge-UE-Stoff); **jede Option hat einen substanziellen,
   textgedeckten `data-grund`** (richtig wie falsch); `data-richtig` steht
   an jeder richtigen Option (0–4, bei 0 keine), **kein `data-loesung`**;
   die Optionsreihenfolge ändert sich bei Reload (Shuffle), Farbe und
   Infokugel müssen der richtigen Option folgen. Keine Stufen- oder
   Modal-Reste.
5. Aufgabe: `aufgabe.md` mit `Beispiel 1:`–`Beispiel 3:`
   (je mindestens zwei Teilaufgaben) **und** Abschnitt „Aufgabe" am
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
    Überprüfen → Färbung/Infokugeln → Nochmal versuchen): Lokal kann das
    Timing den `DOMContentLoaded`-Fallstrick kaschieren, unter der
    Pages-Basis tritt er auf (siehe Bauablauf Schritt 4).
14. **Markup und Prosa:** Seitengerüst und Quiz-Vertrag (§ Markup &
    Lesbarkeit) eingehalten; kein `radio`, kein `data-stufe`, kein
    `niveau`, kein Show-Element, keine Inline-Styles, keine
    Kohorten-/UE-Angaben im Kopf; Sätz- und Absatzlängen im Rahmen;
    Kopfzeile der Quizze zeigt `Quiz: <thema-slug>`.

## Nachziehen (gleicher Commit)

- `aufgabe.md` (Beispiel 1–3) und der `<details>`-Block
  „Lehrplan & Einordnung" in der Lesson.
- Neue Lesson im Root-`index.html` verlinken (Lernplattform-Navigator) —
  Pflicht im selben Commit, nur `unterricht/`-Ziele.
- Neue Fachbegriffe ins **Root-`GLOSSAR.md`** (mit KM-Verweis; UE-Verweis
  nur, wenn tatsächlich zugeordnet).
- Im Abschlussbericht: **Kopierzeile** (Pfad + Kurztitel) für das
  Kohorten-README.
- Commit-Message nach Repo-Konvention (mit Issue-Nummer, falls verlangt).

## Done when

- [ ] `unterricht/<PREFIX>-<NN>-<slug>/` enthält `lesson.html` und
      `aufgabe.md` — sonst nichts (kein lauffähiger Projektcode, kein
      Hilfsordner, kein separates `praesentation.html`).
- [ ] Die Verifikationsliste (14 Punkte) ist durchgegangen: jeder Code-Block
      läuft wie abgedruckt, alle relativen Links lösen auf, kein CDN.
- [ ] Die Lesson trägt eine Doppelstunde: Stoff für ~90 min, Quizze nach jedem
      Stoffabschnitt, Beamer-Check bestanden (keine dunklen Code-Boxen, ein
      Gedanke pro Block).
- [ ] `aufgabe.md` enthält `Beispiel 1:`–`Beispiel 3:` mit je mindestens zwei
      Teilaufgaben; die Lesson endet mit dem Abschnitt „Aufgabe" und dem
      `<details>`-Block „Lehrplan & Einordnung".
- [ ] Das Quiz ist **klickbar** geprüft (Überprüfen → Färbung + Infokugeln →
      „Nochmal versuchen") und läuft lokal, im VS-Code-Browser und unter der
      Pages-Basis.
- [ ] Die Lesson ist im Root-`index.html` verlinkt (Titel + Ein-Zeiler) und
      neue Fachbegriffe stehen im Root-`GLOSSAR.md`.
- [ ] Der Abschlussbericht enthält die Kopierzeile für das Kohorten-README —
      und nirgends (Lesson, Bericht, `HANDOFF.md`/`STATE.md`) eine
      Kohorten- oder UE-Zuordnung.
- [ ] Lesson, `index.html`-Eintrag und Glossar-Ergänzung liegen im selben
      Commit.

## Was dieser Skill NICHT tut

- Keine Semesterpläne entwerfen (lehrplan-Skill, Aufgabe 3).
- Keine Lessons unterhalb der KM-Anforderung oder ohne Bezug zu KM/Unterlagen
  erfinden.
- Keinen separaten Foliensatz anlegen. Die `lesson.html` **ist** die
  Präsentation (Lektion und Präsentation in einem, Grundregel 6). Die
  Aufgaben gehören in die Lesson — ein separater Aufgaben-Master entsteht
  nur, wenn die Repo-Konvention einen verlangt.
- **Keine Kohorten-Verwaltung:** nicht in Kohortenordner schreiben, keine
  Lessons-Tabellen in Klassen-READMEs pflegen, keinen Lernfortschritt von
  Kohorten verfolgen. Lessons-Tabellen in Klassen-READMEs, Übernahme-Datum
  und Kohorten-Zuordnung führt ausschließlich die Lehrperson manuell.
- Keine lauffähigen Beispielprojekte unter `unterricht/` anlegen oder dorthing
  kopieren — sie gehören in die Beispielprojekt-Ablage des Repos
  (§ Beispielprojekte).
- Keine Selbstlern-Pfade (teach-Skill).
