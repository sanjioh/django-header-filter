from header_filter.actions import Enforce, Forbid
from header_filter.matchers import Header


def test_enforce_allow(rf):
    h_name, h_value = 'HTTP_X_A', 'val_x'
    matcher = Header(h_name, h_value)
    action = Enforce(matcher)
    request = rf.get('/', **{h_name: h_value})
    assert action.allow(request) is True


def test_enforce_deny(rf):
    matcher = Header('HTTP_X_A', 'val_x')
    action = Enforce(matcher)
    request = rf.get('/', **{'HTTP_X_B': 'val_y'})
    assert action.allow(request) is False


def test_forbid_allow(rf):
    h_name, h_value = 'HTTP_X_A', 'val_x'
    matcher = Header(h_name, h_value)
    action = Forbid(matcher)
    request = rf.get('/', **{h_name: h_value})
    assert action.allow(request) is False


def test_forbid_deny(rf):
    matcher = Header('HTTP_X_A', 'val_x')
    action = Forbid(matcher)
    request = rf.get('/', **{'HTTP_X_B': 'val_y'})
    assert action.allow(request) is True
