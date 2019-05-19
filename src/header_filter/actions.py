from django.http import HttpResponseBadRequest


class Enforce:
    def __init__(self, matcher, reject_response=None):
        self._matcher = matcher
        self._reject_response = reject_response or HttpResponseBadRequest()

    def process(self, request):
        if self._matcher.match(request):
            return None
        return self._reject_response


class Forbid:
    def __init__(self, matcher, reject_response=None):
        self._matcher = matcher
        self._reject_response = reject_response or HttpResponseBadRequest()

    def process(self, request):
        if not self._matcher.match(request):
            return None
        return self._reject_response
