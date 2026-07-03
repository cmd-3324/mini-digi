 
# shop/views/chat.py
# pip install openai   (OpenRouter uses the OpenAI-compatible SDK)

import json
from openai import OpenAI
from django.conf import settings
from django.http import JsonResponse
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST

client = OpenAI(
    api_key=settings.OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
)

MODEL = "openrouter/free"   # auto-picks a working free model each request
# Or pin a specific one, e.g.:
# MODEL = "meta-llama/llama-3.3-70b-instruct:free"
# MODEL = "google/gemini-2.0-flash-exp:free"
# MODEL = "deepseek/deepseek-r1:free"


@require_POST
def chat_view(request):
    try:
        body       = json.loads(request.body)
        messages   = body.get("messages", [])[-20:]
        system     = body.get("system", "You are Vex, a helpful shopping assistant.")
        session_id = body.get("session_id", "")

        if not messages:
            return JsonResponse({"error": _("No messages provided.")}, status=400)

        # OpenAI/OpenRouter format needs system as first message in the list
        full_messages = [{"role": "system", "content": system}] + messages

        response = client.chat.completions.create(
            model=MODEL,
            messages=full_messages,
            max_tokens=1024,
            extra_headers={
                # Optional but recommended by OpenRouter for free-tier routing
                "HTTP-Referer": "http://localhost:8000",
                "X-Title": "MultiShop Vex Assistant",
            },
        )

        reply = response.choices[0].message.content
        return JsonResponse({"reply": reply, "session_id": session_id})

    except json.JSONDecodeError:
        return JsonResponse({"error": _("Invalid JSON.")}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=502)