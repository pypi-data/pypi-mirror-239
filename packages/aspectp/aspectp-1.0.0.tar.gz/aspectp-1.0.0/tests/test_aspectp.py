import aspectp
import capturepy
import inspect
import importlib
import math
import pytest
import tests.advice
import tests.lib


@pytest.fixture(autouse=True)
def reload_lib():
    importlib.reload(tests.lib)


TEST_INPUTS = (
    (aspectp.before, tests.advice.add_1_before, 2, 9),
    (aspectp.around, tests.advice.add_1_around, 2, 10),
    (aspectp.after, tests.advice.add_1_after, 2, 5),
)


@pytest.mark.parametrize('weave, advice, value, expected', TEST_INPUTS)
def test_aspect(weave, advice, value, expected):
    assert tests.lib.square(value) == value ** 2

    id = weave(tests.lib.square, advice)
    assert tests.lib.square(value) == expected

    aspectp.remove(tests.lib.square, id)
    assert tests.lib.square(value) == value ** 2


LOG_TEST_INPUTS = (
    (aspectp.before, tests.advice.log_before, 2, 'before arguments: (2,) {}\n'),
    (aspectp.around, tests.advice.log_around, 2, 'around arguments: (2,) {}\naround result: 4\n'),
    (aspectp.after, tests.advice.log_after, 2, 'after result: 4\n'),
)


@pytest.mark.parametrize('weave, advice, value, expected', LOG_TEST_INPUTS)
def test_log_aspect(weave, advice, value, expected):
    with capturepy.Capture() as capture:
        assert tests.lib.square(value) == value ** 2
        assert capture.get() == ''

    id = weave(tests.lib.square, advice)
    with capturepy.Capture() as capture:
        assert tests.lib.square(value) == value ** 2
        assert capture.get() == expected

    aspectp.remove(tests.lib.square, id)
    with capturepy.Capture() as capture:
        assert tests.lib.square(value) == value ** 2
        assert capture.get() == ''


def test_error():
    assert tests.lib.sqrt(1) == 1
    with pytest.raises(ValueError):
        tests.lib.sqrt(-1)

    id = aspectp.error(tests.lib.sqrt, tests.advice.error)
    error = tests.lib.sqrt(-1)
    assert isinstance(error, ValueError)

    aspectp.remove(tests.lib.sqrt, id)
    with pytest.raises(ValueError):
        assert tests.lib.sqrt(-1)
    assert tests.lib.sqrt(1) == 1


TEST_MULTIPLE_ADVICE_INPUTS = (
    (aspectp.before, tests.advice.add_1_before, tests.advice.add_2_before, 2, 25),
    (aspectp.around, tests.advice.add_1_around, tests.advice.add_2_around, 2, 28),
    (aspectp.after, tests.advice.add_1_after, tests.advice.add_2_after, 2, 7),
)


@pytest.mark.parametrize('weave, first_advice, second_advice, value, expected', TEST_MULTIPLE_ADVICE_INPUTS)
def test_multiple_advices(weave, first_advice, second_advice, value, expected):
    assert tests.lib.square(value) == value ** 2

    first_id = weave(tests.lib.square, first_advice)
    second_id = weave(tests.lib.square, second_advice)
    assert tests.lib.square(value) == expected

    aspectp.remove(tests.lib.square)
    assert tests.lib.square(value) == value ** 2


TEST_MULTIPLE_ADVICE_DIFFERENT_POINT_INPUTS = (
    (aspectp.before, aspectp.after, tests.advice.add_1_before, tests.advice.add_2_after, 2, 11),
    (aspectp.after, aspectp.before, tests.advice.add_1_after, tests.advice.add_2_before, 2, 17),
    (aspectp.around, aspectp.before, tests.advice.add_1_around, tests.advice.add_2_before, 2, 26),
)


@pytest.mark.parametrize('first_weave, second_weave, first_advice, second_advice, value, expected', TEST_MULTIPLE_ADVICE_DIFFERENT_POINT_INPUTS)
def test_multiple_advices_different_point(first_weave, second_weave, first_advice, second_advice, value, expected):
    assert tests.lib.square(value) == value ** 2

    first_id = first_weave(tests.lib.square, first_advice)
    second_id = second_weave(tests.lib.square, second_advice)
    assert tests.lib.square(value) == expected

    aspectp.remove(tests.lib.square)
    assert tests.lib.square(value) == value ** 2


def get_order():
    order = tests.lib.Order()
    order.add_item(tests.lib.Item('milk', 1.5, 2))
    order.add_item(tests.lib.Item('bread', 1.0, 3))
    return order


def test_class():
    assert get_order().total() == 6.0

    id = aspectp.after(tests.lib.Order.total, tests.advice.add_1_after)
    assert get_order().total() == 7.0

    aspectp.remove(tests.lib.Order.total, id)
    assert get_order().total() == 6.0


def test_object():
    order = get_order()
    assert order.total() == 6.0

    id = aspectp.after(order.total, tests.advice.add_1_after)
    assert order.total() == 7.0

    aspectp.remove(order.total, id)
    assert order.total() == 6.0


def test_whole_class():
    with capturepy.Capture() as capture:
        id = aspectp.before(tests.lib.Order, tests.advice.log_len_before)
        order = get_order()
        assert capture.get() == 'around arguments: 1 0\naround arguments: 2 0\naround arguments: 2 0\n'
    for attribute in aspectp._get_funcs(order):
        assert hasattr(attribute, '_aspect')
        assert len(attribute._aspect.get(aspectp._AdviceType.BEFORE)) == 1


def test_whole_object():
    with capturepy.Capture() as capture:
        order = get_order()
        id = aspectp.before(order, tests.advice.log_len_before)
        order.add_item(tests.lib.Item('egg', 0.2, 12))
        order.add_item(tests.lib.Item('water', 0.5, 5))
        order.total()
        assert capture.get() == 'around arguments: 1 0\naround arguments: 1 0\naround arguments: 0 0\n'
    for attribute in aspectp._get_funcs(order):
        assert hasattr(attribute, '_aspect')
        assert len(attribute._aspect.get(aspectp._AdviceType.BEFORE)) == 1


def test_whole_module():
    with capturepy.Capture() as capture:
        id = aspectp.before(tests.lib, tests.advice.log_len_before)
        tests.lib.square(2)
        tests.lib.sqrt(2)
        assert capture.get() == 'around arguments: 1 0\naround arguments: 1 0\n'
    for attribute in aspectp._get_funcs(tests.lib):
        assert hasattr(attribute, '_aspect')
        assert len(attribute._aspect.get(aspectp._AdviceType.BEFORE)) == 1


BUILTIN_TEST_INPUTS = (
    (aspectp.before, tests.advice.add_1_before, (2, 2), 9),
    (aspectp.before, tests.advice.add_1_before, (3, 5), 1024),
    (aspectp.before, tests.advice.add_1_before, (1, 4), 16),
    (aspectp.after, tests.advice.add_1_after, (2, 2), 5),
    (aspectp.after, tests.advice.add_1_after, (3, 5), 244),
    (aspectp.after, tests.advice.add_1_after, (1, 4), 2),
)


@pytest.mark.parametrize('weave, advice, args, expected', BUILTIN_TEST_INPUTS)
def test_builtin(weave, advice, args, expected):
    importlib.reload(math)

    base, exponent = args
    assert math.pow(base, exponent) == base ** exponent

    id = weave(math.pow, advice)
    assert math.pow(base, exponent) == expected

    aspectp.remove(math.pow, id)
    assert math.pow(base, exponent) == base ** exponent
