"""Write HTML files to disk."""
from __future__ import annotations

from pathlib import Path


class HTMLWriterTool:
    name = "html_writer"
    description = "Write HTML content to a file."
    input_schema = {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "Output file path",
            },
            "content": {
                "type": "string",
                "description": "HTML content to write",
            },
        },
        "required": ["file_path", "content"],
    }

    def __init__(self, allowed_root: str | Path | None = None):
        self.allowed_root = Path(allowed_root).resolve() if allowed_root else None

    def set_allowed_root(self, allowed_root: str | Path):
        self.allowed_root = Path(allowed_root).resolve()

    async def execute(self, file_path: str, content: str) -> str:
        path = Path(file_path)
        if self.allowed_root:
            resolved = path.resolve()
            try:
                resolved.relative_to(self.allowed_root)
            except ValueError:
                return f"Error: Refusing to write outside allowed root: {self.allowed_root}"
            path = resolved
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return f"Written {len(content)} chars to {file_path}"
