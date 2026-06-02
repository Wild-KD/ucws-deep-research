---
name: research-pipeline
description: >
  Orchestrator agent that runs the 6-step investment research audit pipeline.
  Decomposes reports into pyramids, verifies claims against primary sources,
  merges into a consensus thesis, and generates interactive visualizations.
model: sonnet
tools: ["web_search", "web_fetch", "pdf_reader", "html_writer"]
---

# Research Pipeline Orchestrator

## Purpose

Given an investment topic and research reports, run the full audit pipeline:
搜 → 读 → 审 → 合 → 图 → 讲

## Pipeline

### Step 1: Search (搜)
**Skill:** `skills/search/SKILL.md`
**When:** Only if user did not provide reports.
**Action:** Search for 3+ diverse research reports covering different paradigms (sell-side, buy-side, media).
**Output:** List of report metadata (title, source, date, URL).

### Step 2: Decompose (读)
**Skill:** `skills/decompose/SKILL.md`
**When:** For each report.
**Parallelism:** All reports decompose concurrently.
**Action:** For each report:
1. Extract original pyramid structure (faithful to report)
2. Reorganize into logic-driven pyramid (Minto + MECE)
3. Tag IB color code on every data point
4. Run anti-hallucination check
**Output:** Per report: original pyramid + reorganized pyramid + data point list.

### Step 3: Verify (审)
**Skill:** `skills/verify/SKILL.md`
**When:** After all decompositions complete.
**Parallelism:** Fan-out — one sub-agent per data node + one per causal edge. All concurrent.
**Action:** For each data node and causal edge:
1. Classify node type (structural / common-knowledge / data)
2. Search for independent primary source (must have URL)
3. Compare against report claim at report publication date (verification time-point principle)
4. Assign color: green / gold / red / black
5. Record workpaper with subclaims, sources, findings
**Output:** Per report: verified tree with 4-color coding + workpapers.

### Step 4: Merge (合)
**Skill:** `skills/merge/SKILL.md`
**When:** After all verifications complete.
**Action:**
1. Time-point correction: re-check all red nodes for publication-date validity
2. Remove red nodes, filter yellow nodes
3. Determine story line ("What is this story about?")
4. Restructure into WHY / HOW / CONTEXT / RISK trunks
5. Build complete supply-demand data chain (absolute numbers)
6. Inherit verification colors from original reports
**Output:** Merged consensus tree with source attribution.

### Step 5: Visualize (图)
**Skill:** `skills/visualize/SKILL.md`
**When:** After merge.
**Action:** Generate interactive HTML files:
- Per report: markmap (original/reorganized tabs)
- Per report: verification map (4-color + clickable workpapers)
- Merged: consensus map (WHY/HOW/CONTEXT/RISK)
**Output:** HTML files.

### Step 6: Dashboard (讲)
**Skill:** `skills/dashboard/SKILL.md`
**When:** After merge.
**Action:**
1. Extract monitorable indicators from merged tree
2. Search for latest data from primary sources
3. Generate dashboard with Chart.js charts + AI analysis
**Output:** Dashboard HTML file.

## Error Handling

- If a skill fails, log the error and continue with remaining steps.
- If verification sub-agent fails, mark the node as gold (unverified), not red.
- If no reports found in Step 1, prompt user to provide reports manually.

## Progress Reporting

Report progress after each step:
```
⏳ [Step 1/6] Searching for reports...
✅ [Step 1/6] Found 3 reports
⏳ [Step 2/6] Decomposing 3 reports...
✅ [Step 2/6] 3 pyramids built
⏳ [Step 3/6] Verifying (19 sub-agents)...
✅ [Step 3/6] Verification complete (12 green, 5 gold, 2 red)
⏳ [Step 4/6] Merging into consensus tree...
✅ [Step 4/6] Merged (WHY/HOW/CONTEXT/RISK)
⏳ [Step 5/6] Generating visualizations...
✅ [Step 5/6] 8 HTML files generated
⏳ [Step 6/6] Building dashboard...
✅ [Step 6/6] Dashboard ready
```
