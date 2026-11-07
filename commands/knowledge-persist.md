---
description: Persist session knowledge to docs/ai/ files
---

Review our entire conversation and update the knowledge files in
docs/ai/.
Use the knowledge-persistence skill for this.

The knowledge set is an Open Knowledge Format (OKF v0.2) bundle: every
concept file carries the frontmatter envelope (`type`, `generated`,
`verified`, `status`, optional `sources`), `log.md` gets a date-grouped
entry for this run, and `index.md` is regenerated. Legacy files without
frontmatter migrate on touch. Full templates: FILE-TEMPLATES.md in the
skill; OKF conformance: OKF-SPEC.md in the skill.

For each file, only add what is new or changed. Do not duplicate
existing entries. Write directly to disk.

Then commit and push the updated knowledge files (its own commit with the
active issue reference; SVN: `svn ci`) — persistence is only complete once the
changes are on the trunk. Never create an empty commit, and never close/reopen
an issue here.
