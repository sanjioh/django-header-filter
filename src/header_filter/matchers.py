"""Composable matchers for HTTP headers."""
import re

RE_TYPE = type(re.compile(r''))


class BaseMatcher:
    """Matcher base class."""

    def match(self, request):
        """
        Check HTTP request headers against some criteria.

        This method checks whether the request headers satisfy some
        criteria or not. Subclasses should override it and provide a
        specialized implementation.
        The default implementation just returns False.

        `request`: a Django request.
        returns: a boolean.
        """
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
    """Composite matcher that implements the bitwise AND operation."""

    def __init__(self, matcher1, matcher2):
        """
        Initialize the instance.

        `matcher1`, `matcher2`: matchers of any type.
        """
        self._matchers = (matcher1, matcher2)

    def match(self, request):
        """
        Compute the bitwise AND between the results of two matchers.

        `request`: a Django request.
        returns: a boolean.
        """
        return all(matcher.match(request) for matcher in self._matchers)


class Or(BaseMatcher):
    """Composite matcher that implements the bitwise OR operation."""

    def __init__(self, matcher1, matcher2):
        """
        Initialize the instance.

        `matcher1`, `matcher2`: matchers of any type.
        """
        self._matchers = (matcher1, matcher2)

    def match(self, request):
        """
        Compute the bitwise OR between the results of two matchers.

        `request`: a Django request.
        returns: a boolean.
        """
        return any(matcher.match(request) for matcher in self._matchers)


class Xor(BaseMatcher):
    """Composite matcher that implements the bitwise XOR operation."""

    def __init__(self, matcher1, matcher2):
        """
        Initialize the instance.

        `matcher1`, `matcher2`: matchers of any type.
        """
        self._matcher1 = matcher1
        self._matcher2 = matcher2

    def match(self, request):
        """
        Compute the bitwise XOR between the results of two matchers.

        `request`: a Django request.
        returns: a boolean.
        """
        return self._matcher1.match(request) is not self._matcher2.match(request)


class Not(BaseMatcher):
    """Composite matcher that implements the bitwise NOT operation."""

    def __init__(self, matcher):
        """
        Initialize the instance.

        `matcher`: a matcher of any type.
        """
        self._matcher = matcher

    def match(self, request):
        """
        Compute the bitwise NOT of the result of a matcher.

        `request`: a Django request.
        returns: a boolean.
        """
        return not self._matcher.match(request)


class Header(BaseMatcher):
    """HTTP header matcher."""

    def __init__(self, name, value):
        """
        Initialize the instance.

        `name`: a header name, as string.
        `value`: a header value, as string, compiled regular expression
        object, or iterable.
        """
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
        """
        Inspect a request for headers with given name and value.

        This method checks whether:
        a) the request contains a header with the same exact name the
        matcher has been initialized with, and
        b) the header value is equal, matches, or belongs to the value
        the matcher has been initialized with, depending on that being
        respectively a string, a compiled regexp object, or an iterable.

        `request`: a Django request.
        returns: a boolean.
        """
        try:
            request_value = request.META[self._name]
        except KeyError:
            return False
        else:
            return self._compare_value(request_value)


class HeaderRegexp(BaseMatcher):
    """HTTP header matcher based on regular expressions."""

    def __init__(self, name_re, value_re):
        """
        Initialize the instance.

        `name_re`: a header name, as regexp string or compiled regexp
        object.
        `value_re`: a header value, as regexp string or compiled regexp
        object.
        """
        self._name_re = re.compile(name_re)
        self._value_re = re.compile(value_re)

    def match(self, request):
        """
        Inspect a request for headers that match regular expressions.

        This method checks whether the request contains at least one
        header whose name and value match the respective regexps the
        matcher has been initialized with.

        `request`: a Django request.
        returns: a boolean.
        """
        for name, value in request.META.items():
            if self._name_re.fullmatch(name) and self._value_re.fullmatch(value):
                return True
        return False
