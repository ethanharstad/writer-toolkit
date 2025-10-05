import json
from .get_url import get_url

tools = [
    {
        "type": "function",
        "name": "get_url",
        "description": "Get the content of a URL.",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "A URL to get content of"
                },
            },
        },
    },
]

function_map = {
    "get_url": get_url
}

def function_handler(response):
    results = []
    for item in response.output:
        if item.type == "function_call":
            try:
                print(f"{item.call_id} Calling {item.name}({item.arguments})")
                result = function_map[item.name](**json.loads(item.arguments))
                results.append({
                    "type": "function_call_output",
                    "call_id": item.call_id,
                    "output": json.dumps(dict(result))
                })
            except KeyError:
                print(f"Tool not found: {item.name}")
    return results
