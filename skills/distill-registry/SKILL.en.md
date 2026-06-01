---
name: distill-registry
description: Extract all sources from the verification working papers, validate URL accessibility, register each source's data offerings, and build a structured Source Registry.
model: sonnet
tools: ["web_fetch"]
---

# Distill-Registry: Verification Working Papers → Source Registry

You receive the verification working papers produced by the "Verify" skill. Extract all cited sources, verify each one, register and classify them, and output a structured Source Registry.

---

## What This Skill Does NOT Do

- Does not verify the data itself (the "Verify" skill has already done that)
- Does not deep-dive into a source's complete data landscape (that is the "Distill-Explore" skill)
- Does not determine the investment thesis (that is the "Merge" skill)

---

## Step 1: Extract All Sources from the Working Papers

Traverse all verification working papers and extract the sources cited by each verification entry.

For each source, record:
- Source name (e.g., "Silver Institute World Silver Survey 2026")
- URL
- Which verification entries cited it (list of node_ids)
- What data it confirmed when cited

→ Merge and deduplicate: the same source may appear across multiple verification entries — consolidate into a single record.

---

## Step 2: Classify

For each source, determine its type:

| Ask Yourself | → Classification |
|--------------|------------------|
| Does it publish original data? (Silver Institute, CME, LBMA) | **Primary data source** |
| Does it re-cite data from others? (Financial news, broker re-citations) | **Secondary citation** |
| Is it an industry association or government statistical release? | **Official statistics** |
| Is it an academic paper or research report? | **Research literature** |
| Is it a paid database? (Bloomberg Terminal, Wind) | **Paid source** |

**Priority order: Primary data source > Official statistics > Research literature > Secondary citation**

---

## Step 3: Validate URL Accessibility

For each source's URL, use `web_fetch` to check:

| Check Item | Result |
|------------|--------|
| URL opens and content matches expectations | ✅ Accessible |
| URL opens but content has changed (e.g., annual report has been updated) | ⚠️ Accessible but note the version difference |
| URL fails to open (404, domain expired) | ❌ Inaccessible — flag as needing a replacement |
| URL is behind a paywall | 🔒 Paid — flag as restricted access |

---

## Step 4: Register Each Source's Data Offerings

For each accessible primary data source, record what data it provided during the verification process:

```
Source: Silver Institute - World Silver Survey 2026
Data provided:
  - Global mine silver annual production (Moz, annual, 2015–2026E)
  - Industrial demand breakdown (Moz, annual)
  - Photovoltaic silver demand (Moz, annual)
  - Supply-demand balance/deficit (Moz, annual)
```

**Note:** This step only registers data that was **actually used** during the verification process. The source may offer additional data — that is the job of the "Distill-Explore" skill.

---

## Step 5: Assess Source Quality

Assign a credibility rating to each source:

| Rating | Criteria |
|--------|----------|
| **Authoritative** | Widely recognized data publisher in the field; data is broadly cited |
| **Reliable** | Good institutional reputation, methodology is documented, but not the most authoritative in the field |
| **Reference-only** | Data provenance is not fully transparent, or conflicts of interest exist — use for reference only |

---

## Step 6: Screen for Core Judgments

From the verified data points, screen for "core judgments" — key facts with decisive impact on the investment thesis.

**Screening criteria:**

→ If this fact did not exist, would the investment thesis change?
  → Yes: **Core judgment** — must be retained
  → No: **Supporting detail** — can be retained but is not core

→ Can this fact be summarized in one sentence?
  → Yes: Suitable as a core judgment
  → No: Probably too granular

**Examples:**
- ✅ Core judgment: "Cumulative supply-demand deficit from 2021–2025 drew down 762 Moz of inventory"
- ❌ Supporting detail: "A specific miner's Q3 2025 production increased 3.2% year-over-year"

---

## Output Format

```json
{
  "report_ids": ["guotai", "galaxy", "founder"],
  "source_registry": [
    {
      "id": "src_001",
      "name": "Silver Institute - World Silver Survey 2026",
      "type": "primary data source",
      "url": "https://...",
      "url_status": "accessible",
      "reliability": "authoritative",
      "data_provided": [
        {
          "metric": "Global mine silver annual production",
          "unit": "Moz",
          "granularity": "annual",
          "range": "2015–2026E"
        }
      ],
      "used_in_nodes": ["T1.2", "D1.1", "D1.3"],
      "notes": "Published April 2026, includes 2025 actuals + 2026 forecast"
    }
  ],
  "core_judgments": [
    {
      "id": "cj_001",
      "statement": "Silver has been in supply-demand deficit for five consecutive years, drawing down 762 Moz of cumulative inventory",
      "supporting_nodes": ["T1.2", "D1.1"],
      "verification_color": "green",
      "source_ids": ["src_001"]
    }
  ],
  "summary": {
    "total_sources": 0,
    "primary": 0,
    "secondary": 0,
    "accessible": 0,
    "paywalled": 0,
    "broken": 0,
    "core_judgments_count": 0
  }
}
```
