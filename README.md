# django-header-filter

[![GitHub Actions](https://github.com/sanjioh/django-header-filter/workflows/CI/badge.svg)](https://github.com/sanjioh/django-header-filter/actions)
[![codecov](https://codecov.io/gh/sanjioh/django-header-filter/branch/master/graph/badge.svg)](https://codecov.io/gh/sanjioh/django-header-filter)
[![version](https://img.shields.io/pypi/v/django-header-filter)](https://pypi.org/project/django-header-filter)
[![python](https://img.shields.io/pypi/pyversions/django-header-filter)](https://pypi.org/project/django-header-filter)
[![license](https://img.shields.io/pypi/l/django-header-filter)](https://pypi.org/project/django-header-filter)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

`django-header-filter` implements header-based filtering for Django
applications. That is, it allows to reject requests whose headers are
not compliant to a user-defined set of rules.

## Compatibility

`django-header-filter` is compatible with:

- Python 3.5, 3,6, 3.7, 3.8
- Django 1.11, 2.0, 2.1, 2.2

## Installation

```shell
$ pip install django-header-filter
```

## Quickstart

Imagine you need to make sure that every request routed to a specific
view has a header named `X-Planet` with `Mars` as value.

This constraint can be implemented as follows:

```python
# views.py
from django.http import HttpResponse
from header_filter import Enforce, Header, header_rules


@header_rules([Enforce(Header('HTTP_X_PLANET', 'Mars'))])
def do_things(request):
    # ...
    return HttpResponse()
```

In short:

- the `@header_rules` decorator applies a list of *rules* to the view
- in the example that list is made up of one single rule, `Enforce`,
which allows the request to be handed over to the view only if the
respective *matcher* holds true (otherwise a `400 Bad Request` response
is returned to the client)
- the `Header` matcher is responsible for checking whether a header
compliant to your needs belongs to the request or not

## Matchers

Matchers are the basic building blocks for defining header-based
filters. Their job is to check whether user-defined header combinations
belong to the request or not.

`django-header-filter` provides the following matchers:

### `Header`

The `Header` matcher must be instantiated with two arguments: the first
argument is the *name* of the header; the second one is its *value*.

The header name must be a string.

> **NOTE**: header names in Django are usually different from the ones
that a client actually sends, due to some string manipulations that
happen server side (refer to the [docs][2] for details). Matchers do
nothing to guess the original names, so be sure to initialize them with
the right format (e.g. `X-Planet` becomes `HTTP_X_PLANET` when used for
a `Header` matcher instantiation).

The type of the header value may be one of the following:

- a string
- a compiled regular expression object (as returned by
[`re.compile()`][3])
- an iterable of strings

The `Header` matcher will check whether a header with the given name and
value actually exists. As far as the value is concerned, the matching
logic depends on its type:

- exact match for strings
- regexp match for regular expression objects
- membership for iterables

```python
import re

from header_filter import Header

# matches X-Planet: Mars
Header('HTTP_X_PLANET', 'Mars')

# matches X-Planet: Mars or X-Planet: Mercury
Header('HTTP_X_PLANET', re.compile(r'^M.*'))

# matches X-Planet: Mars or X-Planet: Venus
Header('HTTP_X_PLANET', ['Mars', 'Venus'])
```

### `HeaderRegexp`

The `HeaderRegexp` matcher is similar to the `Header` matcher, but the
arguments it takes at instantiation may be:

- compiled regular expression objects
- regexp pattern strings

both for name and value.

```python
import re

from header_filter import HeaderRegexp

# matches X-Planet: Mars and X-Planet: Mercury
HeaderRegexp(r'^HTTP_X_PLANET$', re.compile(r'^M.*'))

# same as above
HeaderRegexp(re.compile(r'^HTTP_X_PLANET$'), r'^M.*')
```

## Matchers are composable

Matchers can be aggregated into composite matchers by means of bitwise
operators:

- `&` (and)
- `|` (or)
- `^` (xor)
- `~` (not)

A composite matcher allows for checks that cannot be expressed by just
using the matchers described above.

```python
from header_filter import Header

# matches if X-Planet: Mars and X-Rover: Curiosity are both present
Header('HTTP_X_PLANET', 'Mars') & Header('HTTP_X_ROVER', 'Curiosity')

# matches if at least one of X-Planet: Mars and X-Rover: Curiosity is present
Header('HTTP_X_PLANET', 'Mars') | Header('HTTP_X_ROVER', 'Curiosity')

# matches if exactly one of X-Planet: Mars and X-Rover: Curiosity is present
Header('HTTP_X_PLANET', 'Mars') ^ Header('HTTP_X_ROVER', 'Curiosity')

# matches if X-Planet: Mars is not present
~Header('HTTP_X_PLANET', 'Mars')
```

From the usage point of view, there's no difference between a simple
matcher and a composite one: both can be used in the same contexts.
Besides, there's no limit in how much matchers can be combined: simple
matchers can be combined into composites, which in turn can be used as
atoms for further composition.

```python
from header_filter import Header

# matches if X-Planet: Mars and X-Rover: Curiosity aren't both present
~(Header('HTTP_X_PLANET', 'Mars') & Header('HTTP_X_ROVER', 'Curiosity'))

# matches if
# X-Planet: Mars is not present, and
# exactly one of X-Rover: Curiosity and X-Aliens: false is present
(
    ~Header('HTTP_X_PLANET', 'Mars')
    & (
        Header('HTTP_X_ROVER', 'Curiosity') ^ Header('HTTP_X_ALIENS', 'false')
    )
)
```

## Matchers support string representation

A matcher can be inspected by printing its string representation.

```python
from header_filter import Header

matcher1 = Header('HTTP_X_PLANET', 'Mars')
matcher2 = Header('HTTP_X_ROVER', 'Curiosity')
composite = ~(matcher1 & matcher2)
print(repr(composite))
# ~(Header('HTTP_X_PLANET', 'Mars') & Header('HTTP_X_ROVER', 'Curiosity'))
```

## Rules

Rules rely on matchers to implement actual header-based filtering.

`django-header-filter` provides two rules: `Enforce` and `Forbid`. Both
require a matcher to be instantiated, but behave differently:

- `Enforce` rejects requests whose headers **do not** comply with its
matcher
- `Forbid` rejects requests whose headers **do** comply with its
matcher

```python
from header_filter import Enforce, Forbid, Header

# rejects requests *lacking* an X-Planet: Mars header
Enforce(Header('HTTP_X_PLANET', 'Mars'))

# rejects requests *containing* an X-Planet: Mars header
Forbid(Header('HTTP_X_PLANET', 'Mars'))
```

Rules can use matchers of any type (simple or composite).

## Custom reject responses

By default rules reject requests with a
`django.http.HttpResponseBadRequest` response.
The default behavior can be overridden by passing an optional argument
at rule instantiation, named `reject_response`. The argument must be an
instance of a Django Response, which will be returned to the client
whenever the rule triggers the rejection of a request.

```python
from django.http import HttpResponseNotFound
from header_filter import Enforce, Header

# rejects requests *lacking* an X-Planet: Mars header with a 404 response
Enforce(
    Header('HTTP_X_PLANET', 'Mars'),
    reject_response=HttpResponseNotFound(reason='Sorry!')
)
```

## `@header_rules` decorator

The `@header_rules` decorator binds a list of rules to a view. The
decorator checks the headers of every request routed to that view
against each rule of the list, in order. The first rule that results in
a rejection determines the response that will be sent back to the
client. If no rule triggers a rejection, the request is handed over to
the view for regular processing.

```python
from django.http import HttpResponse
from header_filter import Enforce, Forbid, Header, header_rules


# requests *lacking* an X-Planet: Mars header or *containing* an
# X-Rover: Curiosity header will be rejected
@header_rules(
    [
        Enforce(Header('HTTP_X_PLANET', 'Mars')),
        Forbid(Header('HTTP_X_ROVER', 'Curiosity')),
    ]
)
def do_things(request):
    # ...
    return HttpResponse()
```

`@header_rules` works fine with class-based views as well, by means of
`@method_decorator`.

```python
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from header_filter import Enforce, Forbid, Header, header_rules


class DoThings(View):
    # requests *lacking* an X-Planet: Mars header or *containing* an
    # X-Rover: Curiosity header will be rejected
    @method_decorator(header_rules([
        Enforce(Header('HTTP_X_PLANET', 'Mars')),
        Forbid(Header('HTTP_X_ROVER', 'Curiosity')),
    ]))
    def get(self, request, *args, **kwargs):
        # ...
        return HttpResponse()
```

## `HeaderFilterMiddleware`

By using the `HeaderFilterMiddleware` middleware, a list of rules can be
applied globally, at application level. Every request will be then
checked against the global rule list, independently of views.

For this to work you need to properly tweak your Django settings module,
as follows:

```python
# settings.py
from header_filter import Enforce, Header

MIDDLEWARE = [
    # ...
    'header_filter.HeaderFilterMiddleware',
    # ...
]

HEADER_FILTER_RULES = [
    Enforce(Header('HTTP_X_PLANET', 'Mars')),
    # ...additional rules...
]
```

## License

See: [LICENSE][1]

[1]: https://github.com/sanjioh/django-header-filter/blob/master/LICENSE
[2]: https://docs.djangoproject.com/en/dev/ref/request-response/#django.http.HttpRequest.META
[3]: https://docs.python.org/3/library/re.html#re.compile
