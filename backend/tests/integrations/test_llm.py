import json
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import pytest

from app.core.exceptions import LLMNotAvailableError
from app.integrations.llm import chat
from app.integrations.llm.tools import execute_tool


@pytest.mark.asyncio
async def test_generate_response_returns_assistant_content():
    assistant_message = SimpleNamespace(content="Hello", tool_calls=None)
    response = SimpleNamespace(
        choices=[SimpleNamespace(message=assistant_message)]
    )

    with patch.object(
        chat.client.chat.completions,
        "create",
        new=AsyncMock(return_value=response),
    ) as create:
        result = await chat.generate_response([{"role": "user", "content": "Hi"}])

    assert result == "Hello"
    create.assert_awaited_once()
    assert create.await_args.kwargs["tools"] == [chat.WEB_SEARCH_TOOL]
    assert create.await_args.kwargs["tool_choice"] == "auto"


@pytest.mark.asyncio
async def test_generate_response_executes_tool_and_continues():
    tool_call = SimpleNamespace(
        id="call-1",
        function=SimpleNamespace(name="web_search", arguments='{"query":"cats"}'),
    )
    tool_message = SimpleNamespace(
        content=None,
        tool_calls=[tool_call],
        model_dump=lambda **_: {"role": "assistant", "tool_calls": []},
    )
    final_message = SimpleNamespace(content="Search complete", tool_calls=None)
    responses = [
        SimpleNamespace(choices=[SimpleNamespace(message=tool_message)]),
        SimpleNamespace(choices=[SimpleNamespace(message=final_message)]),
    ]
    messages = [{"role": "user", "content": "Find cats"}]

    with (
        patch.object(
            chat.client.chat.completions,
            "create",
            new=AsyncMock(side_effect=responses),
        ) as create,
        patch(
            "app.integrations.llm.chat.execute_tool",
            new=AsyncMock(return_value='[{"title":"Cats"}]'),
        ) as execute,
    ):
        result = await chat.generate_response(messages)

    assert result == "Search complete"
    execute.assert_awaited_once_with("web_search", '{"query":"cats"}')
    assert messages[-1] == {
        "role": "tool",
        "tool_call_id": "call-1",
        "content": '[{"title":"Cats"}]',
    }
    assert create.await_count == 2


@pytest.mark.asyncio
async def test_generate_response_wraps_provider_error():
    with patch.object(
        chat.client.chat.completions,
        "create",
        new=AsyncMock(side_effect=RuntimeError("provider unavailable")),
    ):
        with pytest.raises(LLMNotAvailableError):
            await chat.generate_response([{"role": "user", "content": "Hi"}])


@pytest.mark.asyncio
async def test_stream_response_yields_text_deltas():
    async def response_stream():
        for text in ("Hello", " world"):
            yield SimpleNamespace(
                choices=[SimpleNamespace(delta=SimpleNamespace(content=text))]
            )
            yield SimpleNamespace(
                choices=[SimpleNamespace(delta=SimpleNamespace(content=None))]
            )

    with patch.object(
        chat.client.chat.completions,
        "create",
        new=AsyncMock(return_value=response_stream()),
    ) as create:
        result = [
            delta
            async for delta in chat.stream_response(
                [{"role": "user", "content": "Hi"}]
            )
        ]

    assert result == ["Hello", " world"]
    assert create.await_args.kwargs["stream"] is True


@pytest.mark.asyncio
async def test_execute_tool_serializes_search_results():
    with patch(
        "app.integrations.llm.tools.web_search",
        new=AsyncMock(return_value=[{"title": "Cats"}]),
    ) as search:
        result = await execute_tool("web_search", '{"query":"cats"}')

    assert json.loads(result) == [{"title": "Cats"}]
    search.assert_awaited_once_with("cats")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("name", "arguments"),
    [
        ("unknown", "{}"),
        ("web_search", "invalid json"),
        ("web_search", "[]"),
        ("web_search", '{"query": 42}'),
    ],
)
async def test_execute_tool_rejects_invalid_calls(name, arguments):
    with pytest.raises(ValueError):
        await execute_tool(name, arguments)
