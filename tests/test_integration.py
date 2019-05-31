import pytest
from django.http import HttpResponseForbidden
from django.urls import reverse

from header_filter import Enforce, Forbid, Header


@pytest.fixture
def testurl(settings):
    return reverse('testurl')


@pytest.fixture
def settings(settings):
    settings.ROOT_URLCONF = 'fake_app.urls'
    settings.MIDDLEWARE = ['header_filter.HeaderFilterMiddleware']
    return settings


def test_enforce_single_header_success(client, testurl, settings):
    h_name, h_value = 'HTTP_X_A', 'val_x'
    settings.HEADER_FILTER_RULES = [
        Enforce(Header(h_name, h_value)),
    ]
    response = client.get(testurl, **{h_name: h_value})
    assert response.status_code == 200


def test_enforce_single_header_failure(client, testurl, settings):
    settings.HEADER_FILTER_RULES = [
        Enforce(Header('HTTP_X_A', 'val_x')),
    ]
    response = client.get(testurl, **{'HTTP_X_B': 'val_y'})
    assert response.status_code == 400


def test_forbid_single_header_success(client, testurl, settings):
    settings.HEADER_FILTER_RULES = [
        Forbid(Header('HTTP_X_A', 'val_x')),
    ]
    response = client.get(testurl, **{'HTTP_X_B': 'val_y'})
    assert response.status_code == 200


def test_forbid_single_header_failure(client, testurl, settings):
    h_name, h_value = 'HTTP_X_A', 'val_x'
    settings.HEADER_FILTER_RULES = [
        Forbid(Header(h_name, h_value)),
    ]
    response = client.get(testurl, **{h_name: h_value})
    assert response.status_code == 400


def test_custom_response_on_failure(client, testurl, settings):
    settings.HEADER_FILTER_RULES = [
        Enforce(Header('HTTP_X_A', 'val_x'), reject_response=HttpResponseForbidden()),
    ]
    response = client.get(testurl, **{'HTTP_X_B': 'val_y'})
    assert response.status_code == 403


def test_multiple_rules_success(client, testurl, settings):
    h_name, h_value = 'HTTP_X_A', 'val_x'
    settings.HEADER_FILTER_RULES = [
        Enforce(Header(h_name, h_value)),
        Forbid(Header('HTTP_X_B', 'val_y')),
    ]
    response = client.get(testurl, **{h_name: h_value})
    assert response.status_code == 200


def test_multiple_rules_failure(client, testurl, settings):
    h_name_1, h_value_1 = 'HTTP_X_A', 'val_x'
    h_name_2, h_value_2 = 'HTTP_X_B', 'val_y'
    settings.HEADER_FILTER_RULES = [
        Enforce(Header(h_name_1, h_value_1)),
        Forbid(Header(h_name_2, h_value_2)),
    ]
    response = client.get(testurl, **{h_name_1: h_value_1, h_name_2: h_value_2})
    assert response.status_code == 400


def test_not_matcher_success(client, testurl, settings):
    settings.HEADER_FILTER_RULES = [
        Enforce(~Header('HTTP_X_A', 'val_x')),
    ]
    response = client.get(testurl, **{'HTTP_X_B': 'val_y'})
    assert response.status_code == 200


def test_not_matcher_failure(client, testurl, settings):
    h_name, h_value = 'HTTP_X_A', 'val_x'
    settings.HEADER_FILTER_RULES = [
        Enforce(~Header(h_name, h_value)),
    ]
    response = client.get(testurl, **{h_name: h_value})
    assert response.status_code == 400


def test_and_matcher_success(client, testurl, settings):
    h_name_1, h_value_1 = 'HTTP_X_A', 'val_x'
    h_name_2, h_value_2 = 'HTTP_X_B', 'val_y'
    settings.HEADER_FILTER_RULES = [
        Enforce(Header(h_name_1, h_value_1) & Header(h_name_2, h_value_2)),
    ]
    response = client.get(testurl, **{h_name_1: h_value_1, h_name_2: h_value_2})
    assert response.status_code == 200


def test_and_matcher_failure(client, testurl, settings):
    h_name, h_value = 'HTTP_X_A', 'val_x'
    settings.HEADER_FILTER_RULES = [
        Enforce(Header(h_name, h_value) & Header('HTTP_X_B', 'val_y')),
    ]
    response = client.get(testurl, **{h_name: h_value})
    assert response.status_code == 400


def test_or_matcher_success(client, testurl, settings):
    h_name, h_value = 'HTTP_X_A', 'val_x'
    settings.HEADER_FILTER_RULES = [
        Enforce(Header(h_name, h_value) | Header('HTTP_X_B', 'val_y')),
    ]
    response = client.get(testurl, **{h_name: h_value})
    assert response.status_code == 200


def test_or_matcher_failure(client, testurl, settings):
    settings.HEADER_FILTER_RULES = [
        Enforce(Header('HTTP_X_A', 'val_x') | Header('HTTP_X_B', 'val_y')),
    ]
    response = client.get(testurl, **{'HTTP_X_C': 'val_z'})
    assert response.status_code == 400


def test_xor_matcher_success(client, testurl, settings):
    h_name, h_value = 'HTTP_X_A', 'val_x'
    settings.HEADER_FILTER_RULES = [
        Enforce(Header(h_name, h_value) ^ Header('HTTP_X_B', 'val_y')),
    ]
    response = client.get(testurl, **{h_name: h_value})
    assert response.status_code == 200


def test_xor_matcher_failure(client, testurl, settings):
    h_name_1, h_value_1 = 'HTTP_X_A', 'val_x'
    h_name_2, h_value_2 = 'HTTP_X_B', 'val_y'
    settings.HEADER_FILTER_RULES = [
        Enforce(Header(h_name_1, h_value_1) ^ Header(h_name_2, h_value_2)),
    ]
    response = client.get(testurl, **{h_name_1: h_value_1, h_name_2: h_value_2})
    assert response.status_code == 400
