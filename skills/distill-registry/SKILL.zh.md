---
name: distill-registry
description: 从验证底稿中提取所有Source，验证URL可用性，登记每个Source包含哪些数据，构建结构化的Source注册表。
model: sonnet
tools: ["web_fetch"]
---

# 沉·整：验证底稿 → Source 注册表

你收到"审"技能产出的验证底稿。从中提取所有引用过的 Source，逐个验证、登记、分类，输出一张结构化的 Source 注册表。

---

## 本技能不做的事

- 不验证数据本身（那是"审"技能已经做过的）
- 不深挖 Source 的完整数据版图（那是"沉·探"技能）
- 不判断投资主线（那是"合"技能）

---

## 第 1 步：从底稿中提取所有 Source

遍历所有验证底稿，提取每个验证项引用的 Source。

对每个 Source 记录：
- 来源名称（如 "Silver Institute World Silver Survey 2026"）
- URL
- 在哪个验证项中被引用（node_id 列表）
- 被引用时的用途（确认了什么数据）

→ 合并去重：同一个 Source 可能在多个验证项中出现，合并为一条记录。

---

## 第 2 步：分类

对每个 Source 判断类型：

| 问自己 | → 分类 |
|--------|--------|
| 它是发布原始数据的机构？（Silver Institute、CME、LBMA） | **一手数据源** |
| 它是转引别人数据的文章/报道？（财经新闻、券商转引） | **二手引用** |
| 它是行业协会/政府的统计数据？ | **官方统计** |
| 它是学术论文或研究报告？ | **研究文献** |
| 它是付费数据库？（Bloomberg Terminal、Wind） | **付费源** |

**优先级：一手数据源 > 官方统计 > 研究文献 > 二手引用**

---

## 第 3 步：验证 URL 可用性

对每个 Source 的 URL，用 `web_fetch` 检查：

| 检查项 | 结果 |
|--------|------|
| URL 能打开，内容与预期一致 | ✅ 可用 |
| URL 能打开，但内容已变（如年度报告更新了） | ⚠️ 可用但需注意版本 |
| URL 打不开（404、域名失效） | ❌ 不可用，标记需要替代 |
| URL 是付费墙 | 🔒 付费，标记为受限访问 |

---

## 第 4 步：登记每个 Source 包含哪些数据

对每个可用的一手数据源，记录它在验证过程中提供了什么数据：

```
Source: Silver Institute - World Silver Survey 2026
提供的数据:
  - 全球矿产银年产量 (Moz, 年度, 2015-2026E)
  - 工业需求分项 (Moz, 年度)
  - 光伏用银需求 (Moz, 年度)
  - 供需平衡/缺口 (Moz, 年度)
```

**注意：** 这一步只登记验证过程中**实际用到**的数据。Source 可能还有其他数据，那是"沉·探"技能的工作。

---

## 第 5 步：评估 Source 质量

对每个 Source 给一个可信度评级：

| 评级 | 标准 |
|------|------|
| **权威** | 行业公认的数据发布机构，数据被广泛引用 |
| **可靠** | 机构信誉好，数据有方法论说明，但非该领域最权威 |
| **参考** | 数据来源不够透明，或存在利益冲突，仅供参考 |

---

## 第 6 步：筛选核心判断

从验证通过的数据点中，筛选出"核心判断"：对投资主线有决定性影响的关键事实。

**筛选标准：**

→ 这个事实如果不存在，投资主线会改变吗？
  → 会：**核心判断**，必须保留
  → 不会：**支撑细节**，可以保留但不是核心

→ 这个事实能用一句话概括吗？
  → 能：适合作为核心判断
  → 不能：可能太细节了

**举例：**
- ✅ 核心判断："2021-2025年累计供需缺口消耗库存762Moz"
- ❌ 支撑细节："某矿企2025年Q3产量同比增3.2%"

---

## 输出格式

```json
{
  "report_ids": ["guotai", "galaxy", "founder"],
  "source_registry": [
    {
      "id": "src_001",
      "name": "Silver Institute - World Silver Survey 2026",
      "type": "一手数据源",
      "url": "https://...",
      "url_status": "可用",
      "reliability": "权威",
      "data_provided": [
        {
          "metric": "全球矿产银年产量",
          "unit": "Moz",
          "granularity": "年度",
          "range": "2015-2026E"
        }
      ],
      "used_in_nodes": ["T1.2", "D1.1", "D1.3"],
      "notes": "2026年4月发布，含2025实际值+2026预测"
    }
  ],
  "core_judgments": [
    {
      "id": "cj_001",
      "statement": "白银连续五年供需缺口，累计消耗库存762Moz",
      "supporting_nodes": ["T1.2", "D1.1"],
      "verification_color": "green",
      "source_ids": ["src_001"]
    }
  ],
  "summary": {
    "total_sources": 0,
    "primary": 0,
    "secondary": 0,
    "accessible": 0,
    "paywalled": 0,
    "broken": 0,
    "core_judgments_count": 0
  }
}
```
