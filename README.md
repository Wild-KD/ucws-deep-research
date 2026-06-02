**English** | **[中文](README_CN.md)**

# Investment Detective 投资侦探

> A new paradigm for investment research: humans go deep, AI goes wide.

**[Live Demo](https://www.askmbb.com/investment/)** · **[Silver Case Journey](https://www.askmbb.com/investment/docs/demo.html)** · **[AGENT.md](AGENT.md)** · **[SKILL.md](SKILL.md)**

UCWS Singapore 2026 × MiroMind Deep Research Special Track · Team KDLD

---

## The Problem

When doing investment research, you've probably faced this:

- You **can't quickly AND deeply understand** a new sector, company, or investment thesis. An 81-page broker report takes half a day just to read.
- AI gives you scattered facts with **no thesis, no logic chain, and no way to tell what's real** from what's hallucinated.

---

## Our Approach

Every financial AI **generates** research. This one **audits** it.

Upload a few research reports, and the system walks you through six steps:

| Step | Name | What it does |
|------|------|-------------|
| **搜** | Search | Identify authoritative sources, collect high-quality reports across paradigms |
| **读** | Read | Pyramid-principle decomposition with IB Color Code credibility tagging |
| **审** | Verify | Multi-agent concurrent verification of both data sources and logical reasoning |
| **沉** | Distill | Distill core judgments and build a trackable knowledge asset registry |
| **合** | Merge | Merge multiple reports into one coherent investment thesis (MECE + Storytelling) |
| **追** | Track | Generate a custom dashboard to continuously monitor key indicators |

The output is not a report. It's a **verifiable thesis tree** where every data point has a source URL and every causal link is tagged with its verification status.

---

## Demo: Silver Investment Case

**[→ View the full Demo Journey](https://www.askmbb.com/investment/docs/demo.html)**

A researcher wants to understand why silver surged. Never studied metals before. Downloaded 3 Chinese broker reports (81 pages total).

| Report | Source | Pages | Perspective |
|--------|--------|-------|------------|
| Precious Metals Futures Outlook | Guotai Junan Futures | 45 | Futures, most detailed |
| New Perspectives on Asset Allocation (III) | Founder Securities | 23 | Supply-demand + historical review |
| Global Asset Allocation Weekly | Galaxy Securities | 13 | Macro weekly |

After six steps: 3 reports → 3 logic lines → multi-agent verification → 1 merged thesis → tracking dashboard.

### Demo Outputs

| Output | What you'll see |
|--------|----------------|
| [Guotai · Pyramid](https://www.askmbb.com/investment/demo/silver/markmap_guotai.html) | Original / reorganized toggle, IB Color Code |
| [Guotai · Verification](https://www.askmbb.com/investment/demo/silver/verify_guotai.html) | 3-color coding, click nodes for audit workpapers |
| [Galaxy · Pyramid](https://www.askmbb.com/investment/demo/silver/markmap_galaxy.html) | Macro perspective decomposition |
| [Founder · Pyramid](https://www.askmbb.com/investment/demo/silver/markmap_founder.html) | Supply-demand + history decomposition |
| [Merged Thesis](https://www.askmbb.com/investment/demo/silver/merged.html) | WHY/HOW/CONTEXT/RISK consensus tree |
| [Tracking Dashboard](https://www.askmbb.com/investment/demo/silver/dashboard.html) | Supply-demand / spot / macro indicator monitoring |

---

## Core Methodology

### IB Financial Model Color Code

Borrowed from investment banking financial models to instantly distinguish fact from judgment:

- **Blue** = External reference data
- **Green** = Assumption / forecast
- **Black** = Calculated result

### Consulting Methodology

- **MECE Principle**: Mutually exclusive, collectively exhaustive — no gaps, no overlaps
- **Storytelling**: Weave scattered data points into a compelling investment narrative
- **Pyramid Principle**: Conclusion first — every heading is a directional judgment

### Social Science Verification Paradigm

- **Data node verification**: Every data point independently traced to primary sources
- **Logic verification**: Every causal link independently examined
- **Multi-agent cross-verification**: Filter out "sounds right but doesn't hold up" hallucinations
- **3-color coding**: Green = verified, Yellow = unverified, Red = conflicting

---

## Skills: The Core of the Project

**The 8 Skills ARE the product.** Each Skill is a structured Markdown file that encodes a specific research methodology. They are human-readable, bilingual (Chinese + English), and portable across any LLM provider.

| # | Skill | File | What it encodes |
|---|-------|------|-----------------|
| 1 | **Search** | `skills/search/SKILL.{zh,en}.md` | Multi-round authority-source identification, analyst pre-research, diversity checks |
| 2 | **Decompose** | `skills/decompose/SKILL.{zh,en}.md` | 9-step Minto pyramid extraction, MECE 5-step checklist, IB Color Code, anti-hallucination |
| 3 | **Verify** | `skills/verify/SKILL.{zh,en}.md` | Node-level data verification, causal-edge logic testing, 3-color coding, time-point principle |
| 4 | **Distill Registry** | `skills/distill-registry/SKILL.{zh,en}.md` | Source extraction, URL validation, core judgment filtering |
| 5 | **Distill Explore** | `skills/distill-explore/SKILL.{zh,en}.md` | Source data-landscape mapping, gap discovery, tracking recommendations |
| 6 | **Merge** | `skills/merge/SKILL.{zh,en}.md` | 10-step Storyteller merge, WHY/HOW/CONTEXT/RISK, color inheritance |
| 7 | **Visualize** | `skills/visualize/SKILL.{zh,en}.md` | markmap rendering, verification-color functions, workpaper panels |
| 8 | **Dashboard** | `skills/dashboard/SKILL.{zh,en}.md` | 3-framework indicator extraction, Chart.js generation, YTD + anomaly analysis |

Each Skill can be read directly — open any `SKILL.en.md` file and you'll see exactly how the agent reasons, step by step, with decision branches and verification tables. No code required.

## Architecture

The Skills are orchestrated by a lightweight pipeline runner. The runner is intentionally thin — the reasoning logic lives entirely in the Skills.

```
Topic + Reports
      │
  Pipeline Runner (loads Skills as system prompts)
      │
  Skill 1: Search ─→ Skill 2: Decompose ─→ Skill 3: Verify
                       (×N reports)            │ fan-out per node
                                           [Agent₁ Agent₂ ... Agentₙ]
                                               │
                 Skill 4-5: Distill ─→ Skill 6: Merge ─→ Skill 8: Dashboard
      │
  Interactive Outputs (Skill 7: Visualize)
```

- **8 Skills** define all reasoning logic in readable Markdown
- **1 Pipeline Runner** chains Skills and manages concurrency
- **Powered by MiroMind Deep Research API** (`mirothinker-1-7-deepresearch-mini`); also supports OpenAI-compatible endpoints

---

## Quick Start

```bash
git clone https://github.com/Wild-KD/ucws-deep-research.git
cd ucws-deep-research

pip install -r requirements.txt

cp .env.example .env
# Edit .env: add your MIROMIND_API_KEY (get one at platform.miromind.ai)

# Serve the pre-computed demo
python main.py demo

# Or run the full pipeline
python main.py run --topic "silver" --reports report1.pdf report2.pdf
```

---

## Team KDLD

**UCWS Singapore 2026 × MiroMind Deep Research Special Track**

Powered by MiroMind Deep Research API

*"You don't need to trust this agent. You just need to see what it checked, what it found, and what it couldn't verify."*
