---
name: decompose
description: Decompose research reports into two pyramids (faithful reproduction + logical reorganization), following Minto, MECE, IB Color Code, and anti-hallucination rules. The core goal is to break complex reports into a logical structure that can be presented to others.
model: sonnet
tools: ["pdf_reader"]
---

# Decompose: Research Report → Pyramid Structure

You receive a research report (PDF or text). Produce two outputs:
1. **Original Pyramid** — faithfully reproduce the report's own logical structure
2. **Reorganized Pyramid** — rebuild by causal logic, fill logical gaps, apply color coding, so one can tell this story to others

---

## What This Skill Does NOT Do

- Does not verify data authenticity (that is the "Verify" skill)
- Does not merge multiple reports (that is the "Merge" skill)
- Does not add any data from outside the report. Every number must come from the report's original text.

---

## Step 1: Load the Report

1. Use `pdf_reader` to read the full report
2. Record metadata: title, institution, publication date, total pages
3. Read through once and answer in one sentence: what is this report's core thesis?

Output: One-sentence thesis + metadata.

---

## Step 2: Faithful Reproduction

Preserve the report's original logical structure — no rewriting, no reorganization.

For each section:
- Retain the report's original section headings verbatim
- Extract the key data points and assertions under each section
- Annotate each data point with its **page number**

→ This is the **Original Pyramid**. Ensure it faithfully reproduces the report's reasoning flow, letting the user see "how the report author was thinking."

---

## Step 3: Find the Trunks

**Forget the report's own chapter structure.** Ask yourself: if I had to explain this report's core thesis to someone with zero background in this domain, how many things would I need to cover?

### 3.1 Extract All Arguments

First, list out every argument, judgment, and data-driven conclusion in the report — no hierarchy, no filtering. This is your raw material.

### 3.2 Cluster into Trunks

Find patterns among these scattered arguments: which ones address different facets of the same issue?

**Mental test:** Imagine you are giving a 15-minute briefing to your boss. How would you group these arguments into major blocks? Each block is a trunk.

Reference by report type:

| Report Type | Typical Trunks |
|-------------|---------------|
| Commodity Outlook | Supply / Demand / Macro / Risk |
| Company Analysis | Business Model / Financials / Valuation / Catalysts |
| Industry Overview | Market Size / Competitive Landscape / Growth Drivers / Risk |
| Macro Research | Current State / Policy / Transmission Mechanism / Outlook |

### 3.3 Check Relationships Between Trunks

**Key judgment:** Do any two trunks have a causal relationship?
→ Yes (A causes B): Merge into one trunk; A→B becomes the internal logic chain of that trunk
→ No (A and B are independent): Keep as two parallel trunks

Each report should have **2–4 trunks**. More than 4 suggests some are sub-arguments, not trunks.

---

## Step 4: Write Minto Headings

**This step determines whether someone can understand your story by reading headings alone.**

Every heading at every level must be a **directional conclusion**, not a category label.

### Test Method

Cover all body text and read only the headings, top to bottom. Ask yourself:
- Can I follow the complete argument? → Yes → headings pass
- Do I only see a bunch of category names? → headings are labels not conclusions — must rewrite

### How to Convert

| ❌ Category Label | ✅ Conclusion-First |
|------------------|---------------------|
| Supply Side | Supply is contracting short-term; byproduct constraints limit production upside |
| Interest Rates | Continued rate cuts reduce the opportunity cost of holding precious metals |
| Demand Outlook | Demand will not collapse; photovoltaic transition offsets traditional decline |
| Historical Comparison | Current setup resembles the pre-squeeze environment of 2010–2011 |

**Rules:**
- Headings must include a direction (up / down / stable / risk)
- Headings must include the mechanism or cause ("because...", "driven by...", "as a result of...")
- If you cannot write a conclusion → this section may need to be split or merged

---

## Step 5: MECE Decomposition (Core Step)

**This is the single most critical step of the entire skill.**

The goal is not merely "mutually exclusive, collectively exhaustive." After decomposition, **every level** must simultaneously satisfy three criteria:

