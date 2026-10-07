# Axis Briefs

Each brief is pasted into the corresponding axis sub-agent prompt, together with the recon summary, the relevant tool outputs, and the finding schema from [SKILL.md](./SKILL.md).

An axis agent returns findings only for its axis, with evidence (`path:line`) for every one, and no speculation that lacks a concrete failure or change path.

---

## 1. Security (in depth)

Find exploitable or risky security issues and rank them by severity. The scanners in [TOOLS.md](./TOOLS.md) give the mechanical baseline; you add the reasoning they cannot: authorization logic, business-logic bypass, and trust boundaries.

Check, at least:

- **Secrets** - hardcoded credentials, tokens, keys (`gitleaks`/`trufflehog`), committed `.env`, secrets written to logs.
- **Injection** - SQL/NoSQL, shell/command, template/SSTI, LDAP, XPath; unsafe string building (`semgrep`, `bandit`).
- **Authn/Authz** - missing checks, IDOR (object access without an ownership check), privilege escalation, insecure session handling, JWT misuse (algorithm confusion, no expiry).
- **Deserialization** - `pickle`, Java serialization, YAML `load`, `eval`/`exec`.
- **Crypto** - weak hashes (MD5/SHA1) for passwords, ECB mode, hardcoded IV/salt, `Math.random` for security, disabled TLS verification.
- **Web** - SSRF, path traversal, XXE, open redirect, CORS `*` with credentials, CSRF, missing rate limiting, error messages leaking internals.
- **Dependencies** - known CVEs (`osv-scanner`/`npm audit`/`pip-audit`/`govulncheck`/`cargo audit`); flag only reachable, real risk, not scanner noise.
- **Config** - debug enabled in production, permissive file modes, containers running as root, over-broad IAM.

Prioritize trust boundaries: request handlers, auth, DB access, file IO, external calls. Discard a finding if you cannot state a concrete attack or failure path.

---

## 2. Structure & clean layers

Decide whether the code respects its intended layering and boundaries. The dependency graph from the tools is authoritative for the edges; read only the offending seams.

Check:

- **Layer direction** - dependencies flowing inward (domain <- application <- infrastructure); infrastructure details leaking into the domain; UI talking to persistence directly.
- **Boundary leaks** - modules reaching into another's internals; cross-package imports that should cross an interface.
- **Responsibility placement** - business rules in controllers/handlers; SQL in views; validation only at the edge.
- **Consistency** - the same concern solved two different ways in sibling modules.

Feed from `dependency-cruiser`/`import-linter`/`jdeps`/`ArchUnit`/`go list`/`cargo-modules` for the edge list; quote the specific offending imports as evidence.

---

## 3. Coupling & entanglement (Wartbarkeit)

Find what makes change expensive. This axis is graph- and history-driven, so lean on the tool output rather than reading code.

Check:

- **Cycles** - import/dependency cycles (tools).
- **Hubs** - high fan-in/fan-out modules everything depends on; god modules.
- **Change coupling** - files that nearly always change together (git co-change); a single change forcing edits in many files (shotgun surgery).
- **Duplicated concepts** - the same entity or logic modeled twice across modules; shared mutable global state; hidden temporal coupling (order-dependent initialization).
- **Blast radius** - how far one change ripples.

Quote the co-change pairs and the graph edges as evidence.

---

## 4. Architecture & deep modules

Judge module **shape**: a lot of behaviour behind a small interface at a clean seam. Use the `codebase-design` vocabulary exactly (module, interface, depth, seam, adapter, leverage, locality); never drift into "service", "component", or "boundary".

Check, weighted to the churn hotspots:

- **Shallow modules** - interface nearly as complex as the implementation; pass-throughs.
- **Deletion test** - if deleting the module concentrates complexity, it earns its keep; if complexity merely moves, it is a pass-through.
- **Seam placement** - seams that do not correspond to any real variation; missing seams where behaviour actually varies.
- **Testability** - can behaviour be exercised through the interface? Are bugs hidden in how pure functions are wired together?
- **Locality** - does understanding one concept require bouncing between many small files?

Scope: read only the hotspot modules chosen in the scaling step, not the whole repo.
