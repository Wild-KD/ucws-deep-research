"""
Pipeline Orchestrator: runs the 6-step research pipeline.
搜 → 读 → 审 → 合 → 图 → 讲
"""
from __future__ import annotations

import asyncio
import inspect
import json
import logging
import os
from pathlib import Path
from datetime import datetime

from core.agent import BaseAgent
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
            reports_data = json.dumps(
                {
                    "topic": topic,
                    "reports": [
                        {"file_path": p, "id": Path(p).stem} for p in report_paths
                    ],
                },
                ensure_ascii=False,
            )
            await progress("s1_search", "skipped", "Reports provided by user")
        else:
            agent = self._make_agent("search", self.search_tools)
            reports_data = await agent.run(
                f"Search for at least 3 diverse research reports on: {topic}"
            )
            self._save_step_output(run_dir, "s1_search", reports_data)
            await progress("s1_search", "completed")
        results["s1"] = reports_data

        # ── Step 2: 读 (parallel per report) ─────────────────────
        await progress("s2_decompose", "started")
        report_list = json.loads(reports_data).get("reports", [])

        async def decompose_one(report: dict) -> str:
            agent = self._make_agent("decompose", self.read_tools)
            return await agent.run(
                f"Decompose this report into pyramid structure.",
                context=report,
            )

        pyramids = await asyncio.gather(
            *[decompose_one(r) for r in report_list]
        )
        for i, p in enumerate(pyramids):
            self._save_step_output(run_dir, f"s2_pyramid_{i}", p)
        await progress("s2_decompose", "completed", f"{len(pyramids)} reports decomposed")
        results["s2"] = pyramids

        # ── Step 3: 审 (fan-out verification) ─────────────────────
        await progress("s3_verify", "started")

        async def verify_one(pyramid_data: str) -> str:
            agent = self._make_agent("verify", self.verify_tools)
            return await agent.run(
                "Verify all data nodes and causal edges in this pyramid.",
                context=json.loads(pyramid_data) if isinstance(pyramid_data, str) else pyramid_data,
            )

        verified = await asyncio.gather(
            *[verify_one(p) for p in pyramids]
        )
        for i, v in enumerate(verified):
            self._save_step_output(run_dir, f"s3_verified_{i}", v)
        await progress("s3_verify", "completed", f"{len(verified)} reports verified")
        results["s3"] = verified

        # ── Step 4: 合 ───────────────────────────────────────────
        await progress("s4_merge", "started")
        agent = self._make_agent("merge")
        merged = await agent.run(
            f"Merge these {len(verified)} verified pyramids into a consensus tree.",
            context={"verified_trees": [json.loads(v) if isinstance(v, str) else v for v in verified]},
        )
        self._save_step_output(run_dir, "s4_merged", merged)
        await progress("s4_merge", "completed")
        results["s4"] = merged

        # ── Step 5: 图 ───────────────────────────────────────────
        await progress("s5_visualize", "started")
        agent = self._make_agent("visualize", self.write_tools)
        viz_result = await agent.run(
            "Generate markmap HTML visualizations for all pyramids and the merged tree.",
            context={
                "pyramids": [json.loads(p) if isinstance(p, str) else p for p in pyramids],
                "verified": [json.loads(v) if isinstance(v, str) else v for v in verified],
                "merged": json.loads(merged) if isinstance(merged, str) else merged,
                "output_dir": str(run_dir),
            },
        )
        await progress("s5_visualize", "completed")
        results["s5"] = viz_result

        # ── Step 6: 讲 ───────────────────────────────────────────
        await progress("s6_dashboard", "started")
        agent = self._make_agent("dashboard", self.dashboard_tools)
        dashboard = await agent.run(
            f"Generate a forward monitoring dashboard for: {topic}",
            context={
                "merged": json.loads(merged) if isinstance(merged, str) else merged,
                "output_dir": str(run_dir),
            },
        )
        await progress("s6_dashboard", "completed")
        results["s6"] = dashboard

        await progress("pipeline", "completed", f"All outputs in {run_dir}")
        return {
            "run_dir": str(run_dir),
            "topic": topic,
            "steps": results,
        }
