import os

from backend.server import offline_agricultural_expert, query_openai_chat


def handler(request):
    payload = request.get_json() if hasattr(request, "get_json") else {}
    message = str(payload.get("message", "")).strip()
    if not message:
        return {"statusCode": 400, "body": {"error": "Message is required"}}

    api_key = os.getenv("OPENAI_API_KEY", "")
    history = payload.get("history", [])
    if api_key:
        try:
            return {"statusCode": 200, "body": {"reply": query_openai_chat(api_key, message, history), "source": "openai"}}
        except Exception:
            pass
    return {"statusCode": 200, "body": {"reply": offline_agricultural_expert(message), "source": "kisan_ai_offline"}}
