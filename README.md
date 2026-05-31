# Investment Research Logic Engine

> A compiler for investment theses — from story to spec.

It turns an investment narrative into a tree of falsifiable claims, tests each against the evidence, and recompiles them into a transparent thesis you can audit.

## What Makes This Different

Every financial AI agent **generates** research. This one **audits** it.

Given N research reports on any investment topic, the engine:
1. **Decomposes** each report into a Minto-style pyramid of structured claims
2. **Verifies** every data point and causal link against independent primary sources
3. **Merges** verified findings into a consensus tree (WHY / HOW / CONTEXT / RISK)
4. **Visualizes** everything as interactive mind maps with 4-color verification coding
5. **Monitors** key indicators via a forward-looking dashboard

You don't need to trust this agent. You just need to be able to see exactly what it checked, what it found, and what it couldn't verify.

## Demo

The silver case study analyzes 3 Chinese research reports (81 pages total) on why silver prices surged:

```bash
cd agent
pip install -r requirements.txt
python main.py demo
# Open http://localhost:8000
```

## Run the Pipeline

```bash
export ANTHROPIC_API_KEY=your_key    # or MIROMIND_API_KEY
export TAVILY_API_KEY=your_key

python main.py run --topic "白银" --reports report1.pdf report2.pdf report3.pdf
```

Supports three LLM providers: `anthropic` (Claude), `openai` (GPT), `miromind`.

## Architecture

```
Topic + Reports → Search → Decompose → Verify → Merge → Visualize → Dashboard
                           (×N)         (fan-out)
                                     ┌──┬──┬──┐
                                     V1 V2..VN  ← parallel sub-agents
                                     └──┴──┴──┘
```

- **6-step deterministic pipeline**, each step is an LLM agent with tools
- **Skills as system prompts** — reasoning logic in readable Markdown, not code
- **Multi-agent parallel verification** — one sub-agent per data node and causal edge
- **4-color system** — Green (verified) / Gold (unverified) / Red (conflict) / Black (structural)

See [AGENT.md](AGENT.md) for full architecture, [SKILL.md](SKILL.md) for skill details.

## Project Structure

```
agent/
├── main.py              # CLI entry point
├── server.py            # FastAPI demo server
├── config.py            # Multi-provider LLM config
├── core/
│   ├── agent.py         # BaseAgent: agentic loop with tool use
│   └── orchestrator.py  # 6-step pipeline orchestration
├── llm/
│   ├── base.py          # Abstract LLM interface
│   ├── anthropic_provider.py
│   ├── openai_provider.py    # Also serves MiroMind (OpenAI-compatible)
│   └── factory.py
├── tools/
│   ├── web_search.py    # Tavily search API
│   ├── web_fetch.py     # URL content extraction
│   ├── pdf_reader.py    # PyMuPDF PDF parsing
│   └── html_writer.py   # File output
├── skills/              # 6 Skills = system prompts
│   ├── search/SKILL.md
│   ├── decompose/SKILL.md
│   ├── verify/SKILL.md
│   ├── merge/SKILL.md
│   ├── visualize/SKILL.md
│   └── dashboard/SKILL.md
├── demo/silver/         # Pre-computed silver case demo (8 HTML files)
├── AGENT.md             # Architecture documentation
├── SKILL.md             # Skills reference
└── APP.md               # Application guide
```

## Team KDLD

UCWS Singapore 2026 × MiroMind Deep Research Special Track

*Built with Claude + MiroMind API*
