from django.conf import settings

from .compat import MiddlewareMixin


class HeaderFilterMiddleware(MiddlewareMixin):
    def _process_enforce(self, request_headers, rule_headers):
        headers_set = set(request_headers.keys())


    def process_request(self, request):
        # request_headers = request.META
        # for rule in settings.HEADER_FILTER_RULES:
        #     rule_action, rule_headers, rule_response = rule['ACTION'], rule['HEADERS'], rule['RESPONSE']
        #     getattr(self, '_process_' + rule_action)(request_headers, rule_headers)

        pass
