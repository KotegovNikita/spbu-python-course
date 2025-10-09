from functools import reduce
from typing import Callable, Iterable, Generator, Any, Sequence


def generate_data(new_data: Iterable[Any]) -> Generator:
    """Creates a generator from an iterable.

    This function takes any iterable object and yields its elements one by one,
    effectively turning it into a generator stream.

    Args:
        new_data (Iterable[Any]): An iterable object (e.g., a list, tuple)
            to be used as the data source.

    Yields:
        Generator: An element from the source iterable.
    """
    for i in new_data:
        yield i


def pipeline(source_data: Iterable[Any], *operations: Callable) -> Generator:
    """Applies a sequence of operations to a data stream in a lazy manner.

    This function chains together multiple processing functions (operations).
    Each operation is applied to the output of the previous one. The processing
    is lazy, meaning computations are only performed when an element is
    requested from the final generator.

    Args:
        source_data (Iterable[Any]): The initial data stream, which can be any
            iterable (e.g., a list or another generator).
        *operations (Callable): A variable number of functions to be applied
            sequentially. Each function must accept an iterable as input and
            return an iterable.

    Returns:
        Generator: A generator that will yield the processed data when iterated over.
    """
    stream = source_data
    for op in operations:
        stream = op(stream)
    yield from stream


def square(numbers: Iterable[int]) -> Generator:
    """Yields the square of each number from an iterable.

    This is a generator function that takes an iterable of numbers and yields
    the square of each number one by one.

    Args:
        numbers (Iterable[int]): An iterable of integers.

    Yields:
        Generator: The square of the next number in the sequence.
    """
    for num in numbers:
        yield num * num


def add_one(numbers: Iterable[int]) -> Generator:
    """Yields each number from an iterable incremented by one.

    This is a generator function that takes an iterable of numbers and yields
    each number plus one.

    Args:
        numbers (Iterable[int]): An iterable of integers.

    Yields:
        Generator: The next number in the sequence incremented by one.
    """
    for num in numbers:
        yield num + 1


def aggregator(source_data: Iterable[Any], output_type: Callable = list) -> Sequence:
    """Collects all items from a data stream into a collection.

    This function triggers the execution of a lazy pipeline by iterating over
    the source data stream and storing the results in a specified collection type.

    Args:
        source_data (Iterable[Any]): The data stream (typically the output of a
            pipeline) to be consumed.
        output_type (Callable, optional): The constructor for the desired output
            collection. Defaults to list. Can be set, tuple, etc.

    Returns:
        Sequence: A collection (e.g., a list, tuple, set) containing all the
            processed items from the source data stream.
    """
    return output_type(source_data)
