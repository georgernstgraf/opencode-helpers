---
name: sync-upstream-skills
description: Re-transplant owned skills from their mattpocock upstream after a git pull, applying upstream content changes while preserving opencode-native frontmatter. Also checks for duplicate skill names and dangling cross-skill references. Use when the user says "sync skills", "refresh from upstream", "pull matt's skills", or wants to bring the owned transplanted skills up to date.
license: MIT
---

# Sync Upstream Skills

This repo owns a small set of skills transplanted from mattpocock's `skills` repo. They live here with opencode-native frontmatter (the upstream's `disable-model-invocation: true` becomes `slash: true` or is dropped; `argument-hint` and other Claude-specific fields are dropped). This skill re-applies upstream changes on demand without re-introducing a live second source.

## The mapping

Read [mapping.json](./mapping.json) in this directory. Each entry maps an owned skill name (the directory name under `skills/`) to its upstream path relative to `~/repos/mattpocock/skills/skills/`.

## Procedure

### 1. Update the upstream

```
git -C ~/repos/mattpocock/skills pull
```

If already up to date, report that and stop.

### 2. For each mapped skill

For each `name -> upstream-path` entry in mapping.json:

1. Read the upstream `SKILL.md` at `~/repos/mattpocock/skills/skills/<upstream-path>/SKILL.md`.
2. Read the owned `SKILL.md` at `skills/<name>/SKILL.md`.
3. Compare the **body** (everything after the frontmatter delimiter). opencode ignores Claude-specific frontmatter fields (`disable-model-invocation`, `argument-hint`, `policy.*` in `agents/openai.yaml`), so ignore those when diffing; only the prose body is what changes upstream.
4. If the body changed:
   - Take the upstream body verbatim.
   - Re-attach the owned frontmatter (preserve `name`, `description`, `slash`, `license`). If the upstream `description` changed, update ours to match verbatim (the description is what steers the model's invocation in opencode, so it must stay in sync).
   - Write the merged file back to `skills/<name>/SKILL.md`.
5. Copy any **sibling files** the upstream changed (e.g. `*-FORMAT.md`, `GLOSSARY.md`). These are resource files referenced by the skill body. Copy verbatim; they carry no opencode frontmatter.
6. If the upstream **added** a new sibling file the owned copy doesn't have, copy it. If the upstream **removed** one, delete ours.

### 3. Dup-name check

After syncing, scan every `skills/*/SKILL.md` in this repo:

- Extract the `name` field from each frontmatter.
- Report any name that appears more than once. opencode requires the directory name to match the `name` field and last-write-wins resolves duplicates by source order, so two skills with the same `name` silently shadow each other.
- Also report any skill directory whose name doesn't match its frontmatter `name` (opencode validation: `^[a-z0-9]+(-[a-z0-9]+)*$`, must match the directory).

### 4. Dangling cross-reference check

Several transplanted skills reference other skills by name in their body (e.g. `grill-with-docs` calls `/domain-modeling`, `grill-me` calls `/grilling`). For each `/skill-name` reference in any owned skill body:

- If `skill-name` is **not** in mapping.json and **not** present as a directory under `skills/`, report it as a dangling reference. The skill would tell the agent to load a skill that doesn't exist in this repo.

### 5. Report

Summarize: which skills changed, which sibling files changed, any dup-name or dangling-reference issues found. Then ask the user to review and commit.

## What this skill does NOT do

- It does **not** add a live `~/.opencode/skills` source or a `skills` array pointing at matt's repo. The single-source rule stands: this repo is the only global source, matt's repo is pull-only.
- It does **not** transplanted-skills sync rename or namespace skills. If you want to rename a transplanted skill, edit the directory + frontmatter `name` together and remove the entry from mapping.json (or point it at a new upstream) manually.
- It does **not** add new transplanted skills. To add one, create the directory, copy `SKILL.md` + siblings, write opencode-native frontmatter, and add an entry to mapping.json by hand.

## Frontmatter translation table

When syncing, translate upstream frontmatter to opencode-native:

| Upstream field | Owned field |
|---|---|
| `name` | `name` (verbatim) |
| `description` | `description` (verbatim; keep up to date, this steers model invocation) |
| `disable-model-invocation: true` | `slash: true` (user-invoked) |
| (no `disable-model-invocation`) | omit `slash` (model-invoked) |
| `argument-hint` | drop (opencode ignores it) |
| `policy.*` in `agents/openai.yaml` | drop (opencode-specific; not transplanted) |
| (none) | `license: MIT` (attribution) |

opencode only reads `name`, `description`, `slash` from the frontmatter. Everything else is ignored at runtime but kept for attribution and human readability.
