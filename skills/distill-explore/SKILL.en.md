---
name: distill-explore
description: Deep-dive into each primary data source in the Source Registry, map its complete data landscape, and discover valuable data dimensions not mentioned in the research reports.
model: sonnet
tools: ["web_search", "web_fetch"]
---

# Distill-Explore: Source Registry → Data Map

You receive the Source Registry produced by the "Distill-Registry" skill. For each primary data source listed, perform a deep exploration to map its complete data landscape and discover data that the research reports did not mention but would be valuable for investment research.

---

## What This Skill Does NOT Do

- Does not verify data accuracy (that is the "Verify" skill)
- Does not build the registry (that is the "Distill-Registry" skill)
- Does not determine investment themes (that is the "Merge" skill)
- Does not download paid data (only maps the freely accessible portion)

---

## Step 1: Select Exploration Targets

From the Source Registry, filter for sources worth deep-diving into:

| Condition | → Explore? |
|-----------|------------|
| Primary data source + URL available + authoritative/reliable | ✅ Must explore |
| Official statistics + URL available | ✅ Worth exploring |
| Secondary citation | ❌ Skip (go find the primary source it cited) |
| URL unavailable or behind paywall | ❌ Skip (flag as "needs alternative") |

---

## Step 2: Map Each Source

For each exploration target, execute the following:

### 2.1 Visit the Homepage — Understand the Site Structure

Use `web_fetch` to open the source's main URL. **Like a researcher visiting this website for the first time, map out its structure:**

- What does this institution/website do? What is its core business?
- What sections appear in the navigation bar? (Data / Research / Publications / Statistics / Downloads)
- Is there a dedicated data center or database portal?
- Is there an API or data download page?
- Is there a free vs. paid section?

### 2.2 Go Deeper — Open Key Sub-Pages

Do not stop at the homepage. **Click through.**

→ Found a "Data" or "Statistics" section → `web_fetch` to open it
→ Found "Publications" or "Reports" → see what periodic publications exist
→ Found "Downloads" or "API" → record the data access method
→ If there is a search function → use `web_search` with `site:source-domain.com {relevant keywords}`

**The goal is to draw a data map of this website: what it has, where it is, and how to get it.**

### 2.3 Register Each Data Dimension

For each data dimension discovered, record:

```
Dimension name: COMEX Silver Inventory
Data type: Time series
Update frequency: Daily
Time range: 2000–present
Access method: Free web page / API / Registration required / Paid
URL: https://...
Format: Web table / CSV download / JSON API
Relevance to investment thesis: Directly relevant (core spot market indicator)
```

### 2.4 Assess Relevance to the Investment Thesis

For each discovered data dimension, ask:

→ Is this data related to our investment thesis?
  → **Directly relevant**: Core data for a specific argument in the investment thesis (e.g., supply-demand deficit)
  → **Indirectly relevant**: Helpful for judgment but not core (e.g., silver consumption in a specific application)
  → **Potential value**: Not currently used in the thesis, but could become relevant if the thesis is revised
  → **Irrelevant**: Completely unrelated to the investment topic — skip

---

## Step 3: Discover Data Overlooked by the Research Reports

Compare data actually cited in the reports vs. the source's complete data landscape to identify:

| Type | Example |
|------|---------|
| **Cited but underutilized** | Report cited WSS annual data, but WSS also has quarterly data |
| **Completely unmentioned** | Silver Institute has monthly ETF holdings tracking, but the report did not use it |
| **Different granularity from the same source** | Report used annual data, but monthly/daily data also exists |
| **Historical backfill from the same source** | Report only looked at the past two years, but data goes back 10 years |

---

## Step 4: Output the Data Map

### 4.1 One Map Per Source

