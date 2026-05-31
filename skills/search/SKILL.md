---
name: search
description: >
  Search for multiple research reports/articles on a given investment topic,
  from diverse paradigms (sell-side, buy-side, media, bloggers).
model: sonnet
tools: ["web_search", "web_fetch"]
output_schema: report.schema.json
---

# Skill: 研报搜索

## 目标
给定一个投资标的/主题, 搜索至少3篇不同范式的研究报告或深度文章。

---

## Step 1: 确定搜索范式
至少覆盖3种不同视角:
- 券商研报(sell-side): 银河/方正/国泰/中信等
- 买方观点(buy-side): 基金公司/资管机构
- 财经媒体: Bloomberg / FT / Reuters / 华尔街见闻
- 独立研究: 知名博主 / 行业专家

## Step 2: 搜索策略
- 关键词: 标的名 + "研报" / "outlook" / "analysis" / "展望"
- 时间范围: 优先最近6个月, 确保时效性
- 语言: 中文+英文都搜
- 来源: 优先一手source(研报原文PDF > 转述文章)

## Step 3: 筛选标准
- 必须有完整论证链(不只是结论)
- 必须有数据支撑(不只是观点)
- 页数>5页(太短说明深度不够)
- 来源可信(机构研报 > 自媒体)

## Step 4: 元数据提取
每篇报告提取:
- 标题
- 机构/作者
- 发布日期
- 页数
- 核心观点(一句话)
- 下载链接/URL

## 输出
```json
{
  "topic": "白银",
  "search_date": "2026-05-31",
  "reports": [
    {
      "id": "guotai_2025Q4",
      "title": "2026年贵金属期货行情展望",
      "source_org": "国泰君安期货",
      "author": "...",
      "publish_date": "2025-12-23",
      "pages": 45,
      "url": "...",
      "file_path": null,
      "core_view": "白银主升浪正当时, 供需缺口+逼空机制驱动"
    }
  ]
}
```