1. **MECE Completeness** — no gaps, no overlaps
2. **Logical Relevance** — sibling branches have a clear logical ordering or parallel relationship
3. **Storytelling Self-Check** — following this sequence, you can tell a coherent story to someone else

These three criteria must be checked at **every level** of the pyramid, not just the top.

### 5.1 First: Extract All Evidence

List every assertion, data point, and piece of reasoning in the report that belongs to this trunk. No filtering yet — be exhaustive.

### 5.2 Second: Identify Reasoning Lines

**Among this body of evidence, how many independent reasoning lines exist?**

One reasoning line = one complete "because A, therefore B" chain.

Example (under a silver supply trunk):
- Reasoning line 1: Mine silver is constrained by byproduct dynamics → even if silver prices rise, production can barely increase → hard supply constraint
- Reasoning line 2: Recycled silver volumes are stable → cannot fill the mine production gap → low supply elasticity
- Reasoning line 3: Some miners are cutting production → further short-term supply contraction

Each reasoning line becomes a sub-argument.

### 5.3 Third: Triple Check (Apply at Every Level)

**Check 1: MECE Completeness**

Mutual exclusivity:
→ For each pair of reasoning lines, ask: do they overlap? Could the same evidence belong to both?
→ Overlap exists: Merge them, or redraw boundaries
→ No overlap: Keep independent

Common violations:
- "Short-term factors" vs. "Long-term factors," but some data straddles both → split by mechanism instead
- "Price factors" vs. "Cost factors," but cost is part of price → merge
- Sequential events in a causal chain treated as parallel → merge into one reasoning line

Collective exhaustiveness:
→ Does the report contain important evidence that does not belong to any reasoning line?
→ Yes: Add or expand → No: Coverage is complete

**Check 2: Logical Relevance**

Sibling branches at the same level must have a clear logical relationship:

→ Are they **parallel**? (Equally important different facets)
→ Are they **progressive**? (A is a premise, B is an inference)
→ Are they **contrastive**? (Pro vs. con)
→ Are they **causal**? → If so, they should not be parallel — merge into a single chain

**Even for parallel branches, there is a logically optimal sequence:**
- If there is a premise → inference relationship → premise first
- If they are different dimensions → most critical dimension first
- If they are pro/con contrast → main viewpoint first, rebuttal second

**Check 3: Storytelling Self-Check**

Ask yourself: if I gave a presentation using this structure:
→ Following this sequence, can the audience keep up?
→ At any point, would the audience ask "why are we suddenly talking about this?" → If so, sequence is wrong
→ After covering all branches, can the audience naturally arrive at the parent node's conclusion? → If not, branches are incomplete or the conclusion leaps too far

### 5.4 Hard Constraints

- **Maximum 4 sub-arguments per level.** More than 4 means two reasoning lines are actually the same thing — merge them.
- **Parallel symmetry.** Sub-arguments under the same parent must be of the same type (all causes, all effects, all participants) — no mixing.
- **Causal chain merge.** A causes B → they are not parallel sub-arguments, but the internal structure of one reasoning line.

### 5.5 Recurse

Repeat steps 5.2–5.4 for each sub-argument, until you reach leaf nodes (individual data points or claims).

**Apply the triple check at every level**, not just the top. The level immediately above leaf nodes must also satisfy MECE + Logical Relevance + Storytelling.

---

## Step 6: Write Leaf Nodes

Each leaf node format:

```
[IB color, bold] One-sentence news-lead style (5W1H)
*(Source: report name, p.XX)*
```

### IB Color Code (text color — only three colors)

| Color | Hex Value | When to Use | Example |
|-------|-----------|------------|---------|
| **Blue** | #005EB8 | Citing external data sources | "LBMA vault holdings fell to 22,858 tonnes (LBMA Monthly Report)" |
| **Green** | #008800 | Author's assumptions, forecasts | "We project PV silver demand to grow 15% annually through 2028" |
| **Black** | #000000 | Calculated results, update notes, structural text | "Deficit = Supply 1,015 − Demand 1,164 = −149 Moz" |

**Decision logic for each data point:**
→ This number comes from an external source cited by the report? → Blue
→ This is the report author's own forecast/assumption? → Green
→ This is derived by calculation from other numbers? → Black
→ Uncertain? → Default to Blue (external citation), and flag the uncertainty

