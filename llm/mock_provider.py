"""Deterministic offline LLM provider for harness tests and replay demos."""
from __future__ import annotations

from config import LLMConfig
from llm.base import LLMProvider, LLMResponse


class MockProvider(LLMProvider):
    """Returns stable JSON without network calls."""

    message_format = "openai"

    def __init__(self, config: LLMConfig):
        self.config = config

    async def chat(
        self,
        messages: list[dict],
        system: str = "",
        tools: list[dict] | None = None,
        max_tokens: int = 4096,
        temperature: float = 0.0,
    ) -> LLMResponse:
        user_text = "\n".join(str(m.get("content", "")) for m in messages if m.get("role") in ("user", "tool"))
        lowered = (system + "\n" + user_text).lower()

        if "decompose" in lowered or "金字塔" in lowered or "拆解" in lowered:
            content = '{"metadata":{"title":"Mock Silver Report","publish_date":"2026-01-01"},"original_pyramid":{"conclusion":"Silver thesis depends on supply deficit."},"reorganized_pyramid":{"trunks":[{"id":"T1","heading":"Supply deficit tightens physical silver","children":[{"id":"D1","heading":"Mine supply is slow to respond","source_ref":{"page":1},"original_text":"Mine supply lags price."}]}]},"data_points":[{"id":"D1","content":"Mine supply is slow to respond","source_ref":{"page":1},"original_text":"Mine supply lags price."}]}'
        elif "search" in lowered or "搜索" in lowered:
            content = '{"topic":"silver","reports":[{"id":"mock_report","file_path":"mock_report.pdf","title":"Mock Silver Report","publish_date":"2026-01-01"}]}'
        elif "verify" in lowered or "验证" in lowered:
            content = '{"verifications":[{"node_id":"D1","type":"data_node","claim":"Mine supply is slow to respond","color":"green","sources":[{"url":"https://example.com/source","title":"Mock source","finding":"Confirmed"}],"workpaper":{"conclusion":"Mock verified."}}]}'
        elif "distill" in lowered or "沉淀" in lowered or "source registry" in lowered:
            content = '{"sources":[{"name":"Mock source","url":"https://example.com/source","provides":["supply"]}],"core_judgments":["Supply response is slow."]}'
        elif "merge" in lowered or "合并" in lowered:
            content = '{"thesis":"Silver upside is driven by tight physical supply.","merged_tree":{"WHY":["Supply response is slow"],"HOW":["Inventory tightness transmits into price"],"RISK":["Demand shock"]}}'
        else:
            content = "<html><body><h1>Mock output</h1></body></html>"

        return LLMResponse(content=content, usage={"input_tokens": 0, "output_tokens": 0})
