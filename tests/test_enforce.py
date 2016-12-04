from __future__ import unicode_literals

import pytest

from header_filter import middleware as mw


@pytest.fixture
def settings(settings):
    settings.HEADER_FILTER_RULES = (
        {
            'ACTION': 'enforce',
            'HEADERS': 'group_a',
            'RESPONSE': (400, 'enforce rule'),
        },
    )
    return settings


def test_enforce_single_vs_missing(settings, rf):
    settings.HEADER_FILTER_GROUPS = {
        'group_a': (
            ('HTTP_X_H_1', 'unused'),
        ),
    }
    hf = mw.HeaderFilterMiddleware()
    request = rf.get('/')
    res = hf.process_request(request)
    assert res.status_code == 400
    assert res.reason_phrase == 'enforce rule'


def test_enforce_single_literal_vs_ok(settings, rf):
    settings.HEADER_FILTER_GROUPS = {
        'group_a': (
            ('HTTP_X_H_1', 'value1'),
        ),
    }
    hf = mw.HeaderFilterMiddleware()
    request = rf.get('/', HTTP_X_H_1='value1')
    res = hf.process_request(request)
    assert res is None


def test_enforce_single_literal_vs_wrong_value(settings, rf):
    settings.HEADER_FILTER_GROUPS = {
        'group_a': (
            ('HTTP_X_H_1', 'value1'),
        ),
    }
    hf = mw.HeaderFilterMiddleware()
    request = rf.get('/', HTTP_X_H_1='wrong_value')
    res = hf.process_request(request)
    assert res.status_code == 400
    assert res.reason_phrase == 'enforce rule'


def test_enforce_single_callable_vs_ok(settings, rf):
    settings.HEADER_FILTER_GROUPS = {
        'group_a': (
            ('HTTP_X_H_1', lambda request: request.META['HTTP_X_H_1'] == 'value1'),
        ),
    }
    hf = mw.HeaderFilterMiddleware()
    request = rf.get('/', HTTP_X_H_1='value1')
    res = hf.process_request(request)
    assert res is None


def test_enforce_single_callable_vs_wrong_value(settings, rf):
    settings.HEADER_FILTER_GROUPS = {
        'group_a': (
            ('HTTP_X_H_1', lambda request: request.META['HTTP_X_H_1'] == 'value1'),
        ),
    }
    hf = mw.HeaderFilterMiddleware()
    request = rf.get('/', HTTP_X_H_1='wrong_value')
    res = hf.process_request(request)
    assert res.status_code == 400
    assert res.reason_phrase == 'enforce rule'
