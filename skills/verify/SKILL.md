---
name: verify
description: >
  Verify every data node and causal edge in a pyramid tree independently,
  apply 4-color coding, and produce audit workpapers with source URLs.
model: sonnet
tools: ["web_search", "web_fetch"]
input_schema: pyramid.schema.json
output_schema: verification.schema.json
---

# Skill: 验证并染色

## 目标
对金字塔的每个节点和边独立验证, 根据结果上色, 留存底稿。

---

## Step 1: 节点分类

| 类型 | 判断规则 | 颜色 |
|------|---------|------|
| 结构节点 | 有子节点的纯MECE标题 | 黑色#333, 不参与验证 |
| 常识节点 | 含"常识"标记 | 黑色#333 |
| 数据节点 | 无子节点, 含数据/事实 | 绿/黄/红(待验证) |
| 结论标题 | Minto结论statement, 有子节点 | 逻辑验证后可标色 |

## Step 2: 四色体系

| 颜色 | Hex | 含义 |
|------|-----|------|
| 绿 | #009A44 | 验证通过 — 独立source确认 |
| 金 | #D4A843 | 有source但未独立验证 |
| 红 | #CC0000 | 与独立source冲突 |
| 黑 | #333333 | 结构/常识 — 不参与验证 |

**重要:** IB文字颜色(蓝/绿/黑)和验证边框色(绿/金/红/黑)是两个独立维度。
蓝色文字(引用)可以有红色验证(数据引错了)。

## Step 2.5: 验证时点原则

**验证标准: 数据在报告发布时点是否准确, 不是"现在还对不对"。**

- 报告发布时准确 → 绿色 + 附UPDATE说明当前变化
- "预期已变化"是update, 不是error
- 用当前数据否定历史数据 → 错误的验证方式

示例:
- 报告(2025.12)称"FedWatch显示2026年将降息两次"
- 2026.5月 FedWatch显示70%概率不降息
- 正确处理: 绿色(发布时数据准确) + UPDATE(预期已大幅转向)

## Step 3: 并发验证

所有数据节点和边可全部并发(每个=一个Sub Agent)。

### 数据节点验证流程
1. 提取claim(数据声明)
2. 搜索原始source(必须有URL)
3. 核对: 数据值 + 口径 + 时间范围
4. 出结论: 绿/黄/红

### 边验证(逻辑层)
1. 提取因果声明("A导致B")
2. 搜索独立证据或反例
3. 判断逻辑是否成立
4. 出结论: 绿/黄/红

## Step 4: 染色规则

- 纯MECE结构标题(供给端/需求端) → 永远黑色
- 含"常识" → 永远黑色
- Minto结论statement标题 → 逻辑验证过可标色
- 叶节点 → 按验证结果标色
- **传导规则: 父色 = 子中最好的(绿>黄>红), 黑色不参与**

## Step 5: 底稿规范

每个验证项必须包含:
1. **结论先行** — 绿/黄/红 + 一句话
2. **子声明** — 独立验证, 默认折叠展示
3. **Source** — 必须有可点击URL, 无URL的source删除
4. **原文引用** — 报告原文(中文报告保持中文)
5. **Findings** — 搜索发现的支持/反驳证据
6. 逻辑验证拆成独立项, 不笼统写"逻辑通过"

## 输出
```json
{
  "report_id": "...",
  "verify_date": "2025-12-23",
  "verifications": [
    {
      "node_id": "S1.2",
      "type": "data_node",
      "claim": "全球矿产银2025年产量846.6Moz",
      "original_text": "2025年全球矿产银产量为846.6百万盎司",
      "original_source": { "report": "guotai", "page": 36 },
      "color": "green",
      "sources": [
        {
          "url": "https://...",
          "title": "World Silver Survey 2026",
          "finding": "Confirmed: 846.6 Moz"
        }
      ],
      "update_note": null,
      "workpaper": {
        "subclaims": [...],
        "conclusion": "..."
      }
    }
  ]
}
```
