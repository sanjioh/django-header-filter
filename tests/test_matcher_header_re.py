from header_filter.matchers import HeaderRegexp


def test_header_re_name_and_value_match(rf):
    matcher = HeaderRegexp(r'^HTTP_X_A.*$', r'^val_.$')
    request = rf.get('/', **{'HTTP_X_A_XYZ': 'val_x'})
    assert matcher.match(request) is True


def test_header_re_name_doesnt_match(rf):
    matcher = HeaderRegexp(r'^HTTP_X_A.*$', r'^val_.$')
    request = rf.get('/', **{'HTTP_X_B_XYZ': 'val_x'})
    assert matcher.match(request) is False


def test_header_re_value_doesnt_match(rf):
    matcher = HeaderRegexp(r'^HTTP_X_A.*$', r'^val_.$')
    request = rf.get('/', **{'HTTP_X_A_XYZ': 'val_'})
    assert matcher.match(request) is False


def test_header_re_name_and_value_dont_match(rf):
    matcher = HeaderRegexp(r'^HTTP_X_A.*$', r'^val_.$')
    request = rf.get('/', **{'HTTP_X_B_XYZ': 'val_'})
    assert matcher.match(request) is False
