---
name: lehrplan
description: "Richtet österreichische HTL-Unterrichts-Repositorien ein und pflegt sie — drei Kernaufgaben: das gesetzliche Lehrplan-Material eines Ausbildungszweigs (z. B. WII, WIT, KIF) aus dem RIS beschaffen inklusive jährlichem Novellen-Check, den Lehrplan eines konkreten Gegenstands aus dem Gesetz extrahieren (mit Erläuterung pro Lernziel: was der Inhalt tatsächlich IST, plus praktische Anwendungen), und Semesterpläne interaktiv entwerfen. Aufrufen, wenn der Nutzer 'Lehrplan', 'Unterrichtsvorbereitung prüfen', 'Lehrplan auf Novellen prüfen', 'RIS sync', 'Lehrplan extrahieren', 'Jahrespläne neu ziehen', 'Semesterplan erstellen/überarbeiten', 'Erläuterungen ergänzen', 'Gesetzesmaterial holen' sagt oder in einem Repo arbeitet, das der lehrplan/-Konvention folgt."
license: MIT
compatibility: opencode
metadata:
  category: education
  scope: ris-curriculum
  output: lehrplan-extracts
---

# Lehrplan-Skill

Reverse-engineered aus dem GRG-PMM-Unterrichtsrepo (HTL Spengergasse).
Dieser Skill ist **konventionsbasiert, nicht auf ein Projekt verdrahtet**:
Er funktioniert in jedem Unterrichtsrepo, das der unten beschriebenen
`lehrplan/`-Konvention folgt.

Der Skill hat drei Kernaufgaben plus ein identifizierendes Präludium:

| Aufgabe | Zweck |
|---------|-------|
| **A** — Gegenstand & Ausbildungszweig identifizieren | Immer aktives Präludium: Repo lesen, Rechtsgrundlage berichten, Konformität prüfen |
| **1** — Gesetzesmaterial beschaffen | Gesetzlichen Lehrplan eines Ausbildungszweigs aus dem RIS holen, Novellen-Check |
| **2** — Fach-Extraktion | Lehrplan eines Gegenstands aus dem Gesetz extrahieren, mit Erläuterungen |
| **3** — Semesterplan | Interaktiv einen Semesterplan (Lehrstoffverteilung) aus den extrahierten Lehrplänen entwerfen |

Die Signatur-Erweiterung dieses Skills ist die **Erläuterungs-Ebene**: Für
jedes Lernziel (und besonders in den Lehrstoffverteilungen) eine
substantielle deutsche Erläuterung, was das Thema inhaltlich **ist** —
Begriffserklärung zuerst, integrierter Anwendungs- und Berufsbezug
zweitens. Siehe „Qualitätskriterien für Erläuterungen" unten.

## Ausgabesprache: DEUTSCH ZWINGEND

Alle erzeugten Dateien (Extrakte, METADATA.md-Abschnitte, Lehrstoff­
verteilungen, Berichte) MÜSSEN in natürlichem Deutsch mit korrekten
UTF-8-Umlauten (ä, ö, ü, ß) geschrieben sein. Niemals Englisch für
Dateiinhalte verwenden. Gesetzeszitate sind wortwörtlich aus dem
RIS-Inhalt zu übernehmen.

## Ziel-Repositorien

Dieser Skill ist für folgende Repositorien konzipiert (Stand 2026-09-10):

**Fach-Repos** (je ein Gegenstand, unter `~/repos/georgernstgraf/`):

`GRG-CS`, `GRG-CYBER`, `GRG-ETH`, `GRG-INFI`, `GRG-JAVA`, `GRG-NVS`,
`GRG-PMM`, `GRG-POSTHEORIE`, `GRG-SWP`, `GRG-WMC`

**Fachgruppen-Repos** (mehrere Gegenstände/Zweige):

- `~/repos/Die-Spengergasse/WI-Fachgruppe-Informatik`
- `~/repos/hoa-spg/pos-wmc-fachgruppe-inf-erw`

Wichtige Regeln dazu:

- **Fach-Repos können mehrere Zweige bedienen.** Ein Gegenstand kann in
  verschiedenen Ausbildungszweigen unterrichtet werden, in unterschiedlicher
  Tiefe — Beispiel GRG-INFI: Informatik im Zweig HWII (Anlage 1.24) und im
  Zweig HWIT (Anlage 1.28). Deshalb bildet die Verzeichnisstruktur **immer
  den Zweig mit ab**, auch in Fach-Repos (siehe Repo-Konventionen).
- **Der Skill wurde bei weitem nicht in allen Ziel-Repos ausgeführt, und
  das ist auch nicht vorgesehen.** Ein Repo ohne `lehrplan/`-Struktur ist
  daher **kein Fehler, sondern ein Zustand**: Aufgabe A berichtet den
  Zustand und listet, welche Aufgaben 1/2/3 noch ausstehen — und unternimmt
  **nichts** davon ohne ausdrückliche Nutzer-Anweisung. Kein
  Auto-Scaffolding, keine Auto-Migration, kein Nörgeln.

## Abgrenzung zum Unterricht (thematischer Schnitt)

Die Welt ist zweigeteilt in zwei Ebenen mit eigenen Wurzeln im Repo-Root:

| Ebene | Wurzel | Inhalt | Zuständig |
|-------|--------|--------|-----------|
| **Lehrplan-Ebene** (Gesetz + Planung) | `lehrplan/` | Gesetzesmaterial, Extrakte, METADATA, KM-Steckbriefe | **dieser Skill** |
| **Unterrichtsebene** (Vorbereitung + Durchführung) | `unterricht/` | Lehrstoffverteilungen, Semesterpläne, Stunden-Ordner | **Unterricht-Skill (noch zu erstellen)** |

Der `/unterricht/`-Ordner am Repo-Root ist **flach** aufgebaut — ein
Ordner pro Zweig-Fach-Kombination, darin die Dateien direkt, **ohne**
Jahrgangs-Unterordner und **ohne** Klassen-Unterordner:

```
unterricht/
  <ZWEIG>-<FACH>/                 # GROSSBUCHSTABEN, z. B. HWII-INFI, WIT-INFI
    jg2-einheiten.md              # Lehrstoffverteilung ("Einheiten") Jahrgang 2
    jg3-einheiten.md
    jg4-einheiten.md
    jg4-semesterplan-ws.md        # Semesterplan Wintersemester
    jg4-semesterplan-ss.md        # Semesterplan Sommersemester
    NN-slug/                      # Stunden-Ordner während der Vorbereitung
    YYYY-MM-DD_thema/             # Stunden-Ordner, sobald der Termin fixiert ist
```

