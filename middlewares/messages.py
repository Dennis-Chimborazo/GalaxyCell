from django.template.loader import render_to_string
from django.contrib import messages

class HtmxMessageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.headers.get('HX-Request'):
            # Si la respuesta redirige, no toques los mensajes para que pasen al Dashboard
            if response.status_code in [301, 302] or response.has_header('HX-Redirect'):
                return response

            storage = messages.get_messages(request)
            if storage:
                messages_html = render_to_string('shared/ui/message.html', {'messages': storage}, request=request)
                
                if "text/html" in response.get("Content-Type", ""):
                    content = response.content.decode(response.charset)
                    response.content = (content + messages_html).encode(response.charset)
                
        return response