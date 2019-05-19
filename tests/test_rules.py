from django.http import HttpResponse, HttpResponseNotFound

from header_filter.matchers import Header
from header_filter.rules import Enforce, Forbid


def test_enforce_with_good_request(rf):
    h_name, h_value = 'HTTP_X_A', 'val_x'
    matcher = Header(h_name, h_value)
    action = Enforce(matcher)
    request = rf.get('/', **{h_name: h_value})
    assert action.process(request) is None


def test_enforce_with_bad_request_and_default_response(rf):
    matcher = Header('HTTP_X_A', 'val_x')
    action = Enforce(matcher)
    request = rf.get('/', **{'HTTP_X_B': 'val_y'})
    response = action.process(request)
    assert isinstance(response, HttpResponse)
    assert response.reason_phrase == 'BAD REQUEST'
    assert response.status_code == 400


def test_enforce_with_bad_request_and_custom_response(rf):
    matcher = Header('HTTP_X_A', 'val_x')
    reject_reason = 'some reason'
    action = Enforce(matcher, reject_response=HttpResponseNotFound(reason=reject_reason))
    request = rf.get('/', **{'HTTP_X_B': 'val_y'})
    response = action.process(request)
    assert isinstance(response, HttpResponse)
    assert response.reason_phrase == reject_reason
    assert response.status_code == 404


def test_forbid_with_good_request(rf):
    matcher = Header('HTTP_X_A', 'val_x')
    action = Forbid(matcher)
    request = rf.get('/', **{'HTTP_X_B': 'val_y'})
    assert action.process(request) is None


def test_forbid_with_bad_request_and_default_response(rf):
    h_name, h_value = 'HTTP_X_A', 'val_x'
    matcher = Header(h_name, h_value)
    action = Forbid(matcher)
    request = rf.get('/', **{h_name: h_value})
    response = action.process(request)
    assert isinstance(response, HttpResponse)
    assert response.reason_phrase == 'BAD REQUEST'
    assert response.status_code == 400


def test_forbid_with_bad_request_and_custom_response(rf):
    h_name, h_value = 'HTTP_X_A', 'val_x'
    matcher = Header(h_name, h_value)
    reject_reason = 'some reason'
    action = Forbid(matcher, reject_response=HttpResponseNotFound(reason=reject_reason))
    request = rf.get('/', **{h_name: h_value})
    response = action.process(request)
    assert isinstance(response, HttpResponse)
    assert response.reason_phrase == reject_reason
    assert response.status_code == 404
