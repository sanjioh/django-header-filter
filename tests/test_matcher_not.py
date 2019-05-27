from header_filter.matchers import Header


def test_not_matcher_supports_bitwise_not(rf):
    h_name, h_value = 'HTTP_X_A', 'val_x'
    matcher = ~~Header(h_name, h_value)
    request = rf.get('/', **{h_name: h_value})
    assert matcher.match(request) is True


def test_not_matcher_supports_bitwise_and(rf):
    h_name_1, h_value_1 = 'HTTP_X_A', 'val_x'
    h_name_2, h_value_2 = 'HTTP_X_B', 'val_y'
    matcher = ~Header(h_name_1, h_value_1) & Header(h_name_2, h_value_2)
    request = rf.get('/', **{h_name_1: h_value_1, h_name_2: h_value_2})
    assert matcher.match(request) is False


def test_not_matcher_supports_bitwise_or(rf):
    h_name_1, h_value_1 = 'HTTP_X_A', 'val_x'
    h_name_2, h_value_2 = 'HTTP_X_B', 'val_y'
    matcher = ~Header(h_name_1, h_value_1) | Header(h_name_2, h_value_2)
    request = rf.get('/', **{h_name_1: h_value_1, h_name_2: h_value_2})
    assert matcher.match(request) is True
