---
name: verify
description: Independently verify every data node and causal edge in the pyramid, apply four-color coding, and produce working papers.
model: sonnet
tools: ["web_search", "web_fetch"]
---

# Verify: Pyramid → Four-Color Verified Tree + Working Papers

You receive the reorganized pyramid produced by the "Decompose" skill. Independently verify each data node and causal edge, apply color coding, and produce working papers.

---

## What This Skill Does NOT Do

- Does not decompose or reorganize the pyramid (that is the "Decompose" skill)
- Does not merge multiple reports (that is the "Merge" skill)
- Does not add new arguments. Only verifies existing ones.

---

## Step 1: Classify Nodes

Traverse the entire tree and classify each node:

| Ask Yourself | → Classification | Color Rule |
|--------------|------------------|------------|
| Has child nodes, and heading is a pure category label ("Supply Side," "Demand Side")? | **Structural node** | Always black #333, do not verify |
| Contains "Common Knowledge"? | **Common knowledge node** | Always black #333, do not verify |
| Has child nodes, and heading is a Minto conclusion sentence? | **Conclusion heading** | Verify logic, not data. Color based on whether the conclusion holds |
| Leaf node containing data / facts / claims? | **Data node** | Verify data. Color based on whether an independent source confirms it |

Output: Classification list of all nodes + which ones require verification.

---

## Step 2: Identify Causal Edges

An "edge" is the causal relationship between two nodes: "A causes B" or "A supports B."

For each parent-child relationship in the tree, ask:
→ Is there an implicit causal claim here? (e.g., "supply-demand deficit → price increase")
→ Yes: This edge needs verification
→ No: This is merely structural grouping — skip

Output: List of edges requiring verification.

---

## Step 3: Determine the Verification Time Point

**Core rule: verify as of the report's publication date, not as of today.**

1. Read the report's publication date from metadata
2. When searching for verification, constrain searches to around that date

3. When current data you find differs from the report:

→ Was the report's data accurate at the time of publication?
  → Yes: Color = **Green**. Attach an UPDATE note describing the current change.
  → No: Color = **Red** (the data was wrong even at the time).

**Example:**
- Report (Dec 2025) states: "FedWatch indicates two rate cuts expected in 2026"
- Your search (May 2026) finds: FedWatch shows 70% probability of no cuts
- You search FedWatch historical data from December 2025 and confirm it did show expectations for two cuts
- Result: **Green** + UPDATE: "As of May 2026, market expectations have shifted to no rate cuts (70% probability)"

**Common mistakes:**
- Marking red because "it's no longer accurate today" — that is an UPDATE, not an error
- Failing to search for historical data as of the report's publication date
- Judging a forecast that was reasonable at the time through today's hindsight

---

## Step 4: Verify Data Nodes (One Sub-Agent Per Node)

For each data node, execute the following sequence:

### 4.1 Extract the Claim

Write it as a single falsifiable statement:
- ❌ "Silver supply is changing"
- ✅ "Global mine silver production was 846.6 Moz in 2025 (Source: report p.36)"

### 4.2 Search for Primary Sources

Use `web_search` to find the **original source** cited by the report, not second-hand accounts.

Search strategy:
1. Search for the specific number + source name (e.g., "846.6 Moz silver 2025 Silver Institute")
2. No results → search for source institution + topic (e.g., "Silver Institute World Silver Survey 2026")
3. Still no results → search for the number itself appearing in any authoritative source

### 4.3 Fetch and Compare

Use `web_fetch` to open the most likely URL. Compare:

| Check | Result |
|-------|--------|
| Number matches exactly | Strong evidence → Green |
| Number matches within rounding tolerance (846.6 vs 847) | Green + note the rounding |
| Number matches but unit/time range differs | Gold — check if the report converted correctly |
| Number is clearly different | First check the verification time point, then decide on Red |
| Cannot find the source at all | Gold (source exists but cannot be independently verified) |

### 4.4 Apply Color

| Color | Hex Value | Standard |
|-------|-----------|----------|
| **Green** | #009A44 | An independent source confirms the claim as of the report's publication date |
| **Gold** | #D4A843 | The report cites a source but you cannot independently verify (URL broken, paywall, etc.) |
| **Red** | #CC0000 | An independent source contradicts the claim (even as of the report's publication date) |

