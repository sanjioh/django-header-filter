from django.conf import settings
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views import View

from header_filter import header_rules


class RuleIterable:
    def __iter__(self):
        return iter(settings.HEADER_FILTER_RULES)


def middleware_test_fbv(request):
    return HttpResponse()


@header_rules(RuleIterable())
def decorator_test_fbv(request):
    return HttpResponse()


class DecoratorTestCBV(View):
    @method_decorator(header_rules(RuleIterable()))
    def get(self, request, *args, **kwargs):
        return HttpResponse()
