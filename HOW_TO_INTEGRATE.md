# MultiShop Chatbot — Integration Steps

## 1. Install the Anthropic SDK
```
pip install anthropic
```
Add `anthropic` to `requirements.txt`.

## 2. Set your API key (never hard-code it)
```bash
export ANTHROPIC_API_KEY=sk-ant-...
```
Or add to `.env` if you use `python-decouple` / `django-environ`:
```
ANTHROPIC_API_KEY=sk-ant-...
```

## 3. Add the Django view
Paste `chat_view.py` contents into your app's `views.py`.

## 4. Wire up the URL
In your app's `urls.py`:
```python
from django.urls import path
from .views import chat_view

urlpatterns = [
    # ... your existing routes ...
    path('api/chat/', chat_view, name='chat'),
]
```

## 5. Copy the widget file
```
chatbot-widget.js  →  yourapp/static/js/chatbot-widget.js
```

## 6. Add ONE line to base.html
Just before `</body>` (after the existing scripts), add:
```html
<script src="{% static 'js/chatbot-widget.js' %}"></script>
```

Then run:
```
python manage.py collectstatic
```

## 7. Test without a backend (optional dev shortcut)
In `chatbot-widget.js` set:
```js
var USE_DJANGO_BACKEND = false;
var ANTHROPIC_API_KEY  = 'sk-ant-your-key';
```
This calls the Anthropic API directly from the browser — fine for local dev,
but switch back to `true` before deploying (keeps your key server-side).

---
That's it. The widget appears as a blue floating button bottom-right on every page.