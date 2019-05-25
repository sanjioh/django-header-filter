from header_filter.matchers import Header


def test_true_or_true_equals_true(rf):
    h_name_1, h_value_1 = 'HTTP_X_A', 'val_x'
    h_name_2, h_value_2 = 'HTTP_X_B', 'val_y'
    matcher = Header(h_name_1, h_value_1) | Header(h_name_2, h_value_2)
    request = rf.get('/', **{h_name_1: h_value_1, h_name_2: h_value_2})
    assert matcher.match(request) is True


def test_true_or_false_equals_true(rf):
    h_name, h_value = 'HTTP_X_A', 'val_x'
    matcher = Header(h_name, h_value) | Header('HTTP_X_B', 'val_y')
    request = rf.get('/', **{h_name: h_value, 'HTTP_X_C': 'val_z'})
    assert matcher.match(request) is True


def test_false_or_true_equals_true(rf):
    h_name, h_value = 'HTTP_X_B', 'val_y'
    matcher = Header('HTTP_X_A', 'val_x') | Header(h_name, h_value)
    request = rf.get('/', **{h_name: h_value, 'HTTP_X_C': 'val_z'})
    assert matcher.match(request) is True


def test_false_or_false_equals_false(rf):
    matcher = Header('HTTP_X_A', 'val_w') | Header('HTTP_X_B', 'val_x')
    request = rf.get('/', **{'HTTP_X_C': 'val_y', 'HTTP_X_D': 'val_z'})
    assert matcher.match(request) is False


def test_or_followed_by_or(rf):
    h_name_1, h_value_1 = 'HTTP_X_A', 'val_x'
    h_name_2, h_value_2 = 'HTTP_X_B', 'val_y'
    h_name_3, h_value_3 = 'HTTP_X_C', 'val_z'
    matcher = Header(h_name_1, h_value_1) | Header(h_name_2, h_value_2) | Header(h_name_3, h_value_3)
    request = rf.get('/', **{h_name_1: h_value_1, h_name_2: h_value_2, h_name_3: h_value_3})
    assert matcher.match(request) is True


def test_or_followed_by_and(rf):
    h_name_1, h_value_1 = 'HTTP_X_A', 'val_x'
    h_name_2, h_value_2 = 'HTTP_X_B', 'val_y'
    h_name_3, h_value_3 = 'HTTP_X_C', 'val_z'
    matcher = (Header(h_name_1, h_value_1) | Header(h_name_2, h_value_2)) & Header(h_name_3, h_value_3)
    request = rf.get('/', **{h_name_1: h_value_1, h_name_2: h_value_2, h_name_3: h_value_3})
    assert matcher.match(request) is True


def test_or_of_not(rf):
    h_name_1, h_value_1 = 'HTTP_X_A', 'val_x'
    h_name_2, h_value_2 = 'HTTP_X_B', 'val_y'
    matcher = ~Header(h_name_1, h_value_1) | Header(h_name_2, h_value_2)
    request = rf.get('/', **{h_name_1: h_value_1, h_name_2: h_value_2})
    assert matcher.match(request) is True
