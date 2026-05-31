# SKILL.md — Skills Reference

This agent uses 6 Skills, each defined as a Markdown file that serves as the system prompt for its pipeline step. Skills encode domain expertise — the rules, frameworks, and constraints that govern how the agent reasons about investment research.

## Skills Overview

| # | Skill | File | Purpose |
|---|-------|------|---------|
| 1 | Search | `skills/search/SKILL.md` | Find diverse research reports across paradigms |
| 2 | Decompose | `skills/decompose/SKILL.md` | Pyramid decomposition + logic reorganization |
| 3 | Verify | `skills/verify/SKILL.md` | Independent data/logic verification + 4-color coding |
| 4 | Merge | `skills/merge/SKILL.md` | Storyteller-driven multi-report merging |
| 5 | Visualize | `skills/visualize/SKILL.md` | Interactive markmap HTML generation |
| 6 | Dashboard | `skills/dashboard/SKILL.md` | Forward monitoring dashboard generation |

## Key Frameworks Embedded in Skills

### Minto Pyramid Principle (Skills 2, 4)
Every heading is a directional conclusion, not a category label.
- BAD: "Supply side"
- GOOD: "Supply contracts short-term as by-product mining constrains expansion"

### MECE (Skills 2, 4)
Max 4 sub-points per level. Parallel and symmetric. Causal chains merge, never sit in parallel.

### IB Color Code (Skill 2)
Text color indicates data provenance:
- **Blue #005EB8** = External reference
- **Green #008800** = Assumption / forecast
- **Black #000000** = Calculated result

### Verification 4-Color System (Skill 3)
Border/line color indicates verification status:
- **Green #009A44** = Verified against independent source
- **Gold #D4A843** = Has source, not independently verified
- **Red #CC0000** = Conflicts with independent source
- **Black #333333** = Structural node / common knowledge

### Anti-Hallucination Rules (Skills 2, 3)
- Only use data explicitly in the original report text
- No self-calculation, unit conversion, or cross-source splicing
- Chinese report quotes must stay in Chinese (no translation presented as direct quote)
- Every data point must carry a page number reference
- Every verification source must have a clickable URL — no URL = delete source

### Verification Time-Point Principle (Skills 3, 4)
Verify data against what was true at the report's publication date.
- Report (Dec 2025) says "FedWatch shows two rate cuts in 2026"
- Current (May 2026) FedWatch shows 70% no cuts
- Correct: GREEN (accurate at publication) + UPDATE note (expectations shifted)

### Storyteller Principle (Skill 4)
Before merging, determine the story first. "Does this contribute to the story?" matters more than "Is this data correct?"
- Green data doesn't automatically belong in the merged tree
- Structure: WHY (fundamentals) / HOW (mechanism) / CONTEXT (macro) / RISK

### Supply-Demand Data Chain (Skills 2, 4)
Must show absolute numbers, not just percentages:
```
Supply: Mine XXX Moz + Recycling XXX Moz = Total Supply XXX Moz
Demand: Industrial XXX + Jewelry XXX + Investment XXX = Total Demand XXX Moz
Balance: Supply - Demand = Deficit XXX Moz
```
