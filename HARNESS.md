# Production Harness

This harness hardens the agent runtime without changing the precomputed demo.

## What It Adds

- Robust JSON extraction from LLM outputs, including fenced JSON and prose-wrapped JSON.
- Lightweight step validation for search, pyramid, verification, and merge outputs.
- Per-run artifacts under `_artifacts/`:
  - `<step>.raw.txt`
  - `<step>.parsed.json`
  - `<step>.manifest.json`
- Deterministic `mock` LLM provider for offline smoke tests.
- Provider-aware tool message handling:
  - Anthropic uses `tool_use` / `tool_result` blocks.
  - OpenAI-compatible and MiroMind use `tool_calls` / `tool` messages.
- Node-level verification fan-out from pyramid data points and causal edges.
- Distill steps aligned with the current `搜 -> 读 -> 审 -> 沉 -> 合 -> 追` product story.
- Harness CLI for validating and parsing saved artifacts.
- HTML writer path guard so model-generated file writes stay inside the run directory.

## Offline Smoke Run

The mock provider does not call external APIs.

```bash
python main.py run --topic mock_silver --reports mock_report.pdf --provider mock --output output
```

Then validate the run:

```bash
python main.py harness validate --run-dir output/<run-name>
```

If a raw model output was saved but parsing failed, retry parsing:

```bash
python main.py harness parse-raw --run-dir output/<run-name> --step s2_pyramid_0
```

## Live Run

```bash
set LLM_PROVIDER=miromind
set MIROMIND_API_KEY=...
set TAVILY_API_KEY=...
python main.py run --topic silver --reports report1.pdf report2.pdf --provider miromind
```

Anthropic and OpenAI-compatible providers are also supported:

```bash
python main.py run --topic silver --reports report1.pdf --provider anthropic
python main.py run --topic silver --reports report1.pdf --provider openai
```

## Artifact Layout

Each run creates:

```text
output/<topic_timestamp>/
  s1_search.json
  s2_pyramid_0.json
  s3_verified_0.json
  s4_distill_registry.json
  s4_distill_explore.json
  s5_merged.json
  _artifacts/
    s1_search.raw.txt
    s1_search.parsed.json
    s1_search.manifest.json
    ...
```

The manifest captures status, validation warnings, parse errors, and metadata.

## Tests

```bash
python -m pytest tests -q
```

The tests cover JSON extraction, schema validation, artifact round-trips, mock provider behavior, OpenAI-compatible tool-message formatting, and a full mock pipeline artifact run.

## Current Boundary

This is a production-grade harness layer for reproducibility and debugging. It is not yet a full multi-user SaaS runtime. Public self-service still needs durable queues, persistent run storage, authentication, cost controls, and external observability.
