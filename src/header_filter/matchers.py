import re

RE_TYPE = type(re.compile(r''))


class BaseMatcher:

    def match(self, request):
        return False

    def __invert__(self):
        return Not(self)

    def __and__(self, other):
        return And(self, other)

    def __or__(self, other):
        return Or(self, other)

    def __xor__(self, other):
        return Xor(self, other)


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


class Xor(BaseMatcher):

    def __init__(self, header1, header2):
        self._header1 = header1
        self._header2 = header2

    def match(self, request):
        return self._header1.match(request) is not self._header2.match(request)


class Not(BaseMatcher):

    def __init__(self, header):
        self._header = header

    def match(self, request):
        return not self._header.match(request)


class Header(BaseMatcher):

    def __init__(self, name, value):
        self._name = name
        self._value = value
        self._compare_value = self._get_value_comparison_method()

    def _get_value_comparison_method(self):
        if isinstance(self._value, RE_TYPE):
            return self._compare_value_to_re_object
        if isinstance(self._value, str):
            return self._compare_value_to_str
        return self._compare_value_to_iterable

    def _compare_value_to_re_object(self, request_value):
        return bool(self._value.fullmatch(request_value))

    def _compare_value_to_str(self, request_value):
        return request_value == self._value

    def _compare_value_to_iterable(self, request_value):
        return request_value in set(self._value)

    def match(self, request):
        try:
            request_value = request.META[self._name]
        except KeyError:
            return False
        else:
            return self._compare_value(request_value)


class HeaderRegexp(BaseMatcher):
    def __init__(self, name_re, value_re):
        self._name_re = re.compile(name_re)
        self._value_re = re.compile(value_re)

    def match(self, request):
        for name, value in request.META.items():
            if self._name_re.fullmatch(name) and self._value_re.fullmatch(value):
                return True
        return False
