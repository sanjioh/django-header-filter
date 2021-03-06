from header_filter.matchers import Header


def test_and_matcher_supports_bitwise_not(rf):
    h_name_1, h_value_1 = 'HTTP_X_A', 'val_x'
    h_name_2, h_value_2 = 'HTTP_X_B', 'val_y'
    matcher = ~(Header(h_name_1, h_value_1) & Header(h_name_2, h_value_2))
    request = rf.get('/', **{h_name_1: h_value_1, h_name_2: h_value_2})
    assert matcher.match(request) is False


def test_and_matcher_supports_bitwise_and(rf):
    h_name_1, h_value_1 = 'HTTP_X_A', 'val_x'
    h_name_2, h_value_2 = 'HTTP_X_B', 'val_y'
    h_name_3, h_value_3 = 'HTTP_X_C', 'val_z'
    matcher = (Header(h_name_1, h_value_1) & Header(h_name_2, h_value_2)) & Header(h_name_3, h_value_3)
    request = rf.get('/', **{h_name_1: h_value_1, h_name_2: h_value_2, h_name_3: h_value_3})
    assert matcher.match(request) is True


def test_and_matcher_supports_bitwise_or(rf):
    h_name_1, h_value_1 = 'HTTP_X_A', 'val_x'
    h_name_2, h_value_2 = 'HTTP_X_B', 'val_y'
    h_name_3, h_value_3 = 'HTTP_X_C', 'val_z'
    matcher = (Header(h_name_1, h_value_1) & Header(h_name_2, h_value_2)) | Header(h_name_3, h_value_3)
    request = rf.get('/', **{h_name_1: h_value_1, h_name_2: h_value_2, h_name_3: h_value_3})
    assert matcher.match(request) is True


def test_and_matcher_supports_bitwise_xor(rf):
    h_name_1, h_value_1 = 'HTTP_X_A', 'val_x'
    h_name_2, h_value_2 = 'HTTP_X_B', 'val_y'
    h_name_3, h_value_3 = 'HTTP_X_C', 'val_z'
    matcher = (Header(h_name_1, h_value_1) & Header(h_name_2, h_value_2)) ^ Header(h_name_3, h_value_3)
    request = rf.get('/', **{h_name_1: h_value_1, h_name_2: h_value_2, h_name_3: h_value_3})
    assert matcher.match(request) is False


def test_repr():
    assert (
        repr(Header('HTTP_X_A', 'val_x') & Header('HTTP_X_B', 'val_y'))
        == "(Header('HTTP_X_A', 'val_x') & Header('HTTP_X_B', 'val_y'))"
    )