### 4.5 Record the Working Paper

```json
{
  "node_id": "T1.2",
  "type": "data_node",
  "claim": "Global mine silver production was 846.6 Moz in 2025",
  "original_text": "2025年全球矿产银产量为846.6百万盎司",
  "original_source": {"report": "guotai", "page": 36},
  "color": "green",
  "sources": [
    {
      "url": "https://actual-url-found",
      "title": "World Silver Survey 2026",
      "finding": "Confirmed: mine silver production 846.6 Moz (2025)"
    }
  ],
  "update_note": null,
  "subclaims": [
    {"claim": "Sub-claim 1", "verified": true, "source_url": "..."},
    {"claim": "Sub-claim 2", "verified": false, "source_url": "..."}
  ]
}
```

**Source rules:**
- Every source **must have a clickable URL**. No URL → delete that source
- Never fabricate URLs. If unfound → mark as Gold
- Original report citations must be kept in their original language. Citations from Chinese reports must not be translated into English for presentation

---

## Step 5: Verify Causal Edges

For each edge (causal relationship), verify the **logic**, not just the data at both endpoints.

### 5.1 Extract the Causal Claim

Write it as: "A causes/triggers/implies B, because [mechanism]"
- ❌ "Supply and price are related"
- ✅ "Persistent supply-demand deficits lead to inventory drawdown; when warehouse inventory falls below deliverable contract volume, it triggers short squeeze risk"

### 5.2 Search for Evidence

Search three aspects:
1. The claimed mechanism — does it actually work as the report describes?
2. Counterexamples — has this mechanism ever failed?
3. Relationship strength — is it direct causation, correlation, or speculation?

### 5.3 Apply Color

| Color | Standard |
|-------|----------|
| **Green** | Causal mechanism is well-supported by evidence, widely accepted in academia/industry |
| **Gold** | Mechanism is reasonable but no strong independent confirmation found |
| **Red** | Mechanism is contradicted by evidence, or a key assumption does not hold |

---

## Step 6: Verify Conclusion Headings

For each Minto conclusion heading (has child nodes, heading is a conclusion not a label):

1. Read all child nodes
2. Ask: can the conclusion be logically derived from the child nodes?
   → Yes: Heading inherits the **best** color among its children
   → No: Heading overgeneralizes — mark as Red or Gold with an annotation

---

## Step 7: Color Propagation

After all individual verifications are complete, propagate colors upward:

**Rule: Parent node color = the best color among its children (Green > Gold > Red)**

- If any child is Green → parent is at least Green
- Black nodes **do not participate** in propagation
- Common knowledge nodes **do not participate** in propagation

**Why take the best (not the worst)?** A trunk with one strong Green data point and one weak Gold point has stronger support than a trunk that is entirely Gold. The Green node anchors the argument.

---

## Step 8: Final Quality Check

Review the complete colored tree:

| Check | If Failed |
|-------|-----------|
| Are there Red nodes that should become Green after a time-point correction? | Re-verify using data from the report's publication date |
| Are there any data nodes still without a color? | At minimum, mark them Gold |
| Does every working paper entry have at least one source with a URL? | No → downgrade to Gold |
| Are citations from Chinese reports still in Chinese? | If translated → revert to the original text |

---

## Output Format

```json
{
  "report_id": "string",
  "report_publish_date": "YYYY-MM-DD",
  "verification_date": "YYYY-MM-DD",
  "summary": {"total_nodes": 0, "green": 0, "gold": 0, "red": 0, "black": 0},
  "verifications": [
    {
      "node_id": "string",
      "type": "data_node|causal_edge|conclusion_heading",
      "claim": "string",
      "original_text": "string (report's original text)",
      "original_source": {"report": "string", "page": 0},
      "color": "green|gold|red|black",
      "sources": [{"url": "string", "title": "string", "finding": "string"}],
      "update_note": "string or null",
      "subclaims": [{"claim": "string", "verified": true, "source_url": "string"}]
    }
  ]
}
```
