---
name: model-params
description: >-
  Maintain scripts/model-params.json, the curated parameter-count table behind
  `oc-models-report`'s PARAM column and `--sort params`. Use when the user says
  "model params aktualisieren", "update model params", "params sync",
  "modellparameter aktualisieren", or "neue Modelle in params aufnehmen" —
  i.e. after new models appear in `oc-models-report` and need parameter totals.
---

# Model Params

Keep `scripts/model-params.json` in sync with the models that
`scripts/oc-models-report` reports. The file is the single source for the
`PARAM` column and `--sort params`; the report reads it from
`model-params.json` next to the script (override: `--params PATH` or
`$OC_MODELS_REPORT_PARAMS`).

## Workflow

1. Refresh the cached model dump:
   `scripts/oc-models-report --refresh <known-substring>` (or `--refresh
   --provider <id>`); this regenerates `~/.local/share/oc-models-report/`.
2. Get the worklist of models still lacking an entry:
   `scripts/oc-models-report --params-missing` (add `--provider ID` to scope).
   Each line is `key<TAB>providers<TAB>example-id`.
3. Research each missing key — see **Sources** and **Quality rules**.
4. Add entries under `models` in `scripts/model-params.json`. The lookup key is
   the model id's last path segment, lowercased, with a trailing `:free`
   stripped. For different spellings of the same model (e.g. `claude-opus-4-5`
   vs `claude-opus-4.5` vs `claude-opus4-5`) add one canonical `models` entry
   and map the variants in the top-level `aliases` object.
5. Smoke-test: `scripts/oc-models-report --provider <id> --sort params`.
6. Run the tests: `python3 -m unittest discover -s tests -v` (must stay green;
   `tests/test_model_params.py` lints the file).
7. Commit and push to `main` (issue-based, see `issue-workflow`).

## Data model

```json
{
  "aliases": { "claude-opus-4-5": "claude-opus-4.5" },
  "models": {
    "gpt-oss-120b":     { "total": 116.8, "active": 5.1, "source": "https://arxiv.org/html/2508.10925v1" },
    "gemini-3.5-flash": { "total": 275, "estimated": true, "source": "https://..." },
    "auto":             { "note": "Router – keine feste Parametergröße" }
  }
}
```

- `total` / `active` — billions of parameters (70 for 70B, 0.65 for 650M,
  2400 for 2.4T). `active` only for sparse/MoE models (activated per token).
- `estimated` — `true` when the number is a third-party estimate, not official.
- `source` — URL for every numeric entry.
- `note` — short reason when there is no usable number (proprietary model,
  router, non-LLM tool). A key with `note` and no `total` renders as `–`.

## Sources

- Open weights: Hugging Face model card and the HF API
  (`https://huggingface.co/api/models/<repo>?blobs=true` → `safetensors.total`),
  MoE config for the active count, plus vLLM recipes.
- Mapping provider ids to HF repos: the OpenRouter API
  (`https://openrouter.ai/api/v1/models`, field `hugging_face_id`).
- Vendors: Mistral, NVIDIA NIM, Z.AI, Moonshot, DeepSeek, Qwen, Meta, Google,
  OpenAI, Anthropic, Microsoft, Amazon, Cohere, xAI, ByteDance Seed, Tencent,
  Xiaomi, MiniMax, Upstage, Reka, Writer, Perplexity, Inception.
- Aggregators: Artificial Analysis, OpenRouter model pages.
- Note: `models.dev` (the source behind `opencode models`) has **no** parameter
  field — only `open_weights`; do not look for counts there.

## Quality rules

- Never invent a number. If no reliable figure exists, use `note`
  (e.g. `"Parameter nicht offengelegt (proprietär)"`,
  `"Router – kein festes Modell"`).
- Every numeric entry carries a `source`; mark third-party figures
  `"estimated": true`.
- Keep keys lowercase and exactly equal to the trailing path segment.
- Prefer one canonical entry plus `aliases` over duplicate entries.

## Done when

- `oc-models-report --params-missing` reports `no missing parameter entries`
  for the refreshed dump (or every remaining key has an explanatory `note`).
- `scripts/oc-models-report --provider <id> --sort params` shows sane values.
- `python3 -m unittest discover -s tests -v` is green.
- Changes are committed and pushed to `main`.
