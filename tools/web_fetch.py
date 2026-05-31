"""Fetch and extract text content from a URL."""
import httpx
import re


class WebFetchTool:
    name = "web_fetch"
    description = "Fetch a web page and extract its text content."
    input_schema = {
        "type": "object",
        "properties": {
            "url": {
                "type": "string",
                "description": "URL to fetch",
            },
            "max_length": {
                "type": "integer",
                "description": "Maximum characters to return (default 5000)",
                "default": 5000,
            },
        },
        "required": ["url"],
    }

    async def execute(self, url: str, max_length: int = 5000) -> str:
        headers = {
            "User-Agent": "Mozilla/5.0 (Research Agent; +https://github.com/KDLD)"
        }
        async with httpx.AsyncClient(timeout=30, follow_redirects=True) as client:
            resp = await client.get(url, headers=headers)
            resp.raise_for_status()
            html = resp.text

        text = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.DOTALL)
        text = re.sub(r"<style[^>]*>.*?</style>", "", text, flags=re.DOTALL)
        text = re.sub(r"<[^>]+>", " ", text)
        text = re.sub(r"\s+", " ", text).strip()

        return text[:max_length]
