"""
Configuration for the Investment Research Logic Engine.
Supports multiple LLM providers: Anthropic (Claude), OpenAI (GPT), MiroMind.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field


@dataclass
class LLMConfig:
    provider: str = "anthropic"  # "anthropic" | "openai" | "miromind" | "mock"
    model: str = "claude-sonnet-4-6"
    api_key: str = ""
    base_url: str | None = None
    max_tokens: int = 4096
    temperature: float = 0.0

    @classmethod
    def from_env(cls, provider: str | None = None) -> "LLMConfig":
        provider = provider or os.getenv("LLM_PROVIDER", "anthropic")

        if provider == "mock":
            return cls(provider="mock", model="mock-deterministic", api_key="mock")
        elif provider == "anthropic":
            return cls(
                provider="anthropic",
                model=os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-6"),
                api_key=os.getenv("ANTHROPIC_API_KEY", ""),
                base_url=os.getenv("ANTHROPIC_BASE_URL"),
            )
        elif provider == "openai":
            return cls(
                provider="openai",
                model=os.getenv("OPENAI_MODEL", "gpt-4o"),
                api_key=os.getenv("OPENAI_API_KEY", ""),
                base_url=os.getenv("OPENAI_BASE_URL"),
            )
        elif provider == "miromind":
            return cls(
                provider="miromind",
                model=os.getenv("MIROMIND_MODEL", "miromind-deep-research"),
                api_key=os.getenv("MIROMIND_API_KEY", ""),
                base_url=os.getenv(
                    "MIROMIND_BASE_URL", "https://platform.miromind.ai/v1"
                ),
            )
        else:
            raise ValueError(f"Unknown provider: {provider}")


@dataclass
class ToolsConfig:
    tavily_api_key: str = field(
        default_factory=lambda: os.getenv("TAVILY_API_KEY", "")
    )
    search_max_results: int = 5


@dataclass
class Config:
    llm: LLMConfig = field(default_factory=LLMConfig.from_env)
    tools: ToolsConfig = field(default_factory=ToolsConfig)
    skills_dir: str = "skills"
    output_dir: str = "output"
    demo_dir: str = "demo"
