"""Write HTML files to disk."""
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

    async def execute(self, file_path: str, content: str) -> str:
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return f"Written {len(content)} chars to {file_path}"
