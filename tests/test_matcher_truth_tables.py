from operator import and_, or_, xor

import pytest

from header_filter.matchers import Header


def test_not_true_equals_false(rf):
    h_name, h_value = 'HTTP_X_A', 'val_x'
    matcher = ~Header(h_name, h_value)
    request = rf.get('/', **{h_name: h_value})
    assert matcher.match(request) is False


def test_not_false_equals_true(rf):
    matcher = ~Header('HTTP_X_A', 'val_x')
    request = rf.get('/', **{'HTTP_X_B': 'val_y'})
    assert matcher.match(request) is True


@pytest.mark.parametrize('op,result', [(and_, True), (or_, True), (xor, False)], ids=['and', 'or', 'xor'])
def test_true_op_true(op, result, rf):
    h_name_1, h_value_1 = 'HTTP_X_A', 'val_x'
    h_name_2, h_value_2 = 'HTTP_X_B', 'val_y'
    matcher = op(Header(h_name_1, h_value_1), Header(h_name_2, h_value_2))
    request = rf.get('/', **{h_name_1: h_value_1, h_name_2: h_value_2})
    assert matcher.match(request) is result


@pytest.mark.parametrize('op,result', [(and_, False), (or_, True), (xor, True)], ids=['and', 'or', 'xor'])
def test_true_op_false(op, result, rf):
    h_name, h_value = 'HTTP_X_A', 'val_x'
    matcher = op(Header(h_name, h_value), Header('HTTP_X_B', 'val_y'))
    request = rf.get('/', **{h_name: h_value, 'HTTP_X_C': 'val_z'})
    assert matcher.match(request) is result


@pytest.mark.parametrize('op,result', [(and_, False), (or_, True), (xor, True)], ids=['and', 'or', 'xor'])
def test_false_op_true(op, result, rf):
    h_name, h_value = 'HTTP_X_B', 'val_y'
    matcher = op(Header('HTTP_X_A', 'val_x'), Header(h_name, h_value))
    request = rf.get('/', **{h_name: h_value, 'HTTP_X_C': 'val_z'})
    assert matcher.match(request) is result


@pytest.mark.parametrize('op,result', [(and_, False), (or_, False), (xor, False)], ids=['and', 'or', 'xor'])
def test_false_op_false(op, result, rf):
    matcher = Header('HTTP_X_A', 'val_w') | Header('HTTP_X_B', 'val_x')
    request = rf.get('/', **{'HTTP_X_C': 'val_y', 'HTTP_X_D': 'val_z'})
    assert matcher.match(request) is result
