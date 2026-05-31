"""Custom tools for AURA crews."""
from crewai.tools import BaseTool
import httpx
import os


class WebSearchTool(BaseTool):
    """Search the web using Serper API."""
    name: str = "web_search"
    description: str = "Search the web for current information on any topic."

    def _run(self, query: str) -> str:
        api_key = os.getenv("SERPER_API_KEY")
        if not api_key:
            return f"[Web search unavailable] Query was: {query}"
        try:
            resp = httpx.post(
                "https://google.serper.dev/search",
                headers={"X-API-KEY": api_key, "Content-Type": "application/json"},
                json={"q": query, "num": 5},
                timeout=10,
            )
            data = resp.json()
            results = []
            for item in data.get("organic", [])[:5]:
                results.append(f"- {item.get('title', '')}: {item.get('snippet', '')}")
            return "\n".join(results) if results else "No results found."
        except Exception as e:
            return f"Search error: {e}"


class AirtableTool(BaseTool):
    """Read from Airtable Content Station."""
    name: str = "airtable_read"
    description: str = "Read recent content from Airtable Content Station (Sakluma)."

    def _run(self, action: str = "list") -> str:
        token = os.getenv("AIRTABLE_TOKEN")
        if not token:
            return "[Airtable unavailable — token not set]"
        try:
            resp = httpx.get(
                "https://api.airtable.com/v0/appX8Ug5r1DgckMwx/Content%20Station",
                headers={"Authorization": f"Bearer {token}"},
                params={"maxRecords": 5},
                timeout=10,
            )
            records = resp.json().get("records", [])
            results = []
            for r in records:
                f = r.get("fields", {})
                results.append(f"- {f.get('Title', 'Untitled')} [{f.get('Status', 'Draft')}]")
            return "\n".join(results) if results else "No records."
        except Exception as e:
            return f"Airtable error: {e}"
