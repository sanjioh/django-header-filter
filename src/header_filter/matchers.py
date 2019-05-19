import re


class BaseMatcher:

    def match(self, request):
        return False

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
        self._name = name
        self._value = value

    def match(self, request):
        try:
            current_value = request.META[self._name]
        except KeyError:
            return False
        else:
            return current_value == self._value


class HeaderRegexp(BaseMatcher):
    def __init__(self, name_re, value_re):
        self._name_re = re.compile(name_re)
        self._value_re = re.compile(value_re)

    def match(self, request):
        for name, value in request.META.items():
            if self._name_re.fullmatch(name) and self._value_re.fullmatch(value):
                return True
        return False
