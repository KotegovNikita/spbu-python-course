import pytest
from functools import reduce
import random

from project.Assignment_2.generator import (
    generate_data,
    pipeline,
    aggregator,
    create_op_adapter,
)


@pytest.fixture(autouse=True)
def fixed_random_seed():
    random.seed(42)


def test_lazy():
    call = False

    def lazy_generate():
        nonlocal call
        call = True
        yield from generate_data(5, 1, 10)

    def times_two(x):
        return x * 2

    map_times_two = create_op_adapter(map, times_two)
    gen = pipeline(lazy_generate(), map_times_two)
    assert call is False
    first = next(gen)
    assert call is True


def test_generate_data():
    data = list(generate_data(10, 1, 5))
    assert len(data) == 10
    assert all(1 <= x <= 5 for x in data)


def test_create_op_map():
    adapter = create_op_adapter(map, lambda x: x * 2)
    data = [1, 2, 3]
    result = list(adapter(data))
    assert result == [2, 4, 6]


def test_create_op_filter():
    adapter = create_op_adapter(filter, lambda x: x > 2)
    data = [1, 2, 3, 4]
    result = list(adapter(data))
    assert result == [3, 4]


def test_create_op_adapter_zip():
    adapter = create_op_adapter(zip, [10, 20, 30])
    data = [1, 2, 3]
    result = list(adapter(data))
    assert result == list(zip(data, [10, 20, 30]))


def test_create_operation_adapter_enumerate():
    adapter = create_op_adapter(enumerate, start=5)
    data = ["a", "b"]
    result = list(adapter(data))
    assert result == list(enumerate(data, start=5))


def test_create_op_adapter_reduce_sum():
    adapter = create_op_adapter(reduce, lambda a, b: a + b)
    data = [1, 2, 3]
    result = list(adapter(data))
    assert result == [6]


def test_create_op_adapter_reduce():
    adapter = create_op_adapter(reduce, lambda a, b: a + b, 5)
    data = [1, 2, 3]
    result = list(adapter(data))
    assert result == [11]


def test_pipeline_single_operation():
    map_double = create_op_adapter(map, lambda x: x * 2)
    data = [1, 2, 3]
    result = list(pipeline(data, map_double))
    assert result == [2, 4, 6]


def test_pipeline_with_reduce():
    reduce_sum = create_op_adapter(reduce, lambda a, b: a + b)
    data = [1, 2, 3, 4]
    result = list(pipeline(data, reduce_sum))
    assert result == [10]


def test_aggregator_list():
    data = [1, 2, 3]
    result = aggregator(data)
    assert type(result) == list
    assert result == data


def test_aggregator_tuple():
    data = [1, 2, 3]
    result = aggregator(data, tuple)
    assert type(result) == tuple
    assert result == tuple(data)


def test_aggregator_set():
    data = [1, 2, 3, 2]
    result = aggregator(data, set)
    assert type(result) == set
    assert result == {1, 2, 3}
