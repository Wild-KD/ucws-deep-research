**[English](README.md)** | **中文**

# 投资侦探 Investment Detective

> AI 投资研究新范式：人类擅长深度，AI 擅长广度

**[在线 Demo](https://www.askmbb.com/investment/)** · **[白银投资 Case Journey](https://www.askmbb.com/investment/docs/demo.html)** · **[AGENT.md](AGENT.md)** · **[SKILL.md](SKILL.md)**

UCWS Singapore 2026 × MiroMind Deep Research 特别赛道 · Team KDLD

---

## 痛点

做投资研究时，你可能遇到过这样的困境：

- **无法快速且深入地了解**一个新行业、一家公司或一个投资课题。81 页的券商研报，光读完就要半天。
- AI 给你的知识点**很散、没有主线、不知道该信哪个**。更糟糕的是，你不确定 AI 说的是事实还是幻觉。

---

## 我们的方案

所有金融 AI 都在**生成**研究。这个 Agent **审计**它。

你上传几篇研报，系统帮你走完六步：

| 步骤 | 名称 | 做什么 |
|------|------|-------|
| **搜** | Search | 识别权威来源，搜索高质量研报与信息源 |
| **读** | Read | 金字塔原则严格拆解，IB Color Code 标注可信度 |
| **审** | Verify | 多 Agent 并发，既审数据来源，也审逻辑推导 |
| **沉** | Distill | 沉淀正确的核心判断与可追踪的知识资产 |
| **合** | Merge | 多篇研报合成一条逻辑主线 (MECE + Storytelling) |
| **追** | Track | 从主线导出定制化看板，持续追踪核心指标 |

最终产出不是一份报告，而是一棵**你可以逐条审查的可验证论点树**。每个数据点有来源 URL，每条逻辑推导标注了验证状态。

---

## Demo：白银投资案例

**[→ 查看完整 Demo Journey](https://www.askmbb.com/investment/docs/demo.html)**

一个研究员想搞清楚白银为什么暴涨。之前从没碰过有色金属，下载了三篇券商研报（共 81 页）。

| 研报 | 来源 | 页数 | 视角 |
|------|------|------|------|
| 贵金属期货行情展望 | 国泰君安期货 | 45 | 期货展望，最详细 |
| 大类资产新视角(三) | 方正证券 | 23 | 供需结构 + 历史复盘 |
| 全球大类资产配置周报 | 中国银河证券 | 13 | 宏观周报 |

六步之后：3 篇研报 → 3 条逻辑线 → 多 Agent 验证 → 合并为 1 条投资主线 → 定制追踪看板。

### 产出

| 产出 | 看什么 |
|------|--------|
| [国泰 · 金字塔](https://www.askmbb.com/investment/demo/silver/markmap_guotai.html) | 原文复刻 / 逻辑重组切换，IB Color Code |
| [国泰 · 验证图](https://www.askmbb.com/investment/demo/silver/verify_guotai.html) | 三色染色，点击节点看验证底稿 |
| [银河 · 金字塔](https://www.askmbb.com/investment/demo/silver/markmap_galaxy.html) | 宏观视角拆解 |
| [方正 · 金字塔](https://www.askmbb.com/investment/demo/silver/markmap_founder.html) | 供需 + 历史复盘拆解 |
| [合并投资主线](https://www.askmbb.com/investment/demo/silver/merged.html) | WHY/HOW/CONTEXT/RISK 共识树 |
| [前瞻追踪看板](https://www.askmbb.com/investment/demo/silver/dashboard.html) | 供需面/现货面/宏观面指标监控 |

---

## 核心方法论

### 投行级 Color Code

借鉴投行财务模型的颜色标注体系，一眼区分事实与判断：

- **蓝色** = 引用外部数据
- **绿色** = 假设与预测
- **黑色** = 计算结果

### 咨询业方法论

- **MECE 原则**：相互独立、完全穷尽，确保逻辑不遗漏、不重复
- **Storytelling**：把零散数据串成一条投资故事，而不是罗列事实
- **金字塔原则**：结论先行，每个标题是方向性判断

### 社科验证范式

- **数据节点验证**：每个数据独立溯源到一手来源
- **逻辑推导验证**：每条因果关系独立检验
- **多 Agent 交叉验证**：把"听起来对但经不起推敲"的幻觉筛出来
- **三色染色**：绿=验证通过、黄=待验证、红=有冲突

---

## 架构

```
标的 + 研报
      │
  Orchestrator Agent (research-pipeline.md)
      │
  01 搜 ─→ 02 读 ─→ 03 审
            (×N 篇)   │ fan-out
                    [Agent₁ Agent₂ ... Agentₙ]
                       │
         04 沉 ─→ 05 合 ─→ 06 追
      │
  交互式产出 (markmap + 验证图 + 看板)
```

- **1 个 Orchestrator Agent** 编排管线 + **8 个 Skills** 定义每步推理逻辑
- Skills 写在 Markdown 里（不是代码），评委可以直接阅读 Agent 的思考过程
- **基于 MiroMind Deep Research API**（`mirothinker-1-7-deepresearch-mini`），同时兼容 OpenAI 兼容接口

### Skills (8 个)

| Skill | 文件 | 用途 |
|-------|------|------|
| 搜 | `skills/search/SKILL.md` | 识别权威源，搜索多范式研报 |
| 读 | `skills/decompose/SKILL.md` | 金字塔拆解 + 逻辑重组 + 反幻觉 |
| 审 | `skills/verify/SKILL.md` | 多 Agent 并发验证 + 三色染色 |
| 沉·整 | `skills/distill-registry/SKILL.md` | 提取 Source，构建注册表 |
| 沉·探 | `skills/distill-explore/SKILL.md` | 深挖 Source 数据版图 |
| 合 | `skills/merge/SKILL.md` | Storyteller 合并 + MECE 重建 |
| 图 | `skills/visualize/SKILL.md` | markmap HTML 渲染 |
| 追 | `skills/dashboard/SKILL.md` | 前瞻看板生成 |

---

## 快速开始

```bash
git clone https://github.com/Wild-KD/ucws-deep-research.git
cd ucws-deep-research

pip install -r requirements.txt

cp .env.example .env
# 编辑 .env，填入 ANTHROPIC_API_KEY 或 MIROMIND_API_KEY

# 启动预计算 demo
python main.py demo

# 或运行完整管线
python main.py run --topic "白银" --reports report1.pdf report2.pdf
```

---

## Team KDLD

**UCWS Singapore 2026 × MiroMind Deep Research 特别赛道**

基于 MiroMind Deep Research API 构建

*"你不需要信任这个 Agent。你只需要看到它查了什么、发现了什么、以及什么没能验证。"*
