from __future__ import unicode_literals

from django.conf import settings
from django.http import HttpResponse

from .compat import MiddlewareMixin


class HeaderFilterMiddleware(MiddlewareMixin):
    def _reject(self, status, reason):
        return HttpResponse(status=status, reason=reason)

    def process_request(self, request):
        group = settings.HEADER_FILTER_RULES[0]['HEADERS']
        rule_header, rule_value = settings.HEADER_FILTER_GROUPS[group][0]
        status, reason = settings.HEADER_FILTER_RULES[0]['RESPONSE']
        if rule_header not in request.META:
            return self._reject(status, reason)
        if callable(rule_value):
            return None if rule_value(request) else self._reject(status, reason)
        if request.META[rule_header] != rule_value:
            return self._reject(status, reason)
