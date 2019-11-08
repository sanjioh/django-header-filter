"""Common useful rule implementations."""
from django.http import HttpResponseBadRequest


class Enforce:
    """Rule that enforces headers as defined by a matcher."""

    def __init__(self, matcher, reject_response=None):
        """
        Initialize the instance.

        `matcher`: a matcher.
        `reject_response`: a Django response.
        """
        self._matcher = matcher
        self._reject_response = reject_response or HttpResponseBadRequest()

    def process(self, request):
        """
        Apply the rule to a request.

        Requests that don't satisfy the criteria of the matcher will be
        rejected.

        `request`: a Django request.
        returns: a Django response or None.
        """
        if self._matcher.match(request):
            return None
        return self._reject_response


class Forbid:
    """Rule that forbids headers as defined by a matcher."""

    def __init__(self, matcher, reject_response=None):
        """
        Initialize the instance.

        `matcher`: a matcher.
        `reject_response`: a Django response.
        """
        self._matcher = matcher
        self._reject_response = reject_response or HttpResponseBadRequest()

    def process(self, request):
        """
        Apply the rule to a request.

        Requests that satisfy the criteria of the matcher will be
        rejected.

        `request`: a Django request.
        returns: a Django response or None.
        """
        if not self._matcher.match(request):
            return None
        return self._reject_response
