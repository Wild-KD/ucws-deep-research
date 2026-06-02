# AGENT.md — Investment Research Logic Engine

## What It Does

This agent **audits the logic of existing investment research reports** — it does not generate new research. Given N research reports on a topic, it decomposes each into a pyramid of falsifiable claims, independently verifies every data point and causal link against primary sources, and recompiles the verified findings into a transparent consensus thesis.

## Architecture

**Deterministic Pipeline + Agentic Steps + Multi-Agent Verification**

```
Input: Topic + Research Reports (PDF)
  ↓
┌──────────────────────────────────────────────┐
│           Pipeline Orchestrator              │
│                                              │
│  ① Search → ② Decompose → ③ Verify → ④ Merge → ⑤ Visualize → ⑥ Dashboard  │
│              (×N reports)    ↓ Fan-out                         │
│                          ┌──┬──┬──┐                           │
│                          V1 V2..VN  (parallel sub-agents)     │
│                          └──┴──┴──┘                           │
└──────────────────────────────────────────────┘
  ↓
Output: Interactive HTML (markmap + verification maps + dashboard)
```

### Six Steps

| Step | Name | What It Does | Tools |
|------|------|-------------|-------|
| ① | Search (搜) | Find 3+ diverse research reports | web_search, web_fetch |
| ② | Decompose (读) | Pyramid decomposition: original + logic-reorganized | pdf_reader |
| ③ | Verify (审) | Parallel sub-agents verify each data node and causal edge | web_search, web_fetch |
| ④ | Merge (合) | Storyteller-driven merge into WHY/HOW/CONTEXT/RISK tree | — |
| ⑤ | Visualize (图) | Generate interactive markmap HTML with 4-color coding | html_writer |
| ⑥ | Dashboard (讲) | Forward monitoring dashboard with latest data | web_search, web_fetch, html_writer |

### Key Design Decisions

1. **Audit, not generation.** We verify existing theses rather than generating new ones. This is the gap in the market — every other financial AI generates; none audits.

2. **Skills as system prompts.** Each step loads a SKILL.md file as its system prompt. The reasoning logic is in plain Markdown, not buried in code. Judges can read exactly how the agent thinks.

3. **Multi-agent fan-out for verification.** Step 3 spawns one sub-agent per data node and causal edge, all running in parallel. A 45-page report with 12 data nodes and 7 edges = 19 concurrent verification agents.

4. **4-color verification system.** Green (#009A44) = verified, Gold (#D4A843) = has source but unverified, Red (#CC0000) = conflicts with independent source, Black (#333) = structural/common knowledge.

5. **Verification time-point principle.** Data is verified against what was true at the report's publication date, not today. "Expectations changed" is an update, not an error.

6. **Anti-hallucination rules.** The decompose step can only use data explicitly stated in the report. No self-calculation, no unit conversion, no cross-source splicing. Every data point carries a page number.

### LLM Providers

Powered by **MiroMind Deep Research API** (`mirothinker-1-7-deepresearch-mini`). The unified provider interface also supports any OpenAI-compatible endpoint.

Switch via environment variable `LLM_PROVIDER=miromind|openai`.

## Running

```bash
# Run the full pipeline
python main.py run --topic "白银" --reports report1.pdf report2.pdf report3.pdf

# Serve the pre-computed demo
python main.py demo --port 8000
```
