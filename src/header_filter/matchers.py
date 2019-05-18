class BaseMatcher:

    def __invert__(self):
        return Not(self)

    def __and__(self, other):
        return And(self, other)

    def __or__(self, other):
        return Or(self, other)


class And(BaseMatcher):

    def __init__(self, header1, header2):
        self._headers = (header1, header2)

    def match(self, request):
        return all(header.match(request) for header in self._headers)


class Or(BaseMatcher):

    def __init__(self, header1, header2):
        self._headers = (header1, header2)

    def match(self, request):
        return any(header.match(request) for header in self._headers)


class Not(BaseMatcher):

    def __init__(self, header):
        self._header = header

    def match(self, request):
        return not self._header.match(request)


class Header(BaseMatcher):

    def __init__(self, name, value):
        self._header = (name, value)

    def match(self, request):
        return self._header in request.META.items()
