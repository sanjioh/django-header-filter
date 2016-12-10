# -*- coding: utf-8 -*-
from django.conf import settings
from django.http import HttpResponse

from .compat import MiddlewareMixin


class HeaderFilterMiddleware(MiddlewareMixin):
    def _reject(self, status, reason):
        return HttpResponse(status=status, reason=reason)

    def _all(self, group, request):
        rule_headers, _ = zip(*group)
        rule_headers = set(rule_headers)
        request_headers = set(request.META.keys())

        if not rule_headers.issubset(request_headers):
            return False

        for header, value in group:
            if callable(value):
                if not value(request):
                    return False
            elif request.META[header] != value:
                return False

        return True

    def _do_enforce(self, rule, request):
        group_name = settings.HEADER_FILTER_RULES[0]['HEADERS']
        group = settings.HEADER_FILTER_GROUPS[group_name]
        status, reason = settings.HEADER_FILTER_RULES[0]['RESPONSE']
        return None if self._all(group, request) else self._reject(status, reason)

    def process_request(self, request):
        rule = settings.HEADER_FILTER_RULES[0]
        action = settings.HEADER_FILTER_RULES[0]['ACTION']
        return getattr(self, '_do_' + action)(rule, request)
