---
name: decompose
description: >
  Decompose a research report into a pyramid structure (original + logic-reorganized),
  following Minto Pyramid Principle, MECE, and IB color code conventions.
model: sonnet
tools: ["pdf_reader"]
input_schema: report.schema.json
output_schema: pyramid.schema.json
---

# Skill: 研报金字塔拆解 + 逻辑重组

## 目标
将一篇研报拆成两棵金字塔:
1. **原文复刻** — 忠实还原报告自身论证结构
2. **逻辑重组** — 按因果链重组, 补常识, 标MECE

## 前提
输入为一篇完整研报(PDF或文本)。

---

## Phase A: 原文复刻

### A1: 提取报告结构
按原文章节层级提取, 保留报告自身的组织方式。

### A2: 标注数据点
每个数据点标注:
- 报告页码
- IB Color (蓝=引用外部数据, 绿=Assumption/预测, 黑=计算结果)

---

## Phase B: 逻辑重组

### B1: 确定金字塔主干
拆成独立主干(不做串行): 宏观背景 / 核心论证 / 前瞻判断

### B2: 标题写法 — Minto 结论先行
每个标题是方向性结论, 不是分类标签。

| BAD | GOOD |
|-----|------|
| 供给端 | 供给短期收缩, 伴生矿制约增产 |
| 降息延续 | 降息延续降低贵金属持有成本 |
| 需求端 | 需求不会断崖, 光伏转型对冲装机下滑 |

### B3: MECE 拆分
- 最多4个分论点, 并列对称同一范畴
- 有因果的合并, 不并列
- 按标准框架展开(供给/需求, 近期/远期)

### B4: 节点写法
- 叶节点: [IB color加粗] 新闻导语(5W1H) + *(Source: 报告名, pXX)*
- IB Color Code:
  - **蓝 #005EB8** = 引用外部数据
  - **绿 #008800** = Assumption / 预测
  - **黑 #000000** = 计算结果
- 常识: 灰色[常识: ...], 必须有source, 可一键隐藏

### B5: 供需分析必须有完整数据链
```
供给: 矿产XXX Moz + 再生XXX Moz = 总供给XXX Moz
需求: 工业XXX + 珠宝XXX + 投资XXX = 总需求XXX Moz
平衡: 供给 - 需求 = deficit XXX Moz
```
不能只放百分比, 必须有绝对数字。多个deficit口径并列标注。

### B6: 反幻觉检查
- "读"步只能使用报告原文明确出现的数据
- 禁止: 自行换算 / 拼接 / 翻译后改义 / 编造数据
- 中文报告引用必须保持中文, 不得翻译成英文后呈现为直接引用
- 每个数据点标注报告页码, 完成后逐条核对

### B7: 逆向复核
只看标题, 能否讲完整故事? 有无跳步? 跳步处补了常识?

## 输出
```json
{
  "report_id": "...",
  "original_pyramid": { "conclusion": "...", "trunks": [...] },
  "reorganized_pyramid": { "conclusion": "...", "trunks": [...] },
  "data_points": [
    {
      "id": "S1.2",
      "content": "...",
      "ib_color": "blue|green|black",
      "source_ref": { "report": "...", "page": 36 },
      "original_text": "报告原文..."
    }
  ]
}
```
