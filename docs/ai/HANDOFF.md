Open tasks:

1. [ ] writing-for-agents audit — **P4** (last phase): add Completion Criteria
      ("Done when …") to each skill's instruction body and split the
      frontmatter `description` into clear trigger branches.
      Scope: ~20 skills under `skills/*/SKILL.md`.
      Prior phases shipped: P1 (`c4cff84`), P2 SSOT (`dbc9bde`),
      P3a progressive disclosure (`070961a`).
      P3a established the sibling pattern (`[X.md](./X.md)`, guarded by
      `tests/test_skill_links.py`) — P4 must keep links resolving and must
      NOT re-duplicate moved reference material. Verify with
      `python3 -m unittest discover -s tests -v`.

2. [ ] dell-repo sync pending: dell's `~/repos/georgernstgraf/opencode-helpers`
      sits on `d14cc25` with an uncommitted local change to
      `skills/lehrplan/SKILL.md` — the **Fachgruppen-Variante** for
      multi-subject repos (43 insertions, 2 deletions; self-contained
      `<fach>-<zweig>/` folders, flat `jahr_<N>_semesterplan_{ws,ss}.md`,
      `Gesetzestexte/` exception). Next session: diff-review it, commit, then
      integrate with `ee3d02f` (think's Drei-Aufgaben-Struktur commit) and the
      newer main (P1/P2/P3a; text conflict in SKILL.md is likely — integrate
      both), push. Also replicate the `agents/` directory + the
      `~/.config/opencode/agents` symlink on dell.

3. [ ] Credentials im SVN (infra) — canonical task lives in
      `~/svn/georg/docs/ai/HANDOFF.md` **Task 5**
      (consolidate → `svn:ignore` → history rewrite → rotation of all leaked
      secrets incl. infra private keys). This repo only contributed the SearXNG
      access-control half (nginx Basic-Auth + `8888` on `127.0.0.1` + wrapper
      credential) — that part is done. Track the SVN/secret work over there.

Last updated: 2026-09-13.