```
┌─────────────────────────────────────────┐
│ Silver Institute                         │
│ silverinstitute.org                      │
│                                         │
│ ┌─ Used ──────────────────────────┐     │
│ │ · Annual supply-demand balance   │     │
│ │   (annual, 2015–26E)            │     │
│ │ · Mine silver production (annual)│     │
│ │ · Photovoltaic silver (annual)   │     │
│ └─────────────────────────────────┘     │
│                                         │
│ ┌─ Unused but directly relevant ──┐     │
│ │ · Monthly ETF holdings           │     │
│ │   (monthly, free)               │     │
│ │ · Silver price history           │     │
│ │   (daily, free)                 │     │
│ └─────────────────────────────────┘     │
│                                         │
│ ┌─ Potential value ───────────────┐     │
│ │ · Recycled silver source analysis│     │
│ │   (annual, paid)                │     │
│ │ · Regional consumption breakdown │     │
│ │   (annual, paid)                │     │
│ └─────────────────────────────────┘     │
└─────────────────────────────────────────┘
```

### 4.2 Recommend Data for Dashboard Tracking

From the "unused but directly relevant" category, recommend which items should be included in the "Dashboard" step for ongoing tracking:

→ High enough update frequency (at least monthly)?
→ Freely accessible?
→ Helpful for assessing whether the investment thesis still holds?

All criteria met → recommend for tracking

---

## Step 5: Preserve as a Data Asset

Once exploration is complete, this information is not disposable — it is a **reusable data asset**.

### 5.1 Build a "Data Source Handbook" for the Domain

Organize all exploration results into a structured handbook that can be reused for future research in the same domain:

- **Where to find what data** — what each source offers, update frequency, access method
- **Which sources are free** — a complete list of free data, reducing dependence on paid terminals
- **Relationships between data sources** — e.g., Silver Institute annual data + CME daily data = annual framework + daily tracking combination

### 5.2 Tag Data Ready for the Dashboard Step

For data recommended for tracking, record a sufficiently detailed access path so the "Dashboard" step can pull data directly:

```
Data: COMEX Silver Registered Inventory
Source: CME Group
URL: https://www.cmegroup.com/... (specific page, not the homepage)
Access method: Web table, updated daily
Data format: Online table, can be scraped manually
Notes: Registered and eligible inventory are displayed separately; track both
```

### 5.3 Record Serendipitous Discoveries

During exploration, you may find unexpectedly valuable information:
- A source provides data from a completely different angle (e.g., environmental regulations' impact on silver mining)
- A source has historical data that enables backtesting
- A source's data has methodological differences from another source that require attention

Record these as well — they are part of the knowledge asset.

---

## Output Format

```json
{
  "explored_sources": [
    {
      "source_id": "src_001",
      "name": "Silver Institute",
      "domain": "silverinstitute.org",
      "data_dimensions": [
        {
          "name": "Annual supply-demand balance",
          "type": "time series",
          "frequency": "annual",
          "range": "2015–2026E",
          "access": "free",
          "url": "https://...",
          "format": "web table",
          "used_in_reports": true,
          "relevance": "directly relevant",
          "recommend_track": false
        },
        {
          "name": "Monthly global ETF holdings",
          "type": "time series",
          "frequency": "monthly",
          "range": "2018–present",
          "access": "free",
          "url": "https://...",
          "format": "web table",
          "used_in_reports": false,
          "relevance": "directly relevant",
          "recommend_track": true
        }
      ],
      "gaps_found": [
        "Report only used annual data, but monthly ETF holdings are available for more timely tracking",
        "Daily silver price history goes back 10 years, suitable for historical analogy analysis"
      ]
    }
  ],
  "recommended_for_tracking": [
    {
      "source_id": "src_001",
      "dimension": "Monthly global ETF holdings",
      "reason": "Monthly updates, free, directly reflects changes in investment demand",
      "url": "https://..."
    }
  ],
  "summary": {
    "sources_explored": 0,
    "total_dimensions_found": 0,
    "used_in_reports": 0,
    "new_relevant": 0,
    "recommended_for_tracking": 0
  }
}
```
