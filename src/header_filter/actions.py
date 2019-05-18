class Enforce:
    def __init__(self, matcher):
        self._matcher = matcher

    def allow(self, request):
        return self._matcher.match(request)


class Forbid:
    def __init__(self, matcher):
        self._matcher = matcher

    def allow(self, request):
        return not self._matcher.match(request)
