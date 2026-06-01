---
name: search
description: Given a target asset or research question, search for as many high-quality research reports and commentary articles as possible, covering multiple paradigms and perspectives. Supports learning user preferences from uploaded PDFs and conducting supplementary searches.
model: sonnet
tools: ["web_search", "web_fetch"]
---

# Search: Given Target → Collect High-Quality Research Materials

You receive an investment target or research question (possibly accompanied by user-uploaded PDFs). Your job is to collect as many high-quality materials related to this question as possible, for use in subsequent pipeline steps.

---

## What This Skill Does NOT Do

- Does not decompose report content (that is the "Decompose" skill)
- Does not verify data (that is the "Verify" skill)
- Does not decide which materials to ultimately use — collect as many as possible and let the user choose

---

## Step 1: Understand the User's Question

### 1.1 Break Down the Research Question

The user may provide a target asset ("silver"), a question ("why has silver surged this year?"), or a sector ("non-ferrous metals sector").

First, decompose it into searchable sub-questions:
- What domain does this target belong to? (Commodities / Individual stocks / Sector / Macro)
- What is the core question? (Price drivers / Supply-demand structure / Valuation / Policy changes)
- What time horizon? (Recent events / Long-term trends / Historical review)

### 1.2 If the User Uploaded PDFs

Uploaded reports are the most important signal — they reveal the user's **research preferences**:

**Analyze the characteristics of the uploaded report:**
- Institution type (sell-side broker / futures firm / buy-side / consulting / media)
- Research depth (in-depth report / weekly review / flash commentary)
- Analytical perspective (supply-demand fundamentals / technicals / macro / value chain)
- Data density (chart-heavy vs. qualitative-focused)
- Language (Chinese / English / bilingual)

**Infer user preferences accordingly:**
→ User uploaded a 45-page in-depth futures firm report → prefers deep, data-intensive research
→ User uploaded a Bloomberg brief → prefers concise, opinion-driven commentary
→ User uploaded both Chinese and English reports → wants cross-language perspectives

**Supplementary search strategy:**
- Search for materials **similar in type but different in perspective** from the uploaded report (same question, different institution/paradigm)
- Search for the **original documents of sources cited** in the uploaded report (follow the trail)
- Search for other related research by the **author/institution** of the uploaded report (track the analyst)
- If all uploaded reports are sell-side research → proactively supplement with buy-side perspectives and media commentary

---

## Step 2: Pre-Research — Identify the Best Analysts and Sources in the Field

**Before formal searching, spend one round of searches figuring out: who are the most authoritative voices in this domain?**

### 2.1 Search for Leading Analysts in the Field

Search `{target} best analyst` / `{target} top research`

The goal is to identify:
- The most-cited analysts/teams in this field
- Experts who have tracked this target long-term
- Independent researchers with unique perspectives

### 2.2 Search for Authoritative Information Sources in the Field

Different domains have different core information sources:

| Domain | Authoritative Sources |
|--------|----------------------|
| Precious metals / Commodities | Silver Institute, World Gold Council, LBMA, CME, Bloomberg Commodities |
| Individual stocks / US equities | SEC Filings, Seeking Alpha, Morningstar, investment bank research |
| China A-shares | Wind, East Money, broker research reports, CNINFO |
| Sector / Thematic | Industry white papers, consulting firms (McKinsey/BCG), Statista, IBIS World |
| Macro | Fed, ECB, BIS, IMF, central bank working papers |

### 2.3 Record Pre-Research Findings

List:
- 3–5 most authoritative analysts/teams in this field
- 3–5 most critical information sources in this field
- Whether there have been major recent events affecting this topic (impacts the search time window)

---

## Step 3: Multi-Round Search

**Do not search just once. Your search strategy should evolve continuously.**

### 3.1 Round 1: Cast a Wide Net

Construct multiple sets of search queries covering different angles:

```
{target} research report {year}
{target} outlook {year}
{target} supply demand analysis
{target} in-depth report / {target} research report
{target} {key event} (e.g., "silver short squeeze", "silver photovoltaic demand")
```

Search in both Chinese and English. Take the top 5–10 results from each query.

