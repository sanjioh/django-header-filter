"""Middleware for enforcing rules at application level."""
from django.conf import settings


class HeaderFilterMiddleware:
    """Middleware that implements header-based filtering."""

    def __init__(self, get_response):
        """Initialize the instance."""
        self.get_response = get_response

    def __call__(self, request):
        """
        Apply a set of rules to every request.

        Rule order matters: the first rule that results in a rejection
        determines the response.
        A request is accepted (and handed over to a later middleware or
        the view) iff no rule rejects it.

        `request`: a Django request.
        returns: a Django response.
        """
        rules = getattr(settings, 'HEADER_FILTER_RULES', [])
        for rule in rules:
            response = rule.process(request)
            if response:
                return response
        return self.get_response(request)
