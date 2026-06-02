# Skills — The Core of Investment Detective

**This directory is the heart of the project.** Each subdirectory contains a Skill: a structured Markdown file that encodes a specific research methodology. Skills are:

- **Human-readable**: Open any `SKILL.en.md` to see exactly how the agent reasons
- **Bilingual**: Every Skill has a Chinese (`SKILL.zh.md`) and English (`SKILL.en.md`) version
- **Portable**: Skills work with any LLM provider (MiroMind, OpenAI, etc.)
- **Self-contained**: Each Skill defines its own inputs, outputs, decision logic, and guardrails

## The 8 Skills

```
skills/
├── search/              ← 搜 Find authoritative reports
├── decompose/           ← 读 Minto pyramid decomposition
├── verify/              ← 审 Multi-agent data & logic verification
├── distill-registry/    ← 沉·整 Source registry + core judgments
├── distill-explore/     ← 沉·探 Source data-landscape mapping
├── merge/               ← 合 Storyteller-driven thesis merge
├── visualize/           ← 图 Interactive markmap rendering
└── dashboard/           ← 追 Forward monitoring dashboard
```

## How Skills Work

Each Skill is loaded as a **system prompt** by the pipeline runner. The runner passes the Skill's markdown to the LLM, along with the current step's input data. The LLM follows the Skill's instructions to produce structured output.

```
Pipeline Runner
      │
      ├── loads skills/search/SKILL.en.md as system prompt
      ├── sends input: "topic: silver"
      └── receives output: JSON list of reports found
```

The Skills encode all domain expertise. The runner is intentionally thin.

## Reading a Skill

Every Skill follows the same structure:

1. **YAML frontmatter**: name, description, tools needed
2. **"What this skill does NOT do"**: clear boundaries
3. **Numbered steps**: each with decision branches (→ YES / → NO)
4. **Output format**: JSON schema

Start with `verify/SKILL.en.md` — it's the most representative of the methodology.
