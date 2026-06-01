# SKILL.md — Skills Reference 技能参考

This agent uses **8 Skills** across a 6-step pipeline: 搜→读→审→沉→合→追. Each Skill is a Markdown file that serves as the system prompt for its pipeline step. Skills are available in both Chinese and English.

本 Agent 使用 **8 个技能**，覆盖六步管线：搜→读→审→沉→合→追。每个技能以 Markdown 文件作为对应步骤的 system prompt，支持中英双语。

## Skills Overview 技能总览

| # | Step 步骤 | Skill | File | Purpose 用途 |
|---|-----------|-------|------|-------------|
| 1 | 搜 Search | Search | `skills/search/SKILL.md` | 识别权威来源，搜索多范式研报，支持用户上传 PDF 后学习偏好并补充搜索 |
| 2 | 读 Read | Decompose | `skills/decompose/SKILL.md` | 金字塔原则严格拆解 + 逻辑重组 + IB Color Code + 反幻觉检查 |
| 3 | 审 Verify | Verify | `skills/verify/SKILL.md` | 多 Agent 并发验证数据节点与因果边 + 三色染色 + 底稿规范 |
| 4 | 沉·整 Distill | Distill Registry | `skills/distill-registry/SKILL.md` | 提取 Source 注册表 + 验证 URL + 筛选核心判断 |
| 5 | 沉·探 Distill | Distill Explore | `skills/distill-explore/SKILL.md` | 深挖 Source 数据版图 + 发现研报遗漏的数据维度 |
| 6 | 合 Merge | Merge | `skills/merge/SKILL.md` | Storyteller 驱动的多报告合并 (WHY/HOW/CONTEXT/RISK) |
| 7 | 图 Visualize | Visualize | `skills/visualize/SKILL.md` | 交互式 markmap HTML 渲染（跨读/审/合三步复用） |
| 8 | 追 Track | Dashboard | `skills/dashboard/SKILL.md` | 前瞻监控看板，从沉步 Source 注册表拉最新数据 |

## Core Methodology 核心方法论

### Minto Pyramid Principle 金字塔原则 (Skills 2, 6)

Every heading is a directional conclusion, not a category label.

每个标题是方向性结论，不是分类标签。

| BAD | GOOD |
|-----|------|
| Supply side 供给端 | Supply contracts short-term as by-product mining constrains expansion 供给短期收缩，伴生矿制约增产 |

### MECE (Skills 2, 6)

Max 4 sub-points per level. Parallel and symmetric. Causal chains merge, never sit in parallel.

每层最多 4 个分论点，并列对称。有因果关系的合并，不并列。

### IB Color Code 投行颜色标注 (Skill 2)

Text color indicates data provenance:

| Color 颜色 | Hex | Meaning 含义 |
|------------|-----|-------------|
| **Blue 蓝** | #005EB8 | External reference 引用外部数据 |
| **Green 绿** | #008800 | Assumption / forecast 假设与预测 |
| **Black 黑** | #000000 | Calculated result 计算结果 |

### Verification 3-Color System 三色验证 (Skill 3)

| Color 颜色 | Hex | Meaning 含义 |
|------------|-----|-------------|
| **Green 绿** | #009A44 | Verified 验证通过 |
| **Gold 黄** | #D4A843 | Has source, unverified 有来源但未独立验证 |
| **Red 红** | #CC0000 | Conflict 与独立来源冲突 |

### Anti-Hallucination 反幻觉 (Skills 2, 3)

- Only use data explicitly in the original report text 只用报告原文数据
- No self-calculation, unit conversion, or cross-source splicing 禁止自行计算/换算/拼接
- Chinese report quotes must stay in Chinese 中文报告引用保持中文
- Every data point must carry a page number 每个数据标页码
- Every verification source must have a clickable URL 每个来源必须有可点击 URL

### Verification Time-Point Principle 验证时点原则 (Skills 3, 6)

Verify data against what was true at the report's publication date, not today.

以报告发布时点为基准验证，不用"现在"否定"当时"。

### Storyteller Principle 叙事原则 (Skill 6)

Before merging, determine the story. "Does it contribute to the story?" outranks "Is it correct?"

合并前先定故事。"对故事有没有贡献" > "数据对不对"。

Structure: **WHY** (fundamentals) / **HOW** (mechanism) / **CONTEXT** (macro) / **RISK**

### Source Distillation 数据源沉淀 (Skills 4, 5)

Two-phase distillation after verification:

验证后分两步沉淀：

1. **Registry 整理** — Extract sources, verify URLs, catalog what data each provides, filter core judgments
2. **Explore 探索** — Deep-dive each primary source, map its full data landscape, discover dimensions the reports missed
