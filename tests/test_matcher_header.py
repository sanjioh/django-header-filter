import re

from header_filter.matchers import Header


def test_header_name_and_value_match(rf):
    h_name, h_value = 'HTTP_X_A', 'val_x'
    matcher = Header(h_name, h_value)
    request = rf.get('/', **{h_name: h_value})
    assert matcher.match(request) is True


def test_header_name_doesnt_match(rf):
    h_value = 'val_x'
    matcher = Header('HTTP_X_A', h_value)
    request = rf.get('/', **{'HTTP_X_B': h_value})
    assert matcher.match(request) is False


def test_header_value_doesnt_match(rf):
    h_name = 'HTTP_X_A'
    matcher = Header(h_name, 'val_x')
    request = rf.get('/', **{h_name: 'val_y'})
    assert matcher.match(request) is False


def test_header_name_and_value_dont_match(rf):
    matcher = Header('HTTP_X_A', 'val_x')
    request = rf.get('/', **{'HTTP_X_B': 'val_y'})
    assert matcher.match(request) is False


def test_header_value_matches_re_object(rf):
    h_name = 'HTTP_X_A'
    matcher = Header(h_name, re.compile(r'^val_.$'))
    request = rf.get('/', **{h_name: 'val_x'})
    assert matcher.match(request) is True


def test_header_value_doesnt_match_re_object(rf):
    h_name = 'HTTP_X_A'
    matcher = Header(h_name, re.compile(r'^val_.$'))
    request = rf.get('/', **{h_name: 'val_xyz'})
    assert matcher.match(request) is False


def test_header_value_matches_iterable(rf):
    h_name = 'HTTP_X_A'
    matcher = Header(h_name, ['val_x', 'val_y', 'val_z'])
    request = rf.get('/', **{h_name: 'val_y'})
    assert matcher.match(request) is True


def test_header_value_doesnt_match_iterable(rf):
    h_name = 'HTTP_X_A'
    matcher = Header(h_name, ['val_x', 'val_y', 'val_z'])
    request = rf.get('/', **{h_name: 'val_w'})
    assert matcher.match(request) is False


def test_repr():
    assert repr(Header('HTTP_X_A', 'val_x')) == "Header('HTTP_X_A', 'val_x')"
    assert repr(Header('HTTP_X_A', re.compile(r'^val_.$'))) == "Header('HTTP_X_A', re.compile('^val_.$'))"
    assert repr(Header('HTTP_X_A', ['val_x', 'val_y', 'val_z'])) == "Header('HTTP_X_A', ['val_x', 'val_y', 'val_z'])"
