# Investment Research Logic Engine 投资研报逻辑审计引擎

> A compiler for investment theses — from story to spec.
> 
> 投资论点的编译器——从叙事到规约。

**Live Demo**: https://www.askmbb.com/investment/
**Public Repo**: https://github.com/Wild-KD/ucws-deep-research
**GitHub Pages**: https://wild-kd.github.io/ucws-deep-research/

---

## Repo 结构与协作说明

### 三层架构

```
┌──────────────────────────────────────────────────────┐
│  Private Repo (本仓库)                                │
│  github.com/Wild-KD/investment-research-engine        │
│  ├── 完整代码 + 部署配置 + CI/CD workflows            │
│  ├── 所有开发工作在这里进行                              │
│  └── push main → 自动触发两个 workflow:                │
│       ├── deploy.yml   → SSH 阿里云部署                │
│       └── sync-public.yml → 同步到 Public Repo        │
├──────────────────────────────────────────────────────┤
│  Public Repo (自动同步，比赛提交)                       │
│  github.com/Wild-KD/ucws-deep-research                │
│  ├── 从 Private Repo 自动 force push                  │
│  ├── GitHub Pages 静态展示                             │
│  └── 比赛表单填这个 repo 的链接                         │
├──────────────────────────────────────────────────────┤
│  Production (阿里云 HK)                               │
│  /opt/investment-engine/                              │
│  ├── 从 Private Repo 自动 git pull                    │
│  ├── PM2 进程: investment-engine (端口 9001)           │
│  ├── Nginx 反代: api.askmbb.com/investment/           │
│  └── Vercel Rewrite: www.askmbb.com/investment/       │
└──────────────────────────────────────────────────────┘
```

### 日常开发流程

```bash
# 1. 改代码（在本仓库）
# 2. push
git add -A && git commit -m "feat: xxx" && git push

# 自动发生：
#   → GitHub Actions SSH 到阿里云，git pull + pm2 restart
#   → GitHub Actions force push 到 public repo
#   → Vercel 也会自动 redeploy（如果改了 AskMBB 前端）
```

不需要手动操作服务器或 public repo。

### 手动部署（如果 CI/CD 挂了）

```bash
# SSH 到服务器
ssh -i ~/.ssh/askmbb_server admin@8.210.132.76

# 拉代码+重启
cd /opt/investment-engine && git pull && pm2 restart investment-engine

# 查看日志
pm2 logs investment-engine --lines 30
```

---

## 产品概述

所有金融 AI 都在**生成**研究报告。这个 Agent **审计**它们。

给定 N 篇研报，引擎会：
1. **搜** — 搜索 3+ 篇不同范式的研报
2. **读** — 金字塔拆解 + 逻辑重组（Minto + MECE + IB Color Code）
3. **审** — 多 Agent 并发验证每个数据节点和因果边（四色染色）
4. **合** — Storyteller 驱动的多报告合并（WHY/HOW/CONTEXT/RISK）
5. **图** — 交互式 markmap 可视化 + 验证色
6. **讲** — 前瞻监控看板（Chart.js + AI 分析）

### 核心设计原则

| 原则 | 说明 |
|------|------|
| 四色验证 | 绿(验证通过) / 金(待验证) / 红(冲突) / 黑(结构) |
| 反幻觉 | 只用报告原文数据，禁止自行计算/编造/翻译改义 |
| 验证时点 | 以报告发布日期为基准验证，不用"现在"否定"当时" |
| 多Agent扇出 | 审计步每个节点/边各一个子Agent并行验证 |
| Storyteller | 先定故事再搭结构，"对故事有没有贡献" > "数据对不对" |
| Skills即Prompt | 推理逻辑在 Markdown Skill 文件里，不埋在代码里 |

---

## 技术栈

