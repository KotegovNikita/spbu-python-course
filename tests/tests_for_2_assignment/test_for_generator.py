import pytest
from functools import reduce

from project.Assignment_2.generator import (
    generate_data,
    pipeline,
    aggregator,
)


@pytest.fixture
def sample_data():
    """Provides a predictable list of integers for testing pipeline logic."""
    return [0, 1, 2, 3, 4]


@pytest.fixture
def empty_data():
    """Provides an empty list for testing edge cases."""
    return []


def test_generate_data_count_type_and_range():
    """
    Tests the `generate_data` function for correct item count, data type, and value range.
    This test is specifically for the random data generator.
    """
    test_count = 100
    test_min_val = -10
    test_max_val = 10

    generator = generate_data(
        count=test_count, min_val=test_min_val, max_val=test_max_val
    )
    result_list = list(generator)

    assert (
        len(result_list) == test_count
    ), f"Expected {test_count} numbers, but got {len(result_list)}"

    all_items_are_valid = all(
        isinstance(num, int) and test_min_val <= num <= test_max_val
        for num in result_list
    )
    assert (
        all_items_are_valid
    ), "Not all generated items are integers or they fall out of the specified range"


def test_pipeline_is_lazy():
    """
    Tests that the pipeline is truly lazy, with operations executing
    only when elements are requested.
    """
    call_counter = [0]

    def spy_operation(stream):
        for item in stream:
            call_counter[0] += 1
            yield item

    source_data = [10, 20, 30]

    processing_pipeline = pipeline(source_data, spy_operation)
    assert (
        call_counter[0] == 0
    ), "Pipeline is not lazy! Operation was called during creation."

    iterator = iter(processing_pipeline)
    next(iterator)
    assert call_counter[0] == 1, "Operation was not called for the first item."

    list(iterator)
    assert call_counter[0] == 3, "Operation was not called for all items."


def test_pipeline_with_zip():
    """
    Tests that the pipeline can process a stream created by `zip`.
    """
    stream1 = [1, 2, 3]
    stream2 = [10, 20, 30]
    zipped_stream = zip(stream1, stream2)
    sum_pairs_op = (map, sum)

    processing_pipeline = pipeline(zipped_stream, sum_pairs_op)
    result = aggregator(processing_pipeline)
    assert result == [11, 22, 33]


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


def test_pipeline_with_builtin_map(sample_data):
    """
    Tests the pipeline using the built-in `map` function to multiply by 10.
    """
    map_operation = (map, lambda x: x * 10)

    processing_pipeline = pipeline(sample_data, map_operation)
    result = aggregator(processing_pipeline)
    assert result == [0, 10, 20, 30, 40]


def test_pipeline_with_builtin_filter(sample_data):
    """Tests the pipeline using the built-in `filter` function to select even numbers."""
    filter_operation = (filter, lambda x: x % 2 == 0)

    processing_pipeline = pipeline(sample_data, filter_operation)
    result = aggregator(processing_pipeline)
    assert result == [0, 2, 4]


def test_pipeline_chained_filter_and_map(sample_data):
    """
    Tests a complex chain: first filter for odd numbers, then square them.
    """
    filter_odd_op = (filter, lambda x: x % 2 != 0)
    square_op = (map, lambda x: x * x)

    processing_pipeline = pipeline(sample_data, filter_odd_op, square_op)
    result = aggregator(processing_pipeline)
    assert result == [1, 9]


def test_pipeline_with_reduce(sample_data):
    """
    Tests how `reduce` can be used on the pipeline's output for aggregation.
    """
    square_op = (map, lambda x: x * x)

    processing_pipeline = pipeline(sample_data, square_op)
    total_sum = reduce(
        lambda accumulator, value: accumulator + value, processing_pipeline, 0
    )
    assert total_sum == 30


def test_pipeline_with_empty_input(empty_data):
    """
    Tests that the pipeline correctly handles an empty input stream.
    """
    square_op = (map, lambda x: x * x)
    add_one_op = (map, lambda x: x + 1)

    processing_pipeline = pipeline(empty_data, square_op, add_one_op)
    result = aggregator(processing_pipeline)
    assert result == []
