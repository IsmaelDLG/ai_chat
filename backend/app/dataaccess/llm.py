from typing import Any
import json
from openai import AsyncOpenAI

from app.core.config import get_settings
from app.utils.web_search import web_search
from app.core.exceptions import LLMNotAvailableError

settings = get_settings()

client = AsyncOpenAI(
    base_url=settings.llm_base_url,
    api_key=settings.llm_api_key,
)

WEB_SEARCH_TOOL = {
    "type": "function",
    "function": {
        "name": "web_search",
        "description": (
            "Busca información en Internet para responder preguntas "
            "que requieran información actual o fuentes externas."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Consulta que se enviará al buscador."
                }
            },
            "required": ["query"],
            "additionalProperties": False,
        },
    },
}

async def execute_tool(name: str, arguments: str) -> str:
    if name != "web_search":
        raise ValueError(f"Unknown tool: {name}")

    try:
        parsed = json.loads(arguments)
    except json.JSONDecodeError as exc:
        raise ValueError("Invalid tool arguments") from exc

    if not isinstance(parsed, dict):
        raise ValueError("Tool arguments must be an object")

    query = parsed.get("query")
    if not isinstance(query, str):
        raise ValueError("Tool query must be a string")

    results = await web_search(query)
    return json.dumps(results, ensure_ascii=False)


async def generate_response(
    messages: list[dict[str, Any]],
) -> str:
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

            messages.append(
                assistant_message.model_dump(exclude_none=True)
            )

            for tool_call in assistant_message.tool_calls:
                result = await execute_tool(
                    tool_call.function.name,
                    tool_call.function.arguments,
                )

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result,
                })

        raise RuntimeError("Maximum tool rounds exceeded")

    except Exception as exc:
        if isinstance(exc, LLMNotAvailableError):
            raise
        raise LLMNotAvailableError() from exc