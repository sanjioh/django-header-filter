from functools import wraps


def header_rules(rules=None):
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
