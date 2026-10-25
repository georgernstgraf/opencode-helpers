---
name: deepseek-search
description: "Search the web via the DeepSeek Search API, falling back to a self-hosted SearXNG instance; on hosts without a DeepSeek key it runs SearXNG only (e.g. school hosts). Use when: user asks to search the web, find information, look something up, or wants current/latest sources."
metadata: { "opencode/autoinvoke": true }
---

# DeepSeek Search Skill

Web search through the **DeepSeek Search API**, with the self-hosted SearXNG
engine chain as the fallback backend. This skill is **provider-neutral and
credential-free**: it ships no key, and which providers are live is decided
entirely by the host's environment overlay (`env.sample`).

Two hosts can therefore behave differently with the same code: a private host
with a DeepSeek key searches DeepSeek first, a school host without a key
searches SearXNG only, and neither can reach the other's credentials.

> **Tool availability:** if this session has no `deepseek_search` tool, the host
> registered no `deepseek` MCP server — use the `searxng` skill's
> `searxng_search` tool instead. If it has `deepseek_search`, always prefer it:
> it routes to SearXNG itself when needed.

## Architecture

Three layers, bottom-up:

1. **DeepSeek Search API** — `POST <base>/v1/tools/search`, JSON in/out
   (provider `deepseek`). Structured hits with a model-readable `summary`,
   publication `date` and an `authority` tier.
2. **SearXNG chain** — the sibling `searxng` skill's `searxng-search.sh`
   (provider `searxng`), which owns the bing → yahoo → free → braveapi tiers
   and the instance/credential contract (`SEARXNG_*`).
3. **`scripts/opencode-deepseek-search`** — MCP stdio server (Python 3, stdlib
   only), one tool `search`, registered as `deepseek_search`.

## Environment contract

| Variable | Meaning |
|---|---|
| `DEEPSEEK_SEARCH_PROVIDERS` | Provider order, default `deepseek,searxng`. A host pins `searxng` to make the absence of DeepSeek structural. |
| `DEEPSEEK_SEARCH_API_KEY` | DeepSeek API key, direct value. |
| `DEEPSEEK_SEARCH_API_KEY_FILE` | File whose first line is the key (mode `600`). Preferred over the direct value. |
| `DEEPSEEK_SEARCH_API_BASE` | Optional API base, default `https://api.deepseek.com`. |
| `DEEPSEEK_SEARCH_TIMEOUT` | Optional request timeout in seconds, default `25`. |
| `SEARXNG_PRIMARY` / `SEARXNG_FALLBACK` (+ `_AUTH` / `_CRED_FILE`), `SEARXNG_CHAIN` | Consumed by the SearXNG fallback — same contract as the `searxng` skill. |

Rules:

- **No credential in this repo, ever.** Keys live in host-local overlays only.
- No key ⇒ the `deepseek` provider **does not exist**; the chain collapses to
  `searxng` and the envelope reports `providers_unavailable: ["deepseek"]`.
  There is no fallback path that could reach another host's token.
- No `SEARXNG_PRIMARY` ⇒ the `searxng` provider does not exist either. With
  neither configured the tool answers a clear configuration error instead of
  searching silently.

## Provider chain

The chain is walked in configured order; the first provider that answers wins.

| Situation | Behaviour |
|---|---|
| DeepSeek `200` with results | returned, `fallback_used: false` |
| `402` (balance), `408`, `429`, `5xx`, network/timeout, `bad_json` | next provider, `fallback_used: true`, `fallback_reason: "http_402"` … |
| `200` with an empty `results` array | next provider, `fallback_reason: "empty"` |
| `400` / `401` / `403` / `404` | **no** fallback — caller error, error envelope (`success: false`) |

`engines`, `category` (other than `general`), `pageno > 1` and `safesearch` are
SearXNG-only features: using any of them routes the call straight to SearXNG
without touching DeepSeek, and emits a `warnings` entry.

## Tool: `deepseek_search`

| Argument | Type | Provider | Description |
|---|---|---|---|
| `query` | string | both | Search query (required). Operators may be embedded directly. |
| `count` | integer | DeepSeek | Results to return, 1–50, default `10`. DeepSeek has no pagination. |
| `need_content` | boolean | DeepSeek | Return page content inline in the same (single, billed) request. Ignored by SearXNG. |
| `language` | string | both | Language code (`en`, `de`, …); `auto` omits the filter. DeepSeek maps it to `lang:`. |
| `time_range` | enum | both | `day`/`week`/`month`/`year`. DeepSeek maps it to `after:<date>` (**always**, strictly — undated pages drop out of a filtered search; SearXNG filters natively). |
| `site` | string | DeepSeek | `github.com` or `github.com,arxiv.org` → `site:github.com OR site:arxiv.org`. |
| `after` / `before` | string | DeepSeek | Publication-date bounds: `YYYY`, `YYYY-MM`, `YYYY-MM-DD`. |
| `category` | enum | SearXNG | `general`, `images`, `news`, `it`, `science`. Routes to SearXNG. |
| `engines` | string | SearXNG | `wikipedia,github` — routes to SearXNG and disables its chain. |
| `pageno` | integer | SearXNG | `> 1` routes to SearXNG. |
| `safesearch` | integer | SearXNG | `0`/`1`/`2`. Routes to SearXNG. |

Queries longer than **128 characters** are shortened at a word boundary,
keeping the operators, and the answer carries a `warnings` entry.

### DeepSeek query operators

| Operator | Example | Effect |
|---|---|---|
| `site:` | `site:github.com` | restrict to a site; several via `OR` |
| `-site:` | `-site:example.com` | exclude a site |
| `-term` / `-"phrase"` | `-advertisement` | exclude term / exact phrase |
| `"phrase"` | `"Gemma 4"` | exact phrase |
| `lang:` | `lang:de,en` | language filter |
| `after:` / `before:` | `after:2026-01-01` | publication-date bounds |

## Envelope

```json
{
  "success": true,
  "provider": "deepseek",
  "query": "… lang:en after:2026-04-01",
  "engine_used": "deepseek",
  "fallback_used": false,
  "fallback_reason": null,
  "providers_tried": ["deepseek"],
  "providers_unavailable": [],
  "total_results": 10,
  "results": [
    {"title": "…", "url": "…", "snippet": "…", "summary": "…",
     "date": "2026-06-01T00:00:00+00:00", "authority": 3, "rerank_score": 2.4}
  ],
  "warnings": []
}
```

Diagnostics:

- `provider` — who actually answered. `fallback_used` is **provider-level**.
- On the SearXNG path the engine chain additionally reports `engine_used`
  (`bing`/`yahoo`/…), `tried`, `unresponsive_engines`, `instance` and
  `engine_fallback_used` (engine-level; it used to be called `fallback_used`).
- `rerank_score` ≥ 1.5 and `authority` ≥ 3 mark high-quality hits.

## Cost and limits

- **$0.75 per 1 000 successful searches** ($0.00075 each). Billed per
  *request*, not per result; failures and empty result sets are free.
- Account-level QPS: **100** for DeepSeek search (SearXNG is not rate-limited
  here, but the instance's own limits and engines apply).
- The "free for harness tool calls" note in DeepSeek's docs covers DeepSeek
  Harness / Claude Code / Codex and **ended 2026-11-01** — do not rely on it.

## Freshness

For rapidly evolving topics (new models, recent releases, market data) always
pass `time_range` — `week` or `month`. Because DeepSeek filters on publication
date and not every page carries a date, a filtered DeepSeek search returns only
dated pages; if the expected sources are undated, pass `after`/`before`
explicitly or drop the filter and check the result dates.
