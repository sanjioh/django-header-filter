import re

from header_filter.matchers import HeaderRegexp


def test_header_name_and_value_match_re_pattern(rf):
    matcher = HeaderRegexp(r'^HTTP_X_A.*$', r'^val_.$')
    request = rf.get('/', **{'HTTP_X_A_XYZ': 'val_x'})
    assert matcher.match(request) is True


def test_header_name_and_value_match_re_object(rf):
    matcher = HeaderRegexp(re.compile(r'^HTTP_X_A.*$'), re.compile(r'^val_.$'))
    request = rf.get('/', **{'HTTP_X_A_XYZ': 'val_x'})
    assert matcher.match(request) is True


def test_header_name_doesnt_match_re_pattern(rf):
    matcher = HeaderRegexp(r'^HTTP_X_A.*$', r'^val_.$')
    request = rf.get('/', **{'HTTP_X_B_XYZ': 'val_x'})
    assert matcher.match(request) is False


def test_header_name_doesnt_match_re_object(rf):
    matcher = HeaderRegexp(re.compile(r'^HTTP_X_A.*$'), re.compile(r'^val_.$'))
    request = rf.get('/', **{'HTTP_X_B_XYZ': 'val_x'})
    assert matcher.match(request) is False


def test_header_value_doesnt_match_re_pattern(rf):
    matcher = HeaderRegexp(r'^HTTP_X_A.*$', r'^val_.$')
    request = rf.get('/', **{'HTTP_X_A_XYZ': 'val_'})
    assert matcher.match(request) is False


def test_header_value_doesnt_match_re_object(rf):
    matcher = HeaderRegexp(re.compile(r'^HTTP_X_A.*$'), re.compile(r'^val_.$'))
    request = rf.get('/', **{'HTTP_X_A_XYZ': 'val_'})
    assert matcher.match(request) is False


def test_header_name_and_value_dont_match_re_pattern(rf):
    matcher = HeaderRegexp(r'^HTTP_X_A.*$', r'^val_.$')
    request = rf.get('/', **{'HTTP_X_B_XYZ': 'val_'})
    assert matcher.match(request) is False


def test_header_name_and_value_dont_match_re_object(rf):
    matcher = HeaderRegexp(re.compile(r'^HTTP_X_A.*$'), re.compile(r'^val_.$'))
    request = rf.get('/', **{'HTTP_X_B_XYZ': 'val_'})
    assert matcher.match(request) is False


def test_repr():
    assert (
        repr(HeaderRegexp(re.compile(r'^HTTP_X_A.*$'), re.compile(r'^val_.$')))
        == "HeaderRegexp(re.compile('^HTTP_X_A.*$'), re.compile('^val_.$'))"
    )
