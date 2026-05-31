---
name: merge
description: >
  Merge verified pyramids from multiple reports into a single consensus tree,
  using Storyteller-driven structure (WHY/HOW/CONTEXT/RISK).
model: sonnet
tools: []
input_schema: verification.schema.json
output_schema: merged.schema.json
---

# Skill: 多报告合并

## 目标
将多篇研报的验证地图合并成一棵"共识树", 用一个清晰的故事把验证通过的内容讲给小白听。

---

## Step 0.5: 验证时点修正
合并前检查所有红色: 如果是用"现在"否定"当时" → 用报告发布时数据重新验证。

## Step 1: 剔除红色
移除验证为红的节点/边。全红子节点的父节点也剔除。

## Step 1.5: 黄色筛选
- **保留**: 对主线有贡献, 量化关键变量, 某报告核心论据
- **丢弃**: 太细节, 规模太小("供参考"), 地基不稳

## Step 2: 提取有效路径
从每份验证地图提取幸存的绿+黄节点/边。

## Step 3: 合并规则
- 同一claim多报告提及 → 取最好色(绿>黄)
- 单篇独有 → 保留并标注来源
- 数字不同 → 并列标差异, 注明各自口径

## Step 4: Storyteller — 先想清楚故事再搭结构

### 4.1 先确定故事主线
一句话: "这个故事在说什么?"
拆成3-4个主干:
- **WHY**: 为什么有结构性问题(供需基本面)
- **HOW**: 问题怎么变成了危机(现货市场机制)
- **CONTEXT**: 大背景是什么(宏观环境)
- **RISK**: 什么情况会反转(风险因素)

### 4.2 筛选: "对故事有没有贡献" > "数据对不对"
- 绿色数据不代表就该放(中国数据对但非主线→降级佐证)
- 每个节点问: "去掉它故事还完整吗?" 完整→不需要

### 4.3 为小白填跳步
- "库存低→价格涨" 要解释逼空机制(常识补充)
- "降息→利好贵金属" 要解释机会成本逻辑
- 不解释→小白卡住→故事断

### 4.4 重建金字塔
- MECE + Minto结论先行
- 每个主干有完整数据链(绝对数字, 不只百分比)
- 佐证/国别数据放对应主干下, 不单独成主干

## Step 5: 验证色继承
- 节点/边色从原始报告直接继承, 不重新验证
- 新构造的结构边标注"合并推导"
- 逆向复核: 从底往上读, 故事通不通

## Step 6: 标注来源
每个节点标注:
- 来自哪些报告(报告简称)
- 报告页码
- 验证source URL

## 输出
```json
{
  "story": "一句话故事主线",
  "merged_tree": {
    "conclusion": "...",
    "trunks": [
      { "key": "WHY", "heading": "...", "children": [...] },
      { "key": "HOW", "heading": "...", "children": [...] },
      { "key": "CONTEXT", "heading": "...", "children": [...] },
      { "key": "RISK", "heading": "...", "children": [...] }
    ]
  },
  "data_chain": {
    "supply": { "total": 1050, "unit": "Moz", "breakdown": {...} },
    "demand": { "total": 1164, "unit": "Moz", "breakdown": {...} },
    "deficit": { "total": -149, "unit": "Moz" }
  },
  "source_reports": ["guotai", "galaxy", "founder"]
}
```
