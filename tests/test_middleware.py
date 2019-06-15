from django.http import HttpResponse, HttpResponseForbidden

from header_filter import Enforce, Forbid, Header, HeaderFilterMiddleware


def test_no_rule_list_setting(settings, rf):
    mw = HeaderFilterMiddleware(lambda request: HttpResponse())
    request = rf.get('/', **{'HTTP_X_A': 'val_x'})
    response = mw(request)
    assert response.status_code == 200


def test_empty_rule_list_setting(settings, rf):
    settings.HEADER_FILTER_RULES = []
    mw = HeaderFilterMiddleware(lambda request: HttpResponse())
    request = rf.get('/', **{'HTTP_X_A': 'val_x'})
    response = mw(request)
    assert response.status_code == 200


def test_one_rule_and_good_request(settings, rf):
    h_name, h_value = 'HTTP_X_A', 'val_x'
    settings.HEADER_FILTER_RULES = [Enforce(Header(h_name, h_value))]
    mw = HeaderFilterMiddleware(lambda request: HttpResponse())
    request = rf.get('/', **{h_name: h_value})
    response = mw(request)
    assert response.status_code == 200


def test_one_rule_and_bad_request(settings, rf):
    settings.HEADER_FILTER_RULES = [Enforce(Header('HTTP_X_A', 'val_x'))]
    mw = HeaderFilterMiddleware(lambda request: HttpResponse())
    request = rf.get('/', **{'HTTP_X_B': 'val_y'})
    response = mw(request)
    assert response.status_code == 400


def test_two_rules_and_bad_request_triggers_the_second(settings, rf):
    settings.HEADER_FILTER_RULES = [Enforce(Header('HTTP_X_A', 'val_x')), Forbid(Header('HTTP_X_B', 'val_y'))]
    mw = HeaderFilterMiddleware(lambda request: HttpResponse())
    request = rf.get('/', **{'HTTP_X_A': 'val_x', 'HTTP_X_B': 'val_y'})
    response = mw(request)
    assert response.status_code == 400


def test_first_violation_is_final(settings, rf):
    settings.HEADER_FILTER_RULES = [
        Enforce(Header('HTTP_X_A', 'val_x')),
        Forbid(Header('HTTP_X_B', 'val_y'), reject_response=HttpResponseForbidden()),
        Enforce(Header('HTTP_X_C', 'val_z')),
    ]
    mw = HeaderFilterMiddleware(lambda request: HttpResponse())
    request = rf.get('/', **{'HTTP_X_A': 'val_x', 'HTTP_X_B': 'val_y'})
    response = mw(request)
    assert response.status_code == 403
