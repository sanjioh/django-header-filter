"""Decorator for enforcing rules at view level."""
from functools import wraps


def header_rules(rules=None):
    """
    Apply a set of rules to a Django view.

    This is a decorator factory.

    Rule order matters: the first rule that results in a rejection
    determines the response.
    A request is accepted (and handed over to the view) iff no rule
    rejects it.

    `rules`: an iterable of rules.
    returns: a decorator function.
    """
    rules = rules or []

    def deco(view):
        @wraps(view)
        def wrapper(request, *args, **kwargs):
            for rule in rules:
                response = rule.process(request)
                if response:
                    return response
            return view(request, *args, **kwargs)

        return wrapper

    return deco
