from header_filter.matchers import HeaderName


def test_header_name_matches(rf):
    h_name = 'HTTP_X_A'
    matcher = HeaderName(h_name)
    request = rf.get('/', **{h_name: 'val_x'})
    assert matcher.match(request) is True


def test_header_name_doesnt_match(rf):
    matcher = HeaderName('HTTP_X_A')
    request = rf.get('/', **{'HTTP_X_B': 'val_x'})
    assert matcher.match(request) is False
