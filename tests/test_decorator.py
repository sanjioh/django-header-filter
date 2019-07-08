from unittest import mock

import pytest
from django.http import HttpResponse, HttpResponseForbidden

from header_filter import Enforce, Forbid, Header, header_rules


@pytest.fixture
def view():
    def view(request, *args, **kwargs):
        return HttpResponse()

    return view


def test_no_rule_list(rf, view):
    decorated_view = header_rules()(view)
    request = rf.get('/', **{'HTTP_X_A': 'val_x'})
    response = decorated_view(request)
    assert response.status_code == 200


def test_empty_rule_list(rf, view):
    decorated_view = header_rules([])(view)
    request = rf.get('/', **{'HTTP_X_A': 'val_x'})
    response = decorated_view(request)
    assert response.status_code == 200


def test_one_rule_and_good_request(rf, view):
    h_name, h_value = 'HTTP_X_A', 'val_x'
    decorated_view = header_rules([Enforce(Header(h_name, h_value))])(view)
    request = rf.get('/', **{h_name: h_value})
    response = decorated_view(request)
    assert response.status_code == 200


def test_one_rule_and_bad_request(rf, view):
    decorated_view = header_rules([Enforce(Header('HTTP_X_A', 'val_x'))])(view)
    request = rf.get('/', **{'HTTP_X_B': 'val_y'})
    response = decorated_view(request)
    assert response.status_code == 400


def test_two_rules_and_bad_request_triggers_the_second(rf, view):
    decorated_view = header_rules([Enforce(Header('HTTP_X_A', 'val_x')), Forbid(Header('HTTP_X_B', 'val_y'))])(view)
    request = rf.get('/', **{'HTTP_X_A': 'val_x', 'HTTP_X_B': 'val_y'})
    response = decorated_view(request)
    assert response.status_code == 400


def test_first_violation_is_final(rf, view):
    decorated_view = header_rules(
        [
            Enforce(Header('HTTP_X_A', 'val_x')),
            Forbid(Header('HTTP_X_B', 'val_y'), reject_response=HttpResponseForbidden()),
            Enforce(Header('HTTP_X_C', 'val_z')),
        ]
    )(view)
    request = rf.get('/', **{'HTTP_X_A': 'val_x', 'HTTP_X_B': 'val_y'})
    response = decorated_view(request)
    assert response.status_code == 403


def test_view_args_kwargs(rf):
    view = mock.Mock()
    decorated_view = header_rules()(view)
    request = rf.get('/')
    args, kwargs = ('arg',), {'kw': 'arg'}
    decorated_view(request, *args, **kwargs)
    view.assert_called_once_with(request, *args, **kwargs)


def test_decorated_view_name(view):
    decorated_view = header_rules()(view)
    assert decorated_view.__name__ == 'view'
