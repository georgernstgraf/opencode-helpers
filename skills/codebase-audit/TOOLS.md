# Tooling

"Deterministic tools compress, the agent synthesizes." Detect what is installed, install what is missing when the user allowed it and the network is up, run what applies, and save the raw output to `<scratch>/tool-output/`. The axis agents read those files, not the repository.

## Policy

1. **Detect:** `command -v <tool>`.
2. **Network check:** `curl -sSf -m 5 https://github.com >/dev/null 2>&1 && echo up || echo down`.
3. **Install missing tools when allowed.** Prefer the language's own manager (`npm i -g`, `pipx install`, `go install`, `cargo install`) or the OS manager (`apt`, `brew`). If the user chose "only if installed", or the network is down, or installation fails, **degrade gracefully**: fall back to bounded hotspot reading and note it in the final report.
4. **Save output** per tool to `<scratch>/tool-output/<tool>.txt` so the main context never loads raw tool noise.
5. **Pick the subset by detected stack.** A Python repo does not need `cargo audit`; a TS repo does not need `radon`.

Git-based analysis needs no installation (see the bottom section).

## Structure & dependency graph

| Tool | Stack | Install | Run |
|------|-------|---------|-----|
| dependency-cruiser | JS/TS | `npm i -g dependency-cruiser` | `depcruise --no-config --output-type dot src` |
| madge | JS/TS | `npm i -g madge` | `madge --circular --extensions ts,tsx src` |
| import-linter | Python | `pipx install import-linter` | `lint-imports` (needs a config file) |
| pydeps | Python | `pipx install pydeps` | `pydeps <pkg> --show-deps` |
| jdeps | Java (ships with JDK) | - | `jdeps -summary -recursive target/classes` |
| go list | Go | - | `go list -deps ./...` |
| goda | Go | `go install github.com/loov/goda@latest` | `goda graph ./...` |
| cargo-modules | Rust | `cargo install cargo-modules` | `cargo modules structure --package <pkg>` |

## Security

| Tool | Purpose | Install | Run |
|------|---------|---------|-----|
| semgrep | multi-language AST rules | `pipx install semgrep` | `semgrep --config auto --json .` |
| gitleaks | secrets | `go install github.com/gitleaks/gitleaks/v8@latest` | `gitleaks detect --no-git -v` |
| trufflehog | secrets | binary from releases (or `brew install trufflehog`) | `trufflehog filesystem .` |
| osv-scanner | dependency CVEs | `go install github.com/google/osv-scanner/v2/cmd/osv-scanner@latest` | `osv-scanner -r .` |
| npm audit | JS deps | ships with npm | `npm audit --json` |
| pip-audit | Python deps | `pipx install pip-audit` | `pip-audit --format json` |
| govulncheck | Go deps | `go install golang.org/x/vuln/cmd/govulncheck@latest` | `govulncheck ./...` |
| cargo audit | Rust deps | `cargo install cargo-audit` | `cargo audit --json` |
| bandit | Python SAST | `pipx install bandit` | `bandit -r . -f json` |
| gosec | Go SAST | `go install github.com/securego/gosec/v2/cmd/gosec@latest` | `gosec -fmt=json ./...` |
| brakeman | Ruby on Rails SAST | `gem install brakeman` | `brakeman -f json` |
| trivy | containers / filesystem / IaC | binary from releases | `trivy fs --format json .` |

## Complexity & duplication

| Tool | Purpose | Install | Run |
|------|---------|---------|-----|
| lizard | cyclomatic complexity, multi-language | `pipx install lizard` | `lizard -l <lang>` |
| radon | Python complexity | `pipx install radon` | `radon cc -s -a .` |
| gocyclo | Go complexity | `go install github.com/fzipp/gocyclo/cmd/gocyclo@latest` | `gocyclo -over 15 .` |
| jscpd | copy-paste detection, multi-language | `npm i -g jscpd` | `jscpd --reporters json --output <scratch> .` |
| knip | JS/TS dead code & unused exports | `npm i -g knip` | `knip` |
| vulture | Python dead code | `pipx install vulture` | `vulture .` |

## Change coupling (git, no install)

- **Churn** (most-changed files):

  ```sh
  git log --format= --name-only | grep -v '^$' | sort | uniq -c | sort -rn | head -30
  ```

- **Co-change pairs** (files that change together; the raw signal for hidden coupling):

  ```sh
  git log --pretty=format:'C %H' --name-only \
    | awk '/^C /{emit(); n=0; next} NF{a[n++]=$0} END{emit()}
           function emit(){for(i=0;i<n;i++)for(j=i+1;j<n;j++)print (a[i]<a[j]?a[i]" "a[j]:a[j]" "a[i])}' \
    | sort | uniq -c | sort -rn | head -30
  ```

- **Blast radius of a path** (how often a file drags neighbours along): the co-change pairs above, filtered to the path of interest.

Feed these to the coupling axis; the dependency graph plus the co-change pairs are its evidence.
