from collections.abc import AsyncGenerator
from typing import Any

from app.core.config import get_settings
from app.core.exceptions import LLMNotAvailableError
from app.integrations.llm.client import client
from app.integrations.llm.tools import WEB_SEARCH_TOOL, execute_tool

settings = get_settings()


async def generate_response(messages: list[dict[str, Any]]) -> str:
    try:
        for _ in range(settings.llm_max_tool_calls + 1):
            response = await client.chat.completions.create(
                model=settings.llm_model,
                messages=messages,
                tools=[WEB_SEARCH_TOOL],
                tool_choice="auto",
            )

            assistant_message = response.choices[0].message

            if not assistant_message.tool_calls:
                return assistant_message.content or ""

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
        response = await client.chat.completions.create(
            model=settings.llm_model,
            messages=messages,
            stream=True,
        )
        async for chunk in response:
            delta = chunk.choices[0].delta.content
            if delta:
                yield delta
    except LLMNotAvailableError:
        raise
    except Exception as exc:
        raise LLMNotAvailableError() from exc
