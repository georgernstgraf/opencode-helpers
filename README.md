# opencode-helpers

Reusable AI agent configuration templates for [opencode](https://opencode.ai) projects.

---

## 🇩🇪 Deutsch

### Über dieses Projekt

**opencode-helpers** ist eine zentrale Sammlung von wiederverwendbaren Skills, Kommandos und Konfigurationen für KI-gestützte Entwicklung mit opencode.

Das Repository richtet sich an:
- **Lehrerkollegen der HTL Spengergasse** — für Notengebung, Hausübungsgenerierung, Schularbeitserstellung und Issue-basiertes Arbeiten
- **Schüler** — die opencode in Projekten einsetzen und von fertigen Workflows profitieren
- **die internationale opencode-Community** — die Standard-Workflows sucht

Alle Skills und Kommandos werden von anderen Projekten mittels **symbolischer Links** eingebunden — kein Fork, kein Copy-Paste.

### 🔍 SearXNG — Eigener Suchserver

Wir betreiben einen selbstgehosteten [SearXNG](https://searxng.claw.graf.priv.at/)-Metasuchserver:
- **Metasearch** über Brave, Wikipedia, GitHub, Hacker News, ArXiv u.v.m.
- **Datenschutzfreundlich** — keine Weitergabe an Google/Bing
- **MCP-Server** in `skills/searxng/scripts/opencode-searxng` — ein JSON-RPC-Wrapper, der SearXNG als opencode-Tool verfügbar macht
- **Konfiguriert in `opencode.json`** — alle Agenten (chat, build, plan) haben Zugriff auf das `searxng_search`-Tool
- **Parameter**: Kategorie (general/images/news/it/science), Zeitfilter (day/week/month/year), Engine-Auswahl, Sprachfilter, Safe Search

### Struktur

```
opencode-helpers/
├── commands/            # Slash-Kommandos (thin wrappers)
├── skills/              # Workflow-Skills (die eigentliche Logik)
├── docs/ai/             # Knowledge-Persistence-Dateien
├── scripts/             # Utility-Skripte (z.B. MCP-Server)
├── AGENTS.md            # Agents-Konfiguration (dieses Projekt)
├── AGENTS.template.md   # Vorlage für andere Projekte
├── IAM.md               # Entwickler-Identität & Präferenzen
└── opencode.json        # MCP-Server-Konfiguration
```

### Identität & Präferenzen (`IAM.md`)

Die Datei [`IAM.md`](IAM.md) beschreibt die Entwickler-Identität (Name, Technologie-Stack, Lehrfächer) sowie Kommunikationspräferenzen. Sie wird vom opencode-Agenten automatisch beim Start eingelesen und hilft, Antworten konsistent an die Bedürfnisse des Entwicklers anzupassen.

### Skills im Überblick

| Skill | Beschreibung | Aufruf |
|-------|-------------|--------|
| `grading-shared` | Geteilte Protokolle: Adressstil, E-Mail-Formeln, DB-Lookup, Bulk-Konkurrenz | Referenziert von anderen Skills |
| `homework` | Generiert per-Lesson `Hausübung.md` aus Git-Historie | Direkter Skill-Aufruf |
| `issue-workflow` | Issue-Lebenszyklus: Start, Commit, Finish mit GitHub-Integration | Sprachsteuerung (s.u.) |
| `knowledge-assessment` | Bewertet Knowledge-Check-Abgaben, erstellt Berichte + E-Mail-JSON | `/knowledge-assess` |
| `knowledge-exam` | Generiert deutsche Mini-Schularbeiten + Lösungen aus Git-Historie | `/knowledge-exam` |
| `knowledge-persistence` | Persistiert Session-Kontext in `docs/ai/` | Sprachsteuerung (s.u.) |
| `projectgrade` | Bewertet Projekt-Repos ganzheitlich (Commits, Issues, PRs) | Direkter Skill-Aufruf |
| `repograde` | Benotet Schüler-Repos (einzeln oder Bulk) | Direkter Skill-Aufruf |
| `fork-policy` | Erzwingt Clean-Main-Branch-Policy auf Forks | On-Demand Skill-Aufruf |
| `orchestration` | Orchestriert Sub-Agenten zur Aufgabenzerlegung | Direkter Skill-Aufruf |
| `searxng` | Websuche über lokale SearXNG-Instanz | Automatisch via `available_skills` geladen (kein Befehl nötig) |
| `grill-me` | Relentlesses Interview zum Schärfen eines Plans/Designs (stateless) | Sprachsteuerung: "grill me", "grill this plan" |
| `grilling` | Die wiederverwendbare Interview-Schleife hinter grill-me/grill-with-docs | Automatisch (model-invoked) |
| `grill-with-docs` | Wie grill-me, baut zusätzlich `CONTEXT.md` und ADRs auf | Sprachsteuerung |
| `domain-modeling` | Aktive Domänenmodell-Disziplin: Glossar schärfen, ADRs erfassen | Automatisch (model-invoked) |
| `teach` | Mehrsession-Lern-Workspace mit Lessons, Referenzen, Lernjournal | Sprachsteuerung: "teach me …" |
| `code-review` | Zweiachsige Review (Standards + Spec) per paralleler Sub-Agenten | Automatisch (model-invoked) |
| `sync-upstream-skills` | Bringt transplantierte Skills auf den Stand des mattpocock-Upstreams | Sprachsteuerung: "sync skills" |

### Transplantierte Skills & Single-Source-Regel

Sechs Skills (`grill-me`, `grilling`, `grill-with-docs`, `domain-modeling`, `teach`, `code-review`) wurden aus [mattpocock/skills](https://github.com/mattpocock/skills) transplantiert und mit opencode-nativem Frontmatter versehen (Claude-spezifische Felder wie `disable-model-invocation` werden zu `slash: true` oder weggelassen; `license: MIT` für Attribution). Upstream-Provenienz steht in `skills/sync-upstream-skills/mapping.json`.

**Single-Source-Regel:** Dieses Repo ist die einzige globale Skill-Quelle (verlinkt via `~/.config/opencode/skills`). Matts Repo (`~/repos/mattpocock/skills`) ist **pull-only** — nie live verlinkt, nie in der opencode-`skills`-Array-Konfiguration. Kein `~/.opencode/skills`-Symlink (cwd-abhängig und nicht v2-stabil). So gibt es pro Skill-Namen genau eine Quelle, Kollisionen sind strukturell ausgeschlossen.

**Sync-Ritual:** `git -C ~/repos/mattpocock/skills pull`, dann den `sync-upstream-skills`-Skill ausführen. Er übernimmt upstream Content-Änderungen, erhält das opencode-Frontmatter, prüft auf Duplikatnamen und dangling Cross-References.

### Kommandos

| Kommando | Beschreibung |
|----------|-------------|
| `/improve` | Prüft Kommandos/Skills auf Inkonsistenzen (Read-only) |
| `/knowledge-assess` | Bewertet Knowledge-Check-Abgaben |
| `/knowledge-exam <klasse> <wochen> <prüfungsdatum>` | Generiert Mini-Schularbeit + Lösungen |
| `/knowledge-persist` | Persistiert Session-Wissen in `docs/ai/` |
| `/nextprompt` | Führt `aitranscribe -q` aus und nutzt Output als nächste Anweisung |
| `/security <output>` | Erstellt Security-Audit-Report |
| `/tmpissue` | Erstellt GitHub-Issue aus `/tmp/issue.md` |

### Natural Language Workflows (keine Slash-Kommandos)

Diese Workflows haben **keine eigenen Slash-Kommandos**. Der Agent erkennt sie an natürlichen Sprachmustern:

**Issue Workflow:**
- *"issue start"*, *"start issue"*, *"begin issue"*, *"neues issue"*, *"ich arbeite an"* → start
- *"issue commit"*, *"commit issue"*, *"speichere issue"*, *"checkpoint"* → commit
- *"issue commit and push"*, *"finish issue"*, *"issue done"*, *"issue fertig"*, *"schließe issue"* → finish

**Knowledge Persistence:**
- *"remember"*, *"merke dir"*, *"don't forget"*, *"behalte das im Kopf"*, *"merk dir das"* → persistieren
- *"save context"*, *"persist knowledge"* → persistieren

### Einbindung in eigene Projekte

1. **opencode-helpers klonen oder als Submodul einbinden:**
   ```bash
   git clone https://github.com/georgernstgraf/opencode-helpers.git
   # oder als Submodul:
   git submodule add https://github.com/georgernstgraf/opencode-helpers.git .opencode-helpers
   ```

2. **Symbolische Links im Zielprojekt anlegen:**
   ```bash
   # Skills (alle Agenten-Workflows)
   ln -s /pfad/zu/opencode-helpers/skills skills

   # Kommandos (Slash-Befehle)
   ln -s /pfad/zu/opencode-helpers/commands commands

   # Knowledge Persistence (docs/ai/ Vorlage)
   cp -r /pfad/zu/opencode-helpers/docs/ai docs/ai

   # AGENTS.md (Onboarding-Template verwenden)
   cp /pfad/zu/opencode-helpers/AGENTS.template.md AGENTS.md
   ```

3. **`AGENTS.md` anpassen:** Platzhalter ausfüllen (`<PROJECT_NAME>`, `<OWNER>`, etc.)

4. **In opencode `/init` ausführen:** Der Agent liest `AGENTS.md`, erkennt die Skill-Trigger und richtet den Rest ein.

### Knowledge Persistence (`docs/ai/`)

Das `docs/ai/`-Verzeichnis erhält Session-Kontext über mehrere KI-Sitzungen hinweg:

| Datei | Zweck | Änderungsmodus |
|-------|-------|---------------|
| `HANDOFF.md` | Offene Aufgaben für nächste Session | Überschreiben |
| `CONVENTIONS.md` | Laufende Regeln und Patterns | Anhängen |
| `DECISIONS.md` | Architekturentscheidungen mit Begründung | Anhängen |
| `ARCHITECTURE.md` | Strukturelle Karte des Systems | Überschreiben |
| `PITFALLS.md` | Gelernte Lektionen und Fallstricke | Anhängen |
| `DOMAIN.md` | Geschäftslogik und Domänenregeln | Anhängen |
| `STATE.md` | Aktueller Projektstatus | Überschreiben |

---

## 🇬🇧 English

### About

**opencode-helpers** is a central collection of reusable skills, commands, and configurations for AI-assisted development with [opencode](https://opencode.ai).

Target audience:
- **Teachers at HTL Spengergasse** — for grading, homework generation, exam creation, and issue-based workflows
- **Students** — using opencode in projects who benefit from ready-made workflows
- **The international opencode community** — looking for standardized agent workflows

All skills and commands are consumed by other projects via **symbolic links** — no forking, no copy-paste.

### 🔍 SearXNG — Self-Hosted Search Server

We run a self-hosted [SearXNG](https://searxng.claw.graf.priv.at/) metasearch instance:
- **Metasearch** across Brave, Wikipedia, GitHub, Hacker News, ArXiv, and more
- **Privacy-friendly** — no data sent to Google/Bing
- **MCP server** in `skills/searxng/scripts/opencode-searxng` — a JSON-RPC wrapper exposing SearXNG as an opencode tool
- **Configured in `opencode.json`** — all agents (chat, build, plan) have access to the `searxng_search` tool
- **Parameters**: category (general/images/news/it/science), time filter (day/week/month/year), engine selection, language filter, safe search

### Structure

```
opencode-helpers/
├── commands/            # Slash commands (thin wrappers)
├── skills/              # Workflow skills (actual logic)
├── docs/ai/             # Knowledge persistence files
├── scripts/             # Utility scripts (e.g., MCP server)
├── AGENTS.md            # Agent config (this project)
├── AGENTS.template.md   # Template for other projects
├── IAM.md               # Developer identity & preferences
└── opencode.json        # MCP server configuration
```

### Identity & Preferences (`IAM.md`)

[`IAM.md`](IAM.md) describes the developer's identity (name, tech stack, teaching subjects) and communication preferences. It is read automatically by opencode on startup and helps tailor responses to the developer's needs.

### Skill Overview

| Skill | Description | Invocation |
|-------|-------------|------------|
| `grading-shared` | Shared protocols: address style, email formulas, DB lookup, bulk concurrency | Referenced by other skills |
| `homework` | Generate per-lesson `Hausübung.md` from Git history | Direct skill invocation |
| `issue-workflow` | Issue lifecycle: start, commit, finish with GitHub integration | Natural language (see below) |
| `knowledge-assessment` | Grade knowledge-check submissions, produce reports + email JSON | `/knowledge-assess` |
| `knowledge-exam` | Generate German mini-exams + solutions from Git history | `/knowledge-exam` |
| `knowledge-persistence` | Persist session context into `docs/ai/` | Natural language (see below) |
| `projectgrade` | Holistic project repo grading (commits, issues, PRs) | Direct skill invocation |
| `repograde` | Grade student repos (single or bulk) | Direct skill invocation |
| `fork-policy` | Enforce clean-main branch policy on forks | On-demand skill invocation |
| `orchestration` | Orchestrate sub-agents for task decomposition | Direct skill invocation |
| `searxng` | Web search via local SearXNG instance | Loaded automatically via `available_skills` (no command needed) |
| `grill-me` | Relentless interview to sharpen a plan/design (stateless) | Natural language: "grill me", "grill this plan" |
| `grilling` | The reusable interview loop behind grill-me/grill-with-docs | Automatic (model-invoked) |
| `grill-with-docs` | Like grill-me, additionally builds `CONTEXT.md` and ADRs | Natural language |
| `domain-modeling` | Active domain-model discipline: sharpen glossary, capture ADRs | Automatic (model-invoked) |
| `teach` | Multi-session learning workspace with lessons, references, learning journal | Natural language: "teach me …" |
| `code-review` | Two-axis review (Standards + Spec) via parallel sub-agents | Automatic (model-invoked) |
| `sync-upstream-skills` | Bring transplanted skills up to date from the mattpocock upstream | Natural language: "sync skills" |

### Transplanted Skills & Single-Source Rule

Six skills (`grill-me`, `grilling`, `grill-with-docs`, `domain-modeling`, `teach`, `code-review`) are transplanted from [mattpocock/skills](https://github.com/mattpocock/skills) and given opencode-native frontmatter (Claude-specific fields like `disable-model-invocation` become `slash: true` or are dropped; `license: MIT` for attribution). Upstream provenance is recorded in `skills/sync-upstream-skills/mapping.json`.

**Single-source rule:** This repo is the only global skill source (linked via `~/.config/opencode/skills`). Matt's repo (`~/repos/mattpocock/skills`) is **pull-only** — never linked live, never listed in an opencode `skills` array. No `~/.opencode/skills` symlink (cwd-dependent and not v2-stable). One source per skill name means collisions are structurally impossible.

**Sync ritual:** `git -C ~/repos/mattpocock/skills pull`, then run the `sync-upstream-skills` skill. It applies upstream content changes while preserving opencode frontmatter, and checks for duplicate names and dangling cross-references.

### Commands

| Command | Description |
|---------|-------------|
| `/improve` | Scan commands/skills for inconsistencies (read-only) |
| `/knowledge-assess` | Grade knowledge-check submissions |
| `/knowledge-exam <class> <weeks> <exam-date>` | Generate mini-exam + solutions |
| `/knowledge-persist` | Persist session knowledge into `docs/ai/` |
| `/nextprompt` | Run `aitranscribe -q` and use output as next instruction |
| `/security <output>` | Generate security audit report |
| `/tmpissue` | Create GitHub issue from `/tmp/issue.md` |

### Natural Language Workflows (no slash commands)

These workflows have **no dedicated slash commands**. The agent recognizes them from natural language patterns:

**Issue Workflow:**
- *"issue start"*, *"start issue"*, *"begin issue"*, *"neues issue"*, *"ich arbeite an"* → start
- *"issue commit"*, *"commit issue"*, *"speichere issue"*, *"checkpoint"* → commit
- *"issue commit and push"*, *"finish issue"*, *"issue done"*, *"issue fertig"*, *"schließe issue"* → finish

**Knowledge Persistence:**
- *"remember"*, *"merke dir"*, *"don't forget"*, *"behalte das im Kopf"*, *"merk dir das"* → persist
- *"save context"*, *"persist knowledge"* → persist

### Integration into Your Project

1. **Clone or add opencode-helpers as a submodule:**
   ```bash
   git clone https://github.com/georgernstgraf/opencode-helpers.git
   # or as submodule:
   git submodule add https://github.com/georgernstgraf/opencode-helpers.git .opencode-helpers
   ```

2. **Create symbolic links in your target project:**
   ```bash
   # Skills (all agent workflows)
   ln -s /path/to/opencode-helpers/skills skills

   # Commands (slash commands)
   ln -s /path/to/opencode-helpers/commands commands

   # Knowledge persistence (docs/ai/ template)
   cp -r /path/to/opencode-helpers/docs/ai docs/ai

   # AGENTS.md (use the onboarding template)
   cp /path/to/opencode-helpers/AGENTS.template.md AGENTS.md
   ```

3. **Customize `AGENTS.md`:** Fill in placeholders (`<PROJECT_NAME>`, `<OWNER>`, etc.)

4. **Run `/init` in opencode:** The agent reads `AGENTS.md`, recognizes the skill triggers, and sets up the rest.

### Knowledge Persistence (`docs/ai/`)

The `docs/ai/` directory maintains context across AI sessions:

| File | Purpose | Update mode |
|------|---------|------------|
| `HANDOFF.md` | Open tasks for next session | Overwrite |
| `CONVENTIONS.md` | Ongoing rules and patterns | Append |
| `DECISIONS.md` | Architecture decisions with rationale | Append |
| `ARCHITECTURE.md` | Structural map of the system | Overwrite |
| `PITFALLS.md` | Hard-won lessons and pitfalls | Append |
| `DOMAIN.md` | Business logic and domain rules | Append |
| `STATE.md` | Current project status | Overwrite |

---

## License

MIT

## Contributing

Issues and PRs welcome at [github.com/georgernstgraf/opencode-helpers](https://github.com/georgernstgraf/opencode-helpers)