- Das `<ZWEIG>`-Kürzel folgt der Klassen-Postfix-Tabelle (siehe
  Klassen-Zuordnung): `HWII`, `HWIT`, `AIF`, `KIF`, `CIF` usw.
- Klein geschriebenes `jg<N>`-Präfix für alle Einheiten- und
  Semesterplan-Dateien — **einheitliches Schema, keine Ausnahmen**.
- Das detaillierte Unterrichts-Layout (Stunden-Ordner-Inhalte, Materialien,
  Hausübungen) gehört zum **zukünftigen Unterricht-Skill**; dieser Skill
  legt hier nur die Lehrstoffverteilungen und Semesterpläne ab (Aufgabe 3)
  und meldet Altbestände als Befund (siehe Retrofit-Klausel).

## Repo-Konventionen

> **⛔ VERBINDLICHES ZIEL-LAYOUT — NICHT NUR EMPFEHLENSAM.**
> Das unten gezeigte Layout ist der **verbindliche Zielzustand** jedes
> Unterrichts-Repos. Wann immer eine Session auf ein Repo trifft, das
> davon abweicht (z. B. Lehrplan-Dateien unter `docs/lehrplan/`,
> Klassenordner oder `kompetenzmodule/` im `lehrplan/`-Root ohne
> Zweig-Ebene, `jgN-einheiten.md`-Sammeldateien unter `lehrplan/`,
> Semesterpläne oder Stunden-Ordner unter `lehrplan/`), gilt: **melden als
> Befund mit Migrationspflicht; Migration selbst nur auf ausdrücklichen
> Nutzer-Wunsch.** Nur eine explizite, dokumentierte Nutzer-Entscheidung
> (DECISIONS-Eintrag) kann eine Ausnahme rechtfertigen. **Einzige erlaubte
> Abweichung** bleibt das dreischichtige `LEHRPLAN.md` als *Dateiformat*
> (② Schuladaption und ③ Didaktik mitlegen) — die **Ablage** unter
> `lehrplan/<fach>-<zweig>/` ist davon nicht berührt und bleibt Pflicht.

### Fach-Repo (z. B. GRG-INFI)

```
lehrplan/
  METADATA.md                    # deckt ALLE Zweige des Fachs ab: Rechtsgrundlage,
                                 #   RIS-Verweise + NOR-Kopf-Belege, Änderungshistorie,
                                 #   Klassen-Zuordnung, Datei-Inventar
  RIS/                           # NUR Gesetzestext-PDFs (Rechtsinformationssystem)
    YYYY-MM-DD_<name>.pdf        # Anlagen/Novellen, ISO-Datum (Kundmachungsdatum)
  <fach>-<zweig>/                # pro Zweig ein Ordner, klein: infi-hwii, infi-hwit
    LEHRPLAN.md                  # ① Komplett-Extrakt (oder dreischichtig ①②③) DIESES Zweigs
    RIS.md                       # Rechtsstand, Novellen-Historie, Schichten-Vergleich
    <FACH>_②.pdf                 # Schuladaption-PDF, falls vorhanden
    kompetenzmodule/             # km<N>.md + README-Matrix — pro Zweig, weil die
                                 #   KM-Nummerierung (KM3–KM9) zwischen Zweigen kollidiert
    <KLASSE>/                    # GROSSBUCHSTABEN, z. B. 4HWII
      <KLASSE>.lehrplan.md       # Klassen-relevanter Extrakt (jahrgangsweise)
unterricht/                      # siehe "Abgrenzung zum Unterricht"
  <ZWEIG>-<FACH>/                # z. B. HWII-INFI
    jg<N>-einheiten.md
    jg<N>-semesterplan-ws.md
    jg<N>-semesterplan-ss.md
    NN-slug/                     # Stunden-Ordner (Vorbereitung)
    YYYY-MM-DD_thema/            # Stunden-Ordner (Termin fixiert)
AGENTS.md                        # Repo-weite Agent-Regeln
GLOSSAR.md                       # Domänen-Abkürzungen und Begriffe
```

### Fachgruppen-Repo (z. B. WI-Fachgruppe-Informatik)

Identisches Muster, nur mit mehreren Fächern/Zweigen nebeneinander:

```
lehrplan/
  METADATA.md                    # deckt ALLE Anlagen/Fächer des Repos ab
  RIS/                           # Gesetzestext-PDFs (über alle Fächer geteilt)
  infi-hwii/                     # jedes Fach-Zweig-Verzeichnis in sich geschlossen
  infi-hwit/
  swp-hwii/
unterricht/
  HWII-INFI/
  HWIT-INFI/
  HWII-SWP/
AGENTS.md
GLOSSAR.md
```

- Jedes `<fach>-<zweig>`-Verzeichnis ist in sich geschlossen: LEHRPLAN,
  RIS, ②-PDF, KM-Steckbriefe und Klassen-Extrakte liegen beieinander;
  Querverweise bleiben flach.
- Die Planungs-Dateien (Einheiten, Semesterpläne) liegen **flach** als
  `jg<N>-einheiten.md` bzw. `jg<N>-semesterplan_{ws,ss}.md` unter
  `unterricht/<ZWEIG>-<FACH>/`; die Zuordnung Jahrgang ↔ KM ↔ generisches
  Klassen-Label steht in `lehrplan/METADATA.md`.

### Ordner- und Datei-Benennung

- `lehrplan/<fach>-<zweig>/`: **klein** geschrieben, Bindestrich
  (z. B. `infi-hwii`). Das Zweig-Kürzel folgt der Klassen-Postfix-Tabelle
  (`hwii`, `hwit`, `aif`, `kif`, `cif`). In Fachgruppen-Repos vorhandene
  Alt-Ordner mit ausgeschriebenem Zweig-Kürzel (z. B. `infi-wii`,
  `infi-wit`) sind ein Befund mit Umbenennungsempfehlung
  (`infi-wii` → `infi-hwii`) — Umbenennung nur auf Nutzer-Wunsch.
- `unterricht/<ZWEIG>-<FACH>/`: **GROSSBUCHSTABEN**, Bindestrich
  (z. B. `HWII-INFI`). Reihenfolge bewusst anders als bei `lehrplan/`
  (dort Fach-Zweig, hier Zweig-Fach) — beide Formen sind verbindlich.
