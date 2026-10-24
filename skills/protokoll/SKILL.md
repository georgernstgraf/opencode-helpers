---
name: protokoll
description: Bereinigt ein Whisper-Meeting-Transkript in-place zu einem Protokoll (Extrakt + Verlauf).
disable-model-invocation: true
---

Turn a raw Whisper meeting transcript into a **Protokoll**, edited in place: the **Extrakt** (decisions, action items, open points) up front, the **Verlauf** (topic-wise narrative) behind it. Output language follows the transcript's language — in practice German with proper UTF-8 umlauts.

The transcript is the only evidence of what was said. Everything serves **fidelity**: nothing invented, nothing substantive dropped, and nothing silent — every change is either a logged correction or a flag.

1. **Recon.** Read the whole file once. Detect: language, speaker situation (none / generic labels / names in text), and whether the file is already processed (structured Protokoll header present → offer refinement instead of re-processing, and stop). Check the target directory for an existing convention — a `README.md` or sibling protocol defines heading names, file naming, and structure; **the local convention overrides** [`TEMPLATE.md`](TEMPLATE.md). Build the two working artifacts in context (no files): a **topic map** — topics in spoken order, reconstructed when there was no agenda — and a **glossary** — canonical spelling of every person, project, tool, and technical term, since Whisper renders the same name three different ways; the transcript often defines a term itself ("Absort … heißt Update, wenn vorhanden, Insert, wenn nicht" → _upsert_). Then one exchange with the user: missing metadata (date, participants, title) and, when speaker names matter, a roster or permission to infer. Done when topic map, glossary, and metadata exist or are explicitly marked open.

2. **Recovery path.** If the file is git-tracked with a clean working tree, git is the backup. Otherwise copy the file to `<name>.orig.md` first. Done when a recovery path provably exists before any write.

3. **Section by topic.** Split the transcript along the topic map; timestamps become coarse anchors (`[ab 00:14]`). Reordering happens only across topics (grouping); within a topic the flow of speech is kept. Side conversations get their own Verlauf section when they carry decisions, facts, or commitments — off-agenda is irrelevant (the personnel discussion between the greetings is a topic; the greetings themselves are not). Pure greeting and logistics chatter compresses to nothing. Done when every part of the original file belongs to exactly one section.

4. **Cleanup.** Repair the transcription, not the speech, per the checklist below. Done when every section is clean and every change is logged or flagged.

5. **Structure.** Rebuild the file following the local convention or [`TEMPLATE.md`](TEMPLATE.md): header with the provenance line ("Maschinell aus einem Whisper-Transkript vorbereitet; Freigabe ausstehend"), then Extrakt, then Verlauf. Every Extrakt line is traceable to transcript text; a missing deadline becomes `[? offen]`, never invented. Done when the file matches the structure and nothing from the transcript is unaccounted for.

6. **Global pass.** Enforce the glossary everywhere; sweep the flags (every marker has a reason, none orphaned); consistent tense and formatting. Done when a grep for the flag marker lists exactly the flags the report will carry.

7. **Write in place.** Same path, no new files except the `.orig.md` from step 2. Done when the file on disk is the Protokoll.

8. **Report.** Changes by category, the **corrections log** (each Kontextfix as `falsch → richtig`), every flag with location and reason, open questions, and convention violations (e.g. a filename missing the topic slug — propose the rename, let the user decide). Done when the user can verify the risky spots from the report alone, without re-reading the transcript. The Protokoll is a draft until the human signs it.

## Cleanup checklist

- Punctuation, sentence boundaries, capitalization.
- Fillers, stutters, false starts, doubled words — removed unless they carry content.
- Crosstalk mashed into run-ons — separated or marked unintelligible.
- **Kontextfix:** repair misheard words from context when the reading is certain or near-certain — the transcript defines the term, the canonical form appears elsewhere, or the term has exactly one plausible standard rendering. Every Kontextfix goes to the corrections log; insufficient context means flag instead.
- **Repair the hearing, not the speech:** the correction target is what the speaker actually said, dialect and colloquialisms included (`abgegradet` → _upgegradet_, not "modernisiert"). Register is content; recognition errors are not.
- Flag, don't fix, for **names, numbers, dates, amounts** — the load-bearing facts a Protokoll stands on.

## Flags

One uniform, greppable marker: `[? <reason>]`, with the nearest timestamp when the transcript has one. Use for: word artifacts with no confident reading, doubts in the protected categories, suspected **Whisper hallucinations** — plausible sentences over silence, repeated boilerplate — which are flagged, never silently kept or dropped, uncertain speaker attributions, and missing deadlines.

## Speakers

Never invent a name that appears nowhere in the transcript or roster. Map generic labels (`Sprecher 1`) to names only via a roster or explicit cues in the text ("Du, Jakob, …"); inference from context is allowed, but each mapping is checked against cues, and uncertain attributions are flagged. Attendees derive from who speaks; people discussed in the third person are noted as absent, not listed as present. Uncertain identities (a relation like "meine Tochter" whose name the transcript never states) stay flagged even when context makes them plausible.
