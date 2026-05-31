"""Web search tool using Tavily API."""
import httpx


class WebSearchTool:
    name = "web_search"
    description = "Search the web for information. Returns titles, URLs, and snippets."
    input_schema = {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Search query",
            },
            "max_results": {
                "type": "integer",
                "description": "Maximum number of results (default 5)",
                "default": 5,
            },
        },
        "required": ["query"],
    }

    def __init__(self, api_key: str):
        self.api_key = api_key

    async def execute(self, query: str, max_results: int = 5) -> str:
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(
                "https://api.tavily.com/search",
                json={
                    "api_key": self.api_key,
                    "query": query,
                    "max_results": max_results,
                    "include_raw_content": False,
                },
            )
            resp.raise_for_status()
            data = resp.json()

        results = []
        for r in data.get("results", []):
            results.append(
                f"Title: {r['title']}\nURL: {r['url']}\nSnippet: {r['content']}\n"
            )
        return "\n---\n".join(results) if results else "No results found."
