"""
Pipeline Orchestrator: runs the 6-step research pipeline.
搜 → 读 → 审 → 合 → 图 → 讲
"""
from __future__ import annotations

import asyncio
import inspect
import logging
import os
from pathlib import Path
from datetime import datetime

from core.agent import BaseAgent
from core.artifacts import ArtifactStore
from core.json_utils import dumps_pretty, parse_json_output
from core.schemas import validate_step
from config import Config
from llm import create_provider
from tools import WebSearchTool, WebFetchTool, PDFReaderTool, HTMLWriterTool

logger = logging.getLogger(__name__)


class Orchestrator:
    def __init__(self, config: Config):
        self.config = config
        self.llm = create_provider(config.llm)
        self.skills_dir = Path(__file__).parent.parent / config.skills_dir
        self.output_dir = Path(config.output_dir)
        self._init_tools()

    def _init_tools(self):
        """Initialize tool instances."""
        self.search_tool = WebSearchTool(self.config.tools.tavily_api_key)
        self.fetch_tool = WebFetchTool()
        self.pdf_tool = PDFReaderTool()
        self.html_tool = HTMLWriterTool()

        self.search_tools = {
            "web_search": self.search_tool,
            "web_fetch": self.fetch_tool,
        }
        self.read_tools = {
            "pdf_reader": self.pdf_tool,
        }
        self.verify_tools = {
            "web_search": self.search_tool,
            "web_fetch": self.fetch_tool,
        }
        self.write_tools = {
            "html_writer": self.html_tool,
        }
        self.dashboard_tools = {
            "web_search": self.search_tool,
            "web_fetch": self.fetch_tool,
            "html_writer": self.html_tool,
        }

    def _make_agent(self, skill_name: str, tools: dict | None = None) -> BaseAgent:
        """Create an agent for a specific pipeline step."""
        lang = os.environ.get("SKILL_LANG", "zh")
        skill_path = self.skills_dir / skill_name / f"SKILL.{lang}.md"
        if not skill_path.exists():
            skill_path = self.skills_dir / skill_name / "SKILL.zh.md"
        return BaseAgent(
            llm=self.llm,
            skill_path=skill_path,
            tool_instances=tools,
        )

    def _save_step_output(self, run_dir: Path, step: str, data: str):
        """Save step output to a JSON file."""
        out_path = run_dir / f"{step}.json"
        out_path.write_text(data, encoding="utf-8")
        logger.info(f"Saved {step} output to {out_path}")

    def _parse_record(self, store: ArtifactStore, step: str, raw: str, *, required: bool = True):
        """Parse, validate, and record one model step output."""
        try:
            parsed = parse_json_output(raw).data
            validation = validate_step(step, parsed)
            store.record(
                step,
                raw=raw,
                parsed=parsed,
                status="completed" if validation.ok else "validation_warning",
                metadata={"validation_errors": validation.errors},
            )
            if required and not validation.ok:
                logger.warning("%s validation warnings: %s", step, validation.errors)
            self._save_step_output(store.run_dir, step, dumps_pretty(parsed))
            return parsed
        except Exception as exc:
            store.record(step, raw=raw, status="error", error=str(exc))
            if required:
                raise
            logger.warning("Could not parse optional step %s: %s", step, exc)
            self._save_step_output(store.run_dir, step, raw)
            return {"raw": raw, "parse_error": str(exc)}

    async def run(
        self,
        topic: str,
        report_paths: list[str] | None = None,
        on_progress: callable = None,
    ) -> dict:
        """
        Execute the full 6-step pipeline.

        Args:
            topic: Investment topic (e.g., "白银")
            report_paths: Optional list of PDF file paths. If empty, Step 1 searches.
            on_progress: Optional callback(step_name, status, detail) for progress updates.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        run_dir = self.output_dir / f"{topic}_{timestamp}"
        run_dir.mkdir(parents=True, exist_ok=True)
        store = ArtifactStore(run_dir)
        self.html_tool.set_allowed_root(run_dir)

        async def progress(step, status, detail=""):
            logger.info(f"[{step}] {status}: {detail}")
            if on_progress:
                result = on_progress(step, status, detail)
                if inspect.isawaitable(result):
                    await result

        results = {}

        # ── Step 1: 搜 ──────────────────────────────────────────
        await progress("s1_search", "started")
        if report_paths:
            reports_parsed = {
                "topic": topic,
                "reports": [
                    {"file_path": p, "id": Path(p).stem} for p in report_paths
                ],
            }
            reports_data = dumps_pretty(reports_parsed)
            store.record("s1_search", raw=reports_data, parsed=reports_parsed, status="skipped")
            await progress("s1_search", "skipped", "Reports provided by user")
        else:
            agent = self._make_agent("search", self.search_tools)
            reports_data = await agent.run(
                f"Search for at least 3 diverse research reports on: {topic}"
            )
            reports_parsed = self._parse_record(store, "s1_search", reports_data)
            await progress("s1_search", "completed")
        results["s1"] = reports_data

        # ── Step 2: 读 (parallel per report) ─────────────────────
        await progress("s2_decompose", "started")
        if "reports_parsed" not in locals():
            reports_parsed = self._parse_record(store, "s1_search", reports_data)
        report_list = reports_parsed.get("reports", [])

        async def decompose_one(report: dict) -> str:
            agent = self._make_agent("decompose", self.read_tools)
            return await agent.run(
                f"Decompose this report into pyramid structure.",
                context=report,
            )

        pyramids = await asyncio.gather(
            *[decompose_one(r) for r in report_list]
        )
        pyramid_objects = []
        for i, p in enumerate(pyramids):
            pyramid_objects.append(self._parse_record(store, f"s2_pyramid_{i}", p))
        await progress("s2_decompose", "completed", f"{len(pyramids)} reports decomposed")
        results["s2"] = pyramid_objects

        # ── Step 3: 审 (node-level fan-out verification) ────────────
        await progress("s3_verify", "started")

        async def extract_verify_tasks(pyramid_data: str) -> list[dict]:
            """Extract individual data nodes and causal edges for parallel verification."""
            pyramid = parse_json_output(pyramid_data).data if isinstance(pyramid_data, str) else pyramid_data

            tasks = []
            nodes = pyramid.get("data_points", pyramid.get("reorganized_pyramid", {}).get("trunks", []))

            def walk(node, parent_heading=""):
                if isinstance(node, dict):
                    children = node.get("children", [])
                    heading = node.get("heading", node.get("content", ""))
                    if not children and heading:
                        tasks.append({
                            "type": "data_node",
                            "claim": heading,
                            "id": node.get("id", ""),
                            "source_ref": node.get("source_ref", {}),
                            "original_text": node.get("original_text", ""),
                        })
                    if children and parent_heading and heading:
                        tasks.append({
                            "type": "causal_edge",
                            "claim": f"{parent_heading} → {heading}",
                            "parent": parent_heading,
                            "child": heading,
                        })
                    for c in children:
                        walk(c, heading)
                elif isinstance(node, list):
                    for item in node:
                        walk(item, parent_heading)

            walk(nodes)
            return tasks if tasks else [{"type": "full_pyramid", "claim": "Verify all nodes", "data": pyramid}]

        async def verify_single_item(item: dict, report_meta: dict) -> str:
            """One sub-agent verifies one data node or causal edge."""
            agent = self._make_agent("verify", self.verify_tools)
            task_desc = (
                f"Verify this {item['type']}:\n"
                f"Claim: {item['claim']}\n"
                f"Report publish date: {report_meta.get('publish_date', 'unknown')}"
            )
            return await agent.run(task_desc, context=item)

        all_verified = []
        for i, p in enumerate(pyramids):
            pyramid = pyramid_objects[i]
            meta = pyramid.get("metadata", {})
            verify_tasks = await extract_verify_tasks(p)
            await progress("s3_verify", "started", f"Report {i+1}: {len(verify_tasks)} verification tasks")

            results_per_report = await asyncio.gather(
                *[verify_single_item(t, meta) for t in verify_tasks]
            )
            verified_report = {
                "report_id": meta.get("title", f"report_{i}"),
                "verifications": list(results_per_report),
            }
            verified_json = dumps_pretty(verified_report)
            parsed_verified = self._parse_record(store, f"s3_verified_{i}", verified_json)
            all_verified.append(parsed_verified)

        total_tasks = 0
        for p in pyramids:
            total_tasks += len(await extract_verify_tasks(p))
        await progress("s3_verify", "completed", f"{len(pyramids)} reports, {total_tasks} sub-agents total")
        results["s3"] = all_verified
        verified = all_verified

        # ── Step 4: 沉 (source registry + exploration) ─────────────
        await progress("s4_distill", "started")
        registry_agent = self._make_agent("distill-registry", self.verify_tools)
        registry_raw = await registry_agent.run(
            "Distill verified reports into a source registry and core judgments.",
            context={"verified_trees": verified},
        )
        registry = self._parse_record(store, "s4_distill_registry", registry_raw, required=False)

        explore_agent = self._make_agent("distill-explore", self.verify_tools)
        explore_raw = await explore_agent.run(
            "Explore the source registry and identify reusable data dimensions.",
            context={"source_registry": registry},
        )
        source_map = self._parse_record(store, "s4_distill_explore", explore_raw, required=False)
        await progress("s4_distill", "completed")
        results["s4_distill"] = {"registry": registry, "source_map": source_map}

        # ── Step 5: 合 ───────────────────────────────────────────
        await progress("s5_merge", "started")
        agent = self._make_agent("merge")
        merged = await agent.run(
            f"Merge these {len(verified)} verified pyramids into a consensus tree.",
            context={"verified_trees": verified, "source_registry": registry, "source_map": source_map},
        )
        merged_obj = self._parse_record(store, "s5_merged", merged, required=False)
        await progress("s5_merge", "completed")
        results["s5_merge"] = merged_obj

        # ── Step 6: 图 ───────────────────────────────────────────
        await progress("s6_visualize", "started")
        agent = self._make_agent("visualize", self.write_tools)
        viz_result = await agent.run(
            "Generate markmap HTML visualizations for all pyramids and the merged tree.",
            context={
                "pyramids": pyramid_objects,
                "verified": verified,
                "merged": merged_obj,
                "output_dir": str(run_dir),
            },
        )
        store.record("s6_visualize", raw=viz_result, status="completed")
        await progress("s6_visualize", "completed")
        results["s6_visualize"] = viz_result

        # ── Step 7: 追 ───────────────────────────────────────────
        await progress("s7_dashboard", "started")
        agent = self._make_agent("dashboard", self.dashboard_tools)
        dashboard = await agent.run(
            f"Generate a forward monitoring dashboard for: {topic}",
            context={
                "merged": merged_obj,
                "source_registry": registry,
                "output_dir": str(run_dir),
            },
        )
        store.record("s7_dashboard", raw=dashboard, status="completed")
        await progress("s7_dashboard", "completed")
        results["s7_dashboard"] = dashboard

        await progress("pipeline", "completed", f"All outputs in {run_dir}")
        return {
            "run_dir": str(run_dir),
            "topic": topic,
            "steps": results,
        }
