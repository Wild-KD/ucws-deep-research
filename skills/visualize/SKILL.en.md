---
name: visualize
description: Render pyramid, verification, and merge data into interactive markmap HTML, supporting original/reorganized tab switching, four-color verification, and clickable working papers.
model: sonnet
tools: ["html_writer"]
---

# Visualize: Structured Data → Interactive Markmap HTML

You receive pyramid data (from the "Decompose" or "Merge" skill). Render it as an interactive markmap mind-map HTML file.

---

## What This Skill Does NOT Do

- Does not decompose or verify data (those are the "Decompose" and "Verify" skills)
- Does not modify data content — only handles visual presentation

---

## Step 1: Determine the Output Type

Based on the input data, decide which visualization to generate:

| Input | Output Type | Key Features |
|-------|-------------|-------------|
| Single-report pyramid (original + reorganized) | **Decomposition Map** | Two tabs to switch: Original / Reorganized; common knowledge hide button |
| Single-report verification results | **Verification Map** | Four-color coded lines/borders; click a node to open the working paper panel |
| Post-merge consensus tree | **Merge Map** | WHY / HOW / CONTEXT / RISK four trunks; source annotations; data chain |

---

## Step 2: Build the Markdown Data

markmap accepts Markdown format as input. Convert the structured JSON into Markdown hierarchy:

```markdown
# Root Conclusion

## Trunk 1 Heading

### Sub-argument 1.1 Heading

- <span style="color:#005EB8">**Data content**</span> *(Source p.36)*

### Sub-argument 1.2 Heading

- <span style="color:#008800">**Forecast content**</span> *(Source p.42)*
- *[Common Knowledge] Explanation text*

## Trunk 2 Heading
...
```

**Rules:**
- IB colors use `<span style="color:XXX">` inline styles
- Common knowledge nodes are marked with italics
- Source annotations use `*(italic parentheses)*`

---

## Step 3: Implement the Color Function (Verification Map Only)

The verification map requires a custom `getNodeColor()` function to control line/border colors:

```javascript
function getNodeColor(node) {
  // 1. Get node text (markmap uses d3 hierarchy wrapper)
  var raw = findContent(node, 0);  // needs to traverse node.data
  var text = decodeHtml(raw.replace(/<[^>]*>/g, ''));
  
  // 2. Check in this exact order (order matters)
  if (text.includes('Common Knowledge')) return '#333333';  // Common Knowledge → black
  if (text.includes('Verified'))         return '#009A44';  // → green
  if (text.includes('Unverified'))       return '#D4A843';  // → gold
  if (text.includes('Conflicted'))       return '#CC0000';  // → red
  if (hasKids(node))                     return '#333333';  // has children → black (structural)
  return '#D4A843';                                         // default → gold
}
```

**Critical technical details:**
- markmap passes d3 hierarchy nodes to the color function; data is in `node.data`, not `node.content`
- markmap stores content as HTML entities (e.g., `&#x5e38;&#x8bc6;` = Chinese characters for "common knowledge") — you must use `decodeHtml()` to decode before keyword matching
- The `findContent` function needs to recursively traverse `obj.data || obj.v || obj.content`

---

## Step 4: Implement the Working Paper Panel (Verification Map Only)

In the verification map, clicking a node should open a working paper panel displaying verification details:

### Panel Content
```
┌─────────────────────────────────┐
│ 🟢 Verified                     │
│                                 │
│ Claim: Mine silver production   │
│ 846.6 Moz                      │
│ Original text: (original text)  │
│                                 │
│ ▸ Sub-claim 1 — ✅ Verified     │
│   Source: [clickable URL]       │
│   Finding: Confirmed 846.6 Moz │
│                                 │
│ ▸ Sub-claim 2 — ✅ Verified     │
│   Source: [clickable URL]       │
│   Finding: WSS 2026 data       │
│   consistent                    │
│                                 │
│ UPDATE: 2026 mine silver        │
│ projected to reach ~855 Moz    │
└─────────────────────────────────┘
```

### Interaction Behavior
- Click a node → panel slides in (from right or bottom)
- Sub-claims are collapsed by default; click to expand
- Source URLs must be clickable and open in a new tab
- Click outside the panel or press ESC to close

---

## Step 5: Build the HTML

Use the following CDN resources:
```html
<script src="https://cdn.jsdelivr.net/npm/d3@7"></script>
<script src="https://cdn.jsdelivr.net/npm/markmap-view"></script>
<script src="https://cdn.jsdelivr.net/npm/markmap-lib"></script>
```

### HTML Structure
```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <!-- CDN scripts -->
  <!-- Styles: tab switching + working paper panel + common knowledge button -->
</head>
<body>
  <!-- Tab buttons (for Decomposition Map) -->
  <div id="tabs">
    <button onclick="switchTab('original')">Original</button>
    <button onclick="switchTab('reorganized')">Reorganized</button>
  </div>
  
  <!-- Common Knowledge toggle button -->
  <button id="toggleCK">Hide Common Knowledge</button>
  
  <!-- markmap container -->
  <svg id="markmap" style="width:100%;height:calc(100vh - 60px)"></svg>
  
  <!-- Working paper panel (for Verification Map) -->
  <div id="workpaper-panel">...</div>
  
  <script>
    // markmap data + rendering + color function + working paper data + interactions
  </script>
</body>
</html>
```

---

## Step 6: Quality Check

After generating the HTML, verify:

| Check Item | If Failed |
|------------|-----------|
| All CDN links load successfully? | Switch to backup CDN or check URLs |
| Color function returns black for common knowledge nodes? | Fix decodeHtml |
| Tab switching works correctly? | Check data binding |
| Working paper panel URLs are clickable? | Verify `<a href>` is correct |
| Content displays correctly? | Confirm charset=UTF-8 |
| Full-screen display without scrollbar issues? | Check CSS height |

---

## Output

Use `html_writer` to write the HTML to the specified path. Each report produces 1–2 HTML files.