| 层 | 选型 |
|---|---|
| LLM | Anthropic Claude (via proxy) / MiroMind / OpenAI |
| 语言 | Python 3.12 |
| Agent 框架 | 自建 BaseAgent (agentic loop + tool use) |
| Web | FastAPI + WebSocket |
| 工具 | Tavily (搜索) + httpx (抓取) + PyMuPDF (PDF) |
| 可视化 | markmap + Chart.js |
| 部署 | 阿里云 HK + PM2 + Nginx + GitHub Actions |
| 前端代理 | Vercel Rewrite (www.askmbb.com/investment/) |

---

## 项目结构

```
├── main.py                      # CLI 入口
├── server.py                    # FastAPI 生产服务器
├── config.py                    # 多 LLM 配置
├── start.sh                     # PM2 启动脚本
├── .env.example                 # 环境变量模板
│
├── agents/
│   └── research-pipeline.md     # Orchestrator Agent 定义
│
├── core/
│   ├── agent.py                 # BaseAgent: agentic loop + tool dispatch
│   └── orchestrator.py          # 六步管线编排
│
├── llm/
│   ├── base.py                  # 抽象 LLM 接口
│   ├── anthropic_provider.py    # Claude API (支持 proxy base_url)
│   ├── openai_provider.py       # OpenAI / MiroMind
│   └── factory.py               # Provider 工厂
│
├── tools/
│   ├── web_search.py            # Tavily 搜索
│   ├── web_fetch.py             # 网页抓取
│   ├── pdf_reader.py            # PDF 解析
│   ├── html_writer.py           # HTML 输出
│   └── registry.py              # 工具注册表
│
├── skills/                      # 6 个 Skill = system prompts
│   ├── search/SKILL.md          # 搜
│   ├── decompose/SKILL.md       # 读 (金字塔+反幻觉)
│   ├── verify/SKILL.md          # 审 (四色+时点原则)
│   ├── merge/SKILL.md           # 合 (Storyteller+MECE)
│   ├── visualize/SKILL.md       # 图 (markmap)
│   └── dashboard/SKILL.md       # 讲 (看板)
│
├── demo/silver/                 # 预计算白银 demo (8 HTML)
├── docs/                        # GitHub Pages + 交互页面
│
├── deploy/
│   ├── deploy.sh                # 服务器部署脚本
│   ├── ecosystem.config.js      # PM2 配置
│   └── nginx-investment.conf    # Nginx 反代配置
│
├── .github/workflows/
│   ├── deploy.yml               # Push → 自动部署阿里云
│   └── sync-public.yml          # Push → 自动同步 public repo
│
├── AGENT.md                     # 架构文档
├── SKILL.md                     # Skills 参考
└── APP.md                       # 应用指南
```

---

## 服务器信息

| 项目 | 值 |
|------|-----|
| 服务器 IP | 8.210.132.76 |
| SSH 用户 | admin |
| SSH Key | ~/.ssh/askmbb_server |
| 代码路径 | /opt/investment-engine |
| PM2 进程名 | investment-engine |
| 端口 | 9001 |
| Nginx | api.askmbb.com → location /investment/ → :9001 |
| Vercel Rewrite | www.askmbb.com/investment/ → api.askmbb.com/investment/ |
| LLM Proxy | superaichao.xin (与 AskMBB 共用) |

---

## 比赛信息

| 项目 | 值 |
|------|-----|
| 比赛 | UCWS Singapore 2026 × MiroMind Deep Research |
| 赛道 | Financial Research Agent |
| 队名 | KDLD |
| 截止 | 2026-06-01 23:59 SGT |
| 提交 Repo | https://github.com/Wild-KD/ucws-deep-research |
| Demo URL | https://www.askmbb.com/investment/ |
| GitHub Pages | https://wild-kd.github.io/ucws-deep-research/ |

### 提交清单

- [x] GitHub 公开仓库
- [x] Agent 代码 + Skills
- [x] AGENT.md / SKILL.md / APP.md
- [x] 预计算 Demo (白银, 8 HTML)
- [x] Live Demo URL
- [x] CI/CD 自动部署
- [ ] ≤3 分钟视频
- [ ] ≤200 字简介
- [ ] 截图 (PNG)

---

## Team KDLD

UCWS Singapore 2026 × MiroMind Deep Research Special Track

*Built with Claude + MiroMind API*
