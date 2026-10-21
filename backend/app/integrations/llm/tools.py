import json

from app.utils.web_search import web_search

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
                    "description": "Consulta que se enviará al buscador.",
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
