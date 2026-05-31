"""Tool registry: maps tool names to instances and provides Anthropic tool definitions."""
from __future__ import annotations

from .web_search import WebSearchTool
from .web_fetch import WebFetchTool
from .pdf_reader import PDFReaderTool
from .html_writer import HTMLWriterTool

TOOL_CLASSES = [WebSearchTool, WebFetchTool, PDFReaderTool, HTMLWriterTool]

TOOL_REGISTRY: dict[str, type] = {cls.name: cls for cls in TOOL_CLASSES}


def get_tool_definitions(names: list[str] | None = None) -> list[dict]:
    """Return Anthropic-format tool definitions for the given tool names."""
    definitions = []
    for cls in TOOL_CLASSES:
        if names and cls.name not in names:
            continue
        definitions.append(
            {
                "name": cls.name,
                "description": cls.description,
                "input_schema": cls.input_schema,
            }
        )
    return definitions