### Common Knowledge Nodes

When the report's logic has a gap that non-expert readers would not understand, insert a common knowledge node:

```
[Common Knowledge] When exchange warehouse inventory falls below deliverable contract volume,
short sellers are forced to buy back ("short squeeze"), causing prices to spike
beyond what fundamentals justify.
*(Source: standard commodity market mechanism)*
```

- Gray text, labeled `[Common Knowledge]`
- Still must cite a source (even if it is "standard market mechanism" or "textbook definition")
- Can be hidden/shown in visualization

---

## Step 7: Supply-Demand Data Chain (If Applicable)

If the report deals with a commodity/industry with supply-demand dynamics, you **must** construct the complete numerical chain:

```
Supply:
  Mine production: XXX Moz
  + Recycled: XXX Moz
  + Other: XXX Moz
  = Total supply: XXX Moz

Demand:
  Industrial demand: XXX Moz
    of which photovoltaic: XXX Moz
  + Jewelry: XXX Moz
  + Investment: XXX Moz
  = Total demand: XXX Moz

Balance: Total supply − Total demand = Deficit/Surplus XXX Moz
```

**Rules:**
- Must have absolute numbers — percentages alone are not acceptable
- The reader must be able to verify: supply − demand = the deficit stated in the report
- If the report uses multiple accounting bases (with/without ETF), present them side by side
- If the report gives a range, write "XXX–YYY Moz"

---

## Step 8: Anti-Hallucination Check

**Mandatory.** Check every data point in the reorganized pyramid one by one:

| Check Item | If Failed |
|------------|-----------|
| Does this number explicitly appear in the original report text? | No → delete it |
| Is the unit correct (Moz, tonnes, %, USD)? | Wrong → correct per the original report |
| Did I perform a calculation or conversion not present in the report? | Yes → delete the calculation, keep only the report's original numbers |
| Did I translate a citation and present the translation as if it were the original text? | Yes → revert to the original language |
| Does every data point have a page number? | No → find the page number or delete it |

**Known hallucination patterns (be especially vigilant):**
- Converting units the report never converted (e.g., "42,640 tonnes" → "covers 1.2 months," but the report never said that)
- Splicing numbers from different tables/sections to compute new figures
- Translating citations from a Chinese report into English and presenting them as direct quotes
- Rounding differently from the report

**When a hallucination is found:** Delete it immediately. Do not attempt to search for the correct number. Only use what the report explicitly states.

---

## Step 9: Reverse Audit

Read only the headings of the reorganized pyramid, top to bottom.

Ask three questions:
1. **Can I understand the complete argument from headings alone?** → No → some heading is a label not a conclusion — rewrite it
2. **Is there a logical gap between any two adjacent headings?** → Yes → insert a common knowledge node
3. **Does the story flow naturally without needing to backtrack?** → No → adjust the sequence

Finally, do a presentation test: using this structure, could you explain this to someone unfamiliar with the domain?

---

## Output Format

```json
{
  "report_id": "string",
  "metadata": {
    "title": "string",
    "source_org": "string",
    "publish_date": "YYYY-MM-DD",
    "pages": 0
  },
  "original_pyramid": {
    "conclusion": "string",
    "trunks": [{"heading": "string (report's original heading)", "children": []}]
  },
  "reorganized_pyramid": {
    "conclusion": "string (Minto conclusion)",
    "trunks": [
      {
        "heading": "string (Minto conclusion)",
        "children": [
          {
            "id": "T1.1",
            "heading": "string (Minto conclusion)",
            "content": "string (leaf node text with IB color)",
            "ib_color": "blue|green|black",
            "source_ref": {"report": "string", "page": 0},
            "original_text": "string (verbatim text from the report)",
            "is_common_knowledge": false
          }
        ]
      }
    ]
  },
  "data_chain": {
    "supply": {"total": 0, "unit": "Moz", "breakdown": {}},
    "demand": {"total": 0, "unit": "Moz", "breakdown": {}},
    "balance": {"value": 0, "unit": "Moz"}
  }
}
```