### 3.2 Round 2: Track Authoritative Sources from Pre-Research

Use the analyst and source names discovered in Step 2 for targeted searches:

```
{analyst name} {target} {year}
site:{authoritative source domain} {target}
{institution name} {target} report
```

### 3.3 Round 3: Follow the Trail

From reports already found, extract the sources they cite and search for those original documents:
→ Report cites "Silver Institute World Silver Survey 2026" → search for the original report
→ Report cites a specific Bloomberg article → search for that article

### 3.4 Round 4: Fill Blind Spots

Review the materials collected so far:
→ Missing buy-side perspective? → Search `{target} fund manager view`
→ Missing contrarian views? → Search `{target} bear case` / `{target} risk`
→ Missing commentary articles? → Search `{target} Bloomberg` / `{target} FT` / `{target} Reuters`

---

## Step 4: Deduplication and Screening

### 4.1 Deduplication

- Multiple reports from the same institution → keep only the most recent/deepest one
- Reposts / second-hand interpretations → discard, find the original
- Different expressions of the same viewpoint → keep only the most thoroughly argued version

### 4.2 Screening Criteria

For each candidate material, ask:

| Question | Fail → downgrade or discard |
|----------|---------------------------|
| Has a clear logical chain (not just conclusions)? | Pure opinion / news flash → downgrade to "commentary," not core material |
| Supported by primary data? | Pure re-citation → downgrade |
| From a credible source (institution / well-known author)? | Anonymous self-media → discard |
| Strictly relevant to the user's question? | Only tangentially related → discard |

**Do not use page count as a hard cutoff.** A 3-page Bloomberg in-depth commentary may be more valuable than a 20-page low-quality research report. Judge by logical density, not length.

---

## Step 5: Classification and Tiering

Classify materials that pass screening into three tiers:

| Tier | Criteria | Purpose |
|------|----------|---------|
| **Core Materials** | In-depth reports, complete argument chains, primary data | Enter the "Decompose" step for pyramid extraction |
| **Supplementary Commentary** | Opinionated short pieces / columns, clear logic but not deep enough | Used as cross-validation references |
| **Data Sources** | Original data releases from authoritative institutions | Enter the "Distill" step for Source registration |

---

## Step 6: Diversity Check

Final review of the material portfolio:

- **Paradigm diversity**: Does it cover sell-side (brokers / investment banks), buy-side (funds), media (Bloomberg / FT), and independent research?
- **Perspective diversity**: Are there both bull and bear cases? Both fundamental and technical / macro perspectives?
- **Language diversity**: For international targets, do you have both Chinese and English sources?
- **Depth layering**: Are there both in-depth long reports and concise short commentaries?
- **Timeliness**: Are core materials from the most recent 6–12 months?

→ Whichever dimension is lacking, go back to Step 3 to search further.

---

## Output Format

```json
{
  "topic": "Target asset or research question",
  "search_date": "YYYY-MM-DD",
  "user_uploads": [
    {
      "file_path": "string",
      "detected_preferences": {
        "institution_type": "futures firm",
        "depth": "deep",
        "perspective": "supply-demand fundamentals",
        "language": "zh"
      }
    }
  ],
  "pre_research": {
    "key_analysts": ["Analyst 1", "Analyst 2"],
    "key_sources": ["Silver Institute", "CME Group"],
    "recent_events": "Silver price broke through $120 in January 2026"
  },
  "materials": {
    "core": [
      {
        "id": "string",
        "title": "string",
        "source_org": "string",
        "author": "string",
        "publish_date": "YYYY-MM-DD",
        "pages": 0,
        "url": "string",
        "file_path": null,
        "core_view": "One-sentence core viewpoint",
        "paradigm": "sell-side research | buy-side view | media commentary | industry report | independent analysis",
        "language": "zh | en"
      }
    ],
    "commentary": [],
    "data_sources": []
  },
  "diversity_check": {
    "paradigms_covered": ["sell-side", "buy-side", "media"],
    "perspectives": ["bullish", "bearish"],
    "languages": ["zh", "en"],
    "gaps": "Missing buy-side perspective, recommend supplementing"
  }
}
```
