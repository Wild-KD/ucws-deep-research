---
name: dashboard
description: >
  Generate a forward-looking monitoring dashboard from the merged tree,
  tracking key indicators across supply-demand, spot market, and macro dimensions.
model: sonnet
tools: ["web_search", "web_fetch", "html_writer"]
input_schema: merged.schema.json
output_schema: null
---

# Skill: 前瞻监控看板

## 目标
从合并验证图中提取核心监控指标, 搜索最新数据, 生成交互式看板HTML。

---

## Step 1: 提取监控指标
从合并树的每个主干提取可量化、可追踪的指标。

按三大框架分类:
- **供需面**: 供需平衡表, 缺口趋势, ETF持仓
- **现货面**: LBMA库存, COMEX库存, Lease Rate
- **宏观面**: FedWatch, 金银比, DXY

## Step 2: 搜索最新数据
每个指标搜索一手数据源:
- 严禁二手数据(不用研报里的图表, 要原始source)
- 必须标注数据口径和更新频率
- Source必须有URL

数据源优先级:
1. 官方机构(Silver Institute, CME, LBMA, ICE)
2. Bloomberg / Reuters
3. 行业协会

## Step 3: 看板布局
```
┌─────────────────────────────┐
│ 标的价格走势 (全宽)          │
├─────────────────────────────┤
│ Summary KPIs (一行)          │
├─────────────────────────────┤
│ 供需面: 3列                  │
├─────────────────────────────┤
│ 现货面: 3列                  │
├─────────────────────────────┤
│ 宏观面: 3列                  │
└─────────────────────────────┘
```

## Step 4: 图表要求
- 全部使用折线图(Chart.js)
- 必须有坐标轴和数据口径
- Hover显示具体数值
- 每个图表标注更新频率标签

## Step 5: AI分析
每个图表下方附两段分析:
- **YTD趋势**: 年初至今的大趋势判断
- **近期异动**: 最近的异常变动分析(如有)

## 输出
单个HTML文件, 包含:
- Chart.js CDN引用
- 全屏网格布局
- 所有图表数据内联(JSON)
- 响应式设计
