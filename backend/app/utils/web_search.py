import asyncio
from urllib.parse import urlparse

from ddgs import DDGS

from app.core.config import get_settings

settings = get_settings()


def _search_sync(query: str) -> list[dict[str, str]]:
    results = DDGS().text(query, max_results=settings.web_search_max_results)
    normalized = []
    for result in results:
        title = (result.get("title") or "").strip()
        url = (result.get("href") or result.get("url") or "").strip()
        snippet = (result.get("body") or result.get("snippet") or "").strip()
        if title and urlparse(url).scheme in {"http", "https"}:
            normalized.append(
                {"title": title, "url": url, "snippet": snippet[:1000]}
            )
    return normalized[: settings.web_search_max_results]


async def web_search(query: str) -> list[dict[str, str]]:
    query = query.strip()
    if not query or len(query) > 500:
        raise ValueError("Search query must contain 1 to 500 characters.")
    return await asyncio.to_thread(_search_sync, query)