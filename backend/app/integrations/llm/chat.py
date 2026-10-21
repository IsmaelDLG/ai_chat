from collections.abc import AsyncGenerator
from typing import Any

from app.core.config import get_settings
from app.core.exceptions import LLMNotAvailableError
from app.integrations.llm.client import client
from app.integrations.llm.tools import WEB_SEARCH_TOOL, execute_tool

settings = get_settings()


async def generate_response(messages: list[dict[str, Any]]) -> str:
    try:
        for tool_round in range(settings.llm_max_tool_calls + 1):
            response = await client.chat.completions.create(
                model=settings.llm_model,
                messages=messages,
                tools=[WEB_SEARCH_TOOL],
                tool_choice="auto",
            )

            assistant_message = response.choices[0].message

            if not assistant_message.tool_calls:
                return assistant_message.content or ""

            if tool_round == settings.llm_max_tool_calls:
                raise RuntimeError("Maximum tool rounds exceeded")

            messages.append(assistant_message.model_dump(exclude_none=True))

            for tool_call in assistant_message.tool_calls:
                result = await execute_tool(
                    tool_call.function.name,
                    tool_call.function.arguments,
                )
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result,
                    }
                )

        raise RuntimeError("Maximum tool rounds exceeded")

    except LLMNotAvailableError:
        raise
    except Exception as exc:
        raise LLMNotAvailableError() from exc


async def stream_response(
    messages: list[dict[str, Any]],
) -> AsyncGenerator[str, None]:
    try:
        for tool_round in range(settings.llm_max_tool_calls + 1):
            response = await client.chat.completions.create(
                model=settings.llm_model,
                messages=messages,
                tools=[WEB_SEARCH_TOOL],
                tool_choice="auto",
                stream=True,
            )

            tool_calls: dict[int, dict[str, Any]] = {}
            assistant_content: list[str] = []

            async for chunk in response:
                delta = chunk.choices[0].delta
                if delta.content:
                    assistant_content.append(delta.content)
                    yield delta.content

                for tool_call_delta in getattr(delta, "tool_calls", None) or []:
                    tool_call = tool_calls.setdefault(
                        tool_call_delta.index,
                        {
                            "id": "",
                            "type": "function",
                            "function": {"name": "", "arguments": ""},
                        },
                    )
                    if tool_call_delta.id:
                        tool_call["id"] = tool_call_delta.id
                    if tool_call_delta.type:
                        tool_call["type"] = tool_call_delta.type

                    function_delta = tool_call_delta.function
                    if function_delta:
                        if function_delta.name:
                            tool_call["function"]["name"] += function_delta.name
                        if function_delta.arguments:
                            tool_call["function"]["arguments"] += (
                                function_delta.arguments
                            )

            if not tool_calls:
                return

            if tool_round == settings.llm_max_tool_calls:
                raise RuntimeError("Maximum tool rounds exceeded")

            assistant_tool_calls = [
                tool_calls[index] for index in sorted(tool_calls)
            ]
            if any(
                not tool_call["id"] or not tool_call["function"]["name"]
                for tool_call in assistant_tool_calls
            ):
                raise ValueError("Incomplete tool call in streamed response")

            messages.append(
                {
                    "role": "assistant",
                    "content": "".join(assistant_content) or None,
                    "tool_calls": assistant_tool_calls,
                }
            )

            for tool_call in assistant_tool_calls:
                result = await execute_tool(
                    tool_call["function"]["name"],
                    tool_call["function"]["arguments"],
                )
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call["id"],
                        "content": result,
                    }
                )

        raise RuntimeError("Maximum tool rounds exceeded")
    except LLMNotAvailableError:
        raise
    except Exception as exc:
        raise LLMNotAvailableError() from exc
