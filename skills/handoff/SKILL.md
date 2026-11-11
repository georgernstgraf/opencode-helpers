---
name: handoff
description: Compact the current conversation into a handoff document for another agent to pick up. Use when the user says "handoff", "write a handoff", "handoff document", "summarize this for the next session", "compact this conversation" or "übergib das an die nächste Session". Do not use for persisting knowledge into docs/ai — that is knowledge-persistence.
metadata: { "opencode/autoinvoke": false }
---

Write a handoff document summarising the current conversation so a fresh agent can continue the work. Save to the temporary directory of the user's OS - not the current workspace.

Include a "suggested skills" section in the document, naming which skills the next agent should call the Skill tool for.

Do not duplicate content already captured in other artifacts (specs, plans, ADRs, issues, commits, diffs). Reference them by path or URL instead.

Redact any sensitive information, such as API keys, passwords, or personally identifiable information.

If the user passed arguments, treat them as a description of what the next session will focus on and tailor the doc accordingly.

## Done when

- [ ] The handoff document is saved to the OS temporary directory, not the
      workspace.
- [ ] It contains a "suggested skills" section naming the skills the next agent
      should load.
- [ ] Specs, plans, ADRs, issues, commits and diffs are referenced by path or URL
      rather than copied.
- [ ] API keys, passwords and personal data are redacted.
- [ ] When arguments were passed, the document is tailored to that next-session
      focus.
