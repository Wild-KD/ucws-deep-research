---
name: visualize
description: >
  Generate interactive markmap HTML visualizations from pyramid/verification/merged data.
  Supports original/reorganized tab switch, 4-color verification, and clickable workpapers.
model: sonnet
tools: ["html_writer"]
input_schema: pyramid.schema.json
output_schema: null
---

# Skill: 可视化 (markmap生成)

## 目标
将结构化的金字塔数据渲染为交互式markmap HTML文件。

---

## 输出类型

### Type 1: 单报告思维导图
- 两个Tab: 原文复刻 / 逻辑重组
- 常识节点可一键隐藏
- IB Color Code 应用于文字颜色:
  - 蓝 #005EB8 = 引用外部数据
  - 绿 #008800 = Assumption
  - 黑 #000000 = 计算结果

### Type 2: 验证地图
- 节点边框/连线使用验证四色:
  - 绿 #009A44 = 验证通过
  - 金 #D4A843 = 有source未验证
  - 红 #CC0000 = 有冲突
  - 黑 #333333 = 结构/常识
- 点击节点弹出底稿面板(workpaper)
- 底稿包含: 子声明 + source URL + findings

### Type 3: 合并验证图
- WHY/HOW/CONTEXT/RISK四主干
- 验证色从原始报告继承
- 每个节点标注来源报告
- 完整供需数据链可视

## 技术要求

### markmap渲染
- 使用 markmap-lib + markmap-view CDN
- 数据格式: Markdown → markmap自动布局
- 自定义颜色函数 getNodeColor():
  - 必须处理 d3 hierarchy wrapper (node.data, 不是node.content)
  - 必须 decodeHtml() 处理HTML实体
  - 判断顺序: 常识→验证关键词→有子节点→默认

### HTML模板结构
```html
<!DOCTYPE html>
<html>
<head>
  <script src="markmap-lib CDN"></script>
  <script src="markmap-view CDN"></script>
  <!-- Tab切换CSS + 底稿面板CSS -->
</head>
<body>
  <div id="tabs">...</div>
  <svg id="markmap"></svg>
  <div id="workpaper-panel">...</div>
  <script>
    // markmap渲染 + 颜色函数 + 底稿交互
  </script>
</body>
</html>
```
