from unittest.mock import MagicMock, patch

import pytest

from app.utils.web_search import web_search


@pytest.mark.asyncio
async def test_web_search_normalizes_and_limits_results():
    results = [
        {
            "title": "Example",
            "href": "https://example.com",
            "body": "A useful result",
        },
        {"title": "Unsafe", "href": "javascript:alert(1)", "body": "Skip"},
    ]
    mock_ddgs = MagicMock()
    mock_ddgs.text.return_value = results

    with patch("app.utils.web_search.DDGS", return_value=mock_ddgs):
        response = await web_search("  current news  ")

    assert response == [
        {
            "title": "Example",
            "url": "https://example.com",
            "snippet": "A useful result",
        }
    ]
    mock_ddgs.text.assert_called_once_with("current news", max_results=5)


@pytest.mark.asyncio
@pytest.mark.parametrize("query", ["", " " , "x" * 501])
async def test_web_search_rejects_invalid_query(query):
    with pytest.raises(ValueError):
        await web_search(query)