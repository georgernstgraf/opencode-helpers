# Grading Email Body Examples

Worked examples of the two homework-grading email bodies. The structure they
follow is defined in `SKILL.md` under **Email Body Format**; use these as shape
references, not as text to copy verbatim.

## Example: Formal Homework Email Body

```
Sehr geehrte Frau Huber,

im Folgenden finden Sie die automatische Beurteilung Ihrer Leistungsfeststellung. Bitte beachten Sie, dass diese Beurteilung Irrtümer enthalten kann.

Ich habe Ihre Hausübungen, welche im Zeitraum vom 4. März bis zum
18. März aufgegeben waren, durchgesehen.

In Ihrem Repository habe ich insgesamt 12 Commits in diesem Zeitraum
gefunden. Die Arbeit war regelmäßig verteilt, mit einem deutlichen
Schwerpunkt in der ersten Woche. Die meisten Änderungen betrafen
SQL-Skripte und Datenbank-Schema-Dateien.

HÜ1: Erstellung einer SQL-Datenbank mit CREATE TABLE und INSERT
statements für ein Bibliotheksverwaltungssystem.
HÜ2: Implementierung von JOIN-Operationen zwischen den Tabellen
der Bibliotheksdatenbank.

HÜ1 – Bibliotheksdatenbank:

Sie haben die Tabellenstruktur sauber entworfen und die
Fremdschlüsselbeziehungen korrekt definiert. Die INSERT-Statements
decken die wesentlichen Daten ab. Bei der Tabelle "Ausleihe" hätte
das Rückgabedatum als nullable Spalte definiert werden sollen, da
ein Buch zum Zeitpunkt der Ausleihe noch nicht zurückgegeben sein
muss. Bewertung: 80%.

HÜ2 – JOIN-Operationen:

```sql
SELECT b.Titel, a.Name
FROM Buecher b
JOIN BuchAutor ba ON b.BuchID = ba.BuchID
JOIN Autoren a ON ba.AutorID = a.AutorID;
```

Dieser Dreifach-Join ist korrekt umgesetzt. Die Alias-Namen sind
sinnvoll gewählt. Bei der LEFT JOIN-Aufgabe fehlt jedoch die
Berücksichtigung von Büchern ohne Ausleihe – hier wäre ein LEFT
JOIN statt des INNER JOIN nötig gewesen. Bewertung: 65%.

Insgesamt zeigen Ihre Abgaben ein solides Grundverständnis der
relationalen Datenbankkonzepte. Es empfiehlt sich, die
Unterschiede zwischen den JOIN-Typen (INNER, LEFT, RIGHT) noch
einmal anhand praktischer Beispiele nachzuvollziehen. Die
Tabellenstruktur der Bibliotheksdatenbank ist Ihnen gut gelungen.

Beide Hausübungen waren erkennbar abgegeben. Die erste Aufgabe war
weitgehend vollständig, bei der zweiten Aufgabe gab es inhaltliche
Lücken bei einzelnen JOIN-Varianten.

Insgesamt ist eine solide Grundlage erkennbar. Es lohnt sich, die
Behandlung unvollständiger Ergebniszeilen bei LEFT JOINs noch gezielt
zu üben.

Endbewertung: 73/100 (73%)

Mit freundlichen Grüßen,

   Georg Graf
```

## Example: Informal Homework Email Body

```
Lieber Thomas,

im Folgenden findest du die automatische Beurteilung deiner Leistungsfeststellung. Bitte beachte, dass diese Beurteilung Irrtümer enthalten kann.

Ich habe deine Hausübungen, welche im Zeitraum vom 4. März bis zum
18. März aufgegeben waren, durchgesehen.

In deinem Repository habe ich 8 Commits gefunden, die meisten davon
in der zweiten Woche. Du hast dich intensiv mit den SQL-Themen
auseinandergesetzt.

HÜ1: Erstellung einer SQL-Datenbank mit CREATE TABLE und INSERT
statements für ein Bibliotheksverwaltungssystem.
HÜ2: Implementierung von JOIN-Operationen zwischen den Tabellen
der Bibliotheksdatenbank.

HÜ1 – Bibliotheksdatenbank:

Du hast die Tabellen korrekt erstellt und die Beziehungen sauber
modelliert. Die Datentypen sind durchgehend passend gewählt.
Die Index-Definitionen fehlen allerdings vollständig – bei einer
Bibliotheksdatenbank mit Suchanfragen auf Titel und Autor wären
Indizes sinnvoll. Bewertung: 75%.

HÜ2 – JOIN-Operationen:

Die einfachen JOINs hast du zuverlässig implementiert. Bei den
komplexeren Abfragen mit Unterabfragen gibt es noch Unsicherheiten.
Die Lösung für "Alle Autoren mit mehr als 3 Büchern" verwendet
einen korrekten Ansatz, die Gruppierung ist aber nicht ganz
vollständig. Bewertung: 60%.

Insgesamt eine ordentliche Leistung. Es wäre hilfreich, wenn du
die JOIN-Typen noch einmal wiederholst – besonders die Fälle,
in denen ein LEFT JOIN nötig ist. Die Grundlagen sitzen, und mit
etwas mehr Übung bei den komplexeren Abfragen wirst du noch
sicherer.

Beide Hausübungen sind erkennbar bearbeitet. Bei der zweiten Aufgabe
zeigen sich aber noch Lücken bei den komplexeren Abfragen.

Insgesamt ist das eine brauchbare Arbeitsgrundlage. Wenn du die
Unterschiede der JOIN-Typen noch sicherer anwenden kannst, wird die
Qualität der Lösungen deutlich steigen.

Endbewertung: 68/100 (68%)

Lieben Gruß,

   Georg Graf
```
