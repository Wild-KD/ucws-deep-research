# APP.md — Application Guide

## Overview

The Investment Research Logic Engine is a **Deep Research Agent** that audits investment thesis logic. It takes research reports as input and produces:

1. **Pyramid decomposition** of each report (original structure + logic-reorganized)
2. **Verification maps** with 4-color coding and clickable audit workpapers
3. **Merged consensus tree** (WHY/HOW/CONTEXT/RISK structure)
4. **Forward monitoring dashboard** tracking key indicators

## Demo: Silver Investment Thesis

The pre-computed demo analyzes why silver prices surged, using 3 Chinese research reports:

| Report | Source | Date | Pages | Perspective |
|--------|--------|------|-------|-------------|
| 贵金属期货行情展望 | 国泰君安期货 | 2025-12-23 | 45 | Futures outlook, most detailed |
| 大类资产新视角(三) | 方正证券 | 2026-01-23 | 23 | Supply-demand + historical review |
| 全球大类资产配置周报 | 中国银河证券 | 2026-01-16 | 13 | Macro weekly, financial attributes |

### Demo Outputs

| Output | Description |
|--------|-------------|
| `markmap_guotai.html` | 国泰 pyramid: original/reorganized tab switch |
| `verify_guotai.html` | 国泰 verification map: 4-color + clickable workpapers |
| `markmap_galaxy.html` | 银河 pyramid decomposition |
| `verify_galaxy.html` | 银河 verification map |
| `markmap_founder.html` | 方正 pyramid decomposition |
| `verify_founder.html` | 方正 verification map |
| `merged.html` | Merged consensus tree: WHY/HOW/CONTEXT/RISK |
| `dashboard.html` | Forward monitoring: supply-demand/spot/macro |

## Quick Start

### Option 1: View the Demo

```bash
cd agent
pip install -r requirements.txt
python main.py demo --port 8000
# Open http://localhost:8000
```

### Option 2: Run the Pipeline

```bash
# Set API keys
export ANTHROPIC_API_KEY=your_key
export TAVILY_API_KEY=your_key

# Run on silver with provided reports
python main.py run --topic "白银" --reports ../3.Demo/1.白银/白银研报/*.pdf

# Or use MiroMind
export LLM_PROVIDER=miromind
export MIROMIND_API_KEY=your_key
python main.py run --topic "白银"
```

## Architecture

See [AGENT.md](AGENT.md) for full architecture documentation.

## Technology

- **Python 3.11+** — Runtime
- **MiroMind Deep Research API** — Primary LLM provider (also supports OpenAI-compatible endpoints)
- **Tavily** — Web search for verification
- **PyMuPDF** — PDF parsing
- **markmap** — Interactive mind map visualization
- **Chart.js** — Dashboard charts
- **FastAPI** — Demo web server

## Team

**KDLD** — UCWS Singapore 2026 × MiroMind Deep Research Special Track

*A compiler for investment theses — from story to spec.*
