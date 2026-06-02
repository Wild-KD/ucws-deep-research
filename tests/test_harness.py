"""Harness hardening tests."""
from __future__ import annotations

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


def test_extract_json_from_fence():
    from runtime.json_utils import parse_json_output

    parsed = parse_json_output('Here:\n```json\n{"a": 1}\n```')
    assert parsed.data == {"a": 1}
    assert parsed.repaired is True


def test_extract_json_from_prose():
    from runtime.json_utils import parse_json_output

    parsed = parse_json_output('Before {"a": {"b": [1, 2]}} after')
    assert parsed.data["a"]["b"] == [1, 2]


def test_schema_search_report_requires_source():
    from runtime.schemas import validate_step

    result = validate_step("s1_search", {"reports": [{"id": "bad"}]})
    assert result.ok is False
    assert "file_path or url" in result.errors[0]


def test_artifact_store_roundtrip(tmp_path):
    from runtime.artifacts import ArtifactStore

    store = ArtifactStore(tmp_path)
    store.record("s1_search", raw='{"reports":[]}', parsed={"reports": []})
    assert store.load_parsed("s1_search") == {"reports": []}
    assert store.list_steps() == ["s1_search"]


def test_mock_provider_returns_json():
    from config import LLMConfig
    from llm.mock_provider import MockProvider

    async def run():
        provider = MockProvider(LLMConfig(provider="mock"))
        resp = await provider.chat([{"role": "user", "content": "Search for silver"}])
        assert '"reports"' in resp.content

    asyncio.run(run())


def test_openai_tool_message_format(tmp_path):
    from runtime.agent import BaseAgent
    from llm.base import LLMProvider, LLMResponse, ToolCall

    class DummyTool:
        name = "dummy"
        description = "dummy"
        input_schema = {"type": "object", "properties": {}}

        async def execute(self):
            return "ok"

    class DummyOpenAIProvider(LLMProvider):
        message_format = "openai"

        def __init__(self):
            self.calls = []

        async def chat(self, messages, system="", tools=None, max_tokens=4096, temperature=0.0):
            self.calls.append(messages)
            if len(self.calls) == 1:
                return LLMResponse(tool_calls=[ToolCall(id="call_1", name="dummy", input={})])
            assert messages[-1]["role"] == "tool"
            assert messages[-1]["tool_call_id"] == "call_1"
            return LLMResponse(content="done")

    skill = tmp_path / "SKILL.md"
    skill.write_text("system prompt", encoding="utf-8")
    provider = DummyOpenAIProvider()
    agent = BaseAgent(provider, skill, {"dummy": DummyTool()})

    async def run():
        result = await agent.run("task")
        assert result == "done"

    asyncio.run(run())


def test_mock_pipeline_writes_artifacts(tmp_path):
    from config import Config, LLMConfig
    from runtime.harness import PipelineHarness
    from runtime.orchestrator import Orchestrator

    async def run():
        config = Config(
            llm=LLMConfig(provider="mock", model="mock-deterministic", api_key="mock"),
            output_dir=str(tmp_path),
        )
        orchestrator = Orchestrator(config)
        result = await orchestrator.run("mock_silver", report_paths=["mock_report.pdf"])
        run_dir = Path(result["run_dir"])
        assert (run_dir / "_artifacts" / "s1_search.parsed.json").exists()
        assert (run_dir / "_artifacts" / "s2_pyramid_0.parsed.json").exists()
        assert (run_dir / "_artifacts" / "s3_verified_0.parsed.json").exists()
        report = PipelineHarness(run_dir).validate()
        assert report.steps
        assert all(row["ok"] for row in report.steps if row["step"].startswith(("s1", "s2", "s3")))

    asyncio.run(run())
