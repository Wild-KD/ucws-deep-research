---
name: merge
description: Merge multiple verified pyramids into a single consensus tree, driven by Storyteller methodology, using a WHY/HOW/CONTEXT/RISK structure.
model: sonnet
tools: []
---

# Merge: N Verified Trees → 1 Consensus Tree

You receive 2+ verified pyramids (outputs of the "Verify" skill). Merge them into a single consensus tree that tells a coherent story to non-expert readers.

---

## What This Skill Does NOT Do

- Does not re-verify data (colors are inherited from source reports)
- Does not add new external data
- Does not include every data point from every report — this is curation, not accumulation

---

## Step 1: Time-Point Correction

Before merging, review all **Red** nodes across all reports.

For each Red node, ask:
→ Was it marked Red because **today's data** was used to reject **data that was accurate at the time of publication**?
→ Yes: Change to **Green** + UPDATE annotation. This was an incorrect verification approach.
→ No: The data was wrong even at the time. Keep it Red.

---

## Step 2: Remove Red Nodes

Traverse all verified trees and remove:
- All Red data nodes (contradicted by evidence)
- All Red causal edges
- All parent nodes whose children are **entirely** Red (the branch is dead)

**What about partially Red branches?**
→ Some children are Green/Gold, some are Red?
→ Keep the branch — only remove the Red children. The branch is weakened but still alive.

---

## Step 3: Screen Gold Nodes

Not all Gold nodes should enter the merged tree. For each Gold node, ask:

