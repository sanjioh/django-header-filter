from header_filter.matchers import Header


def test_not_header_matches(rf):
    matcher = ~Header('HTTP_X_A', 'val_x')
    request = rf.get('/', **{'HTTP_X_B': 'val_y'})
    assert matcher.match(request) is True


def test_not_header_doesnt_match(rf):
    h_name, h_value = 'HTTP_X_A', 'val_x'
    matcher = ~Header(h_name, h_value)
    request = rf.get('/', **{h_name: h_value})
    assert matcher.match(request) is False


def test_double_not(rf):
    h_name, h_value = 'HTTP_X_A', 'val_x'
    matcher = ~~Header(h_name, h_value)
    request = rf.get('/', **{h_name: h_value})
    assert matcher.match(request) is True


def test_not_of_and(rf):
    h_name_1, h_value_1 = 'HTTP_X_A', 'val_x'
    h_name_2, h_value_2 = 'HTTP_X_B', 'val_y'
    matcher = ~(Header(h_name_1, h_value_1) & Header(h_name_2, h_value_2))
    request = rf.get('/', **{h_name_1: h_value_1, h_name_2: h_value_2})
    assert matcher.match(request) is False


def test_not_of_or(rf):
    h_name_1, h_value_1 = 'HTTP_X_A', 'val_x'
    h_name_2, h_value_2 = 'HTTP_X_B', 'val_y'
    matcher = ~(Header(h_name_1, h_value_1) | Header(h_name_2, h_value_2))
    request = rf.get('/', **{h_name_1: h_value_1, h_name_2: h_value_2})
    assert matcher.match(request) is False
