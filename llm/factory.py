"""Factory to create the right LLM provider from config."""
from __future__ import annotations

from config import LLMConfig
from llm.base import LLMProvider


def create_provider(config: LLMConfig) -> LLMProvider:
    if config.provider == "anthropic":
        from llm.anthropic_provider import AnthropicProvider
        return AnthropicProvider(config)
    elif config.provider in ("openai", "miromind"):
        from llm.openai_provider import OpenAIProvider
        return OpenAIProvider(config)
    else:
        raise ValueError(f"Unknown LLM provider: {config.provider}")
