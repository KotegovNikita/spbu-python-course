import pytest
from project.Assignment_3.Decorators import (
    curry_explicit,
    uncurry_explicit,
    Evaluated,
    smart_args,
    Isolated,
)


def f_sum(a, b, c):
    return a + b + c


def f_no_args():
    return 42


def f_one_arg(a):
    return a * 2


EVALUATED_COUNTER = 0


def get_next_value():
    global EVALUATED_COUNTER
    EVALUATED_COUNTER += 1
    return EVALUATED_COUNTER


@pytest.fixture(autouse=True)
def reset_counter():
    global EVALUATED_COUNTER
    EVALUATED_COUNTER = 0


def test_curry_basic():
    curried_f = curry_explicit(f_sum, 3)
    assert curried_f(1)(2)(3) == 6


def test_uncurry_basic():
    curried_f = curry_explicit(f_sum, 3)
    uncurried_f = uncurry_explicit(curried_f, 3)
    assert uncurried_f(1, 2, 3) == 6


def test_arity_zero():
    curried_f = curry_explicit(f_no_args, 0)
    assert curried_f() == 42
    uncurried_f = uncurry_explicit(curried_f, 0)
    assert uncurried_f() == 42


def test_arity_one():
    curried_f = curry_explicit(f_one_arg, 1)
    assert curried_f(10) == 20
    uncurried_f = uncurry_explicit(curried_f, 1)
    assert uncurried_f(10) == 20


def test_negative_arity():
    with pytest.raises(ValueError):
        curry_explicit(f_sum, -1)
    with pytest.raises(ValueError):
        uncurry_explicit(lambda x: x, -1)


def test_curry_wrong_args_count():
    curried_f = curry_explicit(f_sum, 3)
    with pytest.raises(ValueError):
        curried_f(1, 2)
    with pytest.raises(ValueError):
        curried_f()


def test_uncurry_wrong_args_count():
    curried_f = curry_explicit(f_sum, 3)
    uncurried_f = uncurry_explicit(curried_f, 3)
    with pytest.raises(ValueError):
        uncurried_f(1, 2)
    with pytest.raises(ValueError):
        uncurried_f(1, 2, 3, 4)


def test_arbitrary_args_function():
    mock_print = lambda *args, **kwargs: args
    curried_print = curry_explicit(mock_print, 2)
    assert curried_print(1)(2) == (1, 2)
    with pytest.raises(TypeError):
        curried_print(1)(2)(3)


def test_evaluated_basic():
    @smart_args
    def my_func(*, val=Evaluated(get_next_value)):
        return val

    assert my_func() == 1
    assert my_func() == 2
    assert my_func(val=100) == 100
    assert EVALUATED_COUNTER == 2


def test_isolated_basic():
    @smart_args
    def my_func(*, data=Isolated()):
        data.append(4)
        return data

    original_list = [1, 2, 3]
    result = my_func(data=original_list)
    assert result == [1, 2, 3, 4]
    assert original_list == [1, 2, 3]


def test_isolated_nested():
    @smart_args
    def my_func(*, data=Isolated()):
        data[0][0] = 99
        return data

    original_list = [[1], [2]]
    result = my_func(data=original_list)
    assert result == [[99], [2]]
    assert original_list == [[1], [2]]


def test_isolated_requires_argument():
    @smart_args
    def my_func(*, data=Isolated()):
        return data

    with pytest.raises(TypeError):
        my_func()


def test_positional_argument_assertion():
    @smart_args
    def my_func_iso(a, *, data=Isolated()):
        return a, data

    with pytest.raises(AssertionError):
        my_func_iso(1, data=[])

    @smart_args
    def my_func_eval(a, *, val=Evaluated(lambda: 1)):
        return a, val

    with pytest.raises(AssertionError):
        my_func_eval(1)


def test_not_keyword_only_assertion():
    with pytest.raises(AssertionError):

        @smart_args
        def my_func_iso(data=Isolated()):
            pass

    with pytest.raises(AssertionError):

        @smart_args
        def my_func_eval(val=Evaluated(lambda: 1)):
            pass


def test_mixed_arguments():
    @smart_args
    def complex_func(a, *, b=10, c=Evaluated(get_next_value), d=Isolated()):
        d.append(a + b + c)
        return d

    my_list = [100]
    result1 = complex_func(a=5, d=my_list)
    assert result1 == [100, 16]
    assert my_list == [100]

    result2 = complex_func(a=1, b=2, d=my_list)
    assert result2 == [100, 5]
    assert my_list == [100]

    assert EVALUATED_COUNTER == 2
