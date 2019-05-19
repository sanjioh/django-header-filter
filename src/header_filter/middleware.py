from django.conf import settings


class HeaderFilterMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        rules = getattr(settings, 'HEADER_FILTER_RULES', [])
        for rule in rules:
            response = rule.process(request)
            if response:
                return response
        return self.get_response(request)