- Klassenordner: `<Stufe><Postfix>` in **GROSSBUCHSTABEN** (z. B.
  `4HWII`, `4HWIT`), **innerhalb** des `<fach>-<zweig>`-Ordners.
  Generische Labels decken Parallellklassen ab (`4HWIT` deckt
  4AHWIT/4BHWIT ab).
- Stunden-Ordner: `NN-slug/` während der Vorbereitung, umbenannt zu
  `YYYY-MM-DD_slug/`, sobald der Unterrichtstermin fixiert ist —
  **ausschließlich** unter `unterricht/<ZWEIG>-<FACH>/`.
- Einheiten/Semesterpläne: `jg<N>-einheiten.md` und
  `jg<N>-semesterplan-{ws,ss}.md`, kleines `jg`, Unterstrich, flach unter
  `unterricht/<ZWEIG>-<FACH>/`.
- RIS-Ordner: `lehrplan/RIS/` — Großbuchstaben-Ausnahme (Abkürzung, wie
  Klassen-Labels); enthält **nur** RIS-Gesetzestext-PDFs.
- PDFs: `RIS/YYYY-MM-DD_<name>.pdf` (ISO-8601-Datumspräfix).
- Klein mit Bindestrichen für alle mehrteiligen Datei- und Ordnernamen.

## Klassen-Zuordnung (MANUELL GEPFLEGT)

Der Skill führt diese Gegenstand → Klassen-Postfix-Tabelle mit. **Nie
selbst erweitern oder ändern.** Nutzt ein Repo einen Gegenstand, der hier
fehlt, das dem Nutzer melden und einen Eintrag vorschlagen — aber der
Nutzer editiert diese Skill-Datei selbst.

| Gegenstand | Klassen-Postfix(e) |
|------------|--------------------|
| PMM        | HWIT               |
| INFI (Anlage 1.24) | HWII       |
| INFI (Anlage 1.28) | HWIT       |
| SWP (Anlage 1.24)  | HWII       |
| WMC        | AIF, KIF, CIF      |

So funktioniert die Zuordnung:

- Klassenordner sind `<Stufe><Postfix>` (z. B. `4HWII`, `5HWIT`; für WMC
  z. B. `4KIF`, `5KIF`) — jeweils **innerhalb** des
  `lehrplan/<fach>-<zweig>/`-Ordners.
- Die `Stufe` (Ziffer) kommt aus dem Jahrgang, in dem der Gegenstand laut
  Lehrplan unterrichtet wird (siehe METADATA.md / Fachgegenstände-Tabelle).
- **Klassenordner generisch erkennen:** Jedes Verzeichnis unter
  `lehrplan/<fach>-<zweig>/`, das `<Ziffer><bekannter-Postfix>`
  entspricht, ist ein Klassenordner. Keine hardcodierte Liste voller
  Klassennamen verwenden.
- Ein Gegenstand in mehreren Zweigen (z. B. INFI in HWII und HWIT)
  bedeutet: mehrere `<fach>-<zweig>`-Ordner, jeweils mit eigenen
  Klassenordnern — die Tiefe kann je Zweig verschieden sein.

## Spengergasse-Klassen-Decoder (Abendform, Berufstätige-Formen)

