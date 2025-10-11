from functools import reduce
from typing import Callable, Iterable, Generator, Any, Sequence
import random


def generate_data(count: int, min_val: int, max_val: int) -> Generator[int, None, None]:
    """
    Generate a limited number of random integers within a specified range.
    Args:
        count (int): Number of random integers to generate.
        min_val (int): Minimum possible value (inclusive).
        max_val (int): Maximum possible value (inclusive).
    Yields:
        int: Random integers within the specified range, one at a time.
    """
    for _ in range(count):
        yield random.randint(min_val, max_val)


def create_op_adapter(
    func: Callable, *args: Any, **kwargs: Any
) -> Callable[[Iterable[Any]], Generator[Any, None, None]]:
    """
    This adapter standardizes the application of functions such as map, filter,
    zip, enumerate, reduce, or any custom function
    Args:
        func (Callable): The function to adapt
        *args Positional arguments for the `func`.
        **kwargs Keyword arguments for the `func`.
    Returns:
        Callable[[Iterable[Any]], Generator[Any, None, None]]:
        A function that takes an iterable input, applies `func` with given arguments,
    """

    def apply_adapted_op(input_iterable: Iterable[Any]) -> Generator[Any, None, None]:
        """
        Apply the adapted operation to the input iterable and yield results.
        Args:
            input_iterable (Iterable[Any]): Input iterable data to process.
        Yields:
            Processed items as per the adapted function's behavior.
        """
        if func is map:
            yield from map(args[0], input_iterable)
        elif func is filter:
            yield from filter(args[0], input_iterable)
        elif func is zip:
            yield from zip(input_iterable, *args)
        elif func is enumerate:
            yield from enumerate(input_iterable, *args, **kwargs)
        elif func is reduce:
            if args:
                reduction_func = args[0]
            else:
                reduction_func = func

            if len(args) > 1:
                initial = args[1]
            else:
                initial = kwargs.get("initializer", None)

            if initial is not None:
                result = reduce(reduction_func, input_iterable, initial)
            else:
                result = reduce(reduction_func, input_iterable)
            yield result
        else:
            yield from func(input_iterable, *args, **kwargs)

    return apply_adapted_op


def pipeline(
    source_data: Iterable[Any],
    *operations: Callable[[Iterable[Any]], Generator[Any, None, None]]
) -> Generator[Any, None, None]:
    """
    Apply a sequence of operations to the source data
    Args:
        source_data (Iterable[Any]): The initial data stream or iterable.
        *operations (Callable): Functions that take an iterable and yield processed items.
    Yields:
        Any: Processed items after applying all operations in sequence.
    """
    stream = source_data
    for operation in operations:
        stream = operation(stream)
    yield from stream


def aggregator(source_data: Iterable[Any], output_type: Callable = list) -> Sequence:
    """
    Aggregate all items from a source iterable into a collection of specified type
    Args:
        source_data (Iterable[Any]): Iterable data to aggregate.
        output_type (Callable, optional): Constructor for collection type
    Returns:
        Sequence: The aggregated collection
    """
    return output_type(source_data)
