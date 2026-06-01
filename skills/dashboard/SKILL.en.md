---
name: dashboard
description: Determine tracking targets based on the investment thesis, pull latest data from the Source Registry produced in the Distill step, and generate a customized tracking dashboard.
model: sonnet
tools: ["web_search", "web_fetch", "html_writer"]
---

# Dashboard: Investment Thesis + Source Registry → Customized Tracking Dashboard

You receive two inputs:
1. **Merged Consensus Tree** (output of the "Merge" skill) — tells you what logic to track
2. **Source Registry** (output of the "Distill-Registry" skill) — tells you where to pull data from

Based on the investment thesis, determine the core indicators that need tracking, pull the latest data from primary sources registered in the Source Registry, and generate a dashboard for ongoing monitoring.

---

## What This Skill Does NOT Do

- Does not re-analyze investment logic (that is the "Merge" skill)
- Does not use secondary data (does not use charts from research reports — pulls from primary sources in the Source Registry)
- Does not generate investment advice
- Does not invent what to track — tracking targets are derived from the investment thesis

---

## Step 1: Extract Monitoring Indicators

From each trunk of the merged tree, extract quantifiable, continuously trackable indicators.

### 1.1 Classify by Three Frameworks

| Framework | What It Covers | Typical Indicators |
|-----------|---------------|-------------------|
| **Supply-Demand** | Fundamental data | Supply-demand balance table, deficit trend, ETF holdings |
| **Spot Market** | Market microstructure | Exchange inventory, Lease Rate, positioning data |
| **Macro** | External environment | Rate expectations, FX rates, cross-asset ratios |

### 1.2 Select 3 Core Indicators per Framework

→ Approximately 9 total. Do not overload.
→ Selection criteria: does a change in this indicator directly impact a core argument in the merged tree?

### 1.3 Record Metadata for Each Indicator

| Field | Required |
|-------|----------|
| Indicator name | ✅ |
| Data scope/methodology description | ✅ |
| Primary data source (institution name) | ✅ |
| Update frequency (daily / weekly / monthly / quarterly / annual) | ✅ |
| Source URL | ✅ |
| Unit | ✅ |

---

## Step 2: Pull Latest Data from the Source Registry

**Prioritize sources already registered in the "Distill-Registry" step.** Do not re-search — the Distill step has already verified URLs and registered data dimensions.

### 2.1 Data Pull Sequence

1. **Check the Source Registry first**: Is the source for this indicator already registered? Is the URL still valid?
   → Registered and accessible → directly `web_fetch` the URL for latest data
   → Registered but URL broken → use `web_search` to find the source's updated URL
2. **New data from Distill-Explore**: If "Distill-Explore" recommended a data dimension for tracking, use it with priority
3. **Supplementary search**: Only search from scratch for indicators not covered by the Source Registry

### 2.2 Source Priority (When Searching from Scratch)

1. Official institutions (Silver Institute, CME, LBMA, ICE, central banks)
2. Bloomberg / Reuters
3. Industry associations

→ **Secondary data is strictly prohibited.** Do not directly use chart data from research reports.

### 2.3 Search Strategy (When Searching from Scratch)

For each indicator:
1. Search `{indicator name} {year} {source institution}` for the latest value
2. Search `{indicator name} historical data` for time series
3. Need at least 6 months of historical data for trend charts

### 2.4 Record Data

```json
{
  "indicator": "COMEX Silver Inventory",
  "current_value": 340,
  "unit": "Moz",
  "as_of": "2026-05-29",
  "source": "CME Group",
  "source_url": "https://...",
  "frequency": "daily",
  "history": [
    {"date": "2026-01", "value": 440},
    {"date": "2026-02", "value": 410},
    ...
  ]
}
```

---

## Step 3: AI Analysis

For each indicator, write two short analyses:

### 3.1 YTD Trend Analysis

Answer: "From the start of the year to now, what is the overarching trend of this indicator? What does it imply for the thesis?"
- 1–2 sentences
- Include direction (up / down / flat) and magnitude
- Link back to the merged tree's argument

### 3.2 Recent Anomaly Analysis

Answer: "Has there been any unusual movement recently? If so, what does it mean?"

→ Anomaly detected: Describe it + explain possible causes + flag as an alert
→ No anomaly: Can omit or simply state "No significant anomaly in the recent period"

**What counts as an anomaly?**
- Single-day or single-week movement exceeding 2x the historical monthly average
- Breakout above or below the 6-month range
- Divergence from other indicators (e.g., spot tightness but ETF outflows)

---

## Step 4: Build the Dashboard Layout

```
┌─────────────────────────────────────┐
│ Target Asset Price Trend             │
│ (full width, Chart.js line chart)    │
├─────────────────────────────────────┤
│ Summary KPIs (single row, 6 key     │
│ numbers)                             │
├─────────────────────────────────────┤
│ Supply-Demand: 3 columns             │
│ [Indicator 1] [Indicator 2]         │
│ [Indicator 3]                        │
│ Each: title + scope + chart +        │
│ YTD + anomaly                        │
├─────────────────────────────────────┤
│ Spot Market: 3 columns               │
│ [Indicator 4] [Indicator 5]         │
│ [Indicator 6]                        │
├─────────────────────────────────────┤
│ Macro: 3 columns                     │
│ [Indicator 7] [Indicator 8]         │
│ [Indicator 9]                        │
└─────────────────────────────────────┘
```

---

## Step 5: Chart Specifications

All charts use Chart.js (loaded via CDN).

### Line Chart Requirements
- Must have axis labels (X-axis = time, Y-axis = unit)
- Hover displays exact value + unit
- Line style: pointRadius:0 (no points by default), pointHoverRadius:4 (show point on hover)
- Line width: 1.5px, tension: 0.3
- Colors: one color palette per framework — keep it clean

### Each Chart Card Includes
1. Title + update frequency label (small text, top right)
2. Data scope description (gray small text below the title)
3. Chart.js chart
4. YTD trend analysis (below the chart)
5. Recent anomaly analysis (if applicable, in an alert style)

---

## Step 6: Generate HTML

### Technical Requirements
- Single-file HTML, all data inlined
- Chart.js loaded via CDN
- Full-screen layout, CSS Grid
- Design style aligned with AskMBB (dark background #141417, gold accent #d4a76a)
- Responsive: 3 columns on wide screens, 1 column on narrow screens

### Data Disclaimer
Footer must state:
- "Demo data based on approximate values from web searches"
- "Production deployment should connect to Bloomberg Terminal / CME DataMine / LBMA API"
- Update frequency for each indicator

---

## Step 7: Quality Check

| Check Item | If Failed |
|------------|-----------|
| All charts render correctly? | Check Chart.js CDN and canvas IDs |
| Hover shows data? | Check tooltip configuration |
| Data is current (not from 6 months ago)? | Re-search |
| Every chart is labeled with scope and source? | Add them |
| Supply-demand balance numbers add up? | Supply − Demand = Deficit |
| Text labels display correctly? | Confirm charset=UTF-8 |

---

## Output

Use `html_writer` to write the dashboard HTML to the specified path.
