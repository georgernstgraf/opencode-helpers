# Klassen-Zuordnung (MANUELL GEPFLEGT)

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
