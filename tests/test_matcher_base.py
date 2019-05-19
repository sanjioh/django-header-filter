from header_filter.matchers import BaseMatcher


def test_base_never_matches(rf):
    h_name, h_value = 'HTTP_X_A', 'val_x'
    matcher = BaseMatcher()
    request = rf.get('/', **{h_name: h_value})
    assert matcher.match(request) is False
    request = rf.get('/', **{'HTTP_X_B': 'val_y'})
    assert matcher.match(request) is False