Verifiziertes Wissen zu den Klassenkürzeln der HTL Spengergasse
(Erwachsenenbildung, Stand 2026-09-06, Quelle: Schul-Website „Informatik –
Abendform" + Lehrer-Angabe):

**Code-Schema:** `<Semester><Form-Serie>IF` — die Ziffer ist das Semester,
**ungerade = WS, gerade = SS** (z. B. `3AIF` WS → `4AIF` SS; `5KIF` WS →
`6KIF` SS).

| Form-Serie | Form | Dauer | Einstieg | Abschluss |
|------------|------|-------|----------|-----------|
| `AIF` | Aufbaulehrgang | 7 Semester | ohne Reifeprüfung (Vorbereitungslehrgang, Fachschule, facheinschlägiger Lehrabschluss) | **Reife- und Diplomprüfung** (Diplom + Matura) |
| `KIF` | Kolleg | 6 Semester | Reifeprüfung / Berufsreifeprüfung / Studienberechtigungsprüfung → Matura bereits vorhanden | **Diplomprüfung** (nur Diplom) |
| `CIF` | zweite Kolleg-Variante | 6 Semester | Matura bereits vorhanden | Diplomprüfung (nur Diplom); **C = Zweig, dessen Unterricht erst ab 17:10 beginnt** |

- Praxiscodes der Kohorten tragen ein **Zug-Präfix** (A/B/C) auf dem
  Form-Code: `4AAIF` (Zug A, AIF), `4AKIF` (Zug A, KIF), `4BKIF` (Zug B,
  KIF), `4CAIF` (CIF).
- Ein Schuljahrgang kann mehrere Form-Serien parallel bedienen (z. B.
  Jahr 1 in `34AIF` + `34KIF` + `34CIF`); die Klassenordner sind dann
  **Block-Ordner** für semestrierte Berufstätigen-Formen:
  `<Sem3Sem4><Form>` (`34AIF`, `34KIF`, `34CIF`, `56KIF`) statt
  Stufen-Notation — die PMM-Stufen-Notation (`4HWIT`) bleibt für
  Tagesschul-Formen das Gegenmodell.
- WMC/Informatik-Sonderformen: Rechtsgrundlage BGBl. II Nr. 368/2022
  (Anlagen 1 + 1.9, Varianten I.3/I.4); Referenz-Raster Anlage 1.10
  (262/2015 idF 383/2021). **Achtung:** Das signierte 383/2021-PDF enthält
  nur den VO-Text — der Anlagen-Wortlaut steht im BgblAuth-**COO-HTML**
  (konsolidierte Einzel-Anlage, fetchbar).
- Erlaubte Konventions-Abweichung: ein **dreischichtiges `LEHRPLAN.md`**
  statt eines reinen ①-Extrakts, wenn ② Schuladaption und ③ Didaktik
  mitlegen.
- Schul-Websites schreiben pauschal „Abschluss: Diplomprüfung" — die
  Matura-Logik der Formen steht in der **Einstiegsvarianten-Tabelle**,
  nicht in der Abschlusszeile.

## Ausbildungszweig-Konzept

Aufgabe 1 arbeitet auf **Ausbildungszweig**-Ebene (z. B. WII, WIT, KIF),
nicht auf Gegenstands-Ebene. Die rechtliche Hierarchie:

```
Ausbildungszweig (z. B. WII, WIT, KIF)
  → Rechtsgrundlage: BGBl.-Verordnung mit Anlagen (z. B. BGBl. II Nr. 262/2015)
    → Anlage(n): das Gesetz publiziert die Unterrichtsfächer eines
      Ausbildungszweigs MEIST GEMEINSAM in EINEM Dokument (z. B. deckt
      Anlage 1.28 ALLE Gegenstände des Zweigs WIT ab)
    → Variiert: manche Zweige/Fächer haben eigene Anlagen (z. B. WMC:
      Anlage 1.9 aus BGBl. II Nr. 368/2022 statt der WIT-Sammelanlage)
      → einzelne Fächer (Abschnitte der Anlage)
```

Konsequenzen für den Skill:

- **Aufgabe 1 (Beschaffung)** zielt auf die Dokumente des Zweigs. Eine
  gemeinsame Anlage pro Zweig ist der Normalfall; eigene Anlagen werden
  erkannt und berichtet, wenn sie existieren. Die METADATA.md des Repos
  speichert, welche Anlage welchen Gegenstand deckt.
- **Aufgabe 2 (Extraktion)** extrahiert immer EINEN Gegenstand (einen
  Abschnitt) aus dem Zweig-Dokument — nie den ganzen Zweig. Bei einem
  Gegenstand in mehreren Zweigen (z. B. INFI) wird pro Zweig ein eigener
  Extrakt im jeweiligen `lehrplan/<fach>-<zweig>/`-Ordner angelegt.
- Die Fetch-Strategie bleibt anlagen-basiert (NOR-Dokument pro Anlage,
  siehe RIS-Praxiswissen) — ein Zweig-Dokument wird einmal gefetcht und
  dient allen seinen Gegenständen.

## Ablaufübersicht

| Aufgabe | Modus | Trigger-Beispiele |
|---------|-------|-------------------|
| A — Gegenstand & Ausbildungszweig identifizieren | Standard (bei jedem Aufruf) | „Unterricht", „Vorbereitung prüfen" |
| 1 — Gesetzesmaterial beschaffen (Zweig) | Bei Bedarf | „Lehrplan auf Novellen prüfen", „RIS sync", „Gesetzesmaterial holen" |
| 2 — Fach-Extraktion mit Erläuterungen | Bei Bedarf | „Lehrplan extrahieren", „Jahrespläne neu ziehen", „Erläuterungen ergänzen" |
| 3 — Lehrstoffverteilung/Semesterplan (interaktiv) | Bei Bedarf | „Semesterplan erstellen", „Semesterplan überarbeiten", „Einheiten erstellen" |

Vor Aufgabe 1, 2 oder 3: einen kurzen Plan anzeigen (was wird gefetcht,
verglichen, geschrieben) und dann fortfahren. Bei schreiblastigen
Schritten mit dem Nutzer bestätigen, wenn der Plan vom Auftrag abweicht.

## Aufgabe A — Gegenstand & Ausbildungszweig identifizieren

In dieser Reihenfolge lesen:

1. `lehrplan/METADATA.md` — Rechtsgrundlage (BGBl.-Nummer, Anlage),
   RIS-Verweise (ELI, konsolidierte Fassung, NOR-Links),
   Änderungshistorie, Schulautonomie-Notizen, Klassen-Zuordnung,
   Datei-Inventar.
2. `README.md`, `AGENTS.md`, `GLOSSAR.md` — Gegenstandsname, Konventionen,
   Domänenbegriffe.

Danach berichten:

- **Gegenstand**: Name und Abkürzung, **aus den eigenen Docs des Repos
  gelesen** (`METADATA.md`, `README.md`, `AGENTS.md`) — nie eine
  Auflösung erfinden. Beispiel: GRG-PMM nutzt „Prozessmanagement (PMM)"
  als Maturafach-Name (Anlage 1.28, Abschnitt 5).
- **Ausbildungszweig(e)**: welchem Zweig(en) der Gegenstand des Repos
  angehört (z. B. WIT für PMM; HWII **und** HWIT für GRG-INFI) und welche
  Anlage ihn deckt — gemeinsam mit anderen Gegenständen oder als eigene
  (siehe Ausbildungszweig-Konzept).
- **Rechtsgrundlage**: BGBl. II Nummer, Kundmachungsdatum, Anlage (z. B.
  Anlage 1.28 der BGBl. II Nr. 262/2015), plus den Allgemeinen Teil
  (Anlage 1), falls referenziert.
- **RIS-Verweise**: die in METADATA.md gespeicherten Links.
- **Klassen**: vorgefundene Klassenordner (pro `<fach>-<zweig>`), via
  Postfix-Tabelle auf Jahrgänge abgebildet.
- **Lücken**: falls `lehrplan/METADATA.md` fehlt oder unvollständig ist,
  die Standardstruktur vorschlagen (siehe unten), bevor irgendetwas
  erstellt wird — und nur auf ausdrücklichen Nutzer-Wunsch erstellen.

### Konformitäts-Check (immer als Teil von Aufgabe A)

Nach dem Lesen des Repos jeden Punkt prüfen und berichten — das beantwortet
die wiederkehrende Frage „ist alles eingerichtet, muss der Skill noch
laufen?":

| Prüfpunkt | Konform, wenn |
|-----------|---------------|
| METADATA.md vollständig | Alle Skeleton-Abschnitte vorhanden und gefüllt (Rechtsgrundlage, RIS-Verweise, Änderungshistorie, Klassen-Zuordnung, Datei-Inventar) |
| Zweig-Ebene vorhanden | Jeder unterrichtete Zweig hat ein `lehrplan/<fach>-<zweig>/`-Verzeichnis — flache Klassenordner direkt unter `lehrplan/` (Alt-Layout) sind ein Befund mit Migrationspflicht |
| Komplett-Extrakt | `lehrplan/<fach>-<zweig>/LEHRPLAN.md` existiert pro Zweig, deckt alle Jahrgänge des Gegenstands in diesem Zweig ab |
| Klassen-Extrakte | `lehrplan/<fach>-<zweig>/<KLASSE>/<KLASSE>.lehrplan.md` existiert für jeden Klassenordner |
| Klassen-Zuordnung | METADATA.md bildet jeden unterrichteten Jahrgang ↔ KM ↔ GROSSBUCHSTABEN-Klassenname (pro Zweig) ab |
| Novellen-Check-Datum | METADATA.md dokumentiert die letzte RIS-Abfrage („RIS-Status abgefragt am …") und ihr Ergebnis |
| RIS-Verzeichnis | Alle Gesetzestext-PDFs unter `lehrplan/RIS/` — PDFs im `lehrplan/`-Root sind ein Migrationsbefund |
| Erläuterungen | KM-Überblicke und Lernziel-Erläuterungen in allen Extrakten vorhanden (siehe Aufgabe 2) |
| Unterrichts-Ablage | Einheiten (`jg<N>-einheiten.md`) und Semesterpläne (`jg<N>-semesterplan-{ws,ss}.md`) liegen unter `unterricht/<ZWEIG>-<FACH>/` — Gleiches unter `lehrplan/` ist ein Migrationsbefund (Retrofit-Klausel) |
| Stunden-Ordner | `NN-slug/` und `YYYY-MM-DD_thema/` liegen unter `unterricht/<ZWEIG>-<FACH>/` — Gleiches unter `lehrplan/` ist ein Befund (zuständig: Unterricht-Skill) |

Anschließend ausdrücklich feststellen: **„Der Skill muss noch ausgeführt
werden"** (Auflistung, welche Aufgaben 1/2/3 ausstehen) **oder „Der Skill
ist vollständig ausgeführt"** — oder, bei Repos ohne `lehrplan/`-Struktur:
**„Repo noch nicht lehrplan-aktiviert; Aufgaben 1/2/3 stehen aus"** plus
Befundliste. In keinem Fall eigenmächtig migrieren, anlegen oder löschen.

### METADATA.md-Skeleton (nur vorschlagen, wenn fehlend/unvollständig)

```markdown
# Metadaten zum Lehrplan

## Rechtliche Grundlage
<!-- Kundmachungsorgan, Datum, Typ, Titel, einbringende Stelle, Anlage -->

## RIS-Verweise
<!-- ELI, konsolidierte Fassung (Gesetzesnummer), Anlage-Links -->

## Änderungshistorie
<!-- | Datum | Änderung | Betrifft | -->

## Schulautonomie
<!-- Freiheitsgrade, schulautonome Stundentafel -->

## Klassen-Zuordnung
<!-- | Zweig | Jahrgang | Klassenname | -->  <!-- GROSSBUCHSTABEN, generische Labels -->

## Zeitmodell
<!-- Wochenstunden/Doppelstunden pro Semester -->

## Dateien in diesem Verzeichnis
<!-- | Datei (RIS-PDFs als `RIS/<name>.pdf`) | Herkunft | Beschreibung | -->
```

## Aufgabe 1 (bei Bedarf) — Gesetzesmaterial beschaffen (Ausbildungszweig)

Zweck: sicherstellen, dass das Repo das geltende Gesetz für den
Ausbildungszweig des Gegenstands vollständig abbildet und keine
gesetzgeberische Änderung der **letzten 12 Monate** verpasst wurde.

Protokoll:

1. **Gespeicherten Zustand lesen** aus `lehrplan/METADATA.md`:
   Gesetzesnummer der konsolidierten Fassung, RIS-Links (insbesondere der
   Anlage-NOR-Link), Änderungshistorie-Tabelle, PDF-Inventar.
2. **Novellen-Check (letzte 12 Monate)** — mit der NOR-Kopf-Methode (siehe
   „RIS-Praxiswissen" unten; **nie** `webfetch` auf die
   `GeltendeFassung.wxe`-Seite — sie enthält das ganze Lehrplanpaket,
   überschreitet das Fetch-Limit und schlägt fehl):
   - `curl` auf das **NOR-Dokument der Anlage des Zweigs** (Link in
     METADATA.md). Sein Kundmachungsorgan-Kopf enthält die
     autoritative Ein-Zeilen-Prüfung, z. B.:
     „BGBl. II Nr. 262/2015 **zuletzt geändert durch** BGBl. II Nr. 250/2021"
   - Die „zuletzt geändert durch"-Novelle mit der Änderungshistorie-Tabelle
     in METADATA.md vergleichen. Abfragedatum notieren.
   - Ist die Novelle bereits dokumentiert: keine Änderung melden, mit
     Schritt 4 fortfahren.
3. **Bei einer dokumentierten-neueren Novelle (nur wenn neuer als der
   letzte dokumentierte Eintrag):**
   - **Identifizieren** über die **ELI-Seite**
     (`https://www.ris.bka.gv.at/eli/bgbl/II/<Jahr>/<Nr>`): Kurztitel,
     Kundmachungsdatum, Typ.
   - **Herunterladen** des signierten PDFs:
     `https://www.ris.bka.gv.at/Dokumente/BgblAuth/BGBLA_<Jahr>_II_<Nr>/BGBLA_<Jahr>_II_<Nr>.pdf`
   - **Auswirkungen analysieren**: `pdftotext`, dann nach `Anlage <N.N>`
     und Gegenstands-Schlüsselwörtern greppen. Novellen-§§ sind pro
     Novelle nummeriert; das Inkrafttreten-Muster ist typischerweise
     „Abschnitte I und VII … treten hinsichtlich des I. Jahrganges mit
     1. September <Jahr> … jahrgangsweise aufsteigend in Kraft".
   - **Zuerst den Nutzer informieren**: was sich ändert, welche Teile des
     Lehrplans des Zweigs betroffen sind, ob der Lehrstoff des Gegenstands
     (der Abschnitt des Gegenstands in der Anlage) berührt ist.
   - PDF speichern unter `lehrplan/RIS/` als
     `YYYY-MM-DD_BGBl-II-<Nr>_Novelle-<slug>.pdf` (Kundmachungsdatum).
   - METADATA.md aktualisieren: RIS-Verweise (Novellen-ELI-Link),
     Änderungshistorie (Zeile anhängen: Kundmachungsdatum, Novelle +
     Inkrafttreten, Betrifft), Datei-Inventar, plus die Belegzeile
     „RIS-Status abgefragt am …".
   - Aufgabe 2 (Re-Extraktion) als erforderlich markieren **nur, wenn der
     Abschnitt/Lehrstoff des Gegenstands geändert wurde** (z. B. berührte
     250/2021 nur Religion/Ethik — der Prozessmanagement-Abschnitt blieb
     unverändert, die Extrakte blieben gültig).
4. **PDFs vergleichen:** prüfen, ob die gespeicherten PDFs noch den
   aktuellen RIS-Originalen entsprechen (Daten/Dokument-IDs vergleichen;
   Byte-Vergleich, wenn ein frischer Download verfügbar ist).
5. **Bei keiner Änderung:** Bestätigung mit Beleg berichten — die
   gefetchte NOR-Kopf-Zeile (mit Abfragedatum) und das Datum des letzten
   Eintrags in METADATA.md. Ausdrücklich festhalten: „Alles Relevante aus
   dem Gesetz ist im Repository abgebildet."
6. **Bei Fetch-Fehler:** den exakten Fehler melden und stoppen — nie den
   Rechtsstand raten oder fabrizieren.

## Aufgabe 2 (bei Bedarf) — Fach-Extraktion mit Erläuterungen

Zweck: den Gesetzestext in lesbare Markdown-Schichten überführen — das
wortwörtliche Gesetz plus die Erläuterungs-Ebene (was der Inhalt
tatsächlich ist).

1. **Quelle**: Text aus der RIS-HTML der Anlage des Zweigs extrahieren
   (bevorzugt: aktueller konsolidierte-Fassung-Link in METADATA.md) oder
   aus dem gespeicherten PDF. Nur gefetchte Inhalte zitieren — nie
   Gesetzestext aus dem Gedächtnis rekonstruieren.
2. **Komplett-Extrakt** — `lehrplan/<fach>-<zweig>/LEHRPLAN.md`:
   - Alle Jahrgänge des Gegenstands in diesem Zweig, in Reihenfolge
     (I.–V. Jahrgang).
   - Struktur: `## <Jahrgang>` → `### <Semester> — Kompetenzmodul <N>`
     → `#### Bildungs- und Lehraufgabe` → `#### Lehrstoff`.
   - **Erläuterungs-Ebene (zwingend)**, siehe „Qualitätskriterien für
     Erläuterungen":
     - **KM-Überblick**: direkt unter jeder `### <Semester> —
       Kompetenzmodul <N>`-Überschrift eine kurze Einleitungs-Beschreibung
       als Annotation (`> **Überblick:** …`) — worum geht es in diesem
       Kompetenzmodul insgesamt.
     - **Lernziel-Erläuterungen**: direkt **unter jedem Lernziel-Bullet**
       der Bildungs- und Lehraufgabe eine Inline-Annotation
       (`> **Erläuterung:** …`), die erklärt, was das Thema IST.
     - **Lehrstoff-Erläuterungen**: eine Annotation
       (`> **Erläuterung:** …`) pro Lehrstoff-Bereich (Lehrstoff ist
       verdichteter Fließtext — eine Erläuterung pro Bereich, nicht pro
       Fragment).
   - Meilensteine annotieren (z. B. „III. Jahrgang — Statistik beginnt
     hier"), falls in der Quelle vorhanden, klar als Annotation markiert.
   - Kopfzeile: Rechtsgrundlage, RIS-Link, Extraktionsdatum.
3. **Klassen-Extrakte** — einer pro Klassenordner:
   - Ziel: `lehrplan/<fach>-<zweig>/<KLASSE>/<KLASSE>.lehrplan.md`
     (z. B. `lehrplan/infi-hwii/4HWII/4HWII.lehrplan.md`).
   - Inhalt: **nur** der klassenrelevante Jahrgang (z. B. IV. Jahrgang =
     KM 7 + KM 8 für eine 4.-Jahres-Klasse), also Bildungs- und
     Lehraufgabe + Lehrstoff ihrer Kompetenzmodule — **inklusive der
     vollständigen Erläuterungs-Ebene** (KM-Überblicke, Lernziel- und
     Lehrstoff-Erläuterungen).
   - Kopfzeile: Klassenname ↔ Jahrgang ↔ Kompetenzmodule, Rechtsgrundlage,
     Extraktionsdatum.
   - Die Jahrgang ↔ KM-Zuordnung stammt aus METADATA.md.
4. **Klassennamen in den Lehrplan aufnehmen:** sicherstellen, dass die
   Klassen-Zuordnung in METADATA.md jeden unterrichteten Jahrgang (pro
   Zweig) auf seine GROSSBUCHSTABEN-Klassennamen abbildet. Fehlende Zeilen
   ergänzen; nie Zeilen ohne Nutzer-Bestätigung entfernen.
5. **Manuelle Annotationen bewahren:** existiert eine Extrakt-Datei
   bereits, zuerst lesen. Re-Extraktion darf menschliche Annotationen
   (Hervorhebungen, Querverweise) **oder existierende Erläuterungen**
   nicht still verwerfen. Gesetzestext neu aufbauen, dann betroffene
   Annotationen und Erläuterungen neu anwenden, regenerieren oder
   markieren — nie eine menschlich verfasste Erläuterung still löschen;
   im Zweifel behalten und zur Durchsicht markieren.
6. Bericht: geschriebene Dateien, abgedeckte Jahrgänge, Annotationen oder
   Erläuterungen, die manuell nachgeprüft werden müssen.

## Aufgabe 3 (bei Bedarf) — Lehrstoffverteilung/Semesterplan (interaktives Protokoll)

Zweck: aus den extrahierten Lehrplänen eine konkrete Lehrstoffverteilung
entwerfen — `jg<N>-einheiten.md` und `jg<N>-semesterplan-ws.md` bzw.
`jg<N>-semesterplan-ss.md` unter `unterricht/<ZWEIG>-<FACH>/`. Dies ist
ein **interaktives Protokoll**: der Skill entwirft, der Nutzer entscheidet.
Nie eine finale Lehrstoffverteilung ohne den Nutzer-Review-Schritt
schreiben.

Protokoll:

1. **Input-Check** (alles muss existieren; falls nicht, auf die fehlenden
   Aufgaben-1/2-Ausgaben hinweisen und stoppen):
   - Klassen-Extrakt `lehrplan/<fach>-<zweig>/<KLASSE>/<KLASSE>.lehrplan.md`
     mit Erläuterungs-Ebene (die inhaltliche Wirbelsäule).
   - KM-Steckbriefe
     `lehrplan/<fach>-<zweig>/kompetenzmodule/km<N>.md` (zur Kontextlektüre).
   - Zeitmodell aus `lehrplan/METADATA.md` (Wochenstunden/
     Doppelstunden pro Semester — bestimmt die Anzahl der UE).
   - Ressourcen-Matrix (z. B. `lehrplan/ressourcen-matrix.md`), falls
     vorhanden — für Lektüre-Anker.
2. **UE-Raster-Entwurf**: den KM-Inhalt (Lernziele + Lehrstoff) gemäß
   Zeitmodell auf UE-Blöcke abbilden (reale UE + reservierte DS für
   Tests/Admin). Den Entwurf als kompakte Tabelle präsentieren
   (UE | Thema | KM/Lernziel-Bezug | geplante Lektüre-Anker). Annahmen
   explizit nennen (Vorwissen aus früheren KMs, Reihenfolge-Entscheidungen).
3. **Nutzer-Review (Pflichtschritt)**: Entwurf präsentieren und nach
   Bestätigung/Anpassungen fragen — Reihenfolge, Schwerpunkte, reservierte
   Slots. Erst fortfahren, wenn der Nutzer das Raster geprüft hat.
4. **Ausarbeitung**: `unterricht/<ZWEIG>-<FACH>/jg<N>-einheiten.md` bzw.
   `jg<N>-semesterplan-ws.md` / `jg<N>-semesterplan-ss.md` schreiben,
   dem bestehenden Format im Repo folgend (UE-Tabellen nach thematischen
   Blöcken, Kopf mit Zeitmodell, Werkzeug, KM-Steckbrief- und
   Ressourcen-Anker-Verweisen, reservierte DS und Schwerpunkte-Zusammenfassung
   am Ende).
   - `<N>` = Jahrgang der Zielklasse (z. B. 4HWII → `jg4-…`).
   - **Pro UE-Themenblock: eine inhaltliche Beschreibung** — ein kurzer
     Erläuterungsabsatz (oder annotierte Tabellenzeilen) pro thematischem
     Block/UE: was das Thema IST, mit integriertem Anwendungs- und
     Berufsbezug (siehe „Qualitätskriterien für Erläuterungen"). Gerade
     hier müssen die Erläuterungen substantiell sein — dies ist die
     Schicht, aus der Lehrkräfte tatsächlich unterrichten.
5. **Manuellen Inhalt bewahren**: existiert bereits eine
   Lehrstoffverteilung, zuerst lesen. Überarbeitung darf bestehenden
   Inhalt (UE-Blöcke, Annotationen, didaktische Notizen) nicht still
   verwerfen. Diff-artige Zusammenfassung der Änderungen zeigen.
6. **Iteration**: Folge-Anpassungen anbieten (Umreihung, Lektüre-Anker
    tauschen, Reserve-UE ergänzen). Der Nutzer entscheidet, wann der Plan
   final ist.

### Retrofit-Klausel (bereits lehrplan-aktivierte Repos)

In Repos, in denen der Skill **vor der Unterrichts-Trennung** gelaufen
ist, liegen Altbestände unter `lehrplan/` — typischerweise:

- `lehrplan/<KLASSE>/semesterplan-ws.md` / `semesterplan-ss.md`
- `lehrplan/<KLASSE>/jg<N>-einheiten.md` (z. B. GRG-INFI:
  `lehrplan/4HWII/jg4-einheiten.md`)
- `NN-slug/`- und `YYYY-MM-DD_thema/`-Stunden-Ordner unter
  `lehrplan/<KLASSE>/`

Vorgehen beim Antreffen (Aufgabe A oder 3):

1. **Melden, nicht handeln:** Altbestände als Migrationsbefund listen
   (Quelle → Ziel), z. B.
   `lehrplan/4HWII/jg4-einheiten.md` → `unterricht/HWII-INFI/jg4-einheiten.md`.
2. Umbenennungen auf das **einheitliche `jg<N>`-Schema** mit einbeziehen
   (z. B. `semesterplan-ws.md` in einem 4HWII-Ordner →
   `jg4-semesterplan-ws.md`; abweichende Namen wie `JG3-einheiten.md` →
   `jg3-einheiten.md`).
3. Migration (verschieben + umbenennen, bevorzugt `git mv`) **nur nach
   ausdrücklicher Nutzer-Bestätigung** des Vorschlags — nie still
   löschen, nie ohne Bestätigung verschieben.
4. Nach der Migration: Querverweise in METADATA.md, README.md und den
   Semesterplänen auf die neuen Pfade prüfen und (auf Wunsch) anpassen.

Die Stunden-Ordner (`NN-slug/`, `YYYY-MM-DD_thema/`) gehören inhaltlich
zum **Unterricht-Skill** — ihr Umzug wird gemeldet und empfohlen, ihre
Detailpflege liegt danach beim Unterricht-Skill.

## Qualitätskriterien für Erläuterungen

Gemeinsame Regeln für jede Erläuterung (Aufgabe-2-Extrakte und
Aufgabe-3-Lehrstoffverteilungen). Eine Erläuterung beantwortet zuerst und
vornehmlich: **„Was ist das eigentlich? Worum geht es?"**

1. **Begriffserklärung (Kern, Hauptanteil):** Was ist das Thema inhaltlich?
   Grundidee, zentrale Konzepte, Methoden — verständlich auf Deutsch
   beschrieben. Keine bloße Umformulierung des Gesetzestexts: die
   Terminologie auspacken.
2. **Anwendungs- und Berufsbezug (integrierter Bestandteil):** konkrete
   Einsatzmöglichkeiten im Beruf (real, spezifisch — z. B.
   „Annahmeprüfung → Wareneingangskontrolle nach ISO 2859 in der
   Fertigung"). In die Erläuterung integriert, nicht angeflanscht.
3. **Alltagsbezug und Querverweise (optional, wenn sinnvoll):** wo dem
   Thema im Alltag begegnet; Anknüpfungspunkte zu anderen
   Kompetenzmodulen, Fächern oder späteren Jahrgängen.

Regeln:

- **Länge:** 3–7 Sätze sind die Norm; bei bedürftigem Thema darf es gern
  mehr sein — lieber ausführlich als knapp. Keine starre
  2–4-Satz-Schablone.
- **Deutsch, substantiell:** keine generischen Floskeln („wichtiges
  Thema", „in vielen Bereichen relevant"). Jeder Satz muss Inhalt tragen.
- **Niemals mit dem Gesetzestext vermischen:** Erläuterungen sind IMMER
  klar als Annotationen markiert (Blockquote mit `**Überblick:**` /
  `**Erläuterung:**`). Das wortwörtliche Gesetz bleibt unmarkiert.
- **Menschlich verfasste Erläuterungen rangieren über generierten:** bei
  Wiederholungen bewahren (siehe Aufgabe 2, Schritt 5).

## RIS-Praxiswissen (projektübergreifend)

Generisches, gegenstandsunabhängiges Wissen zum Fetchen von
ris.bka.gv.at. Angereichert aus realen Aufgabe-1/2-Läufen.
**Persist-back-Regel: nach jedem Aufgabe-1/2-Lauf neu gelernte generische
RIS-Muster in diesen Abschnitt übernehmen** (Wissen auf Skill-Ebene —
dieses Wissen ist nicht projektspezifisch und darf nicht in den Docs
eines einzelnen Repos gefangen bleiben).

### Fetch-Strategien

- **Nie** `webfetch` auf die `GeltendeFassung.wxe`-Seite
  (Gesetzesnummer-URL) — bei Lehrplanpaketen liefert sie das *gesamte*
  Paket (alle Anlagen, oft > 5 MB) und überschreitet das webfetch-Limit.
  Stattdessen `curl` + lokales Parsen.
- **Autorisierender Ein-Zeilen-Novellen-Check:** `curl` auf das
  **NOR-Dokument der Anlage des Zweigs** (Link in METADATA.md gespeichert).
  Sein Kundmachungsorgan-Kopf liest sich z. B. „BGBl. II Nr. 262/2015
  zuletzt geändert durch BGBl. II Nr. 250/2021" — eine Zeile,
  Änderungsprüfung komplett. Mit
  `rg -o ".{200}zuletzt geändert.{200}"` extrahieren.
- **Novelle identifizieren:** die ELI-Seite
  `https://www.ris.bka.gv.at/eli/bgbl/II/<Jahr>/<Nr>` ist klein und liefert
  Kurztitel, Kundmachungsdatum, Typ, einbringende Stelle.
- **Novellen-Details:** signiertes PDF unter
  `https://www.ris.bka.gv.at/Dokumente/BgblAuth/BGBLA_<Jahr>_II_<Nr>/BGBLA_<Jahr>_II_<Nr>.pdf`,
  dann `pdftotext` + `rg`. Details:
  - Novellen-§§ sind fortlaufend **pro Novelle** nummeriert — nach
    `Anlage <N.N>` / Gegenstands-Schlüsselwörtern greppen, um die §§ zu
    finden, die die Anlage des Gegenstands berühren.
  - Inkrafttreten-Muster: „Die Abschnitte I und VII der Anlage <N.N> …
    treten hinsichtlich des I. Jahrganges mit 1. September <Jahr> und
    hinsichtlich der weiteren Jahrgänge jeweils mit 1. September der
    Folgejahre jahrgangsweise aufsteigend in Kraft."
  - Eine Novelle kann bloß allgemeinbildende Abschnitte berühren (z. B.
    Religion/Ethik 2021), während der Abschnitt des Gegenstands
    unverändert bleibt — in dem Fall bleiben die Extrakte gültig, keine
    Re-Extraktion.
- **ELI-Seite des Stammgesetzes** (`…/eli/bgbl/II/2015/262/20150917`)
  listet alle Anlagen und Kern-Metadaten — nützlich für Aufgabe A.

### PDF-Ablage

- RIS-PDFs nach `lehrplan/RIS/YYYY-MM-DD_<name>.pdf` mit dem
  **Kundmachungsdatum** (das Fetch-Datum ist irrelevant — das Präfix
  datiert den Gesetzestext). Novellen:
  `lehrplan/RIS/YYYY-MM-DD_BGBl-II-<Nr>_Novelle-<slug>.pdf`.
- Der `lehrplan/`-Root bleibt sauber: Gesetzestext-PDFs im
  `lehrplan/`-Root sind ein Konformitäts-Check-Befund mit
  Migrationspflicht.
- Andere (nicht-RIS-)Referenz-PDFs unterliegen **nicht** der
  Datumpräfix-Konvention und kommen nie in `lehrplan/RIS/`.

### Ausgabe in METADATA.md

- Jede RIS-Abfrage in METADATA.md dokumentieren: „RIS-Status abgefragt am
  YYYY-MM-DD: … zuletzt geändert durch …" als Belegzeile unter der
  Änderungshistorie.
- Niemals eine Änderung einer BGBl.-Nummer zuordnen, ohne sie gefetcht zu
  haben — plausibel aussehende Paare (Datum + Nummer) können falsch sein
  (z. B. BGBl. II Nr. 74/2017 = IngG-Fachrichtungsverordnung, hat mit dem
  HTL-Lehrplanpaket nichts zu tun).

## Explizit außerhalb des Scopes

- **Stunden-Material, Präsentationen, Hausübungen** gehören zu anderen
  Skills — der Unterricht-Skill (noch zu erstellen) ist für alles unter
  `unterricht/<ZWEIG>-<FACH>/` außer den Einheiten- und Semesterplan-Dateien
  zuständig; `homework` und `teach` für die jeweiligen Spezialfälle.
- **KM-Steckbriefe** (`kompetenzmodule/`) sind didaktische Autorenschaft;
  dieser Skill liest sie nur zur Kontextlektüre, schreibt sie nie um.
- **Kein Auto-Commit.** Niemals committen. Commits folgen dem
  Issue-Workflow des Repos, falls vorhanden.
- **Keine Auto-Migration.** Alt-Layouts werden gemeldet (Befund mit
  Migrationsvorschlag); verschoben/umbenannt wird nur nach
  ausdrücklicher Nutzer-Bestätigung.

## Randbedingungen

- Deutsche Ausgabe mit korrekten UTF-8-Umlauten; keine Transliterationen
  (ae/oe/ue).
- Niemals Gesetzestext, Daten oder BGBl.-Referenzen fabrizieren. Nur aus
  gefetchtem RIS-Inhalt zitieren; im Zweifel neu fetchen.
- **Erläuterungen sind immer klar als Annotationen markiert**
  (Blockquote mit `**Überblick:**` / `**Erläuterung:**`) — Gesetzestext und
  didaktische Erläuterung dürfen sich visuell nie vermischen.
- RIS-Gesetzestext-PDFs mit ISO-8601-Kundmachungsdatum präfixen; andere
  Referenz-PDFs sind ausgenommen.
- Vor dem Schreiben von Dateien einen Plan zeigen; vor Abweichungen vom
  angefragten Umfang bestätigen lassen.
- Aufgabe 3 schreibt nie eine finale Lehrstoffverteilung ohne den
  Nutzer-Review-Schritt (Pflichtschritt).
- Die Klassen-Zuordnungstabelle in diesem Skill wird manuell gepflegt —
  vorschlagen, nie selbst editieren.
- GROSSBUCHSTABEN-Klassennamen überall (Ordner, Extrakt-Dateien,
  METADATA.md); Ausnahme: die Ordner `lehrplan/<fach>-<zweig>/` sind
  klein, `unterricht/<ZWEIG>-<FACH>/` groß.
- Repos ohne `lehrplan/`-Struktur: nur berichten, nichts anlegen oder
  migrieren ohne ausdrückliche Nutzer-Anweisung.
