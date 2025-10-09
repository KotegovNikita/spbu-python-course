import pytest
from functools import reduce
from project.Assignment_2.generator import (
    generate_data,
    pipeline,
    square,
    add_one,
    aggregator,
)


@pytest.fixture
def sample_data():
    """Provides a simple list of integers for testing."""
    return [0, 1, 2, 3, 4]


@pytest.fixture
def empty_data():
    """Provides an empty list for testing edge cases."""
    return []


def test_generate_data(sample_data):
    """Tests that `generate_data` correctly creates a generator from a list."""
    data_generator = generate_data(sample_data)
    # Convert the generator to a list to verify its contents
    assert list(data_generator) == sample_data


def test_square_function(sample_data):
    """Tests the correctness of the user-defined `square` function."""
    result = list(square(sample_data))
    assert result == [0, 1, 4, 9, 16]


def test_add_one_function(sample_data):
    """Tests the correctness of the user-defined `add_one` function."""
    result = list(add_one(sample_data))
    assert result == [1, 2, 3, 4, 5]


@pytest.mark.parametrize(
    "collection_type, expected_result",
    [(list, [1, 2, 3]), (tuple, (1, 2, 3)), (set, {1, 2, 3})],
)
def test_aggregator_with_different_types(collection_type, expected_result):
    """Tests that the aggregator correctly collects data into different collection types."""
    source = [1, 2, 3]
    result = aggregator(source, output_type=collection_type)
    assert result == expected_result
    assert isinstance(result, collection_type)


def test_pipeline_with_single_user_operation(sample_data):
    """Tests the pipeline with a single user-defined operation (`square`)."""
    processing_pipeline = pipeline(sample_data, square)
    result = aggregator(processing_pipeline)
    assert result == [0, 1, 4, 9, 16]


def test_pipeline_with_chained_user_operations(sample_data):
    """
    Tests the pipeline with a chain of two user-defined operations:
    first `square`, then `add_one`. The expected result is (x*x) + 1.
    """
    processing_pipeline = pipeline(sample_data, square, add_one)
    result = aggregator(processing_pipeline)
    assert result == [1, 2, 5, 10, 17]


def test_pipeline_with_builtin_map(sample_data):
    """
    Tests the pipeline using the built-in `map` function to multiply by 10.
    The `map` call is wrapped in a lambda to match the expected operation format.
    """
    map_operation = lambda stream: map(lambda x: x * 10, stream)

    processing_pipeline = pipeline(sample_data, map_operation)
    result = aggregator(processing_pipeline)
    assert result == [0, 10, 20, 30, 40]


def test_pipeline_with_builtin_filter(sample_data):
    """Tests the pipeline using the built-in `filter` function to select even numbers."""
    filter_operation = lambda stream: filter(lambda x: x % 2 == 0, stream)

    processing_pipeline = pipeline(sample_data, filter_operation)
    result = aggregator(processing_pipeline)
    assert result == [0, 2, 4]


def test_pipeline_chained_filter_and_map(sample_data):
    """
    Tests a complex chain: first filter for odd numbers, then square them.
    """
    filter_odd = lambda stream: filter(lambda x: x % 2 != 0, stream)

    # In sample_data [0, 1, 2, 3, 4], odd numbers are -> [1, 3]
    # Squaring them -> [1*1, 3*3] -> [1, 9]
    processing_pipeline = pipeline(sample_data, filter_odd, square)
    result = aggregator(processing_pipeline)
    assert result == [1, 9]


def test_pipeline_with_reduce(sample_data):
    """
    Tests how `reduce` can be used on the pipeline's output for aggregation.
    The goal is to sum the squares of all numbers.
    """
    processing_pipeline = pipeline(sample_data, square)

    total_sum = reduce(
        lambda accumulator, value: accumulator + value, processing_pipeline, 0
    )
    assert total_sum == 30


def test_pipeline_with_empty_input(empty_data):
    """
    Tests that the pipeline correctly handles an empty input stream,
    producing an empty result.
    """
    processing_pipeline = pipeline(empty_data, square, add_one)
    result = aggregator(processing_pipeline)
    assert result == []
