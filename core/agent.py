"""
BaseAgent: the core agentic loop.
Loads a Skill.md as system prompt, executes tool calls, returns structured output.
"""
from __future__ import annotations

import json
import logging
from pathlib import Path

from llm.base import LLMProvider, LLMResponse
from tools.registry import TOOL_REGISTRY

logger = logging.getLogger(__name__)


class BaseAgent:
    def __init__(
        self,
        llm: LLMProvider,
        skill_path: str | Path,
        tool_instances: dict | None = None,
        max_turns: int = 15,
    ):
        self.llm = llm
        self.system_prompt = self._load_skill(skill_path)
        self.tool_instances = tool_instances or {}
        self.max_turns = max_turns

    @staticmethod
    def _load_skill(path: str | Path) -> str:
        """Load a SKILL.md file, strip YAML frontmatter, return body as system prompt."""
        text = Path(path).read_text(encoding="utf-8")
        if text.startswith("---"):
            parts = text.split("---", 2)
            if len(parts) >= 3:
                return parts[2].strip()
        return text

    def _get_tool_definitions(self) -> list[dict]:
        """Build Anthropic-format tool definitions from registered tool instances."""
        definitions = []
        for name, instance in self.tool_instances.items():
            definitions.append(
                {
                    "name": instance.name,
                    "description": instance.description,
                    "input_schema": instance.input_schema,
                }
            )
        return definitions

    async def _execute_tool(self, name: str, input_data: dict) -> str:
        """Execute a tool by name and return the result as a string."""
        instance = self.tool_instances.get(name)
        if not instance:
            return f"Error: Unknown tool '{name}'"
        try:
            result = await instance.execute(**input_data)
            return str(result)
        except Exception as e:
            logger.error(f"Tool {name} failed: {e}")
            return f"Error executing {name}: {e}"

    async def run(self, task: str, context: dict | None = None) -> str:
        """
        Run the agentic loop:
        1. Send task to LLM with system prompt + tools
        2. If LLM returns tool_use, execute tools and feed results back
        3. Repeat until LLM returns text or max_turns reached
        """
        user_content = task
        if context:
            user_content += f"\n\nContext:\n```json\n{json.dumps(context, ensure_ascii=False, indent=2)}\n```"

        messages = [{"role": "user", "content": user_content}]
        tool_defs = self._get_tool_definitions() if self.tool_instances else None

        for turn in range(self.max_turns):
            logger.info(f"Agent turn {turn + 1}/{self.max_turns}")

            resp = await self.llm.chat(
                messages=messages,
                system=self.system_prompt,
                tools=tool_defs,
                max_tokens=4096,
            )

            if not resp.has_tool_use:
                logger.info("Agent finished (no more tool calls)")
                return resp.content

            # Build assistant message with tool_use blocks
            assistant_content = []
            if resp.content:
                assistant_content.append({"type": "text", "text": resp.content})
            for tc in resp.tool_calls:
                assistant_content.append(
                    {
                        "type": "tool_use",
                        "id": tc.id,
                        "name": tc.name,
                        "input": tc.input,
                    }
                )
            messages.append({"role": "assistant", "content": assistant_content})

            # Execute tools and add results
            tool_results = []
            for tc in resp.tool_calls:
                logger.info(f"  Calling tool: {tc.name}")
                result = await self._execute_tool(tc.name, tc.input)
                tool_results.append(
                    {
                        "type": "tool_result",
                        "tool_use_id": tc.id,
                        "content": result,
                    }
                )
            messages.append({"role": "user", "content": tool_results})

        logger.warning("Agent hit max turns limit")
        return resp.content if resp else ""
