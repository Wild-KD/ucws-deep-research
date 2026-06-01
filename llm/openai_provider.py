"""
OpenAI-compatible API provider.
Works with OpenAI GPT, MiroMind, and any OpenAI-compatible endpoint.
"""
from __future__ import annotations

import json
import httpx
from llm.base import LLMProvider, LLMResponse, ToolCall
from config import LLMConfig


class OpenAIProvider(LLMProvider):
    """Covers OpenAI GPT + any OpenAI-compatible API (MiroMind, etc.)."""
    message_format = "openai"

    def __init__(self, config: LLMConfig):
        self.config = config
        self.base_url = (config.base_url or "https://api.openai.com/v1").rstrip("/")
        self.headers = {
            "Authorization": f"Bearer {config.api_key}",
            "Content-Type": "application/json",
        }

    async def chat(
        self,
        messages: list[dict],
        system: str = "",
        tools: list[dict] | None = None,
        max_tokens: int = 4096,
        temperature: float = 0.0,
    ) -> LLMResponse:
        api_messages = []
        if system:
            api_messages.append({"role": "system", "content": system})
        api_messages.extend(messages)

        body: dict = {
            "model": self.config.model,
            "messages": api_messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
        if tools:
            body["tools"] = self._convert_tools(tools)

        async with httpx.AsyncClient(timeout=120) as client:
            resp = await client.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=body,
            )
            resp.raise_for_status()
            data = resp.json()

        choice = data["choices"][0]
        msg = choice["message"]

        content = msg.get("content", "") or ""
        tool_calls = []
        for tc in msg.get("tool_calls") or []:
            tool_calls.append(
                ToolCall(
                    id=tc["id"],
                    name=tc["function"]["name"],
                    input=json.loads(tc["function"]["arguments"]),
                )
            )

        return LLMResponse(
            content=content,
            tool_calls=tool_calls,
            stop_reason=choice.get("finish_reason", "stop"),
            usage=data.get("usage", {}),
        )

    @staticmethod
    def _convert_tools(anthropic_tools: list[dict]) -> list[dict]:
        """Convert Anthropic tool format to OpenAI function-calling format."""
        openai_tools = []
        for t in anthropic_tools:
            openai_tools.append(
                {
                    "type": "function",
                    "function": {
                        "name": t["name"],
                        "description": t.get("description", ""),
                        "parameters": t.get("input_schema", {}),
                    },
                }
            )
        return openai_tools