| Question | → Keep? |
|----------|---------|
| Does it quantify a key variable in the story's main thread? | Keep |
| Is it a core argument of one of the reports? | Keep |
| Is it too granular (e.g., one mine's production in one quarter)? | Discard |
| Is it a minor supplementary note ("for reference")? | Discard |
| Is its parent/foundation also problematic? | Discard (unstable base) |

**When in doubt:** Ask "if I remove it, does the story break?" No → Discard.

---

## Step 4: Extract Surviving Paths

From each verified tree, extract the nodes and edges that survived Steps 1–3 (Green + retained Gold).

Group by topic/theme (not by source report). You are about to rebuild the structure.

---

## Step 5: Determine the Story (Storyteller Step)

**This is the most important step. It must be completed before building any structure.**

### 5.1 One-Sentence Story

Answer: "What is this story about?"

- ❌ "Silver supply and demand" (that is a topic, not a story)
- ✅ "Silver faces a structural supply-demand deficit, and spot market mechanisms are converting this deficit into potential short-squeeze risk" (this is a story with tension)

### 5.2 Choose the Trunks

Based on the story, select 3–4 trunks. Default framework:

| Trunk | Role | What Question It Answers |
|-------|------|--------------------------|
| **WHY** | Root cause / Fundamentals | Why does the structural problem exist? |
| **HOW** | Transmission mechanism | How does the problem become a crisis/opportunity? |
| **CONTEXT** | Background conditions | What macro/external conditions are amplifying or dampening it? |
| **RISK** | Reversal conditions | Under what circumstances would the story flip? |

**Judgment: Do you need all four?**
→ Simple story (one cause, one effect): WHY + RISK may suffice
→ Complex mechanism (short squeeze, contagion, feedback loops): Add HOW
→ Macro conditions independently affect the outcome: Add CONTEXT

### 5.3 Assign Surviving Nodes to Trunks

For each node from Step 4, ask: "Which trunk does it serve?"

**Core screening principle: "Does it contribute to the story?" > "Is the data correct?"**

→ Green data does **not** automatically qualify. A verified fact about China's silver imports may be correct but irrelevant to the main narrative.
→ Correct but irrelevant nodes → downgrade to "supporting evidence" under the relevant trunk, not a main branch
→ Nodes that do not belong to any trunk → most likely should not appear in the merged tree

**Downgrade example:**
- China silver import data: verified as Green, but China is not the primary driver in the global thesis
- → Do not make "China" a top-level trunk
- → Place under WHY > Supply as supporting evidence: "China data corroborates global supply tightness"

---

## Step 6: Fill Logical Gaps for Non-Expert Readers

Read through the story trunk by trunk. At every point where an expert would understand but a non-expert would get stuck, insert a **Common Knowledge node**.

Common gap checks:

| Gap | Common Knowledge Needed |
|-----|------------------------|
| "Low inventory → price rise" | Explain the short squeeze mechanism: when warehouse stock falls below deliverable contract volume, short sellers are forced to buy at any price |
| "Rate cuts → metals rise" | Explain opportunity cost: metals pay no interest; the lower the rates, the lower the cost of holding metals |
| "Deficit → bullish" | Explain inventory drawdown: persistent deficits consume existing inventory until a supply crisis forces price rationing |
| "Lease rate spikes → squeeze" | Explain borrowing cost: when the annualized cost of borrowing physical metal reaches 20%+, it signals extreme scarcity |

Format: `[Common Knowledge] Explanation text *(Source: standard market mechanism)*`

---

## Step 7: Rebuild the Pyramid

### 7.1 Write Minto Headings for Each Trunk

Same rules as the "Decompose" skill — every heading is a conclusion, not a label.

### 7.2 MECE Within Each Trunk (Triple Check)

MECE in the merged tree is harder than in a single report — you must cross-merge reasoning lines from different reports into a new tree. **Apply the triple check at every level:**

**Check 1: MECE Completeness**
- Maximum 4 sub-arguments per level
- Mutual exclusivity (no overlap) — be especially careful that different reports may have used different decomposition schemes for the same issue; do not mechanically preserve both schemes
- Collective exhaustiveness (no gaps) — a unique perspective mentioned in one report but not others should be included if it contributes to the story
- Causal chain merge — if different reports separately address the first half and second half of a causal chain, merge them into a complete chain

**Check 2: Logical Relevance**
- Are sibling branches parallel / progressive / contrastive?
- Even if parallel, there is a logically optimal sequence: premise first, core dimension first
- When evidence from different reports is placed at the same level, verify they truly address the same dimension

**Check 3: Storytelling Self-Check**
- Using this merged structure, can you deliver a coherent 10-minute presentation?
- Would the audience feel a jarring context switch to a different report at any point? → Need a transition
- After the presentation, can the audience independently arrive at the root conclusion?

### 7.3 Build the Supply-Demand Data Chain (If Applicable)

The merged tree **must** include a complete supply-demand data chain:

```
Supply: XXX Moz (Source A) / YYY Moz (Source B)
Demand: XXX Moz
Deficit: XXX Moz
```

When different reports provide different numbers:
→ Present them side by side, with source attribution
→ **Do not** average them or select one without explanation

---

## Step 8: Inherit Verification Colors

**Rule: Colors are inherited from source reports — do not re-verify.**

| Scenario | Color |
|----------|-------|
| Node comes from one report | Inherit that report's color |
| Same claim mentioned by multiple reports with different colors | Take the best (Green > Gold > Red) |
| Newly constructed structural heading | Black (structural) |
| Newly constructed causal edge (connecting nodes from different reports) | Black, annotated as "merged inference" |
| Common knowledge node | Black |

Propagation rule same as "Verify" skill: parent = best among children; Black does not participate.

---

## Step 9: Annotate Sources

Every node in the merged tree must be annotated with:
1. **Source report(s)**: Which report(s) the data comes from (use short names)
2. **Page number(s)**: Original page references
3. **Verification source URL**: Inherited from the verification working papers

Format: `[Guotai p.36 / Founder p.12]`

When multiple reports support the same claim, list all of them.

---

## Step 10: Reverse Audit

Read the merged tree from bottom to top:

1. Do leaf nodes support their parent headings? → No → heading overgeneralizes
2. Do trunk headings support the root conclusion? → No → the story has a gap
3. Reading only headings top to bottom, does the story flow smoothly? → No → adjust the sequence
4. Are there claims without source annotations? → Yes → add them or delete the claim

---

## Output Format

```json
{
  "story": "One-sentence story line",
  "merged_tree": {
    "conclusion": "Minto conclusion sentence",
    "trunks": [
      {
        "key": "WHY|HOW|CONTEXT|RISK",
        "heading": "Minto conclusion sentence",
        "children": [
          {
            "id": "M1.1",
            "heading": "string",
            "content": "string",
            "color": "green|gold|red|black",
            "sources": ["Guotai p.36", "Galaxy p.8"],
            "verify_url": "https://...",
            "is_common_knowledge": false
          }
        ]
      }
    ]
  },
  "data_chain": {
    "supply": {"total": 0, "unit": "Moz", "sources": {}},
    "demand": {"total": 0, "unit": "Moz", "sources": {}},
    "balance": {"value": 0, "unit": "Moz"}
  },
  "source_reports": [
    {"id": "guotai", "title": "string", "publish_date": "YYYY-MM-DD"}
  ],
  "dropped_nodes": [
    {"id": "string", "reason": "red|irrelevant|too granular"}
  ]
}
```
