---
name: visualize
description: 将金字塔/验证/合并数据渲染为交互式 markmap HTML，支持原文/重组切换、四色验证、可点击底稿。
model: sonnet
tools: ["html_writer"]
---

# 图：结构化数据 → 交互式 markmap HTML

你收到金字塔数据（来自"读"或"合"技能）。将其渲染为可交互的 markmap 思维导图 HTML 文件。

---

## 本技能不做的事

- 不拆解或验证数据（那是"读"和"审"技能）
- 不修改数据内容——只负责可视化呈现

---

## 第 1 步：确定输出类型

根据输入数据，判断生成哪种可视化：

| 输入 | 输出类型 | 关键特性 |
|------|---------|---------|
| 单报告金字塔（原文+重组） | **拆解图** | 两个 Tab 切换：原文/重组；常识隐藏按钮 |
| 单报告验证结果 | **验证图** | 四色染色线条/边框；点击节点弹出底稿面板 |
| 合并后共识树 | **合并图** | WHY/HOW/CONTEXT/RISK 四主干；来源标注；数据链 |

---

## 第 2 步：构建 Markdown 数据

markmap 接受 Markdown 格式输入。将结构化 JSON 转为 Markdown 层级：

```markdown
# 根结论

## 主干1标题

### 分论点1.1标题

- <span style="color:#005EB8">**数据内容**</span> *(来源 p.36)*

### 分论点1.2标题

- <span style="color:#008800">**预测内容**</span> *(来源 p.42)*
- *[常识] 解释文字*

## 主干2标题
...
```

**规则：**
- IB 颜色用 `<span style="color:XXX">` 内联样式
- 常识节点用斜体标记
- 来源标注用 `*(斜体括号)*`

---

## 第 3 步：实现颜色函数（验证图专用）

验证图需要自定义 `getNodeColor()` 函数控制线条/边框颜色：

```javascript
function getNodeColor(node) {
  // 1. 获取节点文本（markmap 使用 d3 hierarchy 包装）
  var raw = findContent(node, 0);  // 需要遍历 node.data
  var text = decodeHtml(raw.replace(/<[^>]*>/g, ''));
  
  // 2. 判断顺序（不能乱）
  if (text.includes('常识')) return '#333333';      // 常识 → 黑色
  if (text.includes('验证通过')) return '#009A44';   // → 绿色
  if (text.includes('待验证')) return '#D4A843';     // → 金色
  if (text.includes('有冲突')) return '#CC0000';     // → 红色
  if (hasKids(node)) return '#333333';              // 有子节点 → 黑色（结构）
  return '#D4A843';                                  // 默认 → 金色
}
```

**关键技术细节：**
- markmap 传给颜色函数的是 d3 hierarchy 节点，数据在 `node.data`，不是 `node.content`
- markmap 存储内容为 HTML 实体（如 `&#x5e38;&#x8bc6;` = 常识），必须用 `decodeHtml()` 解码后才能做关键词匹配
- `findContent` 函数需要递归遍历 `obj.data || obj.v || obj.content`

---

## 第 4 步：实现底稿面板（验证图专用）

验证图中点击节点需要弹出底稿面板，显示验证详情：

### 面板内容
```
┌─────────────────────────────┐
│ 🟢 验证通过                  │
│                             │
│ 声明：矿产银产量846.6Moz     │
│ 报告原文：（中文原文）         │
│                             │
│ ▸ 子声明 1 — ✅ 已验证        │
│   来源：[可点击URL]           │
│   发现：确认846.6Moz          │
│                             │
│ ▸ 子声明 2 — ✅ 已验证        │
│   来源：[可点击URL]           │
│   发现：WSS 2026数据一致      │
│                             │
│ UPDATE：2026年矿产银预计增至  │
│ ~855Moz                     │
└─────────────────────────────┘
```

### 交互行为
- 点击节点 → 面板滑入（从右侧或底部）
- 子声明默认折叠，点击展开
- Source URL 必须可点击跳转
- 点击面板外或按 ESC 关闭

---

## 第 5 步：构建 HTML

使用以下 CDN：
```html
<script src="https://cdn.jsdelivr.net/npm/d3@7"></script>
<script src="https://cdn.jsdelivr.net/npm/markmap-view"></script>
<script src="https://cdn.jsdelivr.net/npm/markmap-lib"></script>
```

### HTML 结构
```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <!-- CDN scripts -->
  <!-- 样式：Tab切换 + 底稿面板 + 常识按钮 -->
</head>
<body>
  <!-- Tab 按钮（拆解图用） -->
  <div id="tabs">
    <button onclick="switchTab('original')">原文复刻</button>
    <button onclick="switchTab('reorganized')">逻辑重组</button>
  </div>
  
  <!-- 常识切换按钮 -->
  <button id="toggleCK">隐藏常识</button>
  
  <!-- markmap 容器 -->
  <svg id="markmap" style="width:100%;height:calc(100vh - 60px)"></svg>
  
  <!-- 底稿面板（验证图用） -->
  <div id="workpaper-panel">...</div>
  
  <script>
    // markmap 数据 + 渲染 + 颜色函数 + 底稿数据 + 交互
  </script>
</body>
</html>
```

---

## 第 6 步：质检

生成 HTML 后检查：

| 检查项 | 不通过则 |
|--------|---------|
| 所有 CDN 链接能加载？ | 换备用 CDN 或检查 URL |
| 颜色函数对常识节点返回黑色？ | 修复 decodeHtml |
| Tab 切换正常？ | 检查 data 绑定 |
| 底稿面板的 URL 可点击？ | 确认 `<a href>` 正确 |
| 中文内容显示正常？ | 确认 charset=UTF-8 |
| 全屏显示无滚动条问题？ | 检查 CSS height |

---

## 输出

使用 `html_writer` 将 HTML 写入指定路径。每个报告产出 1-2 个 HTML 文件。
