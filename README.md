# Investment Research Logic Engine 投资研报逻辑审计引擎

> A compiler for investment theses — from story to spec.
> 
> 投资论点的编译器——从叙事到规约。

[**Live Demo 在线演示**](https://wild-kd.github.io/investment-research-engine/) · [AGENT.md](AGENT.md) · [SKILL.md](SKILL.md) · [APP.md](APP.md)

---

## What Makes This Different 为什么不一样

Every financial AI agent **generates** research. This one **audits** it.

所有金融AI都在**生成**研究报告。这个Agent**审计**它们。

Given N research reports on any investment topic, the engine:

给定任意投资标的的N篇研报，引擎会：

1. **Decomposes 拆解** — Extract each report into a Minto-style pyramid of structured claims  
   将每篇研报拆解为金字塔结构的可证伪声明
2. **Verifies 验证** — Independently verify every data point and causal link against primary sources  
   对每个数据节点和因果链进行独立溯源验证
3. **Merges 合并** — Combine verified findings into a consensus tree (WHY / HOW / CONTEXT / RISK)  
   将验证通过的内容合并为共识树（为什么/怎么发生/大背景/风险）
4. **Visualizes 可视化** — Render interactive mind maps with 4-color verification coding  
   生成带四色验证标注的交互式思维导图
5. **Monitors 监控** — Track key indicators via a forward-looking dashboard  
   通过前瞻看板追踪核心指标

> You don't need to trust this agent. You just need to see exactly what it checked, what it found, and what it couldn't verify.
> 
> 你不需要信任这个Agent。你只需要能看到它查了什么、发现了什么、以及什么没能验证。

---

## Architecture 架构

```
Topic + Reports  标的 + 研报
      ↓
┌──────────────────────────────────────────────────────┐
│              Orchestrator Agent  编排Agent             │
│                                                       │
│  ① 搜 Search  →  ② 读 Decompose  →  ③ 审 Verify     │
│                    (×N reports)       ↓ fan-out        │
│                                   ┌──┬──┬──┐          │
│                                   V1 V2..VN           │
│                                   (parallel)          │
│                                   └──┴──┴──┘          │
│                                       ↓               │
│              ④ 合 Merge  →  ⑤ 图 Visualize  →  ⑥ 讲 Dashboard  │
└──────────────────────────────────────────────────────┘
      ↓
Interactive HTML Outputs  交互式HTML产出
```

### Pipeline Steps 管线六步

| Step | Name | What it does | 做什么 |
|------|------|-------------|--------|
| ① | Search 搜 | Find 3+ diverse reports across paradigms | 搜索3+篇不同范式的研报 |
| ② | Decompose 读 | Minto pyramid extraction + logic reorganization | 金字塔拆解 + 逻辑重组 |
| ③ | Verify 审 | Multi-agent parallel verification + 4-color coding | 多Agent并发验证 + 四色染色 |
| ④ | Merge 合 | Storyteller-driven cross-report consensus tree | 叙事驱动的多报告共识树 |
| ⑤ | Visualize 图 | Interactive markmap with verification colors | 交互式markmap + 验证色 |
| ⑥ | Dashboard 讲 | Forward monitoring with key indicators | 前瞻监控看板 |

### Key Design Principles 核心设计原则

- **Skills as system prompts 技能即提示词** — Reasoning logic lives in readable Markdown, not buried in code. 推理逻辑写在可读的Markdown里，不埋在代码里。
- **Multi-agent fan-out 多Agent扇出** — Step 3 spawns one sub-agent per data node and causal edge (19 concurrent agents for a 45-page report). 审计步每个数据节点和因果边各一个子Agent并行验证。
- **4-color system 四色体系** — Green (#009A44 verified) / Gold (#D4A843 unverified) / Red (#CC0000 conflict) / Black (#333 structural). 绿=验证通过 / 金=待验证 / 红=有冲突 / 黑=结构节点。
- **Anti-hallucination 反幻觉** — Decompose step only uses data explicitly in the report. No self-calculation, no fabrication. 拆解步只用报告原文数据，禁止自行计算或编造。
- **Verification time-point 验证时点** — Data verified against what was true at report publication date, not today. 以报告发布时点验证数据，不用"现在"否定"当时"。

---

## Demo 演示

### Live Demo 在线演示

**https://wild-kd.github.io/investment-research-engine/**

Silver (白银) case study — 3 Chinese research reports (81 pages total):

白银案例——3篇中国券商研报（共81页）：

| Report 研报 | Source 来源 | Pages 页数 | Perspective 视角 |
|-------------|-----------|-----------|-----------------|
| 贵金属期货行情展望 | 国泰君安期货 | 45 | Futures outlook 期货展望 |
| 大类资产新视角(三) | 方正证券 | 23 | Supply-demand + history 供需+历史 |
| 全球大类资产配置周报 | 中国银河证券 | 13 | Macro weekly 宏观周报 |

### Run Locally 本地运行

```bash
# Serve pre-computed demo  启动预计算演示
pip install -r requirements.txt
python main.py demo
# Open http://localhost:8000

# Run the full pipeline  运行完整管线
export ANTHROPIC_API_KEY=your_key    # or MIROMIND_API_KEY
export TAVILY_API_KEY=your_key
python main.py run --topic "白银" --reports report1.pdf report2.pdf
```

Supports three LLM providers 支持三种LLM: `anthropic` (Claude) · `openai` (GPT) · `miromind`

---

## Project Structure 项目结构

```
├── main.py                      # CLI entry point  命令行入口
├── server.py                    # FastAPI demo server  演示服务器
├── config.py                    # Multi-provider LLM config  多LLM配置
│
├── agents/
│   └── research-pipeline.md     # Orchestrator agent  编排Agent
│
├── core/
│   ├── agent.py                 # BaseAgent: agentic loop + tool use  Agent循环
│   └── orchestrator.py          # 6-step pipeline orchestration  六步编排
│
├── llm/
│   ├── base.py                  # Abstract LLM interface  抽象接口
│   ├── anthropic_provider.py    # Claude API
│   ├── openai_provider.py       # OpenAI / MiroMind (compatible)
│   └── factory.py               # Provider factory  工厂函数
│
├── tools/
│   ├── web_search.py            # Tavily search  联网搜索
│   ├── web_fetch.py             # URL content extraction  网页抓取
│   ├── pdf_reader.py            # PyMuPDF PDF parsing  PDF解析
│   └── html_writer.py           # File output  文件输出
│
├── skills/                      # 6 Skills = system prompts  6个技能
│   ├── search/SKILL.md          # 搜: find reports
│   ├── decompose/SKILL.md       # 读: pyramid + anti-hallucination
│   ├── verify/SKILL.md          # 审: 4-color + time-point principle
│   ├── merge/SKILL.md           # 合: storyteller + MECE
│   ├── visualize/SKILL.md       # 图: markmap generation
│   └── dashboard/SKILL.md       # 讲: forward dashboard
│
├── demo/silver/                 # Pre-computed demo  预计算演示 (8 HTML files)
├── docs/                        # GitHub Pages deployment
│
├── AGENT.md                     # Architecture doc  架构文档
├── SKILL.md                     # Skills reference  技能参考
└── APP.md                       # Application guide  应用指南
```

---

## Team KDLD 团队

**UCWS Singapore 2026 × MiroMind Deep Research Special Track**

*Built with Claude + MiroMind API*

---

## License

MIT
