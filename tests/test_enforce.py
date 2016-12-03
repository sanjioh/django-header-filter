import pytest

from header_filter import middleware as mw


@pytest.fixture
def hfconf():
    class Conf:
        pass
    c = Conf()
    c.groups = {
        'group_A': (
            ('X-H-1', 'value1'),
            ('X-H-2', 'value2'),
        ),
    }
    c.rules = (
        {
            'ACTION': 'enforce',
            'HEADERS': 'group_A',
            'RESPONSE': (400, 'enforce rule matched'),
        },
    )
    return c


def test_enforce_with_correct_request(settings, hfconf, rf):
    settings.HEADER_FILTER_GROUPS, settings.HEADER_FILTER_RULES = hfconf.groups, hfconf.rules
    hf = mw.HeaderFilterMiddleware()
    request = rf.get('/', HTTP_X_H_1='value1', HTTP_X_H_2='value2')
    res = hf.process_request(request)
    assert res is None


def test_enforce_with_wrong_request(settings, hfconf, rf):
    settings.HEADER_FILTER_GROUPS, settings.HEADER_FILTER_RULES = hfconf.groups, hfconf.rules
    hf = mw.HeaderFilterMiddleware()
    request = rf.get('/', HTTP_X_H_1='value1')
    res = hf.process_request(request)
    assert res.content == 'enforce rule matched'
    assert res.status == 400
